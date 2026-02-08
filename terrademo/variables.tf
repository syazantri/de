variable "credentials" {
  description = "Path to the GCP credentials file"
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "Project ID"
  default     = "terraform-project-484110"
}

variable "location" {
  description = "Location of the GCS bucket"
  default     = "asia-southeast2"
}

variable "region" {
  description = "Region for the Google provider"
  default     = "asia-southeast2"
}

variable "bq_dataset_name" {
  description = "Sasa's BigQuery dataset name"
  type        = string
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "Name of the GCS bucket"
  default     = "demo-bucket-sasa"
}

variable "gcs_storage_class" {
  description = "Bucket storage class"
  default     = "STANDARD"
}