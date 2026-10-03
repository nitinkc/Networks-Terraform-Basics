# Stage 5: Private IPs, NAT & PAT

!!! note "Key takeaways"
    - Private IP ranges are reusable inside local networks and are not routed across the public internet.
    - NAT translates addresses between an inside network and an outside network.
    - PAT (NAT overload) also translates Layer 4 port numbers, allowing many private hosts to share one public IPv4 address.
    - Static PAT, commonly called port forwarding, makes one service on an inside host reachable from outside.
    - NAT requires correct routing; it does not replace routes, ACLs, or a stateful firewall.

## Private IP ranges (memorize these three)

| Range                         | CIDR           | Common use                       |
|:------------------------------|:---------------|:---------------------------------|
| 10.0.0.0 – 10.255.255.255     | 10.0.0.0/8     | Large enterprise networks        |
| 172.16.0.0 – 172.31.255.255   | 172.16.0.0/12  | Medium networks, some cloud VPCs |
| 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 | Home routers, small offices      |

These addresses are **not globally unique**. Your home network's
`192.168.1.10` and your neighbor's `192.168.1.10` are both valid because neither
address is advertised directly on the public internet. A border router must
translate the private source address before traffic can cross a public network.

## NAT (Network Address Translation)

NAT **changes an IP address** as a packet crosses a NAT-enabled router. A common
example is **_replacing a private source address with a public source address for
outbound internet traffic_**. The router records the translation so that return
traffic can be sent back to the correct inside host.

NAT is an umbrella term. It includes static NAT, dynamic NAT, PAT, and static
PAT/port forwarding.

## Cisco NAT terminology

Cisco describes a translated flow using four address terms:

| Term               | Meaning                                                          | Lab example    |
|:-------------------|:-----------------------------------------------------------------|:---------------|
| **Inside local**   | Address assigned to an inside host as seen on the inside network | `192.168.1.10` |
| **Inside global**  | Address representing an inside host to the outside network       | `203.0.113.1`  |
| **Outside local**  | Address of an outside host as seen by the inside network         | `198.51.100.2` |
| **Outside global** | Actual address of the outside host                               | `198.51.100.2` |

In this lab, the outside local and outside global addresses are identical
because Router0 does not translate outside addresses.

!!! tip "How to read the terms"
    **Inside/outside** describes where the host belongs. **Local/global** describes which version of its address is being discussed.

## NAT types

| NAT type                         | Mapping                                                                | Main use                                                      |
|:---------------------------------|:-----------------------------------------------------------------------|:--------------------------------------------------------------|
| **Static NAT**                   | One inside local address to one inside global address                  | Give an inside device a permanent public identity             |
| **Dynamic NAT**                  | Inside addresses temporarily use addresses from a public pool          | Support several hosts with a limited pool of public addresses |
| **PAT / NAT overload**           | Many inside addresses share one public address, distinguished by ports | Outbound internet access for a LAN                            |
| **Static PAT / port forwarding** | One public IP and port maps to one private IP and port                 | Publish a specific internal service                           |

Dynamic NAT does not necessarily let every inside host connect at once. When all
addresses in its pool are in use, additional translations cannot be created.
PAT avoids that limitation for most client traffic by distinguishing sessions
with transport-layer port numbers.

## PAT (Port Address Translation)

PAT is the form of NAT used by most homes and offices. It is also called **NAT
overload** or **many-to-one NAT**.

Suppose two inside PCs connect to the same public web server:

```text
Inside local                 Inside global                Outside global
192.168.1.10:54211   <-->    203.0.113.1:1025    <-->    198.51.100.2:80 (Server)
192.168.1.11:50876   <-->    203.0.113.1:1026    <-->    198.51.100.2:80 (Server)
```

Both sessions use the same inside global IP, `203.0.113.1`. Router0 assigns a
different translated source port to each session, so it can identify which
inside host should receive each reply.

### Outbound PAT packet flow

1. PC0 sends a packet from `192.168.1.10:54211` to `198.51.100.2:80`.
2. The packet enters Router0 through an interface marked `ip nat inside`.
3. The NAT ACL identifies `192.168.1.10` as an address eligible for translation.
4. Router0 changes the source to an available tuple such as `203.0.113.1:1025`.
5. Router0 stores the mapping in its NAT translation table and forwards the packet through the outside interface.
6. The reply arrives for `203.0.113.1:1025`; Router0 uses the table to restore destination `192.168.1.10:54211`.

