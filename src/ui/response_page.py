from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTextEdit, QStackedWidget,
                             QSizePolicy)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

class ResponsePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet("background-color: #F0F0F0; border-radius: 20px;")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)
        layout.setContentsMargins(30, 30, 30, 30)

        self.response_label = QLabel("Response will appear here...")
        self.response_label.setFont(QFont("Arial", 18))
        self.response_label.setStyleSheet("color: #333;")
        self.response_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.response_label.setWordWrap(True)

        ask_again_button = QPushButton("Ask Another Question")
        ask_again_button.setFont(QFont("Arial", 16))
        ask_again_button.setStyleSheet("QPushButton { background-color: #D37A7A; color: white; border-radius: 15px; padding: 15px; } QPushButton:hover { background-color: #E08C8C; }")        
        ask_again_button.clicked.connect(lambda: self.parent.navigateToPage(1))

        layout.addStretch()
        layout.addWidget(self.response_label)
        layout.addStretch()
        layout.addWidget(ask_again_button)

    def set_response(self, text):
        """Public method to update the response text."""
        self.response_label.setText(text)
