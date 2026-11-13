"""Builds the animated GitHub profile banner (dark and light) for plat.plus.

Usage: python3 -I make.py <font.woff2> <outdir> [--still]
--still writes the end state without animation, for previews.
"""

import base64
import io
import sys

from fontTools import subset
from fontTools.ttLib import TTFont

font_path, out, *flags = sys.argv[1:]
still = "--still" in flags

W, H = 1280, 440

THEMES = {
    "dark": dict(
        bg="#0d1412", card="#141d1a", border="#22322c", fg="#fafafa",
        muted="#9aa8a2", primary="#5fd3a7", primary_fg="#04140e",
        soft="#1b2c26", glow="#0f7a58", bar="#22322c",
    ),
    "light": dict(
        bg="#fbfaf7", card="#ffffff", border="#e6e3da", fg="#0a0a0a",
        muted="#6b6a63", primary="#0f7a58", primary_fg="#ffffff",
        soft="#e9f6f0", glow="#76ffce", bar="#f2f1ec",
    ),
}

TEXTS = [
    "plat.plus",
    "Your course, all in one place.",
    "For everyone who teaches or learns",
    "Hosted in Germany",
    "Week 3 · Sources and methods",
    "Session · Thursday 10:00",
    "Reading list.pdf",
    "Notes · Group work",
    "Task · Exercise sheet 2",
    "18 of 24 handed in",
    "Feedback released",
    "What has been hardest so far?",
    "Reading", "Methods", "Statistics", "46%", "33%", "21%",
    "New task: Exercise sheet 3", "now", "✓",
]


def font_face() -> str:
    f = TTFont(font_path)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    s = subset.Subsetter(opts)
    s.populate(text="".join(TEXTS))
    s.subset(f)
    buf = io.BytesIO()
    f.flavor = "woff2"
    f.save(buf)
    data = base64.b64encode(buf.getvalue()).decode()
    return (
        "@font-face{font-family:N;font-weight:200 1000;"
        f"src:url(data:font/woff2;base64,{data}) format('woff2')}}"
    )


def svg(t: dict) -> str:
    c = t
    anim = "" if still else """
.in{opacity:0;animation:in .7s cubic-bezier(.2,.8,.2,1) both}
.d1{animation-delay:.15s}.d2{animation-delay:.35s}.d3{animation-delay:.55s}
.d4{animation-delay:.9s}.d5{animation-delay:1.2s}.d6{animation-delay:1.5s}
@keyframes in{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.plus{transform-box:fill-box;transform-origin:center;animation:pop 1s .2s cubic-bezier(.3,1.6,.5,1) both, glow 4s 1.4s ease-in-out infinite}
@keyframes pop{from{transform:scale(0) rotate(-90deg)}to{transform:none}}
@keyframes glow{0%,100%{filter:none}50%{filter:drop-shadow(0 0 5px #76ffce)}}
.grow{transform-box:fill-box;transform-origin:left center;animation:grow 7s ease-in-out infinite}
.g1{animation-delay:1.6s}.g2{animation-delay:1.75s}.g3{animation-delay:1.9s}.g4{animation-delay:1.3s}
@keyframes grow{0%{transform:scaleX(0)}14%,86%{transform:scaleX(1)}100%{transform:scaleX(0)}}
.toast{animation:toast 7s 2.2s cubic-bezier(.2,.8,.2,1) infinite both}
@keyframes toast{0%{opacity:0;transform:translateX(40px)}8%,80%{opacity:1;transform:none}92%,100%{opacity:0;transform:translateX(40px)}}
.blob{animation:drift 12s ease-in-out infinite alternate}
@keyframes drift{to{transform:translate(-60px,30px)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;opacity:1!important}}
"""
    font = "font-family:N,'Nunito',ui-sans-serif,system-ui,sans-serif"
    # right-hand course mock
    x0 = 690
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="plat.plus: Your course, all in one place. For everyone who teaches or learns.">
<style>{font_face()}
text{{{font}}}
{anim}</style>
<defs>
<radialGradient id="g" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{c['glow']}" stop-opacity=".35"/><stop offset="1" stop-color="{c['glow']}" stop-opacity="0"/></radialGradient>
<clipPath id="r"><rect width="{W}" height="{H}" rx="24"/></clipPath>
<filter id="sh" x="-10%" y="-20%" width="120%" height="160%"><feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000" flood-opacity=".12"/></filter>
</defs>
<g clip-path="url(#r)">
<rect width="{W}" height="{H}" fill="{c['bg']}"/>
<g class="blob"><circle cx="980" cy="120" r="380" fill="url(#g)"/></g>
<circle cx="120" cy="460" r="260" fill="url(#g)" opacity=".6"/>

