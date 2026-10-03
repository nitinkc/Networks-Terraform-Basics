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

variable "my_ip" {
  description = "Your public IP in CIDR form, for SSH access (e.g. 203.0.113.7/32)"
  type        = string
}

# --- Cloud NAT: the cloud version of "ip nat inside source list ... overload" ---

resource "google_compute_router" "nat_router" {
  name    = "tf-lab-nat-router"
  network = google_compute_network.lab_vpc.id
  region  = var.region
}

resource "google_compute_router_nat" "nat" {
  name   = "tf-lab-nat"
  router = google_compute_router.nat_router.name
  region = var.region

  nat_ip_allocate_option = "AUTO_ONLY"   # PAT behavior: shared ephemeral IPs

  source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"

  subnetwork {
    name                    = google_compute_subnetwork.lan2_servers.id
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }
}

# --- Firewall rules: the cloud version of ACLs ---

# Allow SSH to instances tagged "ssh-allowed", only from your IP
resource "google_compute_firewall" "allow_ssh" {
  name    = "tf-allow-ssh"
  network = google_compute_network.lab_vpc.id

  direction     = "INGRESS"
  source_ranges = [var.my_ip]

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  target_tags = ["ssh-allowed"]
}

# Allow all traffic between our two subnets (like inter-VLAN routing permitting LANs)
resource "google_compute_firewall" "allow_iap_ssh" {
  name    = "tf-allow-iap-ssh"
  network = google_compute_network.lab_vpc.id

  direction     = "INGRESS"
  source_ranges = ["35.235.240.0/20"]

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  target_tags = ["iap-ssh"]
}

resource "google_compute_firewall" "allow_internal" {
  name    = "tf-allow-internal"
  network = google_compute_network.lab_vpc.id

  direction     = "INGRESS"
  source_ranges = ["192.168.10.0/24", "192.168.20.0/24"]

  allow {
    protocol = "tcp"
  }

  allow {
    protocol = "udp"
  }

  allow {
    protocol = "icmp"
  }
}