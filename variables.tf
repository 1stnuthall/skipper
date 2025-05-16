variable "project_id" {
  type        = string
  description = "Your GCP project ID"
}

variable "region" {
  type        = string
  description = "Region for services"
  default     = "us-central1"
}

variable "credentials_file" {
  type        = string
  description = "Path to the GCP service account JSON key file"
}
