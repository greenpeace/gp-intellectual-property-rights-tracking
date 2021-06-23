resource "google_cloudfunctions_function" "ali" {
  name                = "${local.app_name}_${var.entity}_${var.environment}_ali"
  project             = var.project
  region              = var.function_location
  entry_point         = "main"
  runtime             = "python37"
  available_memory_mb = var.function_memory
  timeout             = var.function_timeout

  service_account_email = google_service_account.function.email

  source_archive_bucket = var.source_archive_bucket
  source_archive_object = var.source_archive_object_ali

  trigger_http          = true

  environment_variables = {
    ENTITY      = var.entity
    ENVIRONMENT = var.environment
    PROJECT     = var.project
  }
}

resource "google_cloudfunctions_function" "amazon" {
  name                = "${local.app_name}_${var.entity}_${var.environment}_amazon"
  project             = var.project
  region              = var.function_location
  entry_point         = "main"
  runtime             = "python37"
  available_memory_mb = var.function_memory
  timeout             = var.function_timeout

  service_account_email = google_service_account.function.email

  source_archive_bucket = var.source_archive_bucket
  source_archive_object = var.source_archive_object_amazon

  trigger_http          = true

  environment_variables = {
    ENTITY      = var.entity
    ENVIRONMENT = var.environment
    PROJECT     = var.project
  }
}

resource "google_cloudfunctions_function" "cafepress" {
  name                = "${local.app_name}_${var.entity}_${var.environment}_cafepress"
  project             = var.project
  region              = var.function_location
  entry_point         = "main"
  runtime             = "python37"
  available_memory_mb = var.function_memory
  timeout             = var.function_timeout

  service_account_email = google_service_account.function.email

  source_archive_bucket = var.source_archive_bucket
  source_archive_object = var.source_archive_object_cafepress

  trigger_http          = true

  environment_variables = {
    ENTITY      = var.entity
    ENVIRONMENT = var.environment
    PROJECT     = var.project
  }
}

resource "google_cloudfunctions_function" "bing" {
  name                = "${local.app_name}_${var.entity}_${var.environment}_bing"
  project             = var.project
  region              = var.function_location
  entry_point         = "main"
  runtime             = "python37"
  available_memory_mb = var.function_memory
  timeout             = var.function_timeout

  service_account_email = google_service_account.function.email

  source_archive_bucket = var.source_archive_bucket
  source_archive_object = var.source_archive_object_bing

  trigger_http          = true

  environment_variables = {
    ENTITY      = var.entity
    ENVIRONMENT = var.environment
    PROJECT     = var.project
  }
}

resource "google_service_account" "function" {
  account_id   = "${local.app_name}-${var.entity}-${var.environment}"
  display_name = "IPR Function Account"
  project      = var.project
}

resource "google_project_iam_member" "function_trace" {
  project = var.project
  role    = "roles/cloudtrace.agent"
  member  = "serviceAccount:${google_service_account.function.email}"
}

resource "google_project_iam_member" "cloud_build" {
  project = var.project
  role    = "roles/cloudbuild.builds.builder"
  member  = "serviceAccount:${google_service_account.function.email}"
}

resource "google_project_iam_member" "secret_manager" {
  project = var.project
  role    = "roles/secretmanager.admin"
  member  = "serviceAccount:${google_service_account.function.email}"
}

resource "google_project_iam_member" "cloud_function_invoker" {
  project = var.project
  role    = "roles/cloudfunctions.invoker"
  member  = "serviceAccount:${google_service_account.function.email}"
}
