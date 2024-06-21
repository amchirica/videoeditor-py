from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSlider, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys
from moviepy.editor import VideoFileClip, clips_array
from moviepy.editor import vfx
import os

class BrightnessWindow(QWidget):
    """
    Această clasă reprezintă o fereastră pentru ajustarea luminozității unui videoclip.
    Este un QWidget care va apărea ca o fereastră independentă.
    """
    def __init__(self, window, w, h):
        super().__init__()
        self.file_name = ""
        self.window = window
        self.resize(w, h)
        self.setBaseSize(w, h)

        self.setWindowTitle("Brightness Adjuster")
        self.setGeometry(100, 100, 250, 250)
        
        # Setarea favicon-ului
        favicon_path = "prerequisite/favicon.ico"  # Asigură-te că calea către favicon este corectă
        self.setWindowIcon(QIcon(favicon_path))


        # Crearea slider-ului pentru ajustarea luminozității
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(-100, 100)  # Setarea intervalului pentru luminozitate
        self.slider.setValue(0)  # Valoarea inițială

        # Crearea etichetelor pentru luminozitate
        self.label = QLabel("Brightness", alignment=Qt.AlignCenter)
        self.label2 = QLabel("0", alignment=Qt.AlignCenter)

        # Crearea butonului de confirmare
        self.ok_button = QPushButton("Set Brightness")
        self.ok_button.clicked.connect(lambda: self.window.change_brightness_video(self, b_factor=(self.slider.value() + 100) / 100))
        
        # Actualizarea textului etichetei când se schimbă valoarea slider-ului
        self.slider.valueChanged.connect(lambda: self.label2.setText(str(self.slider.value())))

        # Configurarea layout-ului principal
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)
