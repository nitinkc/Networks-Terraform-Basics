from theory_a import OUT
from theory_d import cross
from dgm import Canvas, PAL, MUTED


def d13_firewall():
    c = Canvas(1360, 1090, "Firewalls: stateless filtering vs stateful connection tracking",
               "A stateful firewall remembers outbound conversations, so replies are allowed automatically and unsolicited traffic is not", "STAGE 13 · FIREWALLS")
    for x0, title, col, stateful in [(44, "STATELESS · classic ACL · judges every packet alone", "orange", False), (700, "STATEFUL · remembers connections", "green", True)]:
        c.group(x0, 130, 616, 450, title, c=col)
        c.rect(x0 + 24, 200, 150, 76, [("#Client", PAL["blue"][2]), ("~10.0.0.5", MUTED)], c="blue")
        c.rect(x0 + 442, 200, 150, 76, [("#Server", PAL["green"][2]), ("~203.0.113.9:443", MUTED)], c="green", pad=4)
        c.line([(x0 + 174, 238), (x0 + 442, 238)], color="#2F6FE0", w=4)
        c.text(x0 + 308, 322, [("!① request  :51000 → :443", PAL["blue"][2])], anchor="m")
        c.text(x0 + 308, 346, [("_permitted by the outbound rule", MUTED)], anchor="m")
        c.icon("firewall", x0 + 268, 196, 80, "red", "Firewall")
        c.line([(x0 + 442, 400), (x0 + 174, 400)], color="#1E9A63" if stateful else "#D93F3F", w=4)
        c.text(x0 + 308, 424, [("!② reply  :443 → :51000", PAL["green" if stateful else "red"][2])], anchor="m")
        if stateful:
            c.text(x0 + 308, 448, [("_matches the connection table → allowed", MUTED)], anchor="m")
            c.rect(x0 + 24, 480, 568, 80, [], c="green", white=True, shadow=False)
            c.text(x0 + 40, 488, [("!Connection table (state)", PAL["green"][2]), ("~TCP 10.0.0.5:51000 → 203.0.113.9:443   ESTABLISHED", PAL["green"][2]), ("~unsolicited SYN from outside → no entry → DROP", PAL["red"][2])])
        else:
            cross(c, x0 + 308, 400)
            c.text(x0 + 308, 448, [("_no rule says 'permit :443 → inside' → dropped", MUTED)], anchor="m")
            c.rect(x0 + 24, 480, 568, 80, [], c="orange", white=True, shadow=False)
            c.text(x0 + 40, 488, [("!Needs TWO rules to work", PAL["orange"][2]), ("~1 permit tcp inside → any eq 443", PAL["orange"][2]), ("~2 permit tcp any eq 443 → inside  (reply rule, risky)", PAL["orange"][2])])
    c.text(44, 620, [("^SECURITY ZONES · POLICY IS WRITTEN PER DIRECTION", PAL["indigo"][2])])
    c.rect(44, 700, 170, 90, [("#Inside", PAL["green"][2]), ("_trusted users", MUTED), ("~10.0.0.0/16", MUTED)], c="green", id="zi")
    c.rect(470, 700, 170, 90, [("#Outside", PAL["red"][2]), ("_the internet", MUTED), ("~0.0.0.0/0", MUTED)], c="red", id="zo")
    c.rect(255, 850, 180, 90, [("#DMZ", PAL["orange"][2]), ("_public-facing servers", MUTED), ("~10.9.0.0/24", MUTED)], c="orange", id="zd", pad=4)
    c.line([(214, 745), (300, 745)], color="#5B6677", w=4, arrow="both")
    c.line([(390, 745), (470, 745)], color="#5B6677", w=4, arrow="both")
    c.line([(345, 790), (345, 850)], color="#5B6677", w=4, arrow="both")
    c.icon("firewall", 300, 690, 90, "red")
    c.text(345, 664, [("^FIREWALL", PAL["red"][2])], anchor="m")
    grid = [["FROM \\ TO", "Inside", "DMZ", "Outside"], ["Inside", "—", "✓ allow", "✓ allow"], ["DMZ", "✗ deny", "—", "✓ updates only"], ["Outside", "✗ deny (new)", "✓ 443 only", "—"]]
    cl = {"✓": "green", "✗": "red", "—": "gray"}
    for r, row in enumerate(grid):
        for k, cell in enumerate(row):
            x, y = 680 + [0, 150, 312, 474][k], 700 + r * 56
            w = [150, 162, 162, 162][k]
            if r == 0 or k == 0:
                c.rect(x, y, w, 52, [f"!{cell}"], c="indigo", solid=True, shape="rect", sw=1, shadow=False, pad=4)
            else:
                c.rect(x, y, w, 52, [(f"!{cell}", PAL[cl[cell[0]]][2])], c=cl[cell[0]], shape="rect", sw=1, shadow=False, pad=4)
    c.text(680, 934, [("_Reading: row = where traffic starts, column = where it is going. Anything not listed is denied.", MUTED)])
    c.footer("", "REMEMBER", lines=["Stateful = a table of established connections. Reply traffic is allowed because the firewall remembers the request.",
                                    "Default posture: deny everything crossing zones, then permit only what each application genuinely needs."])
    c.save(f"{OUT}/13-stateless-vs-stateful-firewall")


