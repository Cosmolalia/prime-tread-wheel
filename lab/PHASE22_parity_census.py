#!/usr/bin/env python3
"""
PHASE 22 — GLM epiphany-log items 6+7: the QR-confinement equivalence and the
layer-parity mirror census.

Item 6 (GLM, 2026-10-14): "free-ring vs confined-phase coverage differs by
exactly the QR criterion 2 - (2m-1)^2 - 8j in QR_p, which is the mirror map's
own square-test." The confined model's definition (handoffs/claude-2026-10-08-
evening/phase/p10_parabola.c header, frozen Oct 8): ring p confined phases
R_p = {-T(j) mod p}, (p+1)/2 of them, and r in R_p  <=>  1 - 8r is a square
or 0 mod p. Since ring p covers tick k iff r == (T(m-1)+k) mod p, substituting
gives 1 - 8(T(m-1)+k) = 1 - 4m(m-1) - 8k = 2 - (2m-1)^2 - 8k. GLM's
criterion is the confinement rule itself; this leg verifies the equivalence
directly rather than trusting either side's assertion.

Item 7 (GLM, 2026-10-14): "mirror pairs exist only on even layers (B7), so odd
layers' primes are all structurally single. The layer-parity conditional
distribution of prime positions should show the mirror gap explicitly."
Conventions frozen from PHASE9 (verbatim there): T(m) = m(m+1)/2; window
(T(m-1), T(m)]; pair = p prime with T(m-1) < p <= m^2/2 and m^2 - p prime;
unordered; m=2 self-pair included. Histograms over 4 <= m < 2000, pair census
re-confirm to m < 3000. Singles = window primes not in any pair.

Headline comparisons:
  (a) parity [F] re-confirm: zero odd-m pairs (parity proof, numeric check);
  (b) prime density P(m)/m by layer parity, in m-bands;
  (c) pairing mass 2B/P by band (even layers): the symmetric excess;
  (d) THE mirror-gap test: shape of even-layer SINGLES vs odd-layer primes.
      Under "B7 window mechanism is the whole parity story", the two single
      populations should match in position distribution. Sampling-noise scale
      estimated by splitting even layers into two independent halves. If
      TV(even-singles, odd) >> TV(even-halfA, even-halfB), there is parity
      structure in singles beyond the mirror mechanism -> news. Otherwise the
      mirror gap is exactly the pairs and nothing else.
  (e) accidental-symmetry statistic per layer (normalized L1 distance between
      the layer's own position histogram and its mirror image), even vs odd:
      even-all should be far more mirror-symmetric than odd-all; even-singles
      should sit at the odd-all level if the mechanism account is complete.

CPU only, deterministic. No files modified except this artifact.
"""
import numpy as np
from math import log

# --------------------------------------------------------------------------
# shared sieve to 3000^2 = 9e6
# --------------------------------------------------------------------------
LIM = 3000 ** 2
sieve = bytearray(b"\x01") * (LIM + 1)
sieve[0:2] = b"\x00\x00"
for i in range(2, int(LIM ** 0.5) + 1):
    if sieve[i]:
        sieve[i * i::i] = b"\x00" * len(sieve[i * i::i])
def is_p(x):
    return sieve[x] == 1

def T(m):
    return m * (m + 1) // 2

