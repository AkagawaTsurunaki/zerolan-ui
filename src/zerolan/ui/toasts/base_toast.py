from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont, QPalette, QPen
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy

from zerolan.ui.animations.fadeout import FadeoutAnimation
from zerolan.ui.themes.modern import DefaultToastTheme


class QtBaseToast(QWidget, FadeoutAnimation):
    BORDER_WIDTH = 1
    BORDER_RADIUS = 6

    def __init__(
            self,
            message: str,
            duration: int = 5,
            screen_center: QPoint = None,
            theme: DefaultToastTheme = None,
    ):
        super().__init__()

        self._theme = theme if theme is not None else DefaultToastTheme()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.layout = QVBoxLayout()
        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.label.setFixedWidth(720)
        self.label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # Text color
        palette = self.label.palette()
        palette.setColor(QPalette.WindowText, QColor(self._theme.font_color))
        self.label.setPalette(palette)

        # Font
        self.setFont(QFont(self._theme.font_family, self._theme.font_size))

        # The initial position is outside the top of the screen so that it can slide down
        self.screen_center = screen_center
        self.x = self.screen_center.x() - self.width() // 2 + 1
        self.y = self.screen_center.y() - self.height() // 2

        # Set animation with timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_fading_out)
        self.timer.start(duration * 1000)  # duration in seconds

        # Animation: Swipe down from the top of the screen
        self.slide_animation = QPropertyAnimation(self, b"pos")
        self.slide_animation.setDuration(500)  # The swipe animation lasts 0.5 seconds
        self.slide_animation.setStartValue(
            QPoint(self.x, -self.height())
        )  # Start outside the top of the screen
        self.slide_animation.setEndValue(QPoint(self.x, 10))  # Slide to the top center of the screen
        self.slide_animation.finished.connect(lambda: self.timer.start(duration * 1000))

        # Close the component when the gradient disappears
        self.fade_animation.finished.connect(self.close)

    def showEvent(self, event):  # Starts the sliding animation when the window is displayed
        self.slide_animation.start()
        super().showEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Anti-aliasing

        # Draw a rounded rectangle filled with color
        painter.setBrush(QColor(self._theme.bg_color))

        # Draw a border
        painter.setPen(
            QPen(
                QColor(self._theme.border_color),
                self.BORDER_WIDTH,
                Qt.SolidLine,
                Qt.RoundCap,
                Qt.RoundJoin,
            )
        )

        rect = self.rect()
        rect.setWidth(rect.width() - 1)
        rect.setHeight(rect.height() - 1)

        # Draw a rounded rectangle
        painter.drawRoundedRect(rect, self.BORDER_RADIUS, self.BORDER_RADIUS)

    def set_message(self, message: str):
        self.label.setText(message)

    def finish(self):
        self.start_fading_out()
