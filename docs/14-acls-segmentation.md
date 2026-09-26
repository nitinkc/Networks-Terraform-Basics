# ACLs and Network Segmentation

> **Key takeaways:** Segmentation creates boundaries; routing permits reachability across them; ACLs selectively restrict that reachability. ACL order, direction, placement, and the implicit deny determine the result.

## Segmentation and policy are different

A VLAN creates a Layer 2 broadcast domain. A subnet defines a Layer 3 prefix. They are commonly paired, but neither alone expresses a complete security policy. Once a router or Layer 3 switch provides inter-VLAN routing, traffic can cross unless a policy blocks it.

Typical zones include user networks, server networks, management networks, guest networks, and a DMZ. Good segmentation limits broadcast scope, reduces failure impact, and creates clear policy enforcement points.

## Standard and extended ACLs

- **Standard ACL:** matches source IPv4 address only. Place it near the destination to avoid blocking that source from unrelated destinations.
- **Extended ACL:** can match protocol, source, destination, and ports. Place it near the source to reject unwanted traffic early.

An IOS ACL is an ordered list. The router checks entries from top to bottom, applies the first match, and stops. Every ACL ends with an invisible `deny any` unless traffic is explicitly permitted.

## Wildcard masks

Cisco IPv4 ACLs use wildcard masks:

- `0` bit: must match.
- `1` bit: ignore.

For a contiguous subnet, subtract the subnet mask from `255.255.255.255`:

| Prefix | Subnet mask | Wildcard |
|---|---|---|
| `/24` | `255.255.255.0` | `0.0.0.255` |
| `/26` | `255.255.255.192` | `0.0.0.63` |
| `/30` | `255.255.255.252` | `0.0.0.3` |

`host 10.1.50.10` is shorthand for `10.1.50.10 0.0.0.0`; `any` matches all addresses.

## Direction and placement

An ACL is applied from the router interface's perspective:

- **Inbound:** evaluated as a packet enters the interface, before the routing decision.
- **Outbound:** evaluated after routing, before the packet leaves the interface.

Trace the packet and name the exact ingress and egress interfaces before choosing a direction. Applying the correct ACL to the wrong interface or direction is equivalent to not enforcing the intended policy.

## Ports and protocols

Extended ACLs distinguish protocols and destination services. For example, allowing TCP destination port 80 permits HTTP but not ICMP echo or TCP port 22. The port number alone is not enough: specify TCP or UDP as required.

Classic router ACL behavior is primarily stateless packet filtering. A permit for a request does not automatically describe a complete stateful security policy. Platform-specific reflexive ACLs, zone firewalls, or cloud firewalls can add connection tracking.

## Policy design method

1. Write a source-to-destination matrix in plain language.
2. Convert each allowed or denied flow into protocol and port terms.
3. Order specific exceptions before broad rules.
4. Add explicit logging or deny entries when the platform supports useful diagnostics.
5. Apply the ACL to the chosen interface and direction.
6. Test both permitted and prohibited flows.
7. Inspect match counters to prove the expected rule handled the packet.

## Example reasoning

For “HR may use HTTP to the corporate server but may not use SSH”:

- Source: HR subnet.
- Destination: corporate server host.
- Permit: TCP destination port 80.
- Deny: TCP destination port 22.
- Consider other traffic explicitly; do not rely on an accidental implicit deny.

## Common failure patterns

- A broad permit appears before a specific deny.
- The ACL is built but never applied.
- Source and destination are reversed.
- The subnet mask is used where a wildcard mask is required.
- The ACL is attached in the wrong direction.
- Testing only an allowed flow hides an ineffective deny rule.
- DNS, DHCP, or return traffic needed by the application was omitted.

## Related theory and labs

- [VLANs](08-vlans.md)
- [TCP and UDP](09-tcp-udp.md)
- [Firewalls](11-firewalls.md)
- [VLAN and ACL lab](labs/8-lan_acl_lab.md)
- [Packet Tracer GCP equivalent](labs/9-networking_gcp_equivalent_lab.md)
