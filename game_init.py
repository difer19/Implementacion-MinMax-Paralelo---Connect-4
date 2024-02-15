from PyQt6.QtWidgets import QApplication
import sys
from View.Impl.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = MainWindow()
    app.exec()