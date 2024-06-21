from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, \
    QComboBox, QFileDialog, QRadioButton
from PyQt5.QtGui import QIcon
import sys
from random import randint
from moviepy.video.io.VideoFileClip import VideoFileClip
from VideoSelf import VideoWindow

class AudioWindow(QWidget):
    """
    Această "fereastră" este un QWidget. Dacă nu are un părinte,
    va apărea ca o fereastră independentă, așa cum dorim.
    """

    def __init__(self, window, w, h):
        super().__init__()
        self.file_name = ""
        self.window = window
        self.resize(w, h)
        self.setBaseSize(w, h)
        
        
        # Setarea favicon-ului
        favicon_path = "prerequisite/favicon.ico"  # Asigură-te că calea către favicon este corectă
        self.setWindowIcon(QIcon(favicon_path))
        # Setarea titlului ferestrei
        self.setWindowTitle("Import Audio")

        # Configurarea layout-ului principal
        self.layout = QVBoxLayout()
        self.concat = QPushButton('Import Audio')  # Buton pentru importarea audio-ului
        self.done = QPushButton("Concatenate")  # Buton pentru concatenare
        self.imp = QLabel()  # Etichetă pentru a afișa starea importului

        # Adăugarea butoanelor și etichetei în layout
        self.layout.addWidget(self.concat)
        self.layout.addWidget(self.imp)
        self.layout.addWidget(self.done)
        self.concat.clicked.connect(self.import_vid)
        self.done.clicked.connect(lambda: self.window.concatenate_audio(self, self.file_name))

        self.setLayout(self.layout)

    def import_vid(self):
        # Deschide un dialog pentru a selecta un fișier audio de importat
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Audio', '', 'Audio files (*.mp3 *.wav *.aac)')
        if file_name != '':
            self.file_name = file_name
            self.imp.setText("Audio is imported")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    videoWindow = VideoWindow()
    audioWindow = AudioWindow(videoWindow, 300, 200)
    audioWindow.show()
    sys.exit(app.exec_())
