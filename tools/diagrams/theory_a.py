from pathlib import Path

from dgm import Canvas, PAL, MUTED

ROOT = Path(__file__).resolve().parents[2]
OUT = str(ROOT / "docs/theory/diagrams")


def d01_models():
    c = Canvas(1360, 900, "OSI and TCP/IP: one stack, two vocabularies",
               "Read left to right: seven teaching layers, the four real-world layers, and what each layer wraps around your data", "STAGE 01 · MODELS")
    y0, rh, gap = 150, 78, 8
    c.text(44, 116, [("^OSI MODEL · 7 LAYERS", PAL["indigo"][2])])
    c.text(670, 116, [("^TCP/IP · 4 LAYERS", PAL["indigo"][2])])
    c.text(900, 116, [("^ENCAPSULATION · SENDING SIDE", PAL["indigo"][2])])
    layers = [
        (7, "Application", "HTTP · FTP · DNS · SSH   —   what apps speak", "pink", "DATA"),
        (6, "Presentation", "Encoding · compression · TLS (often placed here)", "purple", "DATA"),
        (5, "Session", "Opens, keeps and closes conversations", "indigo", "DATA"),
        (4, "Transport", "TCP · UDP   —   ports, reliability, ordering", "blue", "SEGMENT"),
        (3, "Network", "IP · routers   —   addresses, path selection", "teal", "PACKET"),
        (2, "Data Link", "Ethernet · Wi-Fi · switches   —   MAC addresses", "green", "FRAME"),
        (1, "Physical", "Cables · radio · voltages   —   raw bits", "orange", "BITS"),
    ]
    for i, (n, name, job, col, pdu) in enumerate(layers):
        y = y0 + i * (rh + gap)
        c.rect(44, y, 590, rh, [f"#{name}", f"_{job}"], c=col, align="l", pad=70)
        c.badge(n, 80, y + rh / 2, c=col, r=18)
        c.rect(634 - 104, y + rh / 2 - 15, 90, 30, [(f"^{pdu}", "#FFFFFF")], c=col, solid=True, shape="pill", shadow=False)
    def span(a, b):
        return y0 + a * (rh + gap), (b - a + 1) * (rh + gap) - gap
    for (a, b, name, sub, col) in [(0, 2, "Application", "HTTP · DNS · TLS", "pink"), (3, 3, "Transport", "TCP / UDP", "blue"),
                                    (4, 4, "Internet", "IP · ICMP", "teal"), (5, 6, "Link", "Ethernet · Wi-Fi", "green")]:
        y, h = span(a, b)
        c.rect(670, y, 200, h, [f"#{name}", f"_{sub}"], c=col, solid=True)
    sx, wid = 900, 416
    def strip(label, parts, row_y, off, ctext):
        c.text(sx + off, row_y - 25, [(f"^{label}", PAL[ctext][2])])
        x = sx + off
        for lab, w, col in parts:
            c.rect(x, row_y, w, 46, [f"!{lab}"], c=col, solid=(lab != "DATA"), shape="rect", sw=1.8, shadow=False, pad=4)
            x += w
    y_app, _ = span(0, 2)
    strip("Data (HTTP request)", [("DATA", 160, "pink")], y_app + 106, 192, "pink")
    strip("Segment", [("TCP", 64, "blue"), ("DATA", 160, "pink")], span(3, 3)[0] + 18, 128, "blue")
    strip("Packet", [("IP", 64, "teal"), ("TCP", 64, "blue"), ("DATA", 160, "pink")], span(4, 4)[0] + 18, 64, "teal")
    strip("Frame", [("ETH", 64, "green"), ("IP", 64, "teal"), ("TCP", 64, "blue"), ("DATA", 160, "pink"), ("FCS", 64, "green")], span(5, 5)[0] + 18, 0, "green")
    by = span(6, 6)[0] + 18
    c.text(sx, by - 25, [("^Bits on the wire", PAL["orange"][2])])
    c.rect(sx, by, 416, 46, [("~01001000 01010100 01010100 01010000 …")], c="orange", solid=True, shape="rect", shadow=False)
    c.line([(sx - 16, y_app + 100), (sx - 16, by + 22)], c="gray", w=3, color="#7C4DDB")
    c.rect(sx, 150, 416, 74, [("!SENDER wraps going down ↓", PAL["purple"][2]), ("!RECEIVER unwraps going up ↑", PAL["purple"][2])], c="purple")
    c.footer("", "REMEMBER", lines=["Mnemonic 7→1: All People Seem To Need Data Processing.  Switch = L2 · Router = L3 · TCP/UDP = L4 · HTTP = L7.",
                                    "Each layer only talks to the same layer on the other side — headers are added going down, stripped going up."])
    c.save(f"{OUT}/01-osi-tcpip-encapsulation")


