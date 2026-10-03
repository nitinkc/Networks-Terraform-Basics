# Stage 9: TCP vs UDP

!!! note "Key takeaways"
    - TCP = reliable, ordered, connection-based — costs overhead
    - UDP = fire-and-forget, connectionless — costs nothing but reliability
    - Choice of protocol is a direct trade: correctness vs speed

Both operate at the **Transport layer** (Layer 4). Both use ports to
identify applications, as covered in [DNS and Ports](10-dns-and-ports.md). That's where the similarity ends.

## TCP (Transmission Control Protocol)

### The three-way handshake
Before any data flows, TCP establishes a connection:
```
Client → Server:  SYN
Server → Client:  SYN-ACK
Client → Server:  ACK
```
Only after this handshake does actual data start flowing. This is the
overhead cost of TCP's reliability guarantees — every connection pays
this latency upfront (one full round-trip) before useful work begins.

### What TCP guarantees
- **Ordered delivery** — segments are sequenced and reassembled in the
  correct order even if they arrive out of order
- **Reliability** — lost segments are detected (via acknowledgments)
  and retransmitted
- **Flow control** — the receiver can tell the sender to slow down if
  it's being overwhelmed
- **Congestion control** — TCP backs off when it detects network
  congestion, to avoid making things worse for everyone sharing the link

### When to use TCP
Anything where correctness matters more than raw speed: web traffic,
file transfers, email, databases — losing or reordering a byte in a
bank transaction or a downloaded file is unacceptable.

## UDP (User Datagram Protocol)

- **Connectionless** — no handshake, just send
- **No guarantees** — no ordering, no retransmission, no flow control
- Much lower overhead and latency as a direct result

### When to use UDP
Anything where a late or dropped packet is worse than a slightly wrong
one: video calls, live streaming, online gaming, and — notably — **DNS**
queries, covered in [DNS and Ports](10-dns-and-ports.md), which use UDP by default because a single small query
just isn't worth handshake overhead; if it's lost, the client just
retries the whole query rather than needing byte-level retransmission.

## Side-by-side

| | TCP | UDP |
|---|-----|-----|
| Connection | Yes (handshake) | No |
| Reliability | Guaranteed (retransmits) | None |
| Ordering | Guaranteed | None |
| Overhead | Higher | Lower |
| Speed | Slower | Faster |
| Typical use | HTTP, FTP, SSH, databases | DNS, video/voice calls, gaming |

## A common follow-up interview question

*"If UDP has no reliability, how does video calling still mostly work?"*
— reliability is rebuilt at the **application layer** when needed. A
video call would rather drop a frame and keep moving than pause the
entire call to retransmit an old one — so the application itself
decides how to handle loss, rather than relying on the transport layer
to force retransmission the way TCP would.

!!! info "Cloud connection"
    A proxy or load balancer may terminate one TCP connection and create a separate backend connection. In Kubernetes, a Service's `port` is the stable port clients use, while `targetPort` identifies the port on which selected Pods listen.

## Next
[DNS & Ports →](10-dns-and-ports.md)
