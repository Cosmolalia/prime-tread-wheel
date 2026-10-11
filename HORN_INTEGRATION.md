# The horn view — Claude → Kimi, Oct 10 2026

Obi wants the wheel shown as the body its skin wraps. Give every tick the same square tile and put each layer one tile further out. Ring m is then m tiles long at slant distance m, but a flat circle needs 2π·m, so the skin rolls up into a horn with half-angle asin(1/2π) = 9.16°. The page's flat disk is the same skin with every ring stretched 2π×.

Files:
- `horn-view.js` — the renderer. WebGL1, no dependencies, classic script that defines `window.HornView`.
- `horn.html` — standalone page (full document) that loads `horn-view.js`. Built in the wheel's visual language.
- `test_shape.js` — `node test_shape.js` checks that the geometry is exact.
- Live demo: Obi's artifact "Prime Tread Horn". `horn.html` is the same page, built for the repo.

## The geometry (exact, not a look-alike)

Every shape is a cone over a curve of length `wedge` on the unit sphere. `wedge` = tick width ÷ layer gap, in radians. Tick k of layer m sits at slant distance m along d(s), with s = wedge·(k/m − ½) measured from the half-turn. Every ring is therefore exactly wedge·m long and every layer exactly 1 out.

| wedge | shape |
|---|---|
| 1 | Square tiles: the horn. Unrolled, it is a 1-radian (57.3°) wedge. |
| 1 < wedge < 2π | Cones. sin(half-angle) = wedge/2π. |
| 2π | Exactly the flat page. |
| > 2π | Ruffle. The curve is a 4-wave closed curve around a great circle, with the amplitude solved so its length is the wedge. |

`unroll` ∈ [0, 1] (only for wedge ≤ 2π) slits the skin at the seam and opens it into the flat wedge. The slit's angular span shrinks linearly from a full turn to `wedge`, so every ring keeps its length at every stage.

Checked:
- Ring length equals the wedge to within 1e-4 in every state (`test_shape.js`).
- In the page, adjacent ticks on ring 100 are 0.9998 apart (the chord of a unit arc) and tick (100,30) is 100.0000 from the tip.
- The seam closes to within 1e-9 when rolled up.
- Closed-form normals match numeric ones to 1e-16.

## Using it

```js
const hv = new HornView(canvas, {
  maxLayers: 800,
  colorOf: (m, k, x) => "#f0bf55",       // any CSS color; called once per tick, cached
  onHover: (info, at, tapped) => {},     // info = {m, k, x} or null; tapped = true on a click/tap
  seam: "#ecdfc0", half: "#9fb0ff", chainA: "#5f79c4", chainB: "#c4984e", body: "#0c1330", bodyLit: "#232f5a",
});
hv.set({ layers: 120, wedge: 1, unroll: 0, chains: true, marks: true, spin: false, pointScale: 1 });
hv.recolor();             // the colors behind colorOf changed
hv.setFrame(top, bottom); // fractions of the canvas height to keep clear (title, hints)
hv.pick(clientX, clientY) // {m, k, x} | null — exact, via an id buffer, honours occlusion
hv.project([x,y,z]); hv.facing(p, n); hv.labelAnchors; hv.onAfterDraw = (v) => {}   // for label overlays
hv.tickPos(m, k); HornView.makeShape(wedge, unroll)                                     // for tests
```

Input is built in:
- drag to turn;
- wheel or pinch to zoom;
- shift-drag, right-drag or two fingers to pan;
- double-click to reset.

Growth is incremental. When `layers` rises, only the new layer's ticks, colors and lines are computed and uploaded: about 2 ms per layer at 700–800 layers in software GL, and identical to a full rebuild. GPU buffers grow in 1.5× steps. Shrinking and growing back recomputes nothing. Changing wedge or unroll rebuilds positions (about 40–60 ms at 800 layers in software GL; the default 60 layers is instant).

## Two ways to ship it

**A. Sibling page (zero risk).** Drop `horn.html` and `horn-view.js` next to `globe.html`, and link it from the wheel's header or field notes: "Horn — the skin with every tick the same size."

**B. A fifth view inside the wheel, next to the drum.** Line numbers are from `index.html` @ 89a81f7.
1. Load the renderer before the app script: `<script src="horn-view.js"></script>`, or paste it inline.
2. Stage markup: add `<canvas id="hornGL"></canvas>` over the 2D canvas (position absolute, inset 0). CSS: `.app:not(.st-horn) #hornGL { display: none; }`. Add a `styleHorn` button beside `styleCyl` ("Horn").
3. `STYLES` (≈3923): add `"horn"`. In `setStyle`, add `["styleHorn", "horn"]` to the toggle list, and the click handler.
4. Create it lazily, with the Look's own colors so every color mode carries over:
   ```js
   let horn = null, hornN = 0;
   function ensureHorn() {
     if (horn) return horn;
     horn = new HornView($("hornGL"), {
       maxLayers: MAX_LAYER, keepFitOnGrow: true,
       colorOf: (m, k, x) => TP[colorOfX(x)],
       onHover: (info) => { /* reuse statusOf(info.x) etc. for the readout / pin */ },
       seam: C.ray, half: "#9fb0ff", chainA: C.hit, chainB: C.nw,
     });
     return horn;
   }
   ```
5. In `draw()` (≈3857), add the branch `else if (style === "horn") { const h = ensureHorn(); if (n !== hornN) { h.set({ layers: Math.max(1, n) }); hornN = n; } }`. The 2D canvas only needs clearing; the GL canvas draws itself on demand. Only completed layers are shown; `found[m]` must exist for every layer passed to `colorOf`.
6. In `refreshLook()` (≈1975), after `TP = tickPalette()`, add `if (horn) horn.recolor();`.
7. Optional `.hornOnly` controls: tick width (horn / cone / 2π page / ruffle) and unroll. `horn.html` has the markup and the log-scale slider mapping (0.25 → 12, snapping to 1 and 2π).
8. `variable.html`: with square tiles, lap ratio r gives wedge = r. So r = 1 is the horn, r = 6 is a shallow cone, and r = 7 starts to ruffle. 2π is never hit by a whole-number ratio.

## What the horn shows (for the copy)

- **Back (the seam):** the lines of ticks run straight down beside the seam stripe.
- **Front (the half-turn):** the two families of lines meet in a herringbone. On the first half of the turn a tick lines up with the same tick on the next layer; on the second half, with the next tick. This is where the radial locks switch sides and where the 30°, 45° and 90° lines live (section 6 of the Oct 10 handoff).
- **Seen from above:** a wider cone with primes lit looks like a leaf, with the half-turn as its midrib.
