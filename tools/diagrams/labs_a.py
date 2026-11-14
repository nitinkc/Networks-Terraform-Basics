from dgm import Canvas, PAL, MUTED
from labkit import out, steps, cmds

CHIP = "PACKET TRACER LAB"


def link(c, a, b, sa="r", sb="l", label=None, col="gray", lx=None, ly=None, **kw):
    c.edge(a, b, sa, sb, c=col, w=kw.pop("w", 4), arrow=None, **kw)
    if label:
        pa, pb = c.reg[a], c.reg[b]
        x = lx if lx is not None else (pa[0] + pa[2] + pb[0]) / 2
        y = ly if ly is not None else (pa[1] + pa[3] / 2 + pb[1] + pb[3] / 2) / 2
        c.label(x, y, label, c="gray")


def lab01():
    c = Canvas(1360, 840, "Lab 01 — One flat LAN", "192.168.1.0/24 · no router, no default gateway · the switch forwards frames straight between hosts by MAC", f"LAB 01 · {CHIP}")
    c.group(44, 130, 836, 360, "FLAT LAN · 192.168.1.0/24", c="blue", tag="one broadcast domain")
    c.icon_box("pc0", "pc", 110, 190, 72, "blue", "PC0", ["~192.168.1.1"])
    c.icon_box("pc1", "pc", 110, 350, 72, "purple", "PC1", ["~192.168.1.2"])
    c.icon_box("sw", "switch", 400, 262, 110, "yellow", "Switch0 · 2960", ["MAC-table forwarding"])
    c.icon_box("srv", "server", 690, 244, 80, "green", "Server0", ["~192.168.1.100", "HTTP 80 · FTP 21"])
    link(c, "pc0", "sw", "r", "l.2")
    link(c, "pc1", "sw", "r", "l.8")
    link(c, "sw", "srv", "r.2", "l")
    c.label(345, 284, "Fa0/1")
    c.label(345, 350, "Fa0/2")
    c.label(595, 284, "Fa0/3")
    c.table(44, 524, [110, 150, 110, 140], [["Device", "IP", "Mask", "Gateway"], ["PC0", "192.168.1.1", "/24", "none"], ["PC1", "192.168.1.2", "/24", "none"], ["Server0", "192.168.1.100", "/24", "none"]], rowh=34, head="blue", mono_cols=(1, 2, 3))
    c.table(580, 524, [190, 110], [["MAC (learned)", "Port"], ["PC0 · 0001.…", "Fa0/1"], ["PC1 · 0002.…", "Fa0/2"], ["Server0 · 0003.…", "Fa0/3"]], rowh=34, head="yellow", mono_cols=(1,))
    steps(c, 920, 170, 396, [("ARP request (broadcast)", "PC0: “who has 192.168.1.100?” — flooded"), ("ARP reply (unicast)", "Server0 answers; switch learns both MACs"), ("TCP handshake", "SYN · SYN-ACK · ACK to port 80 (or 21)"),
                             ("HTTP GET / FTP login", "application data in Ethernet frames"), ("Switch forwards by MAC", "no router, no gateway, no IP routing")], col="blue", h=60, gap=10)
    cmds(c, 920, 600, 396, ["ping 192.168.1.100", "arp -a", "http://192.168.1.100", "ftp 192.168.1.100"])
    c.footer("", "OBSERVE", lines=["Switch the Packet Tracer view to Simulation and filter ARP, ICMP, HTTP: watch the broadcast flood, then unicast forwarding.",
                                    "Same subnet means no gateway is needed: hosts ARP for each other directly."])
    c.save(out("labs/01-single-subnet-ftp-http/diagrams/lab01-single-lan"))


