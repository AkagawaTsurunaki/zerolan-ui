from dataclasses import dataclass


@dataclass
class DefaultToastTheme:
    bg_color: str = "#222222"
    border_color: str = "#0078d4"
    font_color: str = "#ffffff"
    font_family: str = "Microsoft Yahei UI"
    font_size: int = 10


@dataclass
class WarningToastTheme(DefaultToastTheme):
    bg_color: str = "#382c21"
    border_color: str = "#c6a201"
    font_color: str = "#fa7a27"


@dataclass
class ErrorToastTheme(DefaultToastTheme):
    bg_color: str = "#352525"
    border_color: str = "#f57e6f"
    font_color: str = "#ff4f39"


toast_theme = {
    "info": DefaultToastTheme(),
    "warn": WarningToastTheme(),
    "error": ErrorToastTheme()
}