import os
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

DATA_DIR = r'C:\tmp\airflow_data'
INPUT_FILE = 'healthcare-dataset-stroke-data.csv'
OUTPUT_FILE = 'processed_healthcare_data.csv'

def validate_data(**context):
    input_path = os.path.join(DATA_DIR, INPUT_FILE)
    
    # Create sample data if file missing
    if not os.path.exists(input_path):
        os.makedirs(DATA_DIR, exist_ok=True)
        df = pd.DataFrame({
            'gender': ['Male', 'Female'],
            'age': [65, 45],
            'hypertension': [1, 0],
            'stroke': [0, 1]
        })
        df.to_csv(input_path, index=False)
        print(f"Created sample data at {input_path}")
    
    return True

def process_healthcare_data(**context):
    input_path = os.path.join(DATA_DIR, INPUT_FILE)
    output_path = os.path.join(DATA_DIR, OUTPUT_FILE)
    
    df = pd.read_csv(input_path)
    df.dropna(inplace=True)
    df['age_group'] = pd.cut(df['age'], bins=[0, 30, 50, 70, 100], labels=['Young', 'Middle', 'Senior', 'Elderly'])
    df.to_csv(output_path, index=False)
    print(f"Processed data: {len(df)} rows")

def analyze_data(**context):
    output_path = os.path.join(DATA_DIR, OUTPUT_FILE)
    df = pd.read_csv(output_path)
    
    analysis = {
        'total_records': len(df),
        'age_distribution': df['age_group'].value_counts().to_dict(),
        'stroke_risk_summary': df.groupby('age_group')['stroke'].mean().to_dict()
    }
    
    print("Data Analysis Results:")
    print(analysis)

dag = DAG(
    'healthcare_data_pipeline',
    description='Healthcare Data Processing Pipeline',
    schedule_interval=None,
    start_date=datetime(2025, 1, 23),
    catchup=False,
)

validate_task = PythonOperator(
    task_id='validate_data',
    python_callable=validate_data,
    dag=dag,
)

process_task = PythonOperator(
    task_id='process_healthcare_data',
    python_callable=process_healthcare_data,
    dag=dag,
)

analyze_task = PythonOperator(
    task_id='analyze_healthcare_data',
    python_callable=analyze_data,
    dag=dag,
)

validate_task >> process_task >> analyze_task