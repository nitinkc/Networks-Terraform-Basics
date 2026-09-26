## Router

The **WAN (Wide Area Network) port** is specifically designed to connect your local network to the outside world—most 
commonly your Internet Service Provider (ISP) and the broader Internet.


```text
   [ THE INTERNET ]
          │
          ▼ (Public IP from ISP)
┌──────────────────┐
│     WAN PORT     │  <-- Connects to Modem / ISP (ip nat outside)
├──────────────────┤
│  ROUTER ENGINE   │  <-- Runs NAT/PAT, Firewall, Routing
├──────────────────┤
│  INTERNAL SWITCH │  <-- Layer 2 Switch built into the router
└─┬───┬───┬───┬────┘
  │   │   │   │
 LAN1LAN2LAN3LAN4    <-- Connects to PCs, Printers, Switches
  │   │   │   │          (Shares Private Subnet: 192.168.1.0/24)
  ▼   ▼   ▼   ▼
 [ Local Devices ]

```

| Feature               | WAN Port (Wide Area Network)                                                 | LAN Ports (Local Area Network)                                                |
|:----------------------|:-----------------------------------------------------------------------------|:------------------------------------------------------------------------------|
| **Primary Purpose**   | Connects upstream to the Internet / ISP Modem.                               | Connects downstream to local computers, TVs, switches.                        |
| **IP Address Type**   | Receives a Public IP from your ISP (e.g., `203.0.113.1`).                    | Assigns Private IPs to devices (e.g., `192.168.1.2`, `.3`).                   |
| **NAT Role**          | Acts as `ip nat outside` (the exit point where internal IPs are translated). | Acts as `ip nat inside` (the private zone).                                   |
| **Firewall Behavior** | Blocks unsolicited incoming traffic from the internet by default.            | Allows all devices on the local subnet to communicate freely with each other. |
| **Physical Layout**   | Usually 1 dedicated port (often colored yellow or blue).                     | Multiple ports (usually 4) connected to an internal switch.                   |

**In a Home/All-in-One Router:** The router, 4-port switch, Wi-Fi access point, DHCP server, and NAT engine are all
combined into one physical box.
