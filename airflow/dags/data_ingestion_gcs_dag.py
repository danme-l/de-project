"""
Main ETL Pipeline.
Contains all tasks to retrieve data from the source and load it into the DWH.
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

# data specs
base_url = 'https://sitewebbixi.s3.amazonaws.com/uploads/docs/biximontrealrentals'
years = {'2018':'2018-96034e.zip', '2019':'2019-33ea73.zip', '2020':'2020-8e67d9.zip'}

# Store env variables (from docker container) locally 
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
BQ_DATASET = os.environ.get("BQ_DATASET", "bixi_trips_data")

def unzip_data(zip):
    with zipfile.ZipFile(zip, "r") as zf:
        zf.extractall(path_to_local_home)

# currently not working with parquet files
def format_to_parquet(src_dir, year):
    """Converts a CSV files from a given directory, for a specific year, into a parquet file"""
    for file in os.listdir(src_dir):
        if year in file and file.endswith('.csv'):
            table = pv.read_csv(file)
            pq.write_table(table, file.replace('.csv', '.parquet'))
        
        # account for the one file with different naming convention
        if file == "stations.csv":
            table = pv.read_csv(file)
            pq.write_table(table, file.replace('.csv', '.parquet'))
    
def upload_to_gcs(bucket, local_dir):
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

    # get the buckets
    client = storage.Client()
    bucket = client.bucket(bucket)

    # upload every .parquet file in the local directory
    for file in os.listdir(local_dir):
        if file.endswith(".csv"):
            blob = bucket.blob(f"raw/{file}")
            blob.upload_from_filename(file)

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

    for year, zip_spec in years.items():

        download_dataset_task = BashOperator(
            task_id=f"download_{year}data_task",
            bash_command=f"curl -sS {base_url}{zip_spec} > {path_to_local_home}/bixi{year}.zip"
        )

        unzip_data_task = PythonOperator(
            task_id=f"unzip_{year}data_task",
            python_callable=unzip_data,
            op_kwargs={
                "zip": f"{path_to_local_home}/bixi{year}.zip",
            },
        )

        ## FOR THE MOMENT
        # I'm sticking to CSV as it's a little easier to work with
        # format_trips_to_parquet_task = PythonOperator(
        #     task_id=f"format_{year}trips_to_parquet_task",
        #     python_callable=format_to_parquet,
        #     op_kwargs={
        #         "src_dir": f"{path_to_local_home}",
        #         "year": year,
        #     },
        # )

        local_to_gcs_task = PythonOperator(
            task_id=f"{year}data_to_gcs_task",
            python_callable=upload_to_gcs,
            op_kwargs={
                "bucket": BUCKET,
                "local_dir": f"{path_to_local_home}",
            },
        )

        download_dataset_task >> unzip_data_task >>  local_to_gcs_task