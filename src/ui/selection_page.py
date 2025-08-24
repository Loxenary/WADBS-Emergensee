import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTextEdit, QStackedWidget,
                             QSizePolicy)
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt, QSize

class ModeSelectionPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Header layout for the back button
        header_layout = QHBoxLayout()
        
        # Back Button
        back_btn = QPushButton("←")
        back_btn.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        back_btn.setFixedSize(50, 50)
        back_btn.setStyleSheet("""
            QPushButton {
                color: #FFFFFF;
                background-color: transparent;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        back_btn.clicked.connect(lambda: self.parent.navigateToPage(0)) 
        
        header_layout.addWidget(back_btn)
        header_layout.addStretch()

        # Buttons layout
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(25)
        buttons_layout.addStretch(1) 

        sign_button = self.create_mode_button("I would like to", "SIGN")
        type_button = self.create_mode_button("I would like to", "TYPE")
        speak_button = self.create_mode_button("I would like to", "SPEAK")
        
        sign_button.clicked.connect(lambda: self.parent.navigateToPage(2))
        type_button.clicked.connect(lambda: self.parent.navigateToPage(3)) 

        buttons_layout.addWidget(sign_button)
        buttons_layout.addWidget(type_button)
        buttons_layout.addWidget(speak_button)
        buttons_layout.addStretch(1) 

        # Add header and buttons to the main layout
        main_layout.addLayout(header_layout)
        main_layout.addLayout(buttons_layout)

    def create_mode_button(self, top_text, bottom_text):
        """Helper function to create a styled button with two lines of text."""
        button = QPushButton()
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button.setMinimumHeight(150) # Ensure buttons are large
        
        # Layout for the text inside the button
        button_layout = QVBoxLayout(button)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Top line of text
        top_label = QLabel(top_text)
        top_label.setFont(QFont("Inter", 22, QFont.Weight.Light))
        top_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Bottom line of text
        bottom_label = QLabel(bottom_text)
        bottom_label.setFont(QFont("Inter", 48, QFont.Weight.Bold))
        bottom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        button_layout.addWidget(top_label)
        button_layout.addWidget(bottom_label)

        button.setStyleSheet("""
            QPushButton {
                background-color: #990000; /* Dark Red */
                color: white;
                border: none;
                border-radius: 20px;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #B30000; /* Lighter Red on hover */
            }
            QLabel {
                background-color: transparent;
                color: white;
            }
        """)
        
        return button
