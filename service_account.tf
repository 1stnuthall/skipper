resource "google_service_account_key" "osm_key" {
  service_account_id = google_service_account.osm_bot.name
  keepers = {
    request_time = timestamp()
  }
}

output "private_key_json" {
  value     = google_service_account_key.osm_key.private_key
  sensitive = true
}
