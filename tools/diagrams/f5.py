from dgm import Canvas, PAL, MUTED
from labkit import out, steps, cmds, wrap
from theory_d import cross

T = "theory/diagrams/"


def f5_architecture():
    c = Canvas(1360, 1000, "F5 Distributed Cloud: platform architecture",
               "Clients meet a Regional Edge, the Regional Edge reaches your private site over an encrypted tunnel, and one SaaS control plane configures all of it", "STAGE 16 · F5 XC PLATFORM")
    c.rect(350, 130, 966, 80, [("#XC control plane · SaaS", PAL["red"][2]), ("_tenant · namespaces · sites · policies · PKI  —  one REST API used by both the Console and Terraform", MUTED)], c="red", id="cp")
    c.group(44, 250, 262, 520, "CLIENTS", c="blue")
    for i, (t, s) in enumerate([("Browser", "portal.example.com"), ("Mobile app", "api.example.com"), ("Partner system", "machine to machine")]):
        c.rect(64, 308 + i * 108, 222, 88, [f"#{t}", f"~{s}"], c="blue", white=True, id=f"cl{i}", shadow=False)
    c.rect(64, 640, 222, 110, [("!DNS returns a VIP", PAL["blue"][2]), ("!Routing selects an RE", PAL["blue"][2]), ("_anycast entry, no VPN", MUTED)], c="blue", white=True, shadow=False)
    c.group(350, 250, 490, 520, "F5 XC GLOBAL ADN · REGIONAL EDGES", c="orange")
    for i, (t, d) in enumerate([("RE · Americas", "anycast VIP · TLS termination · WAF · L7 routing"), ("RE · Europe", "anycast VIP · TLS termination · WAF · L7 routing"), ("RE · Asia-Pacific", "anycast VIP · TLS termination · WAF · L7 routing")]):
        c.rect(374, 304 + i * 108, 442, 90, [f"#{t}", f"_{d}"], c="orange", white=True, id=f"re{i}", shadow=False, pad=4)
    c.rect(374, 634, 442, 52, [("!Encrypted site-mesh tunnels on a private backbone", PAL["purple"][2])], c="purple", white=True, shape="pill", shadow=False, pad=4)
    c.rect(374, 698, 442, 56, [("_per request: LB objects · origin pools · health checks", MUTED), ("_WAF · service policy · rate limits · bot defense", MUTED)], c="gray", white=True, shadow=False, pad=4)
    c.group(900, 250, 416, 520, "CUSTOMER INFRASTRUCTURE", c="green")
    c.group(920, 306, 376, 210, "SITE · GCP project gcp-xc-lab", c="teal", hh=34)
    c.rect(940, 356, 336, 70, [("#Customer Edge (CE)", PAL["teal"][2]), ("_SLO + SLI interfaces · XC-managed VM", MUTED)], c="teal", white=True, id="ce1", shadow=False)
    c.rect(940, 438, 336, 60, [("!Origin 10.200.0.10:80", PAL["green"][2]), ("_private · no public IP", MUTED)], c="green", white=True, shadow=False, id="o1")
    c.group(920, 536, 376, 210, "SITE · data center / other cloud", c="purple", hh=34)
    c.rect(940, 586, 336, 70, [("#Customer Edge (CE)", PAL["purple"][2]), ("_VMware · bare metal · AWS · Azure", MUTED)], c="purple", white=True, id="ce2", shadow=False)
    c.rect(940, 668, 336, 60, [("!Legacy apps · databases", PAL["gray"][2]), ("_reached the same way", MUTED)], c="gray", white=True, shadow=False)
    for i in range(3):
        c.edge(f"cl{i}", f"re{i}", "r", "l", c="blue", w=4, label="HTTPS" if i == 0 else None, lc="blue")
    c.line([(816, 349), (870, 349), (870, 391), (940, 391)], color="#7C4DDB", w=7, dash="d")
    c.line([(816, 457), (880, 457), (880, 621), (940, 621)], color="#7C4DDB", w=7, dash="d")
    c.label(868, 420, "tunnel", c="purple", solid=True)
    c.line([(600, 210), (600, 250)], color="#D93F3F", w=3, dash="d")
    c.line([(1100, 210), (1100, 250)], color="#D93F3F", w=3, dash="d")
    c.label(600, 230, "policy push", c="red")
    c.label(1100, 230, "config + certs", c="red")
    c.text(44, 800, [("^LEGEND", PAL["indigo"][2])])
    for i, (t, col) in enumerate([("Regional Edge · F5-owned", "orange"), ("Customer Edge · your site", "teal"), ("Control plane", "red"), ("Encrypted tunnel", "purple")]):
        c.rect(44 + i * 318, 832, 306, 44, [(f"!{t}", "#FFFFFF")], c=col, solid=True, shape="pill", shadow=False)
    c.footer("", "REMEMBER", lines=["Clients never learn backend addresses: every request ends at a Regional Edge, is inspected and policy-checked,",
                                    "then rides an encrypted tunnel to the Customer Edge that owns the inside route to the origin."])
    c.save(out(T + "f5-xc-architecture"))


