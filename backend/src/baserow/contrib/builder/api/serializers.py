from typing import List

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from baserow.api.applications.serializers import ApplicationSerializer
from baserow.contrib.builder.api.pages.serializers import PageSerializer
from baserow.contrib.builder.models import Builder
from baserow.contrib.builder.operations import ListPagesBuilderOperationType
from baserow.contrib.builder.theme.registries import theme_component_registry
from baserow.core.handler import CoreHandler


class BuilderSerializer(ApplicationSerializer):
    pages = serializers.SerializerMethodField(
        help_text="This field is specific to the `builder` application and contains "
        "an array of pages that are in the builder."
    )
    theme = serializers.SerializerMethodField(
        help_text="This field is specific to the `builder` application and contains "
        "the theme settings."
    )

    class Meta(ApplicationSerializer.Meta):
        ref_name = "BuilderApplication"
        fields = ApplicationSerializer.Meta.fields + ("pages", "theme")

    @extend_schema_field(PageSerializer(many=True))
    def get_pages(self, instance: Builder) -> List:
        """
        Because the instance doesn't know at this point it is a Builder we have to
        select the related pages this way.

        :param instance: The builder application instance.
        :return: A list of serialized pages that belong to this instance.
        """

        pages = instance.page_set.all()

        user = self.context.get("user")
        request = self.context.get("request")

        if user is None and hasattr(request, "user"):
            user = request.user

        if user:
            pages = CoreHandler().filter_queryset(
                user,
                ListPagesBuilderOperationType.type,
                pages,
                workspace=instance.workspace,
                context=instance,
                allow_if_template=True,
            )

        return PageSerializer(pages, many=True).data

    def get_theme(self, instance):
        theme = {}

        for theme_component in theme_component_registry.get_all():
            serializer_class = theme_component.get_serializer_class()
            serializer = serializer_class(
                getattr(instance, theme_component.related_name_in_builder_model),
                source=theme_component.related_name_in_builder_model,
            )
            theme.update(**serializer.data)

        return theme