def lab02():
    c = Canvas(1360, 1130, "Lab 02 — Routing between two /26 subnets", "One /24 carved into two /26 networks; Router0 is the only way between them", f"LAB 02 · {CHIP}")
    c.group(44, 130, 450, 350, "SUBNET 1 · 192.168.1.0/26", c="blue", tag=".0–.63")
    c.icon_box("pc1", "pc", 70, 190, 64, "blue", "PC1", ["~.11"])
    c.icon_box("pc2", "pc", 70, 340, 64, "purple", "PC2", ["~.22"])
    c.icon_box("sw0", "switch", 330, 250, 90, "yellow", "Switch0", ["Layer 2"])
    c.icon_box("r0", "router", 590, 240, 100, "teal", "Router0", ["~G0/0 192.168.1.1/26", "~G0/1 192.168.1.65/26"])
    c.group(866, 130, 450, 350, "SUBNET 2 · 192.168.1.64/26", c="green", tag=".64–.127")
    c.icon_box("sw1", "switch", 890, 250, 90, "yellow", "Switch1", ["Layer 2"])
    c.icon_box("lap", "pc", 1170, 190, 64, "orange", "Laptop0", ["~.70"])
    c.icon_box("srv", "server", 1170, 330, 70, "green", "Server0", ["~.100", "HTTP · FTP"])
    link(c, "pc1", "sw0", "r", "l.2")
    link(c, "pc2", "sw0", "r", "l.8")
    link(c, "sw0", "r0", "r", "l", ly=285, lx=540)
    link(c, "r0", "sw1", "r", "l", ly=285, lx=815)
    link(c, "sw1", "lap", "r.2", "l")
    link(c, "sw1", "srv", "r.8", "l")
    c.label(540, 285, "G0/0 .1", c="teal")
    c.label(815, 285, "G0/1 .65", c="teal")
    c.text(44, 504, [("^THE /24 ADDRESS SPACE, SLICED INTO FOUR /26 BLOCKS (256 ADDRESSES)", PAL["indigo"][2])])
    segs = [("Subnet 1 · .0 – .63", ["~R0 .1 · PC1 .11 · PC2 .22"], "blue"), ("Subnet 2 · .64 – .127", ["~R0 .65 · Lap .70 · Srv .100"], "green"), ("unused · .128 – .191", ["spare /26"], "gray"), ("unused · .192 – .255", ["spare /26"], "gray")]
    for i, (t, d, col) in enumerate(segs):
        c.rect(44 + i * 318, 536, 312, 80, [f"#{t}"] + d, c=col, shadow=False)
    steps(c, 44, 700, 780, [("Is .100 on my subnet?", "PC1 .11/26 → .100 is outside .0–.63, so use the default gateway"), ("ARP for the gateway", "PC1 broadcasts “who has 192.168.1.1?”; Router0 G0/0 replies"),
                            ("Router0 routes", "dst .100 matches connected network 192.168.1.64/26 → out G0/1"), ("ARP in subnet 2", "Router0 ARPs for .100, rewrites the Ethernet header, forwards"),
                            ("Reply retraces the path", "Server0 → gateway .65 → Router0 → PC1")], col="indigo", title="PACKET WALK · PC1 → SERVER0", h=56, gap=8)
    c.table(870, 700, [140, 150, 156], [["Hop", "L2 src → dst", "L3 src → dst"], ["PC1 → R0", "PC1 → G0/0", ".11 → .100"], ["R0 → Server", "G0/1 → Server0", ".11 → .100"]], rowh=40, head="teal", mono_cols=(1, 2))
    c.text(870, 836, [("_Orange rule: MAC addresses change at every hop; the IP pair stays the same.", MUTED)])
    cmds(c, 870, 880, 446, ["ping 192.168.1.100", "tracert 192.168.1.100", "show ip route"])
    c.footer("", "OBSERVE", lines=["Change a host to the wrong mask or gateway and watch exactly which step of the packet walk breaks.",
                                    "Directly connected networks appear in the routing table automatically once the interface is up with an IP."])
    c.save(out("labs/02-router-subnets/diagrams/lab02-router-subnets"))


