# Quiz 3 — Transport, DNS, and Web Traffic

Five questions covering TCP, UDP, ports, DNS, HTTPS, and TLS.

<!-- mkdocs-quiz intro -->

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

<!-- mkdocs-quiz results -->

[Previous: Addressing and routing](99-quiz-addressing-routing.md) · [Quiz home](99-quiz.md) · [Next: NAT and cloud](99-quiz-nat-cloud.md)
