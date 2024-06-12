def task_failure_alert(context):

    print("***DAG failed!! do something***")
    print(f"The DAG email: {context['params']['email']}")
    # log_url = f"""{context['params']}/log?dag_id={context['dag']}}&task_id={}&execution_date={}"""
    dag_run = context.get("dag_run")
    for task_instance in dag_run.get_task_instances():
        if task_instance.state == 'failed':
            log_url = dag_run.get_task_instance(context['task_instance'].task_id).log_url
            print(f"{task_instance.task_id} failed inside {context['dag'].dag_id} Log url => {log_url}")
