# Phase 0.6 — stamp kernel v2: size-split window-parallel prototype

Date: 2026-10-10. Prototype: `lab/p06_kernel_v2.py` (standalone, cupy; does
not touch `gpu_frontier.py`). Implements the Phase 0.5 recommendation:
split rings by prime size, give the small primes a window-parallel kernel,
keep the production per-ring kernel for the rest.

**Co-runner note (real this time):** the live pygame window (pid 19718,
python3, ~2.4 GiB) was confirmed present throughout (`nvidia-smi`: 91% GPU
util, 2,465 MiB used). All numbers below were measured **under contention**.
No process was signaled or killed; the probe used ~2 s of GPU time total.
Production-kernel numbers are therefore noisy (mean-of-7 with min reported);
v2 numbers are stable because the critical path is gone.

Shape: W = 1,048,576 window; own sieve of primes ≤ 2,000,000 (148,933
rings); rings seeded on host with the engine's exact closed form
(`seed_kernel` mod-2p even-lift; `advance_kernel` o−d/d+1 mod p), layer
m0 = 100,000, window [T+1, T+W] — same as the Phase 0.5 probe.

## Design

- **SMALL (p ≤ P_CUTOFF)** — `stamp_small`: one thread per tick
  (grid = W/256 blocks), each thread loops over the π(P_CUTOFF) small
  primes and tests `idx % p == (o − k0) mod p`. The modulo uses a
  precomputed magic multiplier `M = ceil(2^40/p)`,
  `q = (idx·M) >> 40`, exact for `idx < 2^20`, `p ≤ 2^16` (proved in the
  source header; branchless, no hardware divide, ~8 instructions per
  prime test). Writes are fully coalesced: `win[idx] = (nhits != 0)` and,
  when witnesses are on, `cnt[idx] = nhits` as a **plain store** — each
  tick is owned by exactly one thread, so this is bit-identical to the
  production `atomicAdd(cnt,1)` semantics *without* any atomics for the
  small set. Per-layer residues `R_i = (o_i − k0) mod p_i` are recomputed
  per layer (measured: 9–36 µs on host for π(C) up to 6,542 — negligible).
- **LARGE (p > P_CUTOFF)** — production `stamp_kernel` verbatim semantics
  (float-reciprocal j0 + integer correction), plus a `use_cnt` flag that
  drops the witness `atomicAdd` for the win-only variant.
- Kernel ordering per layer: `stamp_small` then `stamp_large` (same
  stream). The small kernel's plain `cnt` store must land before the large
  kernel's atomics; `win` writes are idempotent either way.

## Exact-match verification — **PASS**

Before any timing, both kernels ran on the same seeded state for **4
layers** (m = 100,000…100,003), at cutoffs **1024 and 8192**, comparing
against the verbatim production kernel. All layers, both variants:

```
cutoff 1024: layer m=100000..100003: win OK  cnt OK  win-only OK  PASS (x4)
cutoff 8192: layer m=100000..100003: win OK  cnt OK  win-only OK  PASS (x4)
```

`win` and `cnt` are bit-identical (`np.array_equal`) per layer; the win-only
variants additionally match production's win. Verification gates the
benchmark: any mismatch would have stopped the run.

## Benchmark (CUDA events, mean of 7 reps, 1 warmup, co-running pid 19718)

| kernel | variant | mean ms/layer | min ms/layer |
|---|---|---|---|
| production (verbatim per-ring) | witness | 18.15 / 19.25 (two runs) | 10.35 / 19.22 |
| production (verbatim per-ring) | win-only | 16.55–18.11 | 10.49–16.26 |
| **v2, P_CUTOFF = 1024** | **witness** | **0.77–0.81** | **0.76–0.78** |
| **v2, P_CUTOFF = 1024** | **win-only** | **0.62–0.63** | **0.61** |
| v2, P_CUTOFF = 8192 | witness | 3.24–4.74 | 2.38–4.70 |
| v2, P_CUTOFF = 8192 | win-only | 4.73–4.84 | 4.61–4.67 |
| — small kernel alone (1024) | witness | 0.397 | 0.390 |
| — large kernel alone (1024) | witness | 0.339 | 0.331 |

(First block from the dual-verification run, second block from the
single-verification run; both under the same co-runner.)

- **Speedup at the best cutoff (1024), witness: ~23–24×** vs the
  contended production kernel (18.2–19.3 ms → 0.77–0.81 ms).
- **Recovery of the Phase-0.5-measured 16.26 ms:** at 0.72 ms (sweep best)
  v2 leaves 4.4% of the old kernel time — **~95.6% recovered**
  (16.26 / 0.72 ≈ 22× vs the uncontended baseline).
- **Witness cost in v2 is ~0.15 ms/layer** (0.81 vs 0.63) — a coalesced
  store, no longer the ~50% additive tax, because the atomic was only
  expensive on the serial p=2 chain (see the reinterpretation below).

## P_CUTOFF sweep (v2, witness variant)

| P_CUTOFF | π(C) | ms/layer | host residue recompute |
|---:|---:|---:|---:|
| 64 | 18 | 1.042 | 12 µs |
| 128 | 31 | 0.841 | 12 µs |
| 256 | 54 | 0.717 | 9 µs |
| **1,024** | **172** | **0.716** | **11 µs** |
| 2,048 | 309 | 0.923 | 11 µs |
| 4,096 | 564 | 1.415 | 13 µs |
| 8,192 | 1,028 | 4.783 | 17 µs |
| 16,384 | 1,900 | 7.745 | 18 µs |
| 32,768 | 3,512 | 17.684 | 25 µs |
| 65,536 | 6,542 | 31.401 | 36 µs |

