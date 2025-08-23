from PyQt6.QtCore import Qt, QObject, pyqtSignal, QThread, QMetaObject, pyqtSlot
from src.core.mall_nlp import MallNLP
class ResponseService(QObject):
    """Handles final text processing via the NLP engine."""
    response_ready = pyqtSignal(str)

    def __init__(self, text_processor):
        super().__init__()
        self.nlp_engine = MallNLP()
        self.text_processor = text_processor # Use the shared text processor

    @pyqtSlot(str)
    def process_final_sentence(self, text):
        """Processes a complete sentence and emits the result."""
        if not text.strip(): return
        
        # --- Auto-Correction Step ---
        print(f"ResponseService received raw text: '{text}'")
        corrected_text = self.text_processor.correct_sentence(text)
        print(f"Corrected to: '{corrected_text}'")
        
        response = self.nlp_engine.process_sentence(corrected_text)
        self.response_ready.emit(response)