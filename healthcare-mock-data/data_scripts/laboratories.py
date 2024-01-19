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

# Sample test types (modify as needed)
test_types = [
    "Blood Test", "X-ray", "MRI", "CT Scan", "Ultrasound", "Biopsy"
]

# Generate mock data
data = []
for _ in range(num_records):
    laboratory_id = fake.uuid4()
    name = f"{fake.company()} Lab"
    offered_test_types = random.sample(test_types, random.randint(1, len(test_types)))  # Random subset of test types
    contact_information = fake.address()
    data.append((laboratory_id, name, offered_test_types, contact_information))

# Define schema
columns = ["LaboratoryID", "Name", "TestTypesOffered", "ContactInformation"]

# Create DataFrame
df = spark.createDataFrame(data, schema=columns)

# Show some data to verify
df.show()

# Save DataFrame as Parquet file
df.write.mode('overwrite').parquet(os.path.join(data_path, "laboratory_data.parquet"))

# Stop the Spark session
spark.stop()