def f5_anycast():
    c = Canvas(1360, 1000, "Anycast: one public VIP, multiple possible edges",
               "DNS supplies an address; network routing selects an edge; XC load balancing selects a healthy private origin", "STAGE 17 · ANYCAST")
    c.group(44, 130, 1272, 190, "UNICAST · ONE SPECIFIC DESTINATION", c="blue")
    c.rect(70, 194, 260, 80, ["#Client", "_destination: 192.0.2.10"], c="blue", white=True, id="uc")
    c.rect(520, 194, 300, 80, ["#Network routing", "_route toward one destination"], c="gray", white=True, id="ur")
    c.rect(1010, 194, 280, 80, ["#Service at one location", "~192.0.2.10"], c="blue", white=True, id="us")
    c.edge("uc", "ur", c="blue", w=4)
    c.edge("ur", "us", c="blue", w=4)
    c.group(44, 350, 1272, 350, "ANYCAST · SAME VIP AT PARTICIPATING LOCATIONS", c="orange")
    c.rect(70, 416, 260, 96, ["#Client A", "_DNS returns shared VIP", "~203.0.113.10"], c="blue", white=True, id="a")
    c.rect(70, 566, 260, 96, ["#Client B", "_DNS returns SAME VIP", "~203.0.113.10"], c="purple", white=True, id="b")
    c.rect(480, 416, 320, 96, ["#Routing from network A", "_selected BGP route to RE A", "_not a DNS proximity decision"], c="blue", white=True, id="ra")
    c.rect(480, 566, 320, 96, ["#Routing from network B", "_selected BGP route to RE B", "_not packet replication"], c="purple", white=True, id="rb")
    for suffix, y, col in [("a", 416, "blue"), ("b", 566, "purple")]:
        c.rect(1010, y, 280, 96, [f"#Regional Edge {suffix.upper()}", "~VIP 203.0.113.10", "_advertises containing prefix"], c="orange", white=True, id=f"re{suffix}")
        c.edge(suffix, f"r{suffix}", c=col, w=4)
        c.edge(f"r{suffix}", f"re{suffix}", c=col, w=4)
    c.text(44, 722, [("^AFTER INGRESS · A SEPARATE DECISION AT THE SELECTED RE", PAL["indigo"][2])])
    stages = [("TLS + WAF", "inspect request", "orange"), ("Origin selection", "policy + health checks", "pink"), ("RE–CE tunnel", "encrypted site path", "purple"), ("CE → private origin", "unicast: 10.200.0.10", "green")]
    for i, (title, detail, col) in enumerate(stages):
        c.rect(44 + i * 326, 760, 294, 80, [f"#{title}", f"_{detail}"], c=col, id=f"post{i}")
        if i:
            c.edge(f"post{i - 1}", f"post{i}", c="gray", w=3)
    c.footer("", "REMEMBER", lines=["Best route is not necessarily geographically closest. Route withdrawal needs convergence; existing sessions can break.",
                                    "Public IPs shown are documentation examples. Anycast chooses an edge, not a backend; no request is copied to all REs."])
    c.save(out(T + "f5-xc-anycast"))


def f5_slo_sli():
    c = Canvas(1360, 1060, "Customer Edge on GCP: two VPCs, two interfaces (SLO / SLI)",
               "GCP allows one NIC per VPC, so a CE with an outside and an inside network is dual-homed across two VPCs", "STAGE 17 · SITE NETWORKING")
    c.icon("cloud", 400, 125, 70, "orange")
    c.text(452, 200, [("!Regional Edges + clients", PAL["orange"][2])], anchor="m")
    c.rect(1000, 130, 316, 70, [("#XC control plane (SaaS)", PAL["red"][2]), ("_registration · config · certificates", MUTED)], c="red", id="cp")
    c.group(44, 280, 470, 400, "xc-outside-vpc · SLO · 10.190.0.0/24", c="orange")
    c.rect(70, 340, 418, 100, [("#NIC 0 · SLO", PAL["orange"][2]), ("~10.190.0.x + external IP", PAL["orange"][2]), ("_control plane + RE tunnels terminate here", MUTED)], c="orange", white=True, id="slo", shadow=False)
    c.rect(70, 462, 418, 80, [("!Egress", PAL["gray"][2]), ("_default internet route · no inbound listeners needed", MUTED)], c="gray", white=True, shadow=False)
    c.rect(70, 560, 418, 94, [("!Firewall philosophy", PAL["orange"][2]), ("_the outside VPC only needs egress rules —", MUTED), ("_the CE dials out to the RE and the control plane", MUTED)], c="orange", white=True, shadow=False)
    c.group(846, 280, 470, 400, "xc-inside-vpc · SLI · 10.200.0.0/24", c="green")
    c.rect(872, 340, 418, 100, [("#NIC 1 · SLI", PAL["green"][2]), ("~10.200.0.x · private only", PAL["green"][2]), ("_reaches origins over private addresses", MUTED)], c="green", white=True, id="sli", shadow=False)
    c.rect(872, 462, 270, 106, [("#web-inside", PAL["green"][2]), ("~10.200.0.10:80 · NGINX", MUTED), ("!NO external IP — ever", PAL["red"][2]), ("~tag: xc-origin", MUTED)], c="green", white=True, id="web", shadow=False)
    c.rect(1160, 462, 130, 106, [("!Cloud NAT", PAL["teal"][2]), ("_egress only,", MUTED), ("_installs not", MUTED), ("_inbound", MUTED)], c="teal", white=True, shadow=False, pad=4)
    c.rect(872, 584, 418, 74, [("!VPC firewall (inside)", PAL["red"][2]), ("~allow tcp:80 · src 10.200.0.0/24 · tag xc-origin", MUTED)], c="red", white=True, shadow=False, pad=4)
    c.rect(560, 380, 240, 200, [("^CE NODE", "#FFFFFF"), ("#ce-gcp-01", "#FFFFFF"), ("_XC-managed VM", "#FFFFFF"), ("_site gcp-xc-lab", "#FFFFFF"), ("!only device that", "#FFFFFF"), ("!crosses the boundary", "#FFFFFF")], c="teal", solid=True, id="ce", pad=4)
    c.edge("slo", "ce", "r", "l.25", c="orange", w=6, arrow="both")
    c.line([(800, 410), (872, 390)], color="#1E9A63", w=6, arrow="both")
    c.line([(452, 230), (452, 340)], color="#7C4DDB", w=5, dash="d")
    c.label(452, 304, "tunnels", c="purple", solid=True)
    c.line([(1080, 200), (1080, 266), (200, 266), (200, 340)], color="#D93F3F", w=3, dash="d")
    c.label(700, 266, "token → pending → approve → cert", c="red")
    c.line([(800, 540), (872, 520)], color="#1E9A63", w=5)
    c.rect(560, 600, 240, 60, [("!✗ no direct path", PAL["red"][2]), ("_from the internet to origins", MUTED)], c="red", white=True, shadow=False)
    c.text(44, 716, [("^TRUST MODEL · HOW A CE JOINS A SITE", PAL["indigo"][2])])
    for i, (t, d, col) in enumerate([("1 · Site token", "generated in the Console, baked into VM metadata", "blue"), ("2 · CE calls home", "token + hardware ID over the SLO interface", "purple"), ("3 · Admin approves", "pending registration — explicit human gate", "orange"), ("4 · Site goes UP", "certificate + config pushed; SLO/SLI report healthy", "green")]):
        x = 44 + i * 318
        c.rect(x, 752, 306, 110, [f"#{t}"] + [(f"_{l}", None) for l in wrap(d, 36)], c=col, pad=6)
        if i:
            c.line([(x - 12, 807), (x, 807)], color="#5B6677", w=3)
    c.table(44, 896, [320, 480, 472], [["Interface", "Lives in", "Used for"], ["SLO · Site Local Outside", "xc-outside-vpc / slo-subnet", "reaching the RE and control plane"], ["SLI · Site Local Inside", "xc-inside-vpc / sli-subnet", "reaching private origins"]], rowh=36, head="indigo")
    c.save(out(T + "f5-xc-slo-sli-gcp"))


