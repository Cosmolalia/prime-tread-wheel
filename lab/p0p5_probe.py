#!/usr/bin/env python3
"""Phase 0.5 GPU micro-benchmark: why is stamp_kernel bandwidth-poor?

Distinguishes H1 (benchmark-loop overhead dominates) from H2 (scattered
uint8 writes -> sector-write amplification). Standalone: builds its own
sieve, seeds rings on host with the engine's closed form (gpu_frontier.py
seed_kernel/advance_kernel), and measures kernel-only times with CUDA
events on the current stream.

Run with run.sh's LD_LIBRARY_PATH:
  SP=$HOME/.local/lib/python3.10/site-packages/nvidia
  LD_LIBRARY_PATH=$SP/cuda_nvrtc/lib:$SP/cuda_runtime/lib python3 p0p5_probe.py
"""

import time

import numpy as np

import cupy as cp

W = 1 << 20          # window size, same as production
PRIME_BOUND = 2_000_000
REPS = 7             # >= 5 reps requested; rep 0 is warmup, discarded
BLOCK = 256


# ----------------------------------------------------------------- kernels --
TRIAD_SRC = r"""
extern "C" __global__ void triad(const unsigned int* a,
                                 const unsigned int* b,
                                 unsigned int* c, const int n)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i] * 3u;
}
"""

STAMP_U8_SRC = r"""
extern "C" __global__ void stamp_u8(
    const unsigned int* P, const int n,
    const unsigned int* O,
    unsigned long long k0, unsigned long long k1,
    unsigned char* win, unsigned int* cnt)
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
        atomicAdd(cnt + (k - k0), 1u);
    }
}
"""

STAMP_U32_SRC = STAMP_U8_SRC.replace(
    "unsigned char* win", "unsigned int* win").replace(
    "win[k - k0] = 1;", "win[k - k0] = 1u;").replace(
    "stamp_u8", "stamp_u32")

# decomposition variants: isolate win-store cost vs atomic cost
STAMP_U8_NOATOMIC_SRC = STAMP_U8_SRC.replace(
    "atomicAdd(cnt + (k - k0), 1u);", "(void)cnt;").replace(
    "stamp_u8", "stamp_u8_noatomic")
STAMP_ATOMIC_ONLY_SRC = STAMP_U8_SRC.replace(
    "win[k - k0] = 1;", "").replace(
    "unsigned char* win", "unsigned char* win_unused").replace(
    "stamp_u8", "stamp_atomic_only")


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
    return float(np.mean(times)), float(np.min(times))


