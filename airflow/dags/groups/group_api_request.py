from airflow import DAG
from airflow.utils.task_group import TaskGroup
from airflow.providers.http.operators.http import SimpleHttpOperator

def request_api():

    with TaskGroup("api_request", tooltip="Request apis") as group:
        request_api_method_1 = SimpleHttpOperator(
            task_id='request_api_method_1',
            http_conn_id='fast_api',
            endpoint='/search/naver',
            method='GET'
        )

        request_api_method_2 = SimpleHttpOperator(
            task_id='request_api_method_2',
            http_conn_id='fast_api',
            endpoint='/search/kakao',
            method='GET'
        )

        return group