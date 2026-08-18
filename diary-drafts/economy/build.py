#!/usr/bin/env python3
"""Build the Economy & Industry dev-diary PDF page.

Generates dev-diary.src.html (inline SVG charts, Gilded Federal theme) and
prints it to dev-diary.pdf with headless Chromium. All series are seeded so
the output is reproducible. Magnitudes follow the engine numbers already
published on poligeo.org (Hormuz: oil x1.38, CPI +0.8, approval -6;
China sanctions: CPI +2.0, S&P x0.878, approval -4).
"""

import base64
import math
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.environ.get("MARCELLUS_WOFF2", os.path.join(HERE, "marcellus-latin.woff2"))

# ── theme ────────────────────────────────────────────────────────────────────
BG = "#0a0e1a"
PANEL = "#131a2e"
PANEL2 = "#1b2440"
BORDER = "#2b3358"
GILT = "rgba(201,169,97,0.28)"
TEXT = "#eae4d2"
MUTED = "#98937f"
GRID = "#232c4a"
BASELINE = "#3d4674"
BLUE = "#4f8fd9"
BLUE2 = "#74aae6"
RED = "#e05a6d"
GREEN = "#57b57f"
GOLD = "#c9a961"
GOLD_HI = "#e8cf8e"
GOLD_DK = "#8a6d35"

SANS = "-apple-system,'Segoe UI','DejaVu Sans',system-ui,sans-serif"

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL"]


def nice_ticks(lo, hi, n=4):
    span = hi - lo
    raw = span / max(n - 1, 1)
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag:
            step = m * mag
            break
    t0 = math.floor(lo / step) * step
    ticks = []
    t = t0
    while t <= hi + step * 0.001:
        if t >= lo - step * 0.001:
            ticks.append(round(t, 10))
        t += step
    return ticks


def fmt_tick(v, fmt):
    if fmt == "$":
        return f"${v:,.0f}"
    if fmt == "$2":
        return f"${v:,.2f}"
    if fmt == "%":
        return f"{v:g}%"
    if fmt == "int":
        return f"{v:,.0f}"
    return f"{v:g}"


def event_line(x, y0, y1, label, anchor="middle"):
    """Dotted gold vertical marking the enactment date."""
    s = (f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y1}" stroke="{GOLD}" '
         f'stroke-width="1.2" stroke-dasharray="2 4" stroke-linecap="round" opacity="0.9"/>')
    tx, ta = x, anchor
    s += (f'<text x="{tx:.1f}" y="{y0 - 4}" fill="{GOLD}" font-size="7.5" letter-spacing="1.4" '
          f'text-anchor="{ta}" font-family="{SANS}">{label}</text>')
    return s


def frame(w, h, ml, mr, mt, mb):
    return ml, w - mr, mt, h - mb  # x0, x1, y0, y1


def x_month_labels(x0, x1, y, months=MONTHS):
    out = []
    n = len(months) - 1
    for i, m in enumerate(months):
        x = x0 + (x1 - x0) * i / n
        a = "start" if i == 0 else ("end" if i == n else "middle")
        out.append(f'<text x="{x:.1f}" y="{y}" fill="{MUTED}" font-size="8" '
                   f'text-anchor="{a}" font-family="{SANS}" letter-spacing="0.5">{m}</text>')
    return "".join(out)


def line_chart(w, h, pts, *, fmt="", event_t=None, event_label="", color=GOLD,
               end_label=None, end_dy=-8, ylo=None, yhi=None, wash=True,
               markers=False, months=MONTHS):
    """Single-series line chart. pts = [(t 0..1, value)]."""
    x0, x1, y0, y1 = frame(w, h, 40, 10, 16, 16)
    vs = [v for _, v in pts]
    lo = min(vs) if ylo is None else ylo
    hi = max(vs) if yhi is None else yhi
    pad = (hi - lo) * 0.12 or 1
    lo, hi = (lo - pad if ylo is None else lo), (hi + pad if yhi is None else hi)
    ticks = nice_ticks(lo, hi, 4)
    lo = min(lo, ticks[0]); hi = max(hi, ticks[-1])

    def X(t): return x0 + (x1 - x0) * t
    def Y(v): return y1 - (y1 - y0) * (v - lo) / (hi - lo)

    s = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">']
    for tv in ticks:
        y = Y(tv)
        s.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        s.append(f'<text x="{x0 - 5}" y="{y + 2.5:.1f}" fill="{MUTED}" font-size="8" text-anchor="end" '
                 f'font-family="{SANS}" style="font-variant-numeric:tabular-nums">{fmt_tick(tv, fmt)}</text>')
    s.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{BASELINE}" stroke-width="1"/>')

    path = " ".join(f'{"M" if i == 0 else "L"}{X(t):.1f} {Y(v):.1f}' for i, (t, v) in enumerate(pts))
    if wash:
        s.append(f'<path d="{path} L{X(pts[-1][0]):.1f} {y1} L{X(pts[0][0]):.1f} {y1} Z" '
                 f'fill="{color}" opacity="0.10" stroke="none"/>')
    if event_t is not None:
        s.append(event_line(X(event_t), y0, y1, event_label,
                            anchor="start" if event_t < 0.25 else "middle"))
    s.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2" '
             f'stroke-linejoin="round" stroke-linecap="round"/>')
    if markers:
        for t, v in pts:
            s.append(f'<circle cx="{X(t):.1f}" cy="{Y(v):.1f}" r="4" fill="{color}" '
                     f'stroke="{PANEL}" stroke-width="2"/>')
    ex, ey = X(pts[-1][0]), Y(pts[-1][1])
    s.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="{color}" stroke="{PANEL}" stroke-width="2"/>')
    if end_label:
        s.append(f'<text x="{ex - 7:.1f}" y="{ey + end_dy:.1f}" fill="{TEXT}" font-size="9" font-weight="600" '
                 f'text-anchor="end" font-family="{SANS}">{end_label}</text>')
    s.append(x_month_labels(x0, x1, h - 4, months))
    s.append("</svg>")
    return "".join(s)