def f5_request_path():
    c = Canvas(1360, 1060, "The request path: client to a private GCP origin",
               "Six stages, each answering a different question; walk them in order when something breaks", "STAGE 18 · TRAFFIC & SECURITY")
    stages = [("Client", "browser → lb.example.com", "blue"), ("DNS", "resolves to anycast VIP", "purple"), ("Regional Edge", "TLS · WAF · pick origin", "orange"), ("RE → CE tunnel", "encrypted, no public path", "teal"), ("Customer Edge", "SLI → private origin", "green"), ("Origin", "10.200.0.10:80", "pink")]
    for i, (t, d, col) in enumerate(stages):
        x = 44 + i * 213
        c.rect(x, 150, 190, 100, [f"#{t}", f"_{d}"], c=col, id=f"s{i}", pad=4)
        c.badge(i + 1, x + 24, 150, col)
        if i:
            c.edge(f"s{i - 1}", f"s{i}", "r", "l", c="gray", w=4)
    c.line([(1169, 250), (1169, 290), (139, 290), (139, 250)], color="#1E9A63", w=3, dash="d")
    c.label(654, 290, "6 · return path: response retraces the same tunnel", c="green", solid=True)
    c.text(44, 336, [("^WHAT EACH STAGE DECIDES", PAL["indigo"][2])])
    cards = [("DNS + anycast routing", "Decides WHICH edge receives it", "DNS returns the VIP; routing selects an RE. The origin never sees the client session.", "http_loadbalancer.domains", "purple"),
             ("Edge policy", "Decides MAY this request pass", "WAF signatures, threat campaigns, service policy allow/deny, rate limits, bot rules.", "app_firewall · service_policy", "orange"),
             ("Origin pool", "Decides WHICH backend serves it", "Healthy endpoints only; endpoint_selection = LOCAL_PREFERRED picks the nearest site.", "origin_pool · healthcheck", "pink"),
             ("Tunnel + SLI", "Decides HOW to reach the site", "RE tunnel ends on the SLO; the CE forwards inward from its SLI address (SNAT).", "site (gcp_vpc_site)", "teal")]
    for i, (t, q, d, o, col) in enumerate(cards):
        x = 44 + i * 318
        c.rect(x, 372, 306, 230, [f"#{t}", f"!{q}"] + [(f"_{l}", None) for l in wrap(d, 36)] + [("", None), (f"~{o}", PAL[col][2])], c=col, pad=8)
    c.text(44, 640, [("^WHERE EACH FAILURE SHOWS UP", PAL["indigo"][2])])
    fails = [("Wrong DNS / domain", "name does not resolve, or resolves to the wrong VIP", "check: nslookup lb.example.com", "purple"), ("WAF / policy block", "HTTP 403 with a support ID from the edge", "check: security events in Console", "orange"),
             ("Site down / unreachable", "no healthy endpoint → HTTP 503", "check: site status SLO / SLI UP", "teal"), ("Origin down / firewall drop", "health check fails, endpoint removed", "check: firewall logs + pool", "pink")]
    for i, (t, s, ck, col) in enumerate(fails):
        c.rect(44 + i * 318, 676, 306, 150, [f"#{t}"] + [(f"_{l}", None) for l in wrap(s, 34)] + [("", None), (f"!{ck}", PAL[col][2])], c=col, white=True, pad=8)
    c.rect(44, 860, 1272, 84, [("!Debugging rule: failures surface one stage EARLY", PAL["indigo"][2]), ("_a dead origin looks like a site problem, a dead site looks like a load-balancer problem — name the symptom, then walk stages 1 → 6", MUTED)], c="indigo", white=True, shadow=False)
    c.footer("", "REMEMBER", lines=["Two XC-specific checkpoints sit on top of the usual four-question loop: the WAF at the edge and the tunnel to the site.",
                                    "Resolution (stage 1) · Routing (2/4/5) · Policy (3/5) · Application (origin) — the same method you used in the packet-tracer labs."])
    c.save(out(T + "f5-xc-request-path"))


