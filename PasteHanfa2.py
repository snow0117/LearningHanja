from PyQt5.QtWidgets import \
QApplication, QWidget, QVBoxLayout, QPushButton, QMainWindow, QDialog, QLabel, QLineEdit, QListWidget, QTextEdit
import sys
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.list_widget = QListWidget()
        self.text_edit = QTextEdit()
        
        for letter in ['a', 'b', 'c', 'd', 'e']:
            self.list_widget.addItem(letter)
            
        self.list_widget.itemActivated.connect(self.update_text_edit)
        
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.text_edit)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        
        self.setCentralWidget(central_widget)
        
    def update_text_edit(self, item):
        self.text_edit.setText(item.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())