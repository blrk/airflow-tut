# airflow

### Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install the dependencies 
```bash
pip install --upgrade setuptools wheel pandas graphviz apache-airflow-providers-postgres
```

### Install Airflow 
```bash
pip install apache-airflow
```

### Create Airflow’s metadata database schema 
```bash
airflow db migrate  
```

### Check the installed airflow version 
```bash
airflow version
```

### List the dags
```bash
airflow dags list

dag_id                                              | fileloc                                            | owners  | is_paused | bundle_name  | bundle_version
====================================================+====================================================+=========+===========+==============+===============
Extract_Transform_DAG                               | /home/ec2-user/airflow/dags/bash-op.py             | RK      | False     | dags-folder  | None          
Welcome_DAG                                         | /home/ec2-user/airflow/dags/py-op.py               | RK      | False     | dags-folder  | None          
asset1_producer                                     | /home/ec2-user/.venv/lib64/python3.9/site-packages | airflow | True      | example_dags | None  
```

### List import errors
```bash
airflow dags list-import-errors

bundle_name  | filepath                                                              | error                                                                  
=============+=======================================================================+========================================================================
                                                    
dags-folder  | /home/ec2-user/airflow/dags/bash-op.py                                | Traceback (most recent call last):                                     
             |                                                                       |   File "<frozen importlib._bootstrap>", line 228, in                   
             |                                                                       | _call_with_frames_removed                                              
             |                                                                       |   File "/home/ec2-user/airflow/dags/bash-op.py", line 45, in <module>  
             |                                                                       |     extract >> transform                                               
             |                                                                       | NameError: name 'transform' is not defined 
```

### Update the DAGS folder run reseralize to update the metadata
```bash
airflow dags reserialize
```

## Create database
### Create postgres db container
```bash
docker run -d --name airflow-postgres -e POSTGRES_PASSWORD='p@ssword!@123' -p 5432:5432 postgres:19.0
```

### List providers in airflow
```bash
airflow providers list
```

### Execute .sql in container
```bash
docker exec -i airflow-postgres psql -U postgres -d postgres < table_and_data.sql
```
