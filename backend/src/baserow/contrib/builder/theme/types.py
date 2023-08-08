from typing import TypeVar

from .models import ThemeComponent

ThemeComponentSubClass = TypeVar("ThemeComponentSubClass", bound=ThemeComponent)
