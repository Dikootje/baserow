from django.db import models

from baserow.core.fields import AutoOneToOneField


class ThemeComponent(models.Model):
    builder = AutoOneToOneField(
        "builder.Builder",
        on_delete=models.CASCADE,
        related_name="%(class)s",
    )

    class Meta:
        abstract = True


class DefaultThemeComponent(ThemeComponent):
    # colors
    primary_color = models.CharField(max_length=9, default="#000000ff")
    secondary_color = models.CharField(max_length=9, default="#000000ff")
    # headings
    heading_1_font_size = models.SmallIntegerField(default=24)
    heading_1_color = models.CharField(max_length=9, default="#000000ff")
    heading_2_font_size = models.SmallIntegerField(default=20)
    heading_2_color = models.CharField(max_length=9, default="#000000ff")
    heading_3_font_size = models.SmallIntegerField(default=16)
    heading_3_color = models.CharField(max_length=9, default="#000000ff")
    # buttons
    button_background_color = models.CharField(max_length=9, default="#000000ff")
    button_font_color = models.CharField(max_length=9, default="#ffffffff")
    button_font_size = models.CharField(max_length=9, default="#000000ff")
    button_border_radius = models.SmallIntegerField(default=0)
    button_border_size = models.SmallIntegerField(default=0)
    button_border_color = models.CharField(max_length=9, default="#000000ff")
    button_horizontal_padding = models.SmallIntegerField(default=12)
    button_vertical_padding = models.SmallIntegerField(default=6)
