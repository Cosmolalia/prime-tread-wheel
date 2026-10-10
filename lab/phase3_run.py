"""Phase 3: cross-layer correlation closure on the retained-structure axis.

Real: omega_small count series for layers m = 1_500_000 .. 1_500_015 (W = 2**20).
Null: 20 pairs of random 1M-windows at random offsets in [1e11, 1e13].
Statistic per pair: max |FFT cross-correlation| over all lags -(W-1)..(W-1),
series mean-centered and unit-norm (identical construction real vs null).
"""
import json
import math
import time

import numpy as np

W = 1 << 20
M0 = 1_500_000
L = 16
SEED = 20261010
N_NULL_PAIRS = 20

t_start = time.time()

# --- sieve primes up to max bound over the layer range ---
max_bound = max(int((m + 1) / math.sqrt(2)) + 1 for m in range(M0, M0 + L))
limit = max_bound + 1
is_p = np.ones(limit + 1, dtype=bool)
is_p[:2] = False
for i in range(2, int(limit ** 0.5) + 1):
    if is_p[i]:
        is_p[i * i::i] = False
primes = np.flatnonzero(is_p).astype(np.int64)
print(f"sieved {len(primes)} primes <= {limit}  ({time.time()-t_start:.1f}s)", flush=True)


def omega_series(N0):
    """omega_small(N) for N in [N0, N0+W), sieve-style strided increments."""
    cnt = np.zeros(W, dtype=np.uint8)
    for p in primes:
        if p > N0 + W:  # prime cannot divide any N in window if p > max N
            break
        i0 = int((-N0) % p)
        cnt[i0::p] += 1
    return cnt


def layer_N0(m):
    T = m * (m - 1) // 2
    return T + m - W + 1


def xcorr_max(series_a, series_b):
    """Max |cross-correlation| over all lags, with lag of the max.

    Series are mean-centered and unit-norm; FFT cross-correlation on length n=2W.
    Returns (max_abs_corr, lag, corr_at_lag0).
    """
    a = series_a.astype(np.float64)
    b = series_b.astype(np.float64)
    a -= a.mean()
    b -= b.mean()
    a /= np.linalg.norm(a)
    b /= np.linalg.norm(b)
    n = 2 * W
    A = np.fft.rfft(a, n)
    B = np.fft.rfft(b, n)
    c = np.fft.irfft(A * np.conj(B), n)
    # lags 0..W-1 at c[0:W], lags -(W-1)..-1 at c[n-W+1:n]
    pos = c[:W]
    neg = c[n - W + 1:]
    imax_pos = int(np.argmax(np.abs(pos)))
    imax_neg = int(np.argmax(np.abs(neg)))
    if abs(pos[imax_pos]) >= abs(neg[imax_neg]):
        best, lag = pos[imax_pos], imax_pos
    else:
        best, lag = neg[imax_neg], imax_neg - n  # e.g. index n-1 -> lag -1
    return float(abs(best)), int(lag), float(c[0])


# --- real layers ---
real_series = []
for m in range(M0, M0 + L):
    t0 = time.time()
    s = omega_series(layer_N0(m))
    real_series.append(s)
    print(f"layer m={m}: done in {time.time()-t0:.1f}s, mean_omega={s.mean():.4f}", flush=True)

real = {}
for j in range(1, L):
    a = real_series[0]
    b = real_series[j]
    mc, lag, c0 = xcorr_max(a, b)
    real[j] = {"max_abs_corr": mc, "lag_of_max": lag, "corr_lag0": c0}
    print(f"real j={j}: max|corr|={mc:.6f} at lag={lag}, corr(0)={c0:.6f}", flush=True)

# --- null pairs ---
rng = np.random.default_rng(SEED)
null = []
for k in range(N_NULL_PAIRS):
    X = rng.integers(10**11, 10**13, size=2)
    s_a = omega_series(int(X[0]))
    s_b = omega_series(int(X[1]))
    mc, lag, c0 = xcorr_max(s_a, s_b)
    null.append({"max_abs_corr": mc, "lag_of_max": lag, "corr_lag0": c0,
                 "X0": int(X[0]), "X1": int(X[1])})
    print(f"null pair {k}: max|corr|={mc:.6f} at lag={lag}, corr(0)={c0:.6f}", flush=True)

null_max = np.array([n_["max_abs_corr"] for n_ in null])
null_c0 = np.array([n_["corr_lag0"] for n_ in null])


def quantile_of(value, dist):
    return float((dist < value).mean())  # fraction of null strictly below


envelope = {
    "min": float(null_max.min()), "mean": float(null_max.mean()),
    "std": float(null_max.std()), "max": float(null_max.max()),
    "q50": float(np.quantile(null_max, 0.5)), "q90": float(np.quantile(null_max, 0.9)),
    "q95": float(np.quantile(null_max, 0.95)), "q99": float(np.quantile(null_max, 0.99)),
}

report = {"real": {}, "envelope": envelope}
for j in range(1, L):
    r = real[j]
    report["real"][j] = {
        **r,
        "quantile_in_null_maxdist": quantile_of(r["max_abs_corr"], null_max),
        "exceeds_null_max": bool(r["max_abs_corr"] > envelope["max"]),
    }
report["null_pairs"] = null
report["null_lag0"] = {"mean": float(null_c0.mean()), "std": float(null_c0.std()),
                       "min": float(null_c0.min()), "max": float(null_c0.max())}
report["meta"] = {"W": W, "M0": M0, "L": L, "seed": SEED,
                  "n_null_pairs": N_NULL_PAIRS,
                  "primes_sieved_to": int(limit), "n_primes": int(len(primes)),
                  "runtime_s": time.time() - t_start}

out = "/home/solaya/Desktop/TOE/harness/data/projects/prime-tread-wheel/lab/PHASE3_results.json"
with open(out, "w") as f:
    json.dump(report, f, indent=2)
print(f"\nwrote {out}  total {time.time()-t_start:.1f}s", flush=True)
