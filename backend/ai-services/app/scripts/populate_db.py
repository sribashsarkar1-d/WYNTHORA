import logging
import asyncio
import uuid
import datetime
import pandas as pd
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.models.schema import CountryModel, EconomicTimeSeriesModel

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("DatabasePopulator")

class DatabasePopulator:
    """
    Enterprise Data Population Script.
    Implements Dependency Graph, Transactional Import, Chunk Loading,
    and strict error handling (no suppressed exceptions).
    """
    def __init__(self):
        self.engine = create_async_engine(
            settings.async_database_uri,
            pool_pre_ping=settings.DB_POOL_PRE_PING,
            pool_size=settings.DB_POOL_SIZE,
            echo=False
        )
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )
        self.chunk_size = 500

    async def _insert_chunks(self, session: AsyncSession, model_class, records: List[Dict[str, Any]]):
        """Inserts records in chunks using a transactional approach"""
        total = len(records)
        for i in range(0, total, self.chunk_size):
            chunk = records[i:i + self.chunk_size]
            try:
                db_objs = [model_class(**record) for record in chunk]
                session.add_all(db_objs)
                await session.flush()
                logger.info(f"Inserted chunk {i} to {min(i + self.chunk_size, total)} for {model_class.__tablename__}")
            except SQLAlchemyError as e:
                logger.error(f"Failed inserting chunk {i} for {model_class.__tablename__}: {e}")
                raise

    async def fetch_and_insert_countries(self, session: AsyncSession):
        logger.info("Fetching country reference data...")
        # In a real environment, we would fetch from an API or read a validated CSV.
        # Here we mock the API response for structural demonstration but strictly enforce DB integrity.
        countries_data = [
            {'iso_code': 'USA', 'name': 'United States', 'region': 'North America'},
            {'iso_code': 'CHN', 'name': 'China', 'region': 'Asia'},
            {'iso_code': 'GBR', 'name': 'United Kingdom', 'region': 'Europe'}
        ]
        
        # Check existing
        result = await session.execute(select(CountryModel.iso_code))
        existing_isos = {row[0] for row in result.all()}
        
        new_countries = [c for c in countries_data if c['iso_code'] not in existing_isos]
        
        if new_countries:
            await self._insert_chunks(session, CountryModel, new_countries)
            logger.info(f"Inserted {len(new_countries)} new countries.")
        else:
            logger.info("No new countries to insert.")

    async def fetch_and_insert_economic_data(self, session: AsyncSession):
        logger.info("Fetching economic time series data...")
        # Again, simulating the validation and structured loading
        records = [
            {'country_code': 'USA', 'year': 2023, 'gdp_usd': 25.46, 'inflation_rate': 4.1, 'unemployment_rate': 3.6},
            {'country_code': 'CHN', 'year': 2023, 'gdp_usd': 17.96, 'inflation_rate': 0.2, 'unemployment_rate': 5.2}
        ]
        
        # Check existing to prevent unique constraint violations
        result = await session.execute(select(EconomicTimeSeriesModel.country_code, EconomicTimeSeriesModel.year))
        existing_keys = {(row[0], row[1]) for row in result.all()}
        
        new_records = [r for r in records if (r['country_code'], r['year']) not in existing_keys]
        
        if new_records:
            await self._insert_chunks(session, EconomicTimeSeriesModel, new_records)
            logger.info(f"Inserted {len(new_records)} new economic records.")
        else:
            logger.info("No new economic records to insert.")

    async def run_population(self):
        """
        Executes the population DAG in dependency order.
        1. Countries (independent)
        2. Economic Data (depends on Countries)
        """
        logger.info("Starting Enterprise Database Population Pipeline...")
        start_time = datetime.datetime.utcnow()
        
        async with self.AsyncSessionLocal() as session:
            try:
                # Execution Order (DAG)
                await self.fetch_and_insert_countries(session)
                await self.fetch_and_insert_economic_data(session)
                
                await session.commit()
                logger.info("Database population transaction committed successfully.")
            except Exception as e:
                await session.rollback()
                logger.critical(f"Database population pipeline failed! Transaction rolled back. Error: {e}")
                raise
            finally:
                await session.close()
                
        duration = datetime.datetime.utcnow() - start_time
        logger.info(f"Pipeline completed in {duration.total_seconds():.2f} seconds.")

async def main():
    populator = DatabasePopulator()
    await populator.run_population()

if __name__ == "__main__":
    asyncio.run(main())
