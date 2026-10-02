# Lab-aligned learning path

Use this page as the bridge between the theory reference and the hands-on labs. Read the listed theory first, complete the lab, and then return to the verification questions.

## Recommended sequence

| Stage | Lab | Read first | What the lab proves |
|---|---|---|---|
| 1 | [Single-subnet FTP/HTTP](labs/lab1-switch/1-basic-ftp-http-lan.md) | [Models](01-networking-models.md), [MAC and ARP](03-mac-arp.md), [Switches and routers](04-switches-routers.md), [HTTP/HTTPS](11-http-https-tls.md) | Hosts in one subnet communicate through Layer 2 switching without a gateway. |
| 2 | [Router and subnets](labs/lab2-Routers&Subnets/2-router-ftp-http-lab.md) | [IP addressing](02-packets-ip-addressing.md), [Subnetting](06-subnetting-dhcp.md), [Switches and routers](04-switches-routers.md) | Traffic between broadcast domains needs a router and correct default gateways. |
| 3 | [Multi-router NAT and DHCP](labs/3-multi-router-nat-dhcp-lab.md) | [Private IP and NAT](05-private-ip-nat.md), [Subnetting and DHCP](06-subnetting-dhcp.md), [Routing](08-routing-protocols.md) | DHCP, default routing, and PAT combine at an enterprise edge. |
| 4 | [DHCP and relay](labs/lab4-DHCP/4-dhcp_lab.md) | [Subnetting and DHCP](06-subnetting-dhcp.md), [Switches and routers](04-switches-routers.md) | Broadcast-based DORA works locally; a relay carries requests across a router. |
| 5 | [DNS and name resolution](labs/lab5-DNS/5-dns_lab.md) | [DNS and ports](10-dns-and-ports.md), [TCP and UDP](09-tcp-udp.md), [HTTP/HTTPS](11-http-https-tls.md) | DNS resolution precedes application traffic and depends on routing and DHCP options. |
| 6 | [NAT, PAT, and forwarding](labs/lab6-NAT-PAT/6-nat_pat_lab.md) | [Private IP and NAT](05-private-ip-nat.md), [TCP and UDP](09-tcp-udp.md), [Firewalls](13-firewalls.md) | Translation state changes packet endpoints while ports identify simultaneous flows. |
| 7 | [OSPF and BGP](labs/7-bgp_ospf_lab.md) | [Routing protocols](08-routing-protocols.md), [Packets and IP](02-packets-ip-addressing.md) | An IGP distributes internal reachability while BGP exchanges routes between autonomous systems. |
| 8 | [VLANs and ACLs](labs/lab8-LAN-ACL/8-lan_acl_lab.md) | [VLANs](07-vlans.md), [ACLs and segmentation](12-acls-segmentation.md), [TCP and UDP](09-tcp-udp.md) | VLANs create boundaries; inter-VLAN routing reconnects them; ACLs enforce policy. |
| 9 | [Packet Tracer GCP equivalent](labs/9-networking_gcp_equivalent_lab.md) | [Cloud and hybrid networking](15-cloud-hybrid-networking.md), [VLANs](07-vlans.md), [Firewalls](13-firewalls.md) | Physical network concepts map to cloud subnets, routes, NAT, DNS, and policy. |
| 10 | [GCP with Terraform](labs/10-gcp_terraform_networking_scenario.md) | [Cloud and hybrid networking](15-cloud-hybrid-networking.md), [Private IP and NAT](05-private-ip-nat.md), [DNS and ports](10-dns-and-ports.md) | Cloud networking primitives can be expressed as declarative infrastructure. |
| 11 | [VPC peering and Shared VPC](labs/lab_vpc_peering_shared_vpc.md) | [Cloud and hybrid networking](15-cloud-hybrid-networking.md), [Routing protocols](08-routing-protocols.md) | Connectivity and administration are separate design choices; peering is not transitive. |
| 12 | [L4 and L7 load balancing](labs/lab_load_balancing_l4_l7.md) | [VPNs, proxies, and load balancers](14-vpn-proxies-loadbalancers.md), [TCP and UDP](09-tcp-udp.md), [HTTP/HTTPS](11-http-https-tls.md) | L4 distributes connections; L7 can route using application data. |
| 13 | [IPsec VPN and BGP](labs/lab_ipsec_vpn_bgp_hybrid_cloud.md) | [Cloud and hybrid networking](15-cloud-hybrid-networking.md), [Routing protocols](08-routing-protocols.md), [VPNs](14-vpn-proxies-loadbalancers.md) | Encryption provides a tunnel; BGP determines which prefixes use it. |


# Hands-On Terraform Lab Sequence
Step A: VPC, Subnetting & Auto-DHCP (Terraform Track 02)
Write Terraform to provision a custom VPC and a /24 subnet.
Launch Compute Engine VMs without static IPs and inspect how GCP’s hypervisor dynamically issues internal IP leases.
Step B: Cloud NAT & Internet Gateway (Terraform Track 03)
Create a Private Subnet (no public IPs on VMs).
Provision a Cloud Router and Cloud NAT Gateway in Terraform to allow outbound internet access (package updates) while keeping the VMs private.
Step C: Cloud Private DNS (Terraform Track 04)
Provision a Private google_dns_managed_zone (e.g. internal.gcp).
Create google_dns_record_set resources mapping VM hostnames to internal DHCP-leased IP addresses.

## A repeatable study loop

1. **Predict:** identify source, destination, subnet boundary, gateway, and expected protocol.
2. **Build:** follow the lab exactly; treat its addressing plan as authoritative.
3. **Observe:** inspect ARP, DHCP, DNS, routing, NAT, ACL, or session state as applicable.
4. **Explain:** describe every hop using both an OSI layer and the device decision being made.
5. **Break and repair:** change one item, predict the symptom, restore it, and verify again.

## Questions to answer for every lab

- Is the destination local or remote, and how does the sender decide?
- Which addresses remain end-to-end, and which are rewritten?
- Which control-plane process created the forwarding information?
- Where is policy enforced, and is the device stateful or stateless?
- Which command or packet capture proves the explanation?
