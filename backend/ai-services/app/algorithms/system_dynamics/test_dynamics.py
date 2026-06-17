import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from macro_model import MacroEnvironment

def run_test():
    print("Initializing Macro System Dynamics Environment...")
    macro_env = MacroEnvironment()
    
    print("\nInitial State:")
    print(macro_env.get_state())
    
    print("\n--- Simulating 50 Days (Ticks) ---")
    for tick in range(1, 51):
        macro_env.tick()
        if tick % 10 == 0:
            print(f"\n[Day {tick}]")
            state = macro_env.get_state()
            for key, value in state.items():
                print(f"  {key}: {value}")
            
if __name__ == "__main__":
    run_test()
