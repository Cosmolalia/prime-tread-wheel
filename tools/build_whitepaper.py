#!/usr/bin/env python3
"""Build whitepaper.html from WHITEPAPER.md.

grand.html's "White Paper" tab loads whitepaper.html; the HTML file is a
build artifact of this script, the way the other reading pages are
hand-written. Re-run after any WHITEPAPER.md edit:

    python3 tools/build_whitepaper.py
"""
import pathlib
import re

import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "WHITEPAPER.md"
OUT = ROOT / "whitepaper.html"

CSS = """
:root {
  --bg: #0b0e14; --panel: #10141d; --line: #1e2635;
  --ink: #d7dce6; --dim: #7c8698; --gold: #e8b84b;
  --mono: ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, monospace;
  color-scheme: dark;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink);
  font: 16px/1.65 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width: 72ch; margin: 0 auto; padding: 48px 22px 96px; }
h1 { font-size: 1.7rem; letter-spacing: .01em; color: var(--gold); margin: 0 0 4px; }
h2 { font-size: 1.25rem; margin: 2.2em 0 .5em; padding-top: 1em;
  border-top: 1px solid var(--line); }
h3 { font-size: 1.05rem; margin: 1.6em 0 .4em; color: var(--gold); }
p, li { color: var(--ink); }
li { margin: .3em 0; }
a { color: var(--gold); }
code { font-family: var(--mono); font-size: .88em; background: var(--panel);
  border: 1px solid var(--line); border-radius: 4px; padding: .1em .35em; }
pre { background: var(--panel); border: 1px solid var(--line); border-radius: 8px;
  padding: 14px 16px; overflow-x: auto; }
pre code { background: none; border: 0; padding: 0; font-size: .82rem; line-height: 1.5; }
blockquote { margin: 1em 0; padding: .2em 1.1em; border-left: 3px solid var(--gold);
  background: var(--panel); }
blockquote p { margin: .5em 0; }
table { border-collapse: collapse; margin: 1.2em 0; font-size: .92rem; }
th, td { border: 1px solid var(--line); padding: 6px 12px; text-align: left; }
th { background: var(--panel); color: var(--gold); font-weight: 600; }
hr { border: 0; border-top: 1px solid var(--line); margin: 2.5em 0; }
.meta { color: var(--dim); font-size: .85rem; margin: 0 0 2em;
  font-family: var(--mono); }
strong { color: #fff; }
"""

HEADER = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="The Prime Tread Wheel white paper — mechanism-first number theory on a growing wheel of counting. Every claim labeled stated, follows, gap, or established.">
<meta name="color-scheme" content="dark">
<title>The Prime Tread Wheel — White Paper</title>
<style>%s</style>
</head>
<body>
<main>
"""

FOOTER = """
</main>
</body>
</html>
"""


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )
    # The markdown source's closing italic line and epistemic labels need
    # no special handling; keep the build honest and plain.
    out = HEADER % CSS + body + FOOTER
    OUT.write_text(out, encoding="utf-8")
    print(f"{OUT.name}: {len(out)} bytes from {SRC.name}")


if __name__ == "__main__":
    main()
