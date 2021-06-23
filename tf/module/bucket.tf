resource "google_storage_bucket" "sink" {
  name     = "${local.app_name}-${var.entity}-${var.environment}"
  location = "EU"
  project  = var.project

  # For uniform bucket ACL
  uniform_bucket_level_access = true

  // Enable object versioning
  versioning {
    enabled = true
  }

  // Set archived files to NEARLINE
  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
    condition {
      num_newer_versions = 1
      with_state         = "ARCHIVED"
    }
  }

  // Set files older than 7 days to COLDLINE
  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
    condition {
      num_newer_versions = 7
      with_state         = "ARCHIVED"
    }
  }

  // Delete files older than 365 days
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age                = 365
      num_newer_versions = 1
      with_state         = "ARCHIVED"
    }
  }

  labels = {
    app         = local.app_name
    component   = "data"
    environment = var.environment
    entity      = var.entity
  }
}

resource "google_storage_bucket_iam_member" "legacyBucketWriter" {
  bucket = google_storage_bucket.sink.name
  role   = "roles/storage.legacyBucketWriter"
  member = "serviceAccount:${google_service_account.function.email}"
}
