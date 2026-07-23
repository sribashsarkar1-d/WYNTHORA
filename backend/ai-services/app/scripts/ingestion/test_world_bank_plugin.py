import asyncio
import logging
from app.plugins.world_bank import WorldBankPlugin
from app.core.logger import setup_logger

logger = setup_logger("TestWBPlugin", "ingestion.log")

async def test_plugin():
    plugin = WorldBankPlugin(indicator_code="NY.GDP.MKTP.CD") # GDP
    
    # 1. Health Check
    is_healthy = await plugin.health_check()
    logger.info(f"Health Check: {'PASS' if is_healthy else 'FAIL'}")
    if not is_healthy:
        return
        
    # 2. Fetch (and auto-save to Data Lake)
    raw_data = await plugin.fetch()
    logger.info(f"Fetched raw data pages: {len(raw_data)}")
    
    # 3. Normalize
    normalized = plugin.normalize(raw_data)
    logger.info(f"Normalized into {len(normalized)} contracts. Sample: {normalized[0] if normalized else 'None'}")
    
    # 4. Validate
    is_valid = plugin.validate(normalized)
    logger.info(f"Validation passed: {is_valid}")
    
    # 5. Transform
    transformed = plugin.transform(plugin.validated_data)
    
    # 6. Save (Mock)
    await plugin.save(transformed)
    
    print("Plugin E2E Test Completed Successfully!")

if __name__ == "__main__":
    asyncio.run(test_plugin())
