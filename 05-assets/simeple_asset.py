from typing import Any
from airflow.sdk import asset, Asset, Context


@asset(
    schedule="@daily",
    uri="http://192.168.122.168:5000/user",
)
def user(self) -> dict[str, Any]:
    import requests

    r = requests.get(self.uri, timeout=10)
    r.raise_for_status()
    return r.json()


@asset(schedule=user)
def user_location(user: Asset, context: Context) -> dict[str, Any]:
    events = context["triggering_asset_events"][user]
    if not events:
        raise ValueError("No triggering event for the 'user' asset.")
    event = events[-1]

    user_data = context["ti"].xcom_pull(
        dag_id=event.source_dag_id,
        task_ids=event.source_task_id,
        run_id=event.source_run_id,
    )
    if user_data is None:
        raise ValueError(
            f"No XCom found for {event.source_dag_id}/{event.source_task_id} "
            f"run {event.source_run_id}"
        )
    return user_data["personalInfo"]["address"]