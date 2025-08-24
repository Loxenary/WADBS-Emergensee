# camera_service.py (Corrected and Optimized)

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer
from PyQt6.QtGui import QImage
import cv2
from src.core.sign_recognizer import SignRecognizer
from src.config.config import AppConfig

class CameraService(QObject):
    frame_ready = pyqtSignal(QImage)
    sentence_updated = pyqtSignal(str)
    full_sentence_updated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.cap = None
        self.recognizer = SignRecognizer()
        
        # State for sentence building
        self.current_letters = []
        self.words = []
        
        # State for prediction stability
        self.prediction_buffer = "" # Holds the letter being evaluated
        self.buffer_counter = 0
        self.last_known_prediction = "" # The most recent prediction from the model

        # State for optimization
        self.frame_count = 0 
        self.process_every_n_frame = 3 # Run the slow model 1 out of every 3 frames

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._process_single_frame)

    @pyqtSlot()
    def start_camera(self):
        if not self.timer.isActive():
            self.clear_all()
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened(): return
            self.timer.start(33) # ~30 FPS

    @pyqtSlot()
    def stop_camera(self):
        if self.timer.isActive():
            self.timer.stop()
            if self.cap: 
                self.cap.release()
                self.cap = None

    def _process_single_frame(self):
        if not self.cap: return
        ret, frame = self.cap.read()
        if not ret: return

        frame = cv2.flip(frame, 1)
        
        annotated_frame = self.recognizer.detect_and_draw_landmarks(frame)
        
        # Run the heavy prediction model on the most recent landmarks.
        self.frame_count += 1
        if self.frame_count % self.process_every_n_frame == 0:
            
            self.last_known_prediction = self.recognizer.predict_from_last_landmarks()

        # The stability logic now runs every frame using the last prediction we got
        # This makes the recording feel responsive again.
        if self.last_known_prediction:
            if self.last_known_prediction == self.prediction_buffer:
                self.buffer_counter += 1
            else:
                self.prediction_buffer = self.last_known_prediction
                self.buffer_counter = 1
            
            if self.buffer_counter == AppConfig.STABILITY_THRESHOLD:
                self.current_letters.append(self.prediction_buffer)
                self.sentence_updated.emit("".join(self.current_letters))
                
                # Reset for the next letter
                self.prediction_buffer = ""
                self.buffer_counter = 0
                self.last_known_prediction = ""
    
        # Emit the fully annotated frame to the UI.
        rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.frame_ready.emit(qt_image)

    @pyqtSlot()
    def save_current_word(self):
        # This function remains the same
        if not self.current_letters: return
        word = "".join(self.current_letters)
        self.words.append(word)
        self.current_letters = []
        self.prediction_buffer = ""
        self.buffer_counter = 0
        self.sentence_updated.emit("")
        self.full_sentence_updated.emit(" ".join(self.words))

    @pyqtSlot()
    def clear_all(self):
        # Reset all state variables
        self.current_letters = []
        self.words = []
        self.prediction_buffer = ""
        self.buffer_counter = 0
        self.frame_count = 0
        self.last_known_prediction = ""
        self.sentence_updated.emit("")
        self.full_sentence_updated.emit("")

    def get_full_sentence(self):
        # This function remains the same
        if self.current_letters:
            self.save_current_word()
        sentence = " ".join(self.words)
        self.clear_all()
        return sentence