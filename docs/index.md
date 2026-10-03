# Networking Fundamentals — A Systematic Learning Path

This site teaches networking concepts in dependency order. Each theory chapter
first explains the mechanism on its own: what problem it solves, how it works,
which tables or headers it uses, and how to verify it. Short **Cloud connection**
notes show where the same idea appears in modern infrastructure without turning
the cloud example into the definition of the concept.

After completing the theory sequence, use the
[Terraform and GKE networking case study](theory/16-terraform-gke-case-study.md) to
combine the concepts in one production-style microservices architecture.

The Packet Tracer labs remain separate, deliberately small exercises. They make
individual mechanisms observable before cloud abstractions and application
components are added.

## Recommended theory sequence

| Stage | Topic | Why it appears here |
|:------|:------|:--------------------|
| 1 | [Networking Models](theory/01-networking-models.md) | Establish the vocabulary for every later layer. |
| 2 | [Packets & IP Addressing](theory/02-packets-ip-addressing.md) | Explain encapsulation, logical addresses, masks, and basic forwarding. |
| 3 | [MAC Addresses & ARP](theory/03-mac-arp.md) | Show how an IP packet reaches a local next hop. |
| 4 | [Switches vs Routers](theory/04-switches-routers.md) | Separate local Layer 2 forwarding from Layer 3 forwarding between networks. |
| 5 | [Private IPs, NAT & PAT](theory/05-private-ip-nat.md) | Explain private/public boundaries and translation after routing fundamentals. |
| 6 | [Subnetting & DHCP](theory/06-subnetting-dhcp.md) | Design address ranges and automate endpoint configuration. |
| 7 | [VLANs](theory/07-vlans.md) | Divide shared switching infrastructure into broadcast domains. |
| 8 | [Static Routing, OSPF & BGP](theory/08-routing-protocols.md) | Build and exchange paths across multiple networks. |
| 9 | [TCP vs UDP](theory/09-tcp-udp.md) | Add end-to-end transport behavior and application ports. |
| 10 | [DNS & Ports](theory/10-dns-and-ports.md) | Resolve names and identify services after transport is understood. |
| 11 | [HTTP/HTTPS & TLS](theory/11-http-https-tls.md) | Apply transport to web requests, encryption, and identity. |
| 12 | [ACLs & Network Segmentation](theory/12-acls-segmentation.md) | Convert source, destination, protocol, and port requirements into policy. |
| 13 | [Firewalls](theory/13-firewalls.md) | Extend filtering into stateful enforcement and security boundaries. |
| 14 | [VPNs, Proxies & Load Balancers](theory/14-vpn-proxies-loadbalancers.md) | Combine secure connectivity, intermediaries, and traffic distribution. |
| 15 | [Cloud & Hybrid Networking](theory/15-cloud-hybrid-networking.md) | Map the completed foundations to distributed cloud services and Terraform. |

## Applied case study

The [Terraform and GKE networking case study](theory/16-terraform-gke-case-study.md)
uses a three-service application to connect the completed theory:

- Terraform provisions VPC ranges, HA VPN and hybrid routes, Cloud NAT, firewall
  rules, a private GKE cluster, private DNS, an internal HTTPS load balancer, and
  privately reachable Apigee API management.
- Kubernetes deploys workloads, Services, ingress configuration, health checks,
  and NetworkPolicy.
- Two diagrams trace the architecture and the separate connection boundaries.
- Each packet-flow stage links back to the relevant theory chapter.
- A verification matrix and failure walkthroughs turn the architecture into a
  troubleshooting exercise.

The case study is intentionally last. It demonstrates the concepts; it does not
define or replace them.

## How to study

1. Read a theory chapter and explain the mechanism without referring to a cloud product.
2. Use its **Cloud connection** note to map—not redefine—the concept.
3. Complete a focused exercise from the [Lab-Aligned Learning Path](labs/lab-theory-map.md).
4. After Stage 15, trace the complete case study from DNS through application response.
5. For any failure, separate four questions:
   - **Resolution:** Did the name resolve to the intended address?
   - **Routing:** Is there a forward path and a return path?
   - **Policy:** Is the required protocol and port allowed?
   - **Application:** Is a healthy process listening and responding?

## Consolidate your knowledge

After completing the theory sequence, take the [Networking Knowledge Check](theory/99-quiz.md). The scored multiple-choice quiz provides immediate explanations and links back to each topic for review.
