from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy

from animations.fadeout import FadeoutAnimation


class QTSubtitle(QWidget, FadeoutAnimation):
    def __init__(self, content: str, duration: int, screen_center: QPoint):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.layout = QVBoxLayout()
        self.label = QLabel("")
        self.label.setWordWrap(True)
        self.label.setFixedWidth(800)
        self.label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.label.setAlignment(Qt.AlignCenter)
        # Text color
        palette = self.label.palette()
        palette.setColor(QPalette.WindowText, QColor("#ffffff"))
        self.label.setPalette(palette)

        # Font
        self.setFont(QFont("MaoKenAssortedSans", 26))

        # The initial position is outside the top of the screen so that it can slide down
        self.screen_center = screen_center
        self.x = self.screen_center.x() - self.width() // 2
        self.y = self.screen_center.y() - self.height() // 2
        self.move(self.x, 2 * self.screen_center.y() - 300)

        # Set animations with timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_fading_out)
        self.timer.start(duration * 1000)  # duration in seconds

        # Close the component when the gradient disappears
        self.fade_animation.finished.connect(self.close)

        self.typewriter_timer = QTimer(self)
        self.setTypewriterText(content, duration)
        self.typewriter_timer.timeout.connect(self.showNextCharacter)

    def setTypewriterText(self, text, duration):
        self._content = text
        self._cur_text = ""
        self._duration = duration
        self._index = 0
        self.typewriter_timer.start(self._duration * 1000 // len(self._content))  # Calculate interval based on duration

    def showNextCharacter(self):
        if self._index < len(self._content):
            self._cur_text += self._content[self._index]
            self.label.setText(self._cur_text)
            self._index += 1
        else:
            self.typewriter_timer.stop()
