import random
import time
from typing import Dict, Any

class NLPNewsGenerator:
    """
    Generates human-readable news headlines based on the current state 
    of the World Simulation Engine. Can be extended to use a real LLM (like HuggingFace pipeline).
    """
    def __init__(self):
        # We use a template-based approach for speed, but this represents the NLP layer.
        self.templates = {
            "recession": [
                "Global Markets Tumble as Recession Fears Mount.",
                "Economists Warn of Severe Downturn Amid Falling GDP.",
                "Trading Halted: Stocks Plunge in Historic Selloff."
            ],
            "boom": [
                "Markets Hit All-Time Highs on Strong Economic Data.",
                "Tech Sector Drives Unprecedented Global Growth.",
                "Consumer Confidence Surges as Unemployment Drops."
            ],
            "pandemic": [
                "Hospitals Overwhelmed as New Variant Sweeps the Globe.",
                "Borders Close: Nations Struggle to Contain Outbreak.",
                "Vaccine Rollout Accelerates, But Death Toll Rises."
            ],
            "war": [
                "Tensions Escalate: Military Forces Mobilize at Border.",
                "Global Supply Chains Severed by Escalating Conflict.",
                "Energy Prices Spike as War Threatens Oil Reserves."
            ],
            "climate": [
                "Historic Drought Devastates Agricultural Yields.",
                "Unprecedented Heatwave Causes Rolling Blackouts.",
                "Record Hurricane Causes Billions in Infrastructure Damage."
            ]
        }
        self.api_cache = {}
        self.cache_ttl = 60 # 60 seconds

    def fetch_live_news(self, query: str) -> str | None:
        """
        Attempts to fetch live news from NewsAPI or GDELT. 
        Returns a string headline, or None if the API fails/is unavailable.
        Uses a TTL cache to prevent rate-limiting and blocking.
        """
        import requests
        
        # Check Cache
        if query in self.api_cache:
            entry = self.api_cache[query]
            if time.time() - entry['time'] < self.cache_ttl:
                return entry['headline']

        try:
            # Call GDELT free JSON API
            url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=artlist&maxrecords=1&format=json"
            response = requests.get(url, timeout=1.5) # Reduced timeout
            if response.status_code == 200:
                data = response.json()
                if "articles" in data and len(data["articles"]) > 0:
                    headline = data["articles"][0].get("title", None)
                    # Update cache
                    self.api_cache[query] = {'time': time.time(), 'headline': headline}
                    return headline
            return None
        except Exception:
            return None

    def generate_news(self, global_state: Dict[str, Any]) -> list:
        """
        Ingests the global simulation state and outputs relevant news headlines.
        """
        headlines = []
        
        # Check Economic State
        gdp_growth = global_state.get("gdp_growth", 0.0)
        if gdp_growth < -0.02:
            headlines.append(random.choice(self.templates["recession"]))
        elif gdp_growth > 0.03:
            headlines.append(random.choice(self.templates["boom"]))
            
        # Check Health State
        infected = global_state.get("total_infected", 0)
        if infected > 10_000_000: # Arbitrary threshold
            headlines.append(random.choice(self.templates["pandemic"]))
            
        # Check Event Engine State (requires active_events to be passed in)
        active_events = global_state.get("active_events", [])
        for event in active_events:
            if isinstance(event, str):
                event_name = event.lower()
            else:
                event_name = str(event.__class__.__name__).lower()
                
            if "war" in event_name or "conflict" in event_name:
                live = self.fetch_live_news("war conflict")
                headlines.append(live if live else random.choice(self.templates["war"]))
            elif "climate" in event_name or "crisis" in event_name:
                live = self.fetch_live_news("climate crisis")
                headlines.append(live if live else random.choice(self.templates["climate"]))
                
        # If nothing major is happening, output a generic filler
        if not headlines:
            headlines.append("Global Leaders Meet to Discuss Routine Trade Policies.")
            
        return headlines

if __name__ == "__main__":
    generator = NLPNewsGenerator()
    
    # Test recession
    print(generator.generate_news({"gdp_growth": -0.05, "total_infected": 1000}))
    
    # Test pandemic and war
    print(generator.generate_news({"gdp_growth": 0.01, "total_infected": 50_000_000, "active_events": ["WarEvent"]}))