def apigee_scope():
    c = Canvas(1360, 1330, "Apigee vs F5 Distributed Cloud: who owns which layer",
               "XC delivers and shields traffic; Apigee governs APIs as products. The overlap is edge verbs, not feature parity", "STAGE 19 · PLATFORM COMPARISON")
    c.group(44, 130, 1272, 150, "CONSUMERS", c="blue")
    for i, (t, d) in enumerate([("End user", "browser / mobile app"), ("Partner developer", "API key + OAuth client"), ("Machine client", "service to service")]):
        c.rect(70 + i * 330, 184, 300, 76, [f"#{t}", f"_{d}"], c="blue", white=True, shadow=False)
    c.rect(1070, 184, 220, 76, [("!Identity differs", PAL["red"][2]), ("_XC: IP, TLS, requests", MUTED), ("_Apigee: app, product, tier", MUTED)], c="red", white=True, shadow=False, pad=4)
    c.group(44, 330, 620, 560, "F5 XC · delivery & edge security", c="orange")
    for i, (t, d) in enumerate([("Anycast VIP + DNS", "global entry point on every RE"), ("TLS + WAF + DDoS", "terminate, inspect, block · signatures · bots"), ("L4/L7 load balancing", "origin pools · health checks · TCP and HTTP"), ("Site fabric", "CE tunnels into VPCs — backends need NO public IPs · multi-cloud")]):
        c.rect(70, 388 + i * 92, 568, 80, [f"#{t}", f"_{d}"], c="orange", white=True, shadow=False)
    c.rect(70, 758, 568, 110, [("!Knows:", PAL["orange"][2]), ("_VIPs, sites, IPs, requests, attack patterns", MUTED), ("!Does NOT know what an “API product” is", PAL["red"][2])], c="orange", shadow=False)
    c.group(696, 330, 620, 560, "Apigee · API governance", c="purple")
    for i, (t, d) in enumerate([("API proxies", "versioned façades in front of backends"), ("Policy engine", "OAuth · API key · JWT · quota · spike arrest · CORS"), ("Mediation", "transform payloads · SOAP ↔ REST · mashups"), ("Developer platform", "portal · products · apps · analytics · monetization")]):
        c.rect(722, 388 + i * 92, 568, 80, [f"#{t}", f"_{d}"], c="purple", white=True, shadow=False)
    c.rect(722, 758, 568, 110, [("!Knows:", PAL["purple"][2]), ("_developers, apps, products, quotas, payload shapes", MUTED), ("!Does NOT build network paths to your backends", PAL["red"][2])], c="purple", shadow=False)
    c.rect(44, 914, 1272, 70, [("!Overlap zone — both terminate TLS, rate-limit, and allow/deny", PAL["gray"][2]), ("_a coincidence of edge protocols: choose by the problem (governance vs delivery & security), not by the shared verbs", MUTED)], c="gray", white=True, shadow=False)
    c.text(44, 1016, [("^THE COMBINED PATTERN", PAL["indigo"][2])])
    chain = [("Public API consumer", "developer / machine", "blue"), ("F5 XC edge", "VIP · TLS · WAF · DDoS", "orange"), ("Apigee runtime", "key · quota · product", "purple"), ("Private origins", "GKE / CE / legacy", "green")]
    for i, (t, d, col) in enumerate(chain):
        c.rect(44 + i * 322, 1052, 270, 84, [f"#{t}", f"_{d}"], c=col, id=f"p{i}")
        if i:
            c.edge(f"p{i - 1}", f"p{i}", "r", "l", c="gray", w=4)
    c.footer("", "REMEMBER", lines=["XC answers “is this request allowed onto my network, and which private origin serves it?”",
                                    "Apigee answers “is this consumer entitled to this API, and how much?” — each layer is blind to the other's job."])
    c.save(out(T + "apigee-vs-f5xc-scope"))


