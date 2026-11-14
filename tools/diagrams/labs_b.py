from dgm import Canvas, PAL, MUTED
from labkit import out, steps, cmds
from labs_a import link
from labkit import wrap

CHIP = "TERRAFORM LAB"


def matrix(c, x, y, colw, grid, rowh=48):
    cl = {"✓": "green", "✗": "red"}
    for r, row in enumerate(grid):
        cx = x
        for k, cell in enumerate(row):
            if r == 0 or k == 0:
                c.rect(cx, y + r * (rowh + 4), colw[k], rowh, [f"!{cell}"], c="indigo", solid=True, shape="rect", sw=1, shadow=False, pad=4)
            else:
                col = cl.get(cell[0], "gray")
                c.rect(cx, y + r * (rowh + 4), colw[k], rowh, [(f"!{cell}", PAL[col][2])], c=col, shape="rect", sw=1, shadow=False, pad=4)
            cx += colw[k]
    return y + len(grid) * (rowh + 4)


def tf01():
    c = Canvas(1360, 1070, "Terraform Lab 01 — The declarative lifecycle", "You describe the desired network; Terraform compares it with what it recorded and what exists, then makes the difference real", f"TF LAB 01 · {CHIP}")
    c.rect(44, 140, 360, 190, [], c="blue", id="cfg")
    c.icon("doc", 66, 160, 56, "blue")
    c.text(140, 168, [("#main.tf", PAL["blue"][2]), ("_DESIRED state — what you want", MUTED)])
    c.text(66, 242, [("~resource \"google_compute_network\"", PAL["blue"][2]), ("~  name = \"tf-first-vpc\"", PAL["blue"][2]), ("~  auto_create_subnetworks = false", PAL["blue"][2])])
    c.rect(500, 140, 360, 190, [], c="purple", id="st")
    c.icon("db", 528, 160, 56, "purple")
    c.text(612, 168, [("#terraform.tfstate", PAL["purple"][2]), ("_RECORDED state — what it built", MUTED)])
    c.text(526, 242, [("_maps each resource block to a", MUTED), ("_real GCP object ID. Never edit by hand,", MUTED), ("_never commit it (can contain secrets).", MUTED)])
    c.rect(956, 140, 360, 190, [], c="green", id="gcp")
    c.icon("cloud", 976, 150, 50, "green")
    c.text(1066, 168, [("#Google Cloud", PAL["green"][2]), ("_ACTUAL state — what exists", MUTED)])
    c.text(982, 242, [("_the VPC network object in your", MUTED), ("_project, reached through the", MUTED), ("_Compute Engine API.", MUTED)])
    c.edge("cfg", "st", "r", "l", c="indigo", w=4, label="plan compares", lc="indigo", loff=(0, -22))
    c.edge("st", "gcp", "r", "l", c="indigo", w=4, arrow="both", label="refresh · apply", lc="indigo", loff=(0, -22))
    c.text(44, 372, [("^THE COMMANDS · IN ORDER", PAL["indigo"][2])])
    cmds_ = [("init", "Download the google provider into .terraform/ and prepare the directory", "gray", "no cloud changes"), ("validate", "Check syntax and references before touching anything", "teal", "no cloud changes"),
             ("plan", "Show + create, ~ update, - destroy. A preview only", "blue", "read-only diff"), ("apply", "Create tf-first-vpc through the API and update the state file", "green", "creates / changes"),
             ("destroy", "Delete everything Terraform manages — Lab 01 ends cleanly", "red", "removes resources")]
    for i, (n, d, col, eff) in enumerate(cmds_):
        x = 44 + i * 256
        c.rect(x, 406, 246, 210, [("^TERRAFORM", PAL[col][2]), (f"#{n}", PAL[col][2])] + [(f"_{w}", MUTED) for w in wrap(d, 30)] + [("", MUTED), (f"!{eff}", PAL[col][2])], c=col, id=f"cmd{i}", pad=8)
        if i:
            c.edge(f"cmd{i - 1}", f"cmd{i}", "r", "l", c="gray", w=3)
    c.text(44, 656, [("^READING A PLAN", PAL["indigo"][2])])
    for i, (sym, t, col) in enumerate([("+", "create a new resource", "green"), ("~", "update in place", "orange"), ("-/+", "replace (destroy + create)", "red"), ("-", "destroy", "red")]):
        c.rect(44 + i * 318, 688, 306, 56, [(f"!{sym}   {t}", "#FFFFFF")], c=col, solid=True, shape="pill", shadow=False)
    c.table(44, 780, [300, 460, 512], [["File / folder", "Purpose", "Commit to git?"], ["main.tf · variables.tf", "your configuration", "✓ yes"], ["terraform.tfstate", "recorded state (may hold secrets)", "✗ never — use a remote backend"], [".terraform/ · .terraform.lock.hcl", "provider binaries · pinned versions", "lock file ✓ · folder ✗"]], rowh=38, head="indigo", mono_cols=(0,))
    c.footer("", "REMEMBER", lines=["Declarative = you state the end result, Terraform works out the steps. Always read plan before apply.",
                                    "State is the bridge between your code and reality: lose it and Terraform no longer knows what it owns."])
    c.save(out("terraform/01-setup-first-apply/diagrams/lab01-terraform-lifecycle"))


