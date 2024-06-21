from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, \
    QComboBox, QFileDialog, QRadioButton
import sys
from random import randint
from moviepy.video.io.VideoFileClip import VideoFileClip
from VideoSelf import VideoWindow

class ConcatenateWindow(QWidget):
    """
    Această clasă reprezintă o fereastră pentru concatenarea mai multor videoclipuri.
    Este un QWidget care va apărea ca o fereastră independentă.
    """
    def __init__(self, window, w, h, videoSamples):
        super().__init__()
        self.window = window
        self.resize(w, h)
        self.setBaseSize(w, h)
        print(len(videoSamples))

        # Verifică dacă sunt cel puțin două videoclipuri selectate pentru concatenare
        if len(videoSamples) < 2:
            self.layout = QVBoxLayout()
            self.note = QLabel("Choose at least two videos")  # Etichetă de informare
            self.done = QPushButton("Close")  # Buton de închidere
            self.layout.addWidget(self.note)
            self.layout.addWidget(self.done)
            self.done.clicked.connect(self.destroy_it)  # Conectarea butonului la funcția de distrugere
            self.setLayout(self.layout)

        else:
            self.layout = QVBoxLayout()
            self.slide_out = QRadioButton()  # Buton radio pentru alegerea tipului de concatenare
            self.slidelayout = QHBoxLayout()
            self.note = QLabel("Is concatenation slided:")  # Etichetă pentru butonul radio
            self.slidelayout.addWidget(self.note)
            self.slidelayout.addWidget(self.slide_out)
            self.done = QPushButton("Concatenate")  # Buton pentru a începe concatenarea

            self.layout.addLayout(self.slidelayout)
            self.layout.addWidget(self.done)
            # Conectarea butonului de concatenare la funcția din clasa VideoWindow
            self.done.clicked.connect(lambda: self.window.concatenate_video(
                self,
                videoSamples,
                True if self.slide_out.isChecked() else False
            ))
            self.setLayout(self.layout)

    def destroy_it(self):
        # Funcție pentru a închide fereastra
        self.destroy()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    videoWindow = VideoWindow()
    videoSamples = []  # Adaugă aici listele de videoclipuri pentru testare
    concatenateWindow = ConcatenateWindow(videoWindow, 300, 200, videoSamples)
    concatenateWindow.show()
    sys.exit(app.exec_())
