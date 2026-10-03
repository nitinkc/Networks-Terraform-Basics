# Stage 6: Subnetting & DHCP

!!! note "Key takeaways"
    - Subnetting splits one large IP block into smaller, manageable networks
    - CIDR notation (`/24`, `/16`, etc.) tells you the subnet's size
    - DHCP automates handing out IPs so nobody has to manually configure every device

## Subnetting & CIDR

CIDR notation (`/prefix`) tells you how many bits are fixed as the
**network portion** of the address — the remaining bits are available
for host addresses within that subnet.

| CIDR | Subnet mask | Usable hosts (approx) |
|------|--------------|--------------------------|
| /8 | 255.0.0.0 | ~16.7 million |
| /16 | 255.255.0.0 | ~65,000 |
| /24 | 255.255.255.0 | 254 |
| /30 | 255.255.255.252 | 2 (common for point-to-point router links) |

**Rule of thumb:** the *larger* the number after the slash, the
*smaller* the subnet — because more bits are "used up" fixing the
network portion, leaving fewer bits free for host addresses.

### Why subnet at all?
- **Traffic isolation** — broadcast traffic on one subnet doesn't flood
  every other subnet
- **Security boundaries** — a firewall or ACL can allow/deny whole
  subnets at once instead of listing every device
- **Organizational clarity** — e.g., `/24` per floor or per department
  in an enterprise network
- **Address efficiency** — you don't waste a whole `/24` (254 addresses)
  on a link that only ever has 2 devices (this is exactly why
  router-to-router links commonly use `/30` — just enough for 2 usable
  addresses)

### Quick worked example
`192.168.1.0/24`:

- Network address: `192.168.1.0` (reserved, identifies the subnet itself)
- Broadcast address: `192.168.1.255` (reserved, reaches every host on
  the subnet)
- Usable range: `192.168.1.1` – `192.168.1.254` (254 addresses)

## DHCP (Dynamic Host Configuration Protocol)

Without DHCP, every device joining a network would need someone to
manually type in an IP, subnet mask, gateway, and DNS server. DHCP
automates all of it.

### The exchange (DORA — worth memorizing the acronym)
1. **Discover** — device broadcasts "is there a DHCP server here?"
2. **Offer** — a DHCP server responds with a proposed IP + config
3. **Request** — device says "yes, I'll take that one"
4. **Acknowledge** — server confirms and finalizes the **lease**

### What DHCP hands out
- IP address
- Subnet mask
- Default gateway
- DNS server(s)
- **Lease time** — the address is only valid for a set duration; the
  device must renew before it expires or it loses the address

### Cisco config reference (matches your lab)
```
ip dhcp pool LANPOOL
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
 dns-server 8.8.8.8
```
Verify with `show ip dhcp binding` — shows which device (by MAC) holds
which leased IP and for how long.

!!! info "Cloud connection"
    Terraform can declare cloud subnet and secondary ranges. Cloud platforms assign VM addresses through managed networking, while Kubernetes assigns Pod and Service addresses through cluster IP address management—not through the DHCP DORA exchange.

## Practice in Packet Tracer

- [Lab 02 — Router & Subnets](../labs/lab2-Routers&Subnets/2-router-ftp-http-lab.md): assign two `/26` networks and their gateways.
- [Lab 03 — Multi-Router NAT & DHCP](../labs/3-multi-router-nat-dhcp-lab.md): lease client settings at an internet edge.
- [Lab 04 — DHCP Relay](../labs/lab4-DHCP/4-dhcp_lab.md): trace DORA across a relay to a centralized server.

## Next
[VLANs →](07-vlans.md)
