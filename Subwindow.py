from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, \
    QComboBox, QFileDialog, QRadioButton
from PyQt5.QtGui import QIcon
import sys
from random import randint
from moviepy.video.io.VideoFileClip import VideoFileClip
from VideoSelf import VideoWindow
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog
from Terminal import TerminalWidget


class SubWindow(QWidget):
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

        # Setarea favicon-ului
        favicon_path = "prerequisite/favicon.ico"  # Asigură-te că calea către favicon este corectă
        self.setWindowIcon(QIcon(favicon_path))
        # Setarea titlului ferestrei
        self.setWindowTitle("Add or Import Second Video")

        self.layout = QVBoxLayout()
        self.concat = QPushButton('Import Second Video')
        self.done = QPushButton("Add Subvideo")
        self.export_terminal = TerminalWidget()

        self.layout.addWidget(self.concat)
        self.layout.addWidget(self.done)
        self.concat.clicked.connect(self.import_vid)
        self.done.clicked.connect(lambda: self.window.subclip_video(self, self.file_name))

        self.setLayout(self.layout)

    def import_vid(self):
        # Definițiile de formate pot fi extinse pentru a include mai multe tipuri de fișiere
        formats = "Video files (*.mp4 *.MP4 *.avi *.mov *.mkv *.flv *.wmv);;" \
                "Image files (*.jpg *.jpeg *.png *.bmp)"
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', formats)
        if file_name != '':
            self.file_name = file_name
     
    def add_subvideo(self):
        if self.file_name:
            self.window.subclip_video(self, self.file_name)
        else:
            print("No video file selected.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    video_window = VideoWindow()
    sub_window = SubWindow(video_window, 400, 300)
    sub_window.show()
    sys.exit(app.exec_())       