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
| 1 | [Single-subnet FTP/HTTP](01-single-subnet-ftp-http/index.md) | [Models](../theory/01-networking-models.md), [MAC and ARP](../theory/03-mac-arp.md), [Switches and routers](../theory/04-switches-routers.md), [HTTP/HTTPS](../theory/11-http-https-tls.md) | Hosts in one subnet communicate through Layer 2 switching without a gateway. |
| 2 | [Router and subnets](02-router-subnets/index.md) | [IP addressing](../theory/02-packets-ip-addressing.md), [Subnetting](../theory/06-subnetting-dhcp.md), [Switches and routers](../theory/04-switches-routers.md) | Traffic between broadcast domains needs a router and correct default gateways. |
| 3 | [Multi-router NAT and DHCP](03-multi-router-nat-dhcp/index.md) | [Private IP and NAT](../theory/05-private-ip-nat.md), [Subnetting and DHCP](../theory/06-subnetting-dhcp.md), [Routing](../theory/08-routing-protocols.md) | DHCP, default routing, and PAT combine at an enterprise edge. |
| 4 | [DHCP and relay](04-dhcp-relay/index.md) | [Subnetting and DHCP](../theory/06-subnetting-dhcp.md), [Switches and routers](../theory/04-switches-routers.md) | Broadcast-based DORA works locally; a relay carries requests across a router. |
| 5 | [DNS and name resolution](05-dns-name-resolution/index.md) | [DNS and ports](../theory/10-dns-and-ports.md), [TCP and UDP](../theory/09-tcp-udp.md), [HTTP/HTTPS](../theory/11-http-https-tls.md) | DNS resolution precedes application traffic and depends on routing and DHCP options. |
| 6 | [NAT, PAT, and forwarding](06-nat-pat-port-forwarding/index.md) | [Private IP and NAT](../theory/05-private-ip-nat.md), [TCP and UDP](../theory/09-tcp-udp.md), [Firewalls](../theory/13-firewalls.md) | Translation state changes packet endpoints while ports identify simultaneous flows. |
| 7 | [OSPF and BGP](07-ospf-ebgp/index.md) | [Routing protocols](../theory/08-routing-protocols.md), [Packets and IP](../theory/02-packets-ip-addressing.md) | An IGP distributes internal reachability while BGP exchanges routes between autonomous systems. |
| 8 | [VLANs and ACLs](08-vlans-acls/index.md) | [VLANs](../theory/07-vlans.md), [ACLs and segmentation](../theory/12-acls-segmentation.md), [TCP and UDP](../theory/09-tcp-udp.md) | VLANs create boundaries; inter-VLAN routing reconnects them; ACLs enforce policy. |
| 9 | [GCP architecture equivalent](09-gcp-architecture-equivalent/index.md) | [Cloud and hybrid networking](../theory/15-cloud-hybrid-networking.md), [VLANs](../theory/07-vlans.md), [Firewalls](../theory/13-firewalls.md) | Packet Tracer components model the physical concepts behind a two-tier cloud architecture. |

Lab 9 remains in this sequence because it is built and tested in Packet Tracer;
it uses GCP terminology only as a conceptual mapping.

## Terraform & GCP lab sequence

All Terraform exercises are located under `docs/terraform/` and build from a
first provider configuration toward multi-network and hybrid designs.

| Stage | Terraform/GCP lab | Read first | What the lab proves |
|:------|:------------------|:-----------|:--------------------|
| 1 | [Setup and first apply](../terraform/01-setup-first-apply/index.md) | [Cloud and hybrid networking](../theory/15-cloud-hybrid-networking.md) | Provider authentication, state, planning, application, and destruction form the Terraform workflow. |
| 2 | [VPC and subnets](../terraform/02-vpc-subnets/index.md) | [Packets and IP](../theory/02-packets-ip-addressing.md), [Subnetting](../theory/06-subnetting-dhcp.md) | A custom VPC and regional subnet express a software-defined routing domain and address plan. |
| 3 | [Routing, NAT, and firewall](../terraform/03-routing-nat-firewall/index.md) | [NAT and PAT](../theory/05-private-ip-nat.md), [Routing](../theory/08-routing-protocols.md), [Firewalls](../theory/13-firewalls.md) | Routes, Cloud NAT, and firewall rules solve different forwarding, translation, and policy problems. |
| 4 | [VMs and private DNS](../terraform/04-vms-and-dns/index.md) | [DNS and ports](../theory/10-dns-and-ports.md), [Cloud networking](../theory/15-cloud-hybrid-networking.md) | Private workloads receive addresses and resolve internal names without requiring public exposure. |
| 5 | [Two-tier networking scenario](../terraform/05-two-tier-networking-scenario/index.md) | Stages 1–4 | VPC, subnets, private DNS, firewall policy, NAT, and VMs work together in one architecture. |
| 6 | [VPC peering and Shared VPC](../terraform/06-vpc-peering-shared-vpc/index.md) | [Routing](../theory/08-routing-protocols.md), [Cloud networking](../theory/15-cloud-hybrid-networking.md) | Private connectivity and centralized network administration are separate design choices. |
| 7 | [L4 and L7 load balancing](../terraform/07-load-balancing-l4-l7/index.md) | [TCP and UDP](../theory/09-tcp-udp.md), [HTTP/HTTPS](../theory/11-http-https-tls.md), [Load balancers](../theory/14-vpn-proxies-loadbalancers.md) | L4 distributes connections while L7 can route using HTTP information. |
| 8 | [IPsec VPN and BGP](../terraform/08-ipsec-vpn-bgp-hybrid/index.md) | [Routing](../theory/08-routing-protocols.md), [VPNs](../theory/14-vpn-proxies-loadbalancers.md), [Cloud networking](../theory/15-cloud-hybrid-networking.md) | IPsec secures the tunnel while BGP exchanges the private prefixes that use it. |

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
