from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5 import uic

app = QApplication([])
window = uic.loadUi("qv.ui")


window.layout().addWidget(QLabel("NewLabel"))
window.layout().addWidget(QLabel("NewLabel"))



window.show()
app.exec()