def lab03():
    c = Canvas(1360, 1010, "Lab 03 — DHCP, PAT and an ISP edge", "Clients lease addresses from Router0, then share one public address through PAT to reach a server behind an ISP", f"LAB 03 · {CHIP}")
    c.group(44, 130, 420, 330, "PRIVATE LAN · 192.168.1.0/24", c="blue", tag="DHCP clients")
    c.icon_box("pc0", "pc", 70, 190, 64, "blue", "PC0", ["DHCP → .2"])
    c.icon_box("pc1", "pc", 70, 330, 64, "purple", "PC1", ["DHCP → .3"])
    c.icon_box("sw", "switch", 320, 250, 90, "yellow", "Switch0")
    c.icon_box("r0", "router", 560, 240, 100, "orange", "Router0 · Edge/NAT", ["~LAN .1 · WAN 203.0.113.1/30", "DHCP pool + PAT overload"])
    c.icon_box("r1", "router", 880, 240, 100, "red", "Router1 · ISP", ["~203.0.113.2/30", "~198.51.100.1/24"])
    c.group(1100, 130, 216, 330, "PUBLIC · .100.0/24", c="green")
    c.icon_box("srv", "server", 1170, 250, 80, "green", "Server0", ["~198.51.100.2", "HTTP 80 · FTP 21"])
    link(c, "pc0", "sw", "r", "l.2")
    link(c, "pc1", "sw", "r", "l.8")
    link(c, "sw", "r0", "r", "l", ly=285, lx=485)
    link(c, "r0", "r1", "r", "l", ly=285, lx=820)
    link(c, "r1", "srv", "r", "l", ly=285, lx=1085)
    c.label(820, 285, "203.0.113.0/30", c="gray")
    c.line([(610, 425), (930, 425)], color="#2F6FE0", w=5)
    c.label(770, 425, "PAT: 192.168.1.2:49152 → 203.0.113.1:1025", c="blue")
    c.text(44, 506, [("^NAT TABLE ON ROUTER0 (SHOW IP NAT TRANSLATIONS)", PAL["indigo"][2])])
    c.table(44, 536, [90, 250, 250, 220], [["Proto", "Inside local", "Inside global", "Outside"], ["TCP", "192.168.1.2:49152", "203.0.113.1:1025", "198.51.100.2:80"], ["TCP", "192.168.1.3:49153", "203.0.113.1:1026", "198.51.100.2:80"]], rowh=36, head="orange", mono_cols=(1, 2, 3))
    c.rect(44, 660, 810, 74, [("!ISP has no route back to 192.168.1.0/24 — and shouldn't", PAL["red"][2]), ("_Private addresses never cross the edge; only 203.0.113.1 is visible", MUTED)], c="red", white=True, shadow=False)
    steps(c, 900, 540, 416, [("DORA on the LAN", "Discover · Offer · Request · Ack → .2 / .3"), ("Off-subnet destination", "client sends to default gateway 192.168.1.1"), ("Router0 translates", "src 192.168.1.x:port → 203.0.113.1:new port"),
                             ("Server sees one host", "all clients share 203.0.113.1"), ("Return traffic", "NAT table maps it back to the right PC")], col="orange", h=56, gap=8, title="WHAT HAPPENS WHEN PC0 BROWSES")
    cmds(c, 44, 770, 810, ["ipconfig /all", "ping 198.51.100.2", "show ip nat translations", "show ip dhcp binding"])
    c.footer("", "OBSERVE", lines=["Clear the NAT table, browse again and compare how the inside-global port changes while the inside-local port stays put.",
                                    "DHCP supplies address + mask + gateway; PAT then makes those private addresses usable on the public side."])
    c.save(out("labs/03-multi-router-nat-dhcp/diagrams/lab03-nat-dhcp"))


def seq(c, actors, msgs, y0, y_end):
    for t, sub, col, x in actors:
        c.rect(x - 120, y0, 240, 66, [f"#{t}", f"_{sub}"], c=col, pad=4)
        c.lifeline(x, y0 + 66, y_end)


