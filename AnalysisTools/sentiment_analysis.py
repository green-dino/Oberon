import logging
from textblob import TextBlob

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SentimentAnalyzer:
    def get_sentiment_score(self, text: str) -> float:
        """
        Gets the sentiment score for the provided text.

        Args:
            text (str): The input text.

        Returns:
            float: The sentiment score.
        """
        logging.info("Getting sentiment score for text")
        try:
            blob = TextBlob(text)
            sentiment_score = blob.sentiment.polarity
            logging.info(f"Sentiment score: {sentiment_score}")
            return sentiment_score
        except Exception as e:
            logging.error(f"Error getting sentiment score: {e}")
            raise
