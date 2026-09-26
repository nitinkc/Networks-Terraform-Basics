# 4. Private IPs & NAT

!!! note "Key takeaways"
    - Private IP ranges are reserved, non-routable-on-the-internet blocks reused by every home/office network
    - NAT (usually PAT/"overload") lets many private IPs share one public IP
    - This is the direct fix for IPv4 exhaustion (page 2)

## Private IP ranges (memorize these three)

| Range | CIDR | Common use |
|-------|------|-------------|
| 10.0.0.0 – 10.255.255.255 | 10.0.0.0/8 | Large enterprise networks |
| 172.16.0.0 – 172.31.255.255 | 172.16.0.0/12 | Medium networks, some cloud VPCs |
| 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 | Home routers, small offices |

These addresses are **not globally unique** — your home network's
`192.168.1.10` and your neighbor's `192.168.1.10` are both valid and
don't conflict, because neither is ever routed on the public internet
directly.

## NAT (Network Address Translation)

Your router has exactly one public IP from your ISP, but every device
in your house has its own private IP. NAT is what lets all of them
share that one public IP to reach the internet.

### How it works (PAT / "NAT overload" — the common case)
1. PC0 (`192.168.1.10:54211`) sends a packet to `8.8.8.8:443`
2. The router rewrites the source to its own public IP and a new port:
   `203.0.113.5:61234 → 8.8.8.8:443`
3. The router remembers this mapping in a **NAT translation table**
4. When the reply comes back to `203.0.113.5:61234`, the router looks up
   the table, rewrites it back to `192.168.1.10:54211`, and forwards it
   to PC0

```
Inside (private)              NAT table                Outside (public)
192.168.1.10:54211   <--->  203.0.113.5:61234   <--->   8.8.8.8:443
192.168.1.11:50876   <--->  203.0.113.5:61235   <--->   8.8.8.8:443
```

Both PCs share the single public IP `203.0.113.5` — the **port** is
what keeps their traffic distinguishable, which is why this variant is
called PAT (**Port** Address Translation), even though "NAT" is the
term used colloquially for all of this.

### Why this matters practically
- It's *the* reason IPv4 hasn't completely collapsed despite address
  exhaustion — most of the world's devices don't need a public IP at
  all, only a translated path to one
- It incidentally provides a mild security benefit: a device sitting
  behind NAT can't be directly addressed from the internet unless the
  router is explicitly configured to forward a port to it (port
  forwarding) — this is *not* the same as a firewall, but it has a
  similar practical effect for inbound connections

### Cisco config reference (matches your lab)
```
access-list 1 permit 192.168.1.0 0.0.0.255
ip nat inside source list 1 interface gig0/1 overload
interface gig0/0
 ip nat inside
interface gig0/1
 ip nat outside
```
`overload` is the keyword that specifically enables PAT (many-to-one);
without it, NAT would only support a strict one-to-one private-to-public
mapping, which doesn't solve the address-exhaustion problem at all.

## Next
[Subnetting & DHCP →](05-subnetting-dhcp.md)