def lab04():
    c = Canvas(1360, 1200, "Lab 04 — Central DHCP server through a relay", "DHCP discovery is a broadcast and routers stop broadcasts; the relay agent converts it to a unicast the server can answer", f"LAB 04 · {CHIP}")
    c.group(44, 130, 440, 320, "CLIENT LAN · 192.168.10.0/24", c="blue", tag="Sales")
    c.icon_box("pc0", "pc", 70, 190, 64, "blue", "PC0", ["DHCP"])
    c.icon_box("pc1", "pc", 70, 320, 64, "purple", "PC1", ["DHCP"])
    c.icon_box("sw0", "switch", 330, 240, 90, "yellow", "Switch0")
    c.icon_box("r0", "router", 590, 230, 100, "orange", "Router0 · relay", ["~G0/0 192.168.10.1", "~G0/1 192.168.20.1", "ip helper-address 192.168.20.10"])
    c.group(870, 130, 446, 320, "SERVER FARM · 192.168.20.0/24", c="green", tag="DHCP-Server0")
    c.icon_box("sw1", "switch", 890, 240, 90, "yellow", "Switch1")
    c.icon_box("dhcp", "server", 1150, 230, 80, "green", "DHCP-Server0", ["~192.168.20.10", "leases 192.168.10.20+"])
    link(c, "pc0", "sw0", "r", "l.2")
    link(c, "pc1", "sw0", "r", "l.8")
    link(c, "sw0", "r0", "r", "l", ly=275, lx=540)
    link(c, "r0", "sw1", "r", "l", ly=275, lx=830)
    link(c, "sw1", "dhcp", "r", "l", ly=275)
    xs = [190, 680, 1170]
    seq(c, [("Client PC0", "0.0.0.0", "blue", xs[0]), ("Router0 relay", "G0/0 192.168.10.1", "orange", xs[1]), ("DHCP-Server0", "192.168.20.10", "green", xs[2])], [], 500, 1010)
    c.msg(xs[0], xs[1], 640, "DISCOVER · broadcast", "blue", lines=["dst 255.255.255.255 — stops at the router"], w=3.5)
    c.msg(xs[1], xs[2], 720, "DISCOVER · unicast", "orange", lines=["to 192.168.20.10 with giaddr = 192.168.10.1"], w=3.5)
    c.msg(xs[2], xs[1], 800, "OFFER · unicast", "green", lines=["giaddr selects the 192.168.10.0/24 pool"], w=3.5)
    c.msg(xs[1], xs[0], 880, "OFFER · to the client", "green", lines=["relay delivers it on the client's LAN"], w=3.5)
    for i, l in enumerate("DDOO"):
        c.badge(l, 44 + 20, [640, 720, 800, 880][i], ["blue", "orange", "green", "green"][i], r=15)
    c.rect(60, 940, 520, 50, [("!REQUEST and ACK follow the same relayed path", PAL["indigo"][2])], c="indigo", white=True, shape="pill", shadow=False)
    cmds(c, 700, 940, 616, ["ipconfig /renew", "show ip dhcp binding", "show running-config | include helper"], title="VERIFY")
    c.footer("", "OBSERVE", lines=["In Simulation mode filter DHCP: the first packet is a broadcast, the second is addressed to 192.168.20.10.",
                                    "Without ip helper-address the Discover dies at Router0 and clients self-assign 169.254.x.x."])
    c.save(out("labs/04-dhcp-relay/diagrams/lab04-dhcp-relay"))


def lab05():
    c = Canvas(1360, 1240, "Lab 05 — DNS before HTTP", "Humans type names; the client resolves the name to an IP first, then opens the TCP connection to that address", f"LAB 05 · {CHIP}")
    c.group(44, 130, 440, 320, "CLIENT LAN · 192.168.1.0/24", c="blue", tag="DHCP")
    c.icon_box("pc0", "pc", 70, 190, 64, "blue", "PC0", ["DHCP + DNS .5"])
    c.icon_box("pc1", "pc", 70, 320, 64, "purple", "PC1", ["DHCP + DNS .5"])
    c.icon_box("sw0", "switch", 330, 240, 90, "yellow", "Switch0")
    c.icon_box("r0", "router", 590, 230, 100, "teal", "Router0", ["routes both subnets"])
    c.group(870, 130, 446, 320, "SERVER LAN · 198.51.100.0/24", c="green")
    c.icon_box("sw1", "switch", 900, 245, 70, "yellow", "Switch1")
    c.icon_box("dns", "server", 1080, 170, 60, "purple", "DNS-Server0", ["~198.51.100.5", "UDP/TCP 53"])
    c.icon_box("web", "server", 1080, 310, 60, "green", "Web-Server0", ["~198.51.100.10", "HTTP 80 · FTP 21"])
    link(c, "pc0", "sw0", "r", "l.2")
    link(c, "pc1", "sw0", "r", "l.8")
    link(c, "sw0", "r0", "r", "l", ly=275, lx=540)
    link(c, "r0", "sw1", "r", "l")
    link(c, "sw1", "dns", "r", "l")
    link(c, "sw1", "web", "r", "l")
    xs = [190, 640, 1110]
    seq(c, [("PC0", "browser", "blue", xs[0]), ("DNS-Server0", "198.51.100.5", "purple", xs[1]), ("Web-Server0", "198.51.100.10", "green", xs[2])], [], 490, 910)
    c.msg(xs[0], xs[1], 620, "① A? www.company.local", "purple", lines=["UDP 53 — the name has no address yet"], w=3.5)
    c.msg(xs[1], xs[0], 695, "② CNAME → web.company.local · A 198.51.100.10", "purple", lines=["answer travels back to the client"], w=3.5)
    c.msg(xs[0], xs[2], 790, "③ TCP handshake to 198.51.100.10:80", "blue", lines=["only now does the web server see traffic"], w=3.5)
    c.msg(xs[2], xs[0], 870, "④ HTTP 200 OK", "green", lines=["page rendered in the browser"], w=3.5)
    c.table(44, 960, [190, 280, 290], [["Record", "Name", "Value"], ["A", "web.company.local", "198.51.100.10"], ["CNAME", "www.company.local", "web.company.local"]], rowh=34, head="purple", mono_cols=(0, 1, 2))
    cmds(c, 880, 960, 436, ["nslookup www.company.local", "ping www.company.local", "ipconfig /all"], title="VERIFY")
    c.footer("", "OBSERVE", lines=["Ping by IP works but ping by name fails? The problem is DNS (or the DNS server address from DHCP), not routing.",
                                    "Every name lookup is a separate UDP 53 conversation that happens before the HTTP session."])
    c.save(out("labs/05-dns-name-resolution/diagrams/lab05-dns-resolution"))