def apigee_decision():
    c = Canvas(1360, 1290, "Apigee or F5 XC? A scenario decision tree", "Start from what you are exposing and to whom; the answer usually falls out of one sentence", "STAGE 19 · DECISION GUIDE")
    c.rect(480, 130, 400, 80, [("#What are you exposing,", "#FFFFFF"), ("#and to whom?", "#FFFFFF")], c="indigo", solid=True, shape="pill", id="root")
    branches = [("An API product for outside developers", "keys · docs · quotas · versioning · monetization", "e.g. partner ordering API, open-banking feed", "purple", "APIGEE", ["Developer portal + self-serve keys", "Products, quotas, monetization built in", "Mediation: SOAP → REST, transforms", "Versioned façades decouple backends"], "XC has no portal, no products, no per-developer metering"),
                ("A private app for end users / partners", "secure delivery + WAF in front of private backends", "e.g. internal portal exposed externally, SaaS frontend", "orange", "F5 XC", ["Anycast VIP + TLS + WAF at the edge", "CE tunnels reach backends: zero public IPs", "Same policy across GCP / AWS / DC", "Minutes to publish, no portal needed"], "Apigee cannot reach into a VPC or shield origins at the edge"),
                ("TCP/UDP traffic or site connectivity", "non-HTTP protocols · cloud-to-cloud mesh · egress control", "e.g. databases, site-to-site links", "teal", "F5 XC", ["TCP load balancers, not only HTTP", "Site mesh + egress / forward proxy", "Network problem → network tool", "gRPC rides HTTP/2: handled at L7"], "Apigee speaks HTTP APIs only and carries no traffic"),
                ("A public API AND private, WAF-shielded origins", "edge security + developer governance", "e.g. monetized partner API on GKE", "green", "BOTH · layered", ["XC: VIP, WAF, DDoS at the edge", "↓", "Apigee: keys, quota, products", "↓  private origins via CE / private connect"], "cost: two platforms to run")]
    for i, (q, d, e, col, win, pts, lose) in enumerate(branches):
        x = 44 + i * 318
        c.rect(x, 270, 306, 160, [(f"!{l}", None) for l in wrap(q, 26)] + [(f"_{l}", None) for l in wrap(d, 38)] + [(f"_{l}", None) for l in wrap(e, 38)], c=col, id=f"b{i}", pad=6)
        c.edge("root", f"b{i}", "b", "t", c="gray", w=3, via=[(680, 240), (x + 153, 240)])
        c.rect(x, 460, 306, 230, [(f"#✓ {win}", PAL[col][2])] + [(f"_{p}", MUTED) for p in pts], c=col, white=True, shadow=False, pad=8)
        c.line([(x + 153, 430), (x + 153, 460)], color="#5B6677", w=3)
        c.rect(x, 706, 306, 70, [("!Trade-off", PAL["red"][2]), (f"_{lose}", MUTED)], c="red", white=True, shadow=False, pad=4) if len(lose) < 40 else c.rect(x, 706, 306, 86, [("!Trade-off", PAL["red"][2])] + [(f"_{l}", MUTED) for l in wrap(lose, 36)], c="red", white=True, shadow=False, pad=4)
    c.text(44, 836, [("^TIEBREAKERS WHEN BOTH SEEM PLAUSIBLE", PAL["indigo"][2])])
    for i, (t, d, col) in enumerate([("Lean Apigee when…", "consumers self-serve · quotas differ per partner · payloads need mediation · API lifecycle is the deliverable", "purple"),
                                     ("Lean F5 XC when…", "backends must stay dark · you span clouds · WAF/DDoS is the requirement · non-HTTP or connectivity is in scope", "orange"),
                                     ("Neither first when…", "traffic is internal-only (use GCLB / service mesh) · no WAF, portal or multi-cloud need — added platforms are added cost and ops", "gray")]):
        c.rect(44 + i * 424, 872, 412, 160, [f"#{t}"] + [(f"_{l}", None) for l in wrap(d, 44)], c=col, pad=10)
    c.rect(44, 1060, 1272, 72, [("!Rule of thumb: “product”, “portal”, “quota tier”, “monetize” → Apigee · “private”, “WAF”, “multi-cloud”, “no public IP” → F5 XC", PAL["indigo"][2]), ("_both in one sentence → layered", MUTED)], c="indigo", white=True, shadow=False, pad=8)
    c.footer("", "REMEMBER", lines=["Choose by the problem, not the shared verbs: product governance (Apigee) vs delivery and security (F5 XC)."])
    c.save(out(T + "apigee-vs-f5xc-decision"))


def shopnow():
    c = Canvas(1360, 1200, "ShopNow private GCP access: no VPN, no access", "Nothing in the application is public: clients reach it only over the VPN, through private DNS, an internal load balancer and Apigee", "STAGE 16 · CASE STUDY")
    c.group(44, 130, 300, 560, "CORPORATE · 192.168.1.0/24", c="blue")
    c.icon_box("cli", "pc", 100, 190, 60, "blue", "Authorized client", ["corporate-managed device"])
    c.icon_box("dnsc", "server", 100, 340, 60, "purple", "Corporate DNS", ["conditional forwarding"])
    c.icon_box("opgw", "router", 100, 490, 64, "teal", "On-prem VPN gateway", ["IPsec + BGP / static"])
    c.icon("cloud", 360, 280, 56, "gray")
    c.text(402, 350, [("^INTERNET", MUTED)], anchor="m")
    c.icon_box("bad", "pc", 380, 590, 56, "red", "Client w/o VPN", ["✗ DENIED"])
    c.group(520, 130, 796, 940, "GOOGLE CLOUD · Terraform-managed · no public application ingress", c="indigo")
    c.rect(548, 190, 340, 76, [("#HA VPN gateway", PAL["teal"][2]), ("_IPsec termination", MUTED)], c="teal", white=True, id="hv", shadow=False)
    c.rect(930, 190, 360, 76, [("#Cloud Router", PAL["teal"][2]), ("_BGP route exchange", MUTED)], c="teal", white=True, id="cr", shadow=False)
    c.rect(548, 290, 742, 70, [("#Private DNS + inbound forwarding", PAL["purple"][2]), ("~shop.internal   api.shop.internal", MUTED)], c="purple", white=True, id="pdns", shadow=False)
    c.rect(548, 390, 742, 70, [("#Internal HTTPS load balancer", PAL["orange"][2]), ("_private IP · TCP 443", MUTED)], c="orange", white=True, id="ilb", shadow=False)
    c.rect(548, 500, 350, 120, [("#Website entry point", PAL["green"][2]), ("_web Service → Pods", MUTED), ("_route: shop.internal", MUTED)], c="green", white=True, id="web", shadow=False)
    c.rect(940, 500, 350, 120, [("#Private Apigee endpoint", PAL["pink"][2]), ("_authentication · quotas", MUTED), ("_threat protection · analytics", MUTED)], c="pink", white=True, id="apg", shadow=False)
    c.group(548, 660, 742, 260, "Private GKE cluster · internal Gateway / Ingress", c="green", hh=34)
    for i, t in enumerate(["web", "orders", "inventory"]):
        c.rect(572 + i * 236, 718, 220, 90, [f"#{t} service", "_Service + Pods"], c="green", white=True, id=f"g{i}", shadow=False)
    c.rect(572, 826, 692, 70, [("!Managed database · private IP · TCP 5432", PAL["gray"][2])], c="gray", white=True, shadow=False, id="db")
    c.rect(548, 950, 350, 80, [("#Cloud NAT", PAL["teal"][2]), ("_outbound only", MUTED)], c="teal", white=True, id="nat", shadow=False)
    c.rect(940, 950, 350, 80, [("#Approved external APIs", PAL["gray"][2]), ("_public internet destinations", MUTED)], c="gray", white=True, id="ext", shadow=False)
    c.edge("cli", "dnsc", "b", "t", c="blue", w=3)
    c.edge("dnsc", "opgw", "b", "t", c="purple", w=3)
    c.line([(164, 522), (360, 522), (360, 228), (548, 228)], color="#7C4DDB", w=8, arrow=None)
    c.label(360, 390, "IPsec tunnel", c="purple", solid=True)
    c.line([(466, 640), (540, 640)], color="#D93F3F", w=5, dash="d")
    cross(c, 510, 640, 10)
    c.edge("hv", "cr", "r", "l", c="teal", w=4, arrow="both", label="BGP", lc="teal")
    c.edge("pdns", "ilb", "b", "t", c="purple", w=4)
    c.edge("ilb", "web", "b", "t.5", c="green", w=4, label="private website", lc="green", lpos=.5, loff=(-60, 0))
    c.edge("ilb", "apg", "b", "t.5", c="pink", w=4, label="authenticated API", lc="pink", lpos=.5, loff=(60, 0))
    c.line([(723, 620), (723, 660)], color="#1E9A63", w=4)
    c.line([(1115, 620), (1115, 640), (1030, 640), (1030, 660)], color="#E0457B", w=4)
    c.line([(808, 808), (808, 826)], color="#5B6677", w=3)
    c.edge("nat", "ext", "r", "l", c="teal", w=4)
    c.label(919, 1050, "translated egress only", c="teal")
    c.footer("", "REMEMBER", lines=["Three controls must all hold: a route (VPN + BGP), a name (private DNS forwarded across the VPN) and a policy (firewall + Apigee)."])
    c.save(out(T + "shopnow-network-architecture"))


