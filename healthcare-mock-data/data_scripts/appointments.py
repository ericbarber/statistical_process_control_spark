from pyspark.sql import SparkSession
from faker import Faker
import os
from dotenv import load_dotenv
from datetime import timedelta
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

# Sample reasons for visit (modify as needed)
reasons_for_visit = [
    "Routine Checkup", "Consultation", "Follow-up", "Emergency", "Lab Work", "Vaccination"
]

# Sample outcome notes (modify as needed)
outcome_notes = [
    "All clear, follow-up in 6 months", "Prescribed medication, review in 2 weeks",
    "Further tests required", "Immediate treatment provided", "Referred to specialist"
]

# Generate mock data
data = []
for _ in range(num_records):
    appointment_id = fake.uuid4()
    date_and_time = fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
    reason_for_visit = random.choice(reasons_for_visit)
    patient_id = fake.uuid4()  # Generate a random UUID; link to an actual patient in a real scenario
    provider_id = fake.uuid4()  # Generate a random UUID; link to an actual provider in a real scenario
    outcome_note = random.choice(outcome_notes)
    data.append((appointment_id, date_and_time, reason_for_visit, patient_id, provider_id, outcome_note))

# Define schema
columns = ["AppointmentID", "DateAndTime", "ReasonForVisit", "PatientID", "ProviderID", "OutcomeNotes"]

# Create DataFrame
df = spark.createDataFrame(data, schema=columns)

# Show some data to verify
df.show()

# Save DataFrame as Parquet file
df.write.mode('overwrite').parquet(os.path.join(data_path, "appointment_data.parquet"))

# Stop the Spark session
spark.stop()