def multi_line_chart(w, h, series, *, fmt="%", event_t=None, event_label="", months=MONTHS):
    """series = [{name, color, pts, end_label}]. One shared axis."""
    x0, x1, y0, y1 = frame(w, h, 40, 12, 16, 16)
    vs = [v for srs in series for _, v in srs["pts"]]
    lo, hi = min(vs), max(vs)
    pad = (hi - lo) * 0.15 or 1
    lo -= pad; hi += pad
    ticks = nice_ticks(lo, hi, 4)
    lo = min(lo, ticks[0]); hi = max(hi, ticks[-1])

    def X(t): return x0 + (x1 - x0) * t
    def Y(v): return y1 - (y1 - y0) * (v - lo) / (hi - lo)

    s = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">']
    for tv in ticks:
        y = Y(tv)
        s.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        s.append(f'<text x="{x0 - 5}" y="{y + 2.5:.1f}" fill="{MUTED}" font-size="8" text-anchor="end" '
                 f'font-family="{SANS}" style="font-variant-numeric:tabular-nums">{fmt_tick(tv, fmt)}</text>')
    s.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{BASELINE}" stroke-width="1"/>')
    if lo < 0 < hi:
        s.append(f'<line x1="{x0}" y1="{Y(0):.1f}" x2="{x1}" y2="{Y(0):.1f}" '
                 f'stroke="{BASELINE}" stroke-width="1"/>')
    if event_t is not None:
        s.append(event_line(X(event_t), y0, y1, event_label,
                            anchor="start" if event_t < 0.25 else "middle"))
    for srs in series:
        path = " ".join(f'{"M" if i == 0 else "L"}{X(t):.1f} {Y(v):.1f}'
                        for i, (t, v) in enumerate(srs["pts"]))
        s.append(f'<path d="{path}" fill="none" stroke="{srs["color"]}" stroke-width="2" '
                 f'stroke-linejoin="round" stroke-linecap="round"/>')
        ex, ey = X(srs["pts"][-1][0]), Y(srs["pts"][-1][1])
        s.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="{srs["color"]}" '
                 f'stroke="{PANEL}" stroke-width="2"/>')
        s.append(f'<text x="{ex - 2:.1f}" y="{ey - 8:.1f}" fill="{TEXT}" font-size="9" font-weight="600" '
                 f'text-anchor="end" font-family="{SANS}">{srs["end_label"]}</text>')
    s.append(x_month_labels(x0, x1, h - 4, months))
    s.append("</svg>")
    return "".join(s)


def candle_chart(w, h, ohlc, *, fmt="int", event_i=None, event_label="",
                 xlabels=None, note=None, ml=46):
    """Candlesticks: up = hollow green, down = filled red (direction never
    rides on hue alone). ohlc = [(o,h,l,c)], xlabels = [(index, text)]."""
    x0, x1, y0, y1 = frame(w, h, ml, 12, 16, 16)
    n = len(ohlc)
    slot = (x1 - x0) / n
    bw = max(3.0, min(11.0, slot - 2))  # >=2px surface gap between bodies
    los = min(r[2] for r in ohlc); his = max(r[1] for r in ohlc)
    pad = (his - los) * 0.10
    lo, hi = los - pad, his + pad
    ticks = nice_ticks(lo, hi, 5)
    lo = min(lo, ticks[0]); hi = max(hi, ticks[-1])

    def X(i): return x0 + slot * (i + 0.5)
    def Y(v): return y1 - (y1 - y0) * (v - lo) / (hi - lo)

    s = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">']
    for tv in ticks:
        y = Y(tv)
        s.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        s.append(f'<text x="{x0 - 5}" y="{y + 2.5:.1f}" fill="{MUTED}" font-size="8" text-anchor="end" '
                 f'font-family="{SANS}" style="font-variant-numeric:tabular-nums">{fmt_tick(tv, fmt)}</text>')
    s.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{BASELINE}" stroke-width="1"/>')
    if event_i is not None:
        s.append(event_line(x0 + slot * event_i, y0, y1, event_label,
                            anchor="start" if event_i / n < 0.3 else "middle"))
    for i, (o, hh, ll, c) in enumerate(ohlc):
        x = X(i)
        up = c >= o
        col = GREEN if up else RED
        s.append(f'<line x1="{x:.1f}" y1="{Y(hh):.1f}" x2="{x:.1f}" y2="{Y(ll):.1f}" '
                 f'stroke="{col}" stroke-width="1"/>')
        top, bot = Y(max(o, c)), Y(min(o, c))
        bh = max(bot - top, 1.5)
        if up:  # hollow body
            s.append(f'<rect x="{x - bw/2:.1f}" y="{top:.1f}" width="{bw:.1f}" height="{bh:.1f}" '
                     f'fill="{PANEL}" stroke="{col}" stroke-width="1.4" rx="1"/>')
        else:   # filled body
            s.append(f'<rect x="{x - bw/2:.1f}" y="{top:.1f}" width="{bw:.1f}" height="{bh:.1f}" '
                     f'fill="{col}" stroke="none" rx="1"/>')
    if xlabels:
        for i, txt in xlabels:
            a = "start" if i == 0 else ("end" if i >= n - 1 else "middle")
            s.append(f'<text x="{X(i):.1f}" y="{h - 4}" fill="{MUTED}" font-size="8" '
                     f'text-anchor="{a}" font-family="{SANS}" letter-spacing="0.5">{txt}</text>')
    if note:
        s.append(f'<text x="{x1 - 2}" y="{y0 + 8}" fill="{TEXT}" font-size="9.5" font-weight="600" '
                 f'text-anchor="end" font-family="{SANS}">{note}</text>')
    s.append("</svg>")
    return "".join(s)


