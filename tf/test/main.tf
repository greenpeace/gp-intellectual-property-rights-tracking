locals {
  project     = "torbjorn-zetterlund"
  entity      = "extract"
  environment = "dev"
}

provider "google" {
  alias = "initial"
}

data "google_client_config" "config-default" {
  provider = google.initial
}

#data "google_service_account_access_token" "default" {
#  provider               = google.initial
#  target_service_account = "terraform@${local.project}.iam.gserviceaccount.com"
#  scopes                 = ["cloud-platform"]
#  lifetime               = "300s"
#}

provider "google" {
  project      = local.project
  region       = "EU"
  #access_token = data.google_service_account_access_token.default.access_token
}

module "artifacts" {
  source  = "../artifacts/"
  project = local.project
}

module "example" {
  source = "../module/"

  entity      = local.entity
  environment = local.environment
  project     = local.project

  source_archive_bucket = module.artifacts.source_bucket
  source_archive_object_ali = module.artifacts.source_object_ali
  source_archive_object_amazon = module.artifacts.source_object_amazon
  source_archive_object_bing = module.artifacts.source_object_bing
  source_archive_object_cafepress = module.artifacts.source_object_cafepress
  source_archive_object_duckduckgo = module.artifacts.source_object_duckduckgo
  source_archive_object_ebay = module.artifacts.source_object_ebay
  source_archive_object_etsy = module.artifacts.source_object_etsy
  source_archive_object_googlesearch = module.artifacts.source_object_googlesearch
  source_archive_object_redbubble = module.artifacts.source_object_redbubble
  source_archive_object_spreadshirt = module.artifacts.source_object_spreadshirt
  source_archive_object_teepublic = module.artifacts.source_object_teepublic
}

resource "google_project_service" "enable-project-serviceusage-api-host" {
  project            = local.project
  service            = "serviceusage.googleapis.com"
  disable_on_destroy = false
}

output "bucket_name" {
  value = module.example.bucket_name
}