# ==========================================================================
# LEG 1 — QR criterion == confinement rule (item 6 core)
# ==========================================================================
print("=" * 78)
print("LEG 1 — QR equivalence: r in R_p = {-T(j) mod p}  <=>  1 - 8r square or 0 mod p")
print("=" * 78)
bad = []
for p in [q for q in range(3, 600) if sieve[q]]:
    Rp = {(-T(j)) % p for j in range(p)}          # T(j) mod p for j = 0..p-1 covers all j
    squares = {r for r in range(p) if r == 0 or pow((1 - 8 * r) % p, (p - 1) // 2, p) in (0, 1)}
    # Euler criterion: a^((p-1)/2) mod p in {0,1} iff a == 0 or a in QR_p
    fwd_ok = all(pow((1 - 8 * r) % p, (p - 1) // 2, p) in (0, 1) for r in Rp)
    if Rp != squares or not fwd_ok or len(Rp) != (p + 1) // 2:
        bad.append(p)
print("primes checked:", len([q for q in range(3, 600) if sieve[q]]), "(all primes 3..599)")
print("equivalence failures:", bad if bad else "NONE — R_p == {r : 1-8r in QR_p or 0}, |R_p| = (p+1)/2")
print("=> 2 - (2m-1)^2 - 8j in QR_p  is EXACTLY the confined-allowed test for tick j:")
print("   1 - 8(T(m-1)+j) = 1 - 4m(m-1) - 8j = 2 - (2m-1)^2 - 8j.  [F from frozen Oct-8 def]")
print()

# ==========================================================================
# LEG 2 — layer-parity mirror census (item 7)
# ==========================================================================
print("=" * 78)
print("LEG 2 — layer-parity mirror census, conventions frozen in PHASE9")
print("=" * 78)
NB = 24  # histogram bins for u in (0,1]
MMAX_H = 2000   # histogram range
MMAX_P = 3000   # pair-census range (B7 convention re-confirm)

def window_primes(m):
    lo, hi = T(m - 1), T(m)
    return [x for x in range(lo + 1, hi + 1) if sieve[x]]

def pair_count(m, primes):
    n = m * m
    half = n // 2
    c = 0
    for p in primes:
        if p > half:
            break
        if is_p(n - p):
            c += 1
    return c

# --- pair census to 3000: parity re-confirm ---
odd_pairs = 0
tot_pairs_even = 0
first_odd_pair = None
for m in range(2, MMAX_P):
    pr = window_primes(m)
    b = pair_count(m, pr)
    if m % 2 == 0:
        tot_pairs_even += b
    else:
        odd_pairs += b
        if b and first_odd_pair is None:
            first_odd_pair = m
print(f"pair census 2 <= m < {MMAX_P}: even-m pairs = {tot_pairs_even} (reference 11,085 incl m=2)")
print(f"odd-m pairs = {odd_pairs} (parity proof: zero)  ->  {'[F] RE-CONFIRMED' if odd_pairs == 0 else 'PARITY PROOF BROKEN at m=' + str(first_odd_pair)}")
print()

# --- histograms over 4 <= m < 2000 ---
bands = [(4, 500), (500, 1000), (1000, 1500), (1500, 2000)]
hist = {k: np.zeros(NB) for k in ("even_all", "even_sing", "odd_all", "even_halfA", "even_halfB", "even_singA", "even_singB")}
band_stats = {b: dict(Pe=0, Be=0, Po=0, se=0, so=0) for b in bands}
sym = {"even_all": [], "even_sing": [], "odd_all": []}   # accidental symmetry per layer

def rel_u(x, m):
    return (x - T(m - 1)) / m

def hist_add(h, x, m):
    u = rel_u(x, m)
    idx = min(int(u * NB), NB - 1)
    h[idx] += 1

for m in range(4, MMAX_H):
    pr = window_primes(m)
    P = len(pr)
    n = m * m
    half = n / 2.0
    inpair = set()
    B = 0
    for p in pr:
        if p > n // 2:
            break
        if is_p(n - p):
            B += 1
            inpair.add(p); inpair.add(n - p)
    singles = [x for x in pr if x not in inpair]
    assert P == 2 * B + len(singles) or (m % 2 == 1 and P == len(singles))
    per_layer = np.zeros(NB)
    for x in pr:
        u = rel_u(x, m); per_layer[min(int(u * NB), NB - 1)] += 1
    mirror = per_layer[::-1]
    asym = 0.5 * np.abs(per_layer - mirror).sum() / max(P, 1)
    band = next((b for b in bands if b[0] <= m < b[1]), None)
    if m % 2 == 0:
        for x in pr: hist_add(hist["even_all"], x, m)
        for x in singles: hist_add(hist["even_sing"], x, m)
        h2 = "even_halfA" if m % 1000 < 500 else "even_halfB"
        s2 = "even_singA" if m % 1000 < 500 else "even_singB"
        for x in pr: hist_add(hist[h2], x, m)
        for x in singles: hist_add(hist[s2], x, m)
        sym["even_all"].append(asym); sym["even_sing"].append(asym)
        if band:
            band_stats[band]["Pe"] += P; band_stats[band]["Be"] += B; band_stats[band]["se"] += len(singles)
    else:
        for x in pr: hist_add(hist["odd_all"], x, m)
        sym["odd_all"].append(asym)
        if band:
            band_stats[band]["Po"] += P; band_stats[band]["so"] += len(singles)

def tv(a, b):
    na, nb = a.sum(), b.sum()
    if na == 0 or nb == 0: return float("nan")
    return 0.5 * np.abs(a / na - b / nb).sum()

print("band     layers  P_even  B_pairs  S_sing  P_odd   |  P/m even  P/m odd  2B/P(even)")
for b in bands:
    s = band_stats[b]
    lo = max(b[0], 4)
    sum_me = sum(m for m in range(lo, b[1]) if m % 2 == 0)
    sum_mo = sum(m for m in range(lo, b[1]) if m % 2 == 1)
    print(f"{b[0]:>4}-{b[1]:<4} {s['Pe']:>8} {s['Be']:>8} {s['se']:>7} {s['Po']:>7} |"
          f" {s['Pe']/sum_me:.4f}  {s['Po']/sum_mo:.4f}  {2*s['Be']/max(s['Pe'],1):.4f}")
print()
tv_main = tv(hist["even_sing"], hist["odd_all"])
tv_null = tv(hist["even_halfA"], hist["even_halfB"])
tv_snull = tv(hist["even_singA"], hist["even_singB"])
tv_eaoa = tv(hist["even_all"], hist["odd_all"])
tv_eas = tv(hist["even_all"], hist["even_sing"])
print("position-histogram total variation (u = (x - T(m-1))/m, 24 bins, 4 <= m < 2000):")
print(f"  TV(even-all,      odd-all)      = {tv_eaoa:.4f}   <- the raw mirror gap (pairs + any singles effect)")
print(f"  TV(even-all,      even-singles) = {tv_eas:.4f}   <- mass of the symmetric component (the pairs)")
print(f"  TV(even-singles,  odd-all)      = {tv_main:.4f}   <- THE item-7 test")
print(f"  TV(even-half A,   even-half B)  = {tv_null:.4f}   <- sampling noise scale, even primes")
print(f"  TV(even-sing A,   even-sing B)  = {tv_snull:.4f}   <- sampling noise scale, even singles")
verdict = ("MATCH within sampling noise -> the mirror gap is exactly the pairs;"
           " no parity structure in singles beyond the mirror mechanism"
           if tv_main <= 2 * max(tv_null, tv_snull) else
           "EXCEEDS noise scale -> even singles carry parity structure beyond the mirror mechanism")
print("  singles-shape verdict:", verdict)
print()
print("accidental per-layer mirror asymmetry (L1 of layer hist vs its mirror, normalized):")
for k, v in sym.items():
    v = np.array(v)
    print(f"  {k:<10} n={len(v):>4}  mean={v.mean():.4f}  median={np.median(v):.4f}")
print("  (even-all should sit far below odd-all; even-sing should match odd-all if the")
print("   mechanism account is complete — the pairs alone carry the symmetry)")
print()
print("SYMMETRY SPOT CHECK, first bins of even-all minus even-sing (should be mirror-symmetric):")
diff = hist["even_all"] - hist["even_sing"]
nd = diff.sum()
if nd:
    d = diff / nd
    print("  normalized paired-mass histogram:", " ".join(f"{x:+.3f}" for x in d))
    print("  mirror-symmetry L1:", f"{0.5*np.abs(d - d[::-1]).sum():.6f}", "(0 = exactly symmetric, by construction ~0)")
print("DONE")