def donut(w, h, slices, *, cx=None, cy=None, R=None, r_in=None,
          center_top="", center_bot="", palette=None):
    """Part-to-whole ring, 2px surface gaps, every slice direct-labeled with a
    leader line (identity never rides on color-matching)."""
    cx = cx or w / 2
    cy = cy or h / 2
    R = R or min(w, h) / 2 - 64
    r_in = r_in or R * 0.60
    palette = palette or [GOLD_HI, BLUE, GOLD, BLUE2, GOLD_DK, "#3d6ea8", "#b5885a", "#5c7fb8", MUTED]
    total = sum(v for _, v in slices)
    s = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">']
    a = -90.0  # start at 12 o'clock, clockwise
    labels = []
    for i, (name, v) in enumerate(slices):
        frac = v / total
        a2 = a + 360 * frac
        large = 1 if (a2 - a) > 180 else 0
        rad1, rad2 = math.radians(a), math.radians(a2)
        p = (f'M{cx + R*math.cos(rad1):.2f} {cy + R*math.sin(rad1):.2f} '
             f'A{R} {R} 0 {large} 1 {cx + R*math.cos(rad2):.2f} {cy + R*math.sin(rad2):.2f} '
             f'L{cx + r_in*math.cos(rad2):.2f} {cy + r_in*math.sin(rad2):.2f} '
             f'A{r_in} {r_in} 0 {large} 0 {cx + r_in*math.cos(rad1):.2f} {cy + r_in*math.sin(rad1):.2f} Z')
        s.append(f'<path d="{p}" fill="{palette[i % len(palette)]}" stroke="{PANEL}" stroke-width="2"/>')
        mid = math.radians((a + a2) / 2)
        labels.append({"mid": mid, "name": name, "pct": 100 * frac,
                       "color": palette[i % len(palette)]})
        a = a2
    # leader-line labels, collision-resolved per side
    for side in (1, -1):  # 1 = right, -1 = left
        col = [L for L in labels if (math.cos(L["mid"]) >= 0) == (side == 1)]
        col.sort(key=lambda L: cy + (R + 14) * math.sin(L["mid"]))
        ys = [cy + (R + 14) * math.sin(L["mid"]) for L in col]
        for i in range(1, len(ys)):  # push down
            ys[i] = max(ys[i], ys[i - 1] + 15)
        for i in range(len(ys) - 2, -1, -1):  # push back up if we ran past
            ys[i] = min(ys[i], ys[i + 1] - 15)
        for L, y in zip(col, ys):
            ax = cx + R * math.cos(L["mid"]); ay = cy + R * math.sin(L["mid"])
            bx = cx + (R + 10) * math.cos(L["mid"])
            ex = cx + (R + 22) * side
            s.append(f'<path d="M{ax:.1f} {ay:.1f} L{bx:.1f} {y:.1f} L{ex:.1f} {y:.1f}" fill="none" '
                     f'stroke="{BASELINE}" stroke-width="1"/>')
            anchor = "start" if side == 1 else "end"
            tx = ex + 4 * side
            s.append(f'<text x="{tx:.1f}" y="{y - 1:.1f}" fill="{TEXT}" font-size="8.5" '
                     f'text-anchor="{anchor}" font-family="{SANS}">{L["name"]}</text>')
            s.append(f'<text x="{tx:.1f}" y="{y + 8.5:.1f}" fill="{MUTED}" font-size="8" '
                     f'text-anchor="{anchor}" font-family="{SANS}" '
                     f'style="font-variant-numeric:tabular-nums">{L["pct"]:.1f}%</text>')
    if center_top:
        s.append(f'<text x="{cx}" y="{cy - 2}" fill="{TEXT}" font-size="17" font-weight="600" '
                 f'text-anchor="middle" font-family="{SANS}">{center_top}</text>')
    if center_bot:
        s.append(f'<text x="{cx}" y="{cy + 13}" fill="{MUTED}" font-size="7.5" letter-spacing="1.2" '
                 f'text-anchor="middle" font-family="{SANS}">{center_bot}</text>')
    s.append("</svg>")
    return "".join(s)


# ── data (seeded engine-style runs) ─────────────────────────────────────────

def walk_series(rng, n, start, drift, sigma):
    v, out = start, [start]
    for _ in range(n - 1):
        v = v * (1 + drift + rng.gauss(0, sigma))
        out.append(v)
    return out


