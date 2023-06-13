from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout
import sys
class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.qle = QLineEdit(self)  # QLineEdit 위젯 생성

        layout = QVBoxLayout()
        layout.addWidget(self.qle)

        self.setLayout(layout)

        # QLineEdit 위젯의 텍스트가 변경될 때 호출되는 슬롯 연결
        self.qle.textChanged.connect(self.on_text_changed)

        self.show()
    def on_text_changed(self, text):
        print("The current text in the line edit is:", self.qle.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
