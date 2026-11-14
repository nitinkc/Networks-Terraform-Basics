from theory_a import OUT
from dgm import Canvas, PAL, MUTED


def d05_nat():
    c = Canvas(1360, 1100, "NAT and PAT: how private hosts share one public address",
               "The router rewrites the source on the way out and remembers the swap in a table, so replies find their way back", "STAGE 05 · NAT / PAT")
    c.group(44, 130, 326, 380, "INSIDE · 192.168.1.0/24", c="blue")
    c.rect(70, 192, 190, 84, [("#PC1", PAL["blue"][2]), "~192.168.1.10", ("_private, not routable", MUTED)], c="blue", id="pc1")
    c.rect(70, 340, 190, 84, [("#PC2", PAL["purple"][2]), "~192.168.1.11", ("_private, not routable", MUTED)], c="purple", id="pc2")
    c.rect(590, 200, 220, 200, [("#R1 · NAT border", "#FFFFFF"), ("_inside  Gi0/0", "#FFFFFF"), ("~192.168.1.1", "#FFFFFF"), ("_outside Gi0/1", "#FFFFFF"), ("~198.51.100.1", "#FFFFFF")], c="orange", solid=True, id="r1")
    c.group(1050, 130, 266, 380, "OUTSIDE · public internet", c="green")
    c.rect(1070, 232, 226, 140, [("#Web server", PAL["green"][2]), "~203.0.113.50:80", ("_public address", MUTED)], c="green", id="web")
    c.edge("pc1", "r1", "r", "l", via=[(260, 234), (590, 234)], c="blue", w=4)
    c.edge("pc2", "r1", "r", "l", via=[(260, 382), (590, 382)], c="purple", w=4)
    c.line([(810, 234), (1070, 260)], color=PAL["blue"][3], w=4)
    c.line([(810, 382), (1070, 346)], color=PAL["purple"][3], w=4)
    c.rect(378, 246, 206, 62, [("~src 192.168.1.10:51000", PAL["blue"][2]), ("~dst 203.0.113.50:80", MUTED)], c="blue", white=True, shadow=False, pad=8)
    c.rect(378, 388, 206, 62, [("~src 192.168.1.11:51000", PAL["purple"][2]), ("~dst 203.0.113.50:80", MUTED)], c="purple", white=True, shadow=False, pad=8)
    c.rect(822, 190, 222, 62, [("~src 198.51.100.1:51000", PAL["blue"][2]), ("~dst 203.0.113.50:80", MUTED)], c="blue", white=True, shadow=False, pad=8)
    c.rect(822, 392, 222, 62, [("~src 198.51.100.1:51001", PAL["purple"][2]), ("~dst 203.0.113.50:80", MUTED)], c="purple", white=True, shadow=False, pad=8)
    c.text(480, 150, [("^BEFORE NAT", PAL["blue"][2])], anchor="m")
    c.text(933, 150, [("^AFTER NAT", PAL["orange"][2])], anchor="m")
    c.badge(1, 410, 234, "blue")
    c.badge(2, 700, 160, "orange")
    c.rect(500, 462, 400, 60, [("!Both PCs picked source port 51000!", PAL["red"][2]), ("_PAT gives PC2 port 51001 so the two flows stay unique", MUTED)], c="red", white=True, shadow=False)
    c.text(700, 178, [("!Rewrite source + log it", PAL["orange"][2])], anchor="m")

    c.text(44, 548, [("^THE TRANSLATION TABLE (R1's MEMORY)", PAL["indigo"][2])])
    c.table(44, 578, [90, 220, 230, 190], [["Proto", "Inside local", "Inside global", "Outside"],
                                           ["TCP", "192.168.1.10:51000", "198.51.100.1:51000", "203.0.113.50:80"],
                                           ["TCP", "192.168.1.11:51000", "198.51.100.1:51001", "203.0.113.50:80"],
                                           ["TCP", "192.168.1.100:80", "198.51.100.1:8080", "any"]],
            rowh=40, head="orange", mono_cols=(1, 2, 3), rowc=[None, "purple", "green"])
    c.text(44, 748, [("_Return packet arrives with dst 198.51.100.1:51001 → table lookup → rewritten to 192.168.1.11:51000.", MUTED)])
    c.rect(44, 790, 730, 128, [], c="green")
    c.text(64, 802, [("#Static PAT = port forwarding (the green row)", PAL["green"][2])])
    c.rect(64, 846, 190, 54, [("!Internet client", PAL["gray"][2]), ("_connects to :8080", MUTED)], c="gray", white=True, shadow=False)
    c.rect(300, 846, 200, 54, [("!198.51.100.1:8080", PAL["orange"][2]), ("_R1 outside", MUTED)], c="orange", white=True, shadow=False)
    c.rect(546, 846, 210, 54, [("!192.168.1.100:80", PAL["green"][2]), ("_internal web server", MUTED)], c="green", white=True, shadow=False)
    c.line([(254, 873), (300, 873)], color="#5B6677", w=3)
    c.line([(500, 873), (546, 873)], color="#5B6677", w=3)

    gx, gy = 810, 578
    c.text(gx, 548, [("^THE FOUR CISCO TERMS", PAL["indigo"][2])])
    for i, (t, ex, d, col) in enumerate([("Inside local", "192.168.1.10", "inside host, seen from inside", "blue"), ("Inside global", "198.51.100.1", "same host, seen from outside", "orange"),
                                         ("Outside global", "203.0.113.50", "outside host, seen from outside", "green"), ("Outside local", "203.0.113.50", "outside host, seen from inside", "teal")]):
        x, y = gx + (i % 2) * 256, gy + (i // 2) * 108
        c.rect(x, y, 248, 100, [f"!{t}", f"~{ex}", f"_{d}"], c=col, pad=8)
    c.rect(gx, gy + 224, 504, 94, [("!Inside / outside is about WHERE the host lives;", PAL["gray"][2]), ("!local / global is about WHO is looking at the address.", PAL["gray"][2])], c="gray", white=True, shadow=False)
    c.footer("", "REMEMBER", lines=["NAT swaps addresses · PAT also swaps ports so thousands of hosts share one public IP (the 'overload' keyword).",
                                    "Outbound creates the table row; unsolicited inbound has no row → dropped, unless you add a static PAT row."])
    c.save(f"{OUT}/05-nat-pat-translation")


def d06_subnet_dhcp():
    c = Canvas(1360, 1160, "Subnetting a /24 and the DHCP DORA exchange",
               "Borrow host bits to carve address space into subnets; DHCP then leases addresses out of those subnets automatically", "STAGE 06 · SUBNETTING & DHCP")
    c.text(44, 116, [("^1 · SPLIT 192.168.1.0/24 BY BORROWING HOST BITS", PAL["indigo"][2])])
    W = 626
    c.rect(44, 152, W, 78, [("#192.168.1.0 / 24", PAL["indigo"][2]), ("_256 addresses · 254 usable · mask 255.255.255.0", MUTED)], c="indigo", id="p")
    halves = [("192.168.1.0 / 25", ".0 – .127", "126 usable", "blue", 44), ("192.168.1.128 / 25", ".128 – .255", "126 usable", "green", 44 + W / 2 + 2)]
    for i, (n, r, u, col, x) in enumerate(halves):
        c.rect(x, 274, W / 2 - 2, 78, [f"#{n}", f"~{r}", f"_{u}"], c=col, id=f"h{i}")
        c.edge("p", f"h{i}", "b", "t", c="gray", w=2.5, label="borrow 1 bit" if i == 0 else None, lpos=.5, loff=(-60, 0))
    quarters = [("/26", ".0 – .63", "blue", 44), ("/26", ".64 – .127", "indigo", 44 + W / 4 + 1), ("/26", ".128 – .191", "green", 44 + W / 2 + 2), ("/26", ".192 – .255", "teal", 44 + 3 * W / 4 + 3)]
    for i, (n, r, col, x) in enumerate(quarters):
        c.rect(x, 396, W / 4 - 3, 94, [f"#{n}", f"~{r}", "_62 usable"], c=col, id=f"q{i}", pad=4)
        c.edge(f"h{i // 2}", f"q{i}", "b", "t", c="gray", w=2.5)
    c.text(44, 512, [("^BIT VIEW OF THE LAST OCTET  (2 BITS BORROWED → 4 SUBNETS)", MUTED)])
    for i, (b, col) in enumerate([("00", "blue"), ("01", "indigo"), ("10", "green"), ("11", "teal")]):
        x = 44 + i * (W / 4)
        c.rect(x, 544, 44, 46, [(f"!{b}", "#FFFFFF")], c=col, solid=True, shape="rect", shadow=False, pad=2)
        c.rect(x + 44, 544, W / 4 - 48, 46, [("~000000", PAL[col][2])], c=col, shape="rect", shadow=False, pad=4)
    c.text(44, 596, [("_Borrowed bits (solid) pick the subnet · remaining 6 bits (light) pick the host inside it", MUTED)])
    c.table(44, 640, [150, 150, 150, 176], [["Prefix", "Host bits", "Usable hosts", "Typical use"], ["/24", "8", "254", "a small LAN"], ["/26", "6", "62", "a department"], ["/30", "2", "2", "router-to-router link"]],
            rowh=36, head="indigo", mono_cols=(0, 1, 2))
    c.rect(44, 800, W, 62, [("!usable hosts = 2^(host bits) − 2", PAL["yellow"][2]), ("_minus network address (all 0s) and broadcast (all 1s)", MUTED)], c="yellow", white=True, shadow=False)

    c.text(710, 116, [("^2 · DHCP: D · O · R · A", PAL["indigo"][2])])
    c.rect(720, 150, 210, 80, [("#Client", PAL["blue"][2]), ("~0.0.0.0 (no IP yet)", MUTED)], c="blue", id="cl")
    c.rect(1096, 150, 220, 80, [("#DHCP server", PAL["green"][2]), ("~192.168.1.2:67", MUTED)], c="green", id="sv")
    c.lifeline(825, 230, 700)
    c.lifeline(1206, 230, 700)
    steps = [("D", "DISCOVER · broadcast", "“Is there a DHCP server?”   dst 255.255.255.255", "blue", 825, 1206, 308),
             ("O", "OFFER", "“Take 192.168.1.50 for 8 hours”", "green", 1206, 825, 400),
             ("R", "REQUEST · broadcast", "“I accept .50”   (tells other servers to withdraw)", "blue", 825, 1206, 492),
             ("A", "ACK", "“Confirmed — lease starts now”", "green", 1206, 825, 584)]
    for l, t, sub, col, x1, x2, y in steps:
        c.msg(x1, x2, y, t, col, lines=[sub], w=3.5)
        c.badge(l, 742, y - 38, col)
    c.text(1016, 660, [("_UDP: client port 68 ↔ server port 67", MUTED)], anchor="m")
    c.rect(720, 726, 596, 120, [], c="teal")
    c.text(740, 736, [("#What a lease contains", PAL["teal"][2])])
    for i, (k, v) in enumerate([("IP", "192.168.1.50"), ("Mask", "/24"), ("Gateway", "192.168.1.1"), ("DNS", "8.8.8.8"), ("Lease", "8 hours")]):
        c.rect(740 + i * 114, 780, 106, 52, [("^" + k.upper(), PAL["teal"][2]), (f"~{v}", PAL["teal"][2])], c="teal", white=True, shadow=False, pad=2)

    c.text(44, 896, [("^3 · DHCP RELAY — WHEN THE SERVER LIVES ON ANOTHER SUBNET", PAL["indigo"][2])])
    c.rect(44, 930, 250, 80, [("#Client LAN", PAL["blue"][2]), ("~192.168.1.0/24", MUTED)], c="blue", id="rl1")
    c.rect(510, 930, 340, 80, [("#Router · ip helper-address", PAL["orange"][2]), ("~gi0/0 192.168.1.1", MUTED)], c="orange", id="rl2")
    c.rect(1066, 930, 250, 80, [("#DHCP server LAN", PAL["green"][2]), ("~10.0.0.0/24", MUTED)], c="green", id="rl3")
    c.edge("rl1", "rl2", "r", "l", c="blue", w=4, label="broadcast", loff=(0, -26))
    c.edge("rl2", "rl3", "r", "l", c="green", w=4, label="unicast + giaddr", loff=(0, -26))
    c.footer("", "REMEMBER", lines=["DORA = Discover, Offer, Request, Ack. Broadcasts stop at routers, so a relay converts them to unicast.",
                                    "giaddr tells the server which subnet the client is on, so it hands out an address from the right pool."])
    c.save(f"{OUT}/06-subnetting-and-dhcp")


def d07_vlan():
    c = Canvas(1360, 1080, "VLANs and 802.1Q trunks: many networks on one set of switches",
               "VLAN = a separate broadcast domain. Access ports carry one VLAN untagged; trunk ports carry many VLANs with a tag", "STAGE 07 · VLANS")
    for i, (t, col) in enumerate([("VLAN 10 access link", "blue"), ("VLAN 20 access link", "green"), ("802.1Q trunk (many VLANs, tagged)", "purple")]):
        x = 44 + i * 270
        c.line([(x, 124), (x + 36, 124)], c=col, w=5, arrow=None)
        c.text(x + 46, 114, [(f"!{t}", PAL[col][2])])
    c.icon_box("s1", "switch", 330, 330, 110, "yellow", "Switch 1")
    c.icon_box("s2", "switch", 920, 330, 110, "yellow", "Switch 2")
    hosts = [("a", "VLAN 10 · PC-A", "192.168.10.11", "blue", 60, 160), ("b", "VLAN 20 · PC-B", "192.168.20.11", "green", 60, 470),
             ("c", "VLAN 10 · PC-C", "192.168.10.12", "blue", 1100, 160), ("d", "VLAN 20 · PC-D", "192.168.20.12", "green", 1100, 470)]
    for k, n, ip, col, x, y in hosts:
        c.rect(x, y, 200, 80, [f"#{n}", f"~{ip}"], c=col, id=k)
    c.edge("a", "s1", "r", "l.2", c="blue", w=5, arrow=None)
    c.edge("b", "s1", "r", "l.8", c="green", w=5, arrow=None)
    c.edge("c", "s2", "l", "r.2", c="blue", w=5, arrow=None)
    c.edge("d", "s2", "l", "r.8", c="green", w=5, arrow=None)
    c.line([(440, 385), (920, 385)], color="#7C4DDB", w=9, arrow="both")
    c.label(680, 385, "802.1Q TRUNK · VLAN 10 + 20 (tagged)", c="purple", solid=True)
    c.rect(360, 160, 300, 100, [("!Same VLAN = same L2 network", PAL["blue"][2]), ("_PC-A reaches PC-C over the trunk", MUTED), ("_with no router involved", MUTED)], c="blue", white=True, shadow=False)
    c.rect(700, 160, 300, 100, [("!Different VLAN = different net", PAL["red"][2]), ("_PC-A to PC-B must be routed", MUTED), ("_(a router or L3 switch)", MUTED)], c="red", white=True, shadow=False)
    c.icon_box("r", "router", 630, 590, 90, "teal", "Router on a stick")
    c.edge("s1", "r", "b.85", "l", c="purple", color="#7C4DDB", w=7, arrow="both")
    c.rect(780, 590, 300, 90, [("~Gi0/0.10  192.168.10.1", PAL["blue"][2]), ("~Gi0/0.20  192.168.20.1", PAL["green"][2]), ("_one sub-interface per VLAN = its gateway", MUTED)], c="teal", white=True, shadow=False)
    c.text(44, 800, [("^THE 802.1Q TAG · 4 BYTES INSERTED INTO THE ETHERNET HEADER ON TRUNKS", PAL["indigo"][2])])
    cells = [("Dst MAC", 6, "gray"), ("Src MAC", 6, "gray"), ("TPID 0x8100", 4, "purple"), ("PCP 3b", 2.2, "purple"), ("DEI", 1.2, "purple"), ("VID 10", 3.6, "purple"), ("Type", 2, "gray"), ("Payload", 6, "gray"), ("FCS", 2, "gray")]
    c.fields(44, 832, 54, cells, 880)
    c.text(300, 898, [("!◄──  802.1Q tag: 12-bit VLAN ID → 4094 VLANs  ──►", PAL["purple"][2])])
    c.table(950, 800, [100, 130, 136], [["", "Access port", "Trunk port"], ["Carries", "1 VLAN", "many VLANs"], ["Tagged?", "no", "yes (802.1Q)"], ["Connects", "PCs, servers", "switch ↔ switch"]], rowh=36, head="purple")
    c.footer("", "REMEMBER", lines=["VLAN = broadcast domain = (normally) one subnet. Trunk carries them all; the tag says which VLAN each frame belongs to.",
                                    "Traffic between VLANs MUST be routed (router-on-a-stick or Layer 3 switch). ACLs on that router become the policy point."])
    c.save(f"{OUT}/07-vlans-and-trunking")


def d08_routing():
    c = Canvas(1360, 1190, "Static routes, OSPF and BGP: how routers learn paths",
               "OSPF finds the cheapest path inside one organisation; BGP chooses policy-based paths between organisations", "STAGE 08 · ROUTING")
    c.group(44, 130, 760, 470, "OSPF · inside one organisation (Area 0)", c="teal", tag="IP protocol 89")
    c.rect(80, 300, 150, 90, [("#R1", PAL["teal"][2]), ("_source", MUTED)], c="teal", id="r1")
    c.rect(420, 190, 150, 90, [("#R2", PAL["teal"][2])], c="teal", id="r2")
    c.rect(420, 420, 150, 90, [("#R3", PAL["teal"][2])], c="teal", id="r3")
    c.rect(640, 410, 140, 110, [("#10.3.0.0/24", PAL["green"][2]), ("_destination LAN", MUTED)], c="green", id="net")
    c.edge("r1", "r2", "r", "l", via=[(230, 335), (330, 335), (330, 235), (420, 235)], color="#1E9A63", w=7, label="cost 10", lpos=.5, loff=(-16, 0), lc="green")
    c.edge("r2", "r3", "b", "t", color="#1E9A63", w=7, label="cost 10", lpos=.5, loff=(50, 0), lc="green")
    c.edge("r1", "r3", "r", "l", via=[(230, 355), (330, 355), (330, 465), (420, 465)], c="gray", w=3, dash="d", label="cost 100", lpos=.5, loff=(36, 0))
    c.edge("r3", "net", "r", "l", c="gray", w=4)
    c.rect(80, 440, 220, 110, [("!Lowest total cost wins", PAL["green"][2]), ("~R1→R2→R3  = 20", PAL["green"][2]), ("~R1→R3 direct = 100", MUTED)], c="green", white=True, shadow=False)
    c.text(60, 566, [("_① Hello → neighbours   ② flood link-state (LSAs)   ③ identical map (LSDB)   ④ SPF picks cheapest", PAL["teal"][2])])

    c.group(840, 130, 476, 470, "BGP · between organisations (AS)", c="purple", tag="TCP 179")
    for i, (n, sub, col) in enumerate([("AS 65010 · Enterprise", "owns 203.0.113.0/24", "blue"), ("AS 65001 · ISP", "transit provider", "orange"), ("AS 65100 · Content", "serves 198.51.100.0/24", "green")]):
        c.rect(860, 190 + i * 130, 240, 80, [f"#{n}", f"_{sub}"], c=col, id=f"as{i}", pad=6)
    c.edge("as0", "as1", "b", "t", c="purple", w=4, label="eBGP", loff=(34, 0))
    c.edge("as1", "as2", "b", "t", c="purple", w=4, label="eBGP", loff=(34, 0))
    c.rect(1120, 190, 180, 100, [("^ADVERTISES", PAL["purple"][2]), ("~203.0.113.0/24", PAL["purple"][2]), ("~AS_PATH: 65010", MUTED)], c="purple", white=True, shadow=False, pad=2)
    c.rect(1120, 450, 180, 100, [("^LEARNS", PAL["purple"][2]), ("~198.51.100.0/24", PAL["purple"][2]), ("~AS_PATH:", MUTED), ("~65001 65100", MUTED)], c="purple", white=True, shadow=False, pad=2)
    c.text(860, 556, [("_Path-vector: chosen by policy (LOCAL_PREF,", MUTED), ("_AS_PATH length, MED), not by speed", MUTED)])

    c.text(44, 636, [("^ADMINISTRATIVE DISTANCE · WHICH SOURCE TO TRUST (LOWER WINS)", PAL["indigo"][2])])
    for i, (n, ad, col) in enumerate([("Connected", 0, "green"), ("Static", 1, "blue"), ("eBGP", 20, "purple"), ("OSPF", 110, "teal"), ("iBGP", 200, "gray")]):
        y = 672 + i * 50
        c.text(44, y + 12, [(f"!{n}", PAL[col][2])])
        c.rect(150, y, max(40, 2.4 * ad + 40), 36, [(f"!{ad}", "#FFFFFF")], c=col, solid=True, shape="pill", shadow=False, pad=4)
    c.text(760, 636, [("^HOW A ROUTER CHOOSES · IN THIS ORDER", PAL["indigo"][2])])
    for i, (t, d, col) in enumerate([("Longest prefix match", "/26 beats /24 beats /0", "red"), ("Lowest administrative distance", "static 1 beats OSPF 110", "orange"), ("Lowest metric", "OSPF cost, BGP policy attrs", "teal")]):
        y = 672 + i * 80
        c.rect(760, y, 556, 66, [f"!{t}", f"_{d}"], c=col, align="l", pad=70)
        c.badge(i + 1, 800, y + 33, col)
    c.rect(44, 940, 600, 100, [("#Control plane", PAL["blue"][2]), ("_Builds the routing table (OSPF, BGP, static routes)", MUTED), ("_Slow, software, decides WHERE", MUTED)], c="blue")
    c.rect(716, 940, 600, 100, [("#Data plane", PAL["green"][2]), ("_Forwards each packet using that table", MUTED), ("_Fast, per packet, does the sending", MUTED)], c="green")
    c.footer("", "REMEMBER", lines=["Static = you tell it · OSPF = routers share a map and compute cheapest · BGP = organisations trade reachability by policy.",
                                    "Default route 0.0.0.0/0 is just the least specific prefix: 'if nothing better matches, send it that way'."])
    c.save(f"{OUT}/08-routing-static-ospf-bgp")


if __name__ == "__main__":
    for f in (d05_nat, d06_subnet_dhcp, d07_vlan, d08_routing):
        f()
