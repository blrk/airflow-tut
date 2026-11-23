# airflow

### Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install the dependencies 
```bash
pip install --upgrade setuptools wheel pandas
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
