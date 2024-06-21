from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QLabel, QVBoxLayout, QPushButton, QSlider
import sys
from random import randint
from moviepy.video.io.VideoFileClip import VideoFileClip
from VideoSelf import VideoWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class SpeedWindow(QDialog, QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, window, w, h):
        super().__init__()
        self.file_name = ""
        self.window = window
        self.resize(w, h)
        self.setBaseSize(w, h)


        self.setWindowTitle("Speed video")
        # Setarea favicon-ului
        favicon_path = "prerequisite/favicon.ico"  # Asigură-te că calea către favicon este corectă
        self.setWindowIcon(QIcon(favicon_path))

        self.slider = QSlider(
            orientation=Qt.Horizontal,
            minimum=-10,
            maximum=10,
            singleStep=1,
            pageStep=1
        )
        self.slider.setValue(0)

        label_value = QLabel(alignment=Qt.AlignCenter)
        self.slider.valueChanged.connect(lambda: label_value.setNum(self.slider.value()))
        label_value.setNum((self.slider.value()))


        self.layout = QVBoxLayout()
        self.ok = QPushButton("Set New Speed")

        self.layout.addWidget(self.slider)
        self.layout.addWidget(label_value)
        self.layout.addWidget(self.ok)
        self.ok.clicked.connect(lambda: self.window.change_speed_video(self, ((self.slider.value()+10.01)/10)))

        self.setLayout(self.layout)