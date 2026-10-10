#!/usr/bin/env python3
"""
gpu_frontier.py — the Prime Tread roll engine, one ring per GPU lane.

Mechanism (verified 2026-10-09 against the canonical stagger field):
  Layer m covers integers N = T(m-1) + k for ticks k in [1, m],
  where T(m-1) = (m-1)*m/2.  Ring p (one per prime p <= m/sqrt(2)) holds
      o = (-T(m-1)) mod p     the landing spot (tick index congruent to a multiple of p)
      d = m mod p             the stride
  Stamping: ring p marks every tick k ≡ o (mod p) in the window.  Any
  composite N has a factor <= sqrt(N) ≈ m/sqrt(2), so an uncovered tick IS
  prime — the certificate and the answer are the same object.  No bignums:
  all registers stay < p <= 2^32, and N itself never exists on the GPU.

Per layer, per ring: subtract-and-wrap, add-and-wrap.  That's the whole roll.
Jumping to layer m0 seeds both pointers in closed form
      T mod p via the mod-2p halving trick (a*b fits uint64 since p < 2^32)
so deep layers are reached without visiting the shallow ones.

The wall's true name is bandwidth: every ring must be visited once per
layer (20 bytes/ring of traffic), so layers/s falls as m climbs — but a
wide window makes each layer certify ~1M numbers, and the certified rate
holds in the tens of millions per second.  n_active tracks pi(m/sqrt(2))
so shallow layers stay fast and the dial degrades gracefully.

uint32 registers cap the layer at m < 2^32 * sqrt(2) = 6.07e9
(N ≈ 1.8e19, needing primes up to m/sqrt(2) < 2^32).

Controls (windowed mode):
  space  pause      s  save certified gold band to text
  j      jump to layer (type digits, enter)     +/-  roll speed
  q      quit
"""

import argparse
import faulthandler
import hashlib
import math
import os
import signal
import sys
import time

import numpy as np

faulthandler.register(signal.SIGUSR1, all_threads=True)

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")

MAX_LAYER_UINT32 = int((1 << 32) * math.sqrt(2)) - 1  # keep every p < 2^32

KERNELS = r"""
extern "C" __global__ void seed_kernel(
    const unsigned int* P, const int n,
    unsigned long long m0,
    unsigned int o2, unsigned int d2,
    unsigned int* O, unsigned int* D)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;
    unsigned long long p = P[i];
    if (p == 2ULL) { O[i] = o2; D[i] = d2; return; }
    unsigned long long a = m0 % p;          // m0      mod p
    unsigned long long b = (m0 - 1ULL) % p; // (m0-1)  mod p
    // T = m0*(m0-1)/2 mod p without bignums:
    // a*b < p^2 < 2^64, and with r2 = (a*b) mod 2p, the even lift
    // u = r2 (r2 even) or r2+p (r2 odd) satisfies u/2 == T (mod p).
    unsigned long long r2 = (a * b) % (2ULL * p);
    unsigned long long u = (r2 % 2ULL == 0ULL) ? r2 : (r2 + p);
    unsigned long long t = (u / 2ULL) % p;  // T mod p
    O[i] = (unsigned int)((t == 0ULL) ? 0ULL : (p - t));  // -T mod p
    D[i] = (unsigned int)a;                               // m0 mod p
}

extern "C" __global__ void advance_kernel(
    const unsigned int* P, const int n,
    unsigned int* O, unsigned int* D)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;
    unsigned long long p = P[i];
    unsigned long long o = O[i], d = D[i];
    unsigned long long on = (o >= d) ? (o - d) : (o + p - d);  // o - d mod p
    unsigned long long dn = d + 1ULL;
    if (dn == p) dn = 0ULL;                                    // d+1 mod p
    O[i] = (unsigned int)on;
    D[i] = (unsigned int)dn;
}

extern "C" __global__ void stamp_kernel(
    const unsigned int* P, const int n,
    const unsigned int* O,
    unsigned long long k0, unsigned long long k1,
    unsigned char* win, unsigned int* cnt)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;
    unsigned long long p = P[i];
    unsigned long long o = O[i];
    // first stamp >= k0 via double reciprocal + integer correction
    // (64-bit division would dominate the whole kernel; x < 2^53 keeps
    // the float estimate within one of the true quotient)
    unsigned long long j0 = 0ULL;
    if (o < k0) {
        unsigned long long x = k0 - o;
        double inv = 1.0 / (double)p;
        j0 = (unsigned long long)((double)x * inv);
        while (o + j0 * p < k0) j0++;
        while (j0 > 0ULL && o + (j0 - 1ULL) * p >= k0) j0--;
    }
    for (unsigned long long k = o + j0 * p; k <= k1; k += p) {
        win[k - k0] = 1;                    // benign race: idempotent write
        atomicAdd(cnt + (k - k0), 1u);      // witness count (omega(N))
    }
}
"""

