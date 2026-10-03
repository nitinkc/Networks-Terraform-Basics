<!-- Abbreviation full-forms and concise definitions — auto-appended to every page via pymdownx.snippets auto_append.
     Renders as hover tooltips (content.tooltips must stay enabled in mkdocs.yml). -->

*[ACL]: Access Control List — an ordered set of permit/deny rules that filters traffic by addresses, protocols, and ports.
*[API]: Application Programming Interface — a defined contract through which software systems exchange requests and responses.
*[APIPA]: Automatic Private IP Addressing — a self-assigned 169.254.0.0/16 address used when an IPv4 host cannot obtain DHCP configuration.
*[ARP]: Address Resolution Protocol — resolves a local IPv4 address to the MAC address needed for Layer 2 delivery.
*[AS]: Autonomous System — a network or group of networks operated under one routing policy.
*[AWS]: Amazon Web Services — Amazon's public cloud computing platform.
*[BGP]: Border Gateway Protocol — a path-vector routing protocol used to exchange policy-controlled reachability between autonomous systems.
*[CIDR]: Classless Inter-Domain Routing — prefix notation that defines the network and host portions of an IP range.
*[CLI]: Command-Line Interface — a text-based interface for running commands and configuring a system.
*[CML]: Cisco Modeling Labs — Cisco's network simulation and emulation platform.
*[CSR]: Cloud Services Router — Cisco's virtual router product for cloud and virtualized environments.
*[DHCP]: Dynamic Host Configuration Protocol — automatically leases IP addressing, gateway, DNS, and other network settings to clients.
*[DNS]: Domain Name System — resolves domain names to IP addresses and stores other namespace records.
*[DORA]: Discover, Offer, Request, Acknowledge — the four-message exchange commonly used to obtain a DHCP lease.
*[FTP]: File Transfer Protocol — a TCP-based protocol that uses separate control and data channels to transfer files.
*[GCP]: Google Cloud Platform — Google's public cloud computing platform.
*[HCL]: HashiCorp Configuration Language — the declarative language commonly used to write Terraform configuration.
*[HTTP]: HyperText Transfer Protocol — an application-layer request/response protocol used by web clients and servers.
*[HTTPS]: HyperText Transfer Protocol Secure — HTTP carried over TLS to provide encryption, integrity, and server authentication.
*[IaC]: Infrastructure as Code — managing infrastructure through version-controlled declarative or procedural configuration.
*[IAM]: Identity and Access Management — controls which identities can perform which actions on which resources.
*[ICMP]: Internet Control Message Protocol — carries network diagnostics and control messages, including those used by ping.
*[IGW]: Internet Gateway — a logical gateway that provides a route between a private network and the internet.
*[IP]: Internet Protocol — provides logical addressing and packet delivery across interconnected networks.
*[IPsec]: Internet Protocol Security — a suite of protocols that authenticates and encrypts IP traffic, commonly for VPN tunnels.
*[LAN]: Local Area Network — a network covering a limited local area or broadcast domain.
*[LB]: Load Balancer — distributes connections or requests across multiple healthy backend systems.
*[MAC]: Media Access Control — the Layer 2 addressing mechanism used to identify network interfaces on a local link.
*[NAT]: Network Address Translation — rewrites IP addresses as traffic crosses a routed boundary.
*[NIC]: Network Interface Card — the physical or virtual interface that connects a host to a network.
*[OSI]: Open Systems Interconnection — the seven-layer conceptual model used to describe networking functions.
*[OSPF]: Open Shortest Path First — a link-state interior routing protocol that calculates paths using cost.
*[PAT]: Port Address Translation — allows many private flows to share one public IP by translating transport identifiers.
*[PoP]: Point of Presence — a physical location where a provider exposes network connectivity or services.
*[RFC]: Request for Comments — a publication series containing internet standards, protocols, and technical guidance.
*[SSH]: Secure Shell — an encrypted protocol for remote command-line access and administration.
*[SSL]: Secure Sockets Layer — the obsolete predecessor to TLS; the name is still used informally for certificates and encrypted web traffic.
*[TCP]: Transmission Control Protocol — a reliable, ordered, connection-oriented transport protocol.
*[TCP/IP]: Transmission Control Protocol / Internet Protocol — the practical layered protocol suite used by the internet.
*[TLS]: Transport Layer Security — encrypts traffic and provides integrity and peer authentication.
*[UDP]: User Datagram Protocol — a connectionless transport protocol with low overhead and no delivery or ordering guarantee.
*[VLAN]: Virtual Local Area Network — divides shared switching infrastructure into separate Layer 2 broadcast domains.
*[VM]: Virtual Machine — a software-defined computer running its own operating system on virtualized hardware.
*[VPC]: Virtual Private Cloud — a logically isolated, software-defined cloud networking domain.
*[VPN]: Virtual Private Network — an authenticated, encrypted tunnel that carries private traffic across an untrusted network.
*[VPCS]: Virtual PC Simulator — a lightweight host simulator used in network emulation labs.
*[WAN]: Wide Area Network — a network that connects geographically separated sites or upstream networks.

<!-- Important non-abbreviated terms from the glossary. The Markdown abbr extension also supports multi-word terms. -->

*[Data Link Layer]: OSI Layer 2 — provides local frame delivery using technologies such as Ethernet, MAC addressing, switching, ARP, and VLANs.
*[Default Gateway]: The router address a host uses as its next hop when a destination is outside the local subnet.
*[Firewall]: A policy-enforcement system that allows or denies network traffic using attributes such as direction, address, protocol, port, identity, and connection state.
*[Forward proxy]: An intermediary in front of clients that sends their requests to destination servers and can provide filtering, caching, or source hiding.
*[Frame]: A Layer 2 data unit containing local-link addressing and an encapsulated network-layer packet.
*[Internet Layer]: The TCP/IP layer responsible for logical addressing and routing packets across networks, primarily using IP.
*[IP Address]: A logical address assigned to a network interface and used to identify its location within an IP network.
*[Load Balancer]: A traffic-distribution system that selects healthy backend servers for incoming connections or application requests.
*[Network Layer]: OSI Layer 3 — provides logical addressing, routing, and packet forwarding between networks.
*[OSI Model]: A seven-layer conceptual model used to separate and explain networking responsibilities.
*[Packet]: A Layer 3 data unit containing an IP header and the encapsulated transport-layer payload.
*[Port]: A transport-layer identifier that directs TCP or UDP traffic to the intended application or service on a host.
*[Private IP]: An address from an RFC 1918 range that is reusable inside private networks and is not routed directly across the public internet.
*[Reverse proxy]: An intermediary in front of servers that receives client requests and forwards them to internal backends, often providing TLS termination, routing, caching, or rate limiting.
*[Router]: A Layer 3 device or service that chooses a next hop and forwards packets between different IP networks.
*[Stateful Firewall]: A firewall that tracks connection state and can automatically permit valid return traffic for an allowed session.
*[Stateless Firewall]: A firewall or packet filter that evaluates each packet independently without remembering earlier packets in the flow.
*[Subnet]: A contiguous IP prefix that defines which addresses are local to one Layer 3 network segment.
*[Switch]: A Layer 2 device that learns source MAC addresses and forwards Ethernet frames within a broadcast domain.
*[TCP/IP Model]: The practical four-layer model—application, transport, internet, and link—used to describe the internet protocol suite.
*[Transport Layer]: The layer that provides process-to-process communication using protocols such as TCP and UDP and identifies applications with ports.
