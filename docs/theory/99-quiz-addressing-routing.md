# Quiz 2 — Addressing, DHCP, VLANs, and Routing

Six questions covering CIDR, DHCP, VLANs, route selection, OSPF, and BGP.

<!-- mkdocs-quiz intro -->

<quiz>
What does a `/24` CIDR prefix indicate?

- [ ] The address contains 24 host bits
- [x] The first 24 bits identify the network prefix
- [ ] The subnet supports exactly 24 devices
- [ ] The address must be publicly routable

A `/24` leaves eight IPv4 host bits. Prefix length describes the network portion,
not whether the addresses are public or private.
</quiz>

<quiz>
Which sequence correctly represents the common DHCP lease exchange?

- [ ] Discover, Request, Offer, Acknowledge
- [ ] Offer, Discover, Acknowledge, Request
- [x] Discover, Offer, Request, Acknowledge
- [ ] Request, Discover, Offer, Acknowledge

The sequence is commonly remembered as DORA: Discover, Offer, Request,
Acknowledge.
</quiz>

<quiz>
What problem does a DHCP relay solve?

- [ ] It encrypts DHCP leases over the internet
- [x] It forwards client DHCP requests to a server on another subnet
- [ ] It translates private client addresses to a public address
- [ ] It replaces DNS for devices without hostnames

Initial DHCP discovery is broadcast-based. A relay such as `ip helper-address`
allows a centralized server to serve clients across a router.
</quiz>

<quiz>
What does a VLAN create?

- [ ] A new public IP address for every switch port
- [ ] An encrypted tunnel between two sites
- [x] A separate Layer 2 broadcast domain on shared switching infrastructure
- [ ] A dynamic route between autonomous systems

Different VLANs require Layer 3 routing to communicate with one another.
</quiz>

<quiz>
Which route is selected first when several routes match a destination?

- [ ] The route learned most recently
- [ ] The route with the shortest textual description
- [x] The route with the longest, most-specific matching prefix
- [ ] The default route regardless of other entries

Routers perform longest-prefix matching. A default route is used only when no
more-specific route matches.
</quiz>

<quiz>
Which statement correctly distinguishes OSPF and BGP?

- [ ] OSPF translates addresses; BGP assigns addresses
- [x] OSPF discovers internal paths, while BGP exchanges policy-controlled reachability between autonomous systems
- [ ] OSPF uses TCP 179, while BGP uses raw IP protocol 89
- [ ] OSPF is only for cloud networks, while BGP is only for physical networks

OSPF is a link-state interior gateway protocol using IP protocol 89. BGP is a
path-vector protocol that establishes sessions over TCP 179.
</quiz>

<!-- mkdocs-quiz results -->

[Previous: Models and local delivery](99-quiz-models-local-delivery.md) · [Quiz home](99-quiz.md) · [Next: Transport and web](99-quiz-transport-web.md)
