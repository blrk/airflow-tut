from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
import requests

my_args = {
    'owner': 'RK',
    'start_date': datetime(2026,11,23),
    'email': ['admin@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
}


def print_welcome():
    print('Welcome to Airflow!')

def print_date():
    print('Today is {}'.format(datetime.today().date()))

def print_random_quote():
    response = requests.get('https://api.quotable.io/random')
    quote = response.json()['content']
    print('Quote of the day: "{}"'.format(quote))

mydag = DAG(
    'Welcome_DAG',
    default_args=my_args,
    schedule='@daily',
    catchup=False
)

print_welcome_task = PythonOperator(
    task_id='print_welcome',
    python_callable=print_welcome,
    dag=mydag
)

print_date_task = PythonOperator(
    task_id='print_date',
    python_callable=print_date,
    dag=mydag
)

print_random_quote = PythonOperator(
    task_id='print_random_quote',
    python_callable=print_random_quote,
    dag=mydag
)

# Set the dependencies between the tasks
print_welcome_task >> print_date_task >> print_random_quote
