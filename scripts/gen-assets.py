"""Generates the README assets for bang-prefill: an animated demo and a before/after card.

Usage: python3 -I gen.py <out dir> [--static]
--static draws every element visible, for checking the layout as a still image.
"""
import sys
from html import escape

OUT = sys.argv[1]
STATIC = '--static' in sys.argv

CYCLE = 13.0
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
BG, PANEL, FG, DIM = '#14141c', '#1d1d29', '#e8e6e3', '#8b8a99'
ORANGE, GREEN, RED, BLUE = '#d97757', '#7ec699', '#e0787f', '#7aa2f7'

css_rules = []


def window(start, end=CYCLE - 0.6, fade=0.25):
    """CSS class that shows an element from `start` to `end` seconds of each cycle."""
    name = f'w{len(css_rules)}'
    if STATIC:
        css_rules.append(f'.{name}{{opacity:1}}')
        return name
    p = lambda t: f'{max(0.0, min(100.0, t / CYCLE * 100)):.2f}%'
    css_rules.append(
        f'@keyframes {name}{{0%,{p(start)}{{opacity:0}}{p(start + fade)},{p(end)}{{opacity:1}}'
        f'{p(end + fade)},100%{{opacity:0}}}}'
        f'.{name}{{opacity:0;animation:{name} {CYCLE}s infinite}}'
    )
    return name


def text(x, y, s, cls='', color=FG, size=17, weight=400, family=FONT, anchor='start'):
    return (f'<text x="{x}" y="{y}" class="{cls}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}" font-family="{family}" text-anchor="{anchor}" '
            f'xml:space="preserve">{escape(s)}</text>')


def demo():
    W, H = 900, 520
    parts = []
    # window chrome
    parts.append(f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>')
    parts.append(f'<rect width="{W}" height="40" rx="14" fill="{PANEL}"/>'
                 f'<rect y="26" width="{W}" height="14" fill="{PANEL}"/>')
    for i, c in enumerate(['#ff5f57', '#febc2e', '#28c840']):
        parts.append(f'<circle cx="{24 + i * 22}" cy="20" r="6.5" fill="{c}"/>')
    parts.append(text(W / 2, 26, 'claude — bang-prefill', color=DIM, size=14, family=SANS, anchor='middle'))

    x0, y = 34, 86
    # 1. the person's question
    c = window(0.3)
    parts.append(text(x0, y, '> is my working tree clean?', c, DIM))
    # 2. Claude suggests a command
    y += 44
    c = window(1.1)
    parts.append(f'<circle class="{c}" cx="{x0 + 5}" cy="{y - 6}" r="5" fill="{FG}"/>')
    parts.append(text(x0 + 22, y, "Let's check. Run this:", c))
    y += 34
    c = window(1.7)
    parts.append(f'<rect class="{c}" x="{x0 + 20}" y="{y - 22}" width="236" height="32" rx="6" fill="#2a2235"/>')
    parts.append(text(x0 + 32, y, '! git status --short', c, ORANGE))

    # 3. the prompt box: prefilled, then Enter
    box_y = H - 96
    parts.append(f'<rect x="{x0 - 10}" y="{box_y}" width="{W - 2 * x0 + 20}" height="50" rx="10" '
                 f'fill="none" stroke="#3a3a4d" stroke-width="1.5"/>')
    parts.append(text(x0 + 6, box_y + 32, '>', color=DIM))
    c = window(2.7, 5.0)
    parts.append(f'<rect class="{c}" x="{x0 - 10}" y="{box_y}" width="{W - 2 * x0 + 20}" height="50" rx="10" '
                 f'fill="none" stroke="{ORANGE}" stroke-width="2"/>')
    parts.append(text(x0 + 30, box_y + 32, '! git status --short', c, FG))
    parts.append(f'<rect class="{c}" x="{x0 + 238}" y="{box_y + 16}" width="2" height="22" fill="{FG}"/>')
    parts.append(text(W - x0 - 4, box_y - 12, 'prefilled by bang-prefill', c, ORANGE, 13, family=SANS, anchor='end'))
    # Enter key cap: appears, then "pressed"
    c = window(3.6, 4.6)
    parts.append(f'<g class="{c}"><rect x="{W - x0 - 112}" y="{box_y + 9}" width="96" height="32" rx="7" '
                 f'fill="#2c2c3c" stroke="{DIM}"/>' + text(W - x0 - 64, box_y + 31, 'Enter ⏎', color=FG, size=15,
                                                           family=SANS, anchor='middle') + '</g>')
    c = window(4.6, 5.0, fade=0.1)
    parts.append(f'<g class="{c}"><rect x="{W - x0 - 112}" y="{box_y + 11}" width="96" height="30" rx="7" '
                 f'fill="{ORANGE}"/>' + text(W - x0 - 64, box_y + 31, 'Enter ⏎', color=BG, size=15, weight=600,
                                             family=SANS, anchor='middle') + '</g>')

    # 4. the command ran; Claude got the output
    y += 46
    c = window(5.1)
    parts.append(text(x0, y, '$ git status --short', c, DIM, 15))
    y += 26
    parts.append(text(x0, y, ' M', c, RED, 15) + text(x0 + 30, y, 'src/app.ts', c, FG, 15))
    y += 24
    parts.append(text(x0, y, '??', c, GREEN, 15) + text(x0 + 30, y, 'README.md', c, FG, 15))
    # 5. Claude keeps working on its own
    y += 44
    c = window(6.3)
    parts.append(f'<circle class="{c}" cx="{x0 + 5}" cy="{y - 6}" r="5" fill="{FG}"/>')
    parts.append(text(x0 + 22, y, 'One modified file and one new one. Commit them?', c))
    # 6. tagline
    c = window(8.0)
    parts.append(text(W / 2, box_y - 40, 'No copy. No paste. Just Enter.', c, ORANGE, 22, 700, SANS, 'middle'))

    return W, H, parts


def why():
    W, H = 900, 300
    parts = [f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>']
    col = [(40, 'Without bang-prefill', DIM), (470, 'With bang-prefill', ORANGE)]
    for x, title, color in col:
        parts.append(f'<rect x="{x}" y="28" width="390" height="244" rx="12" fill="{PANEL}"/>')
        parts.append(text(x + 24, 66, title, color=color, size=20, weight=700, family=SANS))
    before = ['Select the command', 'Copy it', 'Paste it, drop the backticks', 'Run it',
              'Type "look at the output"']
    for i, s in enumerate(before):
        y = 108 + i * 32
        parts.append(text(64, y, f'{i + 1}.', color=DIM, size=16, family=SANS))
        parts.append(text(92, y, s, color=FG, size=16, family=SANS))
    parts.append(f'<rect x="530" y="112" width="140" height="56" rx="10" fill="{ORANGE}"/>')
    parts.append(text(600, 148, 'Enter ⏎', color=BG, size=22, weight=700, family=SANS, anchor='middle'))
    parts.append(text(494, 210, 'The command is already in your prompt.', color=FG, size=16, family=SANS))
    parts.append(text(494, 238, 'Claude reads the output and keeps going.', color=FG, size=16, family=SANS))
    return W, H, parts


def write(name, built):
    W, H, parts = built
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<style>{"".join(css_rules)}</style>{"".join(parts)}</svg>\n')
    with open(f'{OUT}/{name}', 'w') as f:
        f.write(svg)


write('demo.svg', demo())
css_rules.clear()
write('why.svg', why())