def lab_f5_01():
    c = Canvas(1360, 1040, "F5 XC Lab 01: the two-VPC landing zone", "Built with gcloud before any Terraform: an outside VPC for the future CE, an inside VPC for a private origin", "F5 XC LAB 01 · GCP FOUNDATION")
    c.group(44, 130, 560, 420, "xc-outside-vpc · SLO", c="orange", tag="slo-subnet 10.190.0.0/24")
    c.rect(70, 190, 508, 130, [("!CE node NIC 0 attaches here in Lab 02", PAL["orange"][2]), ("_public / ephemeral IP, dials out to F5", MUTED), ("_nothing is deployed yet — only the landing zone", MUTED)], c="orange", white=True, dash="d", shadow=False)
    c.rect(70, 340, 508, 90, [("!Firewall: egress allowed", PAL["red"][2]), ("_outside VPC mostly needs outbound reachability", MUTED)], c="red", white=True, shadow=False)
    c.group(756, 130, 560, 420, "xc-inside-vpc · SLI", c="green", tag="sli-subnet 10.200.0.0/24")
    c.rect(782, 190, 508, 130, [("#web-inside", PAL["green"][2]), ("~10.200.0.10 · NGINX · tag xc-origin", MUTED), ("!NO external IP", PAL["red"][2])], c="green", white=True, id="web", shadow=False)
    c.rect(782, 340, 300, 90, [("!Firewall (tag-based)", PAL["red"][2]), ("~allow tcp:80 from 10.200.0.0/24", MUTED)], c="red", white=True, shadow=False)
    c.rect(1100, 340, 190, 90, [("#Cloud NAT", PAL["teal"][2]), ("_installs only", MUTED)], c="teal", white=True, shadow=False)
    c.rect(782, 450, 508, 76, [("!Inbound from the internet: no path", PAL["red"][2]), ("_the origin has no public address", MUTED)], c="red", white=True, shadow=False)
    c.rect(640, 260, 80, 60, [("!?", "#FFFFFF")], c="gray", solid=True, shape="circle", shadow=False)
    c.line([(604, 290), (640, 290)], color="#5B6677", w=3, arrow=None, dash="d")
    c.line([(720, 290), (756, 290)], color="#5B6677", w=3, arrow=None, dash="d")
    c.text(680, 336, [("^NOT CONNECTED", MUTED), ("_(the CE bridges them)", MUTED)], anchor="m")
    c.text(44, 590, [("^GCP VS WHAT YOU MAY KNOW FROM AWS", PAL["indigo"][2])])
    c.table(44, 622, [260, 420, 592], [["Concept", "AWS habit", "GCP reality"], ["VPC scope", "regional", "GLOBAL object; subnets are regional"], ["Firewall", "security groups per ENI", "VPC-level rules selected by network tag"], ["Multi-NIC VM", "several NICs in one VPC", "each NIC must be in a DIFFERENT VPC"]], rowh=40, head="indigo")
    c.text(44, 800, [("^WHAT THE LAB BUILDS", PAL["indigo"][2])])
    for i, (t, d, col) in enumerate([("1 · Two VPCs", "custom mode, one subnet each", "blue"), ("2 · Cloud NAT", "on the inside VPC, installs only", "teal"), ("3 · Firewall rule", "tcp:80 from the subnet to tag xc-origin", "red"), ("4 · Private NGINX", "no external IP flag at all", "green")]):
        c.rect(44 + i * 318, 836, 306, 100, [f"#{t}", f"_{d}"], c=col, pad=6)
    cmds(c, 44, 960, 1272, ["gcloud compute networks create xc-inside-vpc --subnet-mode=custom", "gcloud compute instances describe web-inside (no natIP)"], title="VERIFY")
    c.save(out("f5-xc/01-gcp-networking-site-concepts/diagrams/f5-lab01-landing-zone"))


