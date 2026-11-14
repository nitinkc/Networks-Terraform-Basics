from theory_a import OUT
from dgm import Canvas, PAL, MUTED


def d03_arp():
    c = Canvas(1360, 1110, "ARP: finding the MAC address of a neighbour",
               "IP says which network; ARP discovers which physical device on this wire should receive the frame", "STAGE 03 · MAC & ARP")
    actors = [("A", 170, "blue", "Host A", "192.168.1.10", "MAC AA:AA:AA:AA:AA:AA"), ("S", 520, "yellow", "Switch", "Layer 2", "learns MAC → port"),
              ("B", 870, "green", "Gateway B", "192.168.1.1", "MAC BB:BB:BB:BB:BB:BB"), ("C", 1190, "gray", "Host C", "192.168.1.30", "MAC CC:CC:CC:CC:CC:CC")]
    for k, x, col, t, ip, mac in actors:
        c.rect(x - 130, 130, 260, 92, [f"#{t}", f"~{ip}", f"_{mac}"], c=col, id=k)
        c.lifeline(x, 222, 736)
    X = {k: x for k, x, *_ in actors}
    c.msg(X["A"], X["S"], 292, "Request  (broadcast)", "red", lines=["dst FF:FF:FF:FF:FF:FF"], w=3.5)
    c.badge(1, 62, 292, "red")
    c.text(44, 318, [("_“Who has 192.168.1.1?”", MUTED), ("_“Tell 192.168.1.10”", MUTED)])
    c.msg(X["S"], X["B"], 392, "flooded out every port", "red", dash="d", w=3.5)
    c.msg(X["S"], X["C"] - 6, 500, "flooded out every port", "red", dash="d", w=3.5)
    c.rect(X["C"] - 130, 522, 260, 44, [("!Not my IP — silently ignored", PAL["gray"][2])], c="gray", white=True, shape="pill", shadow=False)
    c.rect(X["B"] - 130, 410, 260, 40, [("!“That is me” — learns A MAC", PAL["green"][2])], c="green", white=True, shape="pill", shadow=False)
    c.msg(X["B"], X["S"], 626, "Reply  (unicast)", "green", lines=["“192.168.1.1 is at BB:BB:BB:BB:BB:BB”"], w=3.5)
    c.msg(X["S"], X["A"], 686, "forwarded to A's port only", "green", w=3.5)
    c.badge(2, 62, 626, "green")
    c.text(44, 712, [("_C never sees the reply — switch knows A's port", MUTED)])
    py = 790
    c.rect(44, py, 400, 180, [], c="purple")
    c.text(64, py + 12, [("#③ A caches the answer", PAL["purple"][2])])
    c.table(64, py + 52, [170, 190], [["IP address", "MAC address"], ["192.168.1.1", "BB:BB:BB:BB:BB:BB"]], rowh=34, head="purple", mono_cols=(0, 1))
    c.text(64, py + 126, [("_Reused for ~minutes; view with  arp -a", MUTED)])
    c.rect(470, py, 520, 180, [], c="blue")
    c.text(490, py + 12, [("#The ARP request frame", PAL["blue"][2])])
    c.fields(490, py + 54, 54, [("Dst MAC", 5, "red"), ("Src MAC", 5, "blue"), ("Type", 2, "gray"), ("ARP payload", 7, "purple")], 480, gap=0)
    c.text(490, py + 112, [("_FF:FF:FF:FF:FF:FF = ‘everyone on this LAN’", MUTED), ("_Type 0x0806 = ARP (not IP) — ARP rides directly on Ethernet", MUTED)])
    c.rect(1016, py, 300, 180, [], c="orange")
    c.text(1036, py + 12, [("#ARP stops at the router", PAL["orange"][2]), ("_Broadcast domains end", MUTED), ("_at Layer 3 boundaries:", MUTED)])
    c.rect(1036, py + 90, 90, 40, ["!LAN 1"], c="blue", white=True, shape="pill", shadow=False)
    c.rect(1140, py + 90, 70, 40, ["!R"], c="orange", solid=True, shape="pill", shadow=False)
    c.rect(1224, py + 90, 76 - 4, 40, ["!LAN 2"], c="green", white=True, shape="pill", shadow=False, pad=4)
    c.text(1126, py + 136, [("^✗ broadcast blocked", PAL["red"][2])], anchor="m")
    c.footer("", "REMEMBER", lines=["IP = which network (changes per network) · MAC = which device on this wire (rewritten at every hop).",
                                    "ARP = broadcast question, unicast answer, then cache. Unauthenticated → ARP spoofing; defence = Dynamic ARP Inspection."])
    c.save(f"{OUT}/03-arp-resolution")


