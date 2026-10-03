# Stage 8: Static Routing, OSPF & BGP

> **Key takeaways:** Forwarding uses the routing table. Static routes are configured directly, OSPF discovers paths inside an organization, and BGP exchanges policy-controlled reachability between autonomous systems.

## Control plane and data plane

The **control plane** learns or creates routes. The **data plane** performs a longest-prefix match for each packet and forwards it through the selected next hop. A routing protocol does not carry user traffic; it supplies information used to build the forwarding table.

A route commonly contains a destination prefix, next hop or exit interface, source, metric, and administrative preference. More-specific prefixes win before metrics are compared.

## Connected, static, and default routes

- **Connected route:** installed when an addressed interface is operational.
- **Static route:** entered by an administrator; predictable but manually maintained.
- **Default route (`0.0.0.0/0`):** used only when no more-specific route matches.

A successful route in one direction does not guarantee a return path. Troubleshooting must check both directions.

## OSPF: routing inside an organization

OSPF is a link-state Interior Gateway Protocol. Routers form neighbor relationships, describe links using Link-State Advertisements, build a common topology database, and run the Shortest Path First algorithm.

Important concepts:

- **Area:** limits flooding and computation; Area 0 is the backbone.
- **Router ID:** stable identifier for an OSPF router.
- **Cost:** path metric, normally derived from interface bandwidth.
- **Passive interface:** advertises a connected subnet without seeking neighbors there.
- **Convergence:** the process of reaching a consistent view after a change.

OSPF uses IP protocol 89, not TCP or UDP. Neighbors require compatible area, subnet, timers, authentication, and network-type settings.

## BGP: routing between autonomous systems

BGP is a path-vector Exterior Gateway Protocol. It exchanges prefixes and path attributes over TCP port 179. Its goal is scalable, policy-driven route selection rather than simply choosing the lowest link cost.

Core terms:

- **Autonomous System (AS):** network under one routing policy, identified by an ASN.
- **eBGP:** session between different autonomous systems.
- **iBGP:** session within one autonomous system.
- **AS_PATH:** AS sequence a route traversed; also prevents loops.
- **NEXT_HOP:** address used to reach an advertised prefix.
- **Local preference:** internal preference for an outbound path.

A BGP session being established proves peer connectivity, not that desired prefixes are advertised, accepted, or installed.

## Joining OSPF and BGP

An edge router can learn external routes through BGP while internal routers run OSPF. Common designs inject only a default route into OSPF rather than redistributing the full external table. Redistribution must be deliberate because it can create loops, unstable routing, or excessive state.

In the lab sequence, focus on three separate facts:

1. OSPF neighbors formed and internal prefixes were learned.
2. BGP peers established and external prefixes were exchanged.
3. The internal network learned an exit path and the external side had a return path.

## Verification model

| Question | Evidence |
|---|---|
| Are interfaces operational? | Interface status and connected routes |
| Are OSPF neighbors formed? | OSPF neighbor table |
| Did OSPF learn the prefix? | Routing table entry marked as OSPF |
| Is the BGP session established? | BGP summary and peer state |
| Is a prefix advertised and selected? | BGP table and routing table |
| Does traffic have a return route? | Remote routing table and traceroute |

## Common failure patterns

- Missing `no shutdown` or incorrect addressing prevents adjacency.
- A wildcard/network statement excludes the intended interface.
- A default route exists at the edge but is not originated into OSPF.
- BGP peers can reach each other, but no `network` statement or redistribution advertises the prefix.
- A prefix is learned but loses to a more preferred route source.
- Forward routing works while the destination lacks a route back.

!!! info "Cloud connection"
    Cloud VPC routes, hybrid BGP routes, and Kubernetes Service or Pod forwarding belong to different routing domains. Troubleshooting starts by identifying which domain currently owns the packet and checking both its forward and return paths.

## Next
[TCP vs UDP →](09-tcp-udp.md)

## Related labs

- [Multi-router NAT and DHCP](../labs/3-multi-router-nat-dhcp-lab.md)
- [OSPF and eBGP](../labs/7-bgp_ospf_lab.md)
- [VPC peering and Shared VPC](../terraform/06-vpc-peering-shared-vpc.md)
- [IPsec VPN with BGP](../terraform/08-ipsec-vpn-bgp-hybrid.md)
