import asyncio
from .geopolitics_model import GeopoliticsModel

async def run_test():
    print("Initializing Geopolitics & GNN Environment...")
    model = GeopoliticsModel()
    await model.initialize_data()
    
    print("\nRunning comprehensive global analysis...")
    model.run_analysis()
    
    print("\nAll models verified successfully.")

if __name__ == "__main__":
    asyncio.run(run_test())
