# Networking labs — Cisco Packet Tracer

Reference configs and topologies used to practice core networking concepts
(subnetting, DHCP, NAT, switching vs routing, FTP/HTTP) for system design /
interview prep, built and tested in Cisco Packet Tracer.

## Structure

```
network-lab-pkt/
├── README.md
├── configs/
│   ├── multi-router-nat-dhcp-lab.md   # 2 PCs -> switch -> router (DHCP+NAT) -> router -> server
│   └── basic-ftp-http-lan.md          # 2 PCs -> switch -> server (FTP + HTTP), single flat subnet
└── topology/
    └── (drop your saved .pkt / .pkz files here)
```

```shell
uvx --with mkdocs-material mkdocs serve
```
## Labs

### 1. Basic FTP/HTTP LAN (`docs/configs`)
The simplest possible setup: two PCs and a server on one flat subnet
(192.168.1.0/24), no router. Server runs both HTTP and FTP services.
Used to isolate application-layer behavior (HTTP GET, FTP control/data
channels) from any routing or NAT complexity.

### 2. Multi-router NAT/DHCP lab (`docs/configs`)
Two PCs on a DHCP-served LAN behind Router0 (which also does NAT/PAT
overload), routed through Router1 to a public-side server. Used to
practice subnetting, DHCP leasing, NAT translation tables, and basic
static routing.

## Why the actual .pkt files aren't committed here

Packet Tracer's `.pkt`/`.pkz` formats are proprietary binaries — they
can't be generated or diffed as text. This repo intentionally keeps the
**reviewable, diffable source of truth** (device addressing, CLI config
blocks, test steps) in Markdown under `docs/configs`, and treats the actual
`.pkt` file you save from Packet Tracer as a build artifact you drop into
`topology/` locally.

If you do want to version the binary `.pkt`/`.pkz` files themselves:

```
git lfs install
git lfs track "*.pkt" "*.pkz"
git add .gitattributes
```

This keeps large/binary files out of your normal Git history while still
letting you push them to the repo via Git LFS.

## How to rebuild a lab from scratch

1. Open the relevant file in `docs/configs`
2. Follow the device-placement + cabling steps
3. Paste each CLI block into the matching device's terminal in Packet Tracer
4. Follow the "What to observe" table at the bottom of each file to connect
   what you're seeing back to the underlying concept
5. Save your working topology as `topology/<lab-name>.pkt`
