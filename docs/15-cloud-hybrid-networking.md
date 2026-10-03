# Stage 15: Cloud & Hybrid Networking

> **Key takeaways:** Cloud networking uses familiar prefixes, routes, NAT, DNS, and filtering, but implements them as distributed services. Separate connectivity, routing, security, and administration when evaluating a design.

## Physical-to-cloud mapping

| Traditional concept | GCP-oriented equivalent |
|---|---|
| Routed enterprise network | VPC network |
| VLAN/subnet segment | VPC subnet (regional) |
| Router route table | Distributed VPC routing table |
| Edge PAT device | Cloud NAT with Cloud Router control plane |
| Packet-filtering policy | VPC firewall rule |
| Internal DNS server/zone | Cloud DNS private zone |
| Site-to-site encrypted link | Cloud VPN |
| Dynamic route exchange | Cloud Router with BGP |
| Shared network administration | Shared VPC |

The mapping is conceptual, not implementation-identical. A VPC is not a physical switch, Cloud Router does not forward packets, and firewall enforcement is distributed.

## Phase 2: The "Networking to Terraform" Bridge (Cloud Parity)

| Packet Tracer component | GCP equivalent | Terraform resource or implementation |
|:------------------------|:---------------|:-------------------------------------|
| Router0 / routed network boundary | Custom-mode VPC | `google_compute_network` |
| LAN 1 / LAN 2 subnets | Regional VPC subnets | `google_compute_subnetwork` |
| DHCP-Server0 relay and address pool | Built-in subnet address assignment through Google Cloud's virtual networking | Managed by the platform; no separate Terraform DHCP resource |
| Local or public DNS server | Cloud DNS managed zone | `google_dns_managed_zone` and `google_dns_record_set` |
| Router NAT/PAT | Cloud NAT attached to Cloud Router | `google_compute_router` and `google_compute_router_nat` |
| Client PCs and application servers | Compute Engine VM instances | `google_compute_instance` |

## Routes, firewalls, and NAT answer different questions

- **Route:** where should traffic go?
- **Firewall rule:** is this traffic permitted?
- **NAT:** should an address be translated at an edge?

A route does not imply permission. A firewall permit does not create a route. NAT does not replace either one.

Cloud NAT provides outbound translation for eligible private instances; it does not make them unsolicited inbound services. Publishing an application normally uses a load balancer or an explicitly addressed endpoint plus suitable firewall policy.

## VPC peering

VPC Network Peering exchanges selected reachability between two VPC networks while each network remains independently administered.

Critical properties:

- Peering must be configured for both sides of the relationship.
- Peering is **not transitive**: if A peers with B and B peers with C, A does not automatically reach C.
- Overlapping subnet ranges prevent usable routing and often prevent peering creation.
- Firewall policy is not automatically shared; each side must permit required flows.
- Peering does not merge the networks into one administrative domain.

## Shared VPC

Shared VPC centralizes a VPC in a host project and lets approved service projects attach workloads to its subnets. It is primarily an ownership and governance model, unlike peering, which connects independent VPCs.

Choose Shared VPC when a central platform team should manage network resources and policy. Choose peering when networks should remain administratively separate but need private connectivity.

## Load balancing at L4 and L7

Layer 4 load balancing uses connection information such as IP addresses, protocol, and ports. Layer 7 load balancing understands application data such as HTTP hostnames and URL paths, enabling content-based routing.

Both depend on health checks. A reachable frontend does not prove a backend is healthy; verify health status, firewall access from health-check sources, named ports or backend ports, and application response.

## Hybrid VPN and BGP

A hybrid design has two independent layers:

1. **IPsec** authenticates peers and encrypts packets across an untrusted network.
2. **BGP** advertises which prefixes are reachable through the tunnel.

A tunnel can be established while routes are missing, and BGP can fail even when IPsec security associations exist. Troubleshoot underlay reachability, IKE/IPsec parameters, tunnel state, BGP addressing/ASN configuration, learned routes, firewall policy, and return paths separately.

## Terraform as a network specification

Terraform expresses intended resources and relationships, but a successful plan does not prove runtime connectivity. Review dependencies and verify the deployed data plane.

A useful reading order is:

1. VPC and subnet CIDRs.
2. Routes, routers, NAT, peerings, and VPNs.
3. Firewall rules and their targets.
4. DNS zones and records.
5. Load-balancer frontends, backends, and health checks.
6. Compute interfaces, addresses, service accounts, and tags.

## Common failure patterns

- Overlapping CIDRs make private routing ambiguous.
- A firewall rule targets the wrong tag, identity, network, or direction.
- Peering exists only on one side or lacks required route exchange.
- A private VM has no valid egress path through NAT.
- VPN encryption succeeds but BGP advertises no application prefixes.
- Health checks are blocked even though user traffic is allowed.
- DNS resolves correctly to an address that routing or policy cannot reach.

## Next

Apply the complete theory track in the [Terraform and GKE networking case study](16-terraform-gke-case-study.md).

## Related labs

- [Packet Tracer GCP equivalent](labs/9-networking_gcp_equivalent_lab.md)
- [GCP networking with Terraform](terraform/05-two-tier-networking-scenario.md)
- [VPC peering and Shared VPC](terraform/06-vpc-peering-shared-vpc.md)
- [L4 and L7 load balancing](terraform/07-load-balancing-l4-l7.md)
- [IPsec VPN with BGP](terraform/08-ipsec-vpn-bgp-hybrid.md)