def lab06():
    c = Canvas(1360, 1090, "Lab 06 — PAT and static port forwarding", "Many inside hosts share one public IP outbound; one published port reaches an inside server inbound", f"LAB 06 · {CHIP}")
    c.group(44, 130, 440, 380, "INSIDE · 192.168.1.0/24", c="blue", tag="private")
    c.icon_box("pc0", "pc", 100, 172, 48, "blue", "PC0", ["~.10"])
    c.icon_box("pc1", "pc", 100, 276, 48, "purple", "PC1", ["~.11"])
    c.icon_box("isv", "server", 100, 380, 48, "green", "Internal-Server", ["~.100:80"])
    c.icon_box("sw", "switch", 330, 270, 90, "yellow", "Switch0")
    c.icon_box("r0", "router", 570, 215, 100, "orange", "Router0 · NAT border", ["~in  192.168.1.1", "~out 203.0.113.1/30"])
    c.icon_box("r1", "router", 860, 215, 100, "red", "Router1 · ISP", ["~203.0.113.2/30", "~198.51.100.1/24"])
    c.group(1060, 130, 256, 380, "PUBLIC · 198.51.100.0/24", c="green", tag="")
    c.icon_box("web", "server", 1160, 175, 52, "green", "Public-Web", ["~.2:80"])
    c.icon_box("cli", "pc", 1160, 340, 52, "teal", "Outside-Client", ["~.50"])
    c.edge("pc0", "sw", "r", "l.15", c="gray", w=4, arrow=None)
    c.edge("pc1", "sw", "r", "l.5", c="gray", w=4, arrow=None)
    c.edge("isv", "sw", "r", "l.85", c="gray", w=4, arrow=None)
    c.edge("sw", "r0", "r", "l", via=[(470, 315), (470, 265)], c="gray", w=4, arrow=None)
    c.edge("r0", "r1", "r", "l", c="gray", w=4, arrow=None)
    c.edge("r1", "web", "r", "l", via=[(1010, 265), (1010, 201)], c="gray", w=4, arrow=None)
    c.edge("r1", "cli", "r", "l", via=[(1010, 265), (1010, 366)], c="gray", w=4, arrow=None)
    c.line([(620, 440), (910, 440)], color="#2F6FE0", w=5)
    c.label(765, 440, "PAT out: .10:50001 → 203.0.113.1:50001", c="blue")
    c.line([(910, 485), (620, 485)], color="#1E9A63", w=5, dash="d")
    c.label(765, 485, "static in: 203.0.113.1:8080 → .100:80", c="green")
    c.table(44, 560, [90, 240, 240, 200], [["Type", "Inside local", "Inside global", "Outside"], ["PAT", "192.168.1.10:50001", "203.0.113.1:50001", "198.51.100.2:80"], ["PAT", "192.168.1.11:50001", "203.0.113.1:50002", "198.51.100.2:80"], ["Static", "192.168.1.100:80", "203.0.113.1:8080", "any"]],
            rowh=38, head="orange", mono_cols=(1, 2, 3), rowc=[None, None, "green"])
    c.rect(44, 730, 810, 78, [("!Same source port, different PCs? PAT assigns a new global port", PAL["orange"][2]), ("_PC0 and PC1 both chose :50001 — .11 becomes :50002 so replies stay unique", MUTED)], c="orange", white=True, shadow=False)
    steps(c, 900, 580, 416, [("Outbound: create entry", "first packet builds the translation row"), ("Reply: look up entry", "dst global port → inside local address"), ("Inbound unsolicited: no row", "dropped, unless a static rule exists"),
                             ("Static PAT row", "8080 on Router0 → .100:80 inside")], col="orange", h=58, gap=8, title="WHAT TO WATCH")
    cmds(c, 44, 830, 810, ["show ip nat translations", "show ip nat statistics", "http://203.0.113.1:8080 (from Outside-Client)"])
    c.footer("", "OBSERVE", lines=["Outside-Client can browse to Router0's public IP on 8080 but cannot reach 192.168.1.100 directly — private space stays hidden.",
                                    "Compare the inside local and inside global columns for every flow: that mapping is the entire NAT idea."])
    c.save(out("labs/06-nat-pat-port-forwarding/diagrams/lab06-nat-pat"))