def main():
    # ------------------------------------------------------- sieve (host) --
    n = PRIME_BOUND
    s = np.ones(n + 1, dtype=bool)
    s[0:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if s[p]:
            s[p * p::p] = False
    primes = np.flatnonzero(s).astype(np.uint64)
    n_rings = len(primes)
    print(f"rings: {n_rings:,} primes <= {PRIME_BOUND:,}")

    # --------------------------------- seed rings with engine closed form --
    # seed_kernel: O = -T(m0-1) mod p  (T = m0*(m0-1)/2, even-lift trick),
    #               D = m0 mod p ; advance: o -= d (mod p), d = d+1 (mod p).
    m0 = 100_000
    k0 = m0 * (m0 - 1) // 2 + 1
    k1 = k0 + W - 1
    a = m0 % primes
    b = (m0 - 1) % primes
    r2 = (a * b) % (2 * primes)
    u = np.where(r2 % 2 == 0, r2, r2 + primes)
    t = (u // 2) % primes
    O_host = np.where(t == 0, np.uint64(0), primes - t).astype(np.uint32)
    D_host = (m0 % primes).astype(np.uint32)

    ringP = cp.array(primes, dtype=cp.uint32)
    ringO = cp.array(O_host, dtype=cp.uint32)
    ringD = cp.array(D_host, dtype=cp.uint32)

    win_u8 = cp.zeros(W, dtype=cp.uint8)
    win_u32 = cp.zeros(W, dtype=cp.uint32)
    cnt = cp.zeros(W, dtype=cp.uint32)

    triad = cp.RawKernel(TRIAD_SRC, "triad")
    stamp_u8 = cp.RawKernel(STAMP_U8_SRC, "stamp_u8")
    stamp_u32 = cp.RawKernel(STAMP_U32_SRC, "stamp_u32")
    stamp_u8_noatomic = cp.RawKernel(STAMP_U8_NOATOMIC_SRC,
                                     "stamp_u8_noatomic")
    stamp_atomic_only = cp.RawKernel(STAMP_ATOMIC_ONLY_SRC,
                                     "stamp_atomic_only")

    results = {}

    # (a) streaming triad, 8M-elem uint32 (~32 MB each) --------------------
    N = 8_000_000
    ta, tb, tc = (cp.full(N, i + 1, dtype=cp.uint32) for i in range(3))
    mean_ms, min_ms = time_kernel(
        lambda: triad(grid(N), (BLOCK,), (ta, tb, tc, N)))
    bytes_moved = N * 4 * 3  # read a, b; write c
    gbps = bytes_moved / (mean_ms * 1e-3) / 1e9
    results["triad"] = (mean_ms, min_ms, gbps)
    print(f"(a) triad 8M uint32: {mean_ms:.3f} ms  -> {gbps:.1f} GB/s")

    # (b) production stamp kernel, uint8 window -----------------------------
    mean_ms, min_ms = time_kernel(
        lambda: stamp_u8(grid(n_rings), (BLOCK,),
                         (ringP, n_rings, ringO, k0, k1, win_u8, cnt)))
    # nominal bytes touched per ring: read P,O (8 B) + win store (1 B)
    # + cnt atomic RMW (4 B)
    nominal = n_rings * 13
    gbps = nominal / (mean_ms * 1e-3) / 1e9
    results["stamp_u8"] = (mean_ms, min_ms, gbps)
    print(f"(b) stamp uint8: {mean_ms:.3f} ms/pass, nominal {gbps:.3f} GB/s")

    # (c) uint32-window variant --------------------------------------------
    mean_ms, min_ms = time_kernel(
        lambda: stamp_u32(grid(n_rings), (BLOCK,),
                          (ringP, n_rings, ringO, k0, k1, win_u32, cnt)))
    nominal32 = n_rings * (8 + 4 + 4)
    gbps = nominal32 / (mean_ms * 1e-3) / 1e9
    results["stamp_u32"] = (mean_ms, min_ms, gbps)
    print(f"(c) stamp uint32: {mean_ms:.3f} ms/pass, nominal {gbps:.3f} GB/s")

    # (c2) decomposition: win-store only vs atomic only --------------------
    mean_ms, min_ms = time_kernel(
        lambda: stamp_u8_noatomic(grid(n_rings), (BLOCK,),
                                  (ringP, n_rings, ringO, k0, k1,
                                   win_u8, cnt)))
    results["stamp_u8_noatomic"] = (mean_ms, min_ms, np.nan)
    print(f"(c2) stamp u8 win-only (no atomic): {mean_ms:.3f} ms/pass")
    mean_ms, min_ms = time_kernel(
        lambda: stamp_atomic_only(grid(n_rings), (BLOCK,),
                                  (ringP, n_rings, ringO, k0, k1,
                                   win_u8, cnt)))
    results["stamp_atomic_only"] = (mean_ms, min_ms, np.nan)
    print(f"(c2) stamp atomic-only (no win store): {mean_ms:.3f} ms/pass")

    # sanity: u8 and u32 windows agree (before (d) zeroes them)
    assert int(cp.count_nonzero(win_u8)) == int(cp.count_nonzero(win_u32))
    n_stamps = int(cnt.sum())
    print(f"total stamps/pass: {n_stamps:,} "
          f"(~{n_stamps / n_rings:.1f} per ring)")

    # (d) fills -------------------------------------------------------------
    for name, arr in (("win_u8.fill", win_u8), ("win_u32.fill", win_u32),
                      ("cnt.fill", cnt)):
        mean_ms, min_ms = time_kernel(lambda a=arr: a.fill(0))
        results[name] = (mean_ms, min_ms,
                         arr.nbytes / (mean_ms * 1e-3) / 1e9)
        print(f"(d) {name}: {mean_ms:.4f} ms "
              f"({arr.nbytes / (mean_ms * 1e-3) / 1e9:.1f} GB/s)")

    print("\nSUMMARY (mean ms, min ms, GB/s):")
    for k, v in results.items():
        print(f"  {k}: {v[0]:.4f} / {v[1]:.4f} ms, {v[2]:.2f} GB/s nominal")


if __name__ == "__main__":
    t0 = time.time()
    main()
    print(f"wall {time.time() - t0:.1f}s")
