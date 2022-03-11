locals {
    data_lake_bucket = "data_lake_bucket"
}

variable "project" {
    description = "GCP Project ID"
}

variable "region" {
    description = "Region for GCP Resources"  
    default = "northamerica-northeast1"
}

# not currently needed since ours is defined in local
variable "bucket_name" {
    description = "Name of Cloud Storage Bucket."
    default = ""
}

variable "storage_class" {
    description = "Storage class type for my bucket"
    default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to."
  type = string
  default = "bixi_trips_data"
}

variable "TABLE_NAME" {
    description = "BigQuery Table"  
    type = string
    default = "bixi_trips"
}