"""Tiny diagram toolkit: one spec -> native draw.io XML and a matching SVG.

Every primitive (rect, text, edge, icon...) is stored once and rendered twice,
so the committed .drawio file (editable) and .svg file (embedded in MkDocs)
always show the same picture.
"""
import html
import math
from pathlib import Path

SANS = "system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
INK = "#1F2A44"
MUTED = "#5B6677"
BG = "#FBFCFE"

PAL = {
    "blue": ("#E8F1FF", "#4C8DF6", "#1C3F94", "#2F6FE0"),
    "green": ("#E4F7EC", "#34B27B", "#11603E", "#1E9A63"),
    "orange": ("#FFF0DC", "#F5A524", "#7A4300", "#E8890C"),
    "red": ("#FDE8E8", "#EF5B5B", "#8E1B1B", "#D93F3F"),
    "purple": ("#F1E9FE", "#9B6CF0", "#4B2A9A", "#7C4DDB"),
    "teal": ("#DFF6F5", "#20B2AA", "#0B5E5A", "#12908A"),
    "yellow": ("#FFF8D6", "#E6C229", "#5F4C00", "#CFA800"),
    "pink": ("#FFE8F3", "#EC5FA5", "#8A1E56", "#D63F8C"),
    "gray": ("#F1F3F6", "#8B95A5", "#2F3846", "#5B6677"),
    "indigo": ("#E9EAFE", "#6366F1", "#2B2D8F", "#4F46E5"),
}
RAINBOW = ["#2F6FE0", "#7C4DDB", "#D63F8C", "#E8890C", "#1E9A63"]

KINDS = {
    "h": (18, 700, False, 26),
    "b": (15, 700, False, 21),
    "p": (15, 400, False, 21),
    "m": (14, 500, True, 20),
    "s": (13, 400, False, 18),
    "k": (12, 700, False, 17),
}
PREFIX = {"#": "h", "!": "b", "~": "m", "_": "s", "^": "k"}


def esc(s):
    return html.escape(str(s), quote=True)


def mix(a, b, t):
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(ca, cb))


def parse_lines(lines):
    out = []
    for ln in ([lines] if isinstance(lines, str) else lines):
        color = None
        if isinstance(ln, tuple):
            ln, color = ln
        kind = "p"
        if ln and ln[0] in PREFIX and (len(ln) == 1 or ln[1] != ln[0]):
            kind, ln = PREFIX[ln[0]], ln[1:]
        out.append((ln, kind, color))
    return out


def est_w(text, kind):
    fs, fw, mono, _ = KINDS[kind]
    return len(text) * fs * (0.6 if mono else (0.56 if fw >= 700 else 0.52)) + (1.2 * len(text) if kind == 'k' else 0)


def lines_h(pl):
    return sum(KINDS[k][3] for _, k, _ in pl)


def style(c, solid=False, white=False):
    light, mid, dark, head = PAL[c]
    if solid:
        return dict(fill=head, grad=mix(head, "#000000", .14), stroke=mix(head, "#000000", .28), text="#FFFFFF", base=head)
    if white:
        return dict(fill="#FFFFFF", grad="#FFFFFF", stroke=mid, text=dark, base="#FFFFFF")
    return dict(fill=light, grad=mix(light, mid, .16), stroke=mid, text=dark, base=light)


def anchor_pt(b, side):
    x, y, w, h = b
    f = .5
    if len(side) > 1:
        f = float("0." + side[2:]) if side[1] == "." else float(side[1:])
    s = side[0]
    return {"l": (x, y + h * f), "r": (x + w, y + h * f), "t": (x + w * f, y), "b": (x + w * f, y + h)}[s], s, f


