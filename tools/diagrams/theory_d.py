from theory_a import OUT
from dgm import Canvas, PAL, MUTED


def cross(c, x, y, r=14):
    c.line([(x - r, y - r), (x + r, y + r)], color="#D93F3F", w=5, arrow=None)
    c.line([(x - r, y + r), (x + r, y - r)], color="#D93F3F", w=5, arrow=None)


def d09_tcp_udp():
    c = Canvas(1360, 1130, "TCP vs UDP: reliable conversation or fire-and-forget",
               "Both ride on IP and use ports; TCP adds a handshake, acknowledgements and retransmission, UDP adds almost nothing", "STAGE 09 · TRANSPORT")
    c.group(44, 130, 716, 640, "TCP · connection-oriented · reliable", c="blue", tag="IP protocol 6")
    c.rect(70, 188, 190, 64, [("#Client", PAL["blue"][2]), ("~port 51000", MUTED)], c="blue")
    c.rect(544, 188, 190, 64, [("#Server", PAL["green"][2]), ("~port 443", MUTED)], c="green")
    xa, xb = 165, 639
    c.lifeline(xa, 252, 750)
    c.lifeline(xb, 252, 750)
    c.msg(xa, xb, 316, "SYN  seq=100", "blue", lines=["“Can we talk?”"], w=3.5)
    c.msg(xb, xa, 392, "SYN-ACK  seq=300 ack=101", "green", lines=["“Yes — and can we?”"], w=3.5)
    c.msg(xa, xb, 468, "ACK  ack=301", "blue", lines=["“Yes.”  → ESTABLISHED"], w=3.5)
    for i, l in enumerate("123"):
        c.badge(l, 84, [316, 392, 468][i], "blue")
    c.msg(xa, xb, 560, "DATA  seq=101 len=100", "blue", w=3.5)
    c.msg(xb, xa, 620, "ACK  ack=201", "green", w=3.5)
    c.line([(xa, 690), (xa + 200, 690)], color="#D93F3F", w=3.5, arrow=None)
    cross(c, xa + 215, 690)
    c.text(xa + 250, 666, [("!DATA seq=201 — lost!", PAL["red"][2])])
    c.msg(xa, xb, 730, "retransmit seq=201 (no ACK in time)", "orange", w=3.5)
    c.group(800, 130, 516, 640, "UDP · connectionless · best effort", c="orange", tag="IP protocol 17")
    c.rect(826, 188, 170, 64, [("#Client", PAL["blue"][2]), ("~port 49152", MUTED)], c="blue")
    c.rect(1120, 188, 170, 64, [("#DNS server", PAL["green"][2]), ("~port 53", MUTED)], c="green")
    ua, ub = 911, 1205
    c.lifeline(ua, 252, 750)
    c.lifeline(ub, 252, 750)
    c.msg(ua, ub, 330, "datagram 1  (query)", "blue", lines=["no handshake first"], w=3.5)
    c.msg(ub, ua, 420, "datagram 2  (answer)", "green", lines=["no ACK needed"], w=3.5)
    c.line([(ua, 520), (ua + 160, 520)], color="#D93F3F", w=3.5, arrow=None)
    cross(c, ua + 176, 520)
    c.text(ua + 205, 494, [("!datagram 3 — lost", PAL["red"][2])])
    c.rect(832, 560, 460, 84, [("!Nobody retransmits for you", PAL["red"][2]), ("_The application decides: retry (DNS) or skip the", MUTED), ("_missing frame (live video, voice, games)", MUTED)], c="red", white=True, shadow=False)
    c.rect(832, 664, 460, 84, [("!Why bother?  Speed and simplicity", PAL["orange"][2]), ("_8-byte header, no waiting, works with broadcast", MUTED), ("_and multicast, perfect for small request/response", MUTED)], c="orange", white=True, shadow=False)
    c.text(44, 800, [("^HEADERS — HOW MUCH EACH PROTOCOL ADDS", PAL["indigo"][2])])
    c.fields(44, 836, 48, [("Src port", 3, "blue"), ("Dst port", 3, "blue"), ("Seq number", 5, "purple"), ("Ack number", 5, "purple"), ("Flags", 4, "red"), ("Window", 4, "gray")], 716)
    c.text(44, 890, [("_TCP header: 20+ bytes — sequence and ack numbers enable ordering, retransmission and flow control", MUTED)])
    c.fields(800, 836, 48, [("Src port", 3, "blue"), ("Dst port", 3, "blue"), ("Length", 2, "orange"), ("Checksum", 2, "gray")], 516)
    c.text(800, 890, [("_UDP header: 8 bytes — ports, length, checksum. That's all.", MUTED)])
    c.table(44, 930, [180, 530, 562], [["", "TCP — use when every byte must arrive", "UDP — use when speed beats perfection"], ["Examples", "HTTP/HTTPS · SSH · email · file transfer · databases", "DNS · DHCP · VoIP · video calls · online games · QUIC"]],
            rowh=38, head="blue")
    c.footer("", "REMEMBER", lines=["TCP = SYN, SYN-ACK, ACK, then numbered data with ACKs and retransmits.  UDP = just send it.",
                                    "Neither is 'better': pick reliability (TCP) or low latency (UDP) based on what the application can tolerate losing."])
    c.save(f"{OUT}/09-tcp-handshake-vs-udp")


