from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QApplication


def get_center_point(qt_app: QApplication) -> QPoint:
    return QPoint(qt_app.screens()[0].size().width() // 2, qt_app.screens()[0].size().height() // 2)
