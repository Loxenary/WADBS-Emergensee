# response_service.py

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from src.core.mall_nlp import MallNLP
# You may need a text processor for spell correction, assumed to be passed in.
# from src.core.text_processor import TextProcessor 

class ResponseService(QObject):
    """Handles final text processing via the NLP engine and packages the response."""
    
    # This signal emits a dictionary, allowing it to carry a rich payload to the UI.
    response_ready = pyqtSignal(dict)

    def __init__(self, text_processor):
        super().__init__()
        self.nlp_engine = MallNLP()
        self.text_processor = text_processor # Use a shared text processor for correction

    @pyqtSlot(str)
    def process_final_sentence(self, text):
        """
        Processes a complete sentence and emits the question, answer, 
        and suggestions as a dictionary.
        """
        if not text.strip(): 
            return 

        # Auto-Correction Step 
        print(f"ResponseService received raw text: '{text}'")
        corrected_text = self.text_processor.correct_sentence(text)
        print(f"Corrected to: '{corrected_text}'")
        
        # NLP Processing Step 
        # Call the new method that returns both an answer and suggestions
        answer, suggestions = self.nlp_engine.process_sentence_with_suggestions(corrected_text)

        response_data = {
            "question": corrected_text,
            "answer": answer,
            "suggestions": suggestions
        }

        # Emit the complete package
        self.response_ready.emit(response_data)