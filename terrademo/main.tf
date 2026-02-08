terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.18.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

#resource {what kind of resource} {name of the resource (local variable)}
resource "google_storage_bucket" "demo-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true



  lifecycle_rule {
    condition {
      age = 1 #in days
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}