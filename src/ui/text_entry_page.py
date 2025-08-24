import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QListWidget)                             
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt,  QMetaObject, Q_ARG

class TextEntryPage(QWidget):
    def __init__(self, parent, response_service, text_processor):
        super().__init__(parent)
        self.parent = parent
        self.response_service = response_service
        self.text_processor = text_processor

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)
        layout.setContentsMargins(30,30,30,30)
        
        title = QLabel("How can we help you?")
        title.setFont(QFont("Arial", 20))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter text here...")
        self.text_input.setFont(QFont("Arial", 14))
        self.text_input.setStyleSheet("background-color: #F0F0F0; border-radius: 15px; padding: 10px; color: black;")
        self.text_input.setFixedHeight(150)
        
        self.suggestion_list = QListWidget()
        self.suggestion_list.setFont(QFont("Arial", 12))
        self.suggestion_list.setStyleSheet("background-color: #444; color: white; border-radius: 10px;")
        self.suggestion_list.setFixedHeight(80)
        self.suggestion_list.hide()
        
        submit = QPushButton("Submit")
        submit.setFont(QFont("Arial", 16))
        submit.setStyleSheet("QPushButton { background-color: #D37A7A; color: white; border-radius: 15px; padding: 15px; }")
        submit.clicked.connect(self.submit_text)
        back = QPushButton("Back") 
        back.clicked.connect(lambda: self.parent.navigateToPage(1))

        
        layout.addWidget(title)
        layout.addWidget(self.text_input)
        layout.addWidget(self.suggestion_list)
        layout.addWidget(submit)
        layout.addStretch()
        layout.addWidget(back, alignment=Qt.AlignmentFlag.AlignRight)

        self.text_input.textChanged.connect(self.update_suggestions)
        self.suggestion_list.itemClicked.connect(self.apply_suggestion)

    def update_suggestions(self):
        current_text = self.text_input.toPlainText()
        suggestions = self.text_processor.get_suggestions(current_text)
        self.suggestion_list.clear()
        if suggestions:
            self.suggestion_list.addItems(suggestions)
            self.suggestion_list.show()
        else:
            self.suggestion_list.hide()

    def apply_suggestion(self, item):
        suggestion = item.text()
        current_text = self.text_input.toPlainText()
        words = current_text.split()
        words[-1] = suggestion # Replace the partial word
        new_text = " ".join(words) + " "
        self.text_input.setText(new_text)
        self.suggestion_list.hide()

    def submit_text(self):
        QMetaObject.invokeMethod(self.response_service, "process_final_sentence", Qt.ConnectionType.QueuedConnection, Q_ARG(str, self.text_input.toPlainText()))
        self.text_input.clear()

