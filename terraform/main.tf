# terraform resource
terraform {
    required_version = ">=1.0"
    backend "local" {} # can change from local to gcs
    required_providers {
      google = {
          source = "hashicorp/google"
      }
    }
}

provider "google" {
    project = var.project
    region = var.region
}

resource "google_storage_bucket" "data_lake_bucket"{
    name = "${local.data_lake_bucket}_${var.project}" # Concatenating DL bucket & Project name for unique naming
    location = var.region

    storage_class = var.storage_class
    uniform_bucket_level_access = true

    versioning {
      enabled = true
    }

    # allows us to delete the bucket and it's contents 
    force_destroy = true
}

# data warehouse
resource "google_bigquery_dataset" "dataset" {
    dataset_id = var.BQ_DATASET 
    project    = var.project
    location   = var.region
}

