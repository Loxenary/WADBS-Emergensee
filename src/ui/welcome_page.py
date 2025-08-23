from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTextEdit, QStackedWidget,
                             QSizePolicy)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

class WelcomePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background-color: #D37A7A; border-radius: 20px;")

        welcome_label = QLabel("Welcome to")
        welcome_label.setFont(QFont("Arial", 24))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("color: white;")

        logo_label = QLabel("HEAR")
        logo_label.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("color: white;")

        layout.addWidget(welcome_label)
        layout.addWidget(logo_label)

        self.timer = self.startTimer(2000) 

    def timerEvent(self, event):
        self.killTimer(self.timer)
        self.parent.navigateToPage(1)