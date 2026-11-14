from pathlib import Path

from dgm import Canvas, PAL, MUTED

ROOT = Path(__file__).resolve().parents[2]


def out(path):
    return str(ROOT / "docs" / path)


def steps(c, x, y, w, items, col="indigo", title="PACKET WALK", gap=10, h=64):
    c.text(x, y - 30, [(f"^{title}", PAL["indigo"][2])])
    for i, (t, d) in enumerate(items):
        yy = y + i * (h + gap)
        c.rect(x, yy, w, h, [f"!{t}", f"_{d}"], c=col, align="l", pad=60, shadow=False)
        c.badge(i + 1, x + 30, yy + h / 2, col)
    return y + len(items) * (h + gap)


def cmds(c, x, y, w, items, title="VERIFY IN PACKET TRACER"):
    c.text(x, y, [(f"^{title}", PAL["indigo"][2])])
    cx, cy = x, y + 30
    for t in items:
        tw = len(t) * 8.6 + 28
        if cx + tw > x + w:
            cx, cy = x, cy + 44
        c.rect(cx, cy, tw, 36, [(f"~{t}", "#E2E8F0")], c="gray", solid=True, shape="pill", shadow=False, pad=6, tcolor="#E2E8F0", fill="#1F2A44", stroke="#0B1220")
        cx += tw + 10
    return cy + 44


def kv_table(c, x, y, colw, rows, head="indigo", mono=(1, 2, 3), rowh=34):
    return c.table(x, y, colw, rows, rowh=rowh, head=head, mono_cols=mono)


def wrap(text, n):
    out_, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > n and cur:
            out_.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return out_ + [cur] if cur else out_
