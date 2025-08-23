from PyQt6.QtCore import  QObject, pyqtSignal,  pyqtSlot
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QInputDialog
import csv
from src.core.sign_recognizer import SignRecognizer, cv2

class CameraService(QObject):
    """Manages webcam, sign recognition, and sentence construction."""
    frame_ready = pyqtSignal(QImage)
    sentence_updated = pyqtSignal(str)
    data_saved_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.cap = None
        self.recognizer = SignRecognizer()
        self.current_sentence = []
        self.prediction_buffer = ""
        self.buffer_counter = 0

    @pyqtSlot()
    def start_camera(self):
        if not self.is_running:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened(): return
            self.is_running = True
            self.run()

    @pyqtSlot()
    def stop_camera(self):
        self.is_running = False
        if self.cap: self.cap.release()

    def run(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret: break

            frame = cv2.flip(frame, 1)
            processed_frame, prediction = self.recognizer.process_frame(frame)
            if prediction:
                if prediction == self.prediction_buffer: self.buffer_counter += 1
                else: self.prediction_buffer = prediction; self.buffer_counter = 0
                if self.buffer_counter == 2:
                    # For sign language, we append letters without spaces
                    self.current_sentence.append(prediction)
                    self.sentence_updated.emit("".join(self.current_sentence))
                    self.buffer_counter = 0
            
            rgb_image = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape; bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            self.frame_ready.emit(qt_image)

    @pyqtSlot()
    def delete_last_char(self):
        if self.current_sentence:
            self.current_sentence.pop()
            self.sentence_updated.emit("".join(self.current_sentence))

    def get_full_sentence(self):
        sentence = "".join(self.current_sentence)
        self.current_sentence = []
        self.sentence_updated.emit("")
        return sentence

    @pyqtSlot()
    def save_current_frame_data(self):
        if self.recognizer.current_landmarks:
            label, ok = QInputDialog.getText(None, 'Save Data', 'Enter label for this sign:')
            if ok and label:
                try:
                    with open('recorded_signs.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([label] + self.recognizer.current_landmarks)
                    self.data_saved_signal.emit(label)
                except Exception as e: print(f"Error saving data: {e}")
