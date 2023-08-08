from abc import ABC
from typing import Type, TypeVar

from django.db.models import QuerySet

from baserow.core.registry import (
    CustomFieldsInstanceMixin,
    ImportExportMixin,
    Instance,
    Registry,
)

from .models import ThemeComponent
from .types import ThemeComponentSubClass


class ThemeComponentType(
    Instance,
    ImportExportMixin[ThemeComponent],
    CustomFieldsInstanceMixin,
    ABC,
):
    """
    A theme component type can be used to add additional theme properties to a
    builder application.
    """

    model_class: Type[ThemeComponentSubClass]
    """
    Deliberately not using the `ModelInstanceMixin` because the models are not
    polymorphic.
    """

    @property
    def related_name_in_builder_model(self) -> str:
        """
        This is the related name of the model, which automatically get a relationship
        if the `model_class` extends the abstract `ThemeComponent` model.
        """

        return self.model_class.__name__.lower()


ThemeComponentTypeSubClass = TypeVar(
    "ThemeComponentTypeSubClass", bound=ThemeComponentType
)


class ThemeComponentRegistry(
    Registry[ThemeComponentTypeSubClass],
):
    """
    Contains all registered theme components.
    """

    name = "theme_component"

    def enhance_list_builder_queryset(self, queryset: QuerySet) -> QuerySet:
        """
        Enhances the list builder application queryset by applying a `select_related`
        for of every registered theme component. This is needed to join all the
        related theme data in the query to avoid N queries.

        :param queryset: The queryset that lists the builder applications.
        :return: The enhanced queryset.
        """

        for theme_component in self.get_all():
            related_name = theme_component.related_name_in_builder_model
            queryset = queryset.select_related(related_name)
        return queryset


theme_component_registry = ThemeComponentRegistry()
