from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from groups.group_api_request import request_api
from airflow.operators.python import PythonOperator

from datetime import datetime

def _process_data(**context):
    request_api_data_1 = context['ti'].xcom_pull(task_ids='api_request.request_api_method_1', key='return_value')

    request_api_data_2 = context['ti'].xcom_pull(task_ids='api_request.request_api_method_2', key='return_value')

    context['ti'].xcom_push(key='api_1', value=request_api_data_1)
    context['ti'].xcom_push(key='api_2', value=request_api_data_2)
    
default_args = {
    "Owner": "hg",
    "depends_on_past": False,
    "start_date": datetime(2022, 8, 1),
    "provide_context": True
}

with DAG(
    "api_request_dag",
    default_args=default_args,
    schedule_interval="@daily"
) as dag:

    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='fast_api',
        endpoint='/'
    )

    send_api_request = request_api()

    process_data = PythonOperator(
        task_id='process_data',
        python_callable=_process_data,
    )

    is_api_available >> send_api_request >> process_data
