from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from groups.group_api_request import request_api
from airflow.operators.python import PythonOperator

from datetime import datetime

def _process_data(ti):
    data = ti.xcom_pull(task_ids="request_api_method_1")
    print(data)


with DAG(
    "api_request_dag",
    start_date=datetime(2022, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='fast_api',
        endpoint='/'
    )

    send_api_request = request_api()

    process_data = PythonOperator(
        task_id='process_data',
        python_callable=_process_data
    )

    is_api_available >> send_api_request >> process_data
