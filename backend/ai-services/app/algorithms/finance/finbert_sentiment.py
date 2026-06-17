try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

class FinBERTSentiment:
    """
    Financial BERT (FinBERT) Wrapper for NLP Sentiment Analysis.
    Predicts if Global News headlines are Bullish or Bearish.
    """
    def __init__(self):
        self.pipeline = None
        if TRANSFORMERS_AVAILABLE:
            # Note: This will download the model on first run if internet is available.
            try:
                self.pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")
            except Exception as e:
                print("FinBERT model download failed. Falling back to simple heuristic.")
                self.pipeline = None

    def analyze(self, headline: str):
        """
        Returns +1 for Bullish, -1 for Bearish, 0 for Neutral
        """
        if self.pipeline is None:
            # Fallback Keyword Heuristic if HuggingFace isn't installed
            headline_lower = headline.lower()
            if "crash" in headline_lower or "war" in headline_lower or "sanctions" in headline_lower:
                return -1.0
            if "boom" in headline_lower or "growth" in headline_lower or "peace" in headline_lower:
                return 1.0
            return 0.0

        result = self.pipeline(headline)[0]
        label = result['label']
        
        if label == 'positive': return 1.0
        if label == 'negative': return -1.0
        return 0.0
