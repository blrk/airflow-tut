from airflow.sdk import asset, Asset, Context

@asset(
    schedule="@daily",
    uri="http://192.168.122.168:5000/user"
)
def user_multi_asset(self) -> dict[str]:
    import requests
    r = requests.get(self.uri)
    return r.json()

@asset.multi(
    schedule=user_multi_asset,
    outlets=[
    Asset(name="user_location_multi"),
    Asset(name="user_login_multi"),
    ]
)

def user_info_multi_asset(user: Asset, context: Context) -> list[dict[str]]:
    user_data = context['ti'].xcom_pull(
        dag_id=user.name,
        task_ids=user.name,
        include_prior_dates=True,
    )
    return [
        user_data['results'][0]['location'],
        user_data['results'][0]['login']
    ]
