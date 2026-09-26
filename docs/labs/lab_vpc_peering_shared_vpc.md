# Lab: VPC Network Peering & Shared VPC (Multi-Project Cloud Networks)

In production cloud environments, single monolithic VPCs are rarely used. Instead, organizations deploy **Multi-VPC Hub-and-Spoke** topologies or **Shared VPCs** to segregate environments (Production vs. Staging vs. Shared Services).

```
   ┌────────────────────────────────────────────────────────┐
   │            [ Hub / Shared Services VPC ]               │
   │               CIDR: 10.0.0.0/16                        │
   │           (DNS, Security Scanners, CI/CD)              │
   └───────────────▲────────────────────────▲───────────────┘
                   │                        │
       VPC Peering │                        │ VPC Peering
                   ▼                        ▼
   ┌────────────────────────┐      ┌────────────────────────┐
   │    [ Production VPC ]  │      │     [ Staging VPC ]    │
   │   CIDR: 10.10.0.0/16   │      │   CIDR: 10.20.0.0/16   │
   │  (Production App VMs)  │      │   (Testing / QA VMs)   │
   └────────────────────────┘      └────────────────────────┘
```

## Key Architectural Rules of VPC Peering

* **Zero Gateway Bottleneck:** Peering connects software-defined SDN controllers directly. Traffic travels over Google’s private fiber with **line-rate latency and no single router bottleneck**.
* **Non-Transitive Routing:** If VPC A peers with VPC B, and VPC B peers with VPC C, **VPC A cannot talk to VPC C through VPC B**. Peering is strictly direct (point-to-point).
* **No Overlapping CIDRs:** Peering will immediately fail if two VPCs share identical or overlapping IP subnets.

## Complete Terraform Configuration: Hub-and-Spoke VPC Peering

```hcl
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
  region        = "us-central1"
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
  region        = "us-central1"
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
```

## Shared VPC vs. VPC Peering Comparison

| Dimension | VPC Network Peering | Shared VPC |
|---|---|---|
| **Organizational Model** | Decentralized (two separate teams connect their VPCs) | Centralized (one Network Admin team manages the Host VPC) |
| **Subnet Ownership** | Each project owns its own subnets | Projects share subnets created in a central Host Project |
| **IAM Control** | Independent IAM permissions | Central Network Admin controls network; Service Admins control VMs |
| **Use Case** | Multi-tenant SaaS, connecting partner networks | Large enterprise dividing Dev, QA, and Prod under one network team |
