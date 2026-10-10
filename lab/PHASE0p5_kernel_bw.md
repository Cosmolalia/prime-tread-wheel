# Phase 0.5 — stamp_kernel bandwidth micro-benchmark

Date: 2026-10-10. Probe: `lab/p0p5_probe.py` (standalone, cupy; own sieve of
primes ≤ 2,000,000 → 148,933 rings; W = 1,048,576 window; rings seeded on
host with the engine's exact closed form from `gpu_frontier.py`
seed_kernel/advance_kernel: `o ≡ −T(m0−1) mod p` via the even-lift trick,
`d = m0 mod p`; layer m0 = 100,000, window [k0, k1] = [T+1, T+W]).
CUDA-event timing, 7 reps after 1 warmup, current stream.

**Co-runner note:** the task brief states a live pygame window (pid 6410)
shares the GPU. At measurement time `nvidia-smi` showed **no such process**
(GPU idle, 0% util, only Xorg at 4 MiB — pid 6410 does not exist). No
process was signaled or killed; the probe used a few seconds of GPU time
total. Absolute numbers below are therefore *uncontended* (if anything,
optimistic vs. production); the relative ordering of (a)/(b)/(c) is the
signal. Under a real co-runner all kernel times scale up roughly uniformly.

## Results (RTX 4070 Laptop, mean of 7)

| # | Measurement | Time | Nominal GB/s | Notes |
|---|-------------|------|--------------|-------|
| (a) | Streaming triad, 8M-elem uint32 ×3 (96 MB moved) | 0.481 ms | **199.8 GB/s** | healthy reference (≈78% of 256 GB/s peak) |
| (b) | Production stamp kernel as-is (uint8 win + atomicAdd cnt), kernel-only | **16.26 ms/pass** | 0.119 GB/s | 3,078,806 stamps/pass |
| (c) | uint32-window variant (4-byte stores, same scatter, same atomic) | **18.13 ms/pass** | 0.131 GB/s | **slower** than uint8 |
| (c2) | u8 win store only, atomic removed | 9.01 ms/pass | — | 3.08 M scattered stores ≈ 2.9 ns each |
| (c2) | atomicAdd only, win store removed | 8.25 ms/pass | — | 3.08 M scattered atomics ≈ 2.7 ns each |
| (d) | win_u8.fill(0) (1 MiB) | 0.0037 ms | 280 GB/s | negligible |
| (d) | win_u32.fill(0) (4 MiB) | 0.0063 ms | 666 GB/s | negligible |
| (d) | cnt.fill(0) (4 MiB) | 0.0062 ms | 672 GB/s | negligible |

## Verdict: **H2 refuted as stated; H1 refuted; the true cause is a third mechanism — per-ring thread serialization + scattered-atomic/store issue rate**

**H1 (benchmark-loop overhead) — refuted.** Production reports ~12 ms/layer
wall at 11M rings. The stamp kernel *alone*, kernel-only time with CUDA
events, at only 149k rings, takes 16.3 ms. The per-layer Python/fill/sum
overhead measured here is <0.05 ms (row d + the win.sum reduction). The
kernel is essentially the entire layer cost; the benchmark is not misleading
about where time goes.

**H2 (uint8 sector-write amplification, ~32×) — refuted.** The uint32-window
variant is *slower* (18.1 vs 16.3 ms), not faster. Store width is irrelevant
because the kernel never approaches bandwidth: 3.08 M scattered writes over
16 ms is ~190 M stores/s, against the ~200 GB/s streaming engine measured in
(a). There is no 32× write amplification to fix.

**What's actually happening.** Two additive costs, each ~half the kernel:

1. **Scattered-store + scattered-atomic issue rate.** 3.08 M stamps each do
   one u8 store and one global atomicAdd to random positions of a 1 MiB/4 MiB
   window. Decomposition shows they cost ~2.9 ns and ~2.7 ns each,
   respectively, and add linearly (9.0 + 8.3 ≈ 16.3 ms). This is an
   occupancy/latency wall, not a bandwidth wall.
2. **Critical-path serialization on small-prime rings.** The kernel maps one
   thread per ring. The p = 2 ring's single thread walks the entire 1 MiB
   window in W/2 = 524,288 sequential loop iterations — ~9–17 ns per
   iteration bounds the whole kernel regardless of how many other threads
   idle. Work per thread varies over ~6 orders of magnitude (524k stamps for
   p=2 vs 0–1 for most rings > W), so the GPU runs at the pace of its
   unluckiest thread.

The "~220 MB nominal ring traffic per layer" framing is a red herring: that
traffic is the *ring arrays*, which the stamp kernel only reads (8 B/ring);
the real work is the stamp loop, whose cost scales with Σ_p W/p ≈ W·(ln ln p_max
+ M) ≈ 3.1 M scattered stores, nearly independent of ring count.

## Implications for the production engine

- **Bit-packed or uint32 window: no.** Measured slower; the store is not the
  bottleneck. Don't spend effort there.
- **Sorting/bucketing ring writes: the right fix, but by inverting the
  parallelization, not by sorting rings.** Options, in expected payoff order:
  1. **Split the kernel by prime size.** For p ≤ W the loop trips W/p times;
     give small primes a *window-parallel* kernel (grid-stride over k ∈
     [k0, k1], each thread tests divisibility by the small-prime list, write
     coalesced). For p > W (the vast majority at production scale, ≤1 stamp
     per ring per layer) keep the current per-ring kernel. This removes the
     W/2 critical path entirely and turns small-prime stamping into coalesced
     writes — a ~5–15× kernel speedup is plausible (16 ms → ~1–3 ms).
  2. **Make the witness-count atomic optional.** atomicAdd(cnt) is ~50% of
     kernel time (8.25/16.26 ms). If omega(N) counting is only needed for
     verification layers, gate it behind a flag; or derive it in a separate
     pass. Halves the cost of whatever kernel remains.
  3. Also note advance_kernel (88 MB write per layer at 11M rings) is
     bandwidth-trivial (<1 ms at the measured ~200 GB/s) — not a target.
- Even with zero stamp cost the ~12 ms/layer would only fall by ~16 ms of
  kernel time; the Python loop overhead is demonstrably negligible, so the
  projected post-fix layer time is fill+stamp+advance+sum ≈ 1–3 ms, i.e.
  the engine would become genuinely memory-bound for the first time.

## Raw sanity checks

- Per-pass stamp count 3,078,806 ≈ W·(ln ln 2e6 + B₁) ≈ 1 MiB × 2.93 —
  matches the theoretical Σ W/p.
- u8 and u32 windows produced identical nonzero counts across all reps.
- Nominal-bytes accounting for (b): 148,933 rings × (4 B P + 4 B O + 1 B win
  + 4 B cnt RMW) = 1.94 MB / 16.26 ms → 0.119 GB/s (table column).
