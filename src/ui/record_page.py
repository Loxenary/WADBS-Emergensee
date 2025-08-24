import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QSizePolicy)
from PyQt6.QtGui import QFont, QPixmap, QImage
from PyQt6.QtCore import Qt, QMetaObject, pyqtSlot, Q_ARG

class RecordPage(QWidget):
    def __init__(self, parent, camera_service, response_service):
        super().__init__(parent)

        # Init Variables
        
        self.parent = parent
        self.camera_service = camera_service
        self.response_service = response_service
        self.is_recording = False

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        header_layout = QHBoxLayout()
        back_btn = QPushButton("←")
        back_btn.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        back_btn.setFixedSize(50, 50)
        back_btn.setStyleSheet("""
            QPushButton { color: white; background-color: transparent; border: none; border-radius: 25px; }
            QPushButton:hover { background-color: #444444; }
        """)
        back_btn.clicked.connect(self.handle_back_button)
        header_layout.addWidget(back_btn)
        header_layout.addStretch()

        self.video_container = QWidget()
        self.video_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.video_container.setStyleSheet("background-color: #E0E0E0; border-radius: 30px;")
        
        video_layout = QVBoxLayout(self.video_container)
        video_layout.setContentsMargins(20, 20, 20, 20)

        self.live_translation_label = QLabel("LIVE TRANSLATION")
        self.live_translation_label.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        self.live_translation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.live_translation_label.setStyleSheet("color: #990000; background-color: transparent;")
        
        self.video_label = QLabel("Press the button to start recording")
        self.video_label.setFont(QFont("Arial", 16))
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.video_label.setStyleSheet("background-color: transparent; color: #555;")

        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(20)
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.retake_btn = QPushButton("⟳\nRetake")
        self.retake_btn.setFont(QFont("Arial", 14))
        self.retake_btn.setFixedSize(90, 90)
        self.retake_btn.setStyleSheet("""
            QPushButton { background-color: transparent; color: #990000; border-radius: 45px; border: 3px solid #990000; }
            QPushButton:hover { background-color: #F0F0F0; }
        """)

        self.record_btn = QPushButton()
        self.record_btn.setFixedSize(110, 110)
        self.record_btn.setStyleSheet("""
            QPushButton { background-color: #D32F2F; border-radius: 55px; border: 5px solid rgba(255, 255, 255, 0.5); }
            QPushButton:hover { background-color: #E53935; }
        """)
        
        self.save_word_btn = QPushButton("Save\nWord")
        self.save_word_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.save_word_btn.setFixedSize(90, 90)
        self.save_word_btn.setStyleSheet("""
            QPushButton { background-color: #4CAF50; color: white; border-radius: 45px; border: 3px solid white; }
            QPushButton:hover { background-color: #66BB6A; }
        """)

        controls_layout.addStretch()
        controls_layout.addWidget(self.retake_btn)
        controls_layout.addWidget(self.record_btn)
        controls_layout.addWidget(self.save_word_btn)
        controls_layout.addStretch()

        self.helper_text = QLabel("Press button to start recording")
        self.helper_text.setFont(QFont("Arial", 12))
        self.helper_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.helper_text.setStyleSheet("color: #990000;")

        video_layout.addWidget(self.live_translation_label)
        video_layout.addWidget(self.video_label, 1)
        video_layout.addLayout(controls_layout)
        video_layout.addWidget(self.helper_text)

        self.final_sentence_display = QLabel("Your sentence will appear here...")
        self.final_sentence_display.setFont(QFont("Arial", 14))
        self.final_sentence_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.final_sentence_display.setStyleSheet("color: white; padding: 10px;")
        self.final_sentence_display.setWordWrap(True)
        self.final_sentence_display.setFixedHeight(60)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.video_container)
        main_layout.addWidget(self.final_sentence_display)
        
        self.record_btn.clicked.connect(self.toggle_recording)
        self.retake_btn.clicked.connect(self.camera_service.clear_all)
        self.save_word_btn.clicked.connect(self.camera_service.save_current_word)
        
        self.camera_service.frame_ready.connect(self.update_video_frame)
        self.camera_service.sentence_updated.connect(self.update_live_translation)
        self.camera_service.full_sentence_updated.connect(self.update_final_sentence_display)

    def toggle_recording(self):
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.helper_text.setText("Press button to finish recording")
            self.record_btn.setStyleSheet("QPushButton { background-color: #990000; border-radius: 55px; border: 5px solid white; }")
            QMetaObject.invokeMethod(self.camera_service, "start_camera", Qt.ConnectionType.QueuedConnection)
        else:
            full_sentence = self.camera_service.get_full_sentence()
            QMetaObject.invokeMethod(self.response_service, "process_final_sentence", Qt.ConnectionType.QueuedConnection, Q_ARG(str, full_sentence))
            self.stop_and_reset()

    def reset_ui_text(self):
        """Resets the text elements of the UI."""
        self.helper_text.setText("Press button to start recording")
        self.video_label.setText("Press the button to start recording")
        self.live_translation_label.setText("LIVE TRANSLATION")
        self.final_sentence_display.setText("Your sentence will appear here...")

    def stop_and_reset(self):
        """Stops the camera and resets the UI."""
        self.is_recording = False
        self.record_btn.setStyleSheet("QPushButton { background-color: #D32F2F; border-radius: 55px; border: 5px solid rgba(255, 255, 255, 0.5); }")
        QMetaObject.invokeMethod(self.camera_service, "stop_camera", Qt.ConnectionType.QueuedConnection)
        self.reset_ui_text()

    def handle_back_button(self):
        """Stops camera before navigating back."""
        if self.is_recording:
            self.stop_and_reset()
        self.parent.navigateToPage(1)

    @pyqtSlot(QImage)
    def update_video_frame(self, qt_image):
        if self.is_recording:
            self.video_label.setText("") 
            scaled_pixmap = QPixmap.fromImage(qt_image).scaled(
            self.video_label.size(), 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.video_label.setPixmap(scaled_pixmap)

    @pyqtSlot(str)
    def update_live_translation(self, current_letters):
        """Updates the live translation text (current word being spelled)."""
        if current_letters:
            self.live_translation_label.setText(current_letters)
        else:
            self.live_translation_label.setText("LIVE TRANSLATION")
    
    @pyqtSlot(str)
    def update_final_sentence_display(self, sentence):
        """Updates the final sentence display at the bottom."""
        if sentence:
            self.final_sentence_display.setText(sentence)
        else:
            self.final_sentence_display.setText("Your sentence will appear here...")

