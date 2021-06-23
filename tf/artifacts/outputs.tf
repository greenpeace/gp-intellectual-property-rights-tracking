output "source_bucket" {
  value = google_storage_bucket.source.name
}
output "source_object_ali" {
  value = google_storage_bucket_object.source_ali.name
}

output "source_object_amazon" {
  value = google_storage_bucket_object.source_amazon.name
}

output "source_object_bing" {
  value = google_storage_bucket_object.source_bing.name
}

output "source_object_cafepress" {
  value = google_storage_bucket_object.source_cafepress.name
}