# Stage 10: DNS & Ports

!!! note "Key takeaways"
    - DNS turns domain names into IP addresses via a hierarchical lookup
    - Ports let one IP address serve many simultaneous applications/connections
    - IP = building address, Port = apartment number

## DNS (Domain Name System)

Humans use `google.com`; the network needs `142.250.72.14`. DNS is the
distributed lookup system that bridges the two.

### The hierarchy, top to bottom
1. **Root servers** — know where to find servers for each top-level domain (`.com`, `.org`, etc.)
2. **TLD servers** — know where to find the authoritative servers for domains under that TLD
3. **Authoritative DNS servers** — hold the actual record for `google.com` and return its IP

### A typical lookup (simplified)
```
Your device → DNS resolver (often your ISP or 8.8.8.8)
  → Resolver asks a root server: "who handles .com?"
  → Root server: "ask this TLD server"
  → TLD server: "ask google.com's authoritative server"
  → Authoritative server: "142.250.72.14"
  → Resolver caches this and returns it to you
```

In practice, most lookups never touch the root/TLD servers directly
because of aggressive caching at every layer — your OS, your browser,
and your resolver all cache DNS answers for a **TTL** (a different TTL
concept from the packet one — this is "how long is this DNS answer
valid before I should ask again").

### Common record types (worth knowing cold)
| Record | Purpose |
|--------|---------|
| A | Domain → IPv4 address |
| AAAA | Domain → IPv6 address |
| CNAME | Domain → another domain (alias) |
| MX | Mail server for the domain |
| TXT | Arbitrary text (often used for domain verification, SPF/DKIM) |
| NS | Which servers are authoritative for this domain |

## Ports

A single device might be running a web server, an SSH daemon, and a
mail client all at once — all sharing one IP address. **Ports**
disambiguate which application on that device a given piece of traffic
is meant for.

- Range: 0–65535
- **IP address ≈ building address, port number ≈ apartment number**
- A connection is really identified by a 4-tuple: `(source IP, source
  port, destination IP, destination port)` — this is what makes
  thousands of simultaneous connections between the same two IPs
  possible (your browser has many tabs open to the same site, each
  using a different source port)

### Well-known ports (memorize these — they come up constantly)
| Port | Protocol |
|------|----------|
| 20/21 | FTP (data / control) |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP (email sending) |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5432 | PostgreSQL |

Ports 0–1023 are "well-known/system" ports (traditionally require admin
privileges to bind to on Unix systems); 1024–49151 are "registered";
above that are "dynamic/ephemeral" — the range your OS picks from when
*your* machine initiates an outbound connection.

!!! info "Cloud connection"
    Public DNS can point a hostname to a cloud load balancer, while Kubernetes cluster DNS resolves internal Service names. DNS returns an address or alias; routing, policy, and a listening application must still make that destination usable.

## Practice in Packet Tracer

- [Lab 05 — DNS & Name Resolution](../labs/lab5-DNS/5-dns_lab.md): configure A/CNAME records and observe DNS before HTTP.

## Next
[HTTP/HTTPS & TLS →](11-http-https-tls.md)
