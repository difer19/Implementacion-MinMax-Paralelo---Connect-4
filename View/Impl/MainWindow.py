from PyQt6.QtWidgets import *
from PyQt6 import uic
from View.Impl.gameWindow import GameWindow
from View.Impl.aboutWindow import AboutWindow
from View.Impl.settingsWindow import SettingsWindow
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.startGUI()
        
    def startGUI(self):
        uic.loadUi(r'View/UI/MainView.ui', self)

        self.setWindowTitle("Connect 4")

        self.central = self.findChild(QWidget, 'centralwidget')
        self.menu = self.central.findChild(QWidget, 'widget')
        self.main = self.central.findChild(QStackedWidget, 'stackedWidget_2')
        self.play = self.menu.findChild(QPushButton, 'play')
        self.settings = self.menu.findChild(QPushButton, 'settings')
        self.about = self.menu.findChild(QPushButton, 'about')
        self.exit = self.menu.findChild(QPushButton, 'exit')

        self.game_window = GameWindow()
        self.settings_window = SettingsWindow()
        self.about_window = AboutWindow()

        self.main.addWidget(self.game_window)
        self.main.addWidget(self.settings_window)
        self.main.addWidget(self.about_window)

        self.play.setEnabled(False)

        self.play.clicked.connect(self.charge_play)
        self.about.clicked.connect(self.charge_about)
        self.settings.clicked.connect(self.charge_settings)
        self.exit.clicked.connect(lambda : sys.exit())
        
        self.show()
    
    def charge_play(self):
        self.main.currentWidget().destroy()
        self.play.setEnabled(False)
        self.settings.setEnabled(True)
        self.about.setEnabled(True)
        self.main.setCurrentIndex(0)

    def charge_settings(self):
        self.main.currentWidget().destroy()
        self.play.setEnabled(True)
        self.settings.setEnabled(False)
        self.about.setEnabled(True)
        self.main.setCurrentIndex(1)
        self.main.widget(1).charge_current_settings()

    def charge_about(self):
        self.main.currentWidget().destroy()
        self.play.setEnabled(True)
        self.settings.setEnabled(True)
        self.about.setEnabled(False)
        self.main.setCurrentIndex(2)

    def exit_application(self):
        pass
