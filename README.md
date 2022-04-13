# Repository for my Project for the DataTalks Data Engineering Zoomcamp

DataTalks ran a free [Data Engineering Course](https://github.com/DataTalksClub/data-engineering-zoomcamp) and this repository contains my final project.

The goal of the project is to build an end-to-end data pipeline, using some or all of the following technologies:
* Cloud: Google Cloud Platform
* Infrastructure as code (IaC): Terraform
* Workflow orchestration: Airflow
* Data Warehouse: BigQuery
* Batch processing: Spark(?)
* Analytics/Visualization: dbt(?), Google Data Studio

The dataset I'm going to use the [trip data from Montreal's Bixi Bike system](https://bixi.com/en/open-data), a network of on-demand bicycles that I used when I was living in my beloved Montreal.

# Project Architecture
... in progress

# Current Status 
## *Just Finished*:
Data Warehouse with the two tables is set up, but there is an issue with table partitioning (see [data-warehouse/README](/data-warehouse/README.md)). I connected the DW to Google Data Studio and begun work on final visualization.

## *Next on the docket*:
* Fix BQ table partitioning issue
* Incorporate the stations script into Airflow pipeline
* Finish visualization