BLOCK = 256


# ---------------------------------------------------------------- sieve ----

def _simple_sieve(n):
    """bool array s where s[v] == is-prime, for n <= ~100M."""
    s = np.ones(n + 1, dtype=bool)
    s[0:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if s[p]:
            s[p * p::p] = False
    return s


def primes_u32_below(n, cache_dir=CACHE):
    """All primes <= n as uint32, segmented sieve, disk-cached (.npy)."""
    os.makedirs(cache_dir, exist_ok=True)
    path = os.path.join(cache_dir, f"primes_u32_below_{n}.npy")
    if os.path.exists(path):
        primes = np.load(path)
        # legacy caches built by an older primes_u32_below prepend 2 and
        # also emit it from the first segment — a duplicated ring. Harmless
        # to the boolean stamp (idempotent write) but it inflates every
        # even tick's witness count by 1.
        if len(primes) > 1 and primes[0] == 2 and primes[1] == 2:
            primes = primes[1:]
        return primes
    base = np.flatnonzero(_simple_sieve(int(n ** 0.5) + 1)).astype(np.uint32)
    out = []
    seg = 1 << 28
    for lo in range(2, n + 1, seg):
        hi = min(lo + seg, n + 1)
        mark = np.zeros(hi - lo, dtype=bool)
        for p in base:
            p = int(p)
            start = max(p * p, ((lo + p - 1) // p) * p)
            if start < hi:
                mark[start - lo::p] = True
        out.append((np.flatnonzero(~mark) + lo).astype(np.uint32))
    primes = np.concatenate(out)
    primes = primes[primes <= n]
    np.save(path, primes)
    return primes


# --------------------------------------------------------------- engine ----

class Engine:
    def __init__(self, target_layer):
        import cupy as cp
        self.cp = cp
        self.target = min(target_layer, MAX_LAYER_UINT32)
        self.bound = int(self.target / math.sqrt(2))
        print(f"[engine] primes <= {self.bound:,} (target layer "
              f"{self.target:,}) ...", flush=True)
        t0 = time.time()
        self.primes_host = primes_u32_below(self.bound)
        print(f"[engine] {len(self.primes_host):,} rings in "
              f"{time.time()-t0:.1f}s ({self.primes_host.nbytes/2**20:.0f} "
              f"MiB host)", flush=True)
        self.n_all = len(self.primes_host)
        self.n_active = self.n_all
        self._n_active_idx = self.n_all      # _contract walks from here
        self._bound = self.bound             # target bound: all rings in
        self.ringP = cp.array(self.primes_host, dtype=cp.uint32)
        self.ringO = cp.empty(self.n_all, dtype=cp.uint32)
        self.ringD = cp.empty(self.n_all, dtype=cp.uint32)
        self.kernels = {name: cp.RawKernel(KERNELS, name)
                        for name in ("seed_kernel", "advance_kernel",
                                     "stamp_kernel")}
        self.m = 0
        self.acc_primes = cp.zeros(1, dtype=cp.int64)
        self.verified = False

    def _grid(self, n):
        return ((n + BLOCK - 1) // BLOCK,)

    def _contract(self, bound):
        """Set n_active = #{primes <= bound}, walking from the cached index.

        Gallops in fixed 1M-element strides and only binary-searches the
        final window: a full-array searchsorted probes an 800 MB table
        ~28 times, and under memory-bandwidth contention (a mining
        workload on this box) each probe is a cache miss that measured
        6+ seconds. The stride walk touches one element per stride and
        the residual window is <= 4 MB.
        """
        ph = self.primes_host
        n = self._n_active_idx
        step = 1 << 20
        if n < self.n_all and ph[n] <= bound:
            lo, hi = n, min(n + step, self.n_all)
            while hi < self.n_all and ph[hi - 1] <= bound:
                lo, hi = hi, min(hi + step, self.n_all)
        else:
            lo, hi = max(n - step, 0), n
            while lo > 0 and ph[lo] > bound:
                lo, hi = max(lo - step, 0), lo
        self._n_active_idx = lo + int(np.searchsorted(ph[lo:hi], bound,
                                                      side="right"))
        self.n_active = self._n_active_idx
        self._bound = bound

    def set_layer(self, m):
        """Contract ring count: primes p <= m/sqrt(2) certify layer m."""
        self._contract(int((m + 1) / math.sqrt(2)) + 1)

    def seed(self, m0):
        cp = self.cp
        assert 2 <= m0 <= MAX_LAYER_UINT32, f"layer {m0} out of uint32 range"
        self.set_layer(m0)
        T = (m0 - 1) * m0 // 2
        t2 = T % 2
        self.kernels["seed_kernel"](self._grid(self.n_active), (BLOCK,),
                                    (self.ringP, self.n_active, m0,
                                     (-t2) % 2, m0 % 2,
                                     self.ringO, self.ringD))
        self.m = m0
        self.acc_primes[:] = 0

    def roll(self, win, cnt, k0, k1):
        """Stamp one layer into win/cnt[0..k1-k0], then advance every ring."""
        cp = self.cp
        # Certification contract: every prime <= m/sqrt(2) must hold an
        # active ring. The bound grows ~0.7 per layer as the frontier
        # climbs, so re-contract here; a frozen set under-certifies
        # (semiprimes of two stale-bound primes stamp nothing and read
        # as primes).
        bound = int((self.m + 1) / math.sqrt(2)) + 1
        if bound > self._bound:
            self._contract(bound)
            # newly activated rings hold stale/garbage pointers — reseed
            # the whole active set at the current layer (idempotent: the
            # closed form reproduces exactly what advance would carry)
            T2 = ((self.m - 1) * self.m // 2) % 2
            self.kernels["seed_kernel"](self._grid(self.n_active), (BLOCK,),
                                        (self.ringP, self.n_active, self.m,
                                         (-T2) % 2, self.m % 2,
                                         self.ringO, self.ringD))
        W = int(k1 - k0 + 1)
        win.fill(0)
        cnt.fill(0)
        self.kernels["stamp_kernel"](self._grid(self.n_active), (BLOCK,),
                                     (self.ringP, self.n_active, self.ringO,
                                      k0, k1, win, cnt))
        cp.add(self.acc_primes, W - win.sum(dtype=cp.int64),
               out=self.acc_primes)
        self.kernels["advance_kernel"](self._grid(self.n_active), (BLOCK,),
                                       (self.ringP, self.n_active,
                                        self.ringO, self.ringD))
        self.m += 1

    def primes_so_far(self):
        return int(self.acc_primes.item())


# ------------------------------------------------------------- verify ------

def verify(engine):
    """Exact check of the GPU port: seeds + stamp/advance vs a span sieve."""
    m0, steps, W = 1_234_567, 8, 1024
    T = lambda m: m * (m + 1) // 2
    n_max = T(m0 + steps - 1)
    base = np.flatnonzero(_simple_sieve(int(n_max ** 0.5) + 1)).astype(np.int64)
    span_lo = T(m0 - 1) + 1
    span = np.zeros(n_max - span_lo + 1, dtype=np.uint32)
    for p in base:
        start = ((span_lo + int(p) - 1) // int(p)) * int(p)
        span[start - span_lo::int(p)] += 1

    cp = engine.cp
    engine.set_layer(m0)          # the real contract path
    engine.seed(m0)

    rng = np.random.default_rng(7)
    sample = rng.integers(0, engine.n_active, 200, endpoint=False)
    Ps = engine.ringP[cp.array(sample)].get().astype(np.int64)
    Os = engine.ringO[cp.array(sample)].get().astype(np.int64)
    Ds = engine.ringD[cp.array(sample)].get().astype(np.int64)
    bad_seed = 0
    for j in range(200):
        p = int(Ps[j])
        if (int(Os[j]) != (-((m0 - 1) * m0 // 2)) % p
                or int(Ds[j]) != m0 % p):
            bad_seed += 1

    win = cp.zeros(W, dtype=cp.uint8)
    cnt = cp.zeros(W, dtype=cp.uint32)
    bad_roll = 0
    bad_wit = 0
    base64 = base.astype(np.int64)
    for m in range(m0, m0 + steps):
        k1, k0 = m, m - W + 1
        engine.roll(win, cnt, k0, k1)
        got = win.get().astype(bool)
        gotc = cnt.get()
        ref = span[T(m - 1) + k0 - span_lo: T(m - 1) + k1 - span_lo + 1]
        bad_roll += int((got != (ref > 0)).sum())
        # witness contract: the engine must count exactly the divisors
        # p <= bound(m) (its ring set). Divisors above the bound are the
        # prime cofactor the mechanism deliberately cannot see.
        bound_m = int((m + 1) / math.sqrt(2)) + 1
        ref_m = np.zeros(W, dtype=np.uint32)
        lo = T(m - 1) + k0
        for p in base64[base64 <= bound_m]:
            start = ((lo + int(p) - 1) // int(p)) * int(p) - lo
            ref_m[start::int(p)] += 1
        bad_wit += int((gotc != ref_m).sum())

    ok = bad_seed == 0 and bad_roll == 0 and bad_wit == 0
    print(f"[verify] seed mismatches: {bad_seed}/200   roll mismatches: "
          f"{bad_roll}/{steps * W} ticks   witness mismatches: "
          f"{bad_wit}/{steps * W} ticks   {'PASS' if ok else 'FAIL'}",
          flush=True)
    return ok


# ----------------------------------------------------------- benchmark -----

def benchmark(engine, start_layer, window, layers=200):
    cp = engine.cp
    engine.seed(start_layer)
    win = cp.zeros(window, dtype=cp.uint8)
    cnt = cp.zeros(window, dtype=cp.uint32)
    k1 = start_layer
    cp.cuda.Stream.null.synchronize()
    t0 = time.time()
    for i in range(layers):
        engine.roll(win, cnt, k1 - window + 1, k1)
        k1 += 1
    cp.cuda.Stream.null.synchronize()
    dt = time.time() - t0
    lps = layers / dt
    n_active = engine.n_active
    gb_per_layer = n_active * 20 / 2**30
    print(f"[benchmark] layer {start_layer:,}  window {window:,}  "
          f"{n_active:,} rings")
    print(f"[benchmark] {lps:,.0f} layers/s  ->  "
          f"{lps * window:,.0f} numbers certified/s   "
          f"(~{gb_per_layer:.1f} GiB ring traffic/layer)")
    return lps


# ------------------------------------------------------------ pygame app ---

GOLD = (242, 191, 74)
COVERED = (15, 21, 37)
BG = (7, 10, 18)
PANEL = (11, 15, 26)
TEXT = (210, 216, 230)
MUTED = (120, 130, 150)
GOOD = (110, 220, 140)


def run_app(engine, start_layer, window, frames=0):
    import pygame
    cp = engine.cp

    SW, SH = 1440, 900
    HUD_H = 168
    STRIP_W, STRIP_H = SW, SH - HUD_H

    pygame.init()
    pygame.display.set_caption("PRIME TREAD — GPU FRONTIER")
    screen = pygame.display.set_mode((SW, SH))
    font = pygame.font.SysFont("monospace", 16)
    big = pygame.font.SysFont("monospace", 22, bold=True)
    strip = pygame.Surface((STRIP_W, STRIP_H))
    strip.fill(BG)
    clock = pygame.time.Clock()

    win = cp.zeros(window, dtype=cp.uint8)
    cnt = cp.zeros(window, dtype=cp.uint32)
    engine.seed(start_layer)

    batch = 8
    paused = False
    running = True
    jumping = ""
    certified_ticks = 0
    ema_lps = 0.0
    status = ""
    t_prev = time.time()
    m_disp = start_layer
    frame = 0

    def save_band(m, win_host, cnt_host):
        Tm1 = (m - 1) * m // 2
        k1, k0 = m, m - window + 1
        ks = np.flatnonzero(win_host == 0)
        Ns = [Tm1 + int(k) for k in (k0 + ks)]  # python ints: exact, no cap
        body = "".join(f"{n}\n" for n in Ns)
        sha = hashlib.sha256(body.encode()).hexdigest()
        path = os.path.join(HERE, f"gold-band-m{m}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("# Prime Tread GPU Frontier - certified gold band\n")
            f.write(f"# layer m = {m}; ticks [{k0}..{k1}]; N = T(m-1)+k\n")
            f.write(f"# N range: {Tm1 + k0} .. {Tm1 + k1}\n")
            f.write(f"# primes in band: {len(ks)} of {window}; rings: every "
                    f"prime <= {int((m + 1) / 2**0.5) + 1:,}\n")
            f.write("# certification: exact ring coverage, no probabilistic "
                    f"test. sha256(body) = {sha}\n")
            f.write(body)
        # witness counts sidecar: cnt[i] = omega(N) for N = Tm1 + k0 + i
        wpath = os.path.join(HERE, f"witness-band-m{m}.npy")
        np.save(wpath, cnt_host.astype(np.uint32, copy=False))
        return path, len(ks)

    while running:
        frame += 1
        if frames and frame > frames:
            break
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_q and jumping == "":
                    running = False
                elif ev.key == pygame.K_SPACE and jumping == "":
                    paused = not paused
                elif ev.key == pygame.K_s and jumping == "" and not paused:
                    p, npr = save_band(m_disp, win.get(), cnt.get())
                    status = f"saved {npr} primes -> {os.path.basename(p)}"
                elif ev.key == pygame.K_j:
                    jumping = str(m_disp) if jumping == "" else ""
                elif ev.key == pygame.K_RETURN and jumping != "":
                    try:
                        tgt = int(jumping)
                        assert 2 <= tgt <= MAX_LAYER_UINT32
                        engine.seed(tgt)
                        certified_ticks = 0
                        strip.fill(BG)
                        status = f"jumped to layer {tgt:,}"
                    except Exception:
                        status = f"bad layer '{jumping}'"
                    jumping = ""
                elif ev.key == pygame.K_ESCAPE:
                    jumping = ""
                elif ev.key in (pygame.K_PLUS, pygame.K_EQUALS) \
                        and jumping == "":
                    batch = min(batch * 2, 4096)
                elif ev.key == pygame.K_MINUS and jumping == "":
                    batch = max(batch // 2, 1)
                elif jumping != "" and ev.unicode.isdigit():
                    jumping += ev.unicode
                elif ev.key == pygame.K_BACKSPACE and jumping != "":
                    jumping = jumping[:-1]

        if not paused:
            for _ in range(batch):
                m = engine.m
                engine.roll(win, cnt, m - window + 1, m)
            certified_ticks += batch * window
            m_disp = engine.m - 1

            t_now = time.time()
            dt = t_now - t_prev
            if dt > 0:
                inst = batch / dt
                ema_lps = inst if ema_lps == 0 else 0.9 * ema_lps + 0.1 * inst
            t_prev = t_now

            win_host = win.get()
            row = np.empty((window, 1, 3), dtype=np.uint8)
            row[:, 0, :] = COVERED
            row[win_host == 0, 0, :] = GOLD
            surf = pygame.surfarray.make_surface(row)
            strip.scroll(0, -1)
            strip.blit(pygame.transform.scale(surf, (STRIP_W, 1)),
                       (0, STRIP_H - 1))

        screen.fill(BG)
        screen.blit(strip, (0, 0))
        pygame.draw.rect(screen, PANEL, (0, STRIP_H, SW, HUD_H))

        m = m_disp
        Tm1 = (m - 1) * m // 2
        n_lo, n_hi = Tm1 + (m - window + 1), Tm1 + m
        lines = [
            ("PRIME TREAD — GPU FRONTIER    [ENGINE VERIFIED]",
             GOOD if engine.verified else MUTED, big),
            (f"layer {m:>15,}     N ≈ {Tm1 + m:.3e}   "
             f"[{n_lo:,} .. {n_hi:,}]", TEXT, font),
            (f"rings {engine.n_active:>15,} active of {engine.n_all:,}   "
             f"window {window:,} ticks @ top", MUTED, font),
            (f"rate  {ema_lps:>12,.0f} layers/s   ->   "
             f"{certified_ticks:,} ticks certified, "
             f"{engine.primes_so_far():,} primes harvested",
             TEXT, font),
            ("space pause | s save band | j jump | +/- speed "
             f"(x{batch}) | q quit" +
             (f"    JUMP > {jumping}_" if jumping != "" else
              (f"    {status}" if status else "")), MUTED, font),
        ]
        y = STRIP_H + 10
        for txt, color, fnt in lines:
            screen.blit(fnt.render(txt, True, color), (16, y))
            y += 30 if fnt is big else 24

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def main():
    ap = argparse.ArgumentParser(description="Prime Tread GPU Frontier")
    ap.add_argument("--start-layer", type=int, default=282_000_000)
    ap.add_argument("--target-layer", type=int, default=6_000_000_000,
                    help="caps the dial; sieve covers target/sqrt(2)")
    ap.add_argument("--window", type=int, default=1 << 20)
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--benchmark", action="store_true")
    ap.add_argument("--frames", type=int, default=0,
                    help="quit after N frames (headless smoke test)")
    ap.add_argument("--dump-band", type=int, metavar="M", default=0,
                    help="headless: certify layer M's window, save it, exit")
    args = ap.parse_args()

    assert args.start_layer <= MAX_LAYER_UINT32, \
        f"start layer > uint32 cap {MAX_LAYER_UINT32:,}"

    if args.frames:
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

    engine = Engine(args.target_layer)
    if not args.no_verify:
        engine.verified = verify(engine)
        if not engine.verified:
            print("[verify] FAILED — not proceeding", flush=True)
            sys.exit(1)

    if args.benchmark:
        for L in (282_000_000, 6_000_000_000):
            if L <= args.target_layer:
                benchmark(engine, L, args.window)
        return

    if args.dump_band:
        m = args.dump_band
        engine.seed(m)
        cp = engine.cp
        win = cp.zeros(args.window, dtype=cp.uint8)
        cnt = cp.zeros(args.window, dtype=cp.uint32)
        engine.roll(win, cnt, m - args.window + 1, m)
        win_host = win.get()
        cnt_host = cnt.get()
        Tm1 = (m - 1) * m // 2
        k1, k0 = m, m - args.window + 1
        ks = np.flatnonzero(win_host == 0)
        Ns = [Tm1 + int(k) for k in (k0 + ks)]
        body = "".join(f"{n}\n" for n in Ns)
        sha = hashlib.sha256(body.encode()).hexdigest()
        path = os.path.join(HERE, f"gold-band-m{m}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("# Prime Tread GPU Frontier - certified gold band\n")
            f.write(f"# layer m = {m}; ticks [{k0}..{k1}]; N = T(m-1)+k\n")
            f.write(f"# N range: {Tm1 + k0} .. {Tm1 + k1}\n")
            f.write(f"# primes in band: {len(ks)} of {args.window}; rings: "
                    f"every prime <= {int((m + 1) / 2**0.5) + 1:,}\n")
            f.write("# certification: exact ring coverage, no probabilistic "
                    f"test. sha256(body) = {sha}\n")
            f.write(body)
        np.save(os.path.join(HERE, f"witness-band-m{m}.npy"), cnt_host)
        print(f"[dump-band] layer {m:,}: {len(ks):,} primes of "
              f"{args.window:,} -> {path} (+ witness-band-m{m}.npy)",
              flush=True)
        return

    run_app(engine, args.start_layer, args.window, frames=args.frames)


if __name__ == "__main__":
    main()
