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
  description = "GCP region for the two-tier stack"
  type        = string
  default     = "us-central1"
}

# -----------------------------------------------------------------------------
# 1. VPC NETWORK & SUBNETS
# -----------------------------------------------------------------------------

# Always use auto_create_subnetworks = false (Custom Mode) in production!
resource "google_compute_network" "vpc_network" {
  name                    = "custom-prod-vpc"
  auto_create_subnetworks = false
  description             = "Custom Enterprise Production VPC"
}

# Web Tier Subnet (Public Ingress)
resource "google_compute_subnetwork" "web_subnet" {
  name          = "web-tier-subnet"
  ip_cidr_range = "10.1.10.0/24"
  region        = var.region
  network       = google_compute_network.vpc_network.id
}

# Backend App Tier Subnet (Private Isolated)
resource "google_compute_subnetwork" "app_subnet" {
  name                     = "app-tier-subnet"
  ip_cidr_range            = "10.1.20.0/24"
  region                   = var.region
  network                  = google_compute_network.vpc_network.id
  private_ip_google_access = true
}

# -----------------------------------------------------------------------------
# 2. CLOUD ROUTER & CLOUD NAT (The Cloud Equivalent of PAT Overload)
# -----------------------------------------------------------------------------

resource "google_compute_router" "nat_router" {
  name    = "prod-nat-router"
  region  = google_compute_subnetwork.app_subnet.region
  network = google_compute_network.vpc_network.id
}

resource "google_compute_router_nat" "app_nat" {
  name                               = "prod-cloud-nat"
  router                             = google_compute_router.nat_router.name
  region                             = google_compute_router.nat_router.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"

  subnetwork {
    name                    = google_compute_subnetwork.app_subnet.id
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }
}

# -----------------------------------------------------------------------------
# 3. FIREWALL RULES (Stateful Traffic Filters)
# -----------------------------------------------------------------------------

resource "google_compute_firewall" "allow_web_http" {
  name    = "allow-web-http"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["web-tier"]
}

resource "google_compute_firewall" "allow_iap_ssh" {
  name    = "allow-iap-ssh"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["35.235.240.0/20"]
  target_tags   = ["web-tier"]
}

# Allow Web Tier to reach Backend App Tier on Port 8080 (Internal East-West)
resource "google_compute_firewall" "allow_web_to_app" {
  name    = "allow-web-to-app-internal"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["8080"]
  }

  allow {
    protocol = "icmp"
  }

  source_tags = ["web-tier"]
  target_tags = ["app-tier"]
}

# -----------------------------------------------------------------------------
# 4. PRIVATE CLOUD DNS (Internal Name Resolution)
# -----------------------------------------------------------------------------

resource "google_dns_managed_zone" "private_zone" {
  name        = "corp-internal-zone"
  dns_name    = "corp.internal."
  description = "Private internal DNS zone for VPC instances"
  visibility  = "private"

  private_visibility_config {
    networks {
      network_url = google_compute_network.vpc_network.id
    }
  }
}

# A-Record mapping api.corp.internal to Backend VM's Private IP
resource "google_dns_record_set" "backend_dns_record" {
  name         = "api.corp.internal."
  managed_zone = google_dns_managed_zone.private_zone.name
  type         = "A"
  ttl          = 300
  rrdatas      = [google_compute_instance.backend_vm.network_interface[0].network_ip]
}

# -----------------------------------------------------------------------------
# 5. COMPUTE ENGINE VIRTUAL MACHINES
# -----------------------------------------------------------------------------

# Frontend Web Server (Has Public IP)
resource "google_compute_instance" "frontend_vm" {
  name         = "frontend-web-vm"
  machine_type = "e2-micro"
  zone         = "${var.region}-a"
  tags         = ["web-tier"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.web_subnet.id
    access_config {
      # Presence of access_config assigns a Public IP
    }
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y nginx
    echo "<h1>Welcome to Frontend Web Tier</h1>" > /var/www/html/index.html
  EOF
}

# Backend App Server (Private IP ONLY - No access_config block!)
resource "google_compute_instance" "backend_vm" {
  name         = "backend-app-vm"
  machine_type = "e2-micro"
  zone         = "${var.region}-a"
  tags         = ["app-tier"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.app_subnet.id
    # No access_config block means NO Public IP (Fully Private)
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y python3
    install -d /opt/backend-api
    echo "Backend API Service Response" > /opt/backend-api/index.html
    cat > /etc/systemd/system/backend-api.service <<'UNIT'
    [Unit]
    Description=Lab 05 backend API
    After=network-online.target

    [Service]
    ExecStart=/usr/bin/python3 -m http.server 8080 --directory /opt/backend-api
    Restart=always

    [Install]
    WantedBy=multi-user.target
    UNIT
    systemctl daemon-reload
    systemctl enable --now backend-api
  EOF
}

output "frontend_vm_name" {
  value = google_compute_instance.frontend_vm.name
}

output "backend_vm_name" {
  value = google_compute_instance.backend_vm.name
}

output "vm_zone" {
  value = google_compute_instance.frontend_vm.zone
}