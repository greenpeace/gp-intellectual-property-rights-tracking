# TARGET BIGQUERY DATASET
locals {
  app_name = "gpiipr"
}

variable "entity" {}
variable "environment" {}
variable "project" {}

variable "function_location" {
  default     = "europe-north1"
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

variable "source_archive_object_selector" {
  description = "Path and filename of function source in GCS bucket"
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

variable "source_archive_object_duckduckgo" {
  description = "Path and filename of function source in GCS bucket"
}

variable "source_archive_object_ebay" {
  description = "Path and filename of function source in GCS bucket"
}

variable "source_archive_object_etsy" {
  description = "Path and filename of function source in GCS bucket"
}

variable "source_archive_object_googlesearch" {
  description = "Path and filename of function source in GCS bucket"
}

variable "source_archive_object_redbubble" {
  description = "Path and filename of function source in GCS bucket"
}

variable "source_archive_object_spreadshirt" {
  description = "Path and filename of function source in GCS bucket"
}

variable "source_archive_object_teepublic" {
  description = "Path and filename of function source in GCS bucket"
}

# Cloud Scheduler ALI Express
variable "cron_pattern_ali" {
  default = "0 9 * * 1"
}

# Cloud Scheduler AMAZON
variable "cron_pattern_amazon" {
  default = "10 9 * * 1"
}

# Cloud Scheduler BING
variable "cron_pattern_bing" {
  default = "10 8 * * 1"
}

# Cloud Scheduler CAFEPRESS
variable "cron_pattern_cafepress" {
  default = "20 9 * * 1"
}

# Cloud Scheduler DuckDuckGo
variable "cron_pattern_duckduckgo" {
  default = "20 8 * * 1"
}

# Cloud Scheduler Ebay
variable "cron_pattern_ebay" {
  default = "30 9 * * 1"
}

# Cloud Scheduler ETSY
variable "cron_pattern_etsy" {
  default = "40 9 * * 1"
}

# Cloud Scheduler Google Search
variable "cron_pattern_googlesearch" {
  default = "0 8 * * 1"
}

# Cloud Scheduler REDBUBBLE
variable "cron_pattern_redbubble" {
  default = "50 9 * * 1"
}

# Cloud Scheduler Spreadshirt
variable "cron_pattern_spreadshirt" {
  default = "0 10 * * 1"
}

# Cloud Scheduler Teepublic
variable "cron_pattern_teepublic" {
  default = "10 10 * * 1"
}