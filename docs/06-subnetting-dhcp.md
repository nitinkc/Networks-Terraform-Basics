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

## ShopNow packet journey: plan the address space

ShopNow reserves non-overlapping ranges for the VPC, GKE nodes, Pods, Services, and any connected office network. For example, nodes might use `10.10.0.0/20`, Pods `10.20.0.0/16`, and Services `10.30.0.0/20`. The exact ranges are design choices; the important rule is that every routed prefix has an unambiguous owner and enough room to grow.

Terraform declares cloud subnet and secondary ranges. GCP supplies addresses to VM and GKE node interfaces through its managed network services, while Kubernetes IP address management assigns Pod and Service addresses. This resembles DHCP's goal of automated assignment, but Kubernetes Services do not obtain addresses through the DHCP DORA exchange.

## Next
[VLANs →](07-vlans.md)
