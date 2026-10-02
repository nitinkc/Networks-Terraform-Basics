# Stage 11: HTTP/HTTPS & TLS

!!! note "Key takeaways"
    - HTTP is plaintext request/response over TCP; HTTPS adds TLS encryption on top
    - TLS provides confidentiality, integrity, and authentication
    - The TLS handshake happens once per connection, then symmetric encryption takes over for speed

## HTTP (HyperText Transfer Protocol)

A request/response protocol between clients and servers, running over
TCP (port 80 by default).

### Methods
| Method | Purpose |
|--------|---------|
| GET | Fetch data |
| POST | Submit/create data |
| PUT | Replace a resource entirely |
| PATCH | Partially update a resource |
| DELETE | Remove a resource |

### A request/response, structurally
```
GET /index.html HTTP/1.1
Host: example.com
User-Agent: ...

(optional body)
```
```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1234

<html>...</html>
```

### Status code ranges (worth having memorized)
| Range | Meaning |
|-------|---------|
| 1xx | Informational |
| 2xx | Success (200 OK, 201 Created) |
| 3xx | Redirection (301 Moved, 304 Not Modified) |
| 4xx | Client error (400 Bad Request, 404 Not Found, 401/403 Auth) |
| 5xx | Server error (500 Internal Server Error, 503 Unavailable) |

## HTTPS = HTTP + TLS

HTTPS is not a separate protocol from HTTP — it's HTTP running inside a
TLS-encrypted tunnel, over port 443 by default.

## TLS (Transport Layer Security)

TLS provides three specific guarantees, worth being able to name
individually (a very common interview ask):

1. **Confidentiality** — data is encrypted in transit, unreadable to
   anyone intercepting it
2. **Integrity** — any tampering with the data in transit is detectable
3. **Authentication** — the client can verify it's actually talking to
   the real server (via the server's certificate), not an impostor

### The TLS handshake (simplified)
```
Client → Server:  "Hello, here's what encryption I support"
Server → Client:  "Here's my certificate + chosen cipher suite"
Client verifies the certificate against a trusted Certificate Authority
Client & Server:  agree on session keys (via asymmetric crypto)
--- switch to symmetric encryption for the actual data ---
```

### Why the switch from asymmetric to symmetric mid-handshake?
Asymmetric encryption (public/private key pairs) is computationally
expensive. It's used only briefly, to safely agree on a **shared
symmetric key** without ever transmitting that key in the clear.
Once both sides have that shared key, they switch to symmetric
encryption for the actual data — much faster, and sufficient once both
sides already securely share a secret.

### Certificates, briefly
A certificate is issued by a trusted **Certificate Authority (CA)** and
cryptographically binds a domain name to a public key. Your
browser/OS ships with a list of trusted CAs; if a certificate wasn't
signed by one of them (or has expired, or doesn't match the domain),
you get the "connection not private" warning.

## ShopNow packet journey: protect the application request

The customer sends an HTTPS request such as `POST /api/orders` to `shop.example.com`. The external load balancer can terminate TLS using a certificate for that hostname, inspect the HTTP host and path, and route the request to ShopNow's web backend. The backend then calls the internal `orders` Service with another HTTP request.

TLS termination defines a trust boundary. If traffic between the load balancer, Pods, and managed services must also be encrypted, ShopNow needs additional TLS connections or a service-mesh design; frontend HTTPS alone does not automatically encrypt every internal hop.

## Next
[ACLs & Network Segmentation →](12-acls-segmentation.md)
