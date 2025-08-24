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
        
        self.timer = None

    def showEvent(self, event):
        """This method is called every time the widget is shown."""
        # Start the timer whenever the page becomes visible.
        if self.timer is None:
            self.timer = self.startTimer(2000) 
        super().showEvent(event)

    def timerEvent(self, event):
        """This method is called when the timer finishes."""
        if self.timer is not None:
            self.killTimer(self.timer)
            self.timer = None
        
        # Navigate to the selection page.
        self.parent.navigateToPage(1)
