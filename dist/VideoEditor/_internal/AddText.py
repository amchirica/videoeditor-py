from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, \
    QComboBox, QLineEdit
from PyQt5.QtGui import QIcon
import sys
from random import randint
from VideoSelf import VideoWindow

class AddTextWindow(QWidget):
    """
    Această clasă reprezintă o fereastră pentru adăugarea textului pe un videoclip.
    Este un QWidget care va apărea ca o fereastră independentă.
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
        self.setWindowTitle("Add Text on Video")

        # Configurarea layout-ului principal
        self.layout = QVBoxLayout()

        # Crearea butonului pentru adăugarea textului
        self.final = QPushButton('Add Text')
        
        # Crearea câmpului de text pentru introducerea textului
        self.text = QLineEdit()
        self.text.setPlaceholderText("Enter Text")
        
        # Crearea câmpului de text pentru dimensiunea fontului
        self.font_size = QLineEdit()
        self.font_size.setPlaceholderText("Enter Font Size")
        
        # Crearea ComboBox-ului pentru selectarea culorii textului
        self.text_color = QComboBox()
        colors = ['black', 'white', 'red', 'blue']
        self.text_color.addItems(colors)
        
        # Crearea layout-ului pentru poziționarea textului
        self.poslayout = QHBoxLayout()
        self.x = QLineEdit()
        self.x.setPlaceholderText("x")
        self.y = QLineEdit()
        self.y.setPlaceholderText("y")
        self.note = QLabel("Pos:")
        
        # Crearea ComboBox-ului pentru alinierea textului
        self.align = QComboBox()
        places = ['center']
        self.align.addItems(places)
        
        # Adăugarea elementelor în layout-ul pentru poziționare
        self.poslayout.addWidget(self.note)
        self.poslayout.addWidget(self.align)
        self.poslayout.addWidget(self.x)
        self.poslayout.addWidget(self.y)

        # Adăugarea elementelor în layout-ul principal
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.font_size)
        self.layout.addWidget(self.text_color)
        self.layout.addLayout(self.poslayout)
        self.layout.addWidget(self.final)
        
        # Conectarea butonului pentru adăugarea textului la funcția din clasa VideoWindow
        self.final.clicked.connect(lambda: self.window.add_text_video(
            self,
            self.text.text(),
            self.font_size.text(),
            self.text_color.currentText(),
            self.align.currentText()
        ))

        self.setLayout(self.layout)