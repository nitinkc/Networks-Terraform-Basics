# Networking Knowledge Check

Use this multiple-choice quiz after completing the theory sequence. Each question
has one correct answer and provides an explanation after submission. Results are
stored locally in your browser by the `mkdocs-quiz` plugin.

<!-- mkdocs-quiz intro -->

## Models, packets, and local delivery

<quiz>
Which description best matches the OSI model?

- [ ] A routing protocol used by internet service providers
- [x] A seven-layer conceptual model for separating networking responsibilities
- [ ] A four-step process for obtaining an IP address
- [ ] A cloud-specific model for VPC design

The OSI model is a conceptual seven-layer framework. The practical internet
protocol suite is commonly described with the four-layer TCP/IP model.
</quiz>

<quiz>
What is a frame?

- [ ] An application request before transport encapsulation
- [ ] A route selected by a router
- [x] A Layer 2 unit containing local-link addressing and an encapsulated packet
- [ ] A DNS response containing several records

Ethernet carries frames on a local link. The frame normally contains an IP
packet as its payload.
</quiz>

<quiz>
What is the primary purpose of an IP address?

- [ ] To identify an application process on a host
- [x] To provide a logical address for an interface within an IP network
- [ ] To identify a switch port permanently
- [ ] To encrypt traffic between two routers

IP addresses support logical addressing and routing. Ports identify application
endpoints, while MAC addresses support local Layer 2 delivery.
</quiz>

<quiz>
A host wants to send traffic to an address outside its subnet. Which local device does it send the frame to?

- [ ] The authoritative DNS server
- [ ] The DHCP server
- [x] Its default gateway
- [ ] The destination host's switch port

The host sends remote traffic to its default gateway. ARP is used to resolve the
gateway's local MAC address—not the remote destination's MAC address.
</quiz>

<quiz>
What does ARP resolve on an IPv4 LAN?

- [ ] A hostname to an IP address
- [x] A local IPv4 address to a MAC address
- [ ] A port number to an application
- [ ] A public address to a private address

ARP operates within a local broadcast domain and does not cross routers.
</quiz>

<quiz>
How does an Ethernet switch normally decide where to forward a frame?

- [ ] By looking up the destination IP in a routing table
- [ ] By querying DNS for the destination hostname
- [x] By looking up the destination MAC address in its MAC table
- [ ] By translating the source address with NAT

A Layer 2 switch learns source MAC addresses and forwards frames using its MAC
address table.
</quiz>

<quiz>
What is the main job of a router?

- [ ] Assign application ports to processes
- [ ] Resolve local IPv4 addresses to MAC addresses
- [x] Forward packets between networks using destination IP routes
- [ ] Encrypt every packet crossing a switch

Routers make Layer 3 forwarding decisions and separate broadcast domains.
</quiz>

## Addressing, DHCP, VLANs, and routing

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

## Transport, DNS, and web traffic

<quiz>
Which property is provided by TCP but not by UDP?

- [ ] Application port numbers
- [ ] IP addressing
- [x] Reliable, ordered delivery with retransmission
- [ ] Name resolution

Both TCP and UDP use ports, but TCP establishes a connection and provides
ordering, acknowledgements, and retransmission.
</quiz>

<quiz>
What does a destination port identify?

- [ ] The physical switch port used by the frame
- [x] The intended application or service on the destination host
- [ ] The next router in the path
- [ ] The VLAN assigned to the source device

An IP address identifies a network interface; a transport port identifies the
application endpoint using that address.
</quiz>

<quiz>
What does DNS primarily provide?

- [ ] Automatic assignment of subnet masks and gateways
- [x] Resolution of names to addresses and other namespace records
- [ ] Reliable retransmission of lost application data
- [ ] Encryption of HTTP requests

DNS resolution identifies an endpoint. Routing, policy, and a listening
application must still make that endpoint reachable and usable.
</quiz>

<quiz>
Which statement about HTTPS is correct?

- [ ] HTTPS is UDP-based HTTP without certificates
- [ ] HTTPS replaces DNS with certificate lookup
- [x] HTTPS carries HTTP over TLS, commonly on TCP port 443
- [ ] HTTPS encrypts only the destination IP address

TLS protects the application data and provides confidentiality, integrity, and
peer authentication. It does not hide normal IP routing information.
</quiz>

<quiz>
Which three guarantees are associated with TLS?

- [ ] Address assignment, routing, and translation
- [ ] Availability, load balancing, and caching
- [x] Confidentiality, integrity, and authentication
- [ ] Ordering, retransmission, and congestion control

TCP provides transport behavior such as ordering and retransmission. TLS protects
the application exchange carried over that transport.
</quiz>

## NAT, policy, proxies, and cloud networking

<quiz>
Why can many private clients share one public IP when PAT is enabled?

- [ ] Every client receives the same MAC address
- [x] The translation table distinguishes flows using translated transport identifiers
- [ ] DNS assigns a different public hostname to every packet
- [ ] The switch creates a separate VLAN for every connection