def tf02():
    c = Canvas(1360, 960, "Terraform Lab 02 — Custom VPC and regional subnets", "A VPC is a global virtual network; subnets are regional IP ranges inside it, and routing between them is built in", f"TF LAB 02 · {CHIP}")
    c.group(44, 130, 1272, 330, "tf-lab-vpc · custom mode · global", c="indigo", tag="auto_create_subnetworks = false")
    c.group(76, 190, 580, 240, "lan1-clients · 192.168.10.0/24", c="blue", tag="us-central1", hh=34)
    c.group(704, 190, 580, 240, "lan2-servers · 192.168.20.0/24", c="green", tag="us-central1", hh=34)
    c.rect(100, 242, 250, 70, [("!Client workloads", PAL["blue"][2]), ("_added in Lab 04", MUTED)], c="blue", white=True, shadow=False)
    c.rect(370, 242, 262, 70, [("!Gateway 192.168.10.1", PAL["blue"][2]), ("_provided automatically", MUTED)], c="blue", white=True, shadow=False)
    c.rect(728, 242, 250, 70, [("!Private servers", PAL["green"][2]), ("_added in Lab 04", MUTED)], c="green", white=True, shadow=False)
    c.rect(998, 242, 262, 70, [("!Gateway 192.168.20.1", PAL["green"][2]), ("_provided automatically", MUTED)], c="green", white=True, shadow=False)
    c.line([(656, 340), (704, 340)], color="#7C4DDB", w=8, arrow="both")
    c.label(680, 372, "built-in routing", c="purple", solid=True)
    c.text(44, 490, [("^INSIDE ONE SUBNET: 192.168.10.0/24 → 256 ADDRESSES", PAL["indigo"][2])])
    x = 44
    for t, a_, w, col in [("Network", ".0", 130, "gray"), ("Gateway", ".1", 130, "teal"), ("Usable VM addresses  .2 – .253", "", 752, "green"), ("Reserved", ".254", 130, "gray"), ("Broadcast", ".255", 130, "gray")]:
        c.rect(x, 520, w - 4, 70, [(f"!{a_}"), (f"_{t}")] if a_ else [f"#{t}"], c=col, shape="rect", shadow=False, pad=4)
        x += w
    c.text(44, 604, [("_GCP reserves 4 addresses in every subnet: network, default gateway, second-to-last, and broadcast.", MUTED)])
    c.text(44, 650, [("^IMPLIED ROUTES CREATED FOR YOU", PAL["indigo"][2])])
    c.table(44, 680, [260, 220, 280], [["Destination", "Next hop", "Why"], ["192.168.10.0/24", "VPC network", "lan1 subnet route"], ["192.168.20.0/24", "VPC network", "lan2 subnet route"], ["0.0.0.0/0", "default internet gateway", "egress (needs external IP/NAT)"]], rowh=38, head="indigo", mono_cols=(0,))
    c.rect(850, 680, 466, 152, [("#Custom mode vs auto mode", PAL["indigo"][2]), ("_auto: GCP creates a /20 in every region — too much", MUTED), ("_custom: you choose every range, so ranges never", MUTED), ("_overlap with on-premises or peered networks", MUTED)], c="indigo", white=True, shadow=False)
    c.text(44, 850, [("^TERRAFORM RESOURCES", PAL["indigo"][2])])
    for i, t in enumerate(["google_compute_network", "google_compute_subnetwork × 2"]):
        c.rect(44 + i * 330, 880, 318, 40, [(f"~{t}", "#E2E8F0")], c="gray", solid=True, shape="pill", shadow=False, pad=6, fill="#1F2A44", stroke="#0B1220", tcolor="#E2E8F0")
    c.save(out("terraform/02-vpc-subnets/diagrams/lab02-vpc-subnets"))


