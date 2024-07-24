import logging
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TextProcessor:
    def __init__(self):
        """
        Initializes the TextProcessor with Spacy and NLTK resources.
        """
        logging.info("Initializing TextProcessor")
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            logging.error(f"Failed to load Spacy model: {e}")
            raise
        
        try:
            nltk.download('punkt')
            nltk.download('stopwords')
        except Exception as e:
            logging.error(f"Failed to download NLTK resources: {e}")
            raise

        self.stop_words = set(stopwords.words('english'))
        logging.info("TextProcessor initialized")

    def extract_keywords(self, text: str) -> list:
        """
        Extracts keywords from the provided text.

        Args:
            text (str): The input text.

        Returns:
            list: A list of extracted keywords.
        """
        logging.info("Extracting keywords from text")
        try:
            word_tokens = word_tokenize(text)
            filtered_text = [w for w in word_tokens if w.lower() not in self.stop_words]
            keywords = filtered_text[:5]
            logging.info(f"Extracted keywords: {keywords}")
            return keywords
        except Exception as e:
            logging.error(f"Error extracting keywords: {e}")
            raise

    def analyze_entities(self, text: str):
        """
        Analyzes entities in the provided text using Spacy.

        Args:
            text (str): The input text.

        Returns:
            doc: The Spacy doc object containing entity analysis.
        """
        logging.info("Analyzing entities in text")
        try:
            doc = self.nlp(text)
            return doc
        except Exception as e:
            logging.error(f"Error analyzing entities: {e}")
            raise
