from django.core.management.base import BaseCommand

from loguru import logger

from baserow.core.models import UserProfile
from baserow.core.notifications.exceptions import EmailNotificationsLimitReached
from baserow.core.notifications.handler import NotificationHandler


class Command(BaseCommand):
    help = "Sends email notifications to users."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--frequency",
            type=str,
            default=UserProfile.EmailNotificationFrequencyOptions.INSTANT,
            help="The frequency of email notifications to send.",
        )
        parser.add_argument(
            "--max_emails",
            type=int,
            default=None,
            help="The maximum number of emails to send.",
        )

    def handle(self, *args, **options):
        frequency = options["frequency"]
        max_emails = options["max_emails"]
        logger.info(f"Sending email notifications with frequency {frequency}.")

        try:
            emails_sent = (
                NotificationHandler.send_email_notifications_to_users_with_frequency(
                    frequency, max_emails=max_emails
                )
            )
            logger.info(
                f"Sent {emails_sent} email notifications to users "
                f"with the frequency set to {frequency}."
            )
        except EmailNotificationsLimitReached:
            logger.info(
                f"The maximum number of {max_emails} email notifications has been reached "
                f"for users with the frequency set to {frequency}."
            )