def hormuz_data():
    rng = random.Random(19)
    days = 183; ev = 30
    # Brent: 83.81 -> spike x1.38 over ~12 days, settle ~x1.29
    brent = []
    v = 83.81
    for d in range(days):
        if d < ev:
            v = 83.81 * (1 + rng.gauss(0, 0.004))
        else:
            k = d - ev
            target = 83.81 * (1.38 - 0.09 * min(1, max(0, (k - 25) / 130)))
            ramp = 1 - math.exp(-k / 5.0)
            base = 83.81 + (target - 83.81) * ramp
            v = base * (1 + rng.gauss(0, 0.008))
        brent.append(v)
    # pump: sticky retail pass-through — fast bursts, plateaus, a late easing
    # ("rockets up, feathers down"), not a smooth curve
    prng = random.Random(23)
    rise_days = range(ev + 5, ev + 75)
    incs = {}
    for d in rise_days:
        r = prng.random()
        if r < 0.42:
            incs[d] = prng.uniform(0.6, 3.8)   # station repricing burst (cents)
        elif r < 0.55:
            incs[d] = prng.uniform(0.1, 0.5)
        else:
            incs[d] = 0.0                       # plateau day
    scale = 0.965 / (sum(incs.values()) / 100)  # net climb $3.11 -> ~$4.075
    pump, v = [], 3.11
    for d in range(days):
        if d < ev + 5:
            v += prng.gauss(0, 0.004)
        elif d in incs:
            v += incs[d] * scale / 100 + prng.gauss(0, 0.004)
        else:
            v += prng.gauss(-0.0016, 0.005)     # slow feathering after the peak
        v = max(v, 3.05)
        pump.append(v)
    cpi = [2.8, 2.8, 3.1, 3.4, 3.6, 3.6, 3.5]  # monthly prints, +0.8 peak
    appr = []
    v = 51.0
    for wk in range(27):
        d = wk * 7
        if d < ev:
            v = 51 + rng.gauss(0, 0.35)
        else:
            k = d - ev
            base = 51 - 6.3 * (1 - math.exp(-k / 20.0)) + 0.5 * min(1, max(0, (k - 90) / 60))
            v = base + rng.gauss(0, 0.4)
        appr.append(v)
    T = days - 1
    return {
        "brent": [(d / T, x) for d, x in enumerate(brent)],
        "pump": [(d / T, x) for d, x in enumerate(pump)],
        "cpi": [(i / 6, x) for i, x in enumerate(cpi)],
        "appr": [(min(1, wk * 7 / T), x) for wk, x in enumerate(appr)],
        "event_t": ev / T,
    }


def china_data():
    rng = random.Random(47)
    ev_w = 4.35  # sanctions land one month in
    us = [2.3, 2.3, 0.4, -0.4, -0.8, -1.0, -1.0]
    cn = [4.8, 4.8, 1.0, -0.6, -1.5, -1.9, -2.0]
    # S&P weekly candles, 26 weeks, 5996 -> x0.878
    closes, v = [], 5996.0
    for wk in range(26):
        if wk <= 4:
            r = 0.002 + rng.gauss(0, 0.004)
        elif wk <= 8:
            r = [-0.042, -0.035, -0.024, -0.013][wk - 5] + rng.gauss(0, 0.004)
        elif wk <= 12:
            r = [0.016, 0.009, -0.006, 0.008][wk - 9] + rng.gauss(0, 0.005)
        else:
            r = rng.gauss(-0.0012, 0.007)
        v *= (1 + r)
        closes.append(v)
    closes[-1] = 5996 * 0.878  # settle on the engine's published multiplier
    ohlc, prev = [], 5996.0
    for c in closes:
        o = prev * (1 + rng.gauss(0, 0.002))
        hi = max(o, c) * (1 + abs(rng.gauss(0, 0.004)))
        lo = min(o, c) * (1 - abs(rng.gauss(0, 0.004)))
        ohlc.append((o, hi, lo, c))
        prev = c
    return {"us": us, "cn": cn, "spx": ohlc, "ev_w": ev_w}


def company_data():
    rng = random.Random(7)
    cos = [
        ("Vantage Systems", "TECH", "$1.94T", "$212.4B", 214.0, 0.0032, 0.011),
        ("First Continental", "FINANCE", "$602B", "$171.8B", 187.0, -0.0014, 0.008),
        ("Meridian Health", "HEALTHCARE", "$418B", "$96.2B", 128.0, 0.0004, 0.007),
        ("Crestline Group", "SERVICES", "$187B", "$64.5B", 54.0, 0.0011, 0.010),
    ]
    out = []
    for name, tick, cap, rev, p0, drift, sig in cos:
        closes = walk_series(rng, 22, p0, drift, sig)
        ohlc, prev = [], closes[0]
        for c in closes[1:]:
            o = prev * (1 + rng.gauss(0, 0.0015))
            hi = max(o, c) * (1 + abs(rng.gauss(0, 0.003)))
            lo = min(o, c) * (1 - abs(rng.gauss(0, 0.003)))
            ohlc.append((o, hi, lo, c))
            prev = c
        out.append({"name": name, "tick": tick, "cap": cap, "rev": rev,
                    "ohlc": ohlc, "last": ohlc[-1][3],
                    "chg": (ohlc[-1][3] / p0 - 1) * 100})
    return out


