import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class AppConfig:
    """
    A centralized configuration class for the application.
    It now uses the resource_path function to create portable file paths.
    """
    # File Paths
    MODEL_PATH = resource_path("models/sibi_asl_robust_model.h5")
    LABELS_PATH = resource_path("config/labels.json")
    KNOWLEDGE_BASE_PATH = resource_path("config/mall_knowledge_base.json")
    NLP_CONFIG_PATH = resource_path("config/nlp_config.json")
    RECORDED_SIGNS_PATH = "recorded_signs.csv" 

    # Recognizer Parameters
    CONFIDENCE_THRESHOLD = 0.4
    SEQUENCE_LENGTH = 15

    # Sentence Building Parameters
    STABILITY_THRESHOLD = 3
