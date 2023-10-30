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
import os
import shutil
from pathlib import Path
from zipfile import ZipFile
from airflow.utils.email import send_email

import pandas as pd

default_args = {
    'depends_on_past': False,
    'email': ['fbianastacio@gmail.com'],
    'email_on_failure': False,  # True
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}

# # schedule_interval="*/3 * * * * "
dag = DAG('telemetria_dag', description='Dados de telematria',
          schedule='50 * * * *', start_date=datetime(2023, 10, 9),
          catchup=False, default_args=default_args, default_view='graph',
          doc_md="## Dag monitoramento dos Rios que cortam Blumenau - Rio do Sul")

group_check_temp = TaskGroup("group_check_temp", dag=dag)
# group_database = TaskGroup('group_database', dag=dag)


file_sensor_task = FileSensor(
    task_id='file_sensor_task',
    filepath=Variable.get('path_file'),
    fs_conn_id='fs_default',
    poke_interval=10,
    dag=dag)


def process_file(**kwarg):
    df_mov = pd.read_csv(Variable.get('path_file'), delimiter=';',
                         encoding='utf-8')

    vlr_nivel_Rio = df_mov['vlr_nivel_rio'].tolist()
    print(vlr_nivel_Rio)
    nome_rio = df_mov['nome_rio'].tolist()
    print(nome_rio)
    # #
    kwarg['ti'].xcom_push(key='nome_rio', value=df_mov['nome_rio'].tolist())
    kwarg['ti'].xcom_push(key='vlr_nivel_rio',
                          value=df_mov['vlr_nivel_rio'].tolist())

   # Copia o arquivo
    shutil.copy(Variable.get('path_file'),
                Variable.get('path_file_expurgo'))
   # remove arquivo
    os.remove(Variable.get('path_file'))


get_data = PythonOperator(
    task_id='get_data',
    python_callable=process_file,
    provide_context=True,
    dag=dag)

send_email_alert = EmailOperator(
    task_id='send_email_alert',
    to='fbianastacio@gmail.com',
    subject="Airlfow alert ",
    html_content=("Alerta de Nivel do Rio."
                  "{% set vlr_nivel = ti.xcom_pull(task_ids='get_data', key='vlr_nivel_rio') %}"
                  "{% set nome_rio = ti.xcom_pull(task_ids='get_data', key='nome_rio') %}"
                  # Rio Itajaí-Açu Rio do Sul - 680
                  "<p>nome_rio: {{ nome_rio[0] }} - {{ vlr_nivel[0]|int }}</p>"
                  # Rio Itajaí do Oeste Rio do Sul - 677
                  "<p>nome_rio: {{ nome_rio[1] }} - {{ vlr_nivel[1]|int }}</p>"
                  # Rio Itajaí do Sul Rio do Sul - 713
                  "<p>nome_rio: {{ nome_rio[2] }} - {{ vlr_nivel[2]|int }}</p>"
                  "{% if vlr_nivel[0]|int  > 1000 %}"
                  "<p style='color:red;'>O nível do rio {{ nome_rio[0] }} é de {{ vlr_nivel[0] }}cm.</p>"
                  "{% endif %}"
                  "{% if vlr_nivel[1]|int  > 1000 %}"
                  "<p style='color:red;'>O nível do rio {{ nome_rio[1] }} é de {{ vlr_nivel[1] }}cm.</p>"
                  "{% endif %}"
                  "{% if vlr_nivel[2]|int  > 700 %}"
                  "<p style='color:red;'>O nível do rio {{ nome_rio[2] }} é de {{ vlr_nivel[2] }}cm.</p>"
                  "{% endif %}"
                  "Dag: telemetria_dag"
                  ),
    task_group=group_check_temp,
    dag=dag)


def avalia_nivel(**context):
    # Recupera os dados do XCom
    vlr_niveis = context['ti'].xcom_pull(
        task_ids='get_data', key='vlr_nivel_rio')
    nomes_rios = context['ti'].xcom_pull(
        task_ids='get_data', key='nome_rio')

    tarefas = []  # Lista para armazenar as tarefas a serem executadas

    for vlr_nivel, nome_rio in zip(vlr_niveis, nomes_rios):
        vlr_nivel = float(vlr_nivel)
        # Concatena o nome do rio e o valor do nível

        if nome_rio == 'Ponte Dom Tito Buss - Rio Itajaí-Açu Rio do Sul' and vlr_nivel >= 1000:
            tarefas.append('group_check_temp.send_email_alert')
        elif nome_rio == 'Ponte BR-470 - Rio Itajaí do Oeste Rio do Sul' and vlr_nivel >= 1000:
            tarefas.append('group_check_temp.send_email_alert')
        elif nome_rio == 'Ponte Hannelore Hartmann Eyng - Rio Itajaí do Sul Rio do Sul' and vlr_nivel >= 700:
            tarefas.append('group_check_temp.send_email_alert')

    return tarefas


check_temp_branc = BranchPythonOperator(
    task_id='check_temp_branc',
    python_callable=avalia_nivel,
    provide_context=True,
    dag=dag,
    task_group=group_check_temp)


with group_check_temp:
    check_temp_branc >> [send_email_alert]

file_sensor_task >> get_data
get_data >> group_check_temp