def d14_vpn_proxy_lb():
    c = Canvas(1360, 1290, "VPNs, proxies and load balancers: three kinds of middlemen",
               "A VPN protects a path, a proxy speaks for one side, a load balancer spreads requests across many servers", "STAGE 14 · VPN · PROXY · LB")
    c.group(44, 130, 1272, 300, "VPN · a private tunnel across a public network", c="purple", tag="IPsec / WireGuard")
    c.rect(70, 215, 190, 90, [("#Branch LAN", PAL["blue"][2]), ("~10.0.0.0/24", MUTED)], c="blue", id="br")
    c.rect(310, 215, 190, 90, [("#VPN gateway A", PAL["teal"][2]), ("~198.51.100.1", MUTED)], c="teal", id="ga")
    c.icon("cloud", 590, 190, 100, "gray")
    c.text(665, 330, [("^PUBLIC INTERNET", MUTED)], anchor="m")
    c.rect(870, 215, 190, 90, [("#VPN gateway B", PAL["teal"][2]), ("~203.0.113.9", MUTED)], c="teal", id="gb")
    c.rect(1110, 215, 190, 90, [("#Data centre", PAL["green"][2]), ("~172.16.0.0/16", MUTED)], c="green", id="dc")
    c.line([(500, 260), (870, 260)], color="#7C4DDB", w=14, arrow="both")
    c.line([(500, 260), (870, 260)], color="#C4A8FF", w=3, arrow=None, dash="d")
    c.label(685, 260, "ESP TUNNEL", c="purple", solid=True)
    c.line([(260, 260), (310, 260)], color="#2F6FE0", w=4, arrow=None)
    c.line([(1060, 260), (1110, 260)], color="#1E9A63", w=4, arrow=None)
    c.text(310, 346, [("^WHAT THE INTERNET SEES", PAL["purple"][2])])
    c.fields(310, 374, 40, [("New IP: A → B", 3, "gray"), ("ESP hdr", 1.6, "purple"), ("Original packet 10.0.0.5 → 172.16.1.8  (encrypted)", 7, "green"), ("ESP trailer", 1.8, "purple")], 990)
    c.group(44, 460, 1272, 300, "PROXIES · an intermediary that talks on someone's behalf", c="orange")
    for x0, ttl, nodes, cap, col, ex in [(64, "FORWARD PROXY", [("Clients", "inside", "blue"), ("Forward proxy", "filter · cache · log", "orange"), ("Internet", "any website", "gray")], "hides the CLIENT · controls egress", "orange", "Squid · corporate web filter · secure web gateway"),
                                     (690, "REVERSE PROXY", [("Internet users", "anyone", "gray"), ("Reverse proxy", "TLS · cache · WAF", "orange"), ("Backends", "private servers", "green")], "hides the SERVER · one front door", "orange", "NGINX · HAProxy · Envoy · CDN · F5 XC edge")]:
        c.text(x0, 512, [(f"^{ttl}", PAL["orange"][2])])
        xs = [x0, x0 + 215, x0 + 430]
        ids = []
        for i, (t, sub, cc) in enumerate(nodes):
            c.rect(xs[i], 548, 170, 84, [f"#{t}", f"_{sub}"], c=cc, id=f"{ttl}{i}", pad=4)
            ids.append(f"{ttl}{i}")
        c.edge(ids[0], ids[1], "r", "l", c="gray", w=4)
        c.edge(ids[1], ids[2], "r", "l", c="gray", w=4)
        c.text(x0, 660, [(f"!{cap}", PAL["orange"][2])])
        c.text(x0, 694, [(f"_{ex}", MUTED)])
    c.group(44, 790, 1272, 330, "LOAD BALANCER · one address in front of many servers", c="teal")
    c.rect(70, 900, 160, 80, [("#Clients", PAL["blue"][2]), ("~many users", MUTED)], c="blue", id="lc")
    c.rect(300, 880, 240, 120, [("#Load balancer", "#FFFFFF"), ("~VIP 203.0.113.10:443", "#E0F7F7"), ("_health checks every 5 s", "#E0F7F7")], c="teal", solid=True, id="lb", pad=4)
    for i, (n, st, col) in enumerate([("web-1", "healthy ✓", "green"), ("web-2", "healthy ✓", "green"), ("web-3", "failed ✗ removed", "red")]):
        c.rect(640, 850 + i * 86, 220, 70, [f"#{n}", f"_{st}"], c=col, id=f"w{i}", dash="d" if i == 2 else None)
        c.edge("lb", f"w{i}", "r", "l", c="gray" if i < 2 else "red", w=3.5, dash="d" if i == 2 else None)
    c.edge("lc", "lb", "r", "l", c="gray", w=4)
    c.table(920, 840, [70, 140, 186], [["", "Layer 4", "Layer 7"], ["Sees", "IP + port", "URL · host · cookies"], ["Speed", "fastest", "smarter, slower"], ["Use", "any TCP/UDP", "HTTP routing"]], rowh=34, head="teal")
    for i, a in enumerate(["round-robin", "least connections", "IP hash", "weighted"]):
        c.rect(920 + (i % 2) * 190, 1000 + (i // 2) * 52, 182, 44, [(f"!{a}", "#FFFFFF")], c="teal", solid=True, shape="pill", shadow=False, pad=4)
    c.footer("", "REMEMBER", lines=["VPN = encrypt a path between networks.  Proxy = terminate the connection and re-open it for someone else.",
                                    "Load balancer = a reverse proxy that picks a healthy backend, giving scale and resilience behind one address."])
    c.save(f"{OUT}/14-vpn-proxy-load-balancer")


def d15_cloud():
    c = Canvas(1360, 1170, "Cloud and hybrid networking: the same ideas with new names",
               "Every cloud building block maps to something you already built in Packet Tracer, now defined as software and managed by Terraform", "STAGE 15 · CLOUD & HYBRID")
    c.icon("cloud", 56, 150, 90, "gray")
    c.text(122, 262, [("^INTERNET", MUTED)], anchor="m")
    c.group(40, 330, 330, 290, "ON-PREMISES · 10.0.0.0/16", c="blue")
    c.icon_box("opr", "router", 70, 390, 70, "teal", "Cisco router")
    c.icon_box("opc", "pc", 250, 396, 80, "blue", "Office PCs")
    c.group(460, 170, 856, 450, "GOOGLE CLOUD · VPC network (global)", c="indigo", tag="custom mode")
    c.rect(500, 226, 250, 50, [("!External HTTPS LB", "#FFFFFF")], c="orange", solid=True, shape="pill", id="lb", shadow=False)
    c.rect(1040, 226, 250, 50, [("!Cloud NAT (egress only)", "#FFFFFF")], c="teal", solid=True, shape="pill", id="nat", shadow=False)
    c.group(484, 320, 390, 270, "Subnet web · 10.10.1.0/24", c="green", tag="us-central1", hh=34)
    c.group(902, 320, 390, 270, "Subnet app · 10.10.2.0/24", c="purple", tag="europe-west1", hh=34)
    for i, (n, ip) in enumerate([("web-1", "10.10.1.10"), ("web-2", "10.10.1.11")]):
        c.rect(506 + i * 178, 376, 164, 70, [f"#{n}", f"~{ip}"], c="green", white=True, id=f"vw{i}", shadow=False)
    for i, (n, ip) in enumerate([("app-1", "10.10.2.10"), ("app-2", "10.10.2.11")]):
        c.rect(924 + i * 178, 376, 164, 70, [f"#{n}", f"~{ip}"], c="purple", white=True, id=f"va{i}", shadow=False)
    c.rect(506, 476, 346, 92, [("!VPC firewall rules (stateful)", PAL["red"][2]), ("_allow tcp:443 from internet to tag 'web'", MUTED), ("_default: deny ingress, allow egress", MUTED)], c="red", white=True, shadow=False, id="fw1")
    c.rect(924, 476, 346, 92, [("!Internal path (no router to build)", PAL["indigo"][2]), ("_subnets route to each other automatically", MUTED), ("_allow tcp:8080 only from tag 'web'", MUTED)], c="indigo", white=True, shadow=False, id="fw2")
    c.line([(146, 195), (500, 251)], color="#E8890C", w=4)
    c.label(300, 223, "users → HTTPS", c="orange")
    c.line([(1165, 226), (1165, 150), (120, 150)], color="#12908A", w=4)
    c.label(780, 150, "egress to internet via NAT", c="teal")
    c.line([(140, 425), (460, 425)], color="#7C4DDB", w=8, arrow="both")
    c.label(300, 425, "Cloud VPN / Interconnect + BGP", c="purple", solid=True)
    c.text(44, 650, [("^CLASSIC TERM → CLOUD TERM → TERRAFORM RESOURCE", PAL["indigo"][2])])
    rows = [["Classic / Packet Tracer", "Google Cloud", "Terraform resource", "Practised in"],
            ["Switch, VLAN, subnet", "VPC subnet (regional)", "google_compute_subnetwork", "TF Lab 02"],
            ["Router, static routes", "Routes, Cloud Router", "google_compute_route / router", "TF Lab 03"],
            ["ACL / firewall", "VPC firewall rules", "google_compute_firewall", "TF Lab 03"],
            ["NAT / PAT", "Cloud NAT", "google_compute_router_nat", "TF Lab 03"],
            ["DNS server", "Cloud DNS private zone", "google_dns_managed_zone", "TF Lab 04"],
            ["Peering / WAN link", "VPC peering · Shared VPC", "google_compute_network_peering", "TF Lab 06"],
            ["Load balancer", "Cloud Load Balancing", "google_compute_forwarding_rule", "TF Lab 07"],
            ["IPsec VPN + BGP", "HA VPN + Cloud Router", "google_compute_ha_vpn_gateway", "TF Lab 08"]]
    c.table(44, 686, [300, 330, 410, 232], rows, rowh=38, head="indigo", mono_cols=(2,))
    c.footer("", "REMEMBER", lines=["Nothing new at the packet level: still IP, subnets, routes, firewalls, NAT and DNS — just declared in code.",
                                    "Terraform describes the desired network; the cloud provider builds and operates the 'switches and routers' for you."])
    c.save(f"{OUT}/15-cloud-hybrid-concept-map")


if __name__ == "__main__":
    for f in (d13_firewall, d14_vpn_proxy_lb, d15_cloud):
        f()
