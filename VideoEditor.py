import functools
import sys
from PyQt5.QtGui import QPalette, QColor, QPixmap, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QToolBar, QAction, QStatusBar, QCheckBox, QComboBox, \
    QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout, QPushButton, QTabWidget, QDialog, \
    QDialogButtonBox, QMessageBox, QFileDialog, QTextEdit, QFrame, QStyle, QSizePolicy, QSlider, \
    QListWidget, QListWidgetItem, QToolButton, QSizePolicy
from PyQt5.QtCore import Qt, QSize, QDir, QRect, QUrl
from PyQt5.QtMultimediaWidgets import QVideoWidget
from moviepy.editor import VideoFileClip
from Photo import AddPhotoWindow
from AddText import AddTextWindow
from ColorBalance import ColorBalance
from Concatenate import ConcatenateWindow
from Optimizer import OptimizerWindow
from Importaudio import AudioWindow
from Rotate import RotateWindow
from Speed import SpeedWindow
from Subwindow import SubWindow
from VideoCut import *
from Brightness import BrightnessWindow
import TimeLine
from FadeInOut import FadeWindow
from TimeLine import QTimeLine
from VideoSelf import VideoWindow
from Terminal import TerminalWidget
from Thread import Thread
import tkinter as tk
from Contrast import ContrastWindow
from PyQt5.QtWidgets import QAction, QMenu

            
            
            
class MainWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)
        main_layout = QVBoxLayout()
        self.file_name = ""
        layout = QHBoxLayout()
        layout1 = QVBoxLayout()
        self.menuLayout = QGridLayout()
        for i in range(10):
            for j in range(10):
                self.menuLayout.addWidget(QLabel(), i, j)
        self.i = 0
        self.j = 0
        self.videoSamples = []
        self.icons = []

        layout3 = QVBoxLayout()
        self.VideoPlay = VideoWindow()
        layout3.addWidget(self.VideoPlay)

        # Adaugă o etichetă pentru informații despre videoclip
        self.video_info_label = QLabel("Video: None\nDuration: 0 seconds\nResolution: N/A\nCodec: N/A")
        self.video_info_label.setWordWrap(True)
        layout1.addWidget(self.video_info_label)

        layout3 = QVBoxLayout()
        self.VideoPlay = VideoWindow()
        layout3.addWidget(self.VideoPlay)
        
        self.audadd = QPushButton('Import/Rewrite Audio')
        self.audadd.setToolTip("Import audio on video")  # Tooltip pentru import audio on video
        self.audadd.clicked.connect(lambda: self.show_sub_window(AudioWindow(self.VideoPlay, 200, 100)))
        self.set_button_style(self.audadd)
        layout1.addWidget(self.audadd)
        
        self.subvid = QPushButton('Add Subvideo')
        self.subvid.setToolTip("Add subvideo on main video in the end") # Tooltip pentru a adauga video la finalul videoclipului principal
        self.subvid.clicked.connect(lambda: self.show_sub_window(SubWindow(self.VideoPlay, 200, 100)))
        self.set_button_style(self.subvid)
        layout1.addWidget(self.subvid)

        self.fade = QPushButton('Fade in/Fade out')
        self.fade.setToolTip("Apply fade in or fade out effects to the video")  # Tooltip pentru efectele de fade in/out
        self.fade.clicked.connect(lambda: self.show_sub_window(FadeWindow(self.VideoPlay, 200, 100)))
        self.set_button_style(self.fade)
        layout1.addWidget(self.fade)
        
        self.rotate = QPushButton('Rotate')
        self.rotate.setToolTip("Rotate the video")  # Tooltip pentru rotirea videoclipului
        self.rotate.clicked.connect(lambda: self.show_sub_window(RotateWindow(self.VideoPlay, 200, 100)))
        self.set_button_style(self.rotate)
        layout1.addWidget(self.rotate)

        self.speed = QPushButton('Speed')
        self.speed.setToolTip("Speed the video") #Tooltip pentru viteza videoclipului
        self.speed.clicked.connect(lambda: self.show_sub_window(SpeedWindow(self.VideoPlay, 200, 100)))
        self.set_button_style(self.speed)
        layout1.addWidget(self.speed)

        self.add_text = QPushButton('Text')
        self.add_text.setToolTip("Add text to the video")  # Tooltip pentru adăugarea de text
        self.add_text.clicked.connect(lambda: self.show_sub_window(AddTextWindow(self.VideoPlay, 200, 100)))
        self.set_button_style(self.add_text)
        layout1.addWidget(self.add_text)

        self.brightness = QPushButton('Brightness')
        self.brightness.setToolTip("Adjust the brightness of the video")  # Tooltip pentru ajustarea luminozității
        self.brightness.clicked.connect(lambda: self.show_sub_window(BrightnessWindow(self.VideoPlay, 200, 100)))
        self.set_button_style(self.brightness)
        layout1.addWidget(self.brightness)
        
        self.contrast = QPushButton('Contrast')
        self.contrast.setToolTip("Adjust the contrast of the video")  # Tooltip pentru ajustarea contrastului
        self.contrast.clicked.connect(lambda: self.show_sub_window(ContrastWindow(self.VideoPlay, 200, 100)))
        self.set_button_style(self.contrast)
        layout1.addWidget(self.contrast)
        
        self.color1 = QPushButton('Color Temperature')
        self.color1.setToolTip("Adjust the color balance of the video")  # Tooltip pentru ajustarea balanței de culoare
        self.color1.clicked.connect(lambda: self.show_sub_window(ColorBalance(self.VideoPlay, 200, 100)))
        self.set_button_style(self.color1)
        layout1.addWidget(self.color1)

        
        self.export_terminal = TerminalWidget(self)
        layout.addWidget(self.export_terminal)

        layout1.addStretch()

        layout.addLayout(layout1, 2)
        layout.addLayout(self.menuLayout, 6)
        layout.addLayout(layout3, 10)
        main_layout.addLayout(layout, 2)
        lay = QVBoxLayout()
        self.time_l = TimeLine.QTimeLine(300, 10)
        lay.addWidget(self.time_l)

        main_layout.addLayout(lay, 1)
        self.setLayout(main_layout)

    def set_button_style(self, button):
        button.setMinimumSize(170, 25)
        button.setMaximumSize(170, 25)

    def import_vid(self, file_name=None):
        formats = "Video files (*.mp4 *.MP4 *.avi *.mov *.mkv *.flv *.wmv);;" \
                "Audio files (*.mp3 *.wav *.aac);;" \
                "Image files (*.jpg *.jpeg *.png *.bmp)"
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', formats)
        if file_name != '':
            self.file_name = file_name
        if file_name != '':
            clip = VideoFileClip(file_name)
            dot_index = file_name.rfind('.')
            cut_frame_name = file_name[: dot_index] + '_{}.png'.format(1)
            duration = clip.duration
            # Verifică dacă durata este suficient de lungă pentru a salva cadrul la timpul specificat
            time_to_save_frame = min(10, duration - 0.1)
            clip.save_frame(cut_frame_name, time_to_save_frame)
            icon = QLabel()
            # Aplicați stilul pentru a evidenția marginile
            icon.setStyleSheet("""
                QLabel {
                    border: 2px solid #FF5733;
                    border-radius: 5px;
                    margin: 5px;
                }
            """)

            icon.mouseDoubleClickEvent = functools.partial(self.playSelectedItem, filename=file_name)
            icon.mouseReleaseEvent = functools.partial(self.add_to_concatenate, filename=file_name, label=icon)
            w = icon.width()
            h = icon.height()
            pixmap = QPixmap(cut_frame_name)
            icon.setPixmap(pixmap.scaled(int(w / 10), int(h / 10)))
            self.menuLayout.addWidget(icon, self.j, self.i)
            if self.i == 9:
                self.i = 0
                self.j += 1
            else:
                self.i += 1
            if self.i == 9 and self.j == 9:
                self.i = 0
                self.j = 0

            self.clipchik = TimeLine.VideoSample(clip.duration)
            self.time_l.videoSamples.append(self.clipchik)

            # Afișează informații despre videoclip în eticheta video_info_label
            video_info = (
                f"Video: {file_name}\n"
                f"Duration: {clip.duration} seconds\n"
                f"Resolution: {clip.size}\n"
                f"Codec: {clip.fps}\n"
            )
            self.video_info_label.setText(video_info)

    def playSelectedItem(self, event, filename):
        self.VideoPlay.openFile(filename)
        self.VideoPlay.video_name = filename
        self.VideoPlay.record_start_time = 0
        if filename != '':
            clip = VideoFileClip(filename)
            self.VideoPlay.record_end_time = clip.duration
            self.VideoPlay.video_duration = clip.duration
            self.VideoPlay.indices_list = [(0, clip.duration)]
        for v in self.icons:
            if v in self.icons:
                v.setStyleSheet("border: 10px solid grey;")
        self.videoSamples.clear()
        self.icons.clear()

    def add_to_concatenate(self, event, filename, label):
        self.videoSamples.append(filename)
        self.icons.append(label)
        label.setStyleSheet("border: 3px solid grey;")
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_last_clip()

    def delete_last_clip(self):
        if self.videoSamples:
            # Ia ultimul element din lista și il șterge
            last_clip = self.videoSamples.pop()
            last_icon = self.icons.pop()

            # Șterge QLabel din layout
            layout = self.layout()
            layout.removeWidget(last_icon)
            last_icon.deleteLater()
            
    def update_video_display(self, video_path):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.player.play()
        
    def start(self):
        # Presupunem că ai o comandă specifică de rulat, de exemplu ffmpeg sau o altă comandă
        self.terminal.start_process("ffmpeg", ["-i", "input.mp4", "-b:v", "64k", "output.mp4"])

    def show_sub_window(self, window):
        window.show()
        
    def showHelp(self):
        helpMessage = """
        Video Editor Help

        - Import Video: Click to open a video file.
        - Add Photo: Click to add a photo to the video.
        - Import/Rewrite Audio: Click to import or replace the audio track.
        - Keep Fragment: Click to keep the selected fragment of the video.
        - Remove Fragment: Click to remove the selected fragment of the video.
        - Add Subvideo/Image: Click to add a subvideo or image to the video.
        - Concatenate: Click to concatenate multiple video clips.
        - Fade in/Fade out: Click to apply fade in or fade out effects.
        - Rotate: Click to rotate the video.
        - Speed: Click to change the playback speed of the video.
        - Text: Click to add text to the video.
        - Brightness: Click to adjust the brightness of the video.
        - Contrast: Click to adjust the contrast of the video.
        - Color Temperature: Click to adjust the color balance of the video.
        - Export Audio Without Video: Click to export the audio track without the video.
        - Export Video Without Audio: Click to export the video without the audio track.
        - Optimize Resolution: Click to optimize the resolution of the video.
        - Show Terminal: Click to show the files on Video Aplication for more information
        
        For more information, refer to the user manual.
        """
        QMessageBox.information(self, "Help", helpMessage)
        
    def showUsageSteps(self):
        usageMessage = """
            Video Editor Usage Steps

            Step 1: Import Video - Click to open a video file.
            Step 2: Add Photo - Click to add a photo to the video.
            Step 3: Import/Rewrite Audio - Click to import or replace the audio track.
            Step 4: Keep Fragment - Click to keep the selected fragment of the video.
            Step 5: Remove Fragment - Click to remove the selected fragment of the video.
            Step 6: Add Subvideo/Image - Click to add a subvideo or image to the video.
            Step 7: Concatenate - Click to concatenate multiple video clips, if you import them in app.
            Step 8: Fade in/Fade out - After you have prepared your sequence, click to apply fade in or fade out effects.
            Step 9: Rotate - Click to rotate the video.
            Step 10: Speed - Click to change the playback speed of the video.
            Step 11: Text - Click to add text to the video, but will apear only in center of your video.
            Step 12: Brightness - Click to adjust the brightness of the video.
            Step 13: Contrast - Click to adjust the contrast of the video, by using Hue and Saturation.
            Step 14: Color Temperature - Click to adjust the color balance of the video.
            Step 15: Export Audio Without Video - Click to export the audio track without the video.
            Step 16: Export Video Without Audio - Click to export the video without the audio track.
            Step 17: Optimize Resolution - Click to optimize the file memory of the video.
            
            Your modifications will be saved after every steps in your origin file and every modification is ireversible.
            For more detailed information, refer to the user manual.
            """
        QMessageBox.information(self, "Usage Steps", usageMessage)
            
        
        
