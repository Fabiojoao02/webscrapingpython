from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.sensors.filesystem import FileSensor
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable
import requests
import zipfile
import os
import shutil
from pathlib import Path
from zipfile import ZipFile
from airflow.utils.email import send_email

from enchentes.riodosul import telemetria


CAMINHO_RAIZ = Path(__file__).parent.parent
currentDateTime = datetime.now()
date = currentDateTime.date()
ano = date.strftime("%Y")

arquivo = str(ano)+'.zip'
caminho = CAMINHO_RAIZ / 'data' / arquivo

expurgos = CAMINHO_RAIZ / 'expurgos' / arquivo


default_args = {
    'depends_on_past': False,
    'email': ['fbianastacio@gmail.com'],
    'email_on_failure': False,  # True
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}

# schedule_interval="*/3 * * * * "
dag = DAG('telemetria_dag', description='Dados de telematria',
          schedule_interval='*/5 * * * *', start_date=datetime(2023, 10, 9),
          catchup=False, default_args=default_args, default_view='graph',
          doc_md="## Dag pegar os dados para monitoramento do Rios que cortam Blumenau Rio do Sul")


def captura_conta_dados():

    telemetria()
    if telemetria():
        qtd = 1
    else:
        qtd = 0

    return qtd


group_check_temp = TaskGroup("group_check_temp", dag=dag)
# group_database = TaskGroup('group_database', dag=dag)

# file_sensor_task = FileSensor(
#     task_id='file_sensor_task',
#     filepath=Variable.get('path_file'),
#     fs_conn_id='fs_default',
#     poke_interval=10,
#     dag=dag)

captura_conta_dados = PythonOperator(
    task_id='captura_conta_dados',
    python_callable=captura_conta_dados
)

send_email_alert = EmailOperator(
    task_id='send_email_alert',
    to='fbianastacio@gmail.com',
    subject='Airlfow alert',
    html_content='''<h3>Erro ao fazer o download do arquivo CSV. </h3>
                                <p> Dag: telemetria_dag </p>
                                ''',
    task_group=group_check_temp,
    dag=dag)

send_email_normal = EmailOperator(
    task_id='send_email_normal',
    to='fbianastacio@gmail.com',
    subject='Airlfow advise',
    html_content='''<h3>Download do arquivo CSV concluído com sucesso. </h3>
                                <p> Dag: telemetria_dag </p>
                                ''',
    task_group=group_check_temp,
    dag=dag)


def avalia_temp(ti):
    number = ti.xcom_pull(task_ids='captura_conta_dados', key="qde")
    if number == 0:
        return 'group_check_temp.send_email_alert'
    else:
        return 'group_check_temp.send_email_normal'


check_temp_branc = BranchPythonOperator(
    task_id='check_temp_branc',
    python_callable=avalia_temp,
    provide_context=True,
    dag=dag,
    task_group=group_check_temp)

with group_check_temp:
    check_temp_branc >> [send_email_alert, send_email_normal]

captura_conta_dados >> group_check_temp
