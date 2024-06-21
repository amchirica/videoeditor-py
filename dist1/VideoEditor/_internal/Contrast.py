# contrast.py

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSlider, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys
from moviepy.editor import VideoFileClip
import os

class ContrastWindow(QWidget):
    """
    Această clasă reprezintă o fereastră pentru ajustarea contrastului unui videoclip.
    Este un QWidget care va apărea ca o fereastră independentă.
    """
    def __init__(self, window, w, h):
        super().__init__()
        self.file_name = ""
        self.window = window
        self.resize(w, h)
        self.setBaseSize(w, h)

        self.setWindowTitle("Contrast Adjuster")
        self.setGeometry(100, 100, 250, 250)
        
        # Setarea favicon-ului
        favicon_path = "prerequisite/favicon.ico"  # Asigură-te că calea către favicon este corectă
        self.setWindowIcon(QIcon(favicon_path))

        # Crearea slider-ului pentru ajustarea hue
        self.slider_hue = QSlider(Qt.Horizontal)
        self.slider_hue.setRange(-100, 100)  # Setarea intervalului pentru hue
        self.slider_hue.setValue(0)  # Valoarea inițială

        # Crearea slider-ului pentru ajustarea saturației
        self.slider_saturation = QSlider(Qt.Horizontal)
        self.slider_saturation.setRange(-100, 100)  # Setarea intervalului pentru saturație
        self.slider_saturation.setValue(0)  # Valoarea inițială

        # Crearea etichetelor pentru hue și saturație
        self.label_hue = QLabel("Hue", alignment=Qt.AlignCenter)
        self.label_saturation = QLabel("Saturation", alignment=Qt.AlignCenter)

        # Crearea butonului de confirmare
        self.ok_button = QPushButton("Set Contrast")
        self.ok_button.clicked.connect(lambda: self.window.change_contrast_video(
            self,
            c_factor=(self.slider_hue.value() + 100) / 100,
            hue=(self.slider_hue.value() + 100) / 100,
            saturation=(self.slider_saturation.value() + 100) / 100
        ))
        
        # Actualizarea textului etichetelor când se schimbă valorile slider-elor
        self.slider_hue.valueChanged.connect(lambda: self.label_hue.setText(str(self.slider_hue.value())))
        self.slider_saturation.valueChanged.connect(lambda: self.label_saturation.setText(str(self.slider_saturation.value())))

        # Configurarea layout-ului principal
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.slider_hue)
        self.layout.addWidget(self.label_hue)
        self.layout.addWidget(self.slider_saturation)
        self.layout.addWidget(self.label_saturation)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)