def lab_f5_02():
    c = Canvas(1360, 1040, "F5 XC Lab 02: manual deployment, object by object", "Every ClickOps object in the Console becomes a Terraform resource in Lab 04. Learn the chain here, then automate it", "F5 XC LAB 02 · CONSOLE")
    objs = [("Site token", "one-time credential", "blue", "Console"), ("CE node VM", "2 NICs · NIC0 = SLO", "teal", "GCP"), ("Registration", "pending → approve", "orange", "Console"), ("Origin pool", "10.200.0.10:80 on SLI", "green", "Console"), ("HTTP load balancer", "VIP + domain + WAF", "purple", "Console")]
    for i, (t, d, col, where) in enumerate(objs):
        x = 44 + i * 256
        c.rect(x, 170, 232, 120, [("^" + where.upper(), PAL[col][2]), f"#{t}", f"_{d}"], c=col, id=f"o{i}", pad=4)
        c.badge(i + 1, x + 22, 170, col)
        if i:
            c.edge(f"o{i - 1}", f"o{i}", "r", "l", c="gray", w=4)
    c.text(44, 320, [("^WHERE EACH OBJECT LIVES", PAL["indigo"][2])])
    c.group(44, 350, 620, 330, "F5 XC SaaS (Console)", c="red")
    for i, (t, d) in enumerate([("Site token + registration", "proves the CE belongs to your tenant"), ("Site object", "logical site the CE joins (auto-created)"), ("Health check + origin pool", "which backends, reached how, via which site"), ("HTTP LB + app firewall", "global anycast VIP, WAF, routes to the pool")]):
        c.rect(70, 408 + i * 66, 568, 58, [f"!{t}", f"_{d}"], c="red", white=True, shadow=False, align="l", pad=16)
    c.group(696, 350, 620, 330, "Your GCP project", c="green")
    c.rect(722, 408, 568, 80, [("!ce-gcp-01 · Compute Engine VM · F5 image", PAL["teal"][2]), ("~NIC0 → xc-outside-vpc (SLO) · NIC1 → xc-inside-vpc (SLI)", MUTED)], c="teal", white=True, shadow=False, pad=4)
    c.rect(722, 504, 568, 80, [("!web-inside · private NGINX", PAL["green"][2]), ("~10.200.0.10:80 · no external IP", MUTED)], c="green", white=True, shadow=False)
    c.rect(722, 600, 568, 64, [("!Token is pasted into VM metadata once, then never again", PAL["blue"][2])], c="blue", white=True, shadow=False, pad=4)
    c.text(44, 716, [("^THE PAYOFF TEST", PAL["indigo"][2])])
    c.rect(44, 750, 400, 110, [("!1 · backend is still dark", PAL["red"][2]), ("~curl http://10.200.0.10 (from outside)", MUTED), ("_times out: no public path", MUTED)], c="red", white=True, shadow=False)
    c.rect(480, 750, 400, 110, [("!2 · but the world reaches it", PAL["green"][2]), ("~curl http://<xc-lb-domain>", MUTED), ("_→ Hello from private web-inside", MUTED)], c="green", white=True, shadow=False)
    c.rect(916, 750, 400, 110, [("!Break and repair (predict first)", PAL["orange"][2]), ("_wrong site network, wrong port, stopped VM:", MUTED), ("_which stage of the request path fails?", MUTED)], c="orange", white=True, shadow=False)
    c.footer("", "REMEMBER", lines=["The critical choice is “IP address on site → Site Local Inside”: it makes XC deliver through the CE's SLI, not the public internet.",
                                    "Console menus move between releases; the object chain token → site → pool → load balancer is stable."])
    c.save(out("f5-xc/02-manual-ce-deployment/diagrams/f5-lab02-manual-deploy"))


