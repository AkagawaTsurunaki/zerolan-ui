from themes.modern import DefaultToastTheme
from toasts.base_toast import QtBaseToast

from PyQt6.QtCore import QPoint, QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication, QProgressBar


class QtProgressToast(QtBaseToast):
    finish_signal = pyqtSignal()

    def __init__(
            self,
            message: str,
            duration: int = 5,
            screen_center: QPoint = None,
            theme: DefaultToastTheme = DefaultToastTheme(),
            is_busy: bool = False,
            max_value: int = 100,
    ):
        super(QtProgressToast, self).__init__(message, -1, screen_center, theme)

        # Create and set QProcessbar
        self.progressBar = QProgressBar(self)
        # Set the stylesheet to hide text labels
        self.progressBar.setStyleSheet(
            """
            QProgressBar {
                background: #242424;
            }
            QProgressBar::chunk{
                border-radius:5px;
                background:{color}
            }
        """.replace(
                "{color}", theme.border_color
            )
        )
        self.max_value = max_value
        if is_busy:
            self.progressBar.setRange(0, 0)
        else:
            self.progressBar.setMinimum(0)  # Set the minimum value of the progress bar
            self.progressBar.setMaximum(self.max_value)  # Sets the maximum value of the progress bar
        self.progressBar.setValue(0)  # The initial value of the progress bar is 0
        self.progressBar.setFormat("")
        self.progressBar.setFixedHeight(2)

        self.layout.addWidget(self.progressBar)
        self.setLayout(self.layout)

        self._duration = duration

        self.finish_signal.connect(self._finish)

    def finish(self):
        self.finish_signal.emit()

    def _finish(self):
        self.progressBar.setRange(0, self.max_value)
        self.set_value(self.max_value)
        timer = QTimer(self)
        timer.timeout.connect(
            self.start_fading_out
        )  # When the timer times out, the start_fading_out method is called
        timer.start(self._duration * 1000)

    def set_value(self, value=None):
        QApplication.processEvents()
        if value is not None:
            self.progressBar.setValue(value)
        else:
            self.progressBar.setValue(0)
