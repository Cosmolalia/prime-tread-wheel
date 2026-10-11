/* horn-view.js — the Prime Tread Wheel's skin with every tick the same size.
 *
 * Give every tick a tile one unit wide and put layer m one unit further out than layer m-1. Then ring m is only
 * wedge*m long at slant distance m (wedge = tick width / layer gap, in radians). A flat circle needs 2*pi*m, so for
 * wedge < 2*pi the skin rolls up into a cone; for square tiles (wedge = 1) it is a slim horn, sin(half-angle) = 1/(2*pi).
 * At wedge = 2*pi it is exactly the flat page; past 2*pi there is more ring than a flat disk holds and it ruffles.
 *
 * Exact construction: every shape here is a cone over a curve on the unit sphere whose length is `wedge`.
 * Tick k of layer m sits at slant distance m along the direction d(s), s = wedge*(k/m - 1/2) measured from the
 * half-turn. Distances along every ring and every generator are therefore exactly the tile sizes (an isometry).
 *   - closed horn / cone: d runs round a small circle of angular radius a, sin(a) = wedge / (2*pi)
 *   - unrolling: the circle's radius grows to 90 degrees (a great circle): the slit horn opens into the flat wedge
 *   - ruffle (wedge > 2*pi): a closed wavy curve round a great circle, amplitude solved so its length is `wedge`
 *
 * No dependencies. WebGL1. Classic script: defines window.HornView.
 *
 *   const hv = new HornView(canvas, { maxLayers: 800, colorOf: (m, k, x) => "#f0bf55", onHover: (info) => {} });
 *   hv.set({ layers: 120, wedge: 1, unroll: 0, chains: true, marks: true, spin: false, pointScale: 1 });
 *   hv.recolor();       // after the colors behind colorOf change
 *   hv.resize();        // after the canvas changes size (also done automatically on window resize)
 *   hv.pick(clientX, clientY) -> { m, k, x } | null
 *   hv.resetView(); hv.destroy();
 */
