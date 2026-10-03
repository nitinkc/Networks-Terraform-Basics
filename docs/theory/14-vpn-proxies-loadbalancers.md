# Stage 14: VPNs, Proxies & Load Balancers

!!! note "Key takeaways"
    - VPN: encrypted tunnel between you and a VPN server, masking your real IP and securing traffic over untrusted networks
    - Forward proxy: sits in front of clients, hides *them* from the destination
    - Reverse proxy: sits in front of servers, hides *them* from the client
    - Load balancer: usually implemented as a reverse proxy, distributes traffic across many backend servers

## VPN (Virtual Private Network)

A VPN creates an encrypted tunnel between your device and a VPN server.
All your traffic is routed through that tunnel before reaching its
real destination.

**What this actually achieves:**

- Anyone snooping on the network between you and the VPN server (e.g.,
  public Wi-Fi) sees only encrypted tunnel traffic, not your actual data
- The destination sees the VPN server's IP as the source, not yours —
  masking your real IP and location
- Commonly used to securely reach an internal corporate network from
  outside it, as if you were physically on-site

## Proxies

The distinction between forward and reverse proxies is entirely about
**which side they sit in front of** — this single fact resolves most
confusion about the terms.

### Forward proxy — sits in front of the client(s)
```
Client → Forward Proxy → Internet/destination
```

- The destination server sees requests coming from the proxy's IP, not
  the client's
- Used for: content filtering (a school/office blocking certain sites),
  caching frequently-requested content, or anonymizing outbound requests

### Reverse proxy — sits in front of the server(s)
```
Client → Reverse Proxy → Backend server(s)
```

- The client only ever talks to the reverse proxy; it never sees or
  knows about the actual backend servers
- Used for: **TLS termination** (the proxy handles the HTTPS encryption
  overhead so backend servers don't have to), caching, rate limiting,
  and hiding internal infrastructure details

## Load balancers

A load balancer is almost always implemented as a **form of reverse
proxy** — but its specific job is distributing incoming requests across
**multiple** backend servers, rather than just forwarding to one.

### Core responsibilities
- **Distribute traffic** using an algorithm:
    - *Round-robin* — cycle through servers in order
    - *Least connections* — send to whichever server currently has the fewest active connections
    - *IP hash* — consistently route a given client to the same backend server (useful when session state lives on a specific server)
- **Health checks** — periodically ping each backend; stop sending traffic to any server that's failing, automatically

## Summary table

| Concept | Sits in front of | Primary job | Example use case |
|---------|-------------------|-------------|-------------------|
| VPN | You (the client) | Encrypt your traffic, mask your IP | Remote access to corporate network |
| Forward Proxy | Clients | Forward client requests outward | Content filtering, caching |
| Reverse Proxy | Servers | Forward client requests inward | TLS termination, hiding backend |
| Load Balancer | Servers (multiple) | Distribute + health-check traffic | Preventing any one server from overloading |

!!! info "Cloud connection"
    Cloud load balancers, Kubernetes Ingress, and Services may be integrated by controllers, but their responsibilities remain distinct: public frontend, TLS policy, health checks, backend selection, Service routing, and Pod endpoints.

## Practice labs

- [Terraform Lab 07 — L4 & L7 Load Balancing](../terraform/07-load-balancing-l4-l7.md): build the load-balancer frontend and path-routing chain.
- [Terraform Lab 08 — IPsec VPN & BGP](../terraform/08-ipsec-vpn-bgp-hybrid.md): build a hybrid VPN and exchange private routes.

!!! note "Packet Tracer coverage"
    The current Packet Tracer track has no dedicated VPN lab. The Terraform/GCP hybrid lab contains the VPN exercise, while the Packet Tracer OSPF/eBGP lab provides the closest routing prerequisite.

## Next
[Cloud & Hybrid Networking →](15-cloud-hybrid-networking.md)
