# Stage 7: VLANs

!!! note "Key takeaways"
    - A VLAN splits **one physical switch** into multiple logically separate networks
    - Devices in different VLANs can't talk to each other without going through a router (or Layer 3 switch)
    - Trunk ports carry multiple VLANs' traffic over a single physical link, tagged with 802.1Q

## The problem VLANs solve

Physically, all your devices might be plugged into the same switch. But
maybe you want the HR department's traffic completely isolated from
Engineering's, without running separate physical cabling and separate
switches for each department. VLANs let you carve one physical switch
into multiple independent broadcast domains — logically separate
networks sharing the same physical hardware.

## How it works

1. Each switch port is assigned to a **VLAN ID** (e.g., VLAN 10 for HR,
   VLAN 20 for Engineering)
2. Devices in VLAN 10 can freely reach each other through the switch —
   ARP broadcasts, everything — as if VLAN 20 didn't exist
3. Devices in VLAN 10 **cannot** reach devices in VLAN 20 through the
   switch alone — they're separate broadcast domains, exactly like
   being on physically separate switches
4. To let VLAN 10 and VLAN 20 talk at all, you need a router (or a
   Layer 3 switch) to route between them — this is called
   **inter-VLAN routing**

```
Switch ports 1-8   → VLAN 10 (HR)
Switch ports 9-16  → VLAN 20 (Engineering)
```

Note the direct parallel to the relationship described in [Switches vs Routers](04-switches-routers.md):
a VLAN *is* essentially a subnet boundary implemented at the switch
level rather than by physically separate hardware.

## Trunk ports & 802.1Q tagging

If you have multiple switches, each carrying multiple VLANs, you don't
want a separate physical cable per VLAN between switches. A **trunk
port** carries traffic for *multiple* VLANs over one physical link, with
each frame tagged (via the **802.1Q** standard) to say which VLAN it
belongs to.

```
Switch A (VLAN 10 + 20) ---[trunk: carries both, tagged]--- Switch B (VLAN 10 + 20)
```

Regular ports connecting to end devices (a PC, a printer) are called
**access ports** — they belong to exactly one VLAN and the device on
the other end has no idea VLANs even exist; tagging only happens
between switches (or to a router) on trunk links.

## Cisco config reference

```
vlan 10
 name HR
vlan 20
 name Engineering

interface fastEthernet 0/1
 switchport mode access
 switchport access vlan 10

interface gig0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20
```

## Why this matters practically

- **Security/segmentation** without extra hardware — isolate guest
  Wi-Fi, IoT devices, or departments from your main network on the same
  physical switches
- **Reduced broadcast traffic** — smaller broadcast domains mean less
  noise per segment, which matters at scale
- Nearly every enterprise network and every cloud provider's virtual
  networking (AWS VPC subnets, for instance) is conceptually built on
  this same idea of logically-separated segments sharing physical
  infrastructure

!!! info "Cloud connection"
    A VPC subnet and a Kubernetes namespace are not VLANs. They can support similar organizational goals, but isolation in cloud and Kubernetes environments comes from routing and explicit firewall or NetworkPolicy rules—not from the namespace name alone.

## Practice in Packet Tracer

- [Lab 08 — VLANs & ACLs](../labs/08-vlans-acls/index.md): configure access ports, an 802.1Q trunk, and router-on-a-stick.
- [Lab 09 — GCP Architecture Equivalent](../labs/09-gcp-architecture-equivalent/index.md): use VLAN-backed tiers as a physical analogy for cloud subnets.

## Next
[Static Routing, OSPF & BGP →](08-routing-protocols.md)
