"""KOLSAG banner SVG'lerini (koyu + açık) üretir.

Çıktı: assets/banner-dark.svg, assets/banner-light.svg
Animasyon SMIL + CSS ile yapılır; GitHub <img> içinde ikisi de çalışır.
Harici font yüklenemez, bu yüzden sistem font yığını kullanılır.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

THEMES = {
    "dark": {
        "paper": "#0a1124",
        "ink": "#f5f7ff",
        "muted": "#9fb0d0",
        "soft": "#3b4a6b",
        "grid": "rgba(160,190,255,0.07)",
        "accent": "#4f8cff",
    },
    "light": {
        "paper": "#eef3ff",
        "ink": "#0a1124",
        "muted": "#3d4a66",
        "soft": "#a9b6d3",
        "grid": "rgba(10,17,36,0.07)",
        "accent": "#2563eb",
    },
}

ROLES = (
    "Partner @ Lune Yazılım",
    "Software Engineer",
    "Building with AI agents",
)

WIDTH, HEIGHT = 1200, 320
ROLE_X, ROLE_Y = 330, 214
CHAR_W = 15.6  # 26px monospace, textLength ile sabitlenir
CYCLE = 4.0  # her rol için saniye
TOTAL = CYCLE * len(ROLES)


def _role_keyframes(index: int, width: float) -> tuple[str, str]:
    """Bir rol için (values, keyTimes): yaz, bekle, sil, gizli kal."""
    start = index * CYCLE / TOTAL
    step = CYCLE / TOTAL
    typed = start + step * 0.30
    hold = start + step * 0.80
    erased = start + step * 0.95
    points = [(0.0, 0.0)]
    if start > 0:
        points.append((start, 0.0))
    points += [(typed, width), (hold, width), (erased, 0.0)]
    if erased < 1:
        points.append((1.0, 0.0))
    values = ";".join(f"{v:.1f}" for _, v in points)
    times = ";".join(f"{t:.4f}" for t, _ in points)
    return values, times


def _role_block(index: int, role: str, theme: dict) -> str:
    width = round(len(role) * CHAR_W, 1)
    values, times = _role_keyframes(index, width)
    cursor_values = ";".join(
        f"{ROLE_X + float(v) + 4:.1f}" for v in values.split(";")
    )
    clip_id = f"role{index}"
    return f"""
  <clipPath id="{clip_id}">
    <rect x="{ROLE_X}" y="{ROLE_Y - 30}" width="0" height="42">
      <animate attributeName="width" values="{values}" keyTimes="{times}" dur="{TOTAL}s" repeatCount="indefinite"/>
    </rect>
  </clipPath>
  <text x="{ROLE_X}" y="{ROLE_Y}" class="role" textLength="{width}" lengthAdjust="spacingAndGlyphs" clip-path="url(#{clip_id})">{role}</text>
  <rect class="cursor" x="{ROLE_X}" y="{ROLE_Y - 24}" width="12" height="30" fill="{theme['accent']}" opacity="0">
    <animate attributeName="x" values="{cursor_values}" keyTimes="{times}" dur="{TOTAL}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{index * CYCLE / TOTAL:.4f};{index * CYCLE / TOTAL + 0.0001:.4f};{(index + 0.97) * CYCLE / TOTAL:.4f};{(index + 0.97) * CYCLE / TOTAL + 0.0001:.4f};1" dur="{TOTAL}s" repeatCount="indefinite" calcMode="discrete"/>
  </rect>"""


def _commit_grid(theme: dict) -> str:
    """Sağda katkı grafiğini andıran, dalga halinde yanan kare ızgara."""
    cols, rows, size, gap = 12, 7, 16, 5
    left, top = WIDTH - 60 - cols * (size + gap), 70
    cells = []
    for c in range(cols):
        for r in range(rows):
            delay = (c * 0.18 + r * 0.07) % 4.2
            # deterministik "yoğunluk": bazı hücreler hiç yanmaz
            level = (c * 7 + r * 13 + c * r) % 5
            peak = (0, 0.25, 0.45, 0.7, 1)[level]
            cells.append(
                f'<rect x="{left + c * (size + gap)}" y="{top + r * (size + gap)}" '
                f'width="{size}" height="{size}" rx="3" fill="{theme["accent"]}" '
                f'style="--p:{peak};animation-delay:{delay:.2f}s" class="cell"/>'
            )
    base = "".join(
        f'<rect x="{left + c * (size + gap)}" y="{top + r * (size + gap)}" '
        f'width="{size}" height="{size}" rx="3" fill="{theme["grid"]}"/>'
        for c in range(cols)
        for r in range(rows)
    )
    return f'<g class="grid-wrap">{base}{"".join(cells)}</g>'


def build_svg(theme: dict) -> str:
    roles = "".join(_role_block(i, r, theme) for i, r in enumerate(ROLES))
    grid = _commit_grid(theme)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}" role="img" aria-label="Emre Kolunsag - Partner at Lune Yazilim, Software Engineer">
  <style>
    .name {{ font: 300 64px 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif; letter-spacing: 2px; fill: {theme['ink']}; opacity: 0; animation: rise 1s .5s cubic-bezier(.2,.7,.2,1) forwards; }}
    .role {{ font: 500 26px ui-monospace, 'Cascadia Code', Consolas, Menlo, monospace; fill: {theme['muted']}; }}
    .prompt {{ font: 500 26px ui-monospace, 'Cascadia Code', Consolas, Menlo, monospace; fill: {theme['accent']}; opacity: 0; animation: fade .6s 1.1s forwards; }}
    .meta {{ font: 400 15px ui-monospace, 'Cascadia Code', Consolas, Menlo, monospace; fill: {theme['muted']}; letter-spacing: 1px; opacity: 0; animation: fade 1s 1.6s forwards; }}
    .k1 {{ opacity: 0; animation: slideR .7s .05s cubic-bezier(.2,.7,.2,1) forwards; }}
    .k2 {{ opacity: 0; animation: slideL .7s .25s cubic-bezier(.2,.7,.2,1) forwards; }}
    .k3 {{ opacity: 0; animation: slideL .7s .40s cubic-bezier(.2,.7,.2,1) forwards; }}
    .bar {{ transform-origin: 330px 0; transform: scaleX(0); animation: grow 1.2s .9s cubic-bezier(.2,.7,.2,1) forwards; }}
    .glow {{ animation: pulse 6s ease-in-out infinite; transform-origin: 160px 160px; }}
    .scan {{ animation: scan 7s linear infinite; }}
    .dot {{ animation: blink 1.6s ease-in-out infinite; }}
    .cell {{ opacity: 0; animation: cell 4.2s ease-in-out infinite; }}
    .grid-wrap {{ opacity: 0; animation: fade 1s 1.2s forwards; }}
    @keyframes cell {{ 0%,100% {{ opacity: 0; }} 30%,55% {{ opacity: var(--p); }} }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes fade {{ to {{ opacity: 1; }} }}
    @keyframes slideR {{ from {{ opacity: 0; transform: translateX(-24px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes slideL {{ from {{ opacity: 0; transform: translateX(24px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes grow {{ to {{ transform: scaleX(1); }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: .55; transform: scale(1); }} 50% {{ opacity: 1; transform: scale(1.12); }} }}
    @keyframes scan {{ from {{ transform: translateX(-200px); }} to {{ transform: translateX({WIDTH + 200}px); }} }}
    @keyframes blink {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .name, .prompt, .meta, .k1, .k2, .k3 {{ animation: none; opacity: 1; }}
      .bar {{ animation: none; transform: none; }}
      .glow, .scan, .dot {{ animation: none; }}
      .grid-wrap {{ animation: none; opacity: 1; }}
      .cell {{ animation: none; opacity: var(--p); }}
    }}
  </style>
  <defs>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="{theme['grid']}" stroke-width="1"/>
    </pattern>
    <radialGradient id="glowGrad">
      <stop offset="0" stop-color="{theme['accent']}" stop-opacity=".35"/>
      <stop offset="1" stop-color="{theme['accent']}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="scanGrad" x1="0" x2="1">
      <stop offset="0" stop-color="{theme['accent']}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{theme['accent']}" stop-opacity=".10"/>
      <stop offset="1" stop-color="{theme['accent']}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="fadeGrid" x1="0" x2="1">
      <stop offset="0" stop-color="#fff" stop-opacity="1"/>
      <stop offset="1" stop-color="#fff" stop-opacity=".15"/>
    </linearGradient>
    <mask id="gridMask"><rect width="{WIDTH}" height="{HEIGHT}" fill="url(#fadeGrid)"/></mask>
  </defs>

  <rect width="{WIDTH}" height="{HEIGHT}" rx="18" fill="{theme['paper']}"/>
  <rect width="{WIDTH}" height="{HEIGHT}" rx="18" fill="url(#grid)" mask="url(#gridMask)"/>
  <rect class="scan" x="0" y="0" width="200" height="{HEIGHT}" fill="url(#scanGrad)"/>
  <circle class="glow" cx="160" cy="160" r="150" fill="url(#glowGrad)"/>

  <g transform="translate(78 78) scale(2.6)">
    <path class="k1" d="M16 8 H28 V27 H22 V37 H28 V56 H16 Z" fill="{theme['ink']}"/>
    <path class="k2" d="M28 31 L58 9 L43 9 L28 21 Z" fill="{theme['accent']}"/>
    <path class="k3" d="M28 33 L58 55 L43 55 Q34 47 28 43 Z" fill="{theme['ink']}"/>
  </g>

  {grid}

  <text x="326" y="148" class="name">Emre Kolunsağ</text>
  <rect class="bar" x="330" y="168" width="140" height="3" fill="{theme['accent']}"/>
  <text x="{ROLE_X - 30}" y="{ROLE_Y}" class="prompt">&gt;</text>
  {roles}

  <g class="meta">
    <circle class="dot" cx="336" cy="265" r="5" fill="{theme['accent']}"/>
    <text x="350" y="270">LUNE YAZILIM  ·  TYPESCRIPT  ·  PYTHON  ·  AI AGENTS</text>
  </g>
  <text x="{WIDTH - 40}" y="{HEIGHT - 28}" text-anchor="end" class="meta" fill="{theme['soft']}">KOLSAG</text>
</svg>
"""


def main() -> None:
    out = ROOT / "assets"
    out.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (out / f"banner-{name}.svg").write_text(build_svg(theme), encoding="utf-8")
        print(f"assets/banner-{name}.svg")


if __name__ == "__main__":
    main()
