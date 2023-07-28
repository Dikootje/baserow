from .models import Notification


class NotificationDoesNotExist(Notification.DoesNotExist):
    pass


class EmailNotificationsLimitReached(Exception):
    pass
