from PyQt5.QtWidgets import \
QApplication, QListWidget, QMainWindow, QDialog, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap, QCloseEvent, QTextCursor
from PyQt5 import QtGui, uic
from PyQt5.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import time
import pyperclip

import glob
import os

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--headless")
driver_service = Service(executable_path="chromedriver_win32/chromdriver.exe")
driver = webdriver.Chrome(service=driver_service, options=options)


def strokeReader():
    elements = driver.find_elements(By.CSS_SELECTOR, 'div.img_area > img[width="60"][height="60"]')
    page = 1
    for page, element in enumerate(elements, start=1):
        time.sleep(0.1)
        element.screenshot(f"strokes//stroke{page}.png")
    return page

class MyListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.text_edit = None
    
    def set_text_edit(self, text_edit):
        self.text_edit = text_edit
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            current_item = self.currentItem()
            if current_item:
                first_letter = current_item.text()[0]
                if self.text_edit:
                    self.text_edit.setText(self.text_edit.toPlainText() +  first_letter + ' ')
                    cursor = self.text_edit.textCursor()
                    cursor.movePosition(QTextCursor.End)
                    self.text_edit.setTextCursor(cursor)
        elif event.key() == Qt.Key_Up:
            if self.currentRow() == 0:
                lineEdit = self.window().findChild(ClickableLineEdit, "lineEdit")
                if lineEdit:
                    lineEdit.setFocus()
            
        super().keyPressEvent(event)


class ClickableLineEdit(QLineEdit):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pass
        super().mousePressEvent(event)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down:
            listWidget = self.window().findChild(MyListWidget, "listWidget")
            if listWidget:
                print("동작!")
                listWidget.setFocus()
                listWidget.setCurrentRow(0)
        else:
            super().keyPressEvent(event)



class MyApp(QMainWindow):
    url = ""
    

    def __init__(self):
        super().__init__()
    
        uic.loadUi("untitled.ui", self)
        self.initUI()

    def initUI(self):
        
        new_line_edit = ClickableLineEdit(self)
        new_line_edit.setObjectName("lineEdit")

        my_list_widget = MyListWidget(self)
        my_list_widget.setObjectName("listWidget")
        my_list_widget.set_text_edit(self.textEdit)
        my_list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.horizontalLayout.replaceWidget(self.lineEdit, new_line_edit)
        self.verticalLayout.replaceWidget(self.listWidget, my_list_widget)
        self.lineEdit.deleteLater()
        self.listWidget.deleteLater()
        self.lineEdit = new_line_edit
        self.listWidget = my_list_widget

        self.setWindowTitle('Web Crawler')
        self.dialog = MyDialog()
        self.btn.clicked.connect(self.start_crawling)
        self.btn.clicked.connect(self.dialog.initUI)
        self.lineEdit.returnPressed.connect(self.take_item) 

        self.pushButton_2.clicked.connect(self.undo)

        
        self.show()
    def on_item_double_clicked(self, item):
        self.lineEdit.setText(item.text()[0])

    def undo(self):
        self.textEdit.setText(self.textEdit.toPlainText()[:-2])
    
    def take_item(self):
        self.listWidget.clear()
        driver.get('https://hanja.dict.naver.com/#/search?query=' + self.lineEdit.text())
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.component_keyword.has-saving-function')))
        elements = driver.find_elements(By.CSS_SELECTOR, 'div[class="hanja_word"]')

        for element in elements:
            self.listWidget.addItem(element.text)
        
        


    def start_crawling(self):
        # files = glob.glob('strokes/*')
        # for f in files:
        #     os.remove(f)

        driver.get('https://hanja.dict.naver.com/#/search?query=' + self.lineEdit.text())
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'strong[class="highlight"]'))).click()
        

        driver.implicitly_wait(10)
        self.url = driver.current_url
        element = driver.find_element(By.CSS_SELECTOR, 'div.entry_title._guide_lang')
        element.screenshot('element_screenshot.png')

        element = driver.find_element(By.CSS_SELECTOR, "div.se-viewer.se-theme-default")
        element.screenshot('element_screenshot2.png')

        element = driver.find_element(By.CSS_SELECTOR, "ul.stroke_list")
        element.screenshot('element_screenshot3.png')
        num_page = strokeReader()
        self.dialog.setStrokeTurner(num_page)
          
    def closeEvent(self, event: QCloseEvent):
        driver.quit()
        if self.dialog is not None:
            self.dialog.close()
            self.dialog = None
        event.accept()
        
class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.totalPages = 0
        
        self.window = uic.loadUi("untitled2.ui")
        self.label_3 = None
    def initUI(self):
        #self.window.pushButton.clicked.connect(strokeReader)

        self.window.label.setPixmap(QPixmap('element_screenshot.png'))
        self.window.label.adjustSize()
        

        self.window.label_2.setPixmap(QPixmap('element_screenshot2.png'))
        self.window.label_2.adjustSize() 
        

        if self.label_3 is not None:
            self.label_3.deleteLater()

        self.label_3 = StrokeLabel(self.totalPages)
        self.window.verticalLayout.addWidget(self.label_3)
        
        self.label_3.setPixmap(QPixmap(f'strokes//stroke1.png'))
        self.label_3.adjustSize() 
        
        self.window.show()                   

    def setStrokeTurner(self, totalPages):
        self.totalPages = totalPages

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.label_3 = None
        return super().closeEvent(a0)

        
class StrokeLabel(QLabel):
    def __init__(self, totalPages):
        super().__init__()
        self.currentPages = 1
        self.totalPages = totalPages
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked!")
            self.currentPages += 1
            print(self.currentPages)
            self.setPixmap(QPixmap(f"strokes//stroke{self.currentPages}.png"))
            self.currentPages = self.currentPages % self.totalPages


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    