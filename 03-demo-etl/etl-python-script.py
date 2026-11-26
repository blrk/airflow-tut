import pandas as pd
from datetime import datetime
import os
from airflow.providers.postgres.hooks.postgres import PostgresHook

def fetch_data_from_postgres():
    # Uses the Airflow connection ID "db"
    postgres_hook = PostgresHook(postgres_conn_id='db')
    query = 'SELECT * FROM customer'
    df = postgres_hook.get_pandas_df(sql=query)
    return df

def transform_data(df):
    # Keep customers whose age is greater than 30
    df_transformed = df[df['age'] > 30]
    return df_transformed

def write_data_to_file(df):
    output_dir = '/opt/airflow/outputs'
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f'etl_output_{timestamp}.csv'
    file_path = os.path.join(output_dir, file_name)
    df.to_csv(file_path, index=False)
    print(f'Data written to {file_path}')

def etl_process():
    # Extract
    df = fetch_data_from_postgres()
    # Transform
    df_transformed = transform_data(df)
    # Load
    write_data_to_file(df_transformed)

if __name__ == "__main__":
    etl_process()