from typing import Any, Dict, List

from baserow.contrib.builder.elements.exceptions import ElementDoesNotExist
from baserow.contrib.builder.elements.models import Element
from baserow.contrib.builder.elements.registries import (
    ElementType,
    element_type_registry,
)
from baserow.contrib.builder.page.models import Page
from baserow.core.utils import extract_allowed


class ElementHandler:
    def get_element(self, element_id: int) -> Element:
        try:
            element = Element.objects.select_related(
                "page", "page__builder", "page__builder__group"
            ).get(id=element_id)
        except Element.DoesNotExist:
            raise ElementDoesNotExist()

        return element

    def get_elements(self, page: Page) -> List[Element]:
        return Element.objects.filter(page=page)

    def create_element(
        self, element_type: ElementType, page: Page, **kwargs
    ) -> Element:
        model_class = element_type.model_class

        last_order = model_class.get_last_order(page)
        element = model_class(page=page, order=last_order, **kwargs)
        element.save()

        return element

    def delete_element(self, element: Element):
        element.delete()

    def update_element(self, element: Element, values: Dict[str, Any]):

        shared_allowed_fields = ["config"]

        element_type = element_type_registry.get_by_model(element)

        allowed_updates = extract_allowed(
            values, shared_allowed_fields + element_type.allowed_fields
        )

        for key, value in allowed_updates.items():
            setattr(element, key, value)

        element.save()

        return element

    def order_elements(self, page, newOrder: List[int]):
        all_elements = Element.objects.filter(page=page)

        full_order = Element.order_objects(all_elements, newOrder)

        return full_order
