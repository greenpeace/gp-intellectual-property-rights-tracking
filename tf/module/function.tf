resource "google_cloudfunctions_function" "selector" {
  name                = "${local.app_name}_${var.entity}_${var.environment}_selector"
  project             = var.project
  region              = var.function_location
  entry_point         = "main"
  runtime             = "python37"
  available_memory_mb = var.function_memory
  timeout             = var.function_timeout

  service_account_email = google_service_account.function.email

  source_archive_bucket = var.source_archive_bucket
  source_archive_object = var.source_archive_object_selector
  
  event_trigger {
    event_type  = "google.pubsub.topic.publish"
    resource    = "projects/${var.project}/topics/items-added"
    failure_policy {
      retry = true
    }
  }

  environment_variables = {
    ENTITY      = var.entity
    ENVIRONMENT = var.environment
    PROJECT     = var.project
  }
}
resource "google_cloudfunctions_function" "ali" {
  name                = "${local.app_name}_${var.entity}_${var.environment}_ali"
  project             = var.project
  region              = var.function_location
  entry_point         = "main"
  runtime             = "nodejs12"
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

resource "google_cloudfunctions_function" "duckduckgo" {
  name                = "${local.app_name}_${var.entity}_${var.environment}_duckduckgo"
  project             = var.project
  region              = var.function_location
  entry_point         = "main"
  runtime             = "python37"
  available_memory_mb = var.function_memory
  timeout             = var.function_timeout

  service_account_email = google_service_account.function.email

  source_archive_bucket = var.source_archive_bucket
  source_archive_object = var.source_archive_object_duckduckgo

  trigger_http          = true

  environment_variables = {
    ENTITY      = var.entity
    ENVIRONMENT = var.environment
    PROJECT     = var.project
  }
}

resource "google_cloudfunctions_function" "ebay" {
  name                = "${local.app_name}_${var.entity}_${var.environment}_ebay"
  project             = var.project
  region              = var.function_location
  entry_point         = "main"
  runtime             = "python37"
  available_memory_mb = var.function_memory
  timeout             = var.function_timeout

  service_account_email = google_service_account.function.email

  source_archive_bucket = var.source_archive_bucket
  source_archive_object = var.source_archive_object_ebay

  trigger_http          = true

  environment_variables = {
    ENTITY      = var.entity
    ENVIRONMENT = var.environment
    PROJECT     = var.project
  }
}
resource "google_cloudfunctions_function" "etsy" {
  name                = "${local.app_name}_${var.entity}_${var.environment}_etsy"
  project             = var.project
  region              = var.function_location
  entry_point         = "main"
  runtime             = "python37"
  available_memory_mb = var.function_memory
  timeout             = var.function_timeout

  service_account_email = google_service_account.function.email

  source_archive_bucket = var.source_archive_bucket
  source_archive_object = var.source_archive_object_etsy

  trigger_http          = true

  environment_variables = {
    ENTITY      = var.entity
    ENVIRONMENT = var.environment
    PROJECT     = var.project
  }
}
resource "google_cloudfunctions_function" "googlesearch" {
  name                = "${local.app_name}_${var.entity}_${var.environment}_googlesearch"
  project             = var.project
  region              = var.function_location
  entry_point         = "main"
  runtime             = "python37"
  available_memory_mb = var.function_memory
  timeout             = var.function_timeout

  service_account_email = google_service_account.function.email

  source_archive_bucket = var.source_archive_bucket
  source_archive_object = var.source_archive_object_googlesearch

  trigger_http          = true

  environment_variables = {
    ENTITY      = var.entity
    ENVIRONMENT = var.environment
    PROJECT     = var.project
  }
}
resource "google_cloudfunctions_function" "redbubble" {
  name                = "${local.app_name}_${var.entity}_${var.environment}_redbubble"
  project             = var.project
  region              = var.function_location
  entry_point         = "main"
  runtime             = "python37"
  available_memory_mb = var.function_memory
  timeout             = var.function_timeout

  service_account_email = google_service_account.function.email

  source_archive_bucket = var.source_archive_bucket
  source_archive_object = var.source_archive_object_redbubble

  trigger_http          = true

  environment_variables = {
    ENTITY      = var.entity
    ENVIRONMENT = var.environment
    PROJECT     = var.project
  }
}
resource "google_cloudfunctions_function" "spreadshirt" {
  name                = "${local.app_name}_${var.entity}_${var.environment}_spreadshirt"
  project             = var.project
  region              = var.function_location
  entry_point         = "main"
  runtime             = "python37"
  available_memory_mb = var.function_memory
  timeout             = var.function_timeout

  service_account_email = google_service_account.function.email

  source_archive_bucket = var.source_archive_bucket
  source_archive_object = var.source_archive_object_spreadshirt

  trigger_http          = true

  environment_variables = {
    ENTITY      = var.entity
    ENVIRONMENT = var.environment
    PROJECT     = var.project
  }
}
resource "google_cloudfunctions_function" "teepublic" {
  name                = "${local.app_name}_${var.entity}_${var.environment}_teepublic"
  project             = var.project
  region              = var.function_location
  entry_point         = "main"
  runtime             = "python37"
  available_memory_mb = var.function_memory
  timeout             = var.function_timeout

  service_account_email = google_service_account.function.email

  source_archive_bucket = var.source_archive_bucket
  source_archive_object = var.source_archive_object_teepublic

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

resource "google_project_iam_member" "cloud_function_invoker" {
  project = var.project
  role    = "roles/cloudfunctions.invoker"
  member  = "serviceAccount:${google_service_account.function.email}"
}

resource "google_project_iam_member" "cloud_function_admin" {
  project = var.project
  role    = "roles/cloudfunctions.admin"
  member  = "serviceAccount:${google_service_account.function.email}"
}

resource "google_project_iam_member" "pubsub" {
  project = var.project
  role    = "roles/pubsub.editor"
  member  = "serviceAccount:${google_service_account.function.email}"
}

resource "google_project_iam_member" "firebase_admin" {
  project = var.project
  role    = "roles/firebase.admin"
  member  = "serviceAccount:${google_service_account.function.email}"
}

resource "google_pubsub_topic" "items_added" {
  name = "items-added"

  labels = {
    data = "test"
  }
}
