from PyQt5.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
import sys

class DragDropLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setDragEnabled(True)  # 이 텍스트 필드에서 드래그를 허용합니다.

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return

        drag = QDrag(self)
        mimedata = QMimeData()

        mimedata.setText(self.text())  # 드래그하는 텍스트를 설정합니다.
        drag.setMimeData(mimedata)

        drag.exec_(Qt.MoveAction)

    def dropEvent(self, event):
        if event.mimeData().hasText():  # 드랍하는 데이터가 텍스트인 경우
            self.setText(event.mimeData().text())  # 드랍한 텍스트를 출력합니다.

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():  # 드래그하는 데이터가 텍스트인 경우
            event.accept()
        else:
            event.ignore()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        for _ in range(2):  # 두 개의 텍스트 필드를 생성합니다.
            edit = DragDropLineEdit()
            vbox.addWidget(edit)

        self.setLayout(vbox)

        self.setWindowTitle('Drag and Drop')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