INDUSTRY = [
    ("Finance & real estate", 20.7),
    ("Professional services", 13.0),
    ("Wholesale & retail", 11.7),
    ("Government", 11.3),
    ("Manufacturing", 10.2),
    ("Education & health", 8.8),
    ("Information", 5.6),
    ("Construction", 4.5),
    ("Other industries", 14.2),
]

BUDGET = [
    ("Social Security", 1452),
    ("Net interest", 882),
    ("Medicare", 874),
    ("National defense", 874),
    ("Income security", 671),
    ("Medicaid", 618),
    ("Veterans", 325),
    ("All other", 1055),
]

BRIEFING = [
    ("Growth", "Real GDP expanded <b>2.8%</b> in 2024; the engine's 2025 baseline tracks <b>+2.1%</b>, cooling but above trend."),
    ("Prices", "CPI at <b>2.9%</b>, core at 3.2%. Disinflation has stalled above the Federal Reserve's 2% target."),
    ("Labor", "Unemployment <b>4.1%</b>; payrolls +256k in December; wage growth 3.9% and outpacing prices."),
    ("Rates", "Fed funds held at <b>4.25&ndash;4.50%</b>; markets price two cuts this year. 10-year Treasury at 4.61%."),
    ("Markets", "S&amp;P 500 at <b>5,996</b>. Dollar index 109 &mdash; the strongest in two years, squeezing exporters."),
    ("Energy", "Brent <b>$83.81</b>, WTI $77; retail gasoline $3.11/gal. Inventories thin; Gulf transit risk is the swing factor."),
    ("Fiscal", "Debt <b>$36.2T</b>; FY24 deficit $1.83T (6.4% of GDP). Net interest now exceeds the defense budget."),
    ("Risks", "Growing interest payments threaten a debt spiral if the budget is not constrained. Voters demand greater wage growth and lower inflation. Geopolitical threats from Russia and Iran could imperil energy prices if not carefully managed."),
]

DIARY = [
    "Every one of PoliGeo's 199 nations runs its own economy, and none of them pauses for you. One deterministic engine ticks forward in real time: output, prices, currencies, markets and jobs are recomputed continuously, whether you are watching or not.",
    "There is no economy tab bolted onto the side. The economy is the transmission system of the whole game. Close the Strait of Hormuz and Brent spikes; oil feeds the inflation print; the print reaches the central bank, the markets, and eventually the voters. Sanction Beijing and trade reroutes, growth bleeds on both sides of the Pacific, and the S&amp;P answers within the week. Every shock propagates through the same chain of consequence &mdash; <b>a war moves oil, oil moves the economy, and the electorate answers at the next election</b>, if you allow one.",
    "Industry is where that economy becomes power. Each nation's productive base &mdash; energy, resources, manufacturing &mdash; determines what it can actually sustain: the materiel a war burns through, the exports a rival can embargo, the leverage a tariff really carries. A blockade is not a status effect; it is missing inputs working through somebody's supply chain.",
    "You hold the real levers: the budget, taxes, tariffs, sanctions, subsidies, the pressure you put on the central bank. The engine weighs every plausible outcome and hands you the bill. Cut rates and the market cheers today; the inflation print answers in six months.",
    "<b>Nothing is scripted. No two economies collapse the same way.</b>",
]


