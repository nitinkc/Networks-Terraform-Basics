# Stage 3: MAC Addresses & ARP

!!! note "Key takeaways"
    - MAC = Layer 2 hardware identifier, burned into the NIC, doesn't change with network
    - IP = Layer 3 logical identifier, changes depending on which network you're on
    - ARP is the bridge: it maps a known IP to the MAC address needed to actually deliver a frame locally

## MAC addresses

- 48 bits, written as `A4:5E:60:1B:2C:3D`
- Assigned by the manufacturer (the first 24 bits identify the vendor —
  this is why looking up a MAC's OUI can tell you the device manufacturer)
- Operates at **Layer 2** — used to deliver frames *within* a single
  local network/broadcast domain
- Stays constant regardless of which network the device joins (unlike
  an IP address, which is assigned per-network)

## Why you need both an IP and a MAC

IP addressing gets a packet to the correct **network**. But once the
packet reaches that local network, something still needs to know which
physical device on the wire to actually hand the frame to — that's the
MAC address's job. This is the core reason both addressing schemes
coexist: IP for *which network*, MAC for *which device on this network*.

## ARP (Address Resolution Protocol)

ARP is the mechanism that fills in that missing link: given a known IP
address on the same local network, what's the corresponding MAC address?

### The process
1. Device A wants to send to `192.168.1.1` but only knows the IP, not the MAC
2. Device A **broadcasts** an ARP request: *"Who has 192.168.1.1? Tell 192.168.1.10"*
3. Every device on the subnet receives it, but only the device that
   actually owns `192.168.1.1` replies
4. That device sends back an ARP reply with its MAC address
5. Device A caches this mapping (in its **ARP cache/table**) so it
   doesn't have to repeat this for every subsequent packet

```bash
# View your ARP cache on macOS/Linux
arp -a
```

### Why ARP is broadcast-based, and why that matters
Because ARP requests go to *everyone* on the subnet, ARP is inherently
a **local-only** protocol — it cannot and does not cross routers.
This is actually a clean way to understand the switch/router boundary:
ARP works within a broadcast domain (delimited by switches), and stops
at the router, because the router is the boundary between broadcast
domains.

### Security note (common interview tangent)
Because ARP has no authentication built in, a malicious device can
reply to ARP requests claiming to own an IP it doesn't — this is **ARP
spoofing/poisoning**, the basis of many man-in-the-middle attacks on
local networks. It's why enterprise switches often support **Dynamic
ARP Inspection (DAI)** to validate ARP replies against known bindings.

!!! info "Cloud connection"
    ARP remains local to a broadcast domain. Cloud platforms may virtualize or proxy Layer 2 behavior, so troubleshoot ARP only at the local hop rather than using it to explain a failure across routed cloud networks.

## Practice in Packet Tracer

- [Lab 01 — Single-Subnet FTP/HTTP](labs/lab1-switch/1-basic-ftp-http-lan.md): inspect ARP before the first local HTTP exchange.

## Next
[Switches vs Routers →](04-switches-routers.md)