def d10_dns():
    c = Canvas(1360, 1260, "DNS: how a name becomes an IP address",
               "A recursive resolver walks the hierarchy from root to authoritative server, then caches the answer for its TTL", "STAGE 10 · DNS & PORTS")
    cols = [("Client", "stub resolver", "blue", 150), ("Recursive resolver", "ISP / 8.8.8.8 / VPC DNS", "purple", 420), ("Root server", ".", "red", 690),
            (".com TLD server", "knows who runs .com", "orange", 960), ("Authoritative", "example.com's NS", "green", 1230)]
    for t, sub, col, x in cols:
        c.rect(x - 112, 130, 224, 78, [f"#{t}", f"_{sub}"], c=col, pad=6)
        c.lifeline(x, 208, 850)
    X = [x for *_, x in cols]
    steps = [(0, 1, "www.example.com ?", "blue", "① the question  (UDP 53)", 290), (1, 2, "www.example.com ?", "purple", "② cache miss → ask a root server", 360),
             (2, 1, "ask .com servers", "red", "③ referral: NS records + glue", 430), (1, 3, "www.example.com ?", "purple", "④ ask the .com TLD", 500),
             (3, 1, "ask ns1.example.com", "orange", "⑤ referral to the authoritative NS", 570), (1, 4, "www.example.com ?", "purple", "⑥ ask the authority", 640),
             (4, 1, "A  93.184.216.34  TTL 300", "green", "⑦ the real answer", 710), (1, 0, "A  93.184.216.34", "purple", "⑧ answer returned, cached 300 s", 780)]
    for a, b, t, col, sub, y in steps:
        c.msg(X[a], X[b], y, t, col, lines=[sub], w=3.5, dash="d" if a > b and b != 0 else None)
    c.text(44, 920, [("^NAME HIERARCHY — READ RIGHT TO LEFT", PAL["indigo"][2])])
    for i, (t, col, x, w) in enumerate([("www", "green", 44, 150), ("example", "green", 214, 190), (".com", "orange", 424, 150), (". (root)", "red", 594, 170)]):
        c.rect(x, 954, w, 56, [f"#{t}"], c=col, solid=True, shape="pill", shadow=False)
    for x in (194, 404, 574):
        c.line([(x, 982), (x + 20, 982)], color="#5B6677", w=3, arrow=None)
    c.text(44, 1022, [("_host → domain → TLD → root. The resolver asks the root first and narrows down.", MUTED)])
    c.table(800, 920, [110, 160, 246], [["Record", "Maps", "Example"], ["A", "name → IPv4", "93.184.216.34"], ["AAAA", "name → IPv6", "2606:2800::1"], ["CNAME", "name → name", "www → example.com"], ["MX", "mail server", "10 mail.example.com"]],
            rowh=34, head="indigo", mono_cols=(0, 2))
    c.footer("", "REMEMBER", lines=["Recursive resolver does the legwork; root, TLD and authoritative servers only point you one step closer.",
                                    "DNS uses port 53 (UDP first, TCP for big answers). Low TTL = faster changes, more lookups."])
    c.save(f"{OUT}/10-dns-resolution-walk")


