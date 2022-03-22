### Airflow
Automated Workflow Orchestration. Airflow allows us to configure workflows as code, using python scripts (essentially configuring files for the workflow) known as DAGs (directed acyclic graphs). There is a very handy webserver with a UI to visualize pipelines, view logs, monitor progress, etc.

I'm using the official Docker setup with some slight modifications courtesy of the DataTalks Team from the main course. See below for the Airflow Docker information.

### DAGS
I currently have two DAGS in here. *data_ingestion_gcs_dag.py* is the main one that handles the data from 2018, 2019 and 2020, and I'll possibly be adding the other years as well soon in the coming days. *data_ingestion_gcs_2020_dag.py* was the original test DAG to make sure I could get everything going and handles only 2020 data. 

Both are structured the exact same way:
**download_dataset_task >> unzip_data_task >> [format_trips_to_parquet_task >>] local_to_gcs_task**
1. Compressed data is retrieved from the source using *cURL* in a BashOperator
2. Data is unzipped into the airflow home directory, /opt/airflow in the airflow worker docker container
3. EDIT: I'm currently not working with parquet as I'm having a little bit of trouble using the format. I'm going to complete the project barebones with CSV first.
 --- All the data is reformatted to parquet. This isn't strictly necessary since I'm working with under 1GB of data at the moment but I figure it's good practice for larger datasets
4. Uploaded to Google Cloud Storage as Parquet files

### Docs for various links and notes
* [Official Docs](https://airflow.apache.org/docs/apache-airflow/stable/index.html) 
* [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
* [Dockerfile with google cloud services](https://airflow.apache.org/docs/docker-stack/recipes.html)
* [Official Setup Guidelines from the course repository](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_2_data_ingestion/airflow/1_setup_official.md)