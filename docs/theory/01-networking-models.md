# Stage 1: Networking Models — OSI & TCP/IP

!!! note "Key takeaways"
    - OSI is a 7-layer **conceptual** model — nothing in it is mandatory to implement literally
    - TCP/IP is the 4-layer model the real internet actually runs on
    - Almost every "which layer does X operate at" interview question maps back to this page

## Why a layered model at all?

Networking is broken into layers so that each layer only has to solve
one problem, and can be swapped out independently. Ethernet can be
replaced by Wi-Fi without touching how HTTP works, because they're at
different layers and only agree on the interface between them.

## The OSI model (7 layers)

| Layer | Name | Job | Example protocols/units |
|-------|------|-----|---------------------------|
| 7 | Application | What the user-facing software talks | HTTP, FTP, DNS |
| 6 | Presentation | Formatting, encryption, compression | TLS (often placed here or at 5) |
| 5 | Session | Manages sessions/connections between apps | Sockets, session tokens |
| 4 | Transport | End-to-end delivery between applications | TCP, UDP (unit: segment/datagram) |
| 3 | Network | Addressing & routing between networks | IP, routers (unit: packet) |
| 2 | Data Link | Delivery within one local network | Ethernet, switches, MAC (unit: frame) |
| 1 | Physical | Actual bits on the wire/air | Cables, radio, voltages (unit: bit) |

Mnemonic: **"All People Seem To Need Data Processing"** (7→1).

### Why interviewers love this model
Almost any "where does X happen" question is really asking you to place
something on this table. A switch = Layer 2. A router = Layer 3. TLS =
somewhere around 5/6. Once you can place a term on this table instantly,
half of networking trivia questions become mechanical.

## The TCP/IP model (4 layers) — what the internet actually uses

OSI is taught because it's a clean teaching model, but real-world
protocol stacks (and the internet itself) follow the simpler TCP/IP
model, which collapses several OSI layers together:

| TCP/IP Layer | Roughly maps to OSI | Protocols |
|---------------|------------------------|-----------|
| Application | 5, 6, 7 | HTTP, FTP, DNS, SSH |
| Transport | 4 | TCP, UDP |
| Internet | 3 | IP, ICMP |
| Link (Network Access) | 1, 2 | Ethernet, Wi-Fi |

**Practical rule of thumb:** when someone says "Layer 3" or "Layer 7"
casually in industry, they're almost always using OSI numbering even
though the actual implementation is TCP/IP-based. This is why both
models are worth knowing — OSI gives you the vocabulary, TCP/IP
describes what's actually running.

## Protocol roadmap

The protocols introduced later in this theory sequence solve different problems
at different layers. Learning them in dependency order prevents them from
becoming a disconnected list of acronyms.

| Protocol | What it does | Layer/context | Learn in |
|:---------|:-------------|:--------------|:---------|
| **ARP** | Maps a local IPv4 address to the MAC address needed to deliver an Ethernet frame | Link between Layers 2 and 3; local broadcast domain only | [Stage 3 — MAC Addresses & ARP](03-mac-arp.md) |
| **NAT/PAT** | Rewrites private addresses, and with PAT transport identifiers, at a routed boundary | Layer 3 with Layer 4 awareness for PAT | [Stage 5 — Private IPs, NAT & PAT](05-private-ip-nat.md) |
| **DHCP** | Leases an IP address, subnet mask, default gateway, DNS servers, and other options to a host | Application protocol using UDP; depends on local broadcast or relay | [Stage 6 — Subnetting & DHCP](06-subnetting-dhcp.md) |
| **OSPF** | Exchanges topology information so routers inside one organization can calculate routes | Layer 3 routing control plane; IP protocol 89 | [Stage 8 — Routing](08-routing-protocols.md) |
| **BGP** | Exchanges policy-controlled network reachability within or between autonomous systems | Routing control plane over TCP 179 | [Stage 8 — Routing](08-routing-protocols.md) |
| **DNS** | Resolves names to addresses and stores other namespace records | Application protocol, normally UDP or TCP 53 | [Stage 10 — DNS & Ports](10-dns-and-ports.md) |

These protocols cooperate but do not replace one another. For example, DHCP can
tell a client which DNS resolver to use; DNS can return a remote IP address; the
routing table chooses a next hop; ARP resolves the local next hop's MAC address;
and NAT/PAT may translate the flow at the network edge.

## Encapsulation (how data moves down and up the stack)

As data travels down the stack on the sending side, each layer wraps
the data from the layer above with its own header (and sometimes
trailer):

```
Application data
  → [TCP header | data]                       (Segment)
    → [IP header | TCP header | data]         (Packet)
      → [Ethernet header | IP header | ... ]  (Frame)
```

The receiving side does the reverse — each layer strips its own header
before passing the payload up. This is *encapsulation* and
*de-encapsulation*, and it's the mechanical reason each layer can stay
ignorant of the layers above and below it.

!!! info "Cloud connection"
    Terraform and Kubernetes are not additional network layers. They configure resources—such as subnets, load balancers, Services, and policies—that operate at the existing layers.

## Practice in Packet Tracer

- [Lab 01 — Single-Subnet FTP/HTTP](../labs/lab1-switch/1-basic-ftp-http-lan.md): observe encapsulation from ARP through TCP and HTTP/FTP.

## Next
[Packets & IP Addressing →](02-packets-ip-addressing.md)
