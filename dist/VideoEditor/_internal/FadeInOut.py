from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QComboBox
import sys
from PyQt5.QtGui import QIcon
from random import randint
from VideoSelf import VideoWindow

class FadeWindow(QWidget):
    """
    Această "fereastră" este un QWidget. Dacă nu are un părinte,
    va apărea ca o fereastră independentă, așa cum dorim.
    """
    def __init__(self, window, w, h):
        super().__init__()
        self.window = window
        self.resize(w, h)
        self.setBaseSize(w, h)
        
        # Setarea favicon-ului
        favicon_path = "prerequisite/favicon.ico"  # Asigură-te că calea către favicon este corectă
        self.setWindowIcon(QIcon(favicon_path))
        # Setarea titlului ferestrei
        self.setWindowTitle("Set Fade In/Out")
        

        # Configurarea layout-ului principal
        self.layout = QHBoxLayout()
        self.fade_in = QPushButton('Fade In')  # Buton pentru efectul de fade in
        self.fade_out = QPushButton('Fade Out')  # Buton pentru efectul de fade out
        self.combobox_duration = QComboBox()  # ComboBox pentru selectarea duratei efectului
        duration = ['1', '3', '5', '7']  # Duratele disponibile pentru efecte
        self.combobox_duration.addItems(duration)

        # Adăugarea butoanelor și comboBox-ului în layout
        self.layout.addWidget(self.fade_in)
        self.layout.addWidget(self.fade_out)
        self.layout.addWidget(self.combobox_duration)

        # Conectarea butoanelor la funcțiile corespunzătoare
        self.fade_in.clicked.connect(lambda: self.window.fade_in_video(self, self.combobox_duration.currentText()))
        self.fade_out.clicked.connect(lambda: self.window.fade_out_video(self, self.combobox_duration.currentText()))

        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    videoWindow = VideoWindow()
    fadeWindow = FadeWindow(videoWindow, 300, 200)
    fadeWindow.show()
    sys.exit(app.exec_())
