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

resource "google_cloud_scheduler_job" "duckduckgo" {
  name        = "Search_BOT_DUCKDUCKGO"
  description = "Search BOT DUCKDUCKGO"
  schedule    = var.cron_pattern_duckduckgo
  region      = var.function_location
  time_zone   = "Europe/Amsterdam"
  attempt_deadline = "320s"

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions_function.duckduckgo.https_trigger_url

    oidc_token {
      service_account_email = google_service_account.function.email
    }
  }
}

resource "google_cloud_scheduler_job" "ebay" {
  name        = "Search_BOT_EBAY"
  description = "Search BOT EBAY"
  schedule    = var.cron_pattern_ebay
  region      = var.function_location
  time_zone   = "Europe/Amsterdam"
  attempt_deadline = "320s"

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions_function.ebay.https_trigger_url

    oidc_token {
      service_account_email = google_service_account.function.email
    }
  }
}

resource "google_cloud_scheduler_job" "etsy" {
  name        = "Search_BOT_ETSY"
  description = "Search BOT ETSY"
  schedule    = var.cron_pattern_etsy
  region      = var.function_location
  time_zone   = "Europe/Amsterdam"
  attempt_deadline = "320s"

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions_function.etsy.https_trigger_url

    oidc_token {
      service_account_email = google_service_account.function.email
    }
  }
}

resource "google_cloud_scheduler_job" "googlesearch" {
  name        = "Search_BOT_GOOGLESEARCH"
  description = "Search BOT GOOGLESEARCH"
  schedule    = var.cron_pattern_googlesearch
  region      = var.function_location
  time_zone   = "Europe/Amsterdam"
  attempt_deadline = "320s"

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions_function.googlesearch.https_trigger_url

    oidc_token {
      service_account_email = google_service_account.function.email
    }
  }
}

resource "google_cloud_scheduler_job" "redbubble" {
  name        = "Search_BOT_REDBUBBLE"
  description = "Search BOT REDBUBBLE"
  schedule    = var.cron_pattern_redbubble
  region      = var.function_location
  time_zone   = "Europe/Amsterdam"
  attempt_deadline = "320s"

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions_function.redbubble.https_trigger_url

    oidc_token {
      service_account_email = google_service_account.function.email
    }
  }
}

resource "google_cloud_scheduler_job" "spreadshirt" {
  name        = "Search_BOT_SPREADSHIRT"
  description = "Search BOT SPREADSHIRT"
  schedule    = var.cron_pattern_spreadshirt
  region      = var.function_location
  time_zone   = "Europe/Amsterdam"
  attempt_deadline = "320s"

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions_function.spreadshirt.https_trigger_url

    oidc_token {
      service_account_email = google_service_account.function.email
    }
  }
}

resource "google_cloud_scheduler_job" "teepublic" {
  name        = "Search_BOT_TEEPUBLIC"
  description = "Search BOT TEEPUBLIC"
  schedule    = var.cron_pattern_teepublic
  region      = var.function_location
  time_zone   = "Europe/Amsterdam"
  attempt_deadline = "320s"

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions_function.teepublic.https_trigger_url

    oidc_token {
      service_account_email = google_service_account.function.email
    }
  }
}
