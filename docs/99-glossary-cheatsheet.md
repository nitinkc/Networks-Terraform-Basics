# Glossary & Interview Cheat-Sheet

Quick-reference for last-minute review. If a term here feels shaky,
click through to its page.

## One-line definitions

| Term | Definition |
|------|------------|
| **OSI Model** | 7-layer conceptual model of networking |
| **TCP/IP Model** | 4-layer model the real internet runs on |
| **Packet** | A chunk of data + header, the basic unit at Layer 3 |
| **Frame** | A packet wrapped with Layer 2 (MAC) header info |
| **IP Address** | Logical address identifying a device on a network |
| **Subnet / CIDR** | A defined sub-range of an IP address space |
| **DNS** | Translates domain names to IP addresses |
| **Port** | Identifies which application on a device traffic is for |
| **Private IP** | Non-internet-routable address reused across networks |
| **NAT/PAT** | Translates private IPs (+ports) to a shared public IP |
| **DHCP** | Automatically assigns IP config to devices |
| **MAC Address** | Hardware address, Layer 2, identifies a NIC |
| **ARP** | Resolves a known IP to its MAC address on the local network |
| **Switch** | Layer 2 device, forwards by MAC within one network |
| **Router** | Layer 3 device, forwards by IP between networks |
| **VLAN** | Logically separates one physical switch into multiple networks |
| **TCP** | Reliable, ordered, connection-based transport protocol |
| **UDP** | Fast, connectionless, no-guarantee transport protocol |
| **HTTP/HTTPS** | Web request/response protocol; HTTPS = HTTP + TLS |
| **TLS** | Encrypts, authenticates, and ensures integrity of a connection |
| **Firewall** | Enforces allow/deny policy on network traffic |
| **VPN** | Encrypted tunnel masking traffic/IP over an untrusted network |
| **Forward Proxy** | Sits in front of clients, forwards requests out |
| **Reverse Proxy** | Sits in front of servers, forwards requests in |
| **Load Balancer** | Distributes traffic across multiple backend servers |

## Layer cheat-sheet (fastest way to answer "what layer is X")

| Layer | # | Lives here |
|-------|---|------------|
| Application | 7 | HTTP, FTP, DNS |
| Presentation/Session | 6/5 | TLS |
| Transport | 4 | TCP, UDP, ports |
| Network | 3 | IP, routers, routing tables |
| Data Link | 2 | Ethernet, switches, MAC, ARP, VLANs |
| Physical | 1 | Cables, radio |

## Common interview questions this material answers directly

- *What happens when you type a URL into a browser?* → DNS lookup (p.3)
  → TCP handshake (p.9) → TLS handshake if HTTPS (p.10) → HTTP
  request/response (p.10) → rendering (out of scope here)
- *Why does NAT exist?* → IPv4 exhaustion (p.2, p.4)
- *Difference between a switch and a router?* → p.7
- *Difference between TCP and UDP, and when to use each?* → p.9
- *What does a VPN actually protect against?* → p.12
- *Why can't two devices in different VLANs talk without a router?* → p.8
- *What three things does TLS guarantee?* → confidentiality, integrity,
  authentication (p.10)
- *Forward vs reverse proxy — how do you keep them straight?* → which
  side it sits in front of (p.12)
