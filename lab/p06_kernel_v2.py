#!/usr/bin/env python3
"""Phase 0.6 — stamp kernel v2 prototype: split by prime size.

Per lab/PHASE0p5_kernel_bw.md, the production stamp kernel (one thread per
ring) is bound by (a) the p=2 ring's single thread walking W/2 ticks and
(b) scattered-store/atomic issue rate (~2.9 ns per scattered u8 store, ~2.7
ns per scattered atomicAdd, additive). v2 splits the rings:

  SMALL (p <= P_CUTOFF): window-parallel kernel. One thread per tick;
  each thread loops over the pi(P_CUTOFF) small primes and tests
  idx % p == (o - k0) mod p using a precomputed magic multiplier
  (q = (idx * ceil(2^40/p)) >> 40 is exact for idx < 2^20, p <= 2^16 —
  branchless, no hardware divide). Writes are fully coalesced:
  win[idx] = (nhits != 0), and cnt[idx] = nhits as a plain store when
  witnesses are enabled (exactly one thread owns each tick, so the
  production atomicAdd semantics are preserved without atomics).

  LARGE (p >  P_CUTOFF): the production per-ring stamp kernel, verbatim
  semantics (few iterations per ring; it is not the bottleneck).

Seeding replicates gpu_frontier.py seed_kernel / advance_kernel exactly on
host with numpy (same mod-2p even-lift closed form; same o-=d / d+=1 mod p
advance), so both kernels see bit-identical ring state.

Verification: both kernels run on the same seeded state for >= 3 layers;
win AND cnt must match bit-for-bit per layer before any timing.

Run with the CUDA runtime libs on LD_LIBRARY_PATH (see gpu-frontier/run.sh):
  SP=$HOME/.local/lib/python3.10/site-packages/nvidia
  LD_LIBRARY_PATH=$SP/cuda_nvrtc/lib:$SP/cuda_runtime/lib python3 p06_kernel_v2.py
"""

import sys
import time

import numpy as np

import cupy as cp

W = 1 << 20            # window size, same as production
PRIME_BOUND = 2_000_000
M0 = 100_000           # seed layer (same as the Phase 0.5 probe)
VERIFY_LAYERS = 4      # >= 3 layers of bit-exact verification
BLOCK = 256
REPS = 7               # >= 7 benchmark reps (rep 0 is warmup, discarded)
CUTOFFS = [64, 128, 256, 1024, 2048, 4096, 8192, 16384, 32768, 65536]


# ----------------------------------------------------------------- kernels --

# Production stamp kernel, verbatim semantics from gpu_frontier.py
# (float-reciprocal j0 + integer correction), renamed. The no-atomic twin
# isolates the win-store cost at production shape.
STAMP_LARGE_SRC = r"""
extern "C" __global__ void stamp_large(
    const unsigned int* P, const int n,
    const unsigned int* O,
    unsigned long long k0, unsigned long long k1,
    unsigned char* win, unsigned int* cnt, const int use_cnt)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;
    unsigned long long p = P[i];
    unsigned long long o = O[i];
    unsigned long long j0 = 0ULL;
    if (o < k0) {
        unsigned long long x = k0 - o;
        double inv = 1.0 / (double)p;
        j0 = (unsigned long long)((double)x * inv);
        while (o + j0 * p < k0) j0++;
        while (j0 > 0ULL && o + (j0 - 1ULL) * p >= k0) j0--;
    }
    for (unsigned long long k = o + j0 * p; k <= k1; k += p) {
        win[k - k0] = 1;
        if (use_cnt) atomicAdd(cnt + (k - k0), 1u);
    }
}
"""

# Window-parallel small-prime kernel. One thread per tick; loop over the
# small primes; magic-multiplier modulo (exact for idx < 2^20, p <= 2^16);
# coalesced win store, optional plain coalesced cnt store (no atomics —
# each tick is owned by exactly one thread).
STAMP_SMALL_SRC = r"""
extern "C" __global__ void stamp_small(
    const unsigned int* __restrict__ P,
    const unsigned long long* __restrict__ MG,
    const unsigned int* __restrict__ RES,
    const int ns, const unsigned int W,
    unsigned char* __restrict__ win,
    unsigned int* __restrict__ cnt, const int use_cnt)
{
    unsigned int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= W) return;
    unsigned int nhits = 0u;
    #pragma unroll 8
    for (int i = 0; i < ns; i++) {
        unsigned int p = P[i];
        unsigned long long q = ((unsigned long long)idx * MG[i]) >> 40;
        unsigned int r = idx - (unsigned int)(q * (unsigned long long)p);
        nhits += (r == RES[i]);
    }
    win[idx] = (unsigned char)(nhits != 0u);
    if (use_cnt) cnt[idx] = nhits;
}
"""


