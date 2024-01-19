from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from faker import Faker
import random
from dotenv import load_dotenv
import os

# Initialize Faker and set seed for reproducibility
fake = Faker()
Faker.seed(4321)
random.seed(4321)

# Load environment variables
load_dotenv()

# Read data path from .env file
data_path = os.getenv('DATA_PATH')

# Initialize Spark Session
spark = SparkSession.builder.appName("HealthcareMockData").getOrCreate()

# Load conditions data
conditions_sdf = spark.read.parquet(os.path.join(data_path,"conditions_data.parquet"))
conditions_pdf = conditions_sdf.toPandas()

# Randonly assign a condition
def get_condition(conditions_pdf, percentage=0.3):
    if random.random() < percentage:
        condition = conditions_pdf.sample().iloc[0]['Condition']
    else:
        condition = ""  # Leave it blank
    return condition


# Number of records to generate
num_records = 1000

# Generate mock data
data = []
for _ in range(num_records):
    patient_id = fake.uuid4()
    name = fake.name()
    date_of_birth = str(fake.date_of_birth(minimum_age=0, maximum_age=100))
    gender = random.choice(['Male', 'Female', 'Other'])
    contact_information = fake.address()
    insurance_details = fake.ssn()  # or any appropriate representation
    medical_history = get_condition(conditions_pdf, percentage=0.3)
    family_history = get_condition(conditions_pdf, percentage=0.5)
    data.append((patient_id, name, date_of_birth, gender, contact_information, insurance_details, medical_history, family_history))

# Define schema
columns = ["PatientID", "Name", "DateOfBirth", "Gender", "ContactInformation", "InsuranceDetails", "MedicalHistory", "FamilyHistory"]

# Create DataFrame
df = spark.createDataFrame(data, schema=columns)

# Show some data to verify
df.show()

# Save DataFrame as Parquet file
df.write.mode('overwrite').parquet(os.path.join(data_path, "patient_data.parquet"))

# Stop the Spark session
spark.stop()