For TCP and UDP, PAT normally distinguishes sessions with port numbers. For
ICMP traffic, the translation table can use an ICMP identifier instead.

## PAT configuration used in the lab

```text
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 ip nat inside

interface GigabitEthernet0/1
 ip address 203.0.113.1 255.255.255.252
 ip nat outside

access-list 10 permit 192.168.1.0 0.0.0.255
ip nat inside source list 10 interface GigabitEthernet0/1 overload

ip route 0.0.0.0 0.0.0.0 203.0.113.2
```

Each part has a separate purpose:

- `ip nat inside` and `ip nat outside` define the NAT boundary. They do not enable translation by themselves.
- ACL 10 identifies the **source addresses to translate**. In this command, it is a NAT classification ACL, not an ACL applied to an interface for packet filtering.
- `interface GigabitEthernet0/1` tells Router0 to use its WAN interface address as the inside global address.
- `overload` enables many-to-one PAT by allowing multiple translations to share that address.
- The default route tells Router0 where outside destinations should be forwarded. NAT does not create the route.

!!! warning "NAT ACL versus filtering ACL"
    `access-list 10 permit 192.168.1.0 0.0.0.255` selects traffic for translation because it is referenced by the NAT command. It does not automatically permit or deny traffic on an interface. An ACL filters packets only when it is applied with a command such as `ip access-group`.

## Static PAT (port forwarding)

Outbound PAT creates temporary translations in response to connections started
from inside. An outside client cannot use those temporary entries to initiate an
unrelated connection to an inside server.

To publish the lab's internal web server, configure a permanent TCP mapping:

```text
ip nat inside source static tcp 192.168.1.100 80 203.0.113.1 8080
```

An outside client then opens:

```text
http://203.0.113.1:8080
```

Router0 translates destination `203.0.113.1:8080` to
`192.168.1.100:80`. The public and private port numbers do not have to be the
same. This makes it possible to publish several internal services through one
public IP, provided each outside port is unique.

Static PAT is different from static one-to-one NAT:

```text
ip nat inside source static 192.168.1.100 203.0.113.10
```

The one-to-one form maps the entire public address to the internal host; the
static PAT form maps only the specified protocol and port.

## Verifying NAT and PAT in Packet Tracer

Generate traffic first, and then inspect Router0:

```text
show ip nat translations
show ip nat statistics
```

`show ip nat translations` displays active mappings. A PAT entry includes a
protocol and port or identifier, while a static port-forward entry remains
configured even when no client session is active.

`show ip nat statistics` shows the inside and outside interfaces, active and
configured translations, hits, misses, and the rules used to create mappings.

To remove dynamic sessions before repeating a test:

```text
clear ip nat translation *
```

The static configuration is not removed by this command.

In Packet Tracer **Simulation Mode**, inspect the packet before and after it
crosses Router0. On an outbound flow, the private source IP and source port
should change on the outside interface. On the reply, the public destination IP
and translated port should change back to the original inside values.

## Troubleshooting checklist

If PAT or port forwarding does not work, verify these items in order:

1. **Host addressing:** Each host has the correct IP, mask, and default gateway.
2. **Interface state:** Router interfaces are addressed, connected, and `no shutdown` has been configured.
3. **NAT direction:** The LAN interface is `ip nat inside`; the WAN interface is `ip nat outside`.
4. **NAT ACL:** The source subnet and wildcard mask match the inside clients.
5. **Overload command:** The NAT rule references the correct ACL and WAN interface and includes `overload` for many-to-one PAT.
6. **Routing:** Router0 has a route toward the outside network, and return traffic can reach Router0's public address.
7. **Service and port:** For static PAT, the internal server service is enabled and the outside client uses the configured public port.
8. **Translation table:** Generate traffic, then check `show ip nat translations` and `show ip nat statistics` for entries, hits, and misses.
9. **Filtering ACLs:** Confirm that no separately applied interface ACL blocks the traffic before or after translation.

!!! note "NAT is not a firewall"
    NAT changes addressing and keeps translation state. Although ordinary outbound PAT makes unsolicited inbound connections difficult, security policy should still be enforced with ACLs or a stateful firewall.

!!! info "Cloud connection"
    Cloud NAT normally provides outbound translation for private workloads; it does not publish an inbound application. Public ingress is usually provided separately by a load balancer or another explicitly exposed endpoint.

## Next
[Subnetting & DHCP →](06-subnetting-dhcp.md)
