import cv2
import json
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
import time 
import psutil
import os
from src.config.config import AppConfig

class SignRecognizer:
    """
    Handles hand landmark detection and sign prediction.
    This class is designed to be easily upgradeable for video (sequence) models.
    """
    def __init__(self):
        """
        Initializes the recognizer.
        
        Args:
            model_path (str): Path to the trained Keras model (.h5 file).
            labels_path (str): Path to the JSON file mapping class indices to labels.
            sequence_length (int): The number of frames to collect for a sequence prediction.
        """
        print("Initializing Sign Recognizer...")
        self.model = load_model(AppConfig.MODEL_PATH)
        self.sequence_length = AppConfig.SEQUENCE_LENGTH
        self.landmark_sequence = []

        #  Dynamic Label Loading 
        try:
            with open(AppConfig.LABELS_PATH, 'r') as f:
                self.class_names = json.load(f)
            print(f"Successfully loaded {len(self.class_names)} labels from '{AppConfig.LABELS_PATH}'.")
        except FileNotFoundError:
            print(f"ERROR: '{AppConfig.LABELS_PATH}' not found. Please create this file.")
            self.class_names = []
        
        #  MediaPipe Setup 
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1, 
            min_detection_confidence=0.7,
            min_tracking_confidence=0.2
        )
        self.mp_drawing = mp.solutions.drawing_utils
        print("Sign Recognizer initialized successfully.")

    def predict_from_sequence(self):
        """
        Makes a prediction from the collected sequence of landmarks.
        *** THIS IS THE PLACEHOLDER FOR YOUR VIDEO MODEL UPGRADE ***
        """
        #  CURRENT LOGIC (for static image model) 
        # It predicts using only the LAST frame in the sequence.
        last_landmarks = np.array([self.landmark_sequence[-1]])
        prediction = self.model.predict(last_landmarks, verbose=0)
        
        #  FUTURE LOGIC (for video/LSTM model) 
        # TODO: Replace the logic above with something like this for a sequence model:
        #
        # sequence_array = np.expand_dims(np.array(self.landmark_sequence), axis=0)
        # prediction = self.model.predict(sequence_array, verbose=0)
        #
        return prediction

    def process_frame(self, frame):
        """
        Processes a single video frame, extracts landmarks, manages the sequence,
        and triggers prediction when the sequence is full.
        
        Returns:
            A tuple of (processed_frame, predicted_word).
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        predicted_word = None
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            
            landmarks = self._extract_landmarks(hand_landmarks)
            self.landmark_sequence.append(landmarks)
            self.landmark_sequence = self.landmark_sequence[-self.sequence_length:]
            
            if len(self.landmark_sequence) == self.sequence_length:
                prediction = self.predict_from_sequence()
                confidence = np.max(prediction)
                predicted_class_index = np.argmax(prediction)
                
                # This is the word that is returned for sentence logic
                stable_prediction = None

                # Display the live prediction and confidence regardless of threshold
                if self.class_names:
                    live_word = self.class_names[predicted_class_index]
                    cv2.putText(frame, f"Live: {live_word} ({confidence:.2f})", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA) 

                # Check if the confidence is high enough to be considered for the sentence
                if confidence > AppConfig.CONFIDENCE_THRESHOLD: 
                    stable_prediction = self.class_names[predicted_class_index] if self.class_names else None
                    self.landmark_sequence = []
                    
                predicted_word = stable_prediction
        else:
            self.landmark_sequence = [] 

        return frame, predicted_word

    def _extract_landmarks(self, hand_landmarks):
        """
        Extracts and normalizes landmarks into a flat list.
        """
        wrist = hand_landmarks.landmark[0]
        # Flatten all 21 landmarks (x, y, z) into a single list of 63 values
        landmark_list = []
        for lm in hand_landmarks.landmark:
            landmark_list.extend([lm.x - wrist.x, lm.y - wrist.y, lm.z - wrist.z])
        return landmark_list

    def close(self):
        """Releases MediaPipe resources."""
        self.hands.close()

#  Standalone Test Block 
if __name__ == '__main__':
    # This block allows you to test this script directly.
    # It will not run when imported by your main PyQt6 app.
    
    # You must have 'sign_language_model.h5' and 'labels.json' in the same folder.
    # Let's create a dummy labels.json for testing purposes.
    dummy_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M',
                    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']
    with open('labels.json', 'w') as f:
        json.dump(dummy_labels, f)
        
    print(" Testing SignRecognizer Standalone ")
    recognizer = SignRecognizer()
    cap = cv2.VideoCapture(0)
    
    #  Variables for live translation 
    sentence = []
    last_prediction = None
    stable_counter = 0
    STABILITY_THRESHOLD = 5 # Number of frames a sign must be held
    
    #  Variables for resource logging 
    process = psutil.Process(os.getpid())
    start_time = time.time()
    frame_count = 0
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
    else:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                continue
            
            frame_count += 1
            frame = cv2.flip(frame, 1) # Flip for selfie view
            processed_frame, prediction = recognizer.process_frame(frame)
            
            #  Live Translation Logic 
            if prediction:
                if prediction == last_prediction:
                    stable_counter += 1
                else:
                    last_prediction = prediction
                    stable_counter = 0
                
                if stable_counter == STABILITY_THRESHOLD:
                    sentence.append(prediction)
                    stable_counter = 0 # Reset after adding
            
            #  Logger Logic 
            elapsed_time = time.time() - start_time
            fps = frame_count / elapsed_time if elapsed_time > 0 else 0
            cpu_usage = process.cpu_percent()
            mem_usage = process.memory_info().rss / (1024 * 1024) # in MB
            
            #  Display Stats and Sentence 
            stats_text = f"FPS: {fps:.1f} | CPU: {cpu_usage:.1f}% | MEM: {mem_usage:.1f}MB"
            cv2.rectangle(processed_frame, (0, 0), (640, 20), (0, 0, 0), -1)
            cv2.putText(processed_frame, stats_text, (5, 15), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            
            cv2.rectangle(processed_frame, (0, 440), (640, 480), (0, 0, 0), -1)
            cv2.putText(processed_frame, ' '.join(sentence), (10, 470), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.imshow('SignRecognizer Test', processed_frame)
            
            key = cv2.waitKey(5) & 0xFF
            if key == 27:
                break
            elif key == ord('c'): 
                sentence = []
                
        recognizer.close()
        cap.release()
        cv2.destroyAllWindows()