def build_html():
    with open(FONT_PATH, "rb") as f:
        font_b64 = base64.b64encode(f.read()).decode()

    hz = hormuz_data()
    ch = china_data()
    cos = company_data()

    hormuz_charts = "".join(
        f'<div class="mini"><div class="mini-t">{title}</div>{svg}</div>'
        for title, svg in [
            ("Brent crude &middot; $/bbl",
             line_chart(218, 148, hz["brent"], fmt="$", event_t=hz["event_t"],
                        event_label="STRAIT CLOSED", color=GOLD,
                        end_label=f'${hz["brent"][-1][1]:.0f}')),
            ("Gasoline at the pump &middot; $/gal",
             line_chart(218, 148, hz["pump"], fmt="$2", event_t=hz["event_t"],
                        event_label="STRAIT CLOSED", color=GOLD,
                        end_label=f'${hz["pump"][-1][1]:.2f}')),
            ("Inflation &middot; CPI, year over year",
             line_chart(218, 148, hz["cpi"], fmt="%", event_t=hz["event_t"],
                        event_label="STRAIT CLOSED", color=BLUE, markers=True,
                        end_label=f'{hz["cpi"][-1][1]:.1f}%', end_dy=16)),
            ("Presidential approval",
             line_chart(218, 148, hz["appr"], fmt="%", event_t=hz["event_t"],
                        event_label="STRAIT CLOSED", color=BLUE,
                        end_label=f'{hz["appr"][-1][1]:.0f}%')),
        ])

    n_us, n_cn = len(ch["us"]) - 1, len(ch["cn"]) - 1
    gdp_chart = multi_line_chart(
        370, 208,
        [{"name": "United States", "color": BLUE, "end_label": f'US {ch["us"][-1]:.1f}%',
          "pts": [(i / n_us, v) for i, v in enumerate(ch["us"])]},
         {"name": "China", "color": GOLD, "end_label": f'CN {ch["cn"][-1]:.1f}%',
          "pts": [(i / n_cn, v) for i, v in enumerate(ch["cn"])]}],
        fmt="%", event_t=1 / 6, event_label="TIER 4 ENACTED")

    spx_chart = candle_chart(
        544, 208, ch["spx"], fmt="int", event_i=ch["ev_w"], event_label="TIER 4 ENACTED",
        xlabels=[(0, "JAN"), (4, "FEB"), (9, "MAR"), (13, "APR"), (17, "MAY"), (22, "JUN"), (25, "JUL")],
        note=f'{(ch["spx"][-1][3] / 5996 - 1) * 100:+.1f}%')

    co_cards = []
    for c in cos:
        chart = candle_chart(200, 118, c["ohlc"], fmt="$", event_i=None, ml=38,
                             xlabels=[(0, "DEC 20"), (20, "JAN 20")])
        chg_col = GREEN if c["chg"] >= 0 else RED
        co_cards.append(f'''
      <div class="co">
        <div class="co-head">
          <span class="co-name">{c["name"]}</span>
          <span class="co-chg" style="color:{chg_col}">{c["chg"]:+.1f}%<span class="co-chg-k">1 MO</span></span>
        </div>
        <div class="co-sec">{c["tick"]}</div>
        {chart}
        <div class="co-stats">
          <span><i>Market cap</i><b>{c["cap"]}</b></span>
          <span><i>Revenue, TTM</i><b>{c["rev"]}</b></span>
          <span><i>Last</i><b>${c["last"]:.2f}</b></span>
        </div>
      </div>''')

    wheel = donut(452, 330, INDUSTRY, center_top="$29.2T", center_bot="US GDP &middot; 2025",
                  R=90, r_in=56)
    budget_total = sum(v for _, v in BUDGET)
    budget_pie = donut(452, 312, [(n, v) for n, v in BUDGET],
                       center_top=f"${budget_total/1000:.2f}T", center_bot="FY24 OUTLAYS",
                       R=86, r_in=53)

    briefing_rows = "".join(
        f'<div class="br-row"><span class="br-k">{k}</span><span class="br-v">{v}</span></div>'
        for k, v in BRIEFING)

    html = f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>Economy &amp; Industry &mdash; PoliGeo Dev Diary</title>
<style>
@font-face {{
  font-family:'Marcellus'; font-style:normal; font-weight:400;
  src:url(data:font/woff2;base64,{font_b64}) format('woff2');
}}
:root {{
  --bg:{BG}; --panel:{PANEL}; --panel-2:{PANEL2}; --border:{BORDER};
  --border-gilt:{GILT}; --text:{TEXT}; --muted:{MUTED}; --grid-ln:{GRID};
  --baseline:{BASELINE}; --accent:{BLUE}; --bad:{RED}; --gold:{GOLD};
  --gold-hi:{GOLD_HI}; --gold-dk:{GOLD_DK};
  --display:'Marcellus','Palatino Linotype',Palatino,'Times New Roman',serif;
}}
* {{ box-sizing:border-box; }}
html,body {{ margin:0; padding:0; }}
body {{
  width:1060px; background:var(--bg); color:var(--text);
  font:12.5px/1.5 {SANS};
  background-image:radial-gradient(120% 40% at 50% 0%, rgba(224,90,109,0.05), transparent 60%);
  print-color-adjust:exact; -webkit-print-color-adjust:exact;
}}
.wrap {{ width:1000px; margin:0 auto; padding:34px 0 26px; }}

.eyebrow {{ font-family:var(--display); text-transform:uppercase; letter-spacing:2.6px;
  font-size:10px; color:var(--gold); text-align:center; margin:0 0 7px; }}
