class AppConfig:
    """
    A centralized configuration class for the application.
    It holds all static data, paths, and model parameters.
    """
    # These paths are relative to the project's root directory.
    MODEL_PATH = "models/sign_language_model.h5"
    LABELS_PATH = "config/labels.json"
    KNOWLEDGE_BASE_PATH = "config/mall_knowledge_base.json"
    NLP_CONFIG_PATH = "config/nlp_config.json"
    RECORDED_SIGNS_PATH = "recorded_signs.csv"

    # The minimum confidence level required from the model to consider a prediction valid.
    CONFIDENCE_THRESHOLD = 0.65

    # The number of frames the recognizer looks at to make a single prediction.
    SEQUENCE_LENGTH = 15

    # The number of consecutive, identical predictions required before a letter is
    # added to the sentence. This prevents flickering predictions.
    STABILITY_THRESHOLD = 3