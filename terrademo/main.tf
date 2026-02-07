terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.18.0"
    }
  }
}

provider "google" {
  project = "terraform-project-484110"
  region  = "asia-southeast2"
}

#resource {what kind of resource} {name of the resource (local variable)}
resource "google_storage_bucket" "demo-bucket" {
  name          = "demo-bucket-sasa"
  location      = "ASIA-SOUTHEAST2"
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