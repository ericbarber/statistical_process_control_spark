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

# Sample test types and normal ranges (modify as needed)
test_types_normal_ranges = {
    "Blood Test": "4.5-6.0 mmol/L",
    "X-ray": "No abnormal findings",
    "MRI": "No abnormal findings",
    "CT Scan": "No abnormal findings",
    "Ultrasound": "No abnormal findings",
    "Biopsy": "No malignancy"
}

# Generate mock data
data = []
for _ in range(num_records):
    test_id = fake.uuid4()
    patient_id = fake.uuid4()  # Generate a random UUID; link to an actual patient in a real scenario
    laboratory_id = fake.uuid4()  # Generate a random UUID; link to an actual laboratory in a real scenario
    date = str(fake.date_between(start_date="-2y", end_date="today"))
    test_type, normal_range = random.choice(list(test_types_normal_ranges.items()))
    result = f"Result for {test_type}"  # Placeholder result; customize as needed
    data.append((test_id, patient_id, laboratory_id, date, test_type, result, normal_range))

# Define schema
columns = ["TestID", "PatientID", "LaboratoryID", "Date", "TestType", "Results", "NormalRanges"]

# Create DataFrame
df = spark.createDataFrame(data, schema=columns)

# Show some data to verify
df.show()

# Save DataFrame as Parquet file
df.write.mode('overwrite').parquet(os.path.join(data_path, "test_result_data.parquet"))

# Stop the Spark session
spark.stop()

