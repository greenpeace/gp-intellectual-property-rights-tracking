locals {
  app_name = "gpiipr"
}

resource "google_storage_bucket" "source" {
  name          = "${var.project}-${local.app_name}-source"
  location      = "EU"
  project       = var.project
  force_destroy = "true"

  # For uniform bucket ACL
  uniform_bucket_level_access = true

  labels = {
    app       = "${local.app_name}-source"
    component = "source"
  }
}
data "archive_file" "source_selector" {
  type        = "zip"
  source_dir  = "${path.module}/../../gp-selector/src"
  output_path = "${path.module}/../../gp-selector/src/build/${local.app_name}_selector.zip"
  excludes    = ["__pycache__", "Makefile", "requirements-dev.txt", "build"]
}

data "archive_file" "source_ali" {
  type        = "zip"
  source_dir  = "${path.module}/../../gp-techlab-alisearchbot/src"
  output_path = "${path.module}/../../gp-techlab-alisearchbot/src/build/${local.app_name}_ali.zip"
  excludes    = ["package-lock.json", "node_modules", "requirements-dev.txt", "build"]
}

data "archive_file" "source_amazon" {
  type        = "zip"
  source_dir  = "${path.module}/../../gp-techlab-amazonsearchbot/src"
  output_path = "${path.module}/../../gp-techlab-amazonsearchbot/src/build/${local.app_name}_amazon.zip"
  excludes    = ["__pycache__", "Makefile", "requirements-dev.txt", "build"]
}

data "archive_file" "source_bing" {
  type        = "zip"
  source_dir  = "${path.module}/../../gp-techlab-bingbot/src"
  output_path = "${path.module}/../../gp-techlab-bingbot/src/build/${local.app_name}_bingbot.zip"
  excludes    = ["__pycache__", "Makefile", "requirements-dev.txt", "build"]
}

data "archive_file" "source_cafepress" {
  type        = "zip"
  source_dir  = "${path.module}/../../gp-techlab-cafepressbot/src"
  output_path = "${path.module}/../../gp-techlab-cafepressbot/src/build/${local.app_name}_cafepress.zip"
  excludes    = ["__pycache__", "Makefile", "requirements-dev.txt", "build"]
}

data "archive_file" "source_duckduckgo" {
  type        = "zip"
  source_dir  = "${path.module}/../../gp-techlab-duckduckgobot/src"
  output_path = "${path.module}/../../gp-techlab-duckduckgobot/src/build/${local.app_name}_duckduckgo.zip"
  excludes    = ["__pycache__", "Makefile", "requirements-dev.txt", "build"]
}

data "archive_file" "source_ebay" {
  type        = "zip"
  source_dir  = "${path.module}/../../gp-techlab-ebaysearchbot/src"
  output_path = "${path.module}/../../gp-techlab-ebaysearchbot/src/build/${local.app_name}_ebay.zip"
  excludes    = ["__pycache__", "Makefile", "requirements-dev.txt", "build"]
}

data "archive_file" "source_etsy" {
  type        = "zip"
  source_dir  = "${path.module}/../../gp-techlab-etsysearchbot/src"
  output_path = "${path.module}/../../gp-techlab-etsysearchbot/src/build/${local.app_name}_etsy.zip"
  excludes    = ["__pycache__", "Makefile", "requirements-dev.txt", "build"]
}

data "archive_file" "source_googlesearch" {
  type        = "zip"
  source_dir  = "${path.module}/../../gp-techlab-googlesearchbot/src"
  output_path = "${path.module}/../../gp-techlab-googlesearchbot/src/build/${local.app_name}_googlesearch.zip"
  excludes    = ["__pycache__", "Makefile", "requirements-dev.txt", "build"]
}

data "archive_file" "source_redbubble" {
  type        = "zip"
  source_dir  = "${path.module}/../../gp-techlab-redbubblesearchbot/src"
  output_path = "${path.module}/../../gp-techlab-redbubblesearchbot/src/build/${local.app_name}_redbubble.zip"
  excludes    = ["__pycache__", "Makefile", "requirements-dev.txt", "build"]
}

