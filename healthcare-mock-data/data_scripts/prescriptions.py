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

# Sample medication details (modify as needed)
medications = [
    "Amoxicillin", "Ibuprofen", "Metformin", "Atorvastatin", "Lisinopril", "Albuterol"
]

# Sample dosage (modify as needed)
dosages = ["250mg", "500mg", "1000mg"]

# Sample frequency (modify as needed)
frequencies = ["Once a day", "Twice a day", "Every 6 hours"]

# Sample duration (modify as needed)
durations = ["7 days", "14 days", "1 month"]

# Generate mock data
data = []
for _ in range(num_records):
    prescription_id = fake.uuid4()
    patient_id = fake.uuid4()  # Generate a random UUID; link to an actual patient in a real scenario
    provider_id = fake.uuid4()  # Generate a random UUID; link to an actual provider in a real scenario
    medication_details = random.choice(medications)
    dosage = random.choice(dosages)
    frequency = random.choice(frequencies)
    duration = random.choice(durations)
    data.append((prescription_id, patient_id, provider_id, medication_details, dosage, frequency, duration))

# Define schema
columns = ["PrescriptionID", "PatientID", "ProviderID", "MedicationDetails", "Dosage", "Frequency", "Duration"]

# Create DataFrame
df = spark.createDataFrame(data, schema=columns)

# Show some data to verify
df.show()

# Save DataFrame as Parquet file
df.write.mode('overwrite').parquet(os.path.join(data_path, "prescription_data.parquet"))

# Stop the Spark session
spark.stop()