class Canvas:
    def __init__(self, w, h, title, subtitle="", chip="", bg=BG):
        self.w, self.h, self.bg = w, h, bg
        self.items, self.reg, self.warns, self.title = [], {}, [], title
        self.subtitle = subtitle
        self._n = 1
        self._banner(title, subtitle, chip)

    def _id(self):
        self._n += 1
        return f"c{self._n}"

    def _add(self, d):
        d.setdefault("cid", self._id())
        self.items.append(d)
        return d

    def _banner(self, title, subtitle, chip):
        self._add(dict(k="strip"))
        self.text(44, 28, [f"#{title}"], big=True)
        if subtitle:
            self.text(44, 72, [("_" + subtitle, MUTED)], sub=True)
        if chip:
            cw = est_w(chip, "k") + 40
            self.rect(self.w - 44 - cw, 30, cw, 30, [(f"^{chip}", "#FFFFFF")], c="indigo", solid=True, shape="pill", shadow=False)

    def rect(self, x, y, w, h, lines=(), c="blue", solid=False, white=False, shape="round", rx=14, dash=None,
             sw=2, id=None, align="c", pad=14, shadow=True, opacity=1, fill=None, stroke=None, tcolor=None, nofill=False):
        st = style(c, solid, white)
        if fill:
            st = dict(st, fill=fill, grad=fill)
        if stroke:
            st["stroke"] = stroke
        if tcolor:
            st["text"] = tcolor
        pl = parse_lines(lines)
        for t, k, _ in pl:
            if shape not in ("circle", "diamond", "cloud") and est_w(t, k) > w - 2 * pad + 6:
                self.warns.append(f"overflow in {id or t[:20]!r}: '{t}' ({est_w(t, k):.0f} > {w - 2 * pad})")
        if shape == "pill":
            rx = h / 2
        if shape == "rect":
            rx = 4
        d = self._add(dict(k="rect", x=x, y=y, w=w, h=h, pl=pl, st=st, shape=shape, rx=rx, dash=dash, sw=sw,
                           align=align, pad=pad, shadow=shadow, opacity=opacity, nofill=nofill))
        if id:
            self.reg[id] = (x, y, w, h, d["cid"])
        return d

    def group(self, x, y, w, h, title, c="blue", tag="", id=None, hh=38):
        st = style(c)
        d = self._add(dict(k="group", x=x, y=y, w=w, h=h, title=title, st=st, solid=style(c, True), hh=hh, tag=tag))
        if id:
            self.reg[id] = (x, y, w, h, d["cid"])
        return d

    def zone(self, x, y, w, h, label="", c="blue", id=None, lpos="tl"):
        st = style(c)
        self._add(dict(k="rect", x=x, y=y, w=w, h=h, pl=[], st=dict(st, fill=mix(st["fill"], "#FFFFFF", .45), grad=mix(st["fill"], "#FFFFFF", .45)),
                       shape="round", rx=18, dash="d", sw=2, align="c", pad=0, shadow=False, opacity=1, nofill=False))
        if label:
            self.text(x + 16, y + 10, [(f"^{label.upper()}", PAL[c][2])])
        if id:
            self.reg[id] = (x, y, w, h, None)

    def text(self, x, y, lines, anchor="l", c=None, bg=None, big=False, sub=False, bold=None, size=None):
        pl = parse_lines(lines)
        d = self._add(dict(k="text", x=x, y=y, pl=pl, anchor=anchor, c=c or INK, bg=bg, big=big, sub=sub, size=size))
        return d

    def label(self, x, y, text, c="gray", anchor="m", solid=False):
        st = style(c, solid)
        pl = parse_lines([f"!{text}"])
        w = est_w(text, "b") + 20
        h = 26
        ox = {"m": x - w / 2, "l": x, "r": x - w}[anchor]
        self._add(dict(k="rect", x=ox, y=y - h / 2, w=w, h=h, pl=[(text, "b", None)], st=dict(st, fill=st["fill"] if solid else "#FFFFFF", grad=st["fill"] if solid else "#FFFFFF"),
                       shape="pill", rx=h / 2, dash=None, sw=1.5, align="c", pad=8, shadow=False, opacity=1, nofill=False, small=True))

    def badge(self, n, x, y, c="blue", r=15):
        self._add(dict(k="rect", x=x - r, y=y - r, w=2 * r, h=2 * r, pl=[(str(n), "b", None)], st=style(c, True), shape="circle",
                       rx=r, dash=None, sw=2, align="c", pad=0, shadow=True, opacity=1, nofill=False))

    def line(self, pts, c="gray", w=2.5, dash=None, arrow="end", color=None, src=None, tgt=None, sa=None, sb=None, rounded=True):
        col = color or PAL[c][3]
        self._add(dict(k="edge", pts=pts, color=col, w=w, dash=dash, arrow=arrow, src=src, tgt=tgt, sa=sa, sb=sb, rounded=rounded))

    def edge(self, a, b, sa="r", sb="l", via=(), c="gray", w=2.5, dash=None, arrow="end", label=None, lpos=.5, loff=(0, 0),
             lc=None, color=None, solid_label=False):
        pa, s1, f1 = anchor_pt(self.reg[a][:4], sa)
        pb, s2, f2 = anchor_pt(self.reg[b][:4], sb)
        if via:
            pts = [pa, *via, pb]
        elif abs(pa[0] - pb[0]) < 1 or abs(pa[1] - pb[1]) < 1:
            pts = [pa, pb]
        elif s1 in "lr" and s2 in "lr":
            mx = (pa[0] + pb[0]) / 2
            pts = [pa, (mx, pa[1]), (mx, pb[1]), pb]
        elif s1 in "tb" and s2 in "tb":
            my = (pa[1] + pb[1]) / 2
            pts = [pa, (pa[0], my), (pb[0], my), pb]
        elif s1 in "lr":
            pts = [pa, (pb[0], pa[1]), pb]
        else:
            pts = [pa, (pa[0], pb[1]), pb]
        col = color or PAL[c][3]
        self._add(dict(k="edge", pts=pts, color=col, w=w, dash=dash, arrow=arrow, rounded=True,
                       src=self.reg[a][4], tgt=self.reg[b][4], sa=(s1, f1), sb=(s2, f2)))
        if label:
            px, py = point_at(pts, lpos)
            self.label(px + loff[0], py + loff[1], label, c=lc or c, solid=solid_label)

    def msg(self, x1, x2, y, text, c="blue", dash=None, w=2.5, lines=None):
        self.line([(x1, y), (x2, y)], c=c, w=w, dash=dash)
        mx = (x1 + x2) / 2
        if text:
            self.text(mx, y - 25, [(f"!{text}", PAL[c][2])], anchor="m")
        if lines:
            self.text(mx, y + 6, [(l, MUTED) for l in lines], anchor="m")

    def lifeline(self, x, y1, y2, c="gray"):
        self.line([(x, y1), (x, y2)], c=c, w=2, dash="d", arrow=None, color="#B8C0CC")

    def fields(self, x, y, h, cells, total_w, c="blue", gap=0, sizes=None):
        tot = sum(wt for _, wt, _ in cells)
        cx = x
        for label, wt, col in cells:
            cw = total_w * wt / tot
            self.rect(cx, y, cw, h, label if isinstance(label, list) else [label], c=col or c, solid=False, shape="rect", sw=1.8,
                      shadow=False, pad=6)
            cx += cw + gap

    def table(self, x, y, colw, rows, rowh=34, head="blue", zebra=True, mono_cols=(), kinds=None, rowc=None):
        cy = y
        for ri, row in enumerate(rows):
            cx = x
            for ci, cell in enumerate(row):
                if ri == 0:
                    self.rect(cx, cy, colw[ci], rowh, [f"!{cell}"], c=head, solid=True, shape="rect", sw=1, shadow=False, pad=8)
                else:
                    col = (rowc[ri - 1] if rowc and rowc[ri - 1] else "gray")
                    pre = "~" if ci in mono_cols else ""
                    self.rect(cx, cy, colw[ci], rowh, [f"{pre}{cell}"] if cell else [], c=col, white=(ri % 2 == 1 or not zebra) and not (rowc and rowc[ri - 1]),
                              shape="rect", sw=1, shadow=False, pad=8, align="c")
                cx += colw[ci]
            cy += rowh
        return cy

    def footer(self, text, label="REMEMBER", c="yellow", lines=None):
        lines = lines or [text]
        h = 30 + 24 * len(lines)
        y = self.h - h - 28
        self.rect(44, y, self.w - 88, h, [], c=c, shape="round", rx=16, shadow=True)
        self.rect(60, y + h / 2 - 15, est_w(label, "k") + 34, 30, [(f"^{label}", "#FFFFFF")], c="orange", solid=True, shape="pill", shadow=False)
        lx = 60 + est_w(label, "k") + 34 + 20
        for i, l in enumerate(lines):
            self.text(lx, y + 15 + i * 24, [(f"!{l}", PAL[c][2])])
            if est_w(l, "b") > self.w - lx - 60:
                self.warns.append(f"footer overflow: {l[:40]}")

    def icon(self, kind, x, y, s=64, c="blue", label=None, lsub=None):
        light, mid, dark, head = PAL[c]
        R = lambda *a, **k: self._add(dict(k="rect", pl=[], st=dict(fill=k.get("fill", head), grad=k.get("fill", head), stroke=k.get("stroke", dark), text="#fff"),
                                          shape=k.get("shape", "round"), rx=k.get("rx", 4), dash=None, sw=k.get("sw", 1.5), align="c", pad=0,
                                          shadow=False, opacity=1, nofill=k.get("nofill", False), x=a[0], y=a[1], w=a[2], h=a[3]))
        L = lambda pts, col="#FFFFFF", w=2: self.line(pts, w=w, arrow=None, color=col, rounded=False)
        if kind == "pc":
            R(x, y, s, .64 * s, rx=6)
            R(x + 5, y + 5, s - 10, .64 * s - 10, fill=light, stroke=mid, rx=3, sw=1)
            R(x + .4 * s, y + .64 * s, .2 * s, .12 * s, fill=mid, stroke=dark, rx=1)
            R(x + .22 * s, y + .76 * s, .56 * s, .08 * s, rx=4)
        elif kind == "server":
            for i in range(3):
                yy = y + i * .34 * s
                R(x, yy, s, .28 * s, rx=6)
                R(x + .1 * s, yy + .09 * s, .1 * s, .1 * s, fill="#7CFFB2", stroke="#7CFFB2", shape="circle", sw=.5)
                L([(x + .3 * s, yy + .14 * s), (x + .85 * s, yy + .14 * s)], w=2.5)
        elif kind == "switch":
            R(x, y + .2 * s, s, .5 * s, rx=8)
            for i in range(6):
                R(x + .08 * s + i * .15 * s, y + .45 * s, .1 * s, .14 * s, fill=light, stroke=light, rx=1, sw=.5)
            L([(x + .12 * s, y + .32 * s), (x + .88 * s, y + .32 * s)], w=2.5)
        elif kind == "router":
            R(x, y, s, s, shape="circle", rx=s / 2)
            m, e = s / 2, .28 * s
            L([(x + m - e - 6, y + m), (x + m + e + 6, y + m)], w=3)
            L([(x + m, y + m - e - 6), (x + m, y + m + e + 6)], w=3)
            for p in [(x + m + e + 8, y + m, 1, 0), (x + m - e - 8, y + m, -1, 0), (x + m, y + m - e - 8, 0, -1), (x + m, y + m + e + 8, 0, 1)]:
                px, py, dx, dy = p
                tri = [(px, py), (px - dx * 9 - dy * 6, py - dy * 9 - dx * 6), (px - dx * 9 + dy * 6, py - dy * 9 + dx * 6)]
                self._add(dict(k="poly", pts=tri, fill="#FFFFFF", stroke="#FFFFFF"))
        elif kind == "firewall":
            R(x, y, s, .78 * s, rx=6)
            for i in (1, 2):
                L([(x + 3, y + i * .26 * s), (x + s - 3, y + i * .26 * s)], w=2)
            for i, off in enumerate([.5, .25, .75]):
                for j in range(3):
                    pass
            for row, offs in enumerate([[.5], [.25, .75], [.5]]):
                for o in offs:
                    L([(x + o * s, y + row * .26 * s + 2), (x + o * s, y + (row + 1) * .26 * s - 2)], w=2)
        elif kind == "lock":
            R(x + .22 * s, y, .56 * s, .62 * s, rx=.28 * s, nofill=True, stroke=head, sw=6)
            R(x + .1 * s, y + .4 * s, .8 * s, .58 * s, rx=8)
            R(x + .44 * s, y + .58 * s, .12 * s, .18 * s, fill="#FFFFFF", stroke="#FFFFFF", rx=3, sw=.5)
        elif kind == "user":
            R(x + .3 * s, y, .4 * s, .4 * s, shape="circle")
            R(x + .12 * s, y + .48 * s, .76 * s, .5 * s, rx=.25 * s)
        elif kind == "globe":
            R(x, y, s, s, fill=light, stroke=head, shape="circle", sw=2.5)
            R(x + .28 * s, y, .44 * s, s, fill=light, stroke=head, shape="circle", sw=1.8, nofill=True)
            L([(x, y + s / 2), (x + s, y + s / 2)], col=head, w=1.8)
            L([(x + s / 2, y), (x + s / 2, y + s)], col=head, w=1.8)
            L([(x + .1 * s, y + .27 * s), (x + .9 * s, y + .27 * s)], col=head, w=1.4)
            L([(x + .1 * s, y + .73 * s), (x + .9 * s, y + .73 * s)], col=head, w=1.4)
        elif kind == "db":
            self._add(dict(k="rect", x=x + .1 * s, y=y, w=.8 * s, h=s, pl=[], st=style(c, True), shape="cyl", rx=0, dash=None, sw=1.5, align="c", pad=0,
                           shadow=False, opacity=1, nofill=False))
        elif kind == "cloud":
            self._add(dict(k="rect", x=x, y=y, w=s * 1.5, h=s, pl=[], st=style(c), shape="cloud", rx=0, dash=None, sw=2.5, align="c", pad=0,
                           shadow=True, opacity=1, nofill=False))
        elif kind == "doc":
            R(x + .1 * s, y, .8 * s, s, fill="#FFFFFF", stroke=head, rx=6, sw=2.5)
            for i in range(4):
                L([(x + .25 * s, y + (.22 + i * .18) * s), (x + .75 * s, y + (.22 + i * .18) * s)], col=head, w=2.5)
        elif kind == "env":
            R(x, y + .12 * s, s, .76 * s, fill="#FFFFFF", stroke=head, rx=6, sw=2.5)
            L([(x + 3, y + .2 * s), (x + s / 2, y + .55 * s), (x + s - 3, y + .2 * s)], col=head, w=2.5)
        if label:
            subs = [lsub] if isinstance(lsub, str) else (lsub or [])
            self.text(x + s / 2, y + s + 10, [(f"!{label}", PAL[c][2])] + [((l if l.startswith("~") else f"_{l}"), MUTED) for l in subs], anchor="m")
        self.reg.setdefault(f"__icon{x}_{y}", (x, y, s, s, None))
        return (x, y, s, s)

    def icon_box(self, id, kind, x, y, s=64, c="blue", label=None, lsub=None):
        self.icon(kind, x, y, s, c, label, lsub)
        self.reg[id] = (x, y, s, s, None)

    # ----------------------------------------------------------------- render
    def save(self, base):
        base = Path(base)
        base.parent.mkdir(parents=True, exist_ok=True)
        base.with_suffix(".svg").write_text(self.to_svg(), encoding="utf-8")
        base.with_suffix(".drawio").write_text(self.to_drawio(), encoding="utf-8")
        for w in self.warns:
            print(f"  WARN {base.name}: {w}")

    def to_svg(self):
        defs, body, grads, marks = [], [], {}, {}

        def grad(c1, c2):
            key = (c1, c2)
            if key not in grads:
                grads[key] = f"g{len(grads)}"
                defs.append(f'<linearGradient id="{grads[key]}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')
            return f"url(#{grads[key]})"

        def mark(col, size):
            key = (col, size)
            if key not in marks:
                marks[key] = f"m{len(marks)}"
                defs.append(f'<marker id="{marks[key]}" markerWidth="{size}" markerHeight="{size * .8:.1f}" refX="{size - 1}" refY="{size * .4:.1f}" orient="auto-start-reverse" markerUnits="userSpaceOnUse"><path d="M0,0 L{size},{size * .4:.1f} L0,{size * .8:.1f} z" fill="{col}"/></marker>')
            return f"url(#{marks[key]})"

        defs.append('<filter id="sh" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#1B2A4A" flood-opacity="0.16"/></filter>')
        for it in self.items:
            k = it["k"]
            if k == "strip":
                n = len(RAINBOW)
                for i, col in enumerate(RAINBOW):
                    body.append(f'<rect x="{self.w * i / n:.1f}" y="0" width="{self.w / n + 1:.1f}" height="8" fill="{col}"/>')
            elif k == "rect":
                body.append(self._svg_rect(it, grad))
            elif k == "group":
                x, y, w, h, hh, st, so = it["x"], it["y"], it["w"], it["h"], it["hh"], it["st"], it["solid"]
                body.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{grad(st["fill"], st["grad"])}" stroke="{st["stroke"]}" stroke-width="2.5" filter="url(#sh)"/>')
                body.append(f'<path d="M{x},{y + hh} V{y + 18} a18,18 0 0 1 18,-18 H{x + w - 18} a18,18 0 0 1 18,18 V{y + hh} z" fill="{grad(so["fill"], so["grad"])}" stroke="{so["stroke"]}" stroke-width="2.5"/>')
                body.append(f'<text x="{x + 18}" y="{y + hh / 2 + 6}" font-family="{SANS}" font-size="17" font-weight="700" fill="#FFFFFF">{esc(it["title"])}</text>')
                if it["tag"]:
                    body.append(f'<text x="{x + w - 18}" y="{y + hh / 2 + 5}" text-anchor="end" font-family="{MONO}" font-size="14" fill="#FFFFFF" opacity=".92">{esc(it["tag"])}</text>')
            elif k == "text":
                body.append(self._svg_text(it))
            elif k == "poly":
                pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in it["pts"])
                body.append(f'<polygon points="{pts}" fill="{it["fill"]}" stroke="{it["stroke"]}"/>')
            elif k == "edge":
                body.append(self._svg_edge(it, mark))
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="t d">'
                f'<title id="t">{esc(self.title)}</title><desc id="d">{esc(self.subtitle)}</desc>')
        return head + "<defs>" + "".join(defs) + "</defs>" + f'<rect width="{self.w}" height="{self.h}" fill="{self.bg}"/>' + "\n".join(body) + "</svg>\n"

    def _svg_rect(self, it, grad):
        x, y, w, h, st, shape = it["x"], it["y"], it["w"], it["h"], it["st"], it["shape"]
        fill = "none" if it["nofill"] else grad(st["fill"], st["grad"])
        common = f'fill="{fill}" stroke="{st["stroke"]}" stroke-width="{it["sw"]}"'
        if it["dash"]:
            common += ' stroke-dasharray="9 7"'
        if it["opacity"] != 1:
            common += f' opacity="{it["opacity"]}"'
        if it["shadow"]:
            common += ' filter="url(#sh)"'
        if shape in ("round", "pill", "rect"):
            s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{it["rx"]}" {common}/>'
        elif shape == "circle":
            s = f'<ellipse cx="{x + w / 2}" cy="{y + h / 2}" rx="{w / 2}" ry="{h / 2}" {common}/>'
        elif shape == "diamond":
            s = f'<polygon points="{x + w / 2},{y} {x + w},{y + h / 2} {x + w / 2},{y + h} {x},{y + h / 2}" {common}/>'
        elif shape == "cyl":
            e = min(14, h * .12)
            s = (f'<path d="M{x},{y + e} a{w / 2},{e} 0 0 1 {w},0 V{y + h - e} a{w / 2},{e} 0 0 1 -{w},0 z" {common}/>'
                 f'<ellipse cx="{x + w / 2}" cy="{y + e}" rx="{w / 2}" ry="{e}" fill="{mix(st["fill"], "#FFFFFF", .35)}" stroke="{st["stroke"]}" stroke-width="{it["sw"]}"/>')
        elif shape == "cloud":
            parts = cloud_ellipses(x, y, w, h)
            s = "".join(f'<ellipse cx="{a}" cy="{b}" rx="{c}" ry="{d}" fill="{st["stroke"]}" stroke="{st["stroke"]}" stroke-width="{it["sw"] * 2}"/>' for a, b, c, d in parts)
            s = f'<g {"filter=" + chr(34) + "url(#sh)" + chr(34) if it["shadow"] else ""}>' + s + "".join(
                f'<ellipse cx="{a}" cy="{b}" rx="{c}" ry="{d}" fill="{grad(st["fill"], st["grad"])}"/>' for a, b, c, d in parts) + "</g>"
        else:
            s = ""
        s += self._svg_lines(it["pl"], x, y, w, h, it["align"], it["pad"], it["st"]["text"], it["st"].get("base", it["st"]["fill"]))
        return s

    def _svg_lines(self, pl, x, y, w, h, align, pad, tcolor, base):
        if not pl:
            return ""
        H = lines_h(pl)
        cy = y + (h - H) / 2
        out = []
        for t, kind, col in pl:
            fs, fw, mono, lh = KINDS[kind]
            c = col or (mix(tcolor, base, .30) if kind in ("s",) else tcolor)
            if align == "c":
                tx, anc = x + w / 2, "middle"
            else:
                tx, anc = x + pad, "start"
            extra = ' letter-spacing="1.2"' if kind == "k" else ""
            out.append(f'<text x="{tx}" y="{cy + lh / 2 + fs * .35:.1f}" text-anchor="{anc}" font-family="{MONO if mono else SANS}" font-size="{fs}" font-weight="{fw}" fill="{c}"{extra}>{esc(t)}</text>')
            cy += lh
        return "".join(out)

    def _svg_text(self, it):
        pl, x, y, anchor = it["pl"], it["x"], it["y"], it["anchor"]
        out = []
        cy = y
        anc = {"l": "start", "m": "middle", "r": "end"}[anchor]
        for t, kind, col in pl:
            fs, fw, mono, lh = KINDS[kind]
            if it["big"]:
                fs, lh = 32, 40
            if it["sub"]:
                fs, lh = 17, 24
            c = col or it["c"]
            extra = ' letter-spacing="1.2"' if kind == "k" else ""
            out.append(f'<text x="{x}" y="{cy + lh / 2 + fs * .35:.1f}" text-anchor="{anc}" font-family="{MONO if mono else SANS}" font-size="{fs}" font-weight="{fw}" fill="{c}"{extra}>{esc(t)}</text>')
            cy += lh
        return "".join(out)

    def _svg_edge(self, it, mark):
        pts, col, w = it["pts"], it["color"], it["w"]
        d = path_d(pts, 12 if it["rounded"] else 0)
        size = 8 + w * 1.6
        attrs = f'fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'
        if it["dash"] == "d":
            attrs += ' stroke-dasharray="10 7"'
        elif it["dash"] == "dot":
            attrs += f' stroke-dasharray="0.1 {w * 2.6:.1f}"'
        if it["arrow"] in ("end", "both"):
            attrs += f' marker-end="{mark(col, size)}"'
        if it["arrow"] in ("start", "both"):
            attrs += f' marker-start="{mark(col, size)}"'
        return f'<path d="{d}" {attrs}/>'

    def to_drawio(self):
        cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
        for it in self.items:
            k = it["k"]
            if k == "strip":
                n = len(RAINBOW)
                for i, col in enumerate(RAINBOW):
                    cells.append(f'<mxCell id="{it["cid"]}s{i}" value="" style="rounded=0;fillColor={col};strokeColor=none;" vertex="1" parent="1"><mxGeometry x="{self.w * i / n:.0f}" y="0" width="{self.w / n + 1:.0f}" height="8" as="geometry"/></mxCell>')
            elif k == "rect":
                cells.append(self._dio_rect(it))
            elif k == "group":
                st, so = it["st"], it["solid"]
                s = (f'swimlane;startSize={it["hh"]};horizontal=1;rounded=1;arcSize=12;html=1;collapsible=0;fillColor={so["fill"]};gradientColor={so["grad"]};'
                     f'swimlaneFillColor={st["fill"]};strokeColor={st["stroke"]};strokeWidth=2.5;fontColor=#FFFFFF;fontStyle=1;fontSize=17;align=left;spacingLeft=14;fontFamily=Helvetica;')
                cells.append(f'<mxCell id="{it["cid"]}" value="{esc(it["title"])}" style="{s}" vertex="1" parent="1"><mxGeometry x="{it["x"]}" y="{it["y"]}" width="{it["w"]}" height="{it["h"]}" as="geometry"/></mxCell>')
                if it["tag"]:
                    cells.append(f'<mxCell id="{it["cid"]}t" value="{esc(it["tag"])}" style="text;html=1;align=right;verticalAlign=middle;fontColor=#FFFFFF;fontFamily=Courier New;fontSize=13;" vertex="1" parent="1"><mxGeometry x="{it["x"] + it["w"] - 300}" y="{it["y"]}" width="282" height="{it["hh"]}" as="geometry"/></mxCell>')
            elif k == "text":
                cells.append(self._dio_text(it))
            elif k == "poly":
                xs, ys = [p[0] for p in it["pts"]], [p[1] for p in it["pts"]]
                cells.append(f'<mxCell id="{it["cid"]}" value="" style="triangle;fillColor=#FFFFFF;strokeColor=#FFFFFF;rotation=0;" vertex="1" parent="1"><mxGeometry x="{min(xs):.0f}" y="{min(ys):.0f}" width="{max(max(xs) - min(xs), 6):.0f}" height="{max(max(ys) - min(ys), 6):.0f}" as="geometry"/></mxCell>')
            elif k == "edge":
                cells.append(self._dio_edge(it))
        body = "\n        ".join(cells)
        return (f'<mxfile host="app.diagrams.net" agent="network-lab-pkt generator">\n  <diagram id="d1" name="{esc(self.title)}">\n'
                f'    <mxGraphModel dx="{self.w}" dy="{self.h}" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
                f'pageWidth="{self.w}" pageHeight="{self.h}" background="{self.bg}" math="0" shadow="0">\n      <root>\n        {body}\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n')

    def _dio_label(self, pl, tcolor, base):
        parts = []
        for t, kind, col in pl:
            fs, fw, mono, lh = KINDS[kind]
            c = col or (mix(tcolor, base, .30) if kind == "s" else tcolor)
            ff = "Courier New" if mono else "Helvetica"
            sp = "letter-spacing:1.2px;" if kind == "k" else ""
            parts.append(f'<div style="font-size:{fs}px;line-height:{lh}px;font-weight:{fw};font-family:{ff};color:{c};{sp}">{html.escape(t, quote=False)}</div>')
        return esc("".join(parts))

    def _dio_rect(self, it):
        st, shape = it["st"], it["shape"]
        base = f'html=1;whiteSpace=wrap;overflow=hidden;strokeColor={st["stroke"]};strokeWidth={it["sw"]};fontColor={st["text"]};'
        if it["nofill"]:
            base += "fillColor=none;"
        else:
            base += f'fillColor={st["fill"]};gradientColor={st["grad"]};gradientDirection=south;' if st["fill"] != st["grad"] else f'fillColor={st["fill"]};'
        if shape in ("round", "pill", "rect"):
            base += f'rounded=1;absoluteArcSize=1;arcSize={min(it["rx"] * 2, min(it["w"], it["h"]))};'
        elif shape == "circle":
            base += "ellipse;"
        elif shape == "diamond":
            base += "rhombus;"
        elif shape == "cyl":
            base += "shape=cylinder3;boundedLbl=1;size=12;"
        elif shape == "cloud":
            base += "ellipse;shape=cloud;"
        if it["dash"]:
            base += "dashed=1;dashPattern=9 7;"
        if it["align"] == "l":
            base += f'align=left;spacingLeft={it["pad"]};'
        else:
            base += "align=center;"
        base += "verticalAlign=middle;spacing=0;"
        if it["opacity"] != 1:
            base += f'opacity={int(it["opacity"] * 100)};'
        val = self._dio_label(it["pl"], st["text"], st.get("base", st["fill"])) if it["pl"] else ""
        return f'<mxCell id="{it["cid"]}" value="{val}" style="{base}" vertex="1" parent="1"><mxGeometry x="{it["x"]:.1f}" y="{it["y"]:.1f}" width="{it["w"]:.1f}" height="{it["h"]:.1f}" as="geometry"/></mxCell>'

    def _dio_text(self, it):
        pl, anchor = it["pl"], it["anchor"]
        pl2 = []
        for t, kind, col in pl:
            pl2.append((t, kind, col or it["c"]))
        if it["big"]:
            val = esc(f'<div style="font-size:32px;line-height:40px;font-weight:700;font-family:Helvetica;color:{INK};">{html.escape(pl[0][0], quote=False)}</div>')
            H = 40
        elif it["sub"]:
            val = esc(f'<div style="font-size:17px;line-height:24px;font-family:Helvetica;color:{MUTED};">{html.escape(pl[0][0], quote=False)}</div>')
            H = 24
        else:
            val = self._dio_label(pl2, it["c"], "#FFFFFF")
            H = lines_h(pl)
        W = max(est_w(t, k) for t, k, _ in pl) + 24 if not (it["big"] or it["sub"]) else self.w - 300
        al = {"l": "left", "m": "center", "r": "right"}[anchor]
        x = {"l": it["x"], "m": it["x"] - W / 2, "r": it["x"] - W}[anchor]
        return (f'<mxCell id="{it["cid"]}" value="{val}" style="text;html=1;strokeColor=none;fillColor=none;align={al};verticalAlign=top;whiteSpace=nowrap;spacing=0;" vertex="1" parent="1">'
                f'<mxGeometry x="{x:.1f}" y="{it["y"]:.1f}" width="{W:.1f}" height="{H}" as="geometry"/></mxCell>')

    def _dio_edge(self, it):
        pts, col, w = it["pts"], it["color"], it["w"]
        s = f'html=1;strokeColor={col};strokeWidth={w};'
        if it["rounded"]:
            s += "rounded=1;"
        if len(pts) > 2:
            s += "edgeStyle=orthogonalEdgeStyle;curved=0;"
        if it["dash"] == "d":
            s += "dashed=1;dashPattern=10 7;"
        elif it["dash"] == "dot":
            s += "dashed=1;dashPattern=1 6;"
        s += "endArrow=block;endFill=1;" if it["arrow"] in ("end", "both") else "endArrow=none;"
        s += "startArrow=block;startFill=1;" if it["arrow"] in ("start", "both") else "startArrow=none;"

        def cons(side, pre):
            (sd, f) = side
            x, y = {"l": (0, f), "r": (1, f), "t": (f, 0), "b": (f, 1)}[sd]
            return f"{pre}X={x};{pre}Y={y};{pre}Dx=0;{pre}Dy=0;"

        attrs, geo = "", ""
        if it["src"] and it["tgt"]:
            s += cons(it["sa"], "exit") + cons(it["sb"], "entry")
            attrs = f' source="{it["src"]}" target="{it["tgt"]}"'
            if len(pts) > 2:
                geo = '<Array as="points">' + "".join(f'<mxPoint x="{px:.1f}" y="{py:.1f}"/>' for px, py in pts[1:-1]) + "</Array>"
        else:
            geo = f'<mxPoint x="{pts[0][0]:.1f}" y="{pts[0][1]:.1f}" as="sourcePoint"/><mxPoint x="{pts[-1][0]:.1f}" y="{pts[-1][1]:.1f}" as="targetPoint"/>'
            if len(pts) > 2:
                geo += '<Array as="points">' + "".join(f'<mxPoint x="{px:.1f}" y="{py:.1f}"/>' for px, py in pts[1:-1]) + "</Array>"
        return f'<mxCell id="{it["cid"]}" value="" style="{s}" edge="1" parent="1"{attrs}><mxGeometry relative="1" as="geometry">{geo}</mxGeometry></mxCell>'


