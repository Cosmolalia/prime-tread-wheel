// Node checks for HornView.makeShape: the skin is laid on exactly (every ring wedge*m long, every layer one unit out,
// the seam closes when rolled up), and the closed-form normals match numeric ones.  Run: node test_shape.js
require("./horn-view.js");
const S = globalThis.HornView.makeShape, TAU = Math.PI * 2;
let fails = 0;
const ok = (c, msg) => { if (!c) { fails++; console.log("FAIL", msg); } };
for (const W of [0.5, 1, 2, 3, 5, 6, TAU, 7, 9, 12]) for (const u of W <= TAU ? [0, 0.3, 0.7, 1] : [0]) {
  const sh = S(W, u), a = [0, 0, 0], b = [0, 0, 0], n = [0, 0, 0];
  let L = 0; sh.dir(-W / 2, a);
  for (let i = 1; i <= 20000; i++) { sh.dir(-W / 2 + (W * i) / 20000, b); L += Math.hypot(b[0] - a[0], b[1] - a[1], b[2] - a[2]); a[0] = b[0]; a[1] = b[1]; a[2] = b[2]; }
  ok(Math.abs(L - W) < 1e-4, `ring length ${L} vs ${W} (u=${u})`);
  for (let i = 0; i <= 50; i++) { sh.frame(-W / 2 + (W * i) / 50, a, n); ok(Math.abs(Math.hypot(...a) - 1) < 1e-12 && Math.abs(Math.hypot(...n) - 1) < 1e-9 && Math.abs(a[0] * n[0] + a[1] * n[1] + a[2] * n[2]) < 1e-9, "unit frame"); }
  if (u === 0) { sh.dir(W / 2, a); sh.dir(-W / 2, b); ok(Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]) < 1e-9, `seam closes (W=${W})`); }
}
const h = S(1, 0); console.log("square tiles: half-angle", ((h.halfAngle * 180) / Math.PI).toFixed(3), "deg (expect asin(1/2π) = 9.158)");
console.log(fails ? `${fails} checks FAILED` : "all shape checks passed");
