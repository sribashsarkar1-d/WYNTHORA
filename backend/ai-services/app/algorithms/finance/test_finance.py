import asyncio
from .market_engine import FinancialMarketEngine

async def run_test():
    print("Initializing Finance & Time-Series Environment...")
    engine = FinancialMarketEngine()
    await engine.initialize_data()
    engine.run_market_simulation()
    
if __name__ == "__main__":
    asyncio.run(run_test())
