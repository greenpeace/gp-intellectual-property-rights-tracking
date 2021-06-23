locals {
  app_name = "gpi-ipr"
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

data "archive_file" "source_ali" {
  type        = "zip"
  source_dir  = "${path.module}/../../gp-techlab-alisearchbot/src"
  output_path = "${path.module}/../../gp-techlab-alisearchbot/src/build/${local.app_name}_ali.zip"
  excludes    = ["__pycache__", "Makefile", "requirements-dev.txt", "build"]
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