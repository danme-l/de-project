import os
import logging 

# airflow 
from airflow import DAG
from airflow.utils.dates import days_ago

# operators
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator

# gcs
from google.cloud import storage

# convert to parquet
import pyarrow.csv as pv 
import pyarrow.parquet as pq 

PROJECT_ID =  os.environ.get("GCP_PROJECT_ID")
BUCKET =  os.environ.get("GCP_GCS_BUCKET")

# dataset 
dataset_file = "bixiTrips2020.zip"
dataset_url = 'https://sitewebbixi.s3.amazonaws.com/uploads/docs/biximontrealrentals2020-8e67d9.zip'
parquet_file = dataset_file.replace('.csv','.parquet')

# Store env variables (from docker container) locally 
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
BQ_DATASET = os.environ.get("BQ_DATASET", "bixi_trips_data")

# currently not in use
def format_to_parquet(src_file):
    """Converts a CSV input into a parquet file"""
    if not src_file.endswith('.csv'):
        logging.error("Can only accept source files in CSV format, for the moment")
        return
    table = pv.read_csv(src_file)
    pq.write_table(table, src_file.replace('.csv', '.parquet'))
    
def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1
}

with DAG(
    dag_id="data_ingestion_gcs_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:

    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"curl -sS {dataset_url} > {path_to_local_home}/{dataset_file}"
    )

    # going to come back to this as well as a csv-to-parquet task when I figure it out/next time I work on this
    '''
    unzip_dataset_task = BashOperator(
        task_id="unzip_data_task",
        bash_command=f"unzip {path_to_local_home}/{dataset_file} -d"
    )
    '''

    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"raw/{dataset_file}",
            "local_file": f"{path_to_local_home}/{dataset_file}",
        },
    )

    download_dataset_task >> local_to_gcs_task
