from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read data path from .env file
data_path = os.getenv('DATA_PATH')

# Initialize a SparkSession
spark = SparkSession.builder \
    .appName("Pre-existing Conditions") \
    .getOrCreate()

# List of pre-existing conditions
conditions = [
    "Diabetes", "Cancer", "Heart disease", "Epilepsy", "Dialysis",
    "Mental health conditions", "Alzheimer's or dementia", "Arthritis",
    "Asthma", "Hepatitis", "Emphysema", "HIV infection", "Obesity",
    "Pregnancy", "Cerebral palsy", "Hypertension", "Substance use disorders",
    "Ulcerative colitis", "Cholesterol", "Hemophilia", "Lupus",
    "Muscular dystrophy", "Neurological disorders", "Organ transplants"
]

# Create a DataFrame with an ID and the condition
df = spark.createDataFrame(conditions, "string").toDF("Condition")
df = df.withColumn("ID", monotonically_increasing_id())

# Write the DataFrame to a Parquet file
df.write.mode('overwrite').parquet(os.path.join(data_path, "conditions_data.parquet"))

# Stop the SparkSession
spark.stop()

