from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, stddev
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Read data path from .env file
data_path = os.getenv('DATA_PATH')

# Initialize Spark Session
spark = SparkSession.builder.appName("HealthcareAnalysis").getOrCreate()

# Load the datasets (Assuming they are saved as Parquet files)
treatments_file_path = os.path.join(data_path, "treatment_data.parquet")
departments_file_path = os.path.join(data_path, "department_data.parquet")

treatments_df = spark.read.parquet(treatments_file_path)
departments_df = spark.read.parquet(departments_file_path)

# Join the datasets on the appropriate key (e.g., DepartmentID)
# Note: Adjust the join keys based on your actual data schema
combined_df = treatments_df.join(departments_df, treatments_df.DepartmentID == departments_df.DepartmentID, "inner")

# Group the data by department and calculate X-bar and S (average and standard deviation)
result_df = combined_df.groupBy("Name").agg(
    avg("Cost").alias("X_bar"),  # Average cost of treatments (X-bar)
    stddev("Cost").alias("S")    # Standard deviation of treatment costs (S)
)

# Save the result to a Parquet file
result_output_path = os.path.join(data_path, "average_treatment_cost_per_department.parquet")
result_df.write.mode('overwrite').parquet(result_output_path)

# Stop the Spark session
spark.stop()

