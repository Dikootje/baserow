from .models import DefaultThemeComponent
from .registries import ThemeComponentType

default_theme_component_fields = [
    "primary_color",
    "secondary_color",
    "heading_1_font_size",
    "heading_1_color",
    "heading_2_font_size",
    "heading_2_color",
    "heading_3_font_size",
    "heading_3_color",
    "button_background_color",
    "button_font_color",
    "button_font_size",
    "button_border_radius",
    "button_border_size",
    "button_border_color",
    "button_horizontal_padding",
    "button_vertical_padding",
]


class DefaultThemeComponentType(ThemeComponentType):
    type = "default"
    model_class = DefaultThemeComponent
    allowed_fields = default_theme_component_fields
    serializer_field_names = default_theme_component_fields

    def export_serialized(self, instance):
        """@TODO implement this method."""

    def import_serialized(self, parent, serialized_values, id_mapping):
        """@TODO implement this method."""
