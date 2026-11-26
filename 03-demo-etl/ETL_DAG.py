import importlib.util
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Load etl_process from your external script path (handles hyphens in filename)
script_path = '/opt/airflow/outputs/etl-python-script.py'
spec = importlib.util.spec_from_file_location('etl_script', script_path)
etl_script = importlib.util.module_from_spec(spec)
spec.loader.exec_module(etl_script)

my_args = {
    'owner': 'RK',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'postgres_etl_dag',
    default_args=my_args,
    description='A PostgreSQL ETL DAG',
    schedule=timedelta(minutes=3),
    start_date=datetime(2026, 11, 23),
    catchup=False,
) as mydag:

    run_etl = PythonOperator(
        task_id='run_etl_postgres',
        python_callable=etl_script.etl_process,
    )
