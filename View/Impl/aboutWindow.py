from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6 import uic

class AboutWindow(QWidget):
    def __init__(self, parent = None):
        super(AboutWindow, self).__init__(parent)
        self.start_Gui()
        
    def start_Gui(self):
        uic.loadUi(r'View/UI/About.ui', self)

        self.im1 = self.findChild(QLabel, 'label_4')
        self.im2 = self.findChild(QLabel, 'label_5')

        pixmap1 = QPixmap(r"View\Images\UdenarLogo.png")
        self.im1.setPixmap(pixmap1)
        self.im1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pixmap2 = QPixmap(r"View\Images\UdenarLogo2.png")
        self.im2.setPixmap(pixmap2)
        self.im2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.show()