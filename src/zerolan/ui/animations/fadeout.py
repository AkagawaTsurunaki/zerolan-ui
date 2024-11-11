from PyQt6.QtCore import QPropertyAnimation


class FadeoutAnimation:
    def __init__(self):
        super().__init__()
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(1000)
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)

    def start_fading_out(self):
        self.fade_animation.start()