def point_at(pts, f):
    segs = [(math.dist(pts[i], pts[i + 1]), pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    tot = sum(s[0] for s in segs)
    t = tot * f
    for L, a, b in segs:
        if t <= L or L == 0:
            r = t / L if L else 0
            return a[0] + (b[0] - a[0]) * r, a[1] + (b[1] - a[1]) * r
        t -= L
    return pts[-1]


def path_d(pts, r):
    if r == 0 or len(pts) < 3:
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(1, len(pts) - 1):
        p0, p1, p2 = pts[i - 1], pts[i], pts[i + 1]
        l1, l2 = math.dist(p0, p1), math.dist(p1, p2)
        rr = min(r, l1 / 2, l2 / 2)
        if rr < 1:
            d += f" L{p1[0]:.1f},{p1[1]:.1f}"
            continue
        a = (p1[0] + (p0[0] - p1[0]) * rr / l1, p1[1] + (p0[1] - p1[1]) * rr / l1)
        b = (p1[0] + (p2[0] - p1[0]) * rr / l2, p1[1] + (p2[1] - p1[1]) * rr / l2)
        d += f" L{a[0]:.1f},{a[1]:.1f} Q{p1[0]:.1f},{p1[1]:.1f} {b[0]:.1f},{b[1]:.1f}"
    d += f" L{pts[-1][0]:.1f},{pts[-1][1]:.1f}"
    return d


def cloud_ellipses(x, y, w, h):
    return [
        (x + w * .50, y + h * .62, w * .42, h * .32),
        (x + w * .28, y + h * .55, w * .22, h * .28),
        (x + w * .72, y + h * .55, w * .22, h * .28),
        (x + w * .38, y + h * .36, w * .20, h * .26),
        (x + w * .62, y + h * .34, w * .24, h * .30),
    ]
