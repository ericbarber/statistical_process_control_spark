from pyspark.sql import SparkSession
from faker import Faker
import os
from dotenv import load_dotenv

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

# Specializations list (modify as needed)
specializations = [
    "General Practice", "Pediatrics", "Cardiology",
    "Orthopedics", "Neurology", "Oncology", "Dermatology"
]

# Affiliations list (modify as needed)
affiliations = ["Hospital A", "Hospital B", "Clinic C", "Clinic D", None]  # None for independent providers

# Generate mock data
data = []
for _ in range(num_records):
    provider_id = fake.uuid4()
    name = fake.name()
    specialization = fake.random.choice(specializations)
    contact_information = fake.address()
    affiliation = fake.random.choice(affiliations)
    data.append((provider_id, name, specialization, contact_information, affiliation))

# Define schema
columns = ["ProviderID", "Name", "Specialization", "ContactInformation", "Affiliation"]

# Create DataFrame
df = spark.createDataFrame(data, schema=columns)

# Show some data to verify
df.show()

# Save DataFrame as Parquet file
df.write.mode('overwrite').parquet(os.path.join(data_path, "provider_data.parquet"))

# Stop the Spark session
spark.stop()

