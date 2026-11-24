from airflow.sdk import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk.bases.sensor import PokeReturnValue
from airflow.providers.postgres.hooks.postgres import PostgresHook

API_URL = "http://192.168.122.168:5000/user"

@dag
def user_processing():

    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="db",
        sql="""
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY,
            firstname VARCHAR(255),
            lastname VARCHAR(255),
            email VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
    )

    @task.sensor(poke_interval=30, timeout=300, mode="poke")
    def is_api_available() -> PokeReturnValue:
        import requests

        try:
            response = requests.get(API_URL, timeout=10)
            print(f"Status code: {response.status_code}")
            if response.status_code == 200:
                return PokeReturnValue(is_done=True)
        except requests.RequestException as exc:
            print(f"API not reachable yet: {exc}")
        return PokeReturnValue(is_done=False)

    @task
    def extract_user() -> dict:
        import requests

        d = requests.get(API_URL, timeout=10).json()
        return {
            "id": int(d["id"]),
            "firstname": d["personalInfo"]["firstName"],
            "lastname": d["personalInfo"]["lastName"],
            "email": d["personalInfo"]["email"],
        }

    @task
    def process_user(user_info: dict) -> str:
        import csv
        import io
        from datetime import datetime

        user_info["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=user_info.keys())
        writer.writeheader()
        writer.writerow(user_info)
        return buf.getvalue()

    @task
    def store_user(csv_data: str) -> None:
        import csv
        import io

        row = next(csv.DictReader(io.StringIO(csv_data)))
        hook = PostgresHook(postgres_conn_id="db")
        hook.run(
            """
            INSERT INTO users (id, firstname, lastname, email, created_at)
            VALUES (%(id)s, %(firstname)s, %(lastname)s, %(email)s, %(created_at)s)
            ON CONFLICT (id) DO NOTHING
            """,
            parameters=row,
        )

    api_check = is_api_available()
    user_data = extract_user()
    csv_payload = process_user(user_data)
    stored = store_user(csv_payload)

    create_table >> api_check >> user_data
    # process_user and store_user run after extract_user automatically,
    # because they take its output as input.

user_processing()