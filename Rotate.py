from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, \
    QComboBox, QFileDialog, QLineEdit
from PyQt5.QtGui import QIcon
import sys
from random import randint
from moviepy.video.io.VideoFileClip import VideoFileClip
from VideoSelf import VideoWindow
import subprocess
import shlex
import json

class RotateWindow(QWidget):
    """
    Această "fereastră" este un QWidget. Dacă nu are un părinte, 
    va apărea ca o fereastră independentă, așa cum dorim.
    """
    
    

    @staticmethod
    def get_rotation(file_path_with_file_name):
        """
        Funcție pentru a obține rotația fișierului video de intrare.
        Adaptată din gist.github.com/oldo/dc7ee7f28851922cca09/revisions folosind comanda ffprobe de Lord Neckbeard de pe
        stackoverflow.com/questions/5287603/how-to-extract-orientation-information-from-videos?noredirect=1&lq=1

        Returnează o rotație None, 90, 180 sau 270.
        """
        cmd = "ffprobe -loglevel error -select_streams v:0 -show_entries stream_tags=rotate -of default=nw=1:nk=1"
        args = shlex.split(cmd)
        args.append(file_path_with_file_name)
        # Rulează procesul ffprobe, decodează stdout în utf-8 și convertește în JSON
        ffprobe_output = subprocess.check_output(args).decode('utf-8')
        if len(ffprobe_output) > 0:  # Outputul cmd este None dacă ar trebui să fie 0
            ffprobe_output = json.loads(ffprobe_output)
            rotation = ffprobe_output
        else:
            rotation = 0

        return rotation

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
        self.setWindowTitle("Rotate")

        # Crearea meniului miniatura
        self.mini_menu = QHBoxLayout()
        self.label_rotate = QLabel('Degree of rotation (counterclockwise)')
        self.combobox_degree = QComboBox()
        degrees = ['0', '90', '180', '270']
        self.combobox_degree.addItems(degrees)
        self.mini_menu.addWidget(self.label_rotate)
        self.mini_menu.addWidget(self.combobox_degree)

        # Crearea butonului OK
        self.ok = QPushButton("Rotate")

        # Configurarea layout-ului principal
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.mini_menu)
        self.layout.addWidget(self.ok)
        self.ok.clicked.connect(lambda: self.window.record_rotate_video(self, self.combobox_degree.currentText()))

        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RotateWindow(None, 300, 200)
    window.show()
    sys.exit(app.exec_())
