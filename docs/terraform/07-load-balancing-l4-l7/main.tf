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
  description = "GCP region for the load-balancer backends"
  type        = string
  default     = "us-central1"
}

resource "google_compute_network" "lb_vpc" {
  name                    = "lb-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "lb_subnet" {
  name          = "lb-backend-subnet"
  ip_cidr_range = "10.20.0.0/24"
  region        = var.region
  network       = google_compute_network.lb_vpc.id
}

resource "google_compute_firewall" "allow_health_checks" {
  name    = "allow-lb-health-checks"
  network = google_compute_network.lb_vpc.id

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  source_ranges = ["35.191.0.0/16", "130.211.0.0/22"]
  target_tags   = ["lb-backend"]
}

resource "google_compute_instance_template" "web" {
  name_prefix  = "web-template-"
  machine_type = "e2-micro"
  tags         = ["lb-backend"]

  disk {
    source_image = "debian-cloud/debian-12"
    auto_delete  = true
    boot         = true
  }

  network_interface {
    subnetwork = google_compute_subnetwork.lb_subnet.id
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    install -d /opt/web
    echo "Web backend response" > /opt/web/index.html
    echo "healthy" > /opt/web/health
    python3 -m http.server 80 --directory /opt/web >/var/log/web-backend.log 2>&1 &
  EOF

  lifecycle {
    create_before_destroy = true
  }
}

resource "google_compute_instance_template" "api" {
  name_prefix  = "api-template-"
  machine_type = "e2-micro"
  tags         = ["lb-backend"]

  disk {
    source_image = "debian-cloud/debian-12"
    auto_delete  = true
    boot         = true
  }

  network_interface {
    subnetwork = google_compute_subnetwork.lb_subnet.id
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    install -d /opt/api/api
    echo "API backend response" > /opt/api/api/users
    echo "healthy" > /opt/api/health
    python3 -m http.server 80 --directory /opt/api >/var/log/api-backend.log 2>&1 &
  EOF

  lifecycle {
    create_before_destroy = true
  }
}

resource "google_compute_instance_group_manager" "web" {
  name               = "web-mig"
  base_instance_name = "web"
  zone               = "${var.region}-a"
  target_size        = 1

  version {
    instance_template = google_compute_instance_template.web.id
  }

  named_port {
    name = "http"
    port = 80
  }
}

resource "google_compute_instance_group_manager" "api" {
  name               = "api-mig"
  base_instance_name = "api"
  zone               = "${var.region}-a"
  target_size        = 1

  version {
    instance_template = google_compute_instance_template.api.id
  }

  named_port {
    name = "http-api"
    port = 80
  }
}

# 1. Health Check (Probes backend VMs on port 80)
resource "google_compute_health_check" "http_health" {
  name                = "app-http-health-check"
  check_interval_sec  = 5
  timeout_sec         = 3
  healthy_threshold   = 2
  unhealthy_threshold = 3

  http_health_check {
    port         = 80
    request_path = "/health"
  }
}

# 2. Backend Services (Groups of VMs serving specific traffic)
resource "google_compute_backend_service" "web_backend" {
  name                  = "web-backend-service"
  protocol              = "HTTP"
  port_name             = "http"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  health_checks         = [google_compute_health_check.http_health.id]

  backend {
    group = google_compute_instance_group_manager.web.instance_group
  }
}

resource "google_compute_backend_service" "api_backend" {
  name                  = "api-backend-service"
  protocol              = "HTTP"
  port_name             = "http-api"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  health_checks         = [google_compute_health_check.http_health.id]

  backend {
    group = google_compute_instance_group_manager.api.instance_group
  }
}

# 3. URL Map (The Layer 7 Routing Brain)
resource "google_compute_url_map" "l7_url_map" {
  name            = "prod-global-url-map"
  default_service = google_compute_backend_service.web_backend.id

  host_rule {
    hosts        = ["*"]
    path_matcher = "allpaths"
  }

  path_matcher {
    name            = "allpaths"
    default_service = google_compute_backend_service.web_backend.id

    # Content-based routing: /api/* routes to dedicated API instances
    path_rule {
      paths   = ["/api", "/api/*"]
      service = google_compute_backend_service.api_backend.id
    }
  }
}

# 4. Target HTTP Proxy
resource "google_compute_target_http_proxy" "http_proxy" {
  name    = "prod-http-proxy"
  url_map = google_compute_url_map.l7_url_map.id
}

# 5. Global Forwarding Rule (Public Entry Point with Anycast VIP)
resource "google_compute_global_forwarding_rule" "forwarding_rule" {
  name                  = "http-global-entry"
  target                = google_compute_target_http_proxy.http_proxy.id
  port_range            = "80"
  load_balancing_scheme = "EXTERNAL_MANAGED"
}

output "load_balancer_ip" {
  description = "Global frontend IP assigned to the HTTP load balancer"
  value       = google_compute_global_forwarding_rule.forwarding_rule.ip_address
}