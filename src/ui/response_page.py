# response_page.py (Redesigned)

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QSizePolicy, QTextEdit, QFrame)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class ResponsePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet("background-color: #F4F6F6;") 

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Card for Question and Response
        content_card = QFrame()
        content_card.setObjectName("contentCard")
        content_card.setStyleSheet("""
            #contentCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
        """)
        card_layout = QVBoxLayout(content_card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(15)
    

        our_response_title = QLabel("Our Response")
        our_response_title.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        our_response_title.setStyleSheet("color: #333333; margin-top: 15px; margin-bottom: 5px;")

        self.response_display = QTextEdit()
        self.response_display.setReadOnly(True)
        self.response_display.setFont(QFont("Inter", 16))
        self.response_display.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                color: #111111;
                border: none;
                padding: 5px;
            }
        """)
        
        # Assemble the card
        card_layout.addWidget(our_response_title)
        card_layout.addWidget(self.response_display, 1)

        # Control Button
        self.ask_again_button = QPushButton("Ask Another Question")
        self.ask_again_button.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.ask_again_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ask_again_button.setStyleSheet("""
            QPushButton { 
                background-color: #D37A7A; 
                color: white; 
                border-radius: 12px; 
                padding: 18px; 
                border: none;
            } 
            QPushButton:hover { 
                background-color: #E08C8C; 
            }
        """)        
        self.ask_again_button.clicked.connect(lambda: self.parent.navigateToPage(1))

        # Assemble the Main Layout
        main_layout.addWidget(content_card)
        main_layout.addStretch()
        main_layout.addWidget(self.ask_again_button)

    def set_response(self, data: dict):
        """Public method to update the page with data from the ResponseService."""
        question = data.get("question", "Question not found.")
        answer = data.get("answer", "Sorry, no response was generated.")        
        print(f"DEBUG: Updating UI with Question='{question}', Answer='{answer}'")
        
        self.response_display.setText(answer)