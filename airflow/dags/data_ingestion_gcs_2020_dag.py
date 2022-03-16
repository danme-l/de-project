"""
Original Test DAG. 
Pipeline only for moving 2020 data from the source into the GCS bucket.
"""
import os
import logging 
import zipfile

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
dataset_zip = "bixiTrips2020.zip"
dataset_file = 'OD_2020.csv'
stations_file = 'stations.csv'
dataset_url = 'https://sitewebbixi.s3.amazonaws.com/uploads/docs/biximontrealrentals2020-8e67d9.zip'
parquet_file = dataset_zip.replace('.csv','.parquet')

# Store env variables (from docker container) locally 
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
BQ_DATASET = os.environ.get("BQ_DATASET", "bixi_trips_data")

def unzip_data(zip):
    with zipfile.ZipFile(zip, "r") as zf:
        zf.extractall(path_to_local_home, [dataset_file, stations_file])


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
    dag_id="data_ingestion_gcs_2020_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:

    download_2020_data_task = BashOperator(
        task_id="download_2020_data_task",
        bash_command=f"curl -sS {dataset_url} > {path_to_local_home}/{dataset_zip}"
    )

    unzip_2020_data_task = PythonOperator(
        task_id="unzip_2020_data_task",
        python_callable=unzip_data,
        op_kwargs={
            "zip": f"{path_to_local_home}/{dataset_zip}",
        },
    )

    format_2020_trips_to_parquet_task = PythonOperator(
        task_id="format_2020_trips_to_parquet_task",
        python_callable=format_to_parquet,
        op_kwargs={
            "src_file": f"{path_to_local_home}/{dataset_file}",
        },
    )

    local_to_gcs_2020_task = PythonOperator(
        task_id="local_to_gcs_2020_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"raw/{parquet_file}",
            "local_file": f"{path_to_local_home}/{parquet_file}",
        },
    )

    download_2020_data_task >> unzip_2020_data_task >> format_2020_trips_to_parquet_task >> local_to_gcs_2020_task