data "archive_file" "source_spreadshirt" {
  type        = "zip"
  source_dir  = "${path.module}/../../gp-techlab-spreadshirt/src"
  output_path = "${path.module}/../../gp-techlab-spreadshirt/src/build/${local.app_name}_spreadshirt.zip"
  excludes    = ["__pycache__", "Makefile", "requirements-dev.txt", "build"]
}

data "archive_file" "source_teepublic" {
  type        = "zip"
  source_dir  = "${path.module}/../../gp-techlab-teepublic/src"
  output_path = "${path.module}/../../gp-techlab-teepublic/src/build/${local.app_name}_teepublic.zip"
  excludes    = ["__pycache__", "Makefile", "requirements-dev.txt", "build"]
}

resource "google_storage_bucket_object" "source_selector" {
  name   = "${local.app_name}-testing-${data.archive_file.source_selector.output_md5}_selector.zip"
  bucket = google_storage_bucket.source.name
  source = data.archive_file.source_selector.output_path
}
resource "google_storage_bucket_object" "source_ali" {
  name   = "${local.app_name}-testing-${data.archive_file.source_ali.output_md5}_ali.zip"
  bucket = google_storage_bucket.source.name
  source = data.archive_file.source_ali.output_path
}

resource "google_storage_bucket_object" "source_amazon" {
  name   = "${local.app_name}-testing-${data.archive_file.source_amazon.output_md5}_amazon.zip"
  bucket = google_storage_bucket.source.name
  source = data.archive_file.source_amazon.output_path
}

resource "google_storage_bucket_object" "source_bing" {
  name   = "${local.app_name}-testing-${data.archive_file.source_bing.output_md5}_bing.zip"
  bucket = google_storage_bucket.source.name
  source = data.archive_file.source_bing.output_path
}

resource "google_storage_bucket_object" "source_cafepress" {
  name   = "${local.app_name}-testing-${data.archive_file.source_cafepress.output_md5}_cafepress.zip"
  bucket = google_storage_bucket.source.name
  source = data.archive_file.source_cafepress.output_path
}

resource "google_storage_bucket_object" "source_duckduckgo" {
  name   = "${local.app_name}-testing-${data.archive_file.source_duckduckgo.output_md5}_duckduckgo.zip"
  bucket = google_storage_bucket.source.name
  source = data.archive_file.source_duckduckgo.output_path
}

resource "google_storage_bucket_object" "source_ebay" {
  name   = "${local.app_name}-testing-${data.archive_file.source_ebay.output_md5}_ebay.zip"
  bucket = google_storage_bucket.source.name
  source = data.archive_file.source_ebay.output_path
}
resource "google_storage_bucket_object" "source_etsy" {
  name   = "${local.app_name}-testing-${data.archive_file.source_etsy.output_md5}_etsy.zip"
  bucket = google_storage_bucket.source.name
  source = data.archive_file.source_etsy.output_path
}

resource "google_storage_bucket_object" "source_googlesearch" {
  name   = "${local.app_name}-testing-${data.archive_file.source_googlesearch.output_md5}_googlesearch.zip"
  bucket = google_storage_bucket.source.name
  source = data.archive_file.source_googlesearch.output_path
}

resource "google_storage_bucket_object" "source_redbubble" {
  name   = "${local.app_name}-testing-${data.archive_file.source_redbubble.output_md5}_redbubble.zip"
  bucket = google_storage_bucket.source.name
  source = data.archive_file.source_redbubble.output_path
}

resource "google_storage_bucket_object" "source_spreadshirt" {
  name   = "${local.app_name}-testing-${data.archive_file.source_spreadshirt.output_md5}_spreadshit.zip"
  bucket = google_storage_bucket.source.name
  source = data.archive_file.source_spreadshirt.output_path
}

resource "google_storage_bucket_object" "source_teepublic" {
  name   = "${local.app_name}-testing-${data.archive_file.source_teepublic.output_md5}_teepublic.zip"
  bucket = google_storage_bucket.source.name
  source = data.archive_file.source_teepublic.output_path
}