def lab07():
    c = Canvas(1360, 1050, "Lab 07 — OSPF inside, eBGP outside", "R1 and R2 learn the enterprise topology with OSPF; R2 and the ISP exchange reachability with eBGP between AS 65001 and AS 65002", f"LAB 07 · {CHIP}")
    c.group(44, 130, 840, 330, "ENTERPRISE · AS 65001", c="teal", tag="OSPF Area 0")
    c.icon_box("pc", "pc", 70, 220, 64, "blue", "PC0", ["~10.1.1.10/24"])
    c.icon_box("r1", "router", 290, 210, 90, "teal", "R1-Core", ["~10.1.1.1 · 10.1.12.1/30"])
    c.icon_box("r2", "router", 600, 210, 90, "orange", "R2-Edge", ["~10.1.12.2/30 · 203.0.113.1/30"])
    c.group(960, 130, 356, 330, "ISP · AS 65002", c="purple", tag="eBGP peer")
    c.icon_box("isp", "router", 990, 210, 90, "red", "ISP-Router", ["~203.0.113.2/30", "~198.51.100.1/24"])
    c.icon_box("srv", "server", 1210, 215, 70, "green", "Cloud Server", ["~198.51.100.2"])
    link(c, "pc", "r1", "r", "l")
    link(c, "r1", "r2", "r", "l")
    link(c, "r2", "isp", "r", "l")
    link(c, "isp", "srv", "r", "l")
    c.label(485, 255, "OSPF adjacency · 10.1.12.0/30", c="teal")
    c.label(920, 255, "eBGP TCP 179", c="purple", solid=True)
    c.rect(70, 360, 380, 70, [("!R2 originates the default route", PAL["teal"][2]), ("~default-information originate", MUTED)], c="teal", white=True, shadow=False, pad=4)
    c.rect(500, 360, 360, 70, [("!R2 ↔ ISP exchange prefixes", PAL["purple"][2]), ("~203.0.113.0/30 ⇄ 198.51.100.0/24", MUTED)], c="purple", white=True, shadow=False, pad=4)
    steps(c, 44, 530, 600, [("OSPF neighbours form", "R1–R2 Hello → 2-Way → Full on 10.1.12.0/30"), ("eBGP session opens", "R2 ↔ ISP over TCP 179: Idle → Active → Established"), ("R2 learns 198.51.100.0/24", "via BGP from AS 65002"),
                            ("R2 injects a default route", "OSPF carries 0.0.0.0/0 to R1 (O*E2)"), ("PC0 pings Cloud Server", "R1 default → R2 → ISP → server and back")], col="indigo", title="ROUTE-LEARNING TIMELINE", h=60, gap=8)
    c.text(690, 500, [("^R1 ROUTING TABLE (EXPECTED)", PAL["indigo"][2])])
    c.table(690, 530, [70, 190, 180, 186], [["Code", "Prefix", "Via", "Meaning"], ["C", "10.1.1.0/24", "Gi0/0", "connected"], ["C", "10.1.12.0/30", "Gi0/1", "connected"], ["O*E2", "0.0.0.0/0", "10.1.12.2", "OSPF default"]], rowh=40, head="teal", mono_cols=(0, 1, 2))
    c.rect(690, 700, 626, 70, [("!Two protocols, two jobs", PAL["indigo"][2]), ("_OSPF = fastest path inside · BGP = policy between organisations", MUTED)], c="indigo", white=True, shadow=False)
    cmds(c, 690, 800, 626, ["show ip ospf neighbor", "show ip bgp summary", "show ip route", "ping 198.51.100.2"], title="VERIFY")
    c.footer("", "OBSERVE", lines=["Shut the R1–R2 link: the OSPF neighbour drops and PC0 loses its default route within the dead interval.",
                                    "Shut the BGP session instead: R1 keeps working internally but R2 can no longer reach 198.51.100.0/24."])
    c.save(out("labs/07-ospf-ebgp/diagrams/lab07-ospf-bgp"))


