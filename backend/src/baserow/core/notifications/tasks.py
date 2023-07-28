from collections import defaultdict
from datetime import timedelta

from django.db import transaction

from celery.exceptions import SoftTimeLimitExceeded
from celery.schedules import crontab

from baserow.api.notifications.serializers import NotificationRecipientSerializer
from baserow.config.celery import app
from baserow.core.models import UserProfile
from baserow.ws.tasks import broadcast_to_users


@app.task(bind=True)
def send_queued_notifications_to_users(self):
    from .models import NotificationRecipient

    with transaction.atomic():
        queued_notificationrecipients = (
            NotificationRecipient.objects.filter(queued=True)
            .select_related("notification", "notification__sender")
            .order_by("recipient_id", "-created_on")
            .select_for_update(of=("notification",), skip_locked=True)
        )

        notifications_grouped_by_user = defaultdict(list)
        notifications_count_per_user_and_workspace = defaultdict(
            lambda: defaultdict(int)
        )
        for notification_recipient in queued_notificationrecipients:
            user_id = notification_recipient.recipient_id
            notifications_grouped_by_user[user_id].append(notification_recipient)
            notifications_count_per_user_and_workspace[user_id][
                notification_recipient.notification.workspace_id
            ] += 1

        if not notifications_grouped_by_user:
            return

        def broadcast_all_notifications_at_once_to_user(
            notification_batch_limit=20,
        ):
            for user_id, notifications in notifications_grouped_by_user.items():
                if len(notifications) <= notification_batch_limit:
                    broadcast_to_users.apply(
                        (
                            [user_id],
                            {
                                "type": "notifications_created",
                                "notifications": NotificationRecipientSerializer(
                                    notifications, many=True
                                ).data,
                            },
                        )
                    )
                else:
                    per_workspace_added_count = [
                        {"workspace_id": k, "count": v}
                        for k, v in notifications_count_per_user_and_workspace[
                            user_id
                        ].items()
                    ]
                    broadcast_to_users.apply(
                        (
                            [user_id],
                            {
                                "type": "notifications_fetch_required",
                                "notifications_added": per_workspace_added_count,
                            },
                        )
                    )

        transaction.on_commit(broadcast_all_notifications_at_once_to_user)

        queued_notificationrecipients.update(queued=False)


def send_email_notifications_to_users_with_frequency(frequency):
    from .handler import NotificationHandler

    NotificationHandler.send_email_notifications_to_users_with_frequency(frequency)


@app.task(bind=True, queue="export", soft_time_limit=50)
def send_instant_notifications_by_email_to_users(self):
    """
    This tasks send the emails to users that have set the notification setting
    to immediate. This task will run every minute and with a soft time limit
    set to 50 seconds we should
    """

    send_email_notifications_to_users_with_frequency(
        UserProfile.EmailNotificationFrequencyOptions.INSTANT.value
    )


@app.task(
    bind=True,
    queue="export",
    autoretry_for=(SoftTimeLimitExceeded,),
    retry_backoff=10,
    max_retries=5,
)
def send_daily_notification_by_email_to_users(self):
    """
    This tasks send the emails to users that have set the notification setting
    to daily. Since this task is scheduled once a week and we cannot know in
    advance how long this task will take to complete, we catch the
    SoftTimeLimitExceeded to reschedule the job and continue later.
    """

    send_email_notifications_to_users_with_frequency(
        UserProfile.EmailNotificationFrequencyOptions.DAILY.value
    )


@app.task(
    bind=True,
    queue="export",
    autoretry_for=(SoftTimeLimitExceeded,),
    retry_backoff=10,
    max_retries=10,
)
def send_weekly_notifications_by_email_to_users(self):
    """
    This tasks send the emails to users that have set the notification setting
    to weekly. Since this task is scheduled once a week and we cannot know in
    advance how long this task will take to complete, we catch the
    SoftTimeLimitExceeded to reschedule the job and continue later.
    """

    send_email_notifications_to_users_with_frequency(
        UserProfile.EmailNotificationFrequencyOptions.WEEKLY.value
    )


@app.on_after_finalize.connect
def setup_periodic_action_tasks(sender, **kwargs):
    sender.add_periodic_task(
        timedelta(seconds=60),
        send_instant_notifications_by_email_to_users.s(),
    )
    sender.add_periodic_task(
        crontab(hour=0, minute=0),
        send_daily_notification_by_email_to_users.s(),
    )
    sender.add_periodic_task(
        crontab(hour=0, minute=0, day_of_week=1),
        send_weekly_notifications_by_email_to_users.s(),
    )
