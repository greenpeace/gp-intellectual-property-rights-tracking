output "service_account_email" {
  value = google_service_account.function.email
}

output "bucket_name" {
  value = google_storage_bucket.sink.name
}
