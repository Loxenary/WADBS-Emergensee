import json
from difflib import get_close_matches
from src.config.config import AppConfig

class TextProcessor:
    """
    A utility class to handle text correction and suggestions.
    """
    def __init__(self):
        """
        Initializes the processor and builds a vocabulary from multiple sources.
        """
        self.vocabulary = self._build_vocabulary(AppConfig.KNOWLEDGE_BASE_PATH, AppConfig.NLP_CONFIG_PATH)
        print(f"TextProcessor initialized with {len(self.vocabulary)} vocabulary words.")

    def _build_vocabulary(self, kb_path, config_path):
        """
        Loads the knowledge base and NLP config to create a comprehensive
        dictionary of all known correct words and phrases.
        """
        vocab = set()
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                kb_data = json.load(f)
                vocab.update(kb_data.keys())
        except FileNotFoundError:
            print(f"Warning: Knowledge base not found at '{kb_path}' for TextProcessor.")

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                for intent in config_data.get('intents', {}).values():
                    vocab.update(intent.get('keywords', []))
        except FileNotFoundError:
            print(f"Warning: NLP config not found at '{config_path}' for TextProcessor.")
            
        return sorted(list(vocab))

    def correct_sentence(self, raw_text):
        """
        Takes a raw, concatenated string of letters and splits it into
        the most likely sequence of words from the vocabulary.
        
        Example: "dmntoilet" -> "dmn toilet"
        """
        raw_text = raw_text.lower()
        corrected_words = []
        
        while raw_text:
            matches = [v for v in self.vocabulary if raw_text.startswith(v.replace(" ", ""))]
            
            if not matches:
                found_word = False
                for i in range(len(raw_text), 0, -1):
                    partial_word = raw_text[:i]
                    close_matches = get_close_matches(partial_word, self.vocabulary, n=1, cutoff=0.7)
                    if close_matches:
                        best_match = close_matches[0]
                        corrected_words.append(best_match)
                        raw_text = raw_text[len(partial_word):]
                        found_word = True
                        break
                if not found_word:
                    print(f"Could not correct: {raw_text}")
                    break
            else:
                best_match = max(matches, key=len)
                corrected_words.append(best_match)
                raw_text = raw_text[len(best_match.replace(" ", "")):]

        return " ".join(corrected_words)

    def get_suggestions(self, current_text):
        """
        Provides auto-complete suggestions for the last word being typed.
        
        Example: "di mana toko s" -> ["sepatu"]
        """
        current_text = current_text.lower()
        words = current_text.split()
        
        if not words or current_text.endswith(' '):
            return []

        partial_word = words[-1]
        
        suggestions = [v for v in self.vocabulary if v.startswith(partial_word)]
        
        return suggestions

if __name__ == '__main__':
    # Create dummy knowledge base and config for testing
    mall_data = {
        "toko sepatu": {}, "toilet": {}, "food court": {}, "bioskop": {}
    }
    with open('mall_knowledge_base.json', 'w', encoding='utf-8') as f:
        json.dump(mall_data, f)
        
    nlp_config_data = {
      "intents": { "find_location": { "keywords": ["di mana", "dmn", "cari"] } }
    }
    with open('nlp_config.json', 'w', encoding='utf-8') as f:
        json.dump(nlp_config_data, f)
        
    processor = TextProcessor()
    
    print("\n Testing Auto-Correction ")
    correction_cases = ["dmntoilet", "caritokosepatu", "dimanabioskop"]
    for case in correction_cases:
        corrected = processor.correct_sentence(case)
        print(f"Raw: '{case}' -> Corrected: '{corrected}'")
        
    print("\n Testing Auto-Completion ")
    completion_cases = ["d", "di mana t", "food c"]
    for case in completion_cases:
        suggestions = processor.get_suggestions(case)
        print(f"Input: '{case}' -> Suggestions: {suggestions}")
