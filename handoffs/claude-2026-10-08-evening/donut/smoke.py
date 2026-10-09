"""Smoke test for The Donut View: errors, screenshots, and its numbers against dims.py."""
import json, math
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
SH = HERE / "shots"; SH.mkdir(exist_ok=True)
html = (HERE / "donut-view.html").read_text()
pv = HERE / "preview.html"
pv.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head><body>' + html + "</body></html>")
URL = pv.resolve().as_uri()
res, errs = {}, []
def guard(p, tag):
    p.on("pageerror", lambda e: errs.append(f"{tag} PAGEERROR {e}"))
    p.on("console", lambda m: errs.append(f"{tag} {m.text}") if m.type == "error" and "net::" not in m.text and "fonts" not in m.text else None)

dims = json.load(open(HERE.parent / "phase" / "dims.json"))
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    guard(pg, "desk")
    pg.goto(URL); pg.wait_for_timeout(1200)
    pg.locator("#stage").screenshot(path=str(SH / "d_donut.png"))
    pg.locator(".panel").screenshot(path=str(SH / "d_panel.png"))
    # layer stats in the page vs dims.py (2 clocks)
    rows = {r["m"]: r for r in dims["2"]["rows"]}
    bad = pg.evaluate("""(rows) => { const out = []; for (let m = 2; m <= 40; m++) { const s = window.__dv.layerStats(m); const r = rows[m];
        if (!r || s.lo !== r.lo || s.hi !== r.hi || s.primes !== r.primes || s.longest !== r.longest || s.cap !== r.cap) out.push(m); } return out; }""",
        {str(k): v for k, v in rows.items()})
    res["layer_mismatch"] = bad
    # open cells are a product grid and match coprime residues on one ring
    res["grid_check"] = pg.evaluate("""() => { const dv = window.__dv; const out = [];
        for (const [a, b] of [[2,3],[5,6],[7,30],[8,9],[11,12]]) { dv.setClocks(a, b); let open = 0, ring = 0;
          for (let r = 0; r < a; r++) for (let s = 0; s < b; s++) if (dv.cellType(r, s, a, b) === 'open') open++;
          const L = a*b; const g = (x, y) => { while (y) [x, y] = [y, x % y]; return x; };
          for (let k = 0; k < L; k++) if (g(k, L) === 1) ring++;
          out.push([a, b, open, ring]); } return out; }""")
    pg.evaluate("() => { window.__dv.setClocks(5, 6); window.__dv.setView('flat'); }"); pg.wait_for_timeout(300)
    pg.locator("#stage").screenshot(path=str(SH / "d_flat56.png"))
    pg.evaluate("() => { window.__dv.setLayer(9); }"); pg.wait_for_timeout(300)
    pg.locator("#stage").screenshot(path=str(SH / "d_layer9.png"))
    res["layer9"] = pg.inner_text("#layerText")
    pg.evaluate("() => { window.__dv.setView('donut'); window.__dv.setClocks(7, 30); window.__dv.setCounting(true); }"); pg.wait_for_timeout(2500)
    pg.locator("#stage").screenshot(path=str(SH / "d_donut730.png"))
    res["now"] = pg.inner_text("#now")
    pg.evaluate("() => { window.__dv.setClocks(4, 6); window.__dv.setCounting(false); }"); pg.wait_for_timeout(300)
    res["shared"] = pg.inner_text("#clockText")
    pg.locator("#stage").screenshot(path=str(SH / "d_donut46.png"))
    pg.locator("#chartGroup").scroll_into_view_if_needed(); pg.wait_for_timeout(200)
    bb = pg.locator("#ch").bounding_box()
    pg.mouse.move(bb["x"] + bb["width"] * 0.9, bb["y"] + bb["height"] * 0.4); pg.wait_for_timeout(200)
    pg.locator("#chartGroup").screenshot(path=str(SH / "d_chart.png"))
    res["tip"] = pg.inner_text("#tip")
    res["desk_sw"] = pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    # frame cost while spinning
    res["ms_frame"] = pg.evaluate("""() => new Promise(r => { let n = 0; const t0 = performance.now(); function f(){ n++; if (n < 60) requestAnimationFrame(f); else r((performance.now()-t0)/60); } requestAnimationFrame(f); })""")
    n = pg.locator("#finds button").count()
    for i in range(n):
        pg.locator("#finds button").nth(i).click(); pg.wait_for_timeout(250)
    res["finds"] = n
    ph = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, has_touch=True, is_mobile=True)
    guard(ph, "phone")
    ph.goto(URL); ph.wait_for_timeout(1200)
    ph.screenshot(path=str(SH / "p_top.png"))
    res["phone_sw"] = ph.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    ph.click("#vFlat"); ph.wait_for_timeout(300)
    ph.screenshot(path=str(SH / "p_flat.png"))
    b.close()
res["errors"] = errs
print(json.dumps(res, indent=1))
