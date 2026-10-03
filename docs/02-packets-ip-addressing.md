# Stage 2: Packets & IP Addressing

!!! note "Key takeaways"
    - Data is chopped into packets so many flows can share a link fairly and recover from loss cheaply
    - Every packet has a header (control info) and a payload (actual data)
    - IPv4 = 32-bit (~4.3B addresses, exhausted); IPv6 = 128-bit (practically inexhaustible)
    - Routers move packets between networks by consulting a routing table

## Why packets, not one continuous stream?

If you sent a whole file as one unbroken transmission, one bit error
partway through would mean resending the entire thing, and no other
device could use the link until you finished. Breaking data into
packets means:

- Loss/corruption only costs you one small packet, not the whole transfer
- Multiple flows can interleave on the same physical link (fairness)
- Packets can take different paths and arrive out of order — the
  transport layer (TCP) reassembles them correctly

## Packet anatomy

```
+------------------+------------------------+
|      Header      |        Payload         |
+------------------+------------------------+
 source/dest IP,        the actual data
 protocol, TTL, etc.
```

The header is what routers and switches actually read to decide what to
do with the packet — they generally never look at the payload (that's
also a security/privacy boundary: a router doesn't need to know *what*
you're sending, only *where*).

## IP addressing

An IP address identifies a device's interface on a network — not the
device itself (a device with two network interfaces has two IPs).

### IPv4
- 32-bit, written as 4 decimal octets: `192.168.1.10`
- Total space: ~4.3 billion addresses
- **Exhausted** as a public-address space years ago — this is *the*
  reason [NAT and private IP ranges](05-private-ip-nat.md) exist

### IPv6
- 128-bit, written in hex groups: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`
- Address space so large that NAT is no longer functionally necessary
  (though it's sometimes still used for other reasons)
- Adoption has been slow because IPv4 and IPv6 aren't directly
  interoperable — this is a common "why hasn't the internet just
  switched" interview tangent

## Subnet Mask and CIDR Notation

An IPv4 address consists of 32 bits divided into four 8-bit blocks called octets.
A subnet mask is also a 32-bit number that runs parallel to an IP address. Subnet masks tells about the network & host 
portion of the IP Address
* Binary `1`s in the subnet mask represent the **Network Portion**.
* Binary `0`s in the subnet mask represent the **Host Portion**.

When a router or computer evaluates an IP address against its subnet mask, it performs a bitwise **logical AND**
operation to determine the network ID.

### Example 1: 192.168.1.0 with Subnet Mask 255.255.255.0 (/24)

This configuration is common in home networks and small office environments (traditionally associated with Class C networks).

#### Decimal Notation
* IP Address: `192.168.1.0`
* Subnet Mask: `255.255.255.0`

#### Binary Alignment
* IP Address:  `11000000.10101000.00000001.00000000`
* Subnet Mask: `11111111.11111111.11111111.00000000`

#### Structure Analysis
* **Network Portion (first 3 octets):** `192.168.1` (represented by 24 contiguous binary 1s)
* **Host Portion (last octet):** `.0` (represented by 8 binary 0s)

In this subnet, every device on the local network shares the prefix `192.168.1.x`, allowing up to 254 unique assignable
host addresses (excluding network and broadcast addresses).

## Summary Comparison

| IP Address | Subnet Mask | CIDR Prefix | Network Portion | Host Portion | Typical Use Case |
|---|---|---|---|---|---|
| `192.168.1.0` | `255.255.255.0` | `/24` | `192.168.1` | `.0` | Small networks / Home routers |
| `172.16.1.0` | `255.255.0.0` | `/16` | `172.16` | `.1.0` | Medium-to-large business networks |
| `10.0.1.0` | `255.0.0.0` | `/8` | `10` | `.0.1.0` | Large enterprises / Datacenters |


## Routers and routing tables

A router's job: look at a packet's **destination IP**, consult its
**routing table**, and forward the packet out the correct interface
toward that destination — one hop at a time.

A simplified routing table entry looks like:

| Destination network | Next hop | Interface |
|------------------------|-----------|-----------|
| 192.168.2.0/24 | directly connected | Gig0/1 |
| 0.0.0.0/0 (default route) | 203.0.113.2 | Gig0/0 |

The `0.0.0.0/0` entry is the **default route** — "anything I don't have
a more specific match for, send here." This is how your home router
gets *any* packet destined for the internet to your ISP without needing
a table entry for every possible destination on Earth.

### TTL (Time To Live)
Every IP packet carries a TTL field that decrements by 1 at each router
hop. When it hits 0, the packet is dropped and an error is sent back.
This exists purely to prevent packets from looping forever if a routing
loop occurs — it's also exactly what `traceroute` exploits to map a
path (it sends packets with deliberately increasing TTLs to force each
router along the way to respond).

!!! info "Cloud connection"
    Cloud designs must reserve non-overlapping CIDRs for VPC subnets and, where applicable, Kubernetes Pods and Services. A load balancer, node, Pod, and Service may each use a different address because they are separate network endpoints or forwarding stages.

## Next
[MAC Addresses & ARP →](03-mac-arp.md)