h1 {{ font-family:var(--display); text-transform:uppercase; letter-spacing:2px;
  font-weight:400; text-align:center; font-size:34px; line-height:1.15; margin:0 0 10px;
  color:#d9b76d; }} /* solid gold: gradient text-clip strokes a hairline box in print */
.orn {{ display:flex; align-items:center; gap:8px; margin:2px auto 18px; max-width:620px; }}
.orn::before,.orn::after {{ content:""; flex:1; height:1px;
  background:linear-gradient(90deg,transparent,var(--border-gilt)); }}
.orn::after {{ background:linear-gradient(90deg,var(--border-gilt),transparent); }}
.orn svg {{ flex:none; }}

.chips {{ display:grid; grid-template-columns:repeat(3,1fr); gap:8px; max-width:620px; margin:0 auto 20px; }}
.chip {{ text-align:center; padding:9px 2px 8px; border:1px solid var(--border); border-radius:8px;
  background:var(--panel-2); }}
.chip b {{ display:block; font-family:var(--display); font-size:19px; letter-spacing:0.5px;
  color:var(--gold-hi); font-weight:400; }}
.chip span {{ font-size:9px; letter-spacing:1.6px; text-transform:uppercase; color:var(--muted); }}

.diary {{ border-left:2px solid var(--border-gilt); padding:4px 0 4px 16px; margin:0 auto 24px;
  max-width:760px; color:#c9c3b0; }}
.diary .dateline {{ font-family:var(--display); text-transform:uppercase; letter-spacing:1.8px;
  font-size:9.5px; color:var(--gold); display:block; margin-bottom:6px; }}
.diary p {{ margin:0 0 9px; }}
.diary p:last-child {{ margin-bottom:0; }}
.diary b {{ color:var(--text); font-weight:600; }}

.grid {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; }}
.panel {{ background:var(--panel); border:1px solid var(--border); border-radius:12px;
  padding:16px 18px 14px; margin-bottom:14px; break-inside:avoid;
  box-shadow:inset 0 1px 0 rgba(201,169,97,0.07); }}
.panel.full {{ grid-column:1 / -1; }}
.kick {{ font-family:var(--display); text-transform:uppercase; letter-spacing:2px;
  font-size:10.5px; color:var(--gold); margin-bottom:5px; display:flex; align-items:baseline; gap:9px; }}
.kick .n {{ color:var(--gold-dk); font-size:12px; }}
.p-title {{ font-family:var(--display); font-size:17.5px; margin:0 0 3px; color:var(--text);
  letter-spacing:0.3px; }}
.p-sub {{ margin:0 0 11px; color:var(--muted); font-size:11.5px; line-height:1.45; }}
.p-sub b {{ color:var(--text); font-weight:600; }}

.row4 {{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; }}
.mini {{ background:var(--panel-2); border:1px solid var(--border); border-radius:9px; padding:9px 6px 4px; }}
.mini-t {{ font-size:9.5px; letter-spacing:1.2px; text-transform:uppercase; color:var(--muted);
  margin:0 0 4px 8px; }}
.duo {{ display:grid; grid-template-columns:388px 1fr; gap:10px; }}
.duo .mini {{ padding:9px 8px 4px; }}

.legend {{ display:flex; gap:16px; margin:7px 0 0 8px; font-size:10px; color:var(--muted); }}
.legend .sw {{ display:inline-block; width:14px; height:3px; border-radius:2px; margin-right:5px;
  vertical-align:middle; }}
.legend .swc {{ display:inline-block; width:8px; height:8px; border-radius:2px; margin-right:5px;
  vertical-align:middle; }}

.facts {{ display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin-top:11px; }}
.fact {{ background:var(--panel-2); border:1px solid var(--border); border-radius:8px;
  padding:7px 10px 6px; }}
.fact .k {{ display:block; font-size:8.5px; letter-spacing:1.1px; text-transform:uppercase;
  color:var(--muted); margin-bottom:2px; }}
.fact .v {{ font-size:15px; font-weight:600; color:var(--gold-hi); }}
.fact .v.dn {{ color:var(--bad); }}

.cos {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; }}
.co {{ background:var(--panel-2); border:1px solid var(--border); border-radius:9px; padding:9px 10px 7px; }}
.co-head {{ display:flex; justify-content:space-between; align-items:baseline; }}
.co-name {{ font-family:var(--display); font-size:13.5px; letter-spacing:0.4px; white-space:nowrap; }}
.co-sec {{ font-size:8.5px; color:var(--muted); letter-spacing:1.5px; margin:0 0 4px; }}
.co-chg {{ font-size:11px; font-weight:600; white-space:nowrap; }}
.co-chg-k {{ font-size:8px; color:var(--muted); font-weight:400; letter-spacing:1px; margin-left:4px; }}
.co-stats {{ display:flex; gap:14px; margin:3px 0 0 4px; }}
.co-stats span i {{ display:block; font-style:normal; font-size:8px; letter-spacing:1px;
  text-transform:uppercase; color:var(--muted); }}
.co-stats span b {{ font-size:12px; font-weight:600; color:var(--text); }}

.br {{ margin-top:4px; }}
.br-head {{ border:1px solid var(--border-gilt); border-radius:9px; background:var(--panel-2);
  padding:10px 14px 9px; margin-bottom:10px; }}
.br-head .t1 {{ font-family:var(--display); letter-spacing:2.4px; font-size:11.5px;
  text-transform:uppercase; color:var(--gold-hi); }}
.br-head .t2 {{ font-size:9px; letter-spacing:1.6px; text-transform:uppercase; color:var(--muted);
  margin-top:2px; }}
.br-row {{ display:flex; gap:12px; padding:5.5px 2px; border-bottom:1px solid var(--grid-ln);
  align-items:baseline; }}
.br-row:last-child {{ border-bottom:none; }}
.br-k {{ flex:0 0 74px; font-family:var(--display); font-size:10px; letter-spacing:1.6px;
  text-transform:uppercase; color:var(--gold); }}
.br-v {{ font-size:11px; color:#c9c3b0; line-height:1.4; }}
.br-v b {{ color:var(--text); font-weight:600; }}

footer {{ margin-top:6px; font-size:10px; color:var(--muted); text-align:center; letter-spacing:0.4px; }}
footer .gold {{ color:var(--gold); }}
.note {{ font-size:8.5px; letter-spacing:1px; text-transform:uppercase; color:#807a66;
  text-align:center; margin-top:10px; }}
</style>
<body>
<div class="wrap">

<header>
  <p class="eyebrow">PoliGeo &middot; Dev Diary</p>
  <h1>Economy &amp; Industry</h1>
  <div class="orn" aria-hidden="true">
    <svg width="46" height="10" viewBox="0 0 46 10"><path d="M23 1 L27 5 L23 9 L19 5 Z" fill="none" stroke="{GOLD}" stroke-width="1"/><circle cx="8" cy="5" r="1.2" fill="{GOLD_DK}"/><circle cx="38" cy="5" r="1.2" fill="{GOLD_DK}"/></svg>
  </div>
</header>

<div class="grid">

<!-- I HORMUZ -->
<div class="panel full">
  <div class="kick"><span class="n">I</span>The Hormuz Shock</div>
  <p class="p-title">One closed strait, four instruments</p>
  <p class="p-sub">A live engine run: the Strait of Hormuz closes one month in, and the same shock is read
  off four different gauges. Crude reprices in days, the pump follows in weeks, the CPI print lands a month
  later, and approval pays for all of it. Dotted line marks the closure.</p>
  <div class="row4">{hormuz_charts}</div>
</div>

<!-- II CHINA -->
<div class="panel full">
  <div class="kick"><span class="n">II</span>Tier 4 on Beijing</div>
  <p class="p-title">Impose maximum sanctions on China and face the consequences</p>
  <p class="p-sub">Imposing full sanctions restricts trade with the recipient country. Democratic
  administrations must answer to their voters, while authoritarian countries have more tolerance
  for pain. Hollow candles close up, filled candles close down.</p>
  <div class="duo">
    <div class="mini"><div class="mini-t">Real GDP growth &middot; annualized</div>{gdp_chart}
      <div class="legend"><span><span class="sw" style="background:{BLUE}"></span>United States</span>
      <span><span class="sw" style="background:{GOLD}"></span>China</span></div>
    </div>
    <div class="mini"><div class="mini-t">S&amp;P 500 &middot; weekly</div>{spx_chart}
      <div class="legend"><span><span class="swc" style="background:{PANEL};border:1.4px solid {GREEN}"></span>Week up</span>
      <span><span class="swc" style="background:{RED}"></span>Week down</span></div>
    </div>
  </div>
  <div class="facts">
    <div class="fact"><span class="k">S&amp;P 500</span><span class="v dn">&minus;12.2%</span></div>
    <div class="fact"><span class="k">CPI, imported goods pass-through</span><span class="v">+2.0 pt</span></div>
    <div class="fact"><span class="k">Dollar index</span><span class="v dn">&minus;2.1</span></div>
    <div class="fact"><span class="k">Presidential approval</span><span class="v dn">&minus;4 pt</span></div>
  </div>
</div>

<!-- III INDUSTRY WHEEL -->
<div class="panel">
  <div class="kick"><span class="n">III</span>The Industrial Base</div>
  <p class="p-title">Sectors of the US Economy</p>
  <p class="p-sub">Every nation's GDP is composed of sectors, represented by real buildings on the map
  that can increase or decrease their levels.</p>
  {wheel}
</div>

<!-- IV CORPORATES -->
<div class="panel">
  <div class="kick"><span class="n">IV</span>The Corporates</div>
  <p class="p-title">The four largest firms, trading normally</p>
  <p class="p-sub">Listed companies are simulated tickers &mdash; one from each sector: tech, finance,
  healthcare and services. A calm month of daily candles, before you touch anything.</p>
  <div class="cos">{"".join(co_cards)}</div>
</div>

<!-- V BUDGET -->
<div class="panel">
  <div class="kick"><span class="n">V</span>The Budget</div>
  <p class="p-title">Federal Budget, FY 2024</p>
  <p class="p-sub">The budget the new US Administration inherits. Growing interest payments as a portion
  of the budget threaten long term financial stability.</p>
  {budget_pie}
</div>

<!-- VI BRIEFING -->
<div class="panel">
  <div class="kick"><span class="n">VI</span>The Briefing</div>
  <p class="p-title">Economic briefing &middot; January 20, 2025</p>
  <p class="p-sub">The macroeconomic situation facing the incoming administration. This is the start
  of the simulation.</p>
  <div class="br">
    <div class="br-head">
      <div class="t1">Memorandum for the President</div>
      <div class="t2">Council of Economic Advisers &middot; Inauguration Day brief &middot; 20 Jan 2025</div>
    </div>
    {briefing_rows}
  </div>
</div>

</div><!-- /grid -->

<footer>
  <span class="gold">poligeo.org</span>
</footer>

</div>
<script>
/* Size the single PDF page to the document. Measure only after webfonts have
   swapped in — Marcellus reflows the serif titles, so a load-time measurement
   under-counts and the print clips the bottom of the page. */
const st = document.createElement('style');
document.head.appendChild(st);
const fit = () => {{
  const h = Math.ceil(Math.max(document.documentElement.scrollHeight,
                               document.body.scrollHeight)) + 2;
  st.textContent = `@page {{ size: 1060px ${{h}}px; margin: 0; }}`;
}};
addEventListener('load', fit);
if (document.fonts && document.fonts.ready)
  document.fonts.ready.then(() => requestAnimationFrame(() => requestAnimationFrame(fit)));
</script>
</body>
</html>
"""
    out = os.path.join(HERE, "dev-diary.src.html")
    with open(out, "w") as f:
        f.write(html)
    return out


def print_pdf(html_path):
    chrome = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
    pdf = os.path.join(HERE, "dev-diary.pdf")
    subprocess.run([
        chrome, "--headless", "--no-sandbox", "--disable-gpu",
        "--force-device-scale-factor=1", "--hide-scrollbars",
        "--no-pdf-header-footer", "--virtual-time-budget=4000",
        f"--print-to-pdf={pdf}", f"file://{html_path}",
    ], check=True, capture_output=True)
    return pdf


if __name__ == "__main__":
    html = build_html()
    print("wrote", html)
    if "--html-only" not in sys.argv:
        print("wrote", print_pdf(html))
