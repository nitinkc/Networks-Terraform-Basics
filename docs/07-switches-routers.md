# 7. Switches vs Routers

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

## Next
[VLANs →](08-vlans.md)
