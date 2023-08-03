from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

import pytz
from celery.exceptions import SoftTimeLimitExceeded
from celery.schedules import crontab
from celery_singleton import DuplicateTaskError, Singleton
from loguru import logger

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

        # Send all the notifications if less or equal to the limit.
        # Otherwise, send just the updated unread count and let the user fetch the
        # new notifications.
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


@app.task(bind=True, queue="export")
def beat_send_instant_notifications_summary_by_email(self):
    """
    This tasks send the emails to users that have set the notification setting
    to instant. Since this task will run every minute by default we want to
    avoid to pile up tasks doing the same thing and potentially sending the same
    email multiple times.
    """

    try:
        singleton_send_instant_notifications_summary_by_email.delay()
    except DuplicateTaskError:
        logger.error(
            "Cannot run `send_instant_notifications_email_to_users` "
            "more than once at the same time."
        )


@app.task(
    base=Singleton,
    bind=True,
    queue="export",
    raise_on_duplicate=True,
    lock_expiry=60 * 5,
)
def singleton_send_instant_notifications_summary_by_email(self):
    send_instant_notifications_email_to_users()


def send_instant_notifications_email_to_users():
    from .handler import NotificationHandler

    notifications_frequency = (
        UserProfile.EmailNotificationFrequencyOptions.INSTANT.value
    )
    max_emails = settings.EMAIL_NOTIFICATIONS_LIMIT_PER_TASK[notifications_frequency]

    return (
        NotificationHandler.send_new_notifications_to_users_matching_filters_by_email(
            Q(profile__email_notification_frequency=notifications_frequency),
            max_emails,
        )
    )


def send_daily_notifications_email_to_users(now: Optional[datetime] = None):
    from .handler import NotificationHandler as handler

    if now is None:
        now = timezone.now()

    hour_of_day = settings.EMAIL_NOTIFICATIONS_DAILY_HOUR_OF_DAY
    timezones_to_send_notifications = [
        tz
        for tz in pytz.all_timezones
        if now.astimezone(pytz.timezone(tz)).hour == hour_of_day
    ]
    logger.debug(
        "Timezones where the hour of the day match settings: %s"
        % "\n - ".join(timezones_to_send_notifications),
    )
    logger.debug(f"Hour of the day to send daily notifications: {hour_of_day}")
    localized_now = now.astimezone(pytz.timezone(timezones_to_send_notifications[0]))
    logger.debug(f"Now: {now} - localized now: {localized_now}")

    notifications_frequency = UserProfile.EmailNotificationFrequencyOptions.DAILY.value
    max_emails = settings.EMAIL_NOTIFICATIONS_LIMIT_PER_TASK[notifications_frequency]

    return handler.send_new_notifications_to_users_matching_filters_by_email(
        Q(
            profile__email_notification_frequency=notifications_frequency,
            profile__timezone__in=timezones_to_send_notifications,
        )
        & ~Q(
            profile__last_notifications_email_sent_at__gt=now - timedelta(hours=12),
        ),
        max_emails,
    )


def send_weekly_notifications_email_to_users(now: Optional[datetime] = None):
    from .handler import NotificationHandler as handler

    if now is None:
        now = timezone.now()

    hour_of_day = settings.EMAIL_NOTIFICATIONS_DAILY_HOUR_OF_DAY
    day_of_week = settings.EMAIL_NOTIFICATIONS_WEEKLY_DAY_OF_WEEK
    timezones_to_send_notifications = [
        tz
        for tz in pytz.all_timezones
        if now.astimezone(pytz.timezone(tz)).hour == hour_of_day
        and now.astimezone(pytz.timezone(tz)).weekday() == day_of_week
    ]
    logger.debug(
        "Timezones where the day of the week and the hour of the day match settings: %s"
        % "\n - ".join(timezones_to_send_notifications or ["None"]),
    )
    logger.debug(f"Hour of the day to send daily notifications: {hour_of_day}")
    logger.debug(f"Day of the week to send weekly notifications: {day_of_week}")
    if timezones_to_send_notifications:
        localized_now = now.astimezone(
            pytz.timezone(timezones_to_send_notifications[0])
        )
        logger.debug(f"Now: {now} - localized now: {localized_now}")
    else:
        logger.debug(f"Now: {now} - No timezones match the settings")

    notifications_frequency = UserProfile.EmailNotificationFrequencyOptions.WEEKLY.value
    max_emails = settings.EMAIL_NOTIFICATIONS_LIMIT_PER_TASK[notifications_frequency]

    return handler.send_new_notifications_to_users_matching_filters_by_email(
        Q(
            profile__email_notification_frequency=notifications_frequency,
            profile__timezone__in=timezones_to_send_notifications,
        )
        & ~Q(
            profile__last_notifications_email_sent_at__gt=now - timedelta(days=4),
        ),
        max_emails,
    )


@app.task(
    bind=True,
    queue="export",
    autoretry_for=(SoftTimeLimitExceeded,),
)
def send_daily_and_weekly_notifications_summary_by_email(self, now=None):
    """
    This task will send a summary of the daily and weekly notifications to users
    that have set the notification setting to daily or weekly. This task will
    run every hour and the report will be sent at the time define in the
    settings according to the user timezone.
    """

    daily_result = send_daily_notifications_email_to_users(now)
    weekly_result = send_weekly_notifications_email_to_users(now)

    if (
        daily_result.remaining_users_to_notify_count > 0
        or weekly_result.remaining_users_to_notify_count > 0
    ):
        logger.error(
            "The maximum number of email of notifications was reached.\n"
            f"Daily sent: {len(daily_result.users_with_notifications)}.\n"
            f"Daily remaining: {daily_result.remaining_users_to_notify_count}.\n"
            f"Weekly sent: {len(weekly_result.users_with_notifications)}.\n"
            f"Weekly reamaining: {weekly_result.remaining_users_to_notify_count}.\n"
        )

        # Retry the task later if we reached the limit of emails to send.
        # Use the same 'now' as argument to continue from where we left off.
        auto_retry_after_seconds = (
            settings.EMAIL_NOTIFICATIONS_AUTO_RETRY_IF_LIMIT_REACHED_AFTER
        )
        if auto_retry_after_seconds:
            raise self.retry(args=[now], countdown=auto_retry_after_seconds)


@app.on_after_finalize.connect
def setup_periodic_action_tasks(sender, **kwargs):
    sender.add_periodic_task(
        settings.EMAIL_NOTIFICATIONS_INSTANT_CRONTAB,
        beat_send_instant_notifications_summary_by_email.s(),
    )
    sender.add_periodic_task(
        crontab(0, "*", "*", "*", "*"),
        send_daily_and_weekly_notifications_summary_by_email.s(),
    )
