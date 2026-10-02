# Networking Fundamentals — One Packet, End to End

This theory track follows one system from a developer's laptop to a production
microservice running on Kubernetes in Google Cloud. Instead of treating each
networking concept as an isolated lesson, every chapter explains one more part
of the same packet journey.

The Packet Tracer labs remain separate, deliberately small exercises. Use them
to observe individual mechanisms after learning how those mechanisms cooperate
in the production story.

## The continuing scenario: ShopNow

ShopNow is a small e-commerce platform with three Kubernetes workloads:

- `web` receives customer HTTPS requests.
- `orders` implements the order API.
- `inventory` checks and reserves stock.

Terraform provisions the infrastructure: a GCP VPC, regional subnets, a private
GKE cluster, Cloud NAT, firewall rules, Cloud DNS, and an external HTTPS load
balancer. Kubernetes then schedules Pods and provides Services and Ingress for
the applications.

```text
Developer laptop
    |
Home/office switch -> router/NAT -> ISP and internet
                                      |
                              Cloud DNS record
                                      |
                           HTTPS load balancer
                                      |
                         GKE Ingress / Service
                                      |
                 web Pod -> orders Pod -> inventory Pod
                                      |
                              managed database
```

The example intentionally has two layers of declarative infrastructure:

- **Terraform** creates cloud networking and the Kubernetes cluster.
- **Kubernetes manifests** describe application networking inside the cluster.

The theory distinguishes physical networking, cloud virtual networking, and
Kubernetes networking rather than pretending that similarly named components
are identical.

## Recommended theory sequence

Read the chapters in this order. The filenames retain their original numbers so
existing lab links and bookmarks continue to work; the navigation order is the
learning order.

| Stage | Topic | Question answered in the ShopNow journey |
|:------|:------|:-------------------------------------------|
| 1 | [Networking Models](01-networking-models.md) | Which layer owns each part of the request? |
| 2 | [Packets & IP Addressing](02-packets-ip-addressing.md) | How is application data addressed and encapsulated? |
| 3 | [MAC Addresses & ARP](03-mac-arp.md) | How does the laptop reach the first local hop? |
| 4 | [Switches vs Routers](04-switches-routers.md) | How does traffic leave the local network? |
| 5 | [Private IPs, NAT & PAT](05-private-ip-nat.md) | How do private clients and private cluster nodes reach public networks? |
| 6 | [Subnetting & DHCP](06-subnetting-dhcp.md) | How are address ranges planned and client settings assigned? |
| 7 | [VLANs](07-vlans.md) | How are local environments separated on shared hardware? |
| 8 | [Routing](08-routing-protocols.md) | How is the next hop selected across networks and hybrid links? |
| 9 | [TCP vs UDP](09-tcp-udp.md) | How do endpoints exchange reliable streams or datagrams? |
| 10 | [DNS & Ports](10-dns-and-ports.md) | How does `shop.example.com` locate the correct service? |
| 11 | [HTTP/HTTPS & TLS](11-http-https-tls.md) | How is the customer request represented and protected? |
| 12 | [ACLs & Segmentation](12-acls-segmentation.md) | Which source-to-destination flows should be allowed? |
| 13 | [Firewalls](13-firewalls.md) | How is stateful network policy enforced? |
| 14 | [VPNs, Proxies & Load Balancers](14-vpn-proxies-loadbalancers.md) | How do operators connect and how is traffic distributed? |
| 15 | [Cloud & Hybrid Networking](15-cloud-hybrid-networking.md) | How do Terraform, GCP, and Kubernetes assemble the complete design? |

## How to study each stage

1. Locate the component in the ShopNow diagram.
2. Predict what addresses, ports, tables, and policies the packet will encounter.
3. Read the theory chapter.
4. Use the [Lab-Aligned Learning Path](lab-theory-map.md) to choose a focused lab.
5. Return to the ShopNow scenario and explain how the lab mechanism appears in production.

A useful troubleshooting habit throughout the track is to ask four separate
questions:

1. **Resolution:** Did the name resolve to the intended address?
2. **Routing:** Is there a forward path and a return path?
3. **Policy:** Is the protocol and port allowed in both directions?
4. **Application:** Is a healthy process actually listening and responding?

## Reference

Use the [Glossary & Interview Cheat-Sheet](99-glossary-cheatsheet.md) for quick
revision rather than as the primary learning sequence.
