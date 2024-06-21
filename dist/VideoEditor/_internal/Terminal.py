from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import QProcess

class TerminalWidget(QWidget):
    def __init__(self, parent=None):
        super(TerminalWidget, self).__init__(parent)
        self.process = QProcess(self)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        layout.addWidget(self.textEdit)

        self.runButton = QPushButton("Show File", self)
        self.runButton.clicked.connect(self.on_start_button_clicked)
        layout.addWidget(self.runButton)

        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)


    def on_start_button_clicked(self):
        self.process.start("cmd.exe", ["/c", "echo Hello! && dir"])

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode('cp850')
        self.textEdit.append(data)

    def handle_stderr(self):
        data = self.process.readAllStandardError().data().decode('cp850')
        self.textEdit.append(data)

if __name__ == '__main__':
    app = QApplication([])
    terminal = TerminalWidget()
    terminal.show()
    app.exec_()