# Define the light and dark styles
light_style = """
    QWidget {
        background-color: #FFFFFF;
        color: #000000;
    }
    QToolBar {
        background: #F0F0F0;
    }
    QPushButton {
        background-color: #E0E0E0;
        color: #000000;
        border: none;
    }
    QPushButton:hover {
        background-color: #D0D0D0;
    }
    QLabel {
        color: #000000;
    }
"""

dark_style = """
    QWidget {
        background-color: #2E2E2E;
        color: #FFFFFF;
    }
    QToolBar {
        background: #3C3C3C;
    }
    QPushButton {
        background-color: #3C3C3C;
        color: #FFFFFF;
        border: none;
    }
    QPushButton:hover {
        background-color: #4C4C4C;
    }
    QLabel {
        color: #FFFFFF;
    }
"""

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("VideoPy")

        # Adauga favicon
        favicon_path = "prerequisite/favicon.ico"
        self.setWindowIcon(QIcon(favicon_path))
        
        w = 700
        h = 500

        self.resize(w, h)

        main_widget = MainWidget()

        #Crează un buton de import și setează stilul
        self.imp = QPushButton('Import Video')
        self.imp.setToolTip("Import a video file")  # Tooltip pentru import video
        self.imp.setStyleSheet("QPushButton { width: 100px; height: 50px; background-color: grey; color: white; }")
        self.imp.clicked.connect(main_widget.import_vid)
        main_widget.layout().addWidget(self.imp)
        

        # Crează un buton pentru Usage Steps
        self.usage_steps_button = QPushButton('Usage Steps')
        self.usage_steps_button.setToolTip("Show usage steps information")  # Tooltip pentru Usage Steps
        self.usage_steps_button.setStyleSheet("QPushButton { width: 100px; height: 50px; background-color: grey; color: white; }")
        self.usage_steps_button.clicked.connect(main_widget.showUsageSteps)
        main_widget.layout().addWidget(self.usage_steps_button)
        
        
        #Crează un buton de ajutor
        self.help_button = QPushButton('Help')
        self.help_button.setToolTip("Show help information")  # Tooltip pentru ajutor
        self.help_button.setStyleSheet("QPushButton { width: 100px; height: 50px; background-color: grey; color: white; }")
        self.help_button.clicked.connect(main_widget.showHelp)
        main_widget.layout().addWidget(self.help_button)

        

        self.setCentralWidget(main_widget)
        
        
        
        # Creează și adaugă bara de instrumente
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        # Adaugă acțiuni în bara de instrumente
        self.add_toolbar_actions(main_widget)

        # Creează meniu pentru schimbarea temei
        self.menu = self.menuBar()
        self.theme_menu = self.menu.addMenu("Theme")
        self.create_theme_actions()
        
        # Adaugă bara de stare
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)


    def add_toolbar_actions(self, main_widget):
        import_action = QAction("Import Video", self)
        import_action.setToolTip("Import a video file")
        import_action.triggered.connect(main_widget.import_vid)
        self.toolbar.addAction(import_action)

        add_photo_action = QAction("Add Photo", self)
        add_photo_action.setToolTip("Add a photo to the video")
        add_photo_action.triggered.connect(lambda: AddPhotoWindow(main_widget.VideoPlay, 200, 100).show())
        self.toolbar.addAction(add_photo_action)

        cut_action = QAction("Keep Fragment", self)
        cut_action.setToolTip("Keep only the selected fragment of the video")
        cut_action.triggered.connect(main_widget.VideoPlay.record_subclip_video)
        self.toolbar.addAction(cut_action)

        remove_action = QAction("Remove Fragment", self)
        remove_action.setToolTip("Remove the selected fragment of the video")
        remove_action.triggered.connect(main_widget.VideoPlay.remove_piece_video)
        self.toolbar.addAction(remove_action)

        concatenate_action = QAction("Concatenate", self)
        concatenate_action.setToolTip("Concatenate multiple video clips")
        concatenate_action.triggered.connect(lambda: ConcatenateWindow(main_widget.VideoPlay, 200, 100, main_widget.videoSamples).show())
        self.toolbar.addAction(concatenate_action)

        export_audio_action = QAction("Export Audio Without Video", self)
        export_audio_action.setToolTip("Export the audio track without the video")
        export_audio_action.triggered.connect(main_widget.VideoPlay.record_subclip_audio)
        self.toolbar.addAction(export_audio_action)
        
        optimize_action = QAction("Optimize Resolution", self)
        optimize_action.setToolTip("Optimize the resolution of the video")
        optimize_action.triggered.connect(lambda: OptimizerWindow(main_widget.VideoPlay, 200, 100).show())
        self.toolbar.addAction(optimize_action)


    def create_theme_actions(self):
        light_theme_action = QAction("Light Theme", self)
        light_theme_action.triggered.connect(lambda: self.set_theme("light"))
        self.theme_menu.addAction(light_theme_action)

        dark_theme_action = QAction("Dark Theme", self)
        dark_theme_action.triggered.connect(lambda: self.set_theme("dark"))
        self.theme_menu.addAction(dark_theme_action)

    def set_theme(self, theme):
        global light_style, dark_style
        if theme == "light":
            self.setStyleSheet(light_style)
        elif theme == "dark":
            self.setStyleSheet(dark_style)
            
    def update_status(self, message):
        self.statusbar.showMessage(message)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.showMaximized()

    app.exec_()
