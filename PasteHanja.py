from PyQt5.QtWidgets import \
QApplication, QWidget, QVBoxLayout, QPushButton, QMainWindow, QDialog, QLabel
from PyQt5.QtGui import QPixmap, QCloseEvent, QIcon
from PyQt5 import uic
from PyQt5.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import sys
import time
import pyperclip

options = Options()
options.add_experimental_option("detach", True)
#options.add_argument("--headless")
driver_service = Service(executable_path="chromedriver_win32/chromdriver.exe")
driver = webdriver.Chrome(service=driver_service, options=options)


class MyApp(QMainWindow):
    url = ""
    
    def __init__(self):
        super().__init__()
    
        uic.loadUi("untitled.ui", self)
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle('Web Crawler')
        self.dialog = MyDialog()
        self.btn.clicked.connect(self.start_crawling)
        self.btn.clicked.connect(self.dialog.initUI)
        
        self.show()
    
    def start_crawling(self):
        
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

        elements = driver.find_elements(By.CSS_SELECTOR, 'div.img_area >  img[width="60"][height="60"]')

        self.page = 1
        for self.page, element in enumerate(elements, start=1):
            element.screenshot(f"strokes//stroke{self.page}.png")

        self.dialog.setStrokeTurner(self.page)


                                
    def mini(self):
        driver.minimize_window()

        
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
    def initUI(self):
        
        self.window.label.setPixmap(QPixmap('element_screenshot.png'))
        self.window.label.adjustSize()
        

        self.window.label_2.setPixmap(QPixmap('element_screenshot2.png'))
        self.window.label_2.adjustSize() 
        
        

        self.label_3 = StrokeLabel(self.totalPages)
        
        self.label_3.setPixmap(QPixmap(f'strokes//stroke1'))
        self.label_3.adjustSize() 
        self.window.horizontalLayout.addWidget(self.label_3)
        self.window.show()

    def setStrokeTurner(self, totalPages):
        self.totalPages = totalPages

        
class StrokeLabel(QLabel):
    def __init__(self, totalPages):
        super().__init__()
        self.currentPages = 1
        self.totalPages = totalPages
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked!")
            self.currentPages += 1
            self.setPixmap(QPixmap(f"strokes//stroke{self.currentPages}"))
            self.currentPages = self.currentPages % self.totalPages



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    