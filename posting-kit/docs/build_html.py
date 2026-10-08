import markdown, re, pathlib

doc = pathlib.Path(__file__).parent
md = (doc / "essay.md").read_text()

body = markdown.markdown(md, extensions=["extra"])

# The markdown carries its own bare-name image refs (![](wheel-16-layers.png));
# they 404 next to the essay and read as long alt-text paragraphs. The injected
# figures below replace them, so drop any img whose src has no directory part.
body = re.sub(r'<p><img alt="[^"]*" src="[^"/]+"\s*/></p>\n?', '', body)

# The X-thread table's "Pair it with" column holds bare filenames as text.
# Render images as thumbnails and the video as an inline player.
def media_cell(m):
    name = m.group(1)
    if name.endswith(".mp4"):
        return (f'<td><video src="post-media/{name}" controls muted loop '
                f'class="thumb"></video></td>')
    return f'<td><img src="post-media/{name}" alt="" class="thumb"></td>'
body = re.sub(r'<td>([\w.-]+\.(?:png|mp4))</td>', media_cell, body)

FIGS = {
    "The rule": ("figures/wheel-diagram.png",
                 "The wheel. Each ring is one layer; gold marks fresh ticks, blue marks revisits."),
    "The slip law": ("figures/slip-burst.png",
                     "Six hundred layers of slip. Each spoke's grain against the next, ratio painted as color."),
    "The drum": ("figures/drum-unrolled.png",
                 "The same wheel, unrolled flat. Columns are spokes, rows are layers, gold is a fresh tick."),
}

for section, (src, cap) in FIGS.items():
    h2 = f"<h2>{section}</h2>"
    fig = (f'{h2}\n<figure><img src="{src}" alt="{cap}">'
           f"<figcaption>{cap}</figcaption></figure>")
    assert h2 in body, f"section not found: {section}"
    body = body.replace(h2, fig, 1)

# The X thread is a list of posts — render as cards for the HTML version.
body = body.replace("<h2>X thread</h2>", '<h2 class="thread">X thread</h2>')

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>I Rolled the Number Line Onto a Wheel</title>
<style>
  :root {{
    --ink:#1a1a1a; --muted:#666; --rule:#e3e0da; --accent:#8a6d1d;
    --paper:#fdfcf9; --card:#f6f4ee;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin:0; background:var(--paper); color:var(--ink);
    font:18px/1.7 Georgia, 'Times New Roman', serif;
  }}
  main {{ max-width:680px; margin:0 auto; padding:48px 24px 96px; }}
  h1 {{ font-size:2.2rem; line-height:1.2; margin:0 0 6px; letter-spacing:-0.5px; }}
  .byline {{ color:var(--muted); font-size:0.95rem; margin-bottom:40px;
             font-family:-apple-system, 'Segoe UI', sans-serif; }}
  h2 {{ font-size:1.5rem; margin:52px 0 8px; letter-spacing:-0.3px; }}
  p  {{ margin:0 0 1.1em; }}
  a  {{ color:var(--accent); }}
  figure {{ margin:28px 0 36px; }}
  figure img {{ width:100%; height:auto; border-radius:8px; display:block;
                background:#0b1020; }}
  figcaption {{ color:var(--muted); font-size:0.9rem; margin-top:10px;
                text-align:center; font-family:-apple-system, 'Segoe UI', sans-serif; }}
  ul, ol {{ padding-left:1.4em; }}
  li {{ margin-bottom:0.5em; }}
  .thread + ol li {{
    list-style:none; background:var(--card); border:1px solid var(--rule);
    border-radius:10px; padding:14px 18px; margin:0 0 12px -1.4em;
    font-family:-apple-system, 'Segoe UI', sans-serif; font-size:0.98rem; line-height:1.5;
  }}
  .thumb {{ width:220px; max-width:100%; border-radius:8px; display:block;
             background:#0b1020; }}
  hr {{ border:0; border-top:1px solid var(--rule); margin:48px 0; }}
  em {{ color:#444; }}
</style>
</head>
<body>
<main>
{body}
</main>
</body>
</html>
"""

out = doc / "essay.html"
out.write_text(html)
print("wrote", out, len(html), "bytes")
