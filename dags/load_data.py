from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

# 1. DEFINE THE DAG
# This works like a wrapper. Everything inside acts as one "Job".
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    'load_ad_data_v1',
    default_args=default_args,
    schedule_interval=None, # We will trigger this manually
    catchup=False
) as dag:

    # 2. TASK 1: CREATE TABLE
    # This sends SQL directly to Postgres to ensure the table exists.
    create_table = PostgresOperator(
        task_id='create_postgres_table',
        postgres_conn_id='postgres_default',
        sql="""
            CREATE TABLE IF NOT EXISTS raw_ad_clicks (
                user_id INT,
                timestamp TIMESTAMP,
                experiment_group TEXT,
                device_type TEXT,
                clicked INT
            );
        """
    )

    # 3. TASK 2: LOAD DATA
    # Python logic to read the CSV and push it to Postgres using the Hook.
    def load_csv_to_postgres():
        # 1. Define the connection string manually
        # Format: postgresql://user:password@host:port/database
        # We use 'postgres' as the host because that is the container name in Docker
        db_url = 'postgresql://user:password@postgres:5432/warehouse'
        
        # 2. Create the engine
        engine = create_engine(db_url)
        
        # 3. Read the CSV
        file_path = '/opt/airflow/data/ad_clicks.csv'
        df = pd.read_csv(file_path)
        print(f"Read {len(df)} rows from CSV.")
        
        # 4. Write to SQL
        df.to_sql(
            'raw_ad_clicks', 
            con=engine, 
            if_exists='replace', 
            index=False,
            chunksize=1000
        )
        print("Data loaded successfully via Direct Connection!")

    load_data = PythonOperator(
        task_id='load_data_from_csv',
        python_callable=load_csv_to_postgres
    )

    # 4. SET DEPENDENCIES
    # "create_table" must finish before "load_data" starts.
    create_table >> load_data