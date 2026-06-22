try:
    from transformers import pipeline # type: ignore
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

import re
from typing import Union, List

class FinBERTSentiment:
    """
    Financial BERT (FinBERT) Wrapper for NLP Sentiment Analysis.
    Predicts if Global News headlines are Bullish or Bearish.
    """
    def __init__(self):
        self._pipeline = None
        self._initialized = False

    def _get_pipeline(self):
        if not self._initialized:
            self._initialized = True
            if TRANSFORMERS_AVAILABLE:
                # Note: This will download the model on first run if internet is available.
                try:
                    self._pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")
                except Exception as e:
                    print("FinBERT model download failed. Falling back to simple heuristic.")
                    self._pipeline = None
        return self._pipeline

    def analyze(self, headlines: Union[str, List[str]]) -> Union[float, List[float]]:
        """
        Returns a continuous score between -1.0 (Bearish) and 1.0 (Bullish).
        Supports processing a single headline or a batch of headlines.
        """
        single_input = isinstance(headlines, str)
        if single_input:
            headlines = [headlines] # type: ignore

        pipe = self._get_pipeline()
        
        if pipe is None:
            # Expanded Fallback Keyword Heuristic using Regex for word boundaries
            results = []
            
            very_negative = re.compile(r'\b(war|sanctions|blockade|coup|crash|collapse|devastates|plunge|damage|hurricane|conflict|severed)\b', re.IGNORECASE)
            negative = re.compile(r'\b(drought|heatwave|crisis|tension|escalate|shortfall|decline|fear|tumble|selloff)\b', re.IGNORECASE)
            positive = re.compile(r'\b(boom|growth|peace|agreement|trade|surge|alliance|recovery)\b', re.IGNORECASE)
            
            for headline in headlines:
                score = 0.0
                if very_negative.search(headline):
                    score = -1.0
                elif negative.search(headline):
                    score = -0.6
                elif positive.search(headline):
                    score = 0.8
                results.append(score)
            
            return results[0] if single_input else results

        # Process batch through pipeline
        predictions = pipe(headlines)
        results = []
        for result in predictions:
            label = result['label']
            score = result['score'] # Confidence score between 0 and 1
            
            if label == 'positive': 
                results.append(score)
            elif label == 'negative': 
                results.append(-score)
            else:
                results.append(0.0)
                
        return results[0] if single_input else results
