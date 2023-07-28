from abc import ABCMeta, abstractmethod
from typing import Optional

from baserow.core.exceptions import (
    InstanceTypeAlreadyRegistered,
    InstanceTypeDoesNotExist,
)
from baserow.core.registry import (
    CustomFieldsRegistryMixin,
    Instance,
    MapAPIExceptionsInstanceMixin,
    ModelRegistryMixin,
    Registry,
)

from .models import Notification


class NotificationType(MapAPIExceptionsInstanceMixin, Instance):
    model_class = Notification
    include_in_notifications_email = False


class EmailRendererNotificationTypeMixin(metaclass=ABCMeta):
    """
    A mixin for notification types that can be sent by email, which provides the
    methods needed to render a title and an optional description in the email message.
    """

    include_in_notifications_email = True

    @classmethod
    @abstractmethod
    def render_title(cls, notification, context) -> str:
        """
        Renders the translatable string for the title of the notification.
        """

    @classmethod
    @abstractmethod
    def render_description(cls, notification, context) -> Optional[str]:
        """
        Renders the translatable string for the description of the notification.
        """


class NotificationTypeDoesNotExist(InstanceTypeDoesNotExist):
    """Raised when a notification type with a given identifier does not exist."""


class NotificationTypeAlreadyRegistered(InstanceTypeAlreadyRegistered):
    """Raised when a notification type is already registered."""


class NotificationTypeRegistry(
    CustomFieldsRegistryMixin,
    ModelRegistryMixin[Notification, NotificationType],
    Registry[NotificationType],
):
    """
    The registry that holds all the available job types.
    """

    name = "notification_type"

    does_not_exist_exception_class = NotificationTypeDoesNotExist
    already_registered_exception_class = NotificationTypeAlreadyRegistered


notification_type_registry: NotificationTypeRegistry = NotificationTypeRegistry()
