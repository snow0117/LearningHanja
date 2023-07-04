from PyQt5.QtWidgets import \
QApplication, QListWidget, QMainWindow, QDialog, QLabel, QLineEdit, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QCloseEvent, QTextCursor
from PyQt5 import QtGui, uic
from PyQt5.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import sys
import time

import glob
import os

from threading import Thread

from queue import Queue
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--headless")
driver_service = Service(executable_path="chromedriver_win32/chromdriver.exe")
driver1 = webdriver.Chrome(service=driver_service, options=options)
driver2 = webdriver.Chrome(service=driver_service, options=options)



def start_naver_crawling(keyword):

    driver1.get('https://hanja.dict.naver.com/#/search?query=' + keyword)
    wait = WebDriverWait(driver1, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'strong[class="highlight"]'))).click()
    

    driver1.implicitly_wait(10)
    element = driver1.find_element(By.CSS_SELECTOR, 'div.entry_title._guide_lang')
    element.screenshot('element_screenshot.png')

    driver1.implicitly_wait(10)
    element = driver1.find_element(By.CSS_SELECTOR, "div.se-main-container")
    element.screenshot('element_screenshot2.png')


def start_currency_crawling(keyword, result_queue):
    driver2.implicitly_wait(10)
    driver2.get('http://tonghanja.com/?s=' + keyword)
    

    driver2.set_window_size(1920, 1080)
    element = driver2.find_element(By.CSS_SELECTOR, 'img.alignnone.size-full')
    
    
    element.screenshot('currency.png')
    
    
    driver2.implicitly_wait(10)
    element = driver2.find_element(By.CSS_SELECTOR, 'div.entry-content')
    html = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    spans = soup.select('span[style*="font-size: 15px"]')

    print(spans[-1].text)

    

    


    result_queue.put(spans[-1].text)





def strokeReader():
    elements = driver1.find_elements(By.CSS_SELECTOR, 'div.img_area > img[width="60"][height="60"]')
    page = 1
    for page, element in enumerate(elements, start=1):
        if page == 2:
            time.sleep(0.1)
        element.screenshot(f"strokes//stroke{page}.png")
    return page



