from pyspark.sql import SparkSession
from faker import Faker
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Read data path from .env file
data_path = os.getenv('DATA_PATH')

# Initialize Spark Session
spark = SparkSession.builder.appName("HealthcareMockData").getOrCreate()

# Number of records to generate
num_records = 1000

# Initialize Faker and set seed for reproducibility
fake = Faker()
Faker.seed(4321)
random.seed(4321)

# Sample diagnosis descriptions (modify as needed)
diagnosis_descriptions = [
    "Type 2 Diabetes", "Hypertension", "Common Cold", "Influenza", "Acute Stress Disorder"
]

# Severity levels (modify as needed)
severity_levels = ["Low", "Medium", "High"]

# Generate mock data
data = []
for _ in range(num_records):
    diagnosis_id = fake.uuid4()
    description = random.choice(diagnosis_descriptions)
    date_of_diagnosis = str(fake.date_between(start_date="-10y", end_date="today"))
    severity = random.choice(severity_levels)
    related_treatment_id = fake.uuid4()  # Generate a random UUID; link to an actual treatment in a real scenario
    data.append((diagnosis_id, description, date_of_diagnosis, severity, related_treatment_id))

# Define schema
columns = ["DiagnosisID", "Description", "DateOfDiagnosis", "Severity", "RelatedTreatmentID"]

# Create DataFrame
df = spark.createDataFrame(data, schema=columns)

# Show some data to verify
df.show()

# Save DataFrame as Parquet file
df.write.mode('overwrite').parquet(os.path.join(data_path, "diagnosis_data.parquet"))

# Stop the Spark session
spark.stop()