def lab08():
    c = Canvas(1360, 1190, "Lab 08 — VLAN segmentation and ACL policy", "Three VLANs reach Router0 over one 802.1Q trunk; per-VLAN ACLs decide what each may reach on the corporate server", f"LAB 08 · {CHIP}")
    vl = [("VLAN 10 · Engineering", "10.1.10.0/24", "full server access", "blue", 160), ("VLAN 20 · HR / Finance", "10.1.20.0/24", "HTTP only", "purple", 280), ("VLAN 30 · Guest", "10.1.30.0/24", "internal denied", "orange", 400)]
    for i, (t, ip, d, col, y) in enumerate(vl):
        c.rect(44, y, 250, 90, [f"#{t}", f"~{ip}", f"_{d}"], c=col, id=f"v{i}", pad=4)
    c.icon_box("sw0", "switch", 380, 270, 90, "yellow", "Switch0 · 2960", ["access ports"])
    c.icon_box("r0", "router", 640, 255, 110, "teal", "Router0 · ROAS", ["~G0/0.10 · .20 · .30"])
    c.icon_box("sw1", "switch", 930, 270, 90, "yellow", "Switch1")
    c.icon_box("srv", "server", 1170, 255, 80, "green", "Server0", ["~10.1.50.10", "HTTP 80 · SSH 22"])
    for i in range(3):
        c.edge(f"v{i}", "sw0", "r", f"l.{2 + 3 * i}", c=["blue", "purple", "orange"][i], w=5, arrow=None)
    c.line([(470, 315), (640, 315)], color="#7C4DDB", w=9, arrow="both")
    c.label(555, 315, "802.1Q trunk", c="purple", solid=True)
    c.edge("r0", "sw1", "r", "l", c="gray", w=4, arrow=None)
    c.edge("sw1", "srv", "r", "l", c="gray", w=4, arrow=None)
    c.label(840, 310, "G0/1 10.1.50.1", c="teal")
    c.rect(600, 410, 190, 56, [("!HR_SECURITY_POLICY", PAL["purple"][2]), ("_ACL on G0/0.20", MUTED)], c="purple", white=True, shadow=False, pad=4)
    c.rect(810, 410, 220, 56, [("!GUEST_ISOLATION_POLICY", PAL["orange"][2]), ("_ACL on G0/0.30", MUTED)], c="orange", white=True, shadow=False, pad=4)
    c.text(44, 540, [("^POLICY MATRIX · WHO MAY REACH 10.1.50.10", PAL["indigo"][2])])
    cl = {"✓": "green", "✗": "red"}
    grid = [["Source", "HTTP 80", "SSH 22", "ICMP ping"], ["VLAN 10 Engineering", "✓ allow", "✓ allow", "✓ allow"], ["VLAN 20 HR / Finance", "✓ allow", "✗ deny", "✗ deny"], ["VLAN 30 Guest", "✗ deny", "✗ deny", "✗ deny"]]
    for r, row in enumerate(grid):
        for k, cell in enumerate(row):
            x, y, w = 44 + [0, 250, 400, 550][k], 572 + r * 52, [250, 150, 150, 150][k]
            if r == 0 or k == 0:
                c.rect(x, y, w, 48, [f"!{cell}"], c="indigo", solid=True, shape="rect", sw=1, shadow=False, pad=4)
            else:
                c.rect(x, y, w, 48, [(f"!{cell}", PAL[cl[cell[0]]][2])], c=cl[cell[0]], shape="rect", sw=1, shadow=False, pad=4)
    steps(c, 800, 600, 516, [("Frame enters an access port", "Switch0 tags it with the port's VLAN ID"), ("Trunk carries it to Router0", "802.1Q tag selects the sub-interface"), ("Router routes between VLANs", "ACL on the sub-interface is checked first"),
                             ("Server reply", "returns via G0/1; ACL on G0/1 or in the policy matches")], col="indigo", h=56, gap=8, title="PACKET WALK · HR PC → SERVER")
    cmds(c, 44, 810, 700, ["show vlan brief", "show interfaces trunk", "show access-lists", "ping 10.1.50.10", "ssh -l admin 10.1.50.10"], title="VERIFY")
    c.rect(44, 960, 730, 62, [("!Test every cell of the matrix — a wrong ACL direction looks identical to no ACL", PAL["red"][2])], c="red", white=True, shape="pill", shadow=False)
    c.footer("", "OBSERVE", lines=["VLANs separate broadcast domains; only the router (with ACLs) lets them communicate, so policy lives in one place.",
                                    "ACL order, direction and the implicit deny decide the result: re-read the matrix after every change."])
    c.save(out("labs/08-vlans-acls/diagrams/lab08-vlan-acl"))


