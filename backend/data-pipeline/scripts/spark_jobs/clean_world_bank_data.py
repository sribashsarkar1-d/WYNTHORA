from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("WorldBankCleaner").getOrCreate()
print("Spark Job Ready")
