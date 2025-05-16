provider "google" {
  project = var.project_id
  region  = var.region
  credentials = file(var.credentials_file)
}

resource "google_project_service" "secretmanager" {
  service = "secretmanager.googleapis.com"
}

resource "google_service_account" "osm_bot" {
  account_id   = "osm-slack-bot"
  display_name = "Slack Bot for OSM"
}

resource "google_project_iam_member" "secretmanager_access" {
  role   = "roles/secretmanager.admin"
  member = "serviceAccount:${google_service_account.osm_bot.email}"
}

output "service_account_email" {
  value = google_service_account.osm_bot.email
}