(function (global) {
  "use strict";
  const TAU = Math.PI * 2;

  // ---------- small helpers ----------
  function parseColor(c) {
    if (Array.isArray(c)) return c;
    c = String(c).trim();
    if (c[0] === "#") {
      let h = c.slice(1);
      if (h.length === 3) h = h.split("").map((ch) => ch + ch).join("");
      const v = parseInt(h.slice(0, 6), 16);
      return [((v >> 16) & 255) / 255, ((v >> 8) & 255) / 255, (v & 255) / 255];
    }
    const m = c.match(/rgba?\(([^)]+)\)/);
    if (m) { const p = m[1].split(",").map((s) => parseFloat(s)); return [p[0] / 255, p[1] / 255, p[2] / 255]; }
    return [1, 1, 1];
  }
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const norm = (a) => { const l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };
  function mat4Persp(fovy, aspect, near, far) {
    const f = 1 / Math.tan(fovy / 2), nf = 1 / (near - far);
    return new Float32Array([f / aspect, 0, 0, 0, 0, f, 0, 0, 0, 0, (far + near) * nf, -1, 0, 0, 2 * far * near * nf, 0]);
  }
  function mat4LookAt(eye, at, up) {
    const z = norm([eye[0] - at[0], eye[1] - at[1], eye[2] - at[2]]), x = norm(cross(up, z)), y = cross(z, x);
    return new Float32Array([x[0], y[0], z[0], 0, x[1], y[1], z[1], 0, x[2], y[2], z[2], 0,
      -(x[0] * eye[0] + x[1] * eye[1] + x[2] * eye[2]), -(y[0] * eye[0] + y[1] * eye[1] + y[2] * eye[2]), -(z[0] * eye[0] + z[1] * eye[1] + z[2] * eye[2]), 1]);
  }
  function mat4Mul(a, b) {
    const o = new Float32Array(16);
    for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) {
      let s = 0; for (let k = 0; k < 4; k++) s += a[k * 4 + j] * b[i * 4 + k];
      o[i * 4 + j] = s;
    }
    return o;
  }

  const segCount = (L) => (L * (L - 1)) / 2 - Math.floor((L - 1) / 2);

  // ---------- the shape: direction d(s) on the unit sphere for signed arc s from the half-turn ----------
  // Half-turn generator points straight down (D); the slit (seam) sits at the back when closed; the open skin faces +z.
  const D = [0, -1, 0], B = [0, 0, -1], X = [1, 0, 0];
  const RUFFLE_WAVES = 4;
  function makeShape(wedge, unroll) {
    if (wedge <= TAU + 1e-9) {
      const a0 = Math.asin(Math.min(1, wedge / TAU));
      const span = TAU * (1 - unroll) + wedge * unroll;          // how far round the slit skin still reaches
      const al = Math.asin(Math.min(1, wedge / span)), sa = Math.sin(al), ca = Math.cos(al);
      const n = [ca * D[0] + sa * B[0], ca * D[1] + sa * B[1], ca * D[2] + sa * B[2]];
      const v = [sa * D[0] - ca * B[0], sa * D[1] - ca * B[1], sa * D[2] - ca * B[2]];
      return {
        kind: unroll > 1e-6 ? "open" : wedge >= TAU - 1e-9 ? "flat" : "cone", wedge, halfAngle: a0,
        dir(s, o) {
          const p = s / sa, c = Math.cos(p), si = Math.sin(p);
          o[0] = ca * n[0] + sa * (c * v[0] + si * X[0]);
          o[1] = ca * n[1] + sa * (c * v[1] + si * X[1]);
          o[2] = ca * n[2] + sa * (c * v[2] + si * X[2]);
          return o;
        },
        // direction d and unit normal d x t (t = unit tangent of the ring), with no allocation
        frame(s, o, nn) {
          const p = s / sa, c = Math.cos(p), si = Math.sin(p);
          const d0 = ca * n[0] + sa * (c * v[0] + si * X[0]), d1 = ca * n[1] + sa * (c * v[1] + si * X[1]), d2 = ca * n[2] + sa * (c * v[2] + si * X[2]);
          const t0 = -si * v[0] + c * X[0], t1 = -si * v[1] + c * X[1], t2 = -si * v[2] + c * X[2];
          o[0] = d0; o[1] = d1; o[2] = d2;
          nn[0] = d1 * t2 - d2 * t1; nn[1] = d2 * t0 - d0 * t2; nn[2] = d0 * t1 - d1 * t0;
        },
      };
    }
    // ruffle: d(th) = cos(phi) c(th) + sin(phi) z, c(th) = (sin th, -cos th, 0), phi = A sin(w th); length over [-pi, pi] = wedge
    const w = RUFFLE_WAVES, NS = 4096;
    const lenOf = (A) => {
      let L = 0;
      for (let i = 0; i < NS; i++) {
        const th = -Math.PI + (i + 0.5) * (TAU / NS), ph = A * Math.sin(w * th), dph = A * w * Math.cos(w * th);
        L += Math.sqrt(Math.cos(ph) ** 2 + dph * dph) * (TAU / NS);
      }
      return L;
    };
    let lo = 0, hi = 1.5;
    for (let it = 0; it < 50; it++) { const mid = (lo + hi) / 2; if (lenOf(mid) < wedge) lo = mid; else hi = mid; }
    const A = (lo + hi) / 2;
    // arc length table s(th) for th in [-pi, pi], s(0) = 0
    const TH = new Float64Array(NS + 1), S = new Float64Array(NS + 1);
    for (let i = 0; i <= NS; i++) TH[i] = -Math.PI + i * (TAU / NS);
    S[0] = 0;
    for (let i = 1; i <= NS; i++) {
      const th = (TH[i] + TH[i - 1]) / 2, ph = A * Math.sin(w * th), dph = A * w * Math.cos(w * th);
      S[i] = S[i - 1] + Math.sqrt(Math.cos(ph) ** 2 + dph * dph) * (TAU / NS);
    }
    const s0 = S[NS / 2];
    for (let i = 0; i <= NS; i++) S[i] -= s0;
    const scale = wedge / (S[NS] - S[0]);              // tiny correction so the ends land exactly on +-wedge/2
    for (let i = 0; i <= NS; i++) S[i] *= scale;
    return {
      kind: "ruffle", wedge, amplitude: A, waves: w,
      dir(s, o) {
        let lo2 = 0, hi2 = NS;
        if (s <= S[0]) hi2 = 1; else if (s >= S[NS]) lo2 = NS - 1;
        else while (hi2 - lo2 > 1) { const md = (lo2 + hi2) >> 1; if (S[md] <= s) lo2 = md; else hi2 = md; }
        const f = Math.max(0, Math.min(1, (s - S[lo2]) / (S[hi2] - S[lo2] || 1)));
        const th = TH[lo2] + f * (TH[hi2] - TH[lo2]), ph = A * Math.sin(w * th), cp = Math.cos(ph);
        o[0] = cp * Math.sin(th); o[1] = -cp * Math.cos(th); o[2] = Math.sin(ph);
        return o;
      },
      frame(s, o, nn) {
        const e = 1e-4, a = [0, 0, 0], b = [0, 0, 0];
        this.dir(s, o); this.dir(s - e, a); this.dir(s + e, b);
        const t0 = b[0] - a[0], t1 = b[1] - a[1], t2 = b[2] - a[2];
        let x = o[1] * t2 - o[2] * t1, y = o[2] * t0 - o[0] * t2, z = o[0] * t1 - o[1] * t0; const l = Math.hypot(x, y, z) || 1;
        nn[0] = x / l; nn[1] = y / l; nn[2] = z / l;
      },
    };
  }

  // ---------- GL plumbing ----------
  function compile(gl, vs, fs) {
    const mk = (type, src) => {
      const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
      return s;
    };
    const p = gl.createProgram();
    gl.attachShader(p, mk(gl.VERTEX_SHADER, vs)); gl.attachShader(p, mk(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
    return p;
  }
  const VS_PT = `attribute vec3 aPos; attribute vec3 aCol; uniform mat4 uMVP; uniform float uSize; uniform float uRef; uniform vec3 uEye; uniform float uLift;
    varying vec3 vCol; void main(){ vec3 p = aPos + normalize(uEye - aPos) * uLift; gl_Position = uMVP * vec4(p, 1.0); gl_PointSize = clamp(uSize * uRef / gl_Position.w, 1.0, 64.0); vCol = aCol; }`;
  const FS_PT = `precision mediump float; varying vec3 vCol; uniform float uRound;
    void main(){ vec2 d = gl_PointCoord - 0.5; if (uRound > 0.5 && dot(d, d) > 0.25) discard; gl_FragColor = vec4(vCol, 1.0); }`;
  const VS_LN = `attribute vec3 aPos; attribute vec3 aCol; uniform mat4 uMVP; uniform vec3 uEye; uniform float uLift; varying vec3 vCol;
    void main(){ vec3 p = aPos + normalize(uEye - aPos) * uLift; gl_Position = uMVP * vec4(p, 1.0); vCol = aCol; }`;
  const FS_LN = `precision mediump float; varying vec3 vCol; uniform float uAlpha; void main(){ gl_FragColor = vec4(vCol, uAlpha); }`;
  const VS_SF = `attribute vec3 aPos; attribute vec3 aNrm; uniform mat4 uMVP; uniform vec3 uEye; varying float vShade;
    void main(){ gl_Position = uMVP * vec4(aPos, 1.0); vec3 L = normalize(uEye - aPos); vShade = abs(dot(normalize(aNrm), L)); }`;
  const FS_SF = `precision mediump float; varying float vShade; uniform vec3 uDark; uniform vec3 uLit; uniform float uPick;
    void main(){ if (uPick > 0.5) { gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0); return; } gl_FragColor = vec4(mix(uDark, uLit, pow(vShade, 1.4)), 1.0); }`;

  class HornView {
    constructor(canvas, opts = {}) {
      this.canvas = canvas;
      this.opts = Object.assign({
        maxLayers: 800, colorOf: null, onHover: null, interactive: true, keepFitOnGrow: false,
        body: "#0d1430", bodyLit: "#24305c", chainA: "#5e78c2", chainB: "#c4974c", seam: "#ecdfc0", half: "#9fb0ff",
        background: [0, 0, 0, 0], fov: 32, frameTop: 0, frameBottom: 0,
      }, opts);
      const gl = canvas.getContext("webgl", { antialias: true, alpha: true, premultipliedAlpha: true, preserveDrawingBuffer: false });
      if (!gl) throw new Error("WebGL is not available");
      this.gl = gl;
      this.p = { layers: 60, wedge: 1, unroll: 0, chains: true, marks: true, spin: false, pointScale: 1, roundPoints: true };
      this.cam = { yaw: 0, pitch: 0.12, zoom: 1, panX: 0, panY: 0 };
      this.progPt = compile(gl, VS_PT, FS_PT);
      this.progLn = compile(gl, VS_LN, FS_LN);
      this.progSf = compile(gl, VS_SF, FS_SF);
      this.buf = {};
      for (const k of ["ptPos", "ptCol", "ptId", "lnPos", "lnCol", "mkPos", "mkCol", "sfPos", "sfNrm"]) this.buf[k] = gl.createBuffer();
      this.colors = null; this.colorsFor = 0; this.shape = null; this._raf = 0; this._dirtyGeom = true;
      this._fbo = null; this._fboW = 0; this._fboH = 0;
      this._listeners = [];
      if (this.opts.interactive) this._bindInput();
      const onResize = () => this.resize();
      window.addEventListener("resize", onResize); this._listeners.push(["resize", onResize, window]);
      this.resize();
    }

    // ---------- public ----------
    set(o) {
      const before = Object.assign({}, this.p);
      Object.assign(this.p, o);
      this.p.layers = Math.max(1, Math.min(this.opts.maxLayers, Math.round(this.p.layers)));
      this.p.wedge = Math.max(0.05, this.p.wedge);
      this.p.unroll = this.p.wedge > TAU + 1e-9 ? 0 : Math.max(0, Math.min(1, this.p.unroll));
      if (before.layers !== this.p.layers) { this._dirtyGeom = true; if (!this.opts.keepFitOnGrow) this._fit = true; }
      if (before.wedge !== this.p.wedge || before.unroll !== this.p.unroll) { this._dirtyGeom = true; this._fit = true; }
      if (before.chains !== this.p.chains || before.marks !== this.p.marks) this._dirtyGeom = true;
      if (this.p.spin && !before.spin) this._loop(); else this.requestDraw();
    }
    recolor() { this._recolorAll = true; this.requestDraw(); }
    // keep the shape clear of overlays: fractions of the canvas height reserved at the top and bottom
    setFrame(top, bottom) { this.opts.frameTop = Math.max(0, top || 0); this.opts.frameBottom = Math.max(0, bottom || 0); this._fit = true; this.requestDraw(); }
    resetView() { this.cam = { yaw: 0, pitch: 0.12, zoom: 1, panX: 0, panY: 0 }; this.requestDraw(); }
    resize() {
      const dpr = Math.min(2, window.devicePixelRatio || 1), c = this.canvas;
      const w = Math.max(1, Math.round(c.clientWidth * dpr)), h = Math.max(1, Math.round(c.clientHeight * dpr));
      if (c.width !== w || c.height !== h) { c.width = w; c.height = h; this._fit = true; }
      this.requestDraw();
    }
    info() { this._shapeNow(); return { layers: this.p.layers, wedge: this.p.wedge, unroll: this.p.unroll, shape: this.shape && this.shape.kind,
      halfAngleDeg: this.shape && this.shape.halfAngle !== undefined ? (this.shape.halfAngle * 180) / Math.PI : null,
      ruffleAmplitudeDeg: this.shape && this.shape.amplitude !== undefined ? (this.shape.amplitude * 180) / Math.PI : null }; }
    destroy() {
      cancelAnimationFrame(this._raf);
      for (const [t, f, el] of this._listeners) el.removeEventListener(t, f);
    }
    // exact tick position (no outward offset), for tests
    tickPos(m, k) { const s = this._shapeNow(), o = [0, 0, 0]; s.dir(this.p.wedge * (k / m - 0.5), o); return [o[0] * m, o[1] * m, o[2] * m]; }

    // ---------- geometry ----------
    _shapeNow() {
      if (!this.shape || this.shape.wedge !== this.p.wedge || this._shapeUnroll !== this.p.unroll) {
        this.shape = makeShape(this.p.wedge, this.p.unroll); this._shapeUnroll = this.p.unroll;
      }
      return this.shape;
    }
    // GPU storage grows in steps; a landing layer only computes and uploads its own ticks and lines.
    // Valid prefixes: _posM (positions, per shape), _lnM (lines, per shape), _colM (colors, per coloring), and the same on the GPU.
    _capacity(M) {
      const gl = this.gl;
      if (this._capM >= M) return;
      let cap = Math.max(64, this._capM || 0);
      while (cap < M) cap = Math.ceil(cap * 1.5);
      cap = Math.max(M, Math.min(cap, Math.max(M, this.opts.maxLayers)));
      const Nc = (cap * (cap + 1)) / 2, Lc = segCount(cap);
      const alloc = (name, bytes) => { gl.bindBuffer(gl.ARRAY_BUFFER, this.buf[name]); gl.bufferData(gl.ARRAY_BUFFER, bytes, gl.DYNAMIC_DRAW); };
      alloc("ptPos", Nc * 12); alloc("ptCol", Nc * 12); alloc("lnPos", Lc * 24);
      const ids = new Float32Array(Nc * 3);                        // picking colors: id + 1 as 24-bit RGB (id = x - 1)
      for (let j = 0; j < Nc; j++) { const v = j + 1; ids[3 * j] = (v & 255) / 255; ids[3 * j + 1] = ((v >> 8) & 255) / 255; ids[3 * j + 2] = ((v >> 16) & 255) / 255; }
      gl.bindBuffer(gl.ARRAY_BUFFER, this.buf.ptId); gl.bufferData(gl.ARRAY_BUFFER, ids, gl.STATIC_DRAW);
      const lc = new Float32Array(Lc * 6), ca = parseColor(this.opts.chainA), cb = parseColor(this.opts.chainB);
      for (let m = 1, r = 0; m < cap; m++) for (let k = 1; k <= m; k++) {
        if (2 * k === m) continue;
        const c = 2 * k < m ? ca : cb;
        lc[r] = c[0]; lc[r + 1] = c[1]; lc[r + 2] = c[2]; lc[r + 3] = c[0]; lc[r + 4] = c[1]; lc[r + 5] = c[2]; r += 6;
      }
      gl.bindBuffer(gl.ARRAY_BUFFER, this.buf.lnCol); gl.bufferData(gl.ARRAY_BUFFER, lc, gl.STATIC_DRAW);
      const grow = (a, n) => { const b = new Float32Array(n); if (a) b.set(a.subarray(0, Math.min(a.length, n))); return b; };
      this.pos = grow(this.pos, Nc * 3); this._lp = grow(this._lp, Lc * 6); this.colors = grow(this.colors, Nc * 3);
      this._capM = cap; this._gpuPosM = 0; this._gpuLnM = 0; this._gpuColM = 0;   // fresh GPU storage: everything goes up again
    }
    _sub(name, data, from, to) {                                   // upload floats [from, to) of a CPU array
      if (to <= from) return;
      const gl = this.gl; gl.bindBuffer(gl.ARRAY_BUFFER, this.buf[name]);
      gl.bufferSubData(gl.ARRAY_BUFFER, from * 4, data.subarray(from, to));
    }
    _build() {
      const gl = this.gl, M = this.p.layers, W = this.p.wedge, shp = this._shapeNow();
      const N = (M * (M + 1)) / 2, d = [0, 0, 0], nv = [0, 0, 0];
      this._capacity(M);
      const key = W + "|" + this.p.unroll;
      if (this._posKey !== key) { this._posKey = key; this._posM = 0; this._lnM = 0; this._gpuPosM = 0; this._gpuLnM = 0; }
      const pos = this.pos;
      const off = 0.08 * Math.min(1, W);              // lift dots and lines just off the body so they never z-fight it
      // ticks: only layers not yet placed for this shape
      for (let m = this._posM + 1, i = ((this._posM * (this._posM + 1)) / 2) * 3; m <= M; m++) for (let k = 1; k <= m; k++) {
        shp.frame(W * (k / m - 0.5), d, nv);
        pos[i++] = d[0] * m + nv[0] * off; pos[i++] = d[1] * m + nv[1] * off; pos[i++] = d[2] * m + nv[2] * off;
      }
      if (M > this._posM) this._posM = M;
      if (M > this._gpuPosM) { this._sub("ptPos", pos, ((this._gpuPosM * (this._gpuPosM + 1)) / 2) * 3, N * 3); this._gpuPosM = M; }
      let minX = Infinity, minY = Infinity, minZ = Infinity, maxX = -Infinity, maxY = -Infinity, maxZ = -Infinity;
      for (let j = 0; j < N * 3; j += 3) {
        const x = pos[j], y = pos[j + 1], z = pos[j + 2];
        if (x < minX) minX = x; if (x > maxX) maxX = x; if (y < minY) minY = y; if (y > maxY) maxY = y; if (z < minZ) minZ = z; if (z > maxZ) maxZ = z;
      }
      this.N = N;
      this.bbox = [minX, minY, minZ, maxX, maxY, maxZ];
      // chains: the same-angle neighbour one layer out (tick k on the first half of the turn, tick k+1 on the second)
      if (this.p.chains) {
        const lp = this._lp;
        for (let m = Math.max(1, this._lnM), q = segCount(Math.max(1, this._lnM)) * 6; m < M; m++) {
          const base = ((m - 1) * m) / 2, nb = (m * (m + 1)) / 2;
          for (let k = 1; k <= m; k++) {
            if (2 * k === m) continue;
            const a = 3 * (base + k - 1), b = 3 * (2 * k < m ? nb + k - 1 : nb + k);
            lp[q] = pos[a]; lp[q + 1] = pos[a + 1]; lp[q + 2] = pos[a + 2];
            lp[q + 3] = pos[b]; lp[q + 4] = pos[b + 1]; lp[q + 5] = pos[b + 2]; q += 6;
          }
        }
        if (M > this._lnM) this._lnM = M;
        if (M > this._gpuLnM) { this._sub("lnPos", lp, segCount(Math.max(1, this._gpuLnM)) * 6, segCount(M) * 6); this._gpuLnM = M; }
        this.nChain = segCount(M);
      } else this.nChain = 0;
      const nrmAt = (s) => { const nn = [0, 0, 0]; shp.frame(s, d, nn); return nn; };
      // marks: the seam (both edges when slit open) and the half-turn line
      {
        const R = M + 2, mk = [], mc = [], cs = parseColor(this.opts.seam), ch = parseColor(this.opts.half);
        const line = (s, col) => { const n0 = nrmAt(s); shp.dir(s, d); mk.push(n0[0] * off * 2, n0[1] * off * 2, n0[2] * off * 2, d[0] * R + n0[0] * off * 2, d[1] * R + n0[1] * off * 2, d[2] * R + n0[2] * off * 2); mc.push(...col, ...col); };
        line(W / 2, cs); if (shp.kind !== "cone" && shp.kind !== "ruffle" && shp.kind !== "flat") line(-W / 2, cs);
        line(0, ch);
        this.nMark = mk.length / 3;
        gl.bindBuffer(gl.ARRAY_BUFFER, this.buf.mkPos); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(mk), gl.DYNAMIC_DRAW);
        gl.bindBuffer(gl.ARRAY_BUFFER, this.buf.mkCol); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(mc), gl.DYNAMIC_DRAW);
        this.labelAnchors = { seam: (shp.dir(W / 2, d), [d[0] * (R + 1.5), d[1] * (R + 1.5), d[2] * (R + 1.5)]),
          half: (shp.dir(0, d), [d[0] * (R + 1.5), d[1] * (R + 1.5), d[2] * (R + 1.5)]), seamN: nrmAt(W / 2), halfN: nrmAt(0) };
      }
      // the body: a fan of thin triangles from the tip (a cone over the curve is ruled by straight generators)
      {
        const SEG = shp.kind === "ruffle" ? 1440 : 720, R = M + 0.6, sp = new Float32Array(SEG * 9), sn = new Float32Array(SEG * 9);
        let px = 0, py = 0, pz = 0, nx = 0, ny = 0, nz = 0;
        for (let j = 0, q = 0; j <= SEG; j++) {
          const n2 = nrmAt(-W / 2 + (W * j) / SEG), X2 = d[0] * R, Y2 = d[1] * R, Z2 = d[2] * R;
          if (j) {
            const t = norm([nx + n2[0], ny + n2[1], nz + n2[2]]);
            sp.set([0, 0, 0, px, py, pz, X2, Y2, Z2], q); sn.set([t[0], t[1], t[2], nx, ny, nz, n2[0], n2[1], n2[2]], q); q += 9;
          }
          px = X2; py = Y2; pz = Z2; nx = n2[0]; ny = n2[1]; nz = n2[2];
        }
        this.nSurf = SEG * 3;
        gl.bindBuffer(gl.ARRAY_BUFFER, this.buf.sfPos); gl.bufferData(gl.ARRAY_BUFFER, sp, gl.DYNAMIC_DRAW);
        gl.bindBuffer(gl.ARRAY_BUFFER, this.buf.sfNrm); gl.bufferData(gl.ARRAY_BUFFER, sn, gl.DYNAMIC_DRAW);
      }
      this._dirtyGeom = false;
    }
    _ensureColors() {
      const M = this.p.layers, N = this.N;
      if (this._recolorAll) { this._colM = 0; this._gpuColM = 0; this._recolorAll = false; }
      const col = this.colors, f = this.opts.colorOf, cache = new Map();
      for (let m = (this._colM || 0) + 1, i = (((this._colM || 0) * ((this._colM || 0) + 1)) / 2) * 3; m <= M; m++) for (let k = 1; k <= m; k++) {
        const x = ((m - 1) * m) / 2 + k, c = f ? f(m, k, x) : "#dfe3f0";
        let rgb = cache.get(c); if (!rgb) { rgb = parseColor(c); cache.set(c, rgb); }
        col[i++] = rgb[0]; col[i++] = rgb[1]; col[i++] = rgb[2];
      }
      if (M > (this._colM || 0)) this._colM = M;
      if (M > (this._gpuColM || 0)) { this._sub("ptCol", col, (((this._gpuColM || 0) * ((this._gpuColM || 0) + 1)) / 2) * 3, N * 3); this._gpuColM = M; }
    }

    // ---------- camera ----------
    _matrices() {
      const c = this.canvas, aspect = c.width / c.height, f = (this.opts.fov * Math.PI) / 180;
      const [x0, y0, z0, x1, y1, z1] = this.bbox;
      const ctr = [(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2];
      const hx = (x1 - x0) / 2, hy = (y1 - y0) / 2, hz = (z1 - z0) / 2, rad = Math.hypot(hx, hy, hz);
      const fT = this.opts.frameTop, fB = this.opts.frameBottom, usable = Math.max(0.3, 1 - fT - fB);
      if (this._fit || !this._dist0) {
        const t = Math.tan(f / 2), r2 = Math.max(Math.hypot(hx, hz), 1e-3);
        this._dist0 = Math.max(hy / (t * usable), r2 / (t * aspect)) * 1.08 + r2;
        this._fit = false;
      }
      const dist = this._dist0 / this.cam.zoom, cy = Math.cos(this.cam.pitch);
      const dir = [Math.sin(this.cam.yaw) * cy, Math.sin(this.cam.pitch), Math.cos(this.cam.yaw) * cy];
      // pan in the camera plane
      const right = norm(cross([0, 1, 0], dir)), up = cross(dir, right), k = dist * Math.tan(f / 2), py = this.cam.panY + (fT - fB);
      const at = [ctr[0] + (right[0] * this.cam.panX + up[0] * py) * k, ctr[1] + (right[1] * this.cam.panX + up[1] * py) * k, ctr[2] + (right[2] * this.cam.panX + up[2] * py) * k];
      const eye = [at[0] + dir[0] * dist, at[1] + dir[1] * dist, at[2] + dir[2] * dist];
      const P = mat4Persp(f, aspect, Math.max(0.05, dist - rad * 2.5), dist + rad * 2.5), V = mat4LookAt(eye, at, [0, 1, 0]);
      const pxPerUnit = c.height / 2 / (dist * Math.tan(f / 2));
      return { MVP: mat4Mul(P, V), eye, dist, pxPerUnit };
    }

    // ---------- drawing ----------
    requestDraw() { if (!this._raf) this._raf = requestAnimationFrame(() => { this._raf = 0; this.draw(); }); }
    _loop() {
      const step = () => {
        if (!this.p.spin) { this._spinRaf = 0; return; }
        if (!this._dragging) this.cam.yaw += 0.004;
        this.draw(); this._spinRaf = requestAnimationFrame(step);
      };
      if (!this._spinRaf) this._spinRaf = requestAnimationFrame(step);
    }
    _attrib(prog, name, buffer, size) {
      const gl = this.gl, loc = gl.getAttribLocation(prog, name);
      if (loc < 0) return;
      gl.bindBuffer(gl.ARRAY_BUFFER, buffer); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, size, gl.FLOAT, false, 0, 0);
    }
    _disableAttribs() { const gl = this.gl; for (let i = 0; i < 4; i++) gl.disableVertexAttribArray(i); }
    draw(pickMode) {
      const gl = this.gl;
      if (this._dirtyGeom) this._build();
      this._ensureColors();
      const { MVP, eye, dist, pxPerUnit } = this._matrices();
      this._last = { MVP, eye };
      const W = this.canvas.width, H = this.canvas.height;
      gl.viewport(0, 0, W, H);
      const bg = pickMode ? [0, 0, 0, 1] : this.opts.background;
      gl.clearColor(bg[0], bg[1], bg[2], bg[3]); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      gl.enable(gl.DEPTH_TEST); gl.depthFunc(gl.LEQUAL);
      // body
      gl.useProgram(this.progSf);
      gl.uniformMatrix4fv(gl.getUniformLocation(this.progSf, "uMVP"), false, MVP);
      gl.uniform3fv(gl.getUniformLocation(this.progSf, "uEye"), eye);
      gl.uniform3fv(gl.getUniformLocation(this.progSf, "uDark"), parseColor(this.opts.body));
      gl.uniform3fv(gl.getUniformLocation(this.progSf, "uLit"), parseColor(this.opts.bodyLit));
      gl.uniform1f(gl.getUniformLocation(this.progSf, "uPick"), pickMode ? 1 : 0);
      this._attrib(this.progSf, "aPos", this.buf.sfPos, 3); this._attrib(this.progSf, "aNrm", this.buf.sfNrm, 3);
      gl.enable(gl.POLYGON_OFFSET_FILL); gl.polygonOffset(2, 4);
      gl.drawArrays(gl.TRIANGLES, 0, this.nSurf);
      gl.disable(gl.POLYGON_OFFSET_FILL); this._disableAttribs();
      // chains and marks
      if (!pickMode) {
        gl.useProgram(this.progLn);
        gl.uniformMatrix4fv(gl.getUniformLocation(this.progLn, "uMVP"), false, MVP);
        gl.uniform3fv(gl.getUniformLocation(this.progLn, "uEye"), eye);
        gl.uniform1f(gl.getUniformLocation(this.progLn, "uLift"), 0.3 * Math.min(1, this.p.wedge));
        gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); gl.depthMask(false);
        if (this.p.chains && this.nChain) {
          gl.uniform1f(gl.getUniformLocation(this.progLn, "uAlpha"), Math.max(0.18, Math.min(0.6, 0.6 * Math.sqrt(70 / this.p.layers))));
          this._attrib(this.progLn, "aPos", this.buf.lnPos, 3); this._attrib(this.progLn, "aCol", this.buf.lnCol, 3);
          gl.drawArrays(gl.LINES, 0, this.nChain * 2); this._disableAttribs();
        }
        if (this.p.marks && this.nMark) {
          gl.uniform1f(gl.getUniformLocation(this.progLn, "uAlpha"), 0.9);
          this._attrib(this.progLn, "aPos", this.buf.mkPos, 3); this._attrib(this.progLn, "aCol", this.buf.mkCol, 3);
          gl.drawArrays(gl.LINES, 0, this.nMark); this._disableAttribs();
        }
        gl.depthMask(true); gl.disable(gl.BLEND);
      }
      // ticks
      gl.useProgram(this.progPt);
      gl.uniformMatrix4fv(gl.getUniformLocation(this.progPt, "uMVP"), false, MVP);
      const unitPx = pxPerUnit * Math.min(1, this.p.wedge);
      const size = Math.max(1.5, Math.min(18, unitPx * 0.62 * this.p.pointScale));
      gl.uniform1f(gl.getUniformLocation(this.progPt, "uSize"), pickMode ? Math.max(size, 6) : size);
      gl.uniform1f(gl.getUniformLocation(this.progPt, "uRef"), dist);
      gl.uniform3fv(gl.getUniformLocation(this.progPt, "uEye"), eye);
      gl.uniform1f(gl.getUniformLocation(this.progPt, "uLift"), 0.5 * Math.min(1, this.p.wedge));
      gl.uniform1f(gl.getUniformLocation(this.progPt, "uRound"), this.p.roundPoints && !pickMode ? 1 : 0);
      this._attrib(this.progPt, "aPos", this.buf.ptPos, 3); this._attrib(this.progPt, "aCol", pickMode ? this.buf.ptId : this.buf.ptCol, 3);
      gl.drawArrays(gl.POINTS, 0, this.N); this._disableAttribs();
      this._pointPx = size;
      if (!pickMode && this.onAfterDraw) this.onAfterDraw(this);
    }
    // project a world point to CSS pixels of the canvas (for labels); returns null when behind the camera
    project(p) {
      if (!this._last) return null;
      const M = this._last.MVP, x = p[0], y = p[1], z = p[2];
      const cx = M[0] * x + M[4] * y + M[8] * z + M[12], cy = M[1] * x + M[5] * y + M[9] * z + M[13], cw = M[3] * x + M[7] * y + M[11] * z + M[15];
      if (cw <= 0) return null;
      const r = this.canvas.getBoundingClientRect();
      return [(cx / cw * 0.5 + 0.5) * r.width, (1 - (cy / cw * 0.5 + 0.5)) * r.height];
    }
    facing(p, n) { if (!this._last) return true; const e = this._last.eye; return (e[0] - p[0]) * n[0] + (e[1] - p[1]) * n[1] + (e[2] - p[2]) * n[2] > 0; }

    // ---------- picking: render tick ids into an offscreen buffer and read one pixel ----------
    pick(clientX, clientY) {
      const gl = this.gl, c = this.canvas, r = c.getBoundingClientRect();
      const px = Math.round(((clientX - r.left) / r.width) * c.width), py = Math.round((1 - (clientY - r.top) / r.height) * c.height);
      if (px < 0 || py < 0 || px >= c.width || py >= c.height) return null;
      if (!this._fbo || this._fboW !== c.width || this._fboH !== c.height) {
        if (this._fbo) { gl.deleteFramebuffer(this._fbo); gl.deleteTexture(this._fboTex); gl.deleteRenderbuffer(this._fboDepth); }
        this._fbo = gl.createFramebuffer(); this._fboTex = gl.createTexture(); this._fboDepth = gl.createRenderbuffer();
        gl.bindTexture(gl.TEXTURE_2D, this._fboTex);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, c.width, c.height, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
        gl.bindRenderbuffer(gl.RENDERBUFFER, this._fboDepth); gl.renderbufferStorage(gl.RENDERBUFFER, gl.DEPTH_COMPONENT16, c.width, c.height);
        gl.bindFramebuffer(gl.FRAMEBUFFER, this._fbo);
        gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, this._fboTex, 0);
        gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.RENDERBUFFER, this._fboDepth);
        this._fboW = c.width; this._fboH = c.height;
      }
      gl.bindFramebuffer(gl.FRAMEBUFFER, this._fbo);
      const aa = gl.isEnabled(gl.SCISSOR_TEST);
      gl.enable(gl.SCISSOR_TEST);
      const R = Math.ceil((this._pointPx || 4) / 2) + 3;
      gl.scissor(Math.max(0, px - R), Math.max(0, py - R), 2 * R + 1, 2 * R + 1);
      this.draw(true);
      const x0 = Math.max(0, px - R), y0 = Math.max(0, py - R), w = Math.min(c.width - x0, 2 * R + 1), h = Math.min(c.height - y0, 2 * R + 1);
      const buf = new Uint8Array(w * h * 4);
      gl.readPixels(x0, y0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, buf);
      if (!aa) gl.disable(gl.SCISSOR_TEST);
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
      let best = null, bd = Infinity;
      for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
        const o = 4 * (j * w + i), id = buf[o] | (buf[o + 1] << 8) | (buf[o + 2] << 16);
        if (!id) continue;
        const dd = (x0 + i - px) ** 2 + (y0 + j - py) ** 2;
        if (dd < bd) { bd = dd; best = id; }
      }
      if (!best || best > this.N) return null;
      const x = best, m = Math.ceil((Math.sqrt(8 * x + 1) - 1) / 2), k = x - ((m - 1) * m) / 2;
      return { m, k, x };
    }

    // ---------- input: drag to turn, wheel or pinch to zoom, shift-drag or two fingers to pan, double-click to reset ----------
    _bindInput() {
      const c = this.canvas, ptrs = new Map();
      c.style.touchAction = "none";
      let last = null, pinch0 = null, hoverQueued = null, moved = false;
      const on = (t, f, el = c, o) => { el.addEventListener(t, f, o); this._listeners.push([t, f, el]); };
      on("pointerdown", (e) => {
        c.setPointerCapture(e.pointerId); ptrs.set(e.pointerId, [e.clientX, e.clientY]); moved = false;
        last = [e.clientX, e.clientY, e.shiftKey]; this._dragging = true;
        if (ptrs.size === 2) { const [a, b] = [...ptrs.values()]; pinch0 = { d: Math.hypot(a[0] - b[0], a[1] - b[1]), z: this.cam.zoom, mid: [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2], pan: [this.cam.panX, this.cam.panY] }; }
      });
      on("pointermove", (e) => {
        if (ptrs.has(e.pointerId)) {
          ptrs.set(e.pointerId, [e.clientX, e.clientY]);
          if (ptrs.size === 2 && pinch0) {
            const [a, b] = [...ptrs.values()], d = Math.hypot(a[0] - b[0], a[1] - b[1]), r = c.getBoundingClientRect();
            this.cam.zoom = Math.max(0.3, Math.min(40, pinch0.z * (d / Math.max(1, pinch0.d))));
            const mid = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
            this.cam.panX = pinch0.pan[0] - ((mid[0] - pinch0.mid[0]) / r.height) * 2 / this.cam.zoom;
            this.cam.panY = pinch0.pan[1] + ((mid[1] - pinch0.mid[1]) / r.height) * 2 / this.cam.zoom;
            moved = true; this.requestDraw(); return;
          }
          if (last) {
            const dx = e.clientX - last[0], dy = e.clientY - last[1], r = c.getBoundingClientRect();
            if (Math.abs(dx) + Math.abs(dy) > 2) moved = true;
            if (e.shiftKey || e.buttons === 2) { this.cam.panX -= (dx / r.height) * 2 / this.cam.zoom; this.cam.panY += (dy / r.height) * 2 / this.cam.zoom; }
            else { this.cam.yaw -= dx * 0.008; this.cam.pitch = Math.max(-1.45, Math.min(1.45, this.cam.pitch + dy * 0.006)); }
            last = [e.clientX, e.clientY]; this.requestDraw();
          }
          return;
        }
        if (this.opts.onHover && e.pointerType === "mouse") {
          hoverQueued = [e.clientX, e.clientY];
          if (!this._hoverRaf) this._hoverRaf = requestAnimationFrame(() => { this._hoverRaf = 0; const h = hoverQueued; this.opts.onHover(this.pick(h[0], h[1]), h); });
        }
      });
      const up = (e) => {
        ptrs.delete(e.pointerId); if (ptrs.size < 2) pinch0 = null;
        if (!ptrs.size) {
          this._dragging = false;
          if (!moved && this.opts.onHover) this.opts.onHover(this.pick(e.clientX, e.clientY), [e.clientX, e.clientY], true);
          last = null;
        }
      };
      on("pointerup", up); on("pointercancel", up);
      on("contextmenu", (e) => e.preventDefault());
      on("wheel", (e) => { e.preventDefault(); this.cam.zoom = Math.max(0.3, Math.min(40, this.cam.zoom * Math.exp(-e.deltaY * 0.0015))); this.requestDraw(); }, c, { passive: false });
      on("dblclick", () => this.resetView());
    }
  }
  HornView.makeShape = makeShape;
  HornView.TAU = TAU;
  global.HornView = HornView;
})(typeof window !== "undefined" ? window : globalThis);