def d11_tls():
    c = Canvas(1360, 1240, "HTTPS = HTTP inside TLS: identity first, then secret keys",
               "TLS proves the server is who it claims to be, agrees on session keys, then encrypts every HTTP request and response", "STAGE 11 · HTTP & TLS")
    c.group(44, 130, 770, 560, "TLS 1.3 handshake · happens after TCP connects", c="purple", tag="TCP 443")
    c.rect(72, 190, 200, 64, [("#Browser", PAL["blue"][2]), ("_the client", MUTED)], c="blue")
    c.rect(588, 190, 200, 64, [("#Web server", PAL["green"][2]), ("_example.com", MUTED)], c="green")
    xa, xb = 172, 688
    c.lifeline(xa, 254, 668)
    c.lifeline(xb, 254, 668)
    c.msg(xa, xb, 330, "ClientHello", "blue", lines=["TLS versions · cipher suites · key share · SNI=example.com"], w=3.5)
    c.msg(xb, xa, 420, "ServerHello + Certificate + key share + Finished", "green", lines=["picks cipher · sends certificate chain · proves it owns the key"], w=3.5)
    c.rect(xa + 8, 452, 240, 62, [("!Client verifies", PAL["purple"][2]), ("_chain · name · dates · signature", MUTED)], c="purple", white=True, shadow=False, pad=4)
    c.msg(xa, xb, 560, "Finished", "blue", lines=["both sides now derive the same session keys"], w=3.5)
    c.rect(222, 610, 410, 54, [("!HTTP over TLS — encrypted both ways", "#FFFFFF")], c="green", solid=True, shape="pill", shadow=False)
    c.badge(1, 62, 330, "blue")
    c.badge(2, 62, 420, "green")
    c.badge(3, 62, 560, "blue")
    c.group(850, 130, 466, 560, "Why you can trust the certificate", c="indigo")
    for i, (t, sub, col) in enumerate([("Root CA", "pre-installed in your OS/browser", "red"), ("Intermediate CA", "signed by the root", "orange"), ("example.com certificate", "signed by the intermediate", "green")]):
        c.rect(890, 190 + i * 112, 300, 74, [f"#{t}", f"_{sub}"], c=col, id=f"ca{i}", pad=6)
    c.edge("ca0", "ca1", "b", "t", c="gray", w=3.5, label="signs", loff=(34, 0))
    c.edge("ca1", "ca2", "b", "t", c="gray", w=3.5, label="signs", loff=(34, 0))
    c.icon("lock", 1220, 214, 64, "green")
    c.rect(870, 540, 426, 128, [("!Browser checks", PAL["indigo"][2]), ("_✓ chain leads to a trusted root", MUTED), ("_✓ hostname matches the certificate", MUTED), ("_✓ not expired · not revoked · signature valid", MUTED)], c="indigo", white=True, shadow=False, align="l", pad=20)
    c.text(44, 726, [("^ASYMMETRIC → SYMMETRIC: WHY THE SWITCH MID-HANDSHAKE", PAL["indigo"][2])])
    c.rect(44, 760, 400, 110, [("#Asymmetric (key pair)", PAL["purple"][2]), ("_public key / private key", MUTED), ("_slow · used to prove identity", MUTED), ("_and agree on a shared secret", MUTED)], c="purple")
    c.rect(480, 760, 140, 110, [("!then", PAL["gray"][2]), ("~→", PAL["gray"][2])], c="gray", white=True, shadow=False)
    c.rect(656, 760, 400, 110, [("#Symmetric (one shared key)", PAL["green"][2]), ("_AES / ChaCha20", MUTED), ("_fast · used to encrypt all the", MUTED), ("_actual HTTP traffic", MUTED)], c="green")
    c.rect(1092, 760, 224, 110, [("!HTTPS port", PAL["orange"][2]), ("#443", PAL["orange"][3]), ("_HTTP is 80", MUTED)], c="orange", white=True, shadow=False)
    c.text(44, 906, [("^THE HTTP CONVERSATION INSIDE THE TUNNEL", PAL["indigo"][2])])
    c.rect(44, 940, 500, 140, [("^REQUEST", PAL["blue"][2]), ("~GET /index.html HTTP/1.1", PAL["blue"][2]), ("~Host: example.com", MUTED), ("~Accept: text/html", MUTED), ("~Cookie: session=…", MUTED)], c="blue", align="l", pad=20)
    c.rect(580, 940, 500, 140, [("^RESPONSE", PAL["green"][2]), ("~HTTP/1.1 200 OK", PAL["green"][2]), ("~Content-Type: text/html", MUTED), ("~Content-Length: 1256", MUTED), ("~<html>…</html>", MUTED)], c="green", align="l", pad=20)
    for i, (k, t, col) in enumerate([("2xx", "success", "green"), ("3xx", "redirect", "blue"), ("4xx", "client error", "orange"), ("5xx", "server error", "red")]):
        c.rect(1116, 940 + i * 36, 200, 32, [(f"!{k}  {t}", "#FFFFFF")], c=col, solid=True, shape="pill", shadow=False)
    c.footer("", "REMEMBER", lines=["TLS gives confidentiality, integrity and server identity. Certificates chain up to a root your device already trusts.",
                                    "Methods: GET read · POST create · PUT replace · DELETE remove. Status class tells you who is at fault: 4xx you, 5xx server."])
    c.save(f"{OUT}/11-tls-handshake-and-http")


