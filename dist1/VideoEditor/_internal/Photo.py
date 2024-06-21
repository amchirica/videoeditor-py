from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, \
    QComboBox, QFileDialog
from PyQt5.QtGui import QIcon
import sys
from random import randint
from moviepy.video.io.VideoFileClip import VideoFileClip
from VideoSelf import VideoWindow

class AddPhotoWindow(QWidget):
    """
    Această clasă reprezintă o fereastră pentru adăugarea unei fotografii într-un videoclip.
    Este un QWidget care va apărea ca o fereastră independentă.
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
        self.setWindowTitle("Add Photo to Video")


        # Configurarea layout-ului principal
        self.layout = QVBoxLayout()
        self.add_photo = QPushButton('Import Photo')
        self.add = QPushButton("Add")

        # Adăugarea butoanelor în layout
        self.layout.addWidget(self.add_photo)
        self.layout.addWidget(self.add)
        self.add_photo.clicked.connect(self.import_vid)
        self.add.clicked.connect(lambda: self.window.add_photo_video(self, self.file_name))

        self.setLayout(self.layout)

    def import_vid(self):
        # Deschide un dialog pentru a selecta o imagine de importat
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image files (*.jpg *.jpeg *.png)')
        print(file_name, self.file_name)
        if file_name != '':
            self.file_name = file_name

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    videoWindow = VideoWindow()
    addPhotoWindow = AddPhotoWindow(videoWindow, 300, 200)
    addPhotoWindow.show()
    sys.exit(app.exec_())
