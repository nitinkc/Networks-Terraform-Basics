# Lab: Layer 4 vs. Layer 7 Cloud Load Balancing & High Availability

Load Balancers act as intelligent traffic dispatchers. This lab covers the difference between **Layer 4 (Transport / TCP/UDP)** and **Layer 7 (Application / HTTP/HTTPS)** Load Balancing.

```
                                  [ INTERNET USERS ]
                                          │
                                          ▼ (Global Anycast IP)
                           [ GCP Cloud HTTP(S) Load Balancer ]
                           (Layer 7 URL Map: host & path rules)
                                   /                                Path: /api/*   /               \   Path: /static/*
                                 ▼                 ▼
                     [ Backend Service: API ]   [ Backend Service: Web ]
                     (Managed Instance Group)   (Managed Instance Group)
                     ┌──────────────────────┐   ┌──────────────────────┐
                     │ VM-API-1 (10.1.20.2) │   │ VM-Web-1 (10.1.10.2) │
                     │ VM-API-2 (10.1.20.3) │   │ VM-Web-2 (10.1.10.3) │
                     └──────────────────────┘   └──────────────────────┘
```

## Comparison Matrix: Layer 4 vs. Layer 7

| Feature | Layer 4 (Network Load Balancer) | Layer 7 (Application Load Balancer) |
|---|---|---|
| **OSI Layer** | Layer 4 (TCP / UDP) | Layer 7 (HTTP / HTTPS / gRPC) |
| **Inspection Capability**| IP addresses and Port numbers only | URLs, HTTP headers, Cookies, Query parameters |
| **Routing Capability** | Distributes to a single backend pool | Content-based routing (`/api` $ightarrow$ API pool, `/images` $ightarrow$ Storage) |
| **SSL/TLS Termination** | Pass-through (Client connects directly to VM) | Offloads TLS certificates at the edge; talks HTTP internally |
| **Performance** | Extreme throughput, lowest latency | Rich traffic management, URL rewrites, and security |

## Complete Terraform Configuration: L7 Cloud HTTP Load Balancer

```hcl
# 1. Health Check (Probes backend VMs on port 80)
resource "google_compute_health_check" "http_health" {
  name               = "app-http-health-check"
  check_interval_sec = 5
  timeout_sec        = 3
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
}

resource "google_compute_backend_service" "api_backend" {
  name                  = "api-backend-service"
  protocol              = "HTTP"
  port_name             = "http-api"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  health_checks         = [google_compute_health_check.http_health.id]
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
```

## Hands-On Verification

```bash
# 1. Fetch the Global Virtual IP assigned to the Load Balancer
VIP=$(terraform output -raw load_balancer_ip)

# 2. Test Default Route (Web Tier)
curl http://$VIP/
# Returns response from web_backend pool

# 3. Test Layer 7 Path-Based Route (/api)
curl http://$VIP/api/users
# Layer 7 URL Map automatically routes request to api_backend pool!
```
