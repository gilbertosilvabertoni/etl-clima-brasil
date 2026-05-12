from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys

# Adiciona o src ao path para importar os módulos
sys.path.insert(0, '/opt/airflow/src')

from extract import extrair_todas_cidades
from transform import transformar
from load import carregar
from database import executar

# Configurações padrão de cada task
default_args = {
    'owner': 'gilberto',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
}

with DAG(
    dag_id='clima_brasil_pipeline',
    description='Pipeline ETL de dados climáticos das 5 capitais brasileiras',
    schedule='0 6 * * *',        # todo dia às 6h da manhã
    start_date=datetime(2026, 5, 1),
    catchup=False,
    default_args=default_args,
    tags=['clima', 'etl', 'brasil'],
) as dag:

    task_extract = PythonOperator(
        task_id='extrair_dados_api',
        python_callable=extrair_todas_cidades,
    )

    task_transform = PythonOperator(
        task_id='transformar_dados',
        python_callable=transformar,
    )

    task_load = PythonOperator(
        task_id='carregar_relatorio',
        python_callable=carregar,
    )

    task_database = PythonOperator(
        task_id='carregar_banco',
        python_callable=executar,
    )

    # Define a ordem de execução
    task_extract >> task_transform >> task_load >> task_database