def tf03():
    c = Canvas(1360, 1130, "Terraform Lab 03 — Routing, firewall policy and Cloud NAT", "Firewall rules decide who may connect in; Cloud Router + Cloud NAT give private VMs outbound-only internet access", f"TF LAB 03 · {CHIP}")
    c.icon_box("adm", "user", 60, 260, 56, "teal", "Administrator", ["~var.admin_cidr/32"])
    c.icon_box("iap", "lock", 210, 260, 56, "purple", "Identity-Aware Proxy", ["~35.235.240.0/20"])
    c.group(330, 130, 720, 440, "tf-lab-vpc", c="indigo", tag="stateful firewall")
    c.group(360, 190, 300, 170, "lan1-clients · 192.168.10.0/24", c="blue", hh=34)
    c.rect(384, 244, 252, 90, [("!future frontend", PAL["blue"][2]), ("~tag: ssh-allowed", MUTED), ("_admin may SSH directly", MUTED)], c="blue", white=True, shadow=False, id="l1")
    c.group(700, 190, 300, 170, "lan2-servers · 192.168.20.0/24", c="green", hh=34)
    c.rect(724, 244, 252, 90, [("!private backend", PAL["green"][2]), ("~tag: iap-ssh", MUTED), ("_no external IP", MUTED)], c="green", white=True, shadow=False, id="l2")
    c.rect(360, 400, 640, 140, [], c="red", white=True, shadow=False)
    c.icon("firewall", 380, 420, 70, "red")
    c.text(470, 420, [("!Firewall policy (stateful)", PAL["red"][2]), ("_✓ IAP range → tcp:22 on tag iap-ssh", MUTED), ("_✓ admin /32 → tcp:22 on tag ssh-allowed", MUTED), ("_✓ internal 192.168.0.0/16 → tcp, udp, icmp", MUTED), ("_✗ everything else ingress is denied (implied rule)", MUTED)])
    c.edge("adm", "iap", "r", "l", c="purple", w=4)
    c.label(300, 232, "IAP TCP 22", c="purple")
    c.edge("l1", "l2", "r", "l", c="green", w=4, arrow="both")
    c.label(680, 289, "internal ✓", c="green")
    c.icon_box("rtr", "router", 1100, 170, 60, "teal", "Cloud Router", ["regional control plane"])
    c.icon_box("nat", "router", 1100, 330, 70, "orange", "Cloud NAT", ["lan2 outbound only"])
    c.icon("cloud", 1220, 330, 70, "gray")
    c.text(1265, 440, [("^INTERNET", MUTED)], anchor="m")
    c.line([(976, 300), (1040, 300), (1040, 365), (1100, 365)], color="#E8890C", w=4)
    c.label(1040, 280, "private egress", c="orange")
    c.line([(1170, 365), (1225, 365)], color="#E8890C", w=4)
    c.line([(1130, 270), (1130, 330)], color="#12908A", w=3, arrow="both", dash="d")
    c.text(44, 610, [("^EGRESS WITHOUT AN EXTERNAL IP", PAL["indigo"][2])])
    steps(c, 44, 646, 640, [("Private VM opens a connection", "src 192.168.20.x → internet:443"), ("Cloud NAT rewrites the source", "to a Google-managed public IP + port"), ("Reply returns to the NAT mapping", "stateful: allowed back to the VM"), ("Unsolicited inbound", "no mapping → dropped; VM stays unreachable")], col="orange", h=56, gap=8, title="")
    c.table(720, 660, [180, 130, 286], [["Rule", "Direction", "Source → target"], ["allow-iap-ssh", "ingress", "35.235.240.0/20 → iap-ssh"], ["allow-admin-ssh", "ingress", "admin/32 → ssh-allowed"], ["allow-internal", "ingress", "192.168.0.0/16 → all"]], rowh=40, head="red", mono_cols=(0, 2))
    cmds(c, 720, 850, 596, ["gcloud compute firewall-rules list", "gcloud compute routers nats list"], title="VERIFY")
    c.footer("", "REMEMBER", lines=["Firewall rules are per VPC but attach by network tag; the implied rules are deny-all ingress and allow-all egress.",
                                    "Cloud NAT is not a VM: it is a managed, outbound-only translation service attached to a Cloud Router."])
    c.save(out("terraform/03-routing-nat-firewall/diagrams/lab03-routing-nat-firewall"))


