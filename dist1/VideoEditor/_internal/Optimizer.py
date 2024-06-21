from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, \
    QComboBox, QFileDialog, QLineEdit
import sys
from random import randint
from moviepy.video.io.VideoFileClip import VideoFileClip
from VideoSelf import VideoWindow

class OptimizerWindow(QWidget):
    def __init__(self, window, w, h):
        super().__init__()  # Inițializează clasa de bază QWidget
        self.file_name = ""  # Inițializează numele fișierului ca un șir gol
        self.window = window  # Salvează referința la fereastra principală pentru a putea apela metodele acesteia
        self.resize(w, h)  # Redimensionează fereastra la lățimea și înălțimea specificate
        self.setBaseSize(w, h)  # Setează dimensiunea de bază a ferestrei

        self.layout = QVBoxLayout()  # Creează un layout vertical pentru widget-uri
        self.changesizey = QLineEdit()  # Creează un câmp de text pentru introducerea înălțimii dorite
        self.changesizey.setPlaceholderText("height")  # Setează textul de ajutor pentru câmpul de înălțime
        self.changesizex = QLineEdit()  # Creează un câmp de text pentru introducerea lățimii dorite
        self.changesizey.setPlaceholderText("width")  # Setează textul de ajutor pentru câmpul de lățime (acesta ar trebui să fie self.changesizex.setPlaceholderText("width"))
        self.ok = QPushButton("Set New Size")  # Creează un buton pentru aplicarea noii dimensiuni

        self.layoutyx = QHBoxLayout()  # Creează un layout orizontal pentru a organiza câmpurile de text
        self.layoutyx.addWidget(self.changesizex)  # Adaugă câmpul de lățime la layout-ul orizontal
        self.layoutyx.addWidget(self.changesizey)  # Adaugă câmpul de înălțime la layout-ul orizontal

        self.layout.addLayout(self.layoutyx)  # Adaugă layout-ul orizontal la layout-ul vertical
        self.layout.addWidget(self.ok)  # Adaugă butonul la layout-ul vertical
        self.ok.clicked.connect(lambda: self.window.optim_video(self, self.changesizex.text(), self.changesizey.text()))  # Conectează butonul la funcția de optim_video cu valorile introduse

        self.setLayout(self.layout)  # Setează layout-ul pentru widget
