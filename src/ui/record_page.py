import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QSizePolicy)
from PyQt6.QtGui import QFont, QPixmap, QImage
from PyQt6.QtCore import Qt, QMetaObject, pyqtSlot, Q_ARG

class RecordPage(QWidget):
    def __init__(self, parent, camera_service, response_service):
        super().__init__(parent)
        
        self.parent = parent
        self.camera_service = camera_service
        self.response_service = response_service
        self.is_recording = False

        # Main layout setup
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Video display label
        self.video_label = QLabel("Press RECORD to start")
        self.video_label.setFont(QFont("Arial", 16))
        self.video_label.setStyleSheet("background-color: #000; color: white; border-radius: 20px;")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Sentence display text area
        self.sentence_display = QTextEdit()
        self.sentence_display.setReadOnly(True)
        self.sentence_display.setFont(QFont("Arial", 16))
        self.sentence_display.setStyleSheet("background-color: #F0F0F0; border-radius: 15px; padding: 10px; color: black;")
        self.sentence_display.setFixedHeight(60)
        
        # Label to show the last saved sign
        self.last_saved_label = QLabel("Last Saved: None")
        self.last_saved_label.setFont(QFont("Arial", 12))
        self.last_saved_label.setStyleSheet("color: #AAA;")
        self.last_saved_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Controls Layout (Record button and action buttons) ---
        controls = QHBoxLayout()
        
        # Record button
        self.record_btn = QPushButton("RECORD\nNOW")
        self.record_btn.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.record_btn.setFixedSize(120, 120)
        self.record_btn.setStyleSheet("QPushButton { background-color: #D32F2F; color: white; border-radius: 60px; border: 4px solid white; }")
        
        # Action buttons (Delete, Okay, Save)
        actions = QVBoxLayout()
        self.delete_btn = QPushButton("Delete")
        self.okay_btn = QPushButton("Okay")
        self.save_btn = QPushButton("Save Sign")
        
        action_buttons = [self.delete_btn, self.okay_btn, self.save_btn]
        for btn in action_buttons:
            btn.setFont(QFont("Arial", 14))
            btn.setStyleSheet("QPushButton { background-color: #555; color: black; border-radius: 10px; padding: 10px; }")
            actions.addWidget(btn)
            
        controls.addWidget(self.record_btn)
        controls.addLayout(actions)
        
        # --- Assembling the Main Layout ---
        layout.addWidget(self.video_label)
        layout.addWidget(self.sentence_display)
        layout.addWidget(self.last_saved_label)
        layout.addLayout(controls)
        
        # Back button
        back_btn = QPushButton("Back to Menu")
        back_btn.clicked.connect(lambda: self.parent.navigateToPage(1))
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignRight)

        # --- Signal and Slot Connections ---
        self.record_btn.clicked.connect(self.toggle_recording)
        self.delete_btn.clicked.connect(self.camera_service.delete_last_char)
        self.okay_btn.clicked.connect(self.confirm_sentence)
        self.save_btn.clicked.connect(self.camera_service.save_current_frame_data)
        self.camera_service.frame_ready.connect(self.update_video_frame)
        self.camera_service.sentence_updated.connect(self.update_sentence_display)
        self.camera_service.data_saved_signal.connect(self.update_last_saved_display)

    def toggle_recording(self):
        """Starts or stops the camera recording."""
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.record_btn.setText("STOP")
            self.record_btn.setStyleSheet("QPushButton { background-color: #1976D2; color: white; border-radius: 60px; border: 4px solid white; }")
            QMetaObject.invokeMethod(self.camera_service, "start_camera", Qt.ConnectionType.QueuedConnection)
        else:
            self.record_btn.setText("RECORD\nNOW")
            self.record_btn.setStyleSheet("QPushButton { background-color: #D32F2F; color: white; border-radius: 60px; border: 4px solid white; }")
            QMetaObject.invokeMethod(self.camera_service, "stop_camera", Qt.ConnectionType.QueuedConnection)
            self.video_label.setText("Press RECORD to start")

    @pyqtSlot(QImage)
    def update_video_frame(self, qt_image):
        """Updates the video label with a new frame from the camera."""
        scaled_pixmap = QPixmap.fromImage(qt_image).scaled(self.video_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.video_label.setPixmap(scaled_pixmap)

    @pyqtSlot(str)
    def update_sentence_display(self, sentence):
        """Updates the text in the sentence display box."""
        self.sentence_display.setText(sentence)

    @pyqtSlot(str)
    def update_last_saved_display(self, label):
        """Updates the 'Last Saved' label."""
        self.last_saved_label.setText(f"Last Saved: {label}")

    def confirm_sentence(self):
        """Confirms the current sentence and sends it for processing."""
        full_sentence = self.camera_service.get_full_sentence()
        QMetaObject.invokeMethod(self.response_service, "process_final_sentence", Qt.ConnectionType.QueuedConnection, Q_ARG(str, full_sentence))
        if self.is_recording:
            self.toggle_recording()
