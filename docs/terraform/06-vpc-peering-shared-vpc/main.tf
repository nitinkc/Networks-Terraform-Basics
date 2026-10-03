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
  description = "GCP region for both VPC subnets"
  type        = string
  default     = "us-central1"
}

# -----------------------------------------------------------------------------
# 1. CREATE HUB VPC (Shared Services)
# -----------------------------------------------------------------------------
resource "google_compute_network" "hub_vpc" {
  name                    = "hub-services-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "hub_subnet" {
  name          = "hub-core-subnet"
  ip_cidr_range = "10.0.0.0/16"
  region        = var.region
  network       = google_compute_network.hub_vpc.id
}

# -----------------------------------------------------------------------------
# 2. CREATE PRODUCTION SPOKE VPC
# -----------------------------------------------------------------------------
resource "google_compute_network" "prod_spoke_vpc" {
  name                    = "prod-workload-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "prod_subnet" {
  name          = "prod-workload-subnet"
  ip_cidr_range = "10.10.0.0/16"
  region        = var.region
  network       = google_compute_network.prod_spoke_vpc.id
}

# -----------------------------------------------------------------------------
# 3. BI-DIRECTIONAL VPC PEERING (Both directions required!)
# -----------------------------------------------------------------------------

# Peering: Hub -> Production
resource "google_compute_network_peering" "hub_to_prod" {
  name                 = "peering-hub-to-prod"
  network              = google_compute_network.hub_vpc.self_link
  peer_network         = google_compute_network.prod_spoke_vpc.self_link
  export_custom_routes = true
  import_custom_routes = true
}

# Peering: Production -> Hub
resource "google_compute_network_peering" "prod_to_hub" {
  name                 = "peering-prod-to-hub"
  network              = google_compute_network.prod_spoke_vpc.self_link
  peer_network         = google_compute_network.hub_vpc.self_link
  export_custom_routes = true
  import_custom_routes = true
}

# -----------------------------------------------------------------------------
# 4. CROSS-VPC FIREWALL RULES
# -----------------------------------------------------------------------------

# Allow Hub Services to communicate with Production VMs on SSH and HTTP
resource "google_compute_firewall" "allow_hub_to_prod" {
  name    = "allow-hub-to-prod"
  network = google_compute_network.prod_spoke_vpc.name

  allow {
    protocol = "tcp"
    ports    = ["22", "80", "443"]
  }

  allow {
    protocol = "icmp"
  }

  source_ranges = ["10.0.0.0/16"]
}