def d04_switch_router():
    c = Canvas(1360, 1040, "Switch vs router: two different forwarding decisions",
               "A switch moves frames inside one network by MAC; a router moves packets between networks by IP prefix", "STAGE 04 · SWITCH VS ROUTER")
    c.group(44, 130, 620, 440, "SWITCH · Layer 2 · learns MAC → port", c="yellow")
    c.icon_box("sw", "switch", 304, 200, 100, "yellow", "Switch0")
    for i, (nm, mac, col, x, y) in enumerate([("PC-A", "AA:AA", "blue", 90, 190), ("PC-B", "BB:BB", "green", 90, 360), ("PC-C", "CC:CC", "purple", 480, 190), ("PC-D", "DD:DD", "pink", 480, 360)]):
        c.rect(x, y, 140, 76, [f"#{nm}", f"~{mac}"], c=col, id=nm)
    c.edge("PC-A", "sw", "r", "l", via=[(230, 228), (230, 250), (304, 250)], c="blue", w=3, label="Fa0/1", lpos=.25, loff=(0, -2))
    c.edge("PC-B", "sw", "r", "l", via=[(230, 398), (270, 398), (270, 270), (304, 270)], c="green", w=3, label="Fa0/2", lpos=.4, loff=(-4, 18))
    c.edge("PC-C", "sw", "l", "r", via=[(450, 228), (450, 250), (404, 250)], c="purple", w=3, label="Fa0/3", lpos=.35, loff=(2, -18))
    c.edge("PC-D", "sw", "l", "r", via=[(450, 398), (430, 398), (430, 270), (404, 270)], c="pink", w=3, label="Fa0/4", lpos=.45, loff=(8, 22))
    c.text(64, 450, [("!MAC address table  (built by watching source MACs)", PAL["yellow"][2])])
    c.table(64, 478, [150, 110, 340], [["MAC", "Port", "Decision"], ["AA:AA", "Fa0/1", "learned from A's first frame"]], rowh=30, head="yellow", mono_cols=(0, 1))
    c.text(64, 540, [("_Dest known → send out one port.  Dest unknown / broadcast → flood all ports except ingress.", MUTED)])

    c.group(696, 130, 620, 440, "ROUTER · Layer 3 · routes by IP prefix", c="teal")
    c.icon_box("rt", "router", 720, 200, 86, "teal", "R1")
    c.table(830, 190, [170, 150, 130], [["Prefix", "Next hop", "Out"], ["192.168.1.0/24", "connected", "Gi0/0"], ["10.0.0.0/24", "connected", "Gi0/1"], ["0.0.0.0/0", "203.0.113.2", "Gi0/2"]],
            rowh=34, head="teal", mono_cols=(0, 1, 2))
    steps = [("1", "Read destination IP, check TTL"), ("2", "Longest-prefix match in routing table"), ("3", "ARP for next hop's MAC"), ("4", "Rewrite L2 header, TTL − 1, send")]
    for i, (n, t) in enumerate(steps):
        y = 352 + i * 51
        c.badge(n, 730, y + 18, "teal")
        c.text(758, y + 5, [(f"!{t}", PAL["teal"][2])])
    c.rect(1156, 450, 140, 90, [("^LONGEST MATCH", PAL["orange"][2]), ("!/26 beats /24", PAL["orange"][2]), ("!/24 beats /0", PAL["orange"][2])], c="orange", white=True, pad=4)

    c.text(44, 598, [("^ONE PACKET, TWO HOPS · WHAT CHANGES AND WHAT STAYS", PAL["indigo"][2])])
    c.rect(44, 636, 150, 70, [("#Host A", PAL["blue"][2]), "~192.168.1.10"], c="blue", id="ha")
    c.rect(560, 636, 240, 70, [("#Router R1", PAL["teal"][2]), "~Gi0/0 .1  |  Gi0/1 .1"], c="teal", id="hr")
    c.rect(1166, 636, 150, 70, [("#Host B", PAL["green"][2]), "~10.0.0.20"], c="green", id="hb")
    c.edge("ha", "hr", "r", "l", c="gray", w=4, label="hop 1 · Ethernet LAN 192.168.1.0/24", lpos=.5, loff=(0, -26))
    c.edge("hr", "hb", "r", "l", c="gray", w=4, label="hop 2 · Ethernet LAN 10.0.0.0/24", lpos=.5, loff=(0, -26))
    for i, (x0, ttl, smac, dmac) in enumerate([(44, "64", "A  (AA:AA)", "R1 Gi0/0"), (700, "63", "R1 Gi0/1", "B  (BB:BB)")]):
        w = 616
        c.rect(x0, 736, w, 190, [], c="gray", white=True)
        c.text(x0 + 18, 748, [(f"!Frame on hop {i + 1}", PAL["gray"][2])])
        c.fields(x0 + 18, 782, 50, [(f"L2 src: {smac}", 4, "orange"), (f"L2 dst: {dmac}", 4, "orange")], w - 36, gap=4)
        c.fields(x0 + 18, 842, 50, [("L3 src 192.168.1.10", 4, "green"), ("L3 dst 10.0.0.20", 4, "green"), (f"TTL {ttl}", 2, "red")], w - 36, gap=4)
        c.text(x0 + 18, 898, [("_Orange = rewritten every hop  ·  Green = end-to-end, never changes  ·  Red = −1 per router", MUTED)])
    c.footer("", "REMEMBER", lines=["Switch: same network, MAC table, floods unknowns.   Router: different networks, routing table, drops broadcasts.",
                                    "L3 addresses are end-to-end; L2 addresses are only valid for the current hop."])
    c.save(f"{OUT}/04-switch-vs-router")


if __name__ == "__main__":
    d03_arp()
    d04_switch_router()
