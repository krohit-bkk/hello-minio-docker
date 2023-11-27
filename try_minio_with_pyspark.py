# docker rm -f minio-etl:latest &&  docker-compose build --no-cache etl
# docker rm $(docker ps -a -q --filter "name=minio-etl-run")
# docker compose run -it etl spark-submit --jars aws-java-sdk-bundle-1.12.540.jar,hadoop-aws-3.3.4.jar /opt/try_pyspark.py

import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import lit

# Define MinIO S3 configuration
minio_access_key = "miniousername"
minio_secret_key = "miniopassword"
minio_endpoint = "http://minio-server:9000"
minio_bucket = "test-bucket-1"
minio_path = "sample_data/sample_data.csv"
minio_object_path1 = "sample_data"
minio_object_path2 = "sample_data1"

# Function to get SparkSession object
def get_spark():
    # Create a Spark session
    spark = SparkSession.builder \
        .appName("MinIO PySpark Example") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    # Set the S3A configuration for MinIO
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID", minio_access_key))
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY", minio_secret_key))
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", os.getenv("ENDPOINT", minio_endpoint))
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "true")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.attempts.maximum", "1")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.connection.establish.timeout", "5000")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.connection.timeout", "10000")

    spark.sparkContext.setLogLevel("WARN")
    return spark 

# Get SparkSession object
spark = get_spark()

print("\n>>>> DEBUG ENV...")
print(f">>>> Access key: {os.getenv('AWS_ACCESS_KEY_ID', 'AWS_ACCESS_KEY_ID not found')}")
print(f">>>> Secret key: {os.getenv('AWS_SECRET_ACCESS_KEY', 'AWS_SECRET_ACCESS_KEY not found')}")
print(f">>>> Entrypoint: {os.getenv('ENDPOINT', 'ENDPOINT not found')}")

# Read from S3
# ------------
# Define schema for the DataFrame
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("salary", IntegerType(), True)
])
# Read data from MinIO S3 into a DataFrame
input_dir = f"s3a://{minio_bucket}/{minio_object_path1}/"
df1 = spark.read.csv(input_dir, header=False, schema=schema)
df1.withColumn("Flag", lit("df1")).show()

# Write to S3
# -----------
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])
output_dir = f"s3a://{minio_bucket}/{minio_object_path2}/"
data = [(1, "Alice", 25), (2, "Bob", 30), (3, "Charlie", 22)]
df2 = spark.createDataFrame(data, schema)
df2.withColumn("Flag", lit("df2")).show()
df2.write.format("parquet").mode("overwrite").save(output_dir)

# Read from output_dir to confirm successful write
df3 = spark.read.parquet(output_dir).withColumn("Flag", lit("df3"))
df3.show()

# Stop the Spark session
spark.stop()