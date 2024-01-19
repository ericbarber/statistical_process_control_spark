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

# Sample department names and types (modify as needed)
department_names = [
    "Emergency", "Cardiology", "Pediatrics", "Neurology", "Oncology", "Orthopedics"
]

# Generate mock data
data = []
for _ in range(num_records):
    department_id = fake.uuid4()
    name = random.choice(department_names)
    department_type = name  # In this mock setup, the department name serves as the type
    associated_provider_ids = [fake.uuid4() for _ in range(random.randint(1, 5))]  # Random number of associated providers

    data.append((department_id, name, department_type, associated_provider_ids))

# Define schema
columns = ["DepartmentID", "Name", "Type", "AssociatedProviderIDs"]

# Create DataFrame
df = spark.createDataFrame(data, schema=columns)

# Save DataFrame as Parquet file
df.write.mode('overwrite').parquet(os.path.join(data_path, "department_data.parquet"))

# Stop the Spark session
spark.stop()

