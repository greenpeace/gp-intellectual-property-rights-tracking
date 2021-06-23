resource "google_cloud_scheduler_job" "ali" {
  name        = "Search_BOT_ALI_EXPRESS"
  description = "Search BOT ALI EXPRESS"
  schedule    = var.cron_pattern_ali
  region      = var.function_location
  time_zone   = "Europe/Amsterdam"
  attempt_deadline = "320s"

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions_function.ali.https_trigger_url

    oidc_token {
      service_account_email = google_service_account.function.email
    }
  }
}

resource "google_cloud_scheduler_job" "bing" {
  name        = "Search_BOT_BING_EXPRESS"
  description = "Search BOT BING"
  schedule    = var.cron_pattern_bing
  region      = var.function_location
  time_zone   = "Europe/Amsterdam"
  attempt_deadline = "320s"

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions_function.bing.https_trigger_url

    oidc_token {
      service_account_email = google_service_account.function.email
    }
  }
}

resource "google_cloud_scheduler_job" "amazon" {
  name        = "Search_BOT_AMAZON"
  description = "Search BOT AMAZON"
  schedule    = var.cron_pattern_amazon
  region      = var.function_location
  time_zone   = "Europe/Amsterdam"
  attempt_deadline = "320s"

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions_function.amazon.https_trigger_url

    oidc_token {
      service_account_email = google_service_account.function.email
    }
  }
}

resource "google_cloud_scheduler_job" "cafepress" {
  name        = "Search_BOT_CAFEPRESS"
  description = "Search BOT CAFEPRESS"
  schedule    = var.cron_pattern_cafepress
  region      = var.function_location
  time_zone   = "Europe/Amsterdam"
  attempt_deadline = "320s"

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions_function.cafepress.https_trigger_url

    oidc_token {
      service_account_email = google_service_account.function.email
    }
  }
}