def d02_packets():
    c = Canvas(1360, 1050, "Anatomy of a packet and how an IPv4 address is read",
               "A header tells every router what to do; the mask splits an address into 'which network' and 'which host'", "STAGE 02 · PACKETS & IP")
    c.text(44, 116, [("^1 · IPV4 HEADER (20 BYTES, 32 BITS PER ROW)", PAL["indigo"][2])])
    rows = [
        [("Version\n4", 4, "blue"), ("IHL", 4, "blue"), ("DSCP / ECN", 8, "blue"), ("Total length", 16, "blue")],
        [("Identification", 16, "purple"), ("Flags", 3, "purple"), ("Fragment offset", 13, "purple")],
        [("TTL — hop limit", 8, "red"), ("Protocol (TCP=6)", 8, "orange"), ("Header checksum", 16, "gray")],
        [("Source IP address", 32, "green")],
        [("Destination IP address", 32, "teal")],
        [("Options + padding (rare)", 32, "gray")],
    ]
    hx, hw, rh = 44, 700, 46
    for i, r in enumerate(rows):
        cells = [(lab.split("\n")[0], w, col) for lab, w, col in r]
        c.fields(hx, 152 + i * (rh + 4), rh, cells, hw)
    c.text(hx, 152 + 6 * (rh + 4) + 4, [("_Routers read only this part (Layer 3) — they never look inside the payload.", MUTED)])
    c.rect(780, 152, 536, 148, [], c="red", shape="round")
    c.text(800, 164, [("#TTL — the loop breaker", PAL["red"][2]), ("Every router subtracts 1.", PAL["red"][2]), ("At 0 the packet is dropped and an", PAL["red"][2]),
                      ("ICMP 'time exceeded' is sent back.", PAL["red"][2]), ("traceroute exploits exactly this.", MUTED)])
    c.rect(1130, 170, 164, 112, [("#64", PAL["red"][3]), "_start", "→ 63 → 62 → …"], c="red", white=True)
    c.rect(780, 316, 536, 90, [], c="orange")
    c.text(800, 326, [("#Protocol — who gets the payload?", PAL["orange"][2]), ("6 → TCP   17 → UDP   1 → ICMP   89 → OSPF", PAL["orange"][2])])
    c.text(800, 380, [("_The value tells the receiving host which Layer-4 handler to hand the data to.", MUTED)])

    c.text(44, 500, [("^2 · READING AN ADDRESS WITH ITS MASK  (192.168.1.77 / 24)", PAL["indigo"][2])])
    bx, by = 44, 538
    octs = ["11000000", "10101000", "00000001", "01001101"]
    dec = ["192", "168", "1", "77"]
    ow = 304
    for i, (b, d) in enumerate(zip(octs, dec)):
        x = bx + i * (ow + 12)
        net = i < 3
        c.rect(x, by, ow, 78, [(f"#{d}", PAL["blue" if net else "green"][2]), (f"~{b}", PAL["blue" if net else "green"][2])], c="blue" if net else "green")
    c.text(bx, by + 92, [("^IP ADDRESS", MUTED)])
    for i in range(4):
        x = bx + i * (ow + 12)
        net = i < 3
        c.rect(x, by + 120, ow, 52, [(f"~{'1' * 8 if net else '0' * 8}", "#FFFFFF")], c="blue" if net else "green", solid=True, shape="rect", shadow=False)
    c.text(bx, by + 180, [("^SUBNET MASK 255.255.255.0 = /24  (24 ones, 8 zeros)", MUTED)])
    c.rect(bx, by + 214, 3 * ow + 24, 56, [("!NETWORK PART  192.168.1.0  — identical for every device on this LAN", PAL["blue"][2])], c="blue", white=True, shape="pill")
    c.rect(bx + 3 * (ow + 12), by + 214, ow, 56, [("!HOST PART  .77", PAL["green"][2])], c="green", white=True, shape="pill")
    cols = [("Network address", "192.168.1.0", "all host bits 0", "gray"), ("First usable", "192.168.1.1", "usually the gateway", "teal"),
            ("Last usable", "192.168.1.254", "2^8 − 2 = 254 hosts", "teal"), ("Broadcast", "192.168.1.255", "all host bits 1", "orange")]
    for i, (a, b, d, col) in enumerate(cols):
        x = bx + i * (ow + 12)
        c.rect(x, by + 290, ow, 86, [f"!{a}", f"#{b}", f"_{d}"], c=col)
    c.footer("", "REMEMBER", lines=["Mask = where the network ends. /24 → 8 host bits → 256 − 2 usable.  Bigger prefix number = smaller network.",
                                    "Router rule: compare destination to routing-table prefixes, longest match wins, TTL − 1, forward."])
    c.save(f"{OUT}/02-packet-header-ipv4-mask")


if __name__ == "__main__":
    d01_models()
    d02_packets()
