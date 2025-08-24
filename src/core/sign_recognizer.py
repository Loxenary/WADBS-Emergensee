# sign_recognizer.py (Upgraded)

import cv2
import json
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
from src.config.config import AppConfig

class SignRecognizer:
    def __init__(self):
        print("Initializing Sign Recognizer...")
        self.model = load_model(AppConfig.MODEL_PATH)
        self.sequence_length = AppConfig.SEQUENCE_LENGTH

        self.landmark_sequence = [] # Stores the last sequence of detected landmarks
        self.last_normalized_landmarks = None

        try:
            with open(AppConfig.LABELS_PATH, 'r') as f:
                self.class_names = json.load(f)
            print(f"Successfully loaded {len(self.class_names)} labels.")
        except FileNotFoundError:
            print(f"ERROR: '{AppConfig.LABELS_PATH}' not found.")
            self.class_names = []
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1, 
            min_detection_confidence=0.7,
            min_tracking_confidence=0.2
        )
        self.mp_drawing = mp.solutions.drawing_utils
        print("Sign Recognizer initialized successfully.")

    def detect_and_draw_landmarks(self, frame):
        """
        Detects, draws, and stores hand landmarks. Runs on every frame.
        Returns the frame with landmarks drawn on it.
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            # Draw the skeleton on the original frame
            self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            
            # Extract, normalize, and store the landmark data
            normalized_landmarks = self._extract_landmarks(hand_landmarks)
            self.last_normalized_landmarks = normalized_landmarks
            self.landmark_sequence.append(self.last_normalized_landmarks)
            self.landmark_sequence = self.landmark_sequence[-self.sequence_length:]
        else:
            self.landmark_sequence =''
            self.last_normalized_landmarks = None

        return frame

    def predict_from_last_landmarks(self):
        """
        Uses the stored landmark data to make a prediction. Runs intermittently.
        Returns a prediction string (e.g., "A") or None.
        """
        # Only predict if we have a full sequence of detected frames
        if len(self.landmark_sequence) < self.sequence_length or self.last_normalized_landmarks is None:
            return None

        # Prepare the landmark data for the model (add a batch dimension)
        input_data = np.expand_dims(self.last_normalized_landmarks, axis=0)
        
        # Make the slow prediction
        prediction = self.model.predict(input_data, verbose=0)
        
        confidence = np.max(prediction)
        predicted_class_index = np.argmax(prediction)
        
        predicted_word = None
        if confidence > AppConfig.CONFIDENCE_THRESHOLD: 
            if self.class_names:
                predicted_word = self.class_names[predicted_class_index]        
            self.landmark_sequence = []
                    
        return predicted_word


    def _extract_landmarks(self, hand_landmarks):
        """
        Extracts and normalizes landmarks. (This method is unchanged).
        """
        landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])
        wrist = landmarks[0]
        relative_landmarks = landmarks - wrist
        max_dist = np.max(np.linalg.norm(relative_landmarks, axis=1))
        if max_dist == 0:
            return np.zeros_like(relative_landmarks)
        normalized_landmarks = relative_landmarks / max_dist
        return normalized_landmarks

    def close(self):
        self.hands.close()