from dataclasses import dataclass
from typing import Literal

from PyQt6.QtWidgets import QApplication
from dataclasses_json import dataclass_json

from toasts.base_toast import QtBaseToast
from toasts.progress_toast import QtProgressToast


@dataclass_json
@dataclass
class ToastEntity:
    id: str
    message: str
    level: Literal["info", "warn", "error"] = "info"
    duration: int = 5


@dataclass_json
@dataclass
class ProgressToastEntity(ToastEntity):
    busy: bool = True
    max_value: int = 100
    cur_value: int = 0


@dataclass
class QtAppWrapper:
    toast: QtBaseToast | QtProgressToast
    qt_app: QApplication
