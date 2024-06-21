from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSlider, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys
from moviepy.editor import VideoFileClip
import os

class ColorBalance(QWidget):
    """
    Această clasă reprezintă o fereastră pentru ajustarea balanței de culoare a unui videoclip.
    Este un QWidget care va apărea ca o fereastră independentă.
    """
    def __init__(self, window, w, h):
        super().__init__()
        self.file_name = ""
        self.window = window
        self.resize(w, h)
        self.setBaseSize(w, h)

        self.setWindowTitle("Color Balance Adjuster")
        self.setGeometry(100, 100, 250, 250)
        
        # Setarea favicon-ului
        favicon_path = "prerequisite/favicon.ico"  # Asigură-te că calea către favicon este corectă
        self.setWindowIcon(QIcon(favicon_path))

        # Crearea slider-ului pentru ajustarea componentei roșii (Red)
        self.slider_red = QSlider(Qt.Horizontal)
        self.slider_red.setRange(-100, 100)  # Setarea intervalului pentru roșu
        self.slider_red.setValue(0)  # Valoarea inițială

        # Crearea slider-ului pentru ajustarea componentei verzi (Green)
        self.slider_green = QSlider(Qt.Horizontal)
        self.slider_green.setRange(-100, 100)  # Setarea intervalului pentru verde
        self.slider_green.setValue(0)  # Valoarea inițială

        # Crearea slider-ului pentru ajustarea componentei albastre (Blue)
        self.slider_blue = QSlider(Qt.Horizontal)
        self.slider_blue.setRange(-100, 100)  # Setarea intervalului pentru albastru
        self.slider_blue.setValue(0)  # Valoarea inițială

        # Crearea etichetelor pentru componentele roșu, verde și albastru
        self.label_red = QLabel("Red", alignment=Qt.AlignCenter)
        self.label_green = QLabel("Green", alignment=Qt.AlignCenter)
        self.label_blue = QLabel("Blue", alignment=Qt.AlignCenter)

        # Crearea butonului de confirmare
        self.ok_button = QPushButton("Set Color Balance")
        self.ok_button.clicked.connect(lambda: self.window.change_color_balance_video(
            self, 
            red=(self.slider_red.value() + 100) / 100, 
            green=(self.slider_green.value() + 100) / 100, 
            blue=(self.slider_blue.value() + 100) / 100
        ))
        
        # Actualizarea textului etichetelor când se schimbă valorile slider-elor
        self.slider_red.valueChanged.connect(lambda: self.label_red.setText(str(self.slider_red.value())))
        self.slider_green.valueChanged.connect(lambda: self.label_green.setText(str(self.slider_green.value())))
        self.slider_blue.valueChanged.connect(lambda: self.label_blue.setText(str(self.slider_blue.value())))

        # Configurarea layout-ului principal
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.slider_red)
        self.layout.addWidget(self.label_red)
        self.layout.addWidget(self.slider_green)
        self.layout.addWidget(self.label_green)
        self.layout.addWidget(self.slider_blue)
        self.layout.addWidget(self.label_blue)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)