class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
    
        uic.loadUi("untitled.ui", self)
        
        self.dialog = MyDialog()
        self.initUI()
    def initUI(self):
        new_line_edit = self.ClickableLineEdit(self)
        new_line_edit.setObjectName("lineEdit")

        my_list_widget = self.MyListWidget(self)
        my_list_widget.setObjectName("listWidget")
        my_list_widget.set_text_edit(self.textEdit)
        my_list_widget.itemClicked.connect(self.on_item_clicked)

        self.horizontalLayout.replaceWidget(self.lineEdit, new_line_edit)
        self.verticalLayout.replaceWidget(self.listWidget, my_list_widget)
        self.lineEdit.deleteLater()
        self.listWidget.deleteLater()
        self.lineEdit = new_line_edit
        self.listWidget = my_list_widget

        self.setWindowTitle('Web Crawler')
        
        self.btn.clicked.connect(self.ClickedPushButton)
        self.btn.clicked.connect(self.dialog.initUI)
        self.lineEdit.returnPressed.connect(self.take_item) 
        self.pushButton.clicked.connect(self.copyText)
        

        self.pushButton_2.clicked.connect(self.undo)

        
        self.show()



    class MyListWidget(QListWidget):
        def __init__(self, outerClass=None):
            super().__init__(outerClass)
            
            self.outerClass = outerClass
            self.text_edit = None
        
        def set_text_edit(self, text_edit):
            self.text_edit = text_edit
        

        
        def keyPressEvent(self, event):
            if event.key() == Qt.Key_Return:
                self.outerClass.ClickedPushButton()
                self.dialog = self.outerClass.dialog
                self.dialog.setStrokeTurner(strokeReader())
                self.dialog.initUI()
            elif event.key() == Qt.Key_Up:
                lineEdit = self.window().findChild(MyApp.ClickableLineEdit, "lineEdit")
                if self.currentRow() == 0:
                    lineEdit.setFocus()
                else:
                    lineEdit.setText(self.item(self.currentRow()-1).text()[0])
            elif event.key() == Qt.Key_Down:
                if self.currentRow() < self.count()-1:
                    lineEdit = self.window().findChild(MyApp.ClickableLineEdit, "lineEdit")
                    lineEdit.setText(self.item(self.currentRow()+1).text()[0])
                    
            elif event.key() == Qt.Key_Space:
                # lineEdit = self.window().findChild(ClickableLineEdit, "lineEdit")
                # if lineEdit:
                #     lineEdit.setText(self.currentItem().text()[0])
                current_item = self.currentItem()
                if current_item:
                    first_letter = current_item.text()[0]
                    if self.text_edit:
                        self.text_edit.setText(self.text_edit.toPlainText() +  first_letter + ' ')
                        cursor = self.text_edit.textCursor()
                        cursor.movePosition(QTextCursor.End)
                        self.text_edit.setTextCursor(cursor)
            super().keyPressEvent(event)

    class ClickableLineEdit(QLineEdit):
        def mousePressEvent(self, event):
            if event.button() == Qt.LeftButton:
                pass
            super().mousePressEvent(event)
        def keyPressEvent(self, event):
            if event.key() == Qt.Key_Down:
                listWidget = self.window().findChild(MyApp.MyListWidget, "listWidget")
                if listWidget:
                    listWidget.setFocus()
                    listWidget.setCurrentRow(0)
                    self.setText(listWidget.currentItem().text()[0])
            else:
                super().keyPressEvent(event)


    
    def copyText(self):
        text = self.textEdit.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
    
    def on_item_clicked(self, item):
        self.lineEdit.setText(item.text()[0])

    def undo(self):
        self.textEdit.setText(self.textEdit.toPlainText()[:-2])
    
    def take_item(self):
        self.listWidget.clear()
        driver1.get('https://hanja.dict.naver.com/#/search?query=' + self.lineEdit.text())
        wait = WebDriverWait(driver1, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.component_keyword.has-saving-function')))
        elements = driver1.find_elements(By.CSS_SELECTOR, 'div[class="hanja_word"]')

        for element in elements:
            self.listWidget.addItem(element.text)
        
    def ClickedPushButton(self):
        keyword = self.lineEdit.text()

        result_queue = Queue()
        thread2 = Thread(target=start_currency_crawling, args=(keyword, result_queue))
        thread1 = Thread(target=start_naver_crawling, args=(keyword, ))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        num_page = strokeReader()
        self.dialog.setStrokeTurner(num_page)

        word = result_queue.get()
       
        self.dialog.setWord(word)
          
    def closeEvent(self, event: QCloseEvent):
        driver1.quit()
        if self.dialog is not None:
            self.dialog.close()
            self.dialog = None
        event.accept()
        
class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.totalPages = 0
        
        self.window = uic.loadUi("untitled2.ui")
        self.window.setStyleSheet("background-color: white;")

        self.label_3 = None
    def initUI(self):
        #self.window.pushButton.clicked.connect(strokeReader)

        self.window.label.setPixmap(QPixmap('element_screenshot.png'))
        self.window.label.adjustSize()
        

        self.window.label_2.setPixmap(QPixmap('element_screenshot2.png'))
        self.window.label_2.adjustSize() 

        self.window.label_5.setPixmap(QPixmap('currency.png'))
        self.window.label_5.adjustSize() 



        if self.label_3 is not None:
            self.label_3.deleteLater()

        self.label_3 = StrokeLabel(self.totalPages)
        self.window.verticalLayout.addWidget(self.label_3)
        
        self.label_3.setPixmap(QPixmap(f'strokes//stroke1.png'))
        self.label_3.adjustSize() 

        
        self.window.show()                   

    def setStrokeTurner(self, totalPages):
        self.totalPages = totalPages

    def setWord(self, word):
        self.window.label_6.setText(word)
        self.window.label_6.adjustSize()

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
            self.currentPages += 1
            self.setPixmap(QPixmap(f"strokes//stroke{self.currentPages}.png"))
            self.currentPages = self.currentPages % self.totalPages

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    