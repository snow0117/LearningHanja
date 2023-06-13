from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("Open a new window", self)
        self.button.clicked.connect(self.open_new_window)

    def open_new_window(self):
        self.new_window = QDialog(self)
        self.new_window.show()

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
