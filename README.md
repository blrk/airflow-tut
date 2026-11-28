# airflow

### Create and activate a Python virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
### Install the dependencies 
```bash
pip install --upgrade setuptools wheel pandas graphviz apache-airflow-providers-postgres
```
### generate fernet token 
```bash
FERNET_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" 2>/dev/null || openssl rand -base64 32)
cat <<EOF > /home/ec2-user/.env
FERNET_KEY=${FERNET_KEY}
AIRFLOW_UID=$(id -u)
EOF
```
# Run airflow using docker 
```bash
mkdir airflow
cd airflow 
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
docker compose up -d
```
### How to compile a dag or assest
```bash
docker exec airflow-airflow-scheduler-1 python -m py_compile /opt/airflow/dags/simeple_asset.py
```

### How list the assest 
```bash
docker exec airflow-airflow-scheduler-1 airflow assets list
```
### How to materalise an asset
```bash
docker exec airflow-airflow-scheduler-1 airflow assets materialize --name user
```
### How to view the errors 
```bash
docker exec airflow-airflow-scheduler-1 airflow dags list-import-errors
```

# Install airflow standalone server

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
