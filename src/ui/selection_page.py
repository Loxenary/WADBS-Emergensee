import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTextEdit, QStackedWidget,
                             QSizePolicy)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

class ModeSelectionPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Help Me Hear Section ---
        help_hear_button = QPushButton("Help me HEAR")
        help_hear_button.setFont(QFont("Arial", 18))
        help_hear_button.setStyleSheet("""
            QPushButton {
                background-color: #D37A7A; color: white; 
                border-radius: 15px; padding: 20px;
            }
            QPushButton:hover { background-color: #E08C8C; }
        """)
        
        # --- Help Me Speak Section ---
        help_speak_button = QPushButton("Help me SPEAK")
        help_speak_button.setFont(QFont("Arial", 18))
        help_speak_button.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0; color: #333; 
                border-radius: 15px; padding: 20px;
            }
            QPushButton:hover { background-color: #FFFFFF; }
        """)

        # --- Sub-buttons for SPEAK ---
        self.sign_button = QPushButton("I would like to SIGN")
        self.sign_button.setFont(QFont("Arial", 16))
        self.sign_button.clicked.connect(lambda: self.parent.navigateToPage(2)) # Go to Record Page
        
        self.type_button = QPushButton("I would like to TYPE")
        self.type_button.setFont(QFont("Arial", 16))
        self.type_button.clicked.connect(lambda: self.parent.navigateToPage(3)) # Go to Text Entry Page

        for btn in [self.sign_button, self.type_button]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #D37A7A; color: white; 
                    border-radius: 15px; padding: 15px;
                }
                QPushButton:hover { background-color: #E08C8C; }
            """)
            btn.hide() # Initially hidden

        help_speak_button.clicked.connect(self.toggle_speak_options)

        layout.addWidget(help_hear_button)
        layout.addWidget(help_speak_button)
        layout.addWidget(self.sign_button)
        layout.addWidget(self.type_button)
        layout.addStretch()

    def toggle_speak_options(self):
        # Show/hide the sign and type buttons
        self.sign_button.setVisible(not self.sign_button.isVisible())
        self.type_button.setVisible(not self.type_button.isVisible())