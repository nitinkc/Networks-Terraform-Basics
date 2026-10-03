# Networking Knowledge Check

The knowledge check is divided into short topic quizzes so you can finish one
section at a time. Each question has one correct answer and displays an
explanation after submission. Results are stored locally in your browser by the
`mkdocs-quiz` plugin.

## Choose a section

| Section | Questions | Topics |
|:--------|----------:|:-------|
| [1. Models, packets, and local delivery](99-quiz-models-local-delivery.md) | 7 | OSI, frames, IP, gateways, ARP, switches, and routers |
| [2. Addressing, DHCP, VLANs, and routing](99-quiz-addressing-routing.md) | 6 | CIDR, DHCP, VLANs, route selection, OSPF, and BGP |
| [3. Transport, DNS, and web traffic](99-quiz-transport-web.md) | 5 | TCP, UDP, ports, DNS, HTTPS, and TLS |
| [4. NAT, policy, proxies, and cloud networking](99-quiz-nat-cloud.md) | 10 | NAT, firewalls, proxies, load balancing, VPN, BGP, and VPCs |

Start with any section. Previous, home, and next links at the bottom of each
quiz make it easy to continue without scrolling through the complete question
bank.

## Adding questions

Add each new question block to the topic file that best matches it, following
the markup pattern used by the existing questions. If a topic becomes long,
create another numbered quiz file, add it to the table
above, and register it under **Knowledge Check Quiz** in `mkdocs.yml`.

## Review by topic

| Quiz topic | Theory review |
|:-----------|:--------------|
| Models, packets, frames | [Networking Models](01-networking-models.md), [Packets & IP Addressing](02-packets-ip-addressing.md) |
| ARP, switches, routers | [MAC Addresses & ARP](03-mac-arp.md), [Switches vs Routers](04-switches-routers.md) |
| NAT and private addressing | [Private IPs, NAT & PAT](05-private-ip-nat.md) |
| Subnets and DHCP | [Subnetting & DHCP](06-subnetting-dhcp.md) |
| VLANs and routing | [VLANs](07-vlans.md), [Static Routing, OSPF & BGP](08-routing-protocols.md) |
| TCP, UDP, DNS, and ports | [TCP vs UDP](09-tcp-udp.md), [DNS & Ports](10-dns-and-ports.md) |
| HTTP and TLS | [HTTP/HTTPS & TLS](11-http-https-tls.md) |
| ACLs and firewalls | [ACLs & Segmentation](12-acls-segmentation.md), [Firewalls](13-firewalls.md) |
| VPNs, proxies, and load balancing | [VPNs, Proxies & Load Balancers](14-vpn-proxies-loadbalancers.md) |
| Cloud networking | [Cloud & Hybrid Networking](15-cloud-hybrid-networking.md) |