<g transform="translate(80 64) scale(1.5)"><g class="in">
<rect width="64" height="64" rx="16" fill="#0f7a58"/>
<rect x="13" y="21" width="8" height="32" rx="4" fill="#fff"/>
<circle cx="28" cy="31" r="10" fill="none" stroke="#fff" stroke-width="8"/>
<path class="plus" d="M47 12v14M40 19h14" stroke="#76ffce" stroke-width="6" stroke-linecap="round"/>
</g></g>
<text class="in d1" x="76" y="262" font-size="88" font-weight="850" fill="{c['fg']}" letter-spacing="-2">plat<tspan fill="{c['primary']}">.plus</tspan></text>
<text class="in d2" x="80" y="316" font-size="31" font-weight="700" fill="{c['fg']}">Your course, all in one place.</text>
<text class="in d3" x="80" y="360" font-size="21" font-weight="600" fill="{c['muted']}">For everyone who teaches or learns<tspan dx="14" fill="{c['primary']}">·</tspan><tspan dx="14">Hosted in Germany</tspan></text>

<g class="in d3" filter="url(#sh)">
<rect x="{x0}" y="56" width="500" height="132" rx="18" fill="{c['card']}" stroke="{c['border']}"/>
<text x="{x0+26}" y="94" font-size="20" font-weight="800" fill="{c['fg']}">Week 3 · Sources and methods</text>
<text x="{x0+26}" y="122" font-size="15" font-weight="600" fill="{c['muted']}">Session · Thursday 10:00</text>
<rect x="{x0+26}" y="140" width="152" height="30" rx="15" fill="{c['soft']}"/>
<text x="{x0+42}" y="160" font-size="14" font-weight="700" fill="{c['primary']}">Reading list.pdf</text>
<rect x="{x0+190}" y="140" width="166" height="30" rx="15" fill="{c['soft']}"/>
<text x="{x0+206}" y="160" font-size="14" font-weight="700" fill="{c['primary']}">Notes · Group work</text>
</g>

<g class="in d4" filter="url(#sh)">
<rect x="{x0}" y="204" width="240" height="176" rx="18" fill="{c['card']}" stroke="{c['border']}"/>
<text x="{x0+22}" y="240" font-size="17" font-weight="800" fill="{c['fg']}">Task · Exercise sheet 2</text>
<text x="{x0+22}" y="268" font-size="14" font-weight="600" fill="{c['muted']}">18 of 24 handed in</text>
<rect x="{x0+22}" y="282" width="196" height="10" rx="5" fill="{c['bar']}"/>
<rect class="grow g4" x="{x0+22}" y="282" width="147" height="10" rx="5" fill="{c['primary']}"/>
<rect x="{x0+22}" y="320" width="178" height="34" rx="17" fill="{c['primary']}"/>
<text x="{x0+40}" y="342" font-size="14" font-weight="800" fill="{c['primary_fg']}">✓  Feedback released</text>
</g>

<g class="in d5" filter="url(#sh)">
<rect x="{x0+256}" y="204" width="244" height="176" rx="18" fill="{c['card']}" stroke="{c['border']}"/>
<text x="{x0+276}" y="238" font-size="14" font-weight="800" fill="{c['fg']}">What has been hardest so far?</text>
""" + "".join(
        f"""<text x="{x0+276}" y="{270+i*36}" font-size="13" font-weight="700" fill="{c['muted']}">{label}</text>
<text x="{x0+480}" y="{270+i*36}" font-size="13" font-weight="800" fill="{c['fg']}" text-anchor="end">{pct}</text>
<rect x="{x0+276}" y="{278+i*36}" width="204" height="8" rx="4" fill="{c['bar']}"/>
<rect class="grow g{i+1}" x="{x0+276}" y="{278+i*36}" width="{w}" height="8" rx="4" fill="{c['primary']}" opacity="{1-i*.25}"/>
"""
        for i, (label, pct, w) in enumerate(
            [("Methods", "46%", 94), ("Reading", "33%", 67), ("Statistics", "21%", 43)]
        )
    ) + f"""</g>

<g class="toast">
<g filter="url(#sh)">
<rect x="{W-404}" y="20" width="300" height="50" rx="25" fill="{c['fg']}"/>
<circle cx="{W-378}" cy="45" r="9" fill="{c['primary']}"/>
<text x="{W-358}" y="51" font-size="15" font-weight="800" fill="{c['bg']}">New task: Exercise sheet 3</text>
<text x="{W-124}" y="51" font-size="13" font-weight="700" fill="{c['muted']}" text-anchor="end">now</text>
</g>
</g>
</g>
</svg>
"""


for name, theme in THEMES.items():
    path = f"{out}/banner-{name}{'-still' if still else ''}.svg"
    with open(path, "w") as fh:
        fh.write(svg(theme))
    print(path)
