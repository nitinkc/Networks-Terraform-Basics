terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  description = "GCP project ID to deploy into"
  type        = string
}

variable "region" {
  description = "GCP region for both subnets"
  type        = string
  default     = "us-central1"
}

# 1. The network boundary (like the Packet Tracer workspace)
resource "google_compute_network" "lab_vpc" {
  name                    = "tf-lab-vpc"
  auto_create_subnetworks = false
}

# 2. LAN 1 — the client network (was behind Router0/Gig0/0)
resource "google_compute_subnetwork" "lan1_clients" {
  name          = "lan1-clients"
  ip_cidr_range = "192.168.10.0/24"
  region        = var.region
  network       = google_compute_network.lab_vpc.id
}

# 3. LAN 2 — the server farm (was behind Router0/Gig0/1)
resource "google_compute_subnetwork" "lan2_servers" {
  name          = "lan2-servers"
  ip_cidr_range = "192.168.20.0/24"
  region        = var.region
  network       = google_compute_network.lab_vpc.id
}