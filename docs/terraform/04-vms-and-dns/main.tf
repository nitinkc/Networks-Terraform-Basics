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

variable "ssh_user" {
  description = "Linux user to create for SSH access"
  type        = string
  default     = "labuser"
}

variable "ssh_public_key" {
  description = "OpenSSH public key used to access both VMs; omit for destroy"
  type        = string
  default     = ""

  validation {
    condition     = trimspace(var.ssh_public_key) == "" || can(regex("^(ssh-(rsa|ed25519)|ecdsa-sha2-nistp(256|384|521)) ", trimspace(var.ssh_public_key)))
    error_message = "ssh_public_key must be empty or a valid OpenSSH public key."
  }
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

  nat_ip_allocate_option = "AUTO_ONLY" # PAT behavior: shared ephemeral IPs

  source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"

  subnetwork {
    name                    = google_compute_subnetwork.lan2_servers.id
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }
}

# --- Firewall rules: the cloud version of ACLs ---

# Allow SSH through Identity-Aware Proxy to explicitly tagged instances
resource "google_compute_firewall" "allow_iap_ssh" {
  name    = "tf-allow-iap-ssh"
  network = google_compute_network.lab_vpc.id

  direction     = "INGRESS"
  source_ranges = ["35.235.240.0/20"]

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  target_tags = ["ssh-allowed", "iap-ssh"]
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

# --- Frontend VM: plays the "PC0" role, reachable via SSH ---
resource "google_compute_instance" "frontend_vm" {
  name         = "frontend-vm"
  machine_type = "e2-micro" # free-tier eligible
  zone         = "${var.region}-a"

  tags = ["ssh-allowed"] # picks up the lab-03 SSH firewall rule

  metadata = trimspace(var.ssh_public_key) == "" ? {} : {
    block-project-ssh-keys = "TRUE"
    enable-oslogin         = "FALSE"
    ssh-keys               = "${var.ssh_user}:${trimspace(var.ssh_public_key)}"
  }

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.lan1_clients.id
    access_config {} # empty block = ephemeral public IP
  }
}

# --- Backend VM: plays the "DHCP-Server0" role, private only ---
resource "google_compute_instance" "backend_vm" {
  name         = "backend-vm"
  machine_type = "e2-micro"
  zone         = "${var.region}-a"

  tags = ["iap-ssh"]

  metadata = trimspace(var.ssh_public_key) == "" ? {} : {
    block-project-ssh-keys = "TRUE"
    enable-oslogin         = "FALSE"
    ssh-keys               = "${var.ssh_user}:${trimspace(var.ssh_public_key)}"
  }

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.lan2_servers.id
    # no access_config → NO public IP; outbound goes through Cloud NAT
  }

  metadata_startup_script = "apt-get update && apt-get install -y nginx"
}

# --- Private DNS: replaces the lab-5 DNS server ---
resource "google_dns_managed_zone" "corp_internal" {
  name        = "corp-internal"
  dns_name    = "corp.internal."
  description = "Private zone for internal service names"

  visibility = "private"

  private_visibility_config {
    networks {
      network_url = google_compute_network.lab_vpc.id
    }
  }
}

resource "google_dns_record_set" "backend_a" {
  name         = "backend.${google_dns_managed_zone.corp_internal.dns_name}"
  type         = "A"
  ttl          = 300
  managed_zone = google_dns_managed_zone.corp_internal.name

  rrdatas = [google_compute_instance.backend_vm.network_interface[0].network_ip]
}