**Best: P_CUTOFF = 1,024 (π = 172), 0.716 ms/layer.** The optimum is a
broad plateau over 256–1,024 (0.72–0.84 ms). It falls off below 256
(large kernel re-acquires a serial tail: the smallest large prime's
single thread walks W/p ticks at ~15–17 ns each — at cutoff 64 the
p = 67..127 rings cost ~0.3–0.7 ms of chain) and rises above 1,024
(the small kernel's π(C)·W prime tests dominate; cost ∝ π(C)).

## Reinterpretation of the Phase 0.5 decomposition (important)

Phase 0.5 read its (b)/(c2) numbers as "scattered store ~2.9 ns + scattered
atomic ~2.7 ns, additive". The v2 decomposition shows that was really the
**p = 2 thread's serial chain** in every variant: 524,288 iterations at
~17 ns (win-only → 9.0 ms) or ~31 ns (witness → 16.3 ms) per iteration.
The machine's actual scattered-store throughput is far higher: the v2
large kernel performs ~0.88 M scattered stores + ~0.88 M scattered
atomics in 0.34 ms (**~0.4 ns/stamp** from 148k parallel threads, whole
1 MiB/4 MiB window L2-resident). So: the per-ring kernel's cost is
`max over rings of (W/p × per-iteration latency)`, dominated by the
smallest primes; issue rate was never the wall. This *strengthens* the
Phase 0.5 verdict — the fix is exactly the parallelism inversion, and the
payoff (~22–24×) exceeds the 5–15× estimate.

## Integration recommendation (flag-gated, into `gpu_frontier.py`)

1. Add `stamp_small` (source above) and a `use_cnt` flag on
   `stamp_kernel`; split at `n_small = searchsorted(primes_host,
   P_CUTOFF)` with `P_CUTOFF = 1024` (a constant; π = 172 rings is fixed
   for all layers, so the split index never changes at runtime).
2. Gate behind `--stamp-v2` (default off) with the existing `verify()`
   re-run as the gate for enabling it by default; keep the production
   kernel path one flag away.
3. Residues: compute `R_i = (O_i − k0) mod p_i` **on device** in
   `advance_kernel`'s wake (a tiny elementwise kernel over 172 rings, or
   fused into advance for the small prefix) instead of the host
   recompute — avoids a host round-trip and keeps the closed-form seed
   as the single source of truth. Prototype used host numpy (11 µs);
   either way it is negligible next to ~0.8 ms/layer.
4. Order per layer: `stamp_small` → `stamp_kernel(large)` on the same
   stream (small's plain `cnt` store must precede large's atomics).
5. Also expose the win-only flag (`use_cnt=0`) for non-verification
   rolling: saves ~0.15 ms/layer in v2 and halves the large kernel.

## Caveats

- **Magic-multiplier validity**: `q = (idx·ceil(2^40/p)) >> 40` is exact
  only for `idx < 2^20` and `p ≤ 2^16` (proved in the prototype header).
  Holds for W = 2^20 and any cutoff ≤ 65,536. If W ever grows to 2^n,
  re-derive with shift s = n + 24 and check `idx_max · ceil(2^s/3) < 2^64`
  (no overflow for n ≤ 24). The uint32 window cap already bounds n ≤ 32;
  above 2^24 use a 64-bit-safe or float-reciprocal variant and re-verify.
- **Per-layer recompute**: yes, the small-prime residues need one
  `(o − k0) mod p` pass per layer (o advances every layer, k0 changes
  every layer). O(π(C)) = 172 elementwise ops — 11 µs host, ~0 on device.
  Not a bottleneck; do it on device to avoid the sync.
- **Where window-parallel loses to per-ring**: marginal cost of moving
  prime p from the large set to the small set is ~W prime-tests
  (~8 inst each, p-independent); the marginal saving is ~W/p scattered
  stamps (~0.4 ns each, no chain once p is not the smallest large
  prime). Empirically the total crosses upward right after 1,024 and the
  plateau floor is 256–1,024; below 256 the large kernel's serial tail
  (new smallest prime p: W/p × ~15 ns chain) takes over. So the answer
  to "at what π(C) does window-parallel become slower than per-ring" is:
  as a *total-system* choice, anything in π ∈ [54, 172] is optimal at
  this W; the window-parallel loop in isolation stops paying for itself
  per-prime once the per-ring cost of that prime (≈ W/p × 0.8 ns) drops
  below ~W × 8 instructions — i.e. only for p below a few hundred, which
  is exactly the region where the *chain* argument forces window-parallel
  anyway. The two constraints pin the optimum together; 1024 is the
  measured sweet spot with margin on both sides.
- **Contention**: production numbers above are inflated/noisy by the
  co-running window (min 10.3, mean 18–19 ms). The 22× figure vs the
  uncontended Phase-0.5 16.26 ms is the more transferable one. Re-run
  `p06_kernel_v2.py` uncontended for a final clean comparison before
  merging.
- **Scale**: the prototype used 148,933 rings (m0 = 100,000). At
  production scale (11 M rings, larger m) the small set p ≤ 1024 is
  unchanged (172 rings), the large kernel keeps its per-ring advance
  cost (bandwidth-trivial per Phase 0.5), and the win/cnt semantics are
  layer-local, so the speedup should carry over — but re-run the
  bit-exact verification at a production ring count before enabling the
  flag by default.
- The small kernel writes the whole 1 MiB window every layer (coalesced
  `win[idx] = (nhits != 0)`), so `win.fill(0)` can be skipped for the
  small kernel's coverage — but keep it if the large kernel's semantics
  ever change (currently included in all timings, 1 MiB ≈ 4 µs).
