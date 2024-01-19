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

# Sample treatment descriptions (modify as needed)
treatment_descriptions = [
    "Physical Therapy Session", "Chemotherapy", "Radiation Therapy", "Cognitive Behavioral Therapy", "Blood Transfusion"
]

# Treatment-specific data examples (modify as needed)
treatment_data_examples = [
    "30-minute session", "Chemotherapy Cycle 1", "15-minute radiation therapy", "1-hour psychotherapy session", "2 units of blood"
]

# Generate mock data
data = []
for _ in range(num_records):
    treatment_id = fake.uuid4()
    description = random.choice(treatment_descriptions)
    cost = round(random.uniform(100, 1000), 2)  # Random cost between $100 and $1000
    treatment_specific_data = random.choice(treatment_data_examples)
    data.append((treatment_id, description, cost, treatment_specific_data))

# Define schema
columns = ["TreatmentID", "Description", "Cost", "TreatmentSpecificData"]

# Create DataFrame
df = spark.createDataFrame(data, schema=columns)

# Show some data to verify
df.show()

# Save DataFrame as Parquet file
df.write.mode('overwrite').parquet(os.path.join(data_path, "treatment_data.parquet"))

# Stop the Spark session
spark.stop()

