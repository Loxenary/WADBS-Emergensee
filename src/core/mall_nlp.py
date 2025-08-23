import json
import random
from src.config.config import AppConfig

class MallNLP:
    """
    A simple rule-based NLP engine that loads its configuration from JSON files.
    """
    def __init__(self):
        """
        Initializes the NLP engine by loading the knowledge base and NLP config.
        """
        self.knowledge_base = self._load_json(AppConfig.KNOWLEDGE_BASE_PATH)
        self.config = self._load_json(AppConfig.NLP_CONFIG_PATH)
        
        # Load intents and fallback response from the config file
        self.intents = self.config.get('intents', {})
        self.fallback_response = self.config.get('fallback_response', "Maaf, saya tidak mengerti.")

    def _load_json(self, path):
        """A helper function to load a JSON file with error handling."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                print(f"File '{path}' loaded successfully.")
                return json.load(f)
        except FileNotFoundError:
            print(f"ERROR: Configuration file not found at '{path}'.")
            return {}
        except json.JSONDecodeError:
            print(f"ERROR: Could not decode JSON from '{path}'.")
            return {}

    def process_sentence(self, sentence):
        """
        Processes a sentence to find an intent and generate a response.
        """
        sentence = sentence.lower().strip()
        if not sentence:
            return "Maaf, saya tidak mengerti. Silakan coba lagi."

        for intent_name, intent_data in self.intents.items():
            if any(keyword in sentence for keyword in intent_data.get('keywords', [])):
                
                if intent_name == 'find_location':
                    return self._handle_find_location(sentence)
                else:                    
                    responses = intent_data.get('responses', [])
                    return random.choice(responses) if responses else self.fallback_response.format(sentence=sentence)
        
        return self.fallback_response.format(sentence=sentence)

    def _handle_find_location(self, sentence):
        """
        Handles the 'find_location' intent by extracting the entity.
        """
        for location_key in self.knowledge_base.keys():
            if location_key in sentence:
                location_info = self.knowledge_base[location_key]
                return f"{location_key.title()} berada di {location_info['lokasi']}, {location_info['deskripsi']}."
        
        return "Maaf, saya tidak dapat menemukan lokasi yang Anda sebutkan. Coba sebutkan nama toko atau tempat yang lebih spesifik?"

# --- Example Usage ---
if __name__ == "__main__":
    mall_data = {
        "toko sepatu": {"lokasi": "Lantai 2, Sektor Barat", "deskripsi": "di dekat eskalator utama"},
        "toilet": {"lokasi": "Lantai 1, Sektor Timur", "deskripsi": "di sebelah food court"},
        "food court": {"lokasi": "Lantai 1, Sektor Timur", "deskripsi": "di dekat pintu masuk utama"},
        "bioskop": {"lokasi": "Lantai 3, Sektor Utara", "deskripsi": "naik eskalator dari toko buku"}
    }
    with open('mall_knowledge_base.json', 'w', encoding='utf-8') as f:
        json.dump(mall_data, f, indent=2)
        
    nlp_config_data = {
      "intents": {
        "find_location": {
            "keywords": ["di mana", "dmn", "cari", "lokasi", "letak"], 
            "responses": []
        },
        "greeting": {
            "keywords": ["halo", "hai", "selamat pagi", "pagi", "selamat siang", "siang"], 
            "responses": ["Halo! Ada yang bisa saya bantu?"]
        },
        "goodbye": {
            "keywords": ["dah", "sampai jumpa"], 
            "responses": ["Sampai jumpa lagi!"]
        },
        "thank_you": {
            "keywords": ["terima kasih", "makasih", "tks"], 
            "responses": ["Sama-sama!"]
        }
      },
      "fallback_response": "Maaf, saya belum mengerti '{sentence}'. Coba tanyakan lokasi sesuatu."
    }
    with open('nlp_config.json', 'w', encoding='utf-8') as f:
        json.dump(nlp_config_data, f, indent=2)

    # Now, initialize and test the NLP engine
    nlp_engine = MallNLP()
    
    print("\n--- Testing NLP Engine ---")
    test_sentences = [
        "DI MANA TOKO SEPATU",
        "halo",
        "toilet dmn?", # <-- Added shortened test case
        "terima kasih banyak",
        "tks", # <-- Added shortened test case
        "bioskop di mana ya",
        "saya mau makan",
        "sampai jumpa"
    ]
    
    for text in test_sentences:
        response = nlp_engine.process_sentence(text)
        print(f"User    : {text}")
        print(f"Bot     : {response}\n" + "-"*20)