PAT combines address translation with port or protocol identifiers so multiple
simultaneous flows can share one public address.
</quiz>

<quiz>
What is static PAT, commonly called port forwarding, used for?

- [ ] Automatically assigning private IP addresses to clients
- [x] Mapping a public protocol/port to a specific private service
- [ ] Advertising routes between autonomous systems
- [ ] Resolving an internal service name

For example, a public TCP port can be mapped to TCP 80 on an internal web server.
</quiz>

<quiz>
Why is NAT not a replacement for a firewall?

- [ ] NAT cannot process IPv4 packets
- [ ] Firewalls only operate at Layer 2
- [x] NAT translates addressing, while a firewall explicitly enforces traffic policy
- [ ] NAT always permits all unsolicited inbound traffic

Translation state can incidentally limit inbound reachability, but it is not a
complete or intentional security policy.
</quiz>

<quiz>
What is the key difference between a stateful and stateless firewall?

- [ ] A stateful firewall can only filter MAC addresses
- [ ] A stateless firewall automatically permits all replies
- [x] A stateful firewall tracks connections; a stateless filter evaluates packets independently
- [ ] A stateless firewall is always implemented in hardware

Connection tracking allows a stateful firewall to recognize valid return traffic
for an allowed session.
</quiz>

<quiz>
Where does a forward proxy sit?

- [x] In front of clients, forwarding their requests outward
- [ ] In front of servers, distributing requests among backends
- [ ] Between two routers to exchange BGP routes
- [ ] Inside a switch to create VLANs

A reverse proxy sits in front of servers. A forward proxy represents clients to
the destinations they access.
</quiz>

<quiz>
What is a reverse proxy commonly used for?

- [ ] Assigning IP addresses with DHCP
- [ ] Resolving MAC addresses with ARP
- [x] Receiving client requests and forwarding them to internal servers
- [ ] Translating all private outbound traffic with PAT

Reverse proxies can also terminate TLS, route by hostname or path, cache content,
and enforce application-layer controls.
</quiz>

<quiz>
What is the primary responsibility of a load balancer?

- [ ] Encrypt every packet crossing a WAN
- [ ] Exchange routes between autonomous systems
- [x] Distribute traffic across healthy backend systems
- [ ] Convert domain names into IP addresses

Layer 4 load balancers distribute connections using transport information. Layer
7 load balancers can additionally inspect application data such as HTTP paths.
</quiz>

<quiz>
What is the relationship between an IPsec VPN tunnel and BGP in a hybrid network?

- [ ] BGP encrypts traffic and IPsec assigns hostnames
- [x] IPsec protects the tunnel, while BGP exchanges the prefixes routed through it
- [ ] IPsec replaces all routes with a default route
- [ ] BGP translates private addresses to public addresses

Tunnel establishment and route exchange are separate control-plane conditions;
either can succeed while the other is misconfigured.
</quiz>

<quiz>
What does Cloud NAT normally provide for private cloud workloads?

- [ ] Public inbound access to every private service
- [x] Outbound address translation without assigning each workload a public IP
- [ ] Layer 7 API authentication and quotas
- [ ] Private DNS resolution between Kubernetes Services

Cloud NAT is an egress mechanism. Public or private application ingress is
provided through separate endpoints and policy.
</quiz>

<quiz>
Which statement best describes a VPC?

- [ ] A physical Ethernet switch installed in a cloud region
- [ ] A VPN tunnel that always connects to an office
- [x] A logically isolated software-defined cloud networking domain
- [ ] A DNS record that points to a load balancer

A VPC contains cloud subnets, routes, and policy relationships, but its
implementation is distributed rather than equivalent to one physical router or
switch.
</quiz>

<!-- mkdocs-quiz results -->

## Review by topic

If a section was difficult, revisit the corresponding theory:

| Quiz topic | Theory review |
|:-----------|:--------------|
| Models, packets, frames | [Networking Models](01-networking-models.md), [Packets & IP Addressing](02-packets-ip-addressing.md) |
| ARP, switches, routers | [MAC Addresses & ARP](03-mac-arp.md), [Switches vs Routers](04-switches-routers.md) |
| NAT and private addressing | [Private IPs, NAT & PAT](05-private-ip-nat.md) |
| Subnets and DHCP | [Subnetting & DHCP](06-subnetting-dhcp.md) |
| VLANs and routing | [VLANs](07-vlans.md), [Static Routing, OSPF & BGP](08-routing-protocols.md) |
| TCP, UDP, DNS, and ports | [TCP vs UDP](09-tcp-udp.md), [DNS & Ports](10-dns-and-ports.md) |
| HTTP and TLS | [HTTP/HTTPS & TLS](11-http-https-tls.md) |
| ACLs and firewalls | [ACLs & Segmentation](12-acls-segmentation.md), [Firewalls](13-firewalls.md) |
| VPNs, proxies, and load balancing | [VPNs, Proxies & Load Balancers](14-vpn-proxies-loadbalancers.md) |
| Cloud networking | [Cloud & Hybrid Networking](15-cloud-hybrid-networking.md) |
