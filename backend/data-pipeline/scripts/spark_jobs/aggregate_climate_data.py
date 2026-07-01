from pyspark.sql import SparkSession # type: ignore
from pyspark.sql.functions import col, avg, max, min, year # type: ignore
import logging
import argparse

def create_spark_session(app_name="ClimateDataAggregation"):
    """Initialize and return a Spark session."""
    spark = SparkSession.builder \
        .appName(app_name) \
        .config("spark.executor.memory", "4g") \
        .getOrCreate()
    return spark

def aggregate_climate_data(input_path, output_path):
    """
    Reads raw climate data, aggregates average temperature and CO2 by country and year,
    and writes the processed dataset.
    """
    spark = create_spark_session()
    logging.info(f"Started Spark Job for Climate Data Aggregation...")

    try:
        # Load raw data (Assuming it's stored in a Data Lake as Parquet or CSV)
        # For demonstration, we'll try reading Parquet. 
        # In a real setup, input_path could be s3a://bucket-name/raw/climate/
        df = spark.read.format("parquet").option("header", "true").load(input_path)

        # Assuming schema has columns: time, iso_code, avg_temp_celsius, co2_ppm
        # Extract year for yearly aggregation
        df = df.withColumn("year", year(col("time")))

        # Perform aggregations
        aggregated_df = df.groupBy("iso_code", "year").agg(
            avg("avg_temp_celsius").alias("mean_temp"),
            max("avg_temp_celsius").alias("max_temp"),
            min("avg_temp_celsius").alias("min_temp"),
            avg("co2_ppm").alias("mean_co2")
        )

        # Write output back to Data Lake
        aggregated_df.write.mode("overwrite").parquet(output_path)
        logging.info(f"Successfully aggregated data and saved to {output_path}")

    except Exception as e:
        logging.error(f"Failed to process climate data: {e}")
    finally:
        spark.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spark Job to Aggregate Climate Data")
    parser.add_argument('--input', type=str, required=True, help="Path to input raw data")
    parser.add_argument('--output', type=str, required=True, help="Path to output processed data")
    args = parser.parse_args()

    aggregate_climate_data(args.input, args.output)
