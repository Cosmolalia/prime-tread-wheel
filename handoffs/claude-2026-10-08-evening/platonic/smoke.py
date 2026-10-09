"""Smoke test for The Platonic Map: errors, screenshots, and the page's numbers against the computation."""
import json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
SHOTS = HERE / "shots"; SHOTS.mkdir(exist_ok=True)
page_html = (HERE / "platonic-map.html").read_text()
preview = HERE / "preview.html"
preview.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head><body>' + page_html + "</body></html>")
URL = preview.resolve().as_uri()
which = sys.argv[1] if len(sys.argv) > 1 else "all"
res, errs = {}, []

def guard(page, tag):
    page.on("pageerror", lambda e: errs.append(f"{tag} PAGEERROR {e}"))
    page.on("console", lambda m: errs.append(f"{tag} {m.text}") if m.type == "error" and "ERR_TUNNEL" not in m.text and "fonts" not in m.text and "net::" not in m.text else None)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    guard(pg, "desk")
    t0 = time.time(); pg.goto(URL); pg.wait_for_timeout(1200); res["load_s"] = round(time.time() - t0, 2)
    pg.locator("#stage").screenshot(path=str(SHOTS / "d_default.png"))
    pg.locator(".panel").screenshot(path=str(SHOTS / "d_panel.png"))
    res["layerText"] = pg.inner_text("#layerText")
    res["pickText"] = pg.inner_text("#pickText")

    if which in ("all", "math"):
        # 1. clean columns == primes in real mode, across several windows
        res["classify"] = pg.evaluate("""() => {
          const pm = window.__pm; pm.setMode('real'); const bad = [];
          for (const [x0, n] of [[1, 300], [800, 600], [5000, 900], [99000, 1200], [298000, 1500]]) {
            pm.setWindow(x0, n);
            pm.S.n = n; pm.S.x0 = x0;
          }
          return 'deferred';
        }""")
        # draw synchronously by waiting a frame per window
        out = []
        for x0, n in [(1, 300), (800, 600), (5000, 900), (99000, 1200), (298000, 1400)]:
            pg.evaluate(f"() => window.__pm.setWindow({x0}, {n})"); pg.wait_for_timeout(60)
            out.append(pg.evaluate("""() => { const G = window.__pm.G(), pm = window.__pm; let bad = 0, primes = 0;
                for (let j = 0; j < G.n; j++) { const x = G.x0 + j; const p = pm.isPrime(x); if (p) primes++; if ((G.info.clean[j] === 1) !== p) bad++; }
                return [G.x0, G.n, primes, bad, G.rings.length]; }"""))
        res["classify"] = out
        # 2. stats in JS == margin.json rows
        res["stats_match"] = pg.evaluate("""() => { const pm = window.__pm; let bad = [];
            for (const r of pm.ROWS) { const s = pm.stats(r.m); if (s.k !== r.k || s.real !== r.real || s.primes !== r.primes || s.free !== r.free || s.can !== r.can) bad.push(r.m); }
            return bad; }""")
        # 3. every layer 2..391: wipe-out setting leaves 0 clean columns when 'can', >0 when not; CRT == first where exact
        res["blank"] = pg.evaluate("""() => { const pm = window.__pm; const out = {can: 0, cant: 0, bad: [], firstMatch: 0, firstChecked: 0, cantMin: 1e9};
            for (let m = 2; m <= 391; m++) {
              const st = pm.stats(m); if (!st.k) continue;
              const bs = pm.blankSetting(m);
              if (bs.phases[0] !== 0) out.bad.push(['ring2', m]);
              if (bs.source === 'built' && bs.t + m > bs.L) out.bad.push(['window', m]);
              pm.blankNow(m);
              const c = pm.cleanInLayer(m);
              if (st.can) { out.can++; if (c !== 0) out.bad.push(['can', m, c]); }
              else { out.cant++; if (c === 0) out.bad.push(['cant', m]); out.cantMin = Math.min(out.cantMin, c); }
              if (st.can && st.first != null) { out.firstChecked++; const {y} = pm.crtPlace(m); if (y === BigInt(st.first)) out.firstMatch++; else out.bad.push(['crt', m, String(y), st.first]); }
            }
            pm.setMode('real'); return out; }""")
        # 3b. the pin demo: every ring up to 83 at 0, layer 390 wiped
        res["pin_demo"] = pg.evaluate("""() => { const pm = window.__pm; pm.pinDemo();
            const small = pm.PRIMES.filter(p => p <= 83).every(p => pm.phaseOf(p) === 0);
            const c = pm.cleanInLayer(390); pm.setMode('real'); return {small_at_zero: small, clean: c}; }""")
        # 4. CRT with all phases 0 is the layer's own start (mod the cycle)
        res["crt_zero"] = pg.evaluate("""() => { const pm = window.__pm; pm.setMode('free'); pm.S.ph.clear(); const bad = [];
            for (const m of [18, 41, 60, 200, 390]) { const {y, M, st} = pm.crtPlace(m); if (y !== BigInt(st.lo) % M) bad.push(m); }
            pm.setMode('real'); return bad; }""")

    # screenshots: free mode wipe-out of layer 41, layer 22 best try, all rings, sqrt edge, big window
    pg.evaluate("() => { window.__pm.setMode('real'); window.__pm.setWindow(1, 120); window.__pm.setLayer(15, false); }"); pg.wait_for_timeout(100)
    pg.click("#mFree"); pg.wait_for_timeout(100)
    pg.fill("#lIn", "41"); pg.click("#lGo"); pg.wait_for_timeout(100)
    pg.click("#bBlank"); pg.wait_for_timeout(2600)
    pg.locator("#stage").screenshot(path=str(SHOTS / "d_blank41.png"))
    res["blank41_layer"] = pg.inner_text("#layerText"); res["blank41_place"] = pg.inner_text("#placeText")
    pg.locator(".panel").screenshot(path=str(SHOTS / "d_panel_free.png"))
    pg.fill("#lIn", "22"); pg.click("#lGo"); pg.click("#bBlank"); pg.wait_for_timeout(2000)
    pg.locator("#stage").screenshot(path=str(SHOTS / "d_blank22.png"))
    res["blank22_layer"] = pg.inner_text("#layerText"); res["blank22_place"] = pg.inner_text("#placeText")
    pg.fill("#lIn", "200"); pg.click("#lGo"); pg.click("#bBlank"); pg.wait_for_timeout(2300)
    pg.locator("#stage").screenshot(path=str(SHOTS / "d_blank200.png"))
    res["blank200_layer"] = pg.inner_text("#layerText"); res["blank200_place"] = pg.inner_text("#placeText")
    # drag a ring in free mode
    box = pg.locator("#cv").bounding_box()
    pg.click("#mReal"); pg.wait_for_timeout(80)
    pg.evaluate("() => { window.__pm.setWindow(1, 120); window.__pm.setLayer(15, false); }"); pg.wait_for_timeout(80)
    # hover a column
    pg.mouse.move(box["x"] + box["width"] * 0.5, box["y"] + box["height"] * 0.7); pg.wait_for_timeout(120)
    res["hover"] = pg.inner_text("#now")
    pg.mouse.click(box["x"] + box["width"] * 0.5, box["y"] + box["height"] * 0.7); pg.wait_for_timeout(120)
    res["picked"] = pg.inner_text("#pickText")
    # pan by dragging
    pg.mouse.move(box["x"] + box["width"] * 0.6, box["y"] + box["height"] * 0.6)
    pg.mouse.down(); pg.mouse.move(box["x"] + box["width"] * 0.3, box["y"] + box["height"] * 0.6, steps=8); pg.mouse.up(); pg.wait_for_timeout(100)
    res["after_pan_x0"] = pg.evaluate("() => window.__pm.S.x0")
    # free-mode drag of ring 3's row
    pg.click("#mFree"); pg.wait_for_timeout(80)
    pg.evaluate("() => { window.__pm.S.ph.clear(); window.__pm.setWindow(1, 120); }"); pg.wait_for_timeout(80)
    G = pg.evaluate("() => { const G = window.__pm.G(); return {top: G.top, R: G.rings.length, cw: G.cw, dpr: devicePixelRatio}; }")
    # ring index 1 (ring 3) is second from the bottom
    yb = pg.evaluate("() => { const G = window.__pm.G(); return (G.B - 1.5 * G.rhF) / devicePixelRatio; }")
    pg.mouse.move(box["x"] + box["width"] * 0.5, box["y"] + yb); pg.mouse.down()
    pg.mouse.move(box["x"] + box["width"] * 0.5 + G["cw"] / G["dpr"] * 1.05, box["y"] + yb, steps=6); pg.mouse.up(); pg.wait_for_timeout(100)
    res["ring3_phase"] = pg.evaluate("() => window.__pm.S.ph.get(3) || 0")
    pg.locator("#stage").screenshot(path=str(SHOTS / "d_turn3.png"))
    pg.click("#mReal"); pg.wait_for_timeout(60)
    pg.click("#rAll"); pg.evaluate("() => window.__pm.setWindow(1, 90)"); pg.wait_for_timeout(120)
    pg.locator("#stage").screenshot(path=str(SHOTS / "d_allrings.png"))
    pg.click("#rPrime"); pg.evaluate("() => window.__pm.setWindow(1, 1000)"); pg.wait_for_timeout(120)
    pg.locator("#stage").screenshot(path=str(SHOTS / "d_edge1000.png"))
    pg.evaluate("() => window.__pm.setWindow(150000, 1400)"); pg.wait_for_timeout(120)
    pg.locator("#stage").screenshot(path=str(SHOTS / "d_far.png"))
    # frame time while panning
    res["ms_per_frame"] = pg.evaluate("""() => new Promise(r => { const cv = document.getElementById('cv'); let n = 0; const t0 = performance.now();
       function f(){ window.__pm.S.x0 += 3; window.__pm.setWindow(window.__pm.S.x0, window.__pm.S.n); n++; if (n < 40) requestAnimationFrame(f); else r((performance.now()-t0)/40); } requestAnimationFrame(f); })""")
    # margin view
    pg.click("#vMargin"); pg.wait_for_timeout(300)
    pg.locator("#stage").screenshot(path=str(SHOTS / "d_margin.png"))
    pg.locator("#figA").screenshot(path=str(SHOTS / "d_figA.png"))
    ca = pg.locator("#chA").bounding_box()
    pg.mouse.move(ca["x"] + ca["width"] * 0.42, ca["y"] + ca["height"] * 0.5); pg.wait_for_timeout(150)
    pg.locator("#figA").screenshot(path=str(SHOTS / "d_figA_hover.png"))
    res["tipA"] = pg.inner_text("#tipA")
    pg.locator("#figB").scroll_into_view_if_needed(); pg.wait_for_timeout(200)
    cb = pg.locator("#chB").bounding_box()
    pg.mouse.move(cb["x"] + cb["width"] * 0.7, cb["y"] + cb["height"] * 0.4); pg.wait_for_timeout(150)
    pg.locator("#figB").screenshot(path=str(SHOTS / "d_figB_hover.png"))
    res["tipB"] = pg.inner_text("#tipB")
    res["desk_sw"] = pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    # findings buttons all run
    pg.click("#vMap"); pg.wait_for_timeout(100)
    nf = pg.locator("#finds button").count()
    for i in range(nf):
        pg.locator("#finds button").nth(i).click(); pg.wait_for_timeout(2300 if i in (3, 4) else 300)
        if i in (0, 3, 4, 7):
            pg.locator("#stage").screenshot(path=str(SHOTS / f"d_find{i}.png"))
    res["finds"] = nf

    # phone
    ph = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, has_touch=True, is_mobile=True)
    guard(ph, "phone")
    ph.goto(URL); ph.wait_for_timeout(1200)
    res["phone_sw"] = ph.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    ph.screenshot(path=str(SHOTS / "p_top.png"))
    ph.locator(".panel").screenshot(path=str(SHOTS / "p_panel.png"))
    ph.click("#mFree"); ph.wait_for_timeout(100); ph.click("#bBlank"); ph.wait_for_timeout(2300)
    ph.screenshot(path=str(SHOTS / "p_blank.png"))
    ph.click("#vMargin"); ph.wait_for_timeout(400)
    ph.screenshot(path=str(SHOTS / "p_margin.png"), full_page=True)
    res["phone_sw_margin"] = ph.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    b.close()

res["errors"] = errs
print(json.dumps(res, indent=1, default=str))
