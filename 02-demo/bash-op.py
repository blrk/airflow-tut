from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime,timedelta

#defining DAG arguments

# You can override them on a per-task basis during operator initialization
my_args = {
'owner':'RK',
'start_date': datetime(2026,11,23),
'email': ['admin@example.com'],
'email_on_failure': False,
'email_on_retry': False,
'retries': 1,
'retry_delay': timedelta(minutes=5),
}

# defining the DAG
dag = DAG(
'Extract_Transform_DAG',
default_args=my_args,
description='Using Bash commands',
schedule=timedelta(days=1),
)

# define the tasks

# first task

extract = BashOperator(
task_id='extract',
bash_command='cut -d":" -f1,3,6 /etc/passwd > /tmp/extracted-data.txt',
dag=dag,
)

# Second task
transform_and_load = BashOperator(
task_id='transform',
bash_command='tr ":" "," < /tmp/extracted-data.txt > /tmp/transformed-data.csv',
dag=dag,
)

# task pipeline 
extract >> transform_and_load