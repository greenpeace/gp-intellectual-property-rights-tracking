# TARGET BIGQUERY DATASET
locals {
  app_name = "gpi-ipr"
}

variable "entity" {}
variable "environment" {}
variable "project" {}

variable "function_location" {
  default     = "europe-west1"
  description = "Location in which to execute cloud functions"
}

variable "function_memory" {
  default = 1024
}

variable "function_timeout" {
  default = 540
}

# FUNCTION ENVIRONMENT VARIABLES
variable "source_archive_bucket" {
  description = "GCS bucket containing function source"
}

variable "source_archive_object_ali" {
  description = "Path and filename of function source in GCS bucket"
}

variable "source_archive_object_amazon" {
  description = "Path and filename of function source in GCS bucket"
}

variable "source_archive_object_bing" {
  description = "Path and filename of function source in GCS bucket"
}

variable "source_archive_object_cafepress" {
  description = "Path and filename of function source in GCS bucket"
}

# Cloud Scheduler ALI Express
variable "cron_pattern_ali" {
  default = "0 4 * * *"
}

# Cloud Scheduler AMAZON
variable "cron_pattern_amazon" {
  default = "10 4 * * *"
}

# Cloud Scheduler BING
variable "cron_pattern_bing" {
  default = "20 4 * * *"
}

# Cloud Scheduler CAFEPRESS
variable "cron_pattern_cafepress" {
  default = "30 4 * * *"
}
