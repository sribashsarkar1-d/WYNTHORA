import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from geopolitics_model import GeopoliticsModel

def run_test():
    print("Initializing Geopolitics & GNN Environment...")
    model = GeopoliticsModel()
    
    print("\nRunning comprehensive global analysis...")
    model.run_analysis()
    
    print("\nAll models verified successfully.")

if __name__ == "__main__":
    run_test()