def tf04():
    c = Canvas(1360, 1180, "Terraform Lab 04 — VMs, private DNS and Cloud NAT", "Two VMs in two subnets: a bastion-style frontend, a private backend reached by name, by IAP, and out through NAT", f"TF LAB 04 · {CHIP}")
    c.icon_box("adm", "user", 60, 240, 56, "teal", "Administrator", ["labuser + key"])
    c.icon_box("iap", "lock", 60, 400, 56, "purple", "IAP", ["35.235.240.0/20"])
    c.group(300, 130, 800, 450, "tf-lab-vpc", c="indigo")
    c.group(330, 190, 360, 250, "lan1-clients · 192.168.10.0/24", c="blue", hh=34)
    c.icon_box("fe", "server", 380, 240, 64, "blue", "frontend-vm", ["private + ephemeral public IP", "~tag: ssh-allowed"])
    c.group(710, 190, 360, 250, "lan2-servers · 192.168.20.0/24", c="green", hh=34)
    c.icon_box("be", "server", 760, 240, 64, "green", "backend-vm", ["private IP only · nginx", "~tag: iap-ssh"])
    c.rect(330, 464, 740, 90, [], c="purple", white=True, shadow=False)
    c.icon("db", 350, 478, 50, "purple")
    c.text(420, 478, [("!Cloud DNS private zone  corp.internal.", PAL["purple"][2]), ("~backend.corp.internal  →  backend private IP", PAL["purple"][2]), ("_visible only inside tf-lab-vpc", MUTED)])
    c.line([(470, 280), (760, 280)], color="#1E9A63", w=4, arrow="both")
    c.label(620, 280, "HTTP / ICMP by private IP", c="green")
    c.line([(116, 262), (330, 262), (380, 262)], color="#12908A", w=4)
    c.label(220, 262, "SSH 22", c="teal")
    c.line([(116, 428), (250, 428), (250, 400), (760, 400), (760, 304)], color="#7C4DDB", w=4, dash="d")
    c.label(480, 400, "IAP-tunnelled SSH 22", c="purple")
    c.icon_box("nat", "router", 1180, 230, 64, "orange", "Cloud Router + NAT", ["outbound translation"])
    c.icon("cloud", 1170, 420, 80, "gray")
    c.line([(824, 262), (1180, 262)], color="#E8890C", w=4)
    c.label(1000, 262, "private egress", c="orange")
    c.line([(1212, 294), (1212, 420)], color="#E8890C", w=4)
    c.text(1215, 508, [("^INTERNET", MUTED)], anchor="m")
    c.text(44, 620, [("^FOUR THINGS TO PROVE", PAL["indigo"][2])])
    items = [("SSH to the frontend", "its ephemeral public IP + your key", "teal"), ("SSH to the backend", "only possible through IAP — it has no public IP", "purple"), ("Reach backend by name", "frontend resolves backend.corp.internal then curls it", "green"), ("Backend reaches the internet", "apt update works via Cloud NAT; nothing reaches it inbound", "orange")]
    for i, (t, d, col) in enumerate(items):
        c.rect(44 + (i % 2) * 640, 652 + (i // 2) * 84, 632, 74, [f"!{t}", f"_{d}"], c=col, align="l", pad=60, shadow=False)
        c.badge(i + 1, 74 + (i % 2) * 640, 689 + (i // 2) * 84, col)
    c.table(44, 840, [330, 330, 612], [["Resource", "Purpose", "Key setting"], ["google_compute_instance × 2", "frontend / backend VMs", "no access_config on backend"], ["google_dns_managed_zone", "private zone corp.internal.", "visibility = private"],
                                       ["google_dns_record_set", "A record for backend", "points at backend private IP"], ["google_compute_router(+_nat)", "outbound NAT", "lan2 range only"]], rowh=36, head="indigo", mono_cols=(0,))
    cmds(c, 44, 1030, 1272, ["gcloud compute ssh frontend-vm", "gcloud compute ssh backend-vm --tunnel-through-iap", "nslookup backend.corp.internal", "curl http://backend.corp.internal"], title="VERIFY")
    c.save(out("terraform/04-vms-and-dns/diagrams/lab04-vms-private-dns"))


def tf05():
    c = Canvas(1360, 1040, "Terraform Lab 05 — The complete two-tier GCP stack", "Public web tier, private app tier, private DNS and NAT: exposure is decided by tags, firewall rules and the absence of public IPs", f"TF LAB 05 · {CHIP}")
    c.icon_box("usr", "user", 56, 250, 56, "teal", "Internet users", ["HTTP 80 · admin SSH"])
    c.group(220, 130, 880, 430, "custom-prod-vpc", c="indigo", tag="global")
    c.group(250, 190, 390, 250, "web-tier-subnet · 10.1.10.0/24", c="green", hh=34)
    c.icon_box("web", "server", 290, 240, 64, "green", "frontend-web-vm", ["public IP · nginx", "~tag: web-tier"])
    c.group(680, 190, 390, 250, "app-tier-subnet · 10.1.20.0/24", c="purple", hh=34)
    c.icon_box("app", "server", 720, 240, 64, "purple", "backend-app-vm", ["private IP · API :8080", "~tag: app-tier · no public IP"])
    c.rect(250, 464, 820, 76, [], c="teal", white=True, shadow=False)
    c.icon("db", 270, 474, 46, "teal")
    c.text(334, 476, [("!Cloud DNS private zone", PAL["teal"][2]), ("~api.corp.internal  →  backend private IP", PAL["teal"][2]), ("_the web tier calls the API by name, never by IP", MUTED)])
    c.line([(112, 280), (250, 280), (290, 280)], color="#12908A", w=4)
    c.label(180, 280, "✓ 80", c="green")
    c.line([(450, 290), (720, 290)], color="#1E9A63", w=4, arrow="both")
    c.label(585, 290, "web → API TCP 8080 ✓", c="green")
    c.icon_box("nat", "router", 1160, 230, 64, "orange", "Cloud Router + NAT", ["app egress only"])
    c.icon("cloud", 1150, 400, 80, "gray")
    c.line([(850, 440), (1000, 440), (1000, 262), (1160, 262)], color="#E8890C", w=4)
    c.label(1000, 360, "app egress", c="orange")
    c.line([(1192, 294), (1192, 400)], color="#E8890C", w=4)
    c.text(44, 596, [("^FIREWALL MATRIX · WHO MAY REACH WHAT", PAL["indigo"][2])])
    matrix(c, 44, 630, [260, 190, 190, 190, 190], [["Source ↓   Target →", "web :80", "web :22", "app :8080", "app :22"], ["Internet (anyone)", "✓ allow", "✗ deny", "✗ deny", "✗ deny"], ["Admin via IAP", "✓ allow", "✓ allow", "✗ deny", "✓ allow"], ["web-tier VM (tag)", "—", "—", "✓ allow", "✗ deny"]], rowh=42)
    c.text(44, 880, [("^TERRAFORM BUILDING BLOCKS", PAL["indigo"][2])])
    for i, t in enumerate(["google_compute_network", "google_compute_subnetwork × 2", "google_compute_firewall × 3", "google_compute_instance × 2", "google_dns_managed_zone + record", "google_compute_router_nat"]):
        c.rect(44 + (i % 3) * 424, 910 + (i // 3) * 48, 410, 40, [(f"~{t}", "#E2E8F0")], c="gray", solid=True, shape="pill", shadow=False, pad=6, fill="#1F2A44", stroke="#0B1220", tcolor="#E2E8F0")
    c.save(out("terraform/05-two-tier-networking-scenario/diagrams/lab05-two-tier-network"))


def tf06():
    c = Canvas(1360, 1130, "Terraform Lab 06 — VPC Network Peering", "Peering links two VPCs privately and exchanges routes — but it is never transitive and never merges firewalls", f"TF LAB 06 · {CHIP}")
    c.group(44, 130, 420, 330, "hub-services-vpc", c="blue", tag="shared services")
    c.rect(70, 190, 368, 120, [("#hub-core-subnet", PAL["blue"][2]), ("~10.0.0.0/16 · us-central1", PAL["blue"][2]), ("_DNS · security scanners · CI/CD", MUTED)], c="blue", white=True, shadow=False, id="hub")
    c.group(896, 130, 420, 330, "prod-workload-vpc", c="green", tag="production")
    c.rect(922, 190, 368, 120, [("#prod-workload-subnet", PAL["green"][2]), ("~10.10.0.0/16 · us-central1", PAL["green"][2]), ("_production application workloads", MUTED)], c="green", white=True, shadow=False, id="prod")
    c.rect(922, 336, 368, 90, [("!Production VPC firewall", PAL["red"][2]), ("_allow tcp 22 / 80 / 443 + ICMP", MUTED), ("~source 10.0.0.0/16 (the hub)", MUTED)], c="red", white=True, shadow=False)
    c.rect(70, 336, 368, 90, [("!Hub keeps its own firewall", PAL["blue"][2]), ("_prod rules do NOT apply here", MUTED), ("_peering shares routes, not policy", MUTED)], c="blue", white=True, shadow=False)
    c.line([(464, 232), (896, 232)], color="#7C4DDB", w=9, arrow="both")
    c.label(680, 200, "hub-to-prod peering", c="purple", solid=True)
    c.label(680, 264, "prod-to-hub peering", c="purple", solid=True)
    c.rect(520, 340, 320, 90, [("!Both halves are required", PAL["purple"][2]), ("_one side alone stays INACTIVE", MUTED), ("_2 × google_compute_network_peering", MUTED)], c="purple", white=True, shadow=False)
    c.text(44, 500, [("^NON-TRANSITIVE: A↔B and B↔C does NOT give A↔C", PAL["indigo"][2])])
    c.rect(44, 540, 300, 90, [("#VPC A · prod", PAL["green"][2]), ("~10.10.0.0/16", MUTED)], c="green", id="ta")
    c.rect(530, 540, 300, 90, [("#VPC B · hub", PAL["blue"][2]), ("~10.0.0.0/16", MUTED)], c="blue", id="tb")
    c.rect(1016, 540, 300, 90, [("#VPC C · staging", PAL["orange"][2]), ("~10.20.0.0/16 · extension", MUTED)], c="orange", id="tc", dash="d")
    c.edge("ta", "tb", "r", "l", c="green", w=5, arrow="both", label="peered ✓", lc="green")
    c.edge("tb", "tc", "r", "l", c="green", w=5, arrow="both", label="peered ✓", lc="green")
    c.edge("ta", "tc", "b", "b", via=[(194, 700), (1166, 700)], c="red", w=4, dash="d", arrow="both", label="no transit ✗", lc="red", lpos=.5)
    c.text(44, 750, [("^PEERING CHECKLIST", PAL["indigo"][2])])
    for i, (t, d, col) in enumerate([("No overlapping CIDRs", "10.0.0.0/16 and 10.10.0.0/16 are distinct", "red"), ("Create both directions", "each VPC must peer to the other", "purple"), ("Add firewall rules", "peering opens routes, not ports", "orange"), ("Private IP only", "traffic stays on Google's network", "teal")]):
        c.rect(44 + i * 318, 782, 306, 90, [f"!{t}", f"_{d}"], c=col, pad=6)
    cmds(c, 44, 900, 900, ["gcloud compute networks peerings list", "ping 10.10.0.x (from the hub VM)"], title="VERIFY")
    c.footer("", "REMEMBER", lines=["Peering = private connectivity between two VPCs. Routes are exchanged; firewall policy, IAM and administration stay separate.",
                                    "Need many-to-many or central control? Use Shared VPC or a hub with VPN/NCC instead of a peering mesh."])
    c.save(out("terraform/06-vpc-peering-shared-vpc/diagrams/lab06-vpc-peering"))


def tf07():
    c = Canvas(1360, 1000, "Terraform Lab 07 — Layer 7 path-based load balancing", "One global address; the URL map reads the path and routes each request to the right backend service", f"TF LAB 07 · {CHIP}")
    chain = [("Internet users", "HTTP requests", "teal", "user"), ("Forwarding rule", "Anycast VIP · TCP 80", "orange", None), ("Target HTTP proxy", "ends the client connection", "purple", None), ("URL map", "reads host + path", "red", None)]
    for i, (t, d, col, ic) in enumerate(chain):
        x = 44 + i * 232
        c.rect(x, 180, 200, 100, [f"#{t}", f"_{d}"], c=col, id=f"c{i}", pad=4)
    for i in range(3):
        c.edge(f"c{i}", f"c{i + 1}", "r", "l", c="gray", w=4)
    c.rect(976, 130, 340, 100, [("#Web backend service", PAL["green"][2]), ("!default route", PAL["green"][2]), ("_named port: http · web MIG", MUTED)], c="green", id="bw")
    c.rect(976, 250, 340, 100, [("#API backend service", PAL["blue"][2]), ("!path /api/*", PAL["blue"][2]), ("_named port: http-api · API MIG", MUTED)], c="blue", id="ba")
    c.edge("c3", "bw", "r", "l", via=[(940, 230), (940, 180)], c="green", w=4)
    c.edge("c3", "ba", "r", "l", via=[(940, 230), (940, 300)], c="blue", w=4)
    c.rect(976, 380, 340, 80, [("!HTTP health check", PAL["teal"][2]), ("~GET /health · port 80", MUTED), ("_unhealthy VMs get no traffic", MUTED)], c="teal", white=True, shadow=False)
    c.text(44, 400, [("^TWO REQUESTS, TWO DESTINATIONS", PAL["indigo"][2])])
    c.rect(44, 436, 880, 120, [], c="green", white=True, shadow=False)
    c.text(64, 448, [("!GET /index.html", PAL["green"][2]), ("_URL map: no rule for /index.html → DEFAULT service → web backend → web VM pool", MUTED)])
    c.rect(64, 504, 840, 36, [("!forwarding rule → proxy → URL map → web backend service → web MIG", "#FFFFFF")], c="green", solid=True, shape="pill", shadow=False)
    c.rect(44, 576, 880, 120, [], c="blue", white=True, shadow=False)
    c.text(64, 588, [("!GET /api/users", PAL["blue"][2]), ("_URL map: path matches /api/* → API backend service → API VM pool", MUTED)])
    c.rect(64, 644, 840, 36, [("!forwarding rule → proxy → URL map → API backend service → API MIG", "#FFFFFF")], c="blue", solid=True, shape="pill", shadow=False)
    c.table(976, 500, [150, 190], [["Layer", "Decides on"], ["L4 (network LB)", "IP + port only"], ["L7 (this lab)", "host · path · headers"], ["Terraform", "url_map path_matcher"]], rowh=40, head="indigo")
    c.text(44, 730, [("^TERRAFORM RESOURCES IN THE CHAIN", PAL["indigo"][2])])
    for i, t in enumerate(["google_compute_global_forwarding_rule", "google_compute_target_http_proxy", "google_compute_url_map", "google_compute_backend_service × 2", "google_compute_health_check"]):
        c.rect(44 + (i % 3) * 424, 762 + (i // 3) * 48, 410, 40, [(f"~{t}", "#E2E8F0")], c="gray", solid=True, shape="pill", shadow=False, pad=6, fill="#1F2A44", stroke="#0B1220", tcolor="#E2E8F0")
    c.footer("", "REMEMBER", lines=["Reading the chain left to right gives the request path; reading the Terraform references right to left gives the build order.",
                                    "Health checks decide eligibility, the URL map decides destination, the backend service decides which VM in the pool."])
    c.save(out("terraform/07-load-balancing-l4-l7/diagrams/lab07-l7-load-balancing"))


def tf08():
    c = Canvas(1360, 1010, "Terraform Lab 08 — Site-to-site IPsec VPN with BGP", "IPsec encrypts the path; BGP runs inside the tunnel so each side learns the other's prefixes dynamically", f"TF LAB 08 · {CHIP}")
    c.group(44, 130, 440, 360, "ON-PREMISES · AS 65001", c="blue", tag="10.1.0.0/16")
    c.icon_box("opc", "pc", 100, 190, 56, "blue", "On-Prem Client", ["~10.1.1.10"])
    c.icon_box("cisco", "router", 330, 220, 80, "teal", "Cisco VPN router", ["~tunnel 169.254.0.1/30", "real static public IP"])
    c.group(876, 130, 440, 360, "GOOGLE CLOUD · AS 65000", c="green", tag="10.200.0.0/16")
    c.icon_box("hv", "router", 900, 220, 80, "orange", "HA VPN gateway", ["tunnel endpoint"])
    c.icon_box("cr", "router", 1060, 360, 64, "purple", "Cloud Router", ["~169.254.0.2/30"])
    c.icon_box("vm", "server", 1220, 190, 56, "green", "GCP test VM", ["~10.200.1.50"])
    c.icon("cloud", 590, 150, 100, "gray")
    c.text(665, 340, [("^PUBLIC INTERNET · UNTRUSTED UNDERLAY", MUTED)], anchor="m")
    link(c, "opc", "cisco", "r", "l", ly=260)
    c.line([(410, 260), (900, 260)], color="#7C4DDB", w=14, arrow="both")
    c.line([(410, 260), (900, 260)], color="#D6C2FF", w=3, arrow=None, dash="d")
    c.label(655, 260, "IPsec · ESP encrypted tunnel", c="purple", solid=True)
    c.line([(410, 310), (900, 310)], color="#E8890C", w=4, arrow="both")
    c.label(655, 310, "BGP over TCP 179 (inside the tunnel)", c="orange")
    c.line([(980, 260), (1220, 260)], color="#5B6677", w=4, arrow=None)
    c.line([(940, 300), (940, 392), (1060, 392)], color="#5B6677", w=4, arrow=None)
    c.rect(70, 400, 380, 70, [("!Advertises 10.1.0.0/16", PAL["blue"][2]), ("~network 10.1.0.0 mask 255.255.0.0", MUTED)], c="blue", white=True, shadow=False)
    c.text(44, 530, [("^HOW THE TUNNEL COMES UP · IN ORDER", PAL["indigo"][2])])
    steps(c, 44, 562, 640, [("IKE negotiation", "UDP 500/4500: peers authenticate with the pre-shared key"), ("IPsec SA created", "ESP tunnel up between the two public IPs"), ("BGP session over 169.254.0.0/30", "AS 65001 ↔ AS 65000: Idle → Active → Established"),
                            ("Prefixes exchanged", "on-prem learns 10.200.0.0/16; GCP learns 10.1.0.0/16"), ("Routes installed both ways", "forward AND return route are required"), ("Encrypted ping works", "10.1.1.10 → 10.200.1.50 and back")], col="indigo", h=54, gap=8, title="")
    c.rect(720, 562, 596, 120, [("#BGP advertisements", PAL["orange"][2]), ("~10.1.0.0/16   → learned by Cloud Router", PAL["blue"][2]), ("~10.200.0.0/16 → learned by Cisco router", PAL["green"][2]), ("_no static routes to maintain", MUTED)], c="orange", white=True, shadow=False, align="l", pad=20)
    c.rect(720, 700, 596, 96, [("!Failure domain check", PAL["red"][2]), ("_tunnel up but no ping?  BGP not Established, a missing", MUTED), ("_return route, or a firewall blocking 10.1.0.0/16 in GCP", MUTED)], c="red", white=True, shadow=False)
    cmds(c, 720, 820, 596, ["show crypto ikev2 sa", "show ip bgp summary", "show ip route bgp", "ping 10.200.1.50 source 10.1.1.1"], title="VERIFY ON THE CISCO ROUTER")
    c.save(out("terraform/08-ipsec-vpn-bgp-hybrid/diagrams/lab08-ipsec-bgp-hybrid"))


if __name__ == "__main__":
    for f in (tf01, tf02, tf03, tf04, tf05, tf06, tf07, tf08):
        f()
