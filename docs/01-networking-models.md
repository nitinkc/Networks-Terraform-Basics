# 1. Networking Models: OSI & TCP/IP

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

## Next
[Packets & IP Addressing →](02-packets-ip-addressing.md)