def lab09():
    c = Canvas(1360, 1100, "Lab 09 — Physical equivalent of a GCP two-tier VPC", "Packet Tracer reproduces the web/app tiers with VLANs, ACLs, NAT, DNS and an ISP edge — the same ideas Terraform declares in the cloud", f"LAB 09 · {CHIP}")
    c.icon_box("cli", "pc", 60, 240, 64, "teal", "Internet-Client", ["~198.51.100.50"])
    c.icon_box("isp", "router", 270, 230, 90, "red", "Router-ISP", ["~203.0.113.2/30", "~198.51.100.1/24"])
    c.group(480, 130, 836, 440, "PRIVATE ENTERPRISE ≈ GCP VPC", c="indigo", tag="Router-Edge")
    c.icon_box("edge", "router", 520, 230, 90, "orange", "Router-Edge", ["ROAS · ACLs · NAT/PAT", "~WAN 203.0.113.1/30"])
    c.icon_box("sw", "switch", 730, 250, 70, "yellow", "Switch")
    c.group(860, 185, 430, 170, "VLAN 10 · Web tier · 10.1.10.0/24", c="green", hh=34)
    c.icon_box("web", "server", 880, 232, 54, "green", "Frontend-Web0", ["~10.1.10.2"])
    c.rect(1010, 236, 260, 62, [("!Reachable from the internet", PAL["green"][2]), ("_via static NAT / port forward", MUTED)], c="green", white=True, shadow=False)
    c.group(860, 372, 430, 190, "VLAN 20 · App tier · 10.1.20.0/24", c="purple", hh=34)
    c.icon_box("app", "server", 880, 420, 54, "purple", "Backend-App0", ["~10.1.20.2:8080"])
    c.icon_box("dns", "server", 1030, 420, 54, "teal", "DNS Server", ["~10.1.20.5"])
    c.rect(1130, 420, 148, 62, [("!No direct path", PAL["red"][2]), ("_from the internet", MUTED)], c="red", white=True, shadow=False, pad=4)
    c.edge("cli", "isp", "r", "l", c="gray", w=4, arrow=None)
    c.edge("isp", "edge", "r", "l", c="gray", w=4, arrow=None)
    c.edge("edge", "sw", "r", "l", c="purple", w=7, arrow="both")
    c.line([(800, 275), (860, 263)], color="#1E9A63", w=4, arrow=None)
    c.line([(800, 290), (830, 290), (830, 450), (860, 450)], color="#7C4DDB", w=4, arrow=None)
    c.text(44, 596, [("^PACKET TRACER → GCP TRANSLATION", PAL["indigo"][2])])
    c.table(44, 626, [310, 310, 310], [["Packet Tracer", "GCP", "Role"], ["VLAN 10 / VLAN 20", "web-tier / app-tier subnets", "tier isolation"], ["ACLs on Router-Edge", "VPC firewall rules (tags)", "micro-segmentation"],
                                       ["NAT/PAT on Router-Edge", "Cloud NAT / external IP", "outbound + published access"], ["DNS Server 10.1.20.5", "Cloud DNS private zone", "internal names"], ["Router-ISP", "Internet", "untrusted outside"]],
            rowh=38, head="indigo")
    steps(c, 1000, 646, 316, [("Client → web tier", "allowed: HTTP via NAT"), ("Web → App :8080", "ACL permits the API port"), ("Client → App", "no path — blocked")], col="indigo", h=56, gap=8, title="THREE FLOWS TO TEST")
    c.rect(44, 884, 930, 86, [("!Design goal: only the web tier is exposed", PAL["indigo"][2]), ("_The app tier and DNS live on a private VLAN; outbound access uses NAT, never inbound reachability", MUTED)], c="indigo", white=True, shadow=False)
    c.footer("", "OBSERVE", lines=["Everything the cloud gives you as a service (subnet, firewall rule, NAT, DNS) is a device or configuration you can see here.",
                                    "Terraform labs 02–05 build exactly this two-tier layout with google_compute_* resources."])
    c.save(out("labs/09-gcp-architecture-equivalent/diagrams/lab09-gcp-equivalent"))


if __name__ == "__main__":
    for f in (lab01, lab02, lab03, lab04, lab05, lab06, lab07, lab08, lab09):
        f()