def lab_f5_03():
    c = Canvas(1360, 1090, "F5 XC Lab 03: one Terraform project, two control planes", "Same workflow, two providers, two credentials, one state file. Prove both sides with the cheapest object each", "F5 XC LAB 03 · TERRAFORM")
    c.rect(480, 140, 400, 120, [("#One Terraform project", "#FFFFFF"), ("_one dependency graph · one terraform.tfstate", "#FFFFFF")], c="indigo", solid=True, id="tf")
    c.rect(44, 360, 560, 190, [("#provider google", PAL["blue"][2]), ("~hashicorp/google", MUTED), ("_credentials: gcloud Application Default Credentials", MUTED), ("~gcloud auth application-default login", MUTED)], c="blue", id="g")
    c.rect(756, 360, 560, 190, [("#provider volterra", PAL["purple"][2]), ("~volterraedge/volterra", MUTED), ("_credentials: API certificate .p12 + VES_P12_PASSWORD", MUTED), ("~env var, never in code", MUTED)], c="purple", id="v")
    c.edge("tf", "g", "b", "t", c="blue", w=5, via=[(680, 320), (324, 320)])
    c.edge("tf", "v", "b", "t", c="purple", w=5, via=[(680, 320), (1036, 320)])
    c.rect(44, 620, 560, 140, [("#GCP project", PAL["green"][2]), ("~google_compute_network.xc_lab_vpc", MUTED), ("_proof the GCP side works", MUTED)], c="green", id="gcp")
    c.rect(756, 620, 560, 140, [("#F5 XC tenant", PAL["orange"][2]), ("~volterra_namespace.lab", MUTED), ("_proof the XC side works (cheapest XC object)", MUTED)], c="orange", id="xc")
    c.edge("g", "gcp", "b", "t", c="blue", w=4, label="GCP API", lc="blue")
    c.edge("v", "xc", "b", "t", c="purple", w=4, label="XC API", lc="purple")
    c.line([(604, 690), (756, 690)], color="#12908A", w=4, arrow="both", dash="d")
    c.label(680, 690, "CE node bridges both", c="teal")
    c.text(44, 800, [("^CREDENTIAL HYGIENE", PAL["indigo"][2])])
    for i, (t, d, col) in enumerate([("Keep the .p12 outside the repo", "e.g. ~/creds/f5xc-api.p12", "red"), ("Password via environment variable", "export VES_P12_PASSWORD=…", "orange"), ("Same dependency graph both sides", "Lab 04 feeds a GCP subnet name into an XC object", "green"), ("Destroy both when done", "terraform destroy removes the VPC and the namespace", "teal")]):
        c.rect(44 + i * 318, 836, 306, 100, [f"!{t}"] + [(f"_{l}", None) for l in wrap(d, 34)], c=col, pad=6)
    cmds(c, 44, 958, 1272, ["terraform init", "terraform apply", "gcloud compute networks list", "curl API: list namespaces"], title="VERIFY BOTH SIDES")
    c.save(out("f5-xc/03-terraform-dual-provider/diagrams/f5-lab03-dual-provider"))


def lab_f5_04():
    c = Canvas(1360, 1290, "F5 XC Lab 04: how the two planes cooperate in one apply", "Your google provider builds the landing zone; XC's own backend builds the Customer Edge VM. Terraform just orders the dependencies", "F5 XC LAB 04 · AUTOMATION")
    c.rect(500, 130, 360, 70, [("#terraform apply", "#FFFFFF")], c="indigo", solid=True, shape="pill", id="tf")
    c.group(44, 260, 600, 470, "GCP PLANE · google provider", c="blue")
    items = [("VPCs + subnets", "xc-outside-vpc / xc-inside-vpc"), ("Router + NAT, firewall", "egress for the private origin"), ("web-inside VM", "NGINX, no external IP"), ("CE VM (created BY XC)", "dashed: not from your google provider")]
    for i, (t, d) in enumerate(items):
        c.rect(70, 318 + i * 98, 548, 84, [f"#{t}", f"_{d}"], c="blue" if i < 3 else "teal", white=True, shadow=False, dash="d" if i == 3 else None, id=f"gp{i}")
    c.group(716, 260, 600, 470, "XC PLANE · volterra provider", c="red")
    xi = [("namespace · cloud credentials", "GCP service-account key XC uses to deploy the CE"), ("gcp_vpc_site", "site SPEC: the desired state for the CE"), ("tf_params_action = apply", "asks XC's backend to run its own apply"), ("health check · origin pool · WAF · HTTP LB", "10.200.0.10:80 on the site's inside network")]
    for i, (t, d) in enumerate(xi):
        c.rect(742, 318 + i * 98, 548, 84, [f"#{t[:40]}", f"_{d}"], c="red", white=True, shadow=False, id=f"xp{i}", pad=6)
    c.line([(500, 165), (344, 165), (344, 260)], color="#2F6FE0", w=4)
    c.line([(860, 165), (1016, 165), (1016, 260)], color="#D93F3F", w=4)
    c.label(344, 230, "google provider", c="blue")
    c.label(1016, 230, "volterra provider", c="red")
    c.edge("xp2", "gp3", "l", "r", c="teal", w=5, dash="d", label="XC builds it", lc="teal", lpos=.5, loff=(0, 0))
    c.text(44, 770, [("^ORDER OF EVENTS", PAL["indigo"][2])])
    steps(c, 44, 806, 640, [("Landing zone exists", "VPCs, subnets, NAT, firewall, private origin"), ("XC gets cloud credentials + site spec", "namespace and gcp_vpc_site created"), ("Deploy action fires", "XC backend provisions the CE VM with its 2 NICs"),
                            ("CE registers, site goes UP", "token → pending → auto-approved by the action"), ("Pool, WAF and LB attach to the site", "traffic path is now complete")], col="indigo", h=54, gap=8, title="")
    c.rect(720, 806, 596, 140, [("#The payoff", PAL["green"][2]), ("~curl http://<lb-domain>", MUTED), ("_→ private NGINX answers through the global VIP", MUTED), ("~terraform destroy → both clouds cleaned up", MUTED)], c="green", white=True, shadow=False)
    c.rect(720, 966, 596, 120, [("!Who creates the CE VM?", PAL["red"][2]), ("_Not your google provider. volterra_gcp_vpc_site stores a spec;", MUTED), ("_the deploy action makes XC run its own apply using the", MUTED), ("_service account in volterra_cloud_credentials.", MUTED)], c="red", white=True, shadow=False)
    c.footer("", "REMEMBER", lines=["Two planes, one command: google builds your VPC world, volterra describes the XC world, XC builds the CE between.",
                                    "Lab 02 did this by hand; every Console click above maps to one resource block here."])
    c.save(out("f5-xc/04-automated-site-waf/diagrams/f5-lab04-two-planes"))


if __name__ == "__main__":
    for f in (f5_architecture, f5_slo_sli, f5_request_path, apigee_scope, apigee_decision, shopnow, lab_f5_01, lab_f5_02, lab_f5_03, lab_f5_04):
        f()
