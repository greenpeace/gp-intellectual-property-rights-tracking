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

output "source_object_duckduckgo" {
  value = google_storage_bucket_object.source_duckduckgo.name
}

output "source_object_ebay" {
  value = google_storage_bucket_object.source_ebay.name
}

output "source_object_etsy" {
  value = google_storage_bucket_object.source_etsy.name
}

output "source_object_googlesearch" {
  value = google_storage_bucket_object.source_googlesearch.name
}

output "source_object_redbubble" {
  value = google_storage_bucket_object.source_redbubble.name
}

output "source_object_spreadshirt" {
  value = google_storage_bucket_object.source_spreadshirt.name
}

output "source_object_teepublic" {
  value = google_storage_bucket_object.source_teepublic.name
}