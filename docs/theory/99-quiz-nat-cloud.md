# Quiz 4 — NAT, Policy, Proxies, and Cloud Networking

Ten questions covering NAT, firewall policy, proxies, load balancing, VPNs, BGP, and VPCs.

<!-- mkdocs-quiz intro -->

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

[Previous: Transport and web](99-quiz-transport-web.md) · [Quiz home](99-quiz.md)
