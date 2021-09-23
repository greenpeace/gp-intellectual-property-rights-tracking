# This directory describes the release bucket

locals {
  app_name = "gpiipr"
  project  = "torbjorn-zetterlund"
}

provider "google" {
  project = local.project
  region  = "US"
  version = "~> 3.40"
}


resource "google_storage_bucket" "source" {
  name     = "${local.app_name}-source"
  location = "EU"
  project  = local.project

  labels = {
    app       = local.app_name
    component = "source"
  }

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }

    condition {
      num_newer_versions = 7
    }
  }
}

resource "google_storage_bucket_iam_member" "all_authenticated_users" {
  bucket = google_storage_bucket.source.name
  role   = "roles/storage.objectViewer"
  member = "allAuthenticatedUsers"
}
