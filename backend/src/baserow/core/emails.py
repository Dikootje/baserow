import re

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext as _

from baserow.core.notifications.registries import notification_type_registry


class BaseEmailMessage(EmailMultiAlternatives):
    """
    The base email message class can be used to create reusable email classes for
    each email. The template_name is rendered to a string and attached as html
    alternative. This content is automatically converted to plain text. The get_context
    method can be extended to add additional context variables while rendering the
    template.

    Example:
        class TestEmail(BaseEmailMessage):
            subject = 'Example subject'
            template_name = 'baserow/core/example.html'

        email = TestEmail(['test@localhost'])
        email.send()
    """

    subject = None
    template_name = None

    def __init__(self, to, from_email=None):
        if not from_email:
            from_email = self.get_from_email()

        subject = self.get_subject()
        template_name = self.get_template_name()
        context = self.get_context()
        html_content = render_to_string(template_name, context)

        text_content = self._get_plain_text_from_html(html_content)

        super().__init__(
            subject=subject, body=text_content, from_email=from_email, to=to
        )
        self.attach_alternative(html_content, "text/html")

    @staticmethod
    def _get_plain_text_from_html(html_content):
        body_start_index = html_content.index("<body")
        body_end_index = html_content.index("</body>")
        body_with_no_tags = strip_tags(html_content[body_start_index:body_end_index])
        body_with_collapsed_spaces = re.compile(r" +").sub(" ", body_with_no_tags)
        body_without_blank_lines = re.compile(r"\n ").sub(
            "\n", body_with_collapsed_spaces
        )
        body_with_collapsed_newlines = re.compile(r"\n+").sub(
            "\n", body_without_blank_lines
        )
        return body_with_collapsed_newlines

    def get_context(self):
        return {
            "public_backend_hostname": settings.PUBLIC_BACKEND_HOSTNAME,
            "public_backend_url": settings.PUBLIC_BACKEND_URL,
            "public_web_frontend_hostname": settings.PUBLIC_WEB_FRONTEND_HOSTNAME,
            "public_web_frontend_url": settings.PUBLIC_WEB_FRONTEND_URL,
        }

    def get_from_email(self):
        return settings.FROM_EMAIL

    def get_subject(self):
        if not self.subject:
            raise NotImplementedError("The subject must be implement.")
        return self.subject

    def get_template_name(self):
        if not self.template_name:
            raise NotImplementedError("The template_name must be implement.")
        return self.template_name

    def send(self, fail_silently=False):
        s = super()
        transaction.on_commit(lambda: s.send(fail_silently))


class WorkspaceInvitationEmail(BaseEmailMessage):
    template_name = "baserow/core/workspace_invitation.html"

    def __init__(self, invitation, public_accept_url, *args, **kwargs):
        self.public_accept_url = public_accept_url
        self.invitation = invitation
        super().__init__(*args, **kwargs)

    def get_subject(self):
        return _(
            "%(by)s invited you to %(workspace_name)s - Baserow",
        ) % {
            "by": self.invitation.invited_by.first_name,
            "workspace_name": self.invitation.workspace.name,
        }

    def get_context(self):
        context = super().get_context()
        context.update(
            invitation=self.invitation, public_accept_url=self.public_accept_url
        )
        return context


class NotificationsSummaryEmail(BaseEmailMessage):
    template_name = "baserow/core/notifications_summary.html"
    MAX_NOTIFICATIONS_PER_EMAIL = 10

    def __init__(self, to, notifications, *args, **kwargs):
        limit = self.MAX_NOTIFICATIONS_PER_EMAIL
        self.notifications = notifications[:limit]
        self.total_count = len(notifications)
        self.unlisted_new = (
            len(notifications) - limit if len(notifications) > limit else None
        )
        super().__init__(to=to, *args, **kwargs)

    def get_subject(self):
        count = len(self.notifications)
        return _("You have %(count)d new notifications - Baserow") % {"count": count}

    def get_context(self):
        context = super().get_context()
        rendered_notifications = []
        for notification in self.notifications:
            notification_type = notification_type_registry.get(notification.type)
            rendered_notifications.append(
                {
                    "title": notification_type.render_title(notification, context),
                    "description": notification_type.render_description(
                        notification, context
                    ),
                }
            )
        context.update(
            notifications=rendered_notifications,
            total_count=self.total_count,
            unlisted_new=self.unlisted_new,
        )
        return context
