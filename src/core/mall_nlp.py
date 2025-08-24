# mall_nlp.py (Upgraded)

import json
import random
from src.config.config import AppConfig

class MallNLP:
    """
    An upgraded, more robust NLP engine that provides location-specific directions
    and suggests related locations.
    """
    def __init__(self, stand_id="stand_pintu_timur"):
        self.stand_id = stand_id
        self.knowledge_base = self._load_json(AppConfig.KNOWLEDGE_BASE_PATH)
        self.config = self._load_json(AppConfig.NLP_CONFIG_PATH)
        
        self.intents = self.config.get('intents', {})
        self.fallback_response = self.config.get('fallback_response', "Maaf, saya tidak mengerti.")
        print(f"Upgraded NLP Engine initialized for stand: '{self.stand_id}'")

    def _load_json(self, path):
        """Helper function to load a JSON file with error handling."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR: Could not load or parse JSON from '{path}'. Details: {e}")
            return {}

    def process_sentence(self, sentence):
        """
        Legacy method for basic processing. Returns only the answer string.
        """
        answer, _ = self.process_sentence_with_suggestions(sentence)
        return answer

    def process_sentence_with_suggestions(self, sentence):
        """
        Processes a sentence to find an answer and generate relevant suggestions.
        
        Returns:
            tuple: (answer_string, suggestions_list)
        """
        sentence = sentence.lower().strip()
        if not sentence:
            return "Maaf, saya tidak mengerti. Silakan coba lagi.", []

        # Upgraded Entity & Intent Matching
        found_entity_key = self._find_entity(sentence)
        found_intent_key = self._find_intent(sentence)

        # Decision Logic
        if found_intent_key == 'find_location' and found_entity_key:
            answer = self._handle_find_location(found_entity_key)
            suggestions = self._get_suggestions(found_entity_key)
            return answer, suggestions
        
        elif found_entity_key:
            answer = self._handle_find_location(found_entity_key)
            suggestions = self._get_suggestions(found_entity_key)
            return answer, suggestions

        elif found_intent_key:
            responses = self.intents[found_intent_key].get('responses', [])
            answer = random.choice(responses) if responses else self.fallback_response
            return answer, []
        
        # If nothing is found
        return self.fallback_response.format(sentence=sentence), []

    def _find_entity(self, sentence):
        """Finds the most relevant entity by matching keywords."""
        for key, data in self.knowledge_base.items():
            # The entity's own key and its keywords are all searchable terms
            search_terms = data.get('keywords', []) + [key.replace('_', ' ')]
            if any(term in sentence for term in search_terms):
                return key
        return None
        
    def _find_intent(self, sentence):
        """Finds the first matching intent from the sentence."""
        for intent_name, intent_data in self.intents.items():
            if any(keyword in sentence for keyword in intent_data.get('keywords', [])):
                return intent_name
        return None

    def _handle_find_location(self, entity_key):
        """Generates a response for a found location."""
        location_info = self.knowledge_base.get(entity_key, {})
        
        # Prioritize directions specific to the current stand
        directions = location_info.get('directions', {}).get(self.stand_id)
        if directions:
            return directions
        
        # Fallback to generic location and description
        nama = location_info.get('nama_display', entity_key.replace('_', ' ').title())
        lokasi = location_info.get('lokasi', 'lokasi tidak diketahui')
        deskripsi = location_info.get('deskripsi', '')
        return f"{nama} berada di {lokasi}, {deskripsi}."

    def _get_suggestions(self, found_entity_key, count=2):
        """Generates a list of suggested questions based on category."""
        found_entity_data = self.knowledge_base.get(found_entity_key, {})
        category = found_entity_data.get('kategori')
        if not category:
            return []

        suggestions = []
        for key, data in self.knowledge_base.items():
            if key != found_entity_key and data.get('kategori') == category:
                display_name = data.get('nama_display', key.replace('_', ' ').title())
                suggestions.append(f"Di mana lokasi {display_name}?")
        
        random.shuffle(suggestions)
        return suggestions[:count]