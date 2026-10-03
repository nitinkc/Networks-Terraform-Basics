# Stage 13: Firewalls

!!! note "Key takeaways"
    - A firewall enforces policy on what traffic is allowed in/out
    - Filtering can be based on IP, port, protocol, or connection state
    - Firewalls exist at every layer: on a single host, at a router, or at a network's edge

## What a firewall actually does

A firewall inspects traffic against a set of **rules** and decides to
allow or deny it. Conceptually simple — the complexity is in how
granular and stateful those rules can be.

### A simple rule, in plain terms
> Allow inbound traffic on TCP port 443. Deny everything else inbound.
> Allow all outbound traffic.

This is a completely standard posture for a public web server: let
HTTPS in, block everything else from initiating contact, but let the
server itself freely make outbound requests (e.g., to a database or an
external API).

## Where firewalls live

| Location | Example |
|----------|---------|
| Host-based | Windows Defender Firewall, `iptables`/`ufw` on Linux — protects one machine |
| Router-based | Home router blocking unsolicited inbound connections by default |
| Network edge | A dedicated firewall appliance or cloud security group in front of an entire network/VPC |

## Stateless vs stateful filtering

- **Stateless** — evaluates each packet in isolation against the rule
  set, with no memory of prior packets
- **Stateful** — tracks active connections, and automatically allows
  return traffic for a connection that was legitimately initiated from
  the inside, without needing an explicit rule for the reply direction

Stateful is the overwhelmingly common approach today — it's why you
don't need a separate inbound rule just to let the *responses* to your
own outbound web requests back in.

## Cisco ACL reference (a basic filtering mechanism)

```
access-list 100 permit tcp any any eq 443
access-list 100 deny ip any any
interface gig0/0
 ip access-group 100 in
```

This is a simplified stateless example — it permits inbound HTTPS and
denies everything else on that interface, applied "in" (inbound
direction).

## Relationship to NAT (a common point of confusion)

[NAT and PAT](05-private-ip-nat.md) *incidentally* block unsolicited inbound connections,
because there's no existing translation-table entry for traffic nobody
inside the network initiated — but that's a side effect of NAT's
address-translation bookkeeping, not a security policy. A firewall is
an explicit, configurable policy layer; NAT's protective effect is
implicit and much less flexible (no way to say "allow this specific
inbound thing" without a separate feature like port forwarding).

!!! info "Cloud connection"
    Terraform can declare cloud firewall rules, but runtime verification is still required. A rule may target the wrong identity, tag, direction, or network, and load-balancer health checks often require their own permitted path.

## Next
[VPNs, Proxies & Load Balancers →](14-vpn-proxies-loadbalancers.md)
