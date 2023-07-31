from django.core.management.base import BaseCommand
from django.db.models import Q

from loguru import logger

from baserow.core.models import UserProfile
from baserow.core.notifications.handler import NotificationHandler


class Command(BaseCommand):
    help = "Sends email notifications to users with the provided user setting or the provided user id."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "-f",
            "--frequency",
            type=str,
            choices=[x.value for x in UserProfile.EmailNotificationFrequencyOptions],
            help="The user frequency setting of email notifications to send.",
        )
        parser.add_argument(
            "-l",
            "--limit",
            type=int,
            default=None,
            help="The maximum number of emails to send.",
        )
        parser.add_argument(
            "-uid",
            "--user-id",
            type=int,
            default=None,
            help="The id of the user to send the email notifications to.",
        )

    def handle(self, *args, **options):
        frequency = options["frequency"]
        max_emails = options["limit"]
        user_id = options["user_id"]

        if user_id is not None and not frequency:
            result = (
                NotificationHandler.send_email_notifications_to_users_matching_filters(
                    Q(id=user_id), max_emails=max_emails
                )
            )
            logger.info(
                f"Sent {result.emails_sent} email notifications to user with user_id {user_id}"
            )
        elif frequency is not None:
            result = (
                NotificationHandler.send_email_notifications_to_users_with_frequency(
                    frequency, max_emails=max_emails
                )
            )
            logger.info(
                f"Sent {result.emails_sent} email notifications to users "
                f"with the frequency set to {frequency}."
            )
        else:
            raise ValueError(
                "Either the frequency or the user id must be provided, but not both."
            )
