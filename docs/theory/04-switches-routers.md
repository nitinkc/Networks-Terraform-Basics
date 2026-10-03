# Stage 4: Switches vs Routers

!!! note "Key takeaways"
    - Switch = Layer 2, forwards by MAC address, connects devices *within* one network
    - Router = Layer 3, forwards by IP address, connects *different* networks together
    - A home "router" is almost always a router + switch + modem combined into one box

## Switches (Layer 2)

A switch's job: receive a frame on one port, figure out which port the
destination MAC address lives on, and forward it *only* there — not to
every other port (that would be a **hub**, an older, dumber device that
just repeats everything to everyone).

### How a switch learns
1. When a frame arrives, the switch notes: *"this source MAC came in on
   this port"* and records it in its **MAC address table**
2. Over time, it builds a complete map of which MAC lives behind which port
3. If it ever receives a frame for a MAC it hasn't learned yet, it
   floods that frame to all ports (except the one it came from) — once
   the real owner responds, the switch learns the mapping and stops flooding

```
show mac address-table    (Cisco command to view the learned table)
```

### Why switches matter for performance
Because a switch only sends traffic where it needs to go, two devices
on the same switch can talk to each other at full speed *simultaneously*
with two other devices talking to each other — unlike a hub, where
every device competes for the same shared bandwidth.

## Routers (Layer 3)

A router's job: receive a packet, look at its **destination IP**,
consult the routing table, and forward it out the correct interface —
potentially onto a completely different physical network.

The router is the device that actually understands the concept of
"different networks" — a switch has no idea what an IP subnet even is;
it only ever thinks in MAC addresses.

## Side-by-side

| | Switch | Router |
|---|--------|--------|
| OSI Layer | 2 | 3 |
| Forwards based on | MAC address | IP address |
| Scope | Within one network/broadcast domain | Between different networks |
| Learns/builds | MAC address table | Routing table |
| Typical use | Connecting PCs, servers, printers in one LAN | Connecting your LAN to another LAN or the internet |

## Why "my router" often does both jobs

Consumer Wi-Fi routers almost always bundle a router, a multi-port
switch, and often a wireless access point (and sometimes a modem too)
into a single physical box. When you plug 4 devices into the back of
your home router and they can all reach each other *and* the internet,
you're actually using its built-in switch for the first part and its
router function for the second — it's easy to conflate the two because
they're physically inseparable in that product.

## WAN and LAN sides of an all-in-one router

The **WAN (Wide Area Network) port** connects the router toward an upstream
network—usually an ISP modem, fiber terminal, or another router. The **LAN
(Local Area Network) ports** connect local devices through the router's built-in
Layer 2 switch.

```text
                 [ ISP / UPSTREAM NETWORK ]
                            │
                            ▼
                 ┌─────────────────────┐
                 │      WAN PORT       │  Outside/upstream interface
                 ├─────────────────────┤
                 │    ROUTER ENGINE    │  Routing, NAT/PAT, policy
                 ├─────────────────────┤
                 │   INTERNAL SWITCH   │  Layer 2 forwarding
                 └──┬────┬────┬────┬───┘
                    │    │    │    │
                  LAN1 LAN2 LAN3 LAN4
                    │    │    │    │
                    ▼    ▼    ▼    ▼
                       Local devices
                    Private LAN subnet
```

| Feature | WAN side | LAN side |
|:--------|:---------|:---------|
| **Primary purpose** | Connects toward an ISP or upstream router | Connects local computers, printers, access points, and switches |
| **Forwarding role** | Carries traffic toward remote networks and a default route | Carries local frames and traffic sent to the default gateway |
| **Typical addressing** | Public ISP address, or sometimes a private address behind another NAT device | Private gateway address such as `192.168.1.1/24` |
| **NAT terminology** | Commonly marked `ip nat outside` | Commonly marked `ip nat inside` |
| **Physical layout** | Often one dedicated Ethernet port | Often several ports on an integrated switch |

A few distinctions prevent common misunderstandings:

- A WAN port is not guaranteed to hold a public address. It may receive a private
  address when the router sits behind an ISP gateway or another router, creating
  **double NAT**.
- LAN switch ports do not assign addresses. A DHCP server—often another function
  inside the same appliance—leases IP address, mask, gateway, and DNS settings.
- NAT, routing, switching, DHCP, Wi-Fi, and firewalling are separate functions
  even when one physical device performs all of them.
- Blocking unsolicited inbound traffic is normally the result of NAT state and
  firewall policy, not an inherent property of the physical WAN socket.
- Enterprise routers may use several routed interfaces without labels such as
  “WAN” and “LAN”; their role comes from addressing, routes, NAT, and policy.

This inside/outside distinction leads directly into
[Private IPs, NAT & PAT](05-private-ip-nat.md).

!!! info "Cloud connection"
    Cloud VPC forwarding is distributed rather than performed by one visible physical router. A Kubernetes Service is also not an Ethernet switch; it is a stable virtual endpoint that directs traffic to selected Pods.

## Practice in Packet Tracer

- [Lab 01 — Single-Subnet FTP/HTTP](../labs/lab1-switch/1-basic-ftp-http-lan.md): prove that same-subnet traffic needs switching, not routing.
- [Lab 02 — Router & Subnets](../labs/lab2-Routers&Subnets/2-router-ftp-http-lab.md): cross two broadcast domains through a router.
- [Lab 04 — DHCP Relay](../labs/lab4-DHCP/4-dhcp_lab.md): observe a router forwarding a normally local broadcast through a relay function.

## Next
[Private IPs, NAT & PAT →](05-private-ip-nat.md)
