from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from datetime import datetime, timedelta
import requests
import pandas as pd
import json

# Function to fecth data from API (103.150.197.96:5005)
def fecth_api_data(ti):
    url = "http://103.150.197.96:5005/api/v1/rekapitulasi_v2/jabar/harian"
    headers = {"Content-Type": "application/json"}
    params = {"level": "kab"}
    
    response = requests.get(url, headers=headers, params=params)
    covid_data = response.json()
    
    ti.xcom_push(key='covid_data', value=covid_data)

# Function to transform data
def transform_data(ti):
    transformed_data = []
    covid_data = ti.xcom_pull(key='covid_data', task_ids='fetch_data')
    
    for data in covid_data['data']['content']:
        closecontact = data['CLOSECONTACT']
        confirmation = data['CONFIRMATION']
        probable = data['PROBABLE']
        suspect = data['SUSPECT']
        closecontact_dikarantina = data['closecontact_dikarantina']
        closecontact_discarded = data['closecontact_discarded']
        closecontact_meninggal = data['closecontact_meninggal']
        confirmation_meninggal = data['confirmation_meninggal']
        confirmation_sembuh = data['confirmation_sembuh']
        kode_kab = data['kode_kab']
        kode_prov = data['kode_prov']
        nama_kab = data['nama_kab']
        nama_prov = data['nama_prov']
        probable_diisolasi = data['probable_diisolasi']
        probable_discarded = data['probable_discarded']
        probable_meninggal = data['probable_meninggal']
        suspect_diisolasi = data['suspect_diisolasi']
        suspect_discarded = data['suspect_discarded']
        suspect_meninggal = data['suspect_meninggal']
        tanggal = data['tanggal']
        
        transformed_data.append((closecontact ,confirmation ,probable ,suspect ,closecontact_dikarantina ,closecontact_discarded ,closecontact_meninggal ,confirmation_meninggal ,confirmation_sembuh ,kode_kab ,kode_prov ,nama_kab ,nama_prov ,probable_diisolasi ,probable_discarded ,probable_meninggal ,suspect_diisolasi ,suspect_discarded ,suspect_meninggal ,tanggal))
    
        ti.xcom_push(key='transformed_data', value=transformed_data)

# Function to inserd data to PostgreSQL
def insert_to_postgres(ti):
    pg_hook = PostgresHook(postgres_conn_id='postgres_conn')
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    
    transformed_data = ti.xcom_pull(key='transformed_data', task_ids='transform_data')
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS jabar_covid_kab (closecontact INT, confirmation INT, probable INT, suspect INT, closecontact_dikarantina INT, closecontact_discarded INT, \
            closecontact_meninggal INT, confirmation_meninggal INT, confirmation_sembuh INT, kode_kab VARCHAR, kode_prov VARCHAR, nama_kab VARCHAR, \
                nama_prov VARCHAR,probable_diisolasi INT, probable_discarded INT, probable_meninggal INT, suspect_diisolasi INT, suspect_discarded INT, \
                    suspect_meninggal INT, tanggal DATE)"
    )
    
    cursor.execute(
        "DELETE FROM jabar_covid_kab"
    )
    
    for record in transformed_data:
        cursor.execute(
            "INSERT INTO jabar_covid_kab(closecontact ,confirmation ,probable ,suspect ,closecontact_dikarantina ,closecontact_discarded ,closecontact_meninggal ,\
                confirmation_meninggal ,confirmation_sembuh ,kode_kab ,kode_prov ,nama_kab ,nama_prov ,probable_diisolasi ,probable_discarded ,\
                    probable_meninggal ,suspect_diisolasi ,suspect_discarded ,suspect_meninggal ,tanggal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", record
        )
    
    connection.commit()
    cursor.close()
    connection.close()

# Function to load data from PostgreSQL to Snowflake
def load_data_to_snowflake(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres_conn')
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    
    # Read data from PostgreSQL
    query = "SELECT * FROM jabar_covid_kab"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Close PostgreSQL connection
    cursor.close()
    connection.close()
    
    # Convert data to pandas DataFrame
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    
    # Snowflake connection details
    snowflake_conn_id = 'snowflake_conn'
    snowflake_hook = SnowflakeHook(snowflake_conn_id)
    engine = snowflake_hook.get_sqlalchemy_engine()
    
    # Write data to Snowflake
    df.to_sql('jabar_covid_kab', engine, if_exists='replace', index=False)

# Define defualt arguments for the DAG
default_args = {
    'owner': 'zainal_abidin',
    'depends_on_past': False,
    'start_date': datetime(2023,1,1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Define the DAG
with DAG(
    'api_postgres_dag',
    default_args=default_args,
    description='Fect Jabar API data and store in PostgreSQL',
    schedule_interval=timedelta(days=1),
    catchup=False
) as dag:
    # Task to fetch data from API
    fecth_data = PythonOperator(
        task_id='fetch_data',
        python_callable=fecth_api_data,
        provide_context=True
    )
    
    # Task to transorm and store data
    transform_api_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        provide_context=True
    )
    
    # Task to transorm and store data
    load_to_postgres = PythonOperator(
        task_id='load_to_postgres',
        python_callable=insert_to_postgres,
        provide_context=True
    )
    
    # Task to load data from PostgreSQL to Snowflake
    load_to_snowflake = PythonOperator(
        task_id='load_to_snowflake',
        python_callable=load_data_to_snowflake,
        provide_context=True
    )
    
    # Set task dependencies
    fecth_data >> transform_api_data >> load_to_postgres >> load_to_snowflake