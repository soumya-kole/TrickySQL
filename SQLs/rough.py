from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 5, 10),
}

def execute_bigquery_query(**context):
    query = context['dag_run'].conf['query']
    
    insert_task = BigQueryInsertJobOperator(
        task_id='insert_into_bigquery',
        configuration={
            "query": {
                "query": query,
                "useLegacySql": False
            },
            "destination_table": "your_project.your_dataset.new_table",
            "create_disposition": "CREATE_IF_NEEDED",
            "write_disposition": "WRITE_TRUNCATE",
            "location": "US",
        },
        dag=context['dag'],
    )
    insert_task.execute(context=None)

with DAG(
    'dynamic_bigquery_dag',
    default_args=default_args,
    description='A DAG to insert data into BigQuery with a dynamic query',
    schedule_interval=timedelta(days=1),
) as dag:

    execute_query_task = PythonOperator(
        task_id='execute_bigquery_query',
        python_callable=execute_bigquery_query,
        provide_context=True,
    )

execute_query_task
