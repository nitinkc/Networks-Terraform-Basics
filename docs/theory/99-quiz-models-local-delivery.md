# Quiz 1 — Models, Packets, and Local Delivery

Seven questions covering OSI, frames, IP addressing, gateways, ARP, switching, and routing.

<!-- mkdocs-quiz intro -->

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

<!-- mkdocs-quiz results -->

[Quiz home](99-quiz.md) · [Next: Addressing and routing](99-quiz-addressing-routing.md)