def grid(n):
    return ((n + BLOCK - 1) // BLOCK,)


def time_kernel(launch, reps=REPS):
    """CUDA-event timing of launch() on the current stream. Returns ms."""
    launch()  # warmup / JIT
    cp.cuda.stream.get_current_stream().synchronize()
    times = []
    for _ in range(reps):
        start = cp.cuda.Event()
        end = cp.cuda.Event()
        start.record()
        launch()
        end.record()
        cp.cuda.stream.get_current_stream().synchronize()
        times.append(cp.cuda.get_elapsed_time(start, end))
    return float(np.mean(times)), float(np.min(times)), times


# ------------------------------------------------------------- host engine --

class HostState:
    """Ring state seeded/advanced with the engine's exact closed form."""

    def __init__(self, primes, m0):
        self.P64 = primes.astype(np.uint64)
        m0 = np.uint64(m0)
        a = np.uint64(m0) % self.P64            # m0 mod p
        b = (np.uint64(m0) - 1) % self.P64      # (m0-1) mod p
        r2 = (a * b) % (2 * self.P64)
        u = np.where(r2 % 2 == 0, r2, r2 + self.P64)
        t = (u // 2) % self.P64                 # T mod p (even-lift halving)
        self.O = np.where(t == 0, np.uint64(0),
                          self.P64 - t).astype(np.uint64)
        self.D = a.copy()
        self.m = int(m0)

    def advance(self):
        """advance_kernel: o = o-d mod p; d = d+1 mod p."""
        P, O, D = self.P64, self.O, self.D
        self.O = np.where(O >= D, O - D, O + P - D)
        self.D = np.where(D + 1 == P, np.uint64(0), D + 1)
        self.m += 1

    def layer_window(self):
        m = self.m
        k0 = (m - 1) * m // 2 + 1     # window [k0, k1], W ticks
        return k0, k0 + W - 1


def sieve_primes(n):
    s = np.ones(n + 1, dtype=bool)
    s[0:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if s[p]:
            s[p * p::p] = False
    return np.flatnonzero(s).astype(np.uint64)


def main():
    print(f"W = {W:,}  prime bound = {PRIME_BOUND:,}  seed layer m0 = {M0:,}",
          flush=True)

    # ------------------------------------------------------------ rings ----
    primes = sieve_primes(PRIME_BOUND)
    n_rings = len(primes)
    print(f"rings: {n_rings:,} primes <= {PRIME_BOUND:,}", flush=True)

    st = HostState(primes, M0)
    O0, D0 = st.O.copy(), st.D.copy()      # pristine seeded state

    ringP = cp.array(primes, dtype=cp.uint32)
    ringO = cp.empty(n_rings, dtype=cp.uint32)

    stamp_large = cp.RawKernel(STAMP_LARGE_SRC, "stamp_large")
    stamp_small = cp.RawKernel(STAMP_SMALL_SRC, "stamp_small")

    win = cp.zeros(W, dtype=cp.uint8)
    cnt = cp.zeros(W, dtype=cp.uint32)

    # ------------------------------------------------- split + host setup --
    def make_split(cutoff):
        ns = int(np.searchsorted(primes, cutoff, side="right"))
        Ps = primes[:ns].astype(np.uint64)
        MG = (np.uint64(1 << 40) + Ps - 1) // Ps     # ceil(2^40 / p)
        d_p = cp.array(primes[:ns], dtype=cp.uint32)
        d_mg = cp.array(MG, dtype=cp.uint64)
        d_res = cp.empty(ns, dtype=cp.uint32)
        nl = n_rings - ns
        d_pl = cp.array(primes[ns:], dtype=cp.uint32)
        d_ol = cp.empty(nl, dtype=cp.uint32)
        return ns, d_p, d_mg, d_res, nl, d_pl, d_ol

    def upload_state(st_, split):
        ns, d_p, d_mg, d_res, nl, d_pl, d_ol = split
        k0, _ = st_.layer_window()
        # per-layer residues: idx == k - k0 congruent (o - k0) mod p
        t0 = time.perf_counter()
        RES = ((st_.O[:ns].astype(np.int64) - k0)
               % primes[:ns].astype(np.int64))
        host_us = (time.perf_counter() - t0) * 1e6
        d_res[...] = cp.array(RES.astype(np.uint32))
        ringO[...] = cp.array(st_.O.astype(np.uint32))   # full set (prod ref)
        d_ol[...] = cp.array(st_.O[ns:].astype(np.uint32))
        return host_us

    CUTOFF_MAIN = 8192   # verification cutoff; sweep below finds the best

    def run_prod(st_, use_cnt):
        k0, k1 = st_.layer_window()
        win.fill(0)
        cnt.fill(0)
        stamp_large(grid(n_rings), (BLOCK,),
                    (ringP, n_rings, ringO, k0, k1, win, cnt,
                     np.int32(use_cnt)))
        cp.cuda.stream.get_current_stream().synchronize()

    def run_v2(st_, split, use_cnt):
        ns, d_p, d_mg, d_res, nl, d_pl, d_ol = split
        k0, k1 = st_.layer_window()
        win.fill(0)
        cnt.fill(0)
        stamp_small(grid(W), (BLOCK,),
                    (d_p, d_mg, d_res, ns, W, win, cnt, np.int32(use_cnt)))
        if nl:
            stamp_large(grid(nl), (BLOCK,),
                        (d_pl, nl, d_ol, k0, k1, win, cnt,
                         np.int32(use_cnt)))
        cp.cuda.stream.get_current_stream().synchronize()

    # ---------------------------------------------------------- verify -----
    for CUTOFF_MAIN in dict.fromkeys((1024, 8192)):   # recommended + wide
        print(f"\n=== exact-match verification (cutoff {CUTOFF_MAIN}) ===",
              flush=True)
        split = make_split(CUTOFF_MAIN)
        ns = split[0]
        print(f"small rings: {ns:,} (p <= {CUTOFF_MAIN}), "
              f"large rings: {split[4]:,}", flush=True)

        st.O, st.D = O0.copy(), D0.copy()
        st.m = M0
        ok_all = True
        for layer in range(VERIFY_LAYERS):
            upload_state(st, split)
            run_prod(st, use_cnt=1)
            win_ref, cnt_ref = win.get(), cnt.get()
            run_v2(st, split, use_cnt=1)
            win_v2, cnt_v2 = win.get(), cnt.get()
            w_ok = np.array_equal(win_ref, win_v2)
            c_ok = np.array_equal(cnt_ref, cnt_v2)
            # win-only variants must also agree on win
            run_prod(st, use_cnt=0)
            win_p0 = win.get()
            run_v2(st, split, use_cnt=0)
            win_v0 = win.get()
            wo_ok = np.array_equal(win_p0, win_v0) and np.array_equal(win_v0,
                                                                      win_ref)
            layer_ok = w_ok and c_ok and wo_ok
            ok_all &= layer_ok
            print(f"layer m={st.m:,}: win {'OK' if w_ok else 'MISMATCH'}  "
                  f"cnt {'OK' if c_ok else 'MISMATCH'}  "
                  f"win-only {'OK' if wo_ok else 'MISMATCH'}  "
                  f"{'PASS' if layer_ok else 'FAIL'}", flush=True)
            if not layer_ok:
                bad = np.flatnonzero(win_ref != win_v2)[:10]
                badc = np.flatnonzero(cnt_ref != cnt_v2)[:10]
                print(f"  win mismatches at idx {bad} "
                      f"({np.count_nonzero(win_ref != win_v2):,} total)",
                      flush=True)
                print(f"  cnt mismatches at idx {badc} "
                      f"({np.count_nonzero(cnt_ref != cnt_v2):,} total)",
                      flush=True)
                break
            st.advance()

        if not ok_all:
            print("\nVERIFICATION FAILED — mismatch pattern above; "
                  "not benchmarking.", flush=True)
            sys.exit(2)
        print(f"verification PASS at cutoff {CUTOFF_MAIN}: bit-identical "
              f"win and cnt on {VERIFY_LAYERS} layers (witness + win-only)",
              flush=True)

    # ---------------------------------------------------------- benchmark --
    print("\n=== benchmark (CUDA events, mean of "
          f"{REPS}, co-running with live pygame pid 19718) ===", flush=True)

    def bench(fn, label):
        mean_ms, min_ms, _ = time_kernel(fn)
        print(f"{label}: {mean_ms:.3f} ms/layer (min {min_ms:.3f})",
              flush=True)
        return mean_ms, min_ms

    # restore the pristine seeded state; benchmarks run at layer m0
    st.O, st.D = O0.copy(), D0.copy()
    st.m = M0
    k0, k1 = st.layer_window()
    upload_state(st, split)
    res = {}
    res["prod_witness"] = bench(
        lambda: stamp_large(grid(n_rings), (BLOCK,),
                            (ringP, n_rings, ringO, k0, k1, win, cnt,
                             np.int32(1))), "production (verbatim) + witness")

    def v2_launch(split_, use_cnt):
        nsl, d_p, d_mg, d_res, nl, d_pl, d_ol = split_
        stamp_small(grid(W), (BLOCK,),
                    (d_p, d_mg, d_res, nsl, W, win, cnt, np.int32(use_cnt)))
        if nl:
            stamp_large(grid(nl), (BLOCK,),
                        (d_pl, nl, d_ol, k0, k1, win, cnt,
                         np.int32(use_cnt)))

    res["v2_witness"] = bench(lambda: v2_launch(split, 1),
                              f"v2 cutoff {CUTOFF_MAIN} + witness")
    res["v2_winonly"] = bench(lambda: v2_launch(split, 0),
                              f"v2 cutoff {CUTOFF_MAIN} win-only")
    res["prod_winonly"] = bench(
        lambda: stamp_large(grid(n_rings), (BLOCK,),
                            (ringP, n_rings, ringO, k0, k1, win, cnt,
                             np.int32(0))), "production win-only (no atomic)")

    # ---------------------------------------------------------- sweep ------
    print("\n=== P_CUTOFF sweep (v2, witness variant) ===", flush=True)
    sweep = []
    for c in CUTOFFS:
        sp = make_split(c)
        st.O, st.D = O0.copy(), D0.copy()
        st.m = M0
        host_us = upload_state(st, sp)
        mean_ms, min_ms, _ = time_kernel(lambda: v2_launch(sp, 1))
        n_small = sp[0]
        sweep.append((c, n_small, mean_ms, min_ms, host_us))
        print(f"cutoff {c:>6,}: pi={n_small:>5,}  {mean_ms:8.3f} ms/layer "
              f"(min {min_ms:.3f})  host residue recompute {host_us:7.1f} us",
              flush=True)

    best = min(sweep, key=lambda r: r[2])
    print(f"\nbest cutoff: {best[0]:,} -> {best[2]:.3f} ms/layer", flush=True)

    # bench v2 at the best cutoff (both variants) + decompose small vs large
    sp_best = make_split(best[0])
    st.O, st.D = O0.copy(), D0.copy()
    st.m = M0
    upload_state(st, sp_best)
    res["v2_best_witness"] = bench(lambda: v2_launch(sp_best, 1),
                                   f"v2 cutoff {best[0]:,} + witness")
    res["v2_best_winonly"] = bench(lambda: v2_launch(sp_best, 0),
                                   f"v2 cutoff {best[0]:,} win-only")
    nsl, d_p, d_mg, d_res, nl, d_pl, d_ol = sp_best
    res["small_only"] = bench(
        lambda: stamp_small(grid(W), (BLOCK,),
                            (d_p, d_mg, d_res, nsl, W, win, cnt,
                             np.int32(1))),
        f"  small kernel alone (cutoff {best[0]:,})")
    res["large_only"] = bench(
        lambda: stamp_large(grid(nl), (BLOCK,),
                            (d_pl, nl, d_ol, k0, k1, win, cnt,
                             np.int32(1))) if nl else None,
        f"  large kernel alone (cutoff {best[0]:,})")

    prod_ms = res["prod_witness"][0]
    v2_ms = res["v2_best_witness"][0]
    print(f"\nspeedup (witness, best cutoff {best[0]:,}): "
          f"{prod_ms / v2_ms:.2f}x  ({prod_ms:.3f} -> {v2_ms:.3f} ms)")
    print(f"vs Phase 0.5 uncontended 16.26 ms: {16.26 / v2_ms:.2f}x recovery")

    print("\nSUMMARY")
    for k_, v_ in res.items():
        print(f"  {k_}: {v_[0]:.3f} ms (min {v_[1]:.3f})")
    for c, n_small, mean_ms, min_ms, host_us in sweep:
        print(f"  sweep cutoff {c}: {mean_ms:.3f} ms")


if __name__ == "__main__":
    t0 = time.time()
    main()
    print(f"wall {time.time() - t0:.1f}s")
