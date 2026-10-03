# Lab-aligned learning path

Use this page as the bridge between theory and hands-on work. The practical
material is divided by platform so Packet Tracer exercises are not mixed with
Terraform/GCP deployments.

- **Packet Tracer labs** isolate Cisco, protocol, and packet-flow fundamentals.
- **Terraform & GCP labs** apply those fundamentals to declarative cloud infrastructure.

Read the listed theory first, predict the flow, complete the lab, and then prove
the result using device state, packet inspection, or cloud runtime evidence.

## Packet Tracer lab sequence

| Stage | Packet Tracer lab | Read first | What the lab proves |
|:------|:------------------|:-----------|:--------------------|
| 1 | [Single-subnet FTP/HTTP](lab1-switch/1-basic-ftp-http-lan.md) | [Models](../01-networking-models.md), [MAC and ARP](../03-mac-arp.md), [Switches and routers](../04-switches-routers.md), [HTTP/HTTPS](../11-http-https-tls.md) | Hosts in one subnet communicate through Layer 2 switching without a gateway. |
| 2 | [Router and subnets](lab2-Routers&Subnets/2-router-ftp-http-lab.md) | [IP addressing](../02-packets-ip-addressing.md), [Subnetting](../06-subnetting-dhcp.md), [Switches and routers](../04-switches-routers.md) | Traffic between broadcast domains needs a router and correct default gateways. |
| 3 | [Multi-router NAT and DHCP](3-multi-router-nat-dhcp-lab.md) | [Private IP and NAT](../05-private-ip-nat.md), [Subnetting and DHCP](../06-subnetting-dhcp.md), [Routing](../08-routing-protocols.md) | DHCP, default routing, and PAT combine at an enterprise edge. |
| 4 | [DHCP and relay](lab4-DHCP/4-dhcp_lab.md) | [Subnetting and DHCP](../06-subnetting-dhcp.md), [Switches and routers](../04-switches-routers.md) | Broadcast-based DORA works locally; a relay carries requests across a router. |
| 5 | [DNS and name resolution](lab5-DNS/5-dns_lab.md) | [DNS and ports](../10-dns-and-ports.md), [TCP and UDP](../09-tcp-udp.md), [HTTP/HTTPS](../11-http-https-tls.md) | DNS resolution precedes application traffic and depends on routing and DHCP options. |
| 6 | [NAT, PAT, and forwarding](lab6-NAT-PAT/6-nat_pat_lab.md) | [Private IP and NAT](../05-private-ip-nat.md), [TCP and UDP](../09-tcp-udp.md), [Firewalls](../13-firewalls.md) | Translation state changes packet endpoints while ports identify simultaneous flows. |
| 7 | [OSPF and BGP](7-bgp_ospf_lab.md) | [Routing protocols](../08-routing-protocols.md), [Packets and IP](../02-packets-ip-addressing.md) | An IGP distributes internal reachability while BGP exchanges routes between autonomous systems. |
| 8 | [VLANs and ACLs](lab8-LAN-ACL/8-lan_acl_lab.md) | [VLANs](../07-vlans.md), [ACLs and segmentation](../12-acls-segmentation.md), [TCP and UDP](../09-tcp-udp.md) | VLANs create boundaries; inter-VLAN routing reconnects them; ACLs enforce policy. |
| 9 | [GCP architecture equivalent](9-networking_gcp_equivalent_lab.md) | [Cloud and hybrid networking](../15-cloud-hybrid-networking.md), [VLANs](../07-vlans.md), [Firewalls](../13-firewalls.md) | Packet Tracer components model the physical concepts behind a two-tier cloud architecture. |

Lab 9 remains in this sequence because it is built and tested in Packet Tracer;
it uses GCP terminology only as a conceptual mapping.

## Terraform & GCP lab sequence

All Terraform exercises are located under `docs/terraform/` and build from a
first provider configuration toward multi-network and hybrid designs.

| Stage | Terraform/GCP lab | Read first | What the lab proves |
|:------|:------------------|:-----------|:--------------------|
| 1 | [Setup and first apply](../terraform/01-setup-first-apply.md) | [Cloud and hybrid networking](../15-cloud-hybrid-networking.md) | Provider authentication, state, planning, application, and destruction form the Terraform workflow. |
| 2 | [VPC and subnets](../terraform/02-vpc-subnets.md) | [Packets and IP](../02-packets-ip-addressing.md), [Subnetting](../06-subnetting-dhcp.md) | A custom VPC and regional subnet express a software-defined routing domain and address plan. |
| 3 | [Routing, NAT, and firewall](../terraform/03-routing-nat-firewall.md) | [NAT and PAT](../05-private-ip-nat.md), [Routing](../08-routing-protocols.md), [Firewalls](../13-firewalls.md) | Routes, Cloud NAT, and firewall rules solve different forwarding, translation, and policy problems. |
| 4 | [VMs and private DNS](../terraform/04-vms-and-dns.md) | [DNS and ports](../10-dns-and-ports.md), [Cloud networking](../15-cloud-hybrid-networking.md) | Private workloads receive addresses and resolve internal names without requiring public exposure. |
| 5 | [Two-tier networking scenario](../terraform/05-two-tier-networking-scenario.md) | Stages 1–4 | VPC, subnets, private DNS, firewall policy, NAT, and VMs work together in one architecture. |
| 6 | [VPC peering and Shared VPC](../terraform/06-vpc-peering-shared-vpc.md) | [Routing](../08-routing-protocols.md), [Cloud networking](../15-cloud-hybrid-networking.md) | Private connectivity and centralized network administration are separate design choices. |
| 7 | [L4 and L7 load balancing](../terraform/07-load-balancing-l4-l7.md) | [TCP and UDP](../09-tcp-udp.md), [HTTP/HTTPS](../11-http-https-tls.md), [Load balancers](../14-vpn-proxies-loadbalancers.md) | L4 distributes connections while L7 can route using HTTP information. |
| 8 | [IPsec VPN and BGP](../terraform/08-ipsec-vpn-bgp-hybrid.md) | [Routing](../08-routing-protocols.md), [VPNs](../14-vpn-proxies-loadbalancers.md), [Cloud networking](../15-cloud-hybrid-networking.md) | IPsec secures the tunnel while BGP exchanges the private prefixes that use it. |

## A repeatable study loop

1. **Predict:** identify source, destination, subnet boundary, gateway, and expected protocol.
2. **Build:** follow the selected platform's lab exactly; treat its addressing plan as authoritative.
3. **Observe:** inspect ARP, DHCP, DNS, routing, NAT, ACL, session state, Terraform output, or cloud runtime state as applicable.
4. **Explain:** describe every hop using an OSI layer and the forwarding or policy decision being made.
5. **Break and repair:** change one item, predict the symptom, restore it, and verify again.

## Questions to answer for every lab

- Is the destination local or remote, and how does the sender decide?
- Which addresses remain end-to-end, and which are rewritten?
- Which control-plane process created the forwarding information?
- Where is policy enforced, and is the device stateful or stateless?
- Which command, packet capture, Terraform output, or cloud log proves the explanation?
