import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from market_engine import FinancialMarketEngine

def run_test():
    print("Initializing Finance & Time-Series Environment...")
    engine = FinancialMarketEngine()
    engine.run_market_simulation()
    
if __name__ == "__main__":
    run_test()
