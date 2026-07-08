import os
import logging
import argparse
from pyspark.sql import SparkSession # type: ignore
from pyspark.sql.functions import col, avg, max, min, year, window # type: ignore
from pyspark.sql.window import Window
import pyspark.sql.functions as F

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ClimateDataAggregation")

DB_URL = os.getenv("DB_JDBC_URL", "jdbc:postgresql://localhost:5432/world_sim")
DB_USER = os.getenv("POSTGRES_USER", "sribash")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "56789")

def create_spark_session(app_name="ClimateDataAggregation"):
    """Initialize and return a Spark session."""
    spark = SparkSession.builder \
        .appName(app_name) \
        .config("spark.executor.memory", "4g") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
        .getOrCreate()
    return spark

def aggregate_climate_data(input_path, output_path):
    spark = create_spark_session()
    logger.info("Started Spark Job for Climate Data Aggregation...")

    try:
        # Load raw data
        logger.info(f"Reading from {input_path}")
        if not os.path.exists(input_path):
            logger.warning("Input path doesn't exist. Creating dummy.")
            from pyspark.sql.types import StructType, StructField, StringType, DoubleType
            schema = StructType([
                StructField("time", StringType(), True),
                StructField("iso_code", StringType(), True),
                StructField("avg_temp_celsius", DoubleType(), True),
                StructField("co2_ppm", DoubleType(), True)
            ])
            df = spark.createDataFrame([], schema)
        else:
            df = spark.read.format("parquet").option("header", "true").load(input_path)
            
        if df.rdd.isEmpty():
            logger.info("Empty dataframe. Exiting.")
            return

        df = df.withColumn("year", year(F.to_timestamp(col("time"))))
        
        # 1. Country-level Aggregation
        country_agg = df.groupBy("iso_code", "year").agg(
            avg("avg_temp_celsius").alias("mean_temp"),
            max("avg_temp_celsius").alias("max_temp"),
            min("avg_temp_celsius").alias("min_temp"),
            avg("co2_ppm").alias("mean_co2")
        )
        
        # 2. Rolling Averages (Feature Engineering)
        windowSpec = Window.partitionBy("iso_code").orderBy("year").rowsBetween(-4, 0) # 5-year rolling avg
        country_agg = country_agg.withColumn("rolling_5yr_mean_temp", avg("mean_temp").over(windowSpec))
        
        # 3. Global Aggregations
        global_agg = country_agg.groupBy("year").agg(
            avg("mean_temp").alias("global_mean_temp"),
            avg("mean_co2").alias("global_mean_co2")
        ).withColumn("iso_code", F.lit("GLB")) # GLB for Global
        
        # Write output back to Data Lake
        country_agg.write.mode("overwrite").parquet(f"{output_path}/country_level")
        global_agg.write.mode("overwrite").parquet(f"{output_path}/global_level")
        logger.info(f"Successfully aggregated data and saved to {output_path}")

    except Exception as e:
        logger.error(f"Failed to process climate data: {e}", exc_info=True)
    finally:
        spark.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spark Job to Aggregate Climate Data")
    parser.add_argument('--input', type=str, required=False, default="climate_raw.parquet")
    parser.add_argument('--output', type=str, required=False, default="climate_processed")
    args = parser.parse_args()

    aggregate_climate_data(args.input, args.output)