def d12_acl():
    c = Canvas(1360, 1110, "ACLs and segmentation: ordered rules, first match wins",
               "Segments separate networks; routers let them talk; ACLs decide exactly which conversations are allowed", "STAGE 12 · ACLs & SEGMENTATION")
    hosts = [("eng", "Engineering VLAN 10", "192.168.10.0/24", "blue", 170), ("hr", "HR VLAN 20", "192.168.20.0/24", "purple", 290), ("gu", "Guest VLAN 30", "192.168.30.0/24", "orange", 410)]
    for k, t, ip, col, y in hosts:
        c.rect(60, y, 230, 84, [f"#{t}", f"~{ip}"], c=col, id=k)
    c.icon_box("rt", "router", 410, 262, 100, "teal", "Router · ACLs")
    c.rect(620, 262, 190, 100, [("#Corp server", PAL["green"][2]), ("~10.1.50.10", MUTED), ("_10.1.50.0/24", MUTED)], c="green", id="srv")
    c.edge("eng", "rt", "r", "l.2", via=[(330, 212), (330, 282)], c="green", w=4)
    c.edge("hr", "rt", "r", "l.7", c="green", w=4)
    c.edge("gu", "rt", "r", "l.9", via=[(370, 452), (370, 352)], c="red", w=4, dash="d")
    c.label(330, 247, "✓ 443 only", c="green")
    c.label(350, 332, "✓ allowed", c="green")
    c.label(370, 402, "✗ blocked", c="red")
    c.edge("rt", "srv", "r", "l", c="gray", w=4)
    c.text(44, 116, [("^TOPOLOGY · INTER-VLAN TRAFFIC CROSSES THE ROUTER", PAL["indigo"][2])])
    c.group(850, 130, 466, 440, "ACL 110 · applied inbound on Gi0/0.30", c="red")
    rules = [("10", "permit", "tcp  Eng  →  server  :443", "green"), ("20", "deny", "ip  Guest  →  10.1.50.0/24", "red"), ("30", "permit", "ip  any  →  any", "blue"), ("∞", "deny", "any any  (implicit, invisible)", "gray")]
    for i, (n, act, t, col) in enumerate(rules):
        y = 190 + i * 86
        c.rect(874, y, 418, 70, [f"!{act.upper()}", f"~{t}"], c=col, align="l", pad=70, dash="d" if n == "∞" else None, shadow=False)
        c.badge(n, 910, y + 35, col, r=16) if n != "∞" else c.badge("0", 910, y + 35, "gray", r=16)
    c.text(874, 540, [("_Top to bottom · first match wins · stop reading", MUTED)])
    c.rect(44, 520, 760, 50, [("!A guest packet to the server hits rule 20 → DENIED. It never reaches rule 30.", PAL["red"][2])], c="red", white=True, shape="pill", shadow=False)
    c.text(44, 606, [("^WHERE AND WHICH WAY? — A RULE ON THE WRONG INTERFACE DOES NOTHING", PAL["indigo"][2])])
    c.rect(44, 642, 200, 70, [("#Source", PAL["blue"][2]), ("_sends packet", MUTED)], c="blue", id="a1")
    c.rect(330, 642, 240, 70, [("#Router", PAL["teal"][2]), ("_routing decision", MUTED)], c="teal", id="a2")
    c.rect(656, 642, 200, 70, [("#Destination", PAL["green"][2]), ("_receives", MUTED)], c="green", id="a3")
    c.edge("a1", "a2", "r", "l", c="gray", w=4)
    c.edge("a2", "a3", "r", "l", c="gray", w=4)
    c.rect(272, 728, 110, 36, [("!IN ▼", "#FFFFFF")], c="orange", solid=True, shape="pill", shadow=False)
    c.rect(518, 728, 110, 36, [("!OUT ▼", "#FFFFFF")], c="purple", solid=True, shape="pill", shadow=False)
    c.text(327, 772, [("_checked BEFORE routing", MUTED)], anchor="m")
    c.text(573, 772, [("_checked AFTER routing", MUTED)], anchor="m")
    c.rect(900, 620, 416, 168, [("!Wildcard mask: 0 = match, 1 = ignore", PAL["indigo"][2]), ("~/24  255.255.255.0   →  0.0.0.255", PAL["indigo"][2]), ("~/26  255.255.255.192 →  0.0.0.63", PAL["indigo"][2]), ("~/30  255.255.255.252 →  0.0.0.3", PAL["indigo"][2]), ("~host 10.1.50.10  =  0.0.0.0", MUTED)], c="indigo", white=True, shadow=False, align="l", pad=18)
    c.rect(44, 812, 380, 150, [("#Standard ACL", PAL["blue"][2]), ("_matches SOURCE address only", MUTED), ("!Place near the DESTINATION", PAL["blue"][2]), ("_(or it blocks the source from everything)", MUTED)], c="blue")
    c.rect(450, 812, 380, 150, [("#Extended ACL", PAL["green"][2]), ("_protocol · source · destination · port", MUTED), ("!Place near the SOURCE", PAL["green"][2]), ("_(drop unwanted traffic early)", MUTED)], c="green")
    c.rect(856, 812, 460, 150, [("#Classic ACLs are stateless", PAL["orange"][2]), ("_each packet judged alone; the reply is a", MUTED), ("_new packet that needs its own permit.", MUTED), ("!Stateful tracking → next stage: firewalls", PAL["orange"][2])], c="orange")
    c.footer("", "REMEMBER", lines=["Order · direction · placement · implicit deny — the four things that decide what an ACL really does.",
                                    "Segmentation (VLAN + subnet) creates the boundary; the ACL is the policy that says who may cross it."])
    c.save(f"{OUT}/12-acl-evaluation-and-segmentation")


if __name__ == "__main__":
    for f in (d09_tcp_udp, d10_dns, d11_tls, d12_acl):
        f()
