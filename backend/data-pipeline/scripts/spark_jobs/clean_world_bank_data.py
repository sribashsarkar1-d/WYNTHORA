import os
import logging
from pyspark.sql import SparkSession # type: ignore
from pyspark.sql.functions import col, to_timestamp, lit, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WorldBankSparkETL")

# DB settings for PySpark JDBC
DB_URL = os.getenv("DB_JDBC_URL", "jdbc:postgresql://localhost:5432/world_sim")
DB_USER = os.getenv("POSTGRES_USER", "sribash")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "56789")

def clean_world_bank_data(input_path: str, output_table: str = "economic_time_series"):
    logger.info(f"Initializing Spark Session for World Bank ETL...")
    spark = SparkSession.builder \
        .appName("WorldBankCleaner") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
        .getOrCreate()
        
    try:
        # 1. Read Data
        # We assume the input is CSV for this example (from some data lake/landing zone)
        logger.info(f"Reading data from {input_path}")
        
        # Define expected schema to enforce validation
        expected_schema = StructType([
            StructField("time", StringType(), True),
            StructField("iso_code", StringType(), True),
            StructField("gdp_usd", DoubleType(), True),
            StructField("inflation_rate", DoubleType(), True),
            StructField("interest_rate", DoubleType(), True),
            StructField("debt_to_gdp", DoubleType(), True)
        ])
        
        # Usually, Spark reads from HDFS/S3, here we'll assume a local path or fallback to dummy dataframe if file doesn't exist
        if os.path.exists(input_path):
            df = spark.read.csv(input_path, header=True, schema=expected_schema)
        else:
            logger.warning(f"Input path {input_path} does not exist. Generating empty DataFrame with correct schema.")
            df = spark.createDataFrame([], expected_schema)
            
        if df.rdd.isEmpty():
            logger.info("DataFrame is empty. Nothing to process.")
            return

        # 2. Data Validation & Cleaning
        logger.info("Cleaning data (Duplicates, Nulls)...")
        # Remove duplicates based on unique keys
        df = df.dropDuplicates(["time", "iso_code"])
        
        # Drop corrupt rows (where essential keys are missing)
        df = df.dropna(subset=["time", "iso_code"])
        
        # Normalize ISO codes (ensure uppercase)
        from pyspark.sql.functions import upper
        df = df.withColumn("iso_code", upper(col("iso_code")))
        
        # Convert time string to timestamp
        df = df.withColumn("time", to_timestamp(col("time"), "yyyy-MM-dd HH:mm:ss"))
        
        # Handle Negative GDP (Reject/Nullify)
        df = df.withColumn("gdp_usd", when(col("gdp_usd") < 0, lit(None)).otherwise(col("gdp_usd")))
        
        # Cache intermediate dataset for performance if we do multiple aggregations
        df.cache()
        
        logger.info(f"Cleaned dataset has {df.count()} rows. Writing to PostgreSQL...")
        
        # 3. Write Output to PostgreSQL
        # Note: PySpark JDBC doesn't easily do true UPSERTs. We use 'append' for now, 
        # or we could write to a temp table and run a raw SQL merge.
        # Since this is a batch job, 'append' is used, and in a production scenario,
        # we'd load to a staging table and use a post-action script to merge.
        
        db_properties = {
            "user": DB_USER,
            "password": DB_PASS,
            "driver": "org.postgresql.Driver"
        }
        
        df.write.jdbc(url=DB_URL, table=output_table, mode="append", properties=db_properties)
        logger.info("Spark Job Completed Successfully.")
        
    except Exception as e:
        logger.error(f"Spark Job Failed: {e}", exc_info=True)
    finally:
        spark.stop()

if __name__ == "__main__":
    # Example usage: python clean_world_bank_data.py /tmp/world_bank_raw.csv
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else "world_bank_raw.csv"
    clean_world_bank_data(input_file)
