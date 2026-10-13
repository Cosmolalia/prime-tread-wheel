#!/usr/bin/env python3
"""
ARCHIVE QUEUE — 2026-10-12. Five queued items from lab/ARCHIVE_TRIAGE_2026-10-12.md,
run as one probe with legs. Every leg has frozen expectations written BEFORE the run.

LEG Q1 — Echo Cascade audit (WhitePapers + Downloads dup). Their claim [S]:
over all 3,001,134 primes to 5e7, the 2p-1 / 2p+1 adjacency counts are
229,551 vs 229,566 (balance ratio 1.000065), with a per-decade "stability"
table decaying 64% -> 14.85% (10M-50M), decay exponent ~0.085.
Audit: reproduce the headline counts; the "stability" metric is not defined
in the corpus [G] — report our own full per-decade table instead and mark
the 0.085 exponent UNCHECKABLE as specified.
Mechanism note (frozen): for p > 3, p == 1 mod 6 forces 3 | 2p+1 and
p == 5 mod 6 forces 3 | 2p-1, so near-balance is forced by a mod-3 sieve;
the residue deviation is a prime-race effect, not a mystery.

LEG Q2 — PRIME^2 "isolated primes" (falsified as printed in triage; kernel
real). Isolated := p such that (p-1)/2, (p+1)/2, 2p-1, 2p+1 are ALL composite.
Frozen: true sequence below 1033 must begin 17, 43, 67, 71, 101, 103, 109,
127, 137 (triage hand-check). Density below 10^3 ~ 40% (their 15.4% FALSE);
heuristic 1 - 4/ln p is approximate [S] (the four events are not
independent: (p-1)/2 and (p+1)/2 are consecutive integers, both odd, differ
by 1 -> cannot both be prime; likewise 2p-1, 2p+1).

LEG Q3 — Knockout wall profile (ancestor probe probes/knockout_test.py,
already implemented, M=3000; this leg re-runs it and captures rows).
Frozen expectations from PAPER.md §7: ~50% of sub-sqrt gears ever needed;
largest-needed / sqrt ~ 0.98 by layers 2000-3000; share not special to the
wheel (any interval that short shows the same).

LEG Q4 — Chained double-shot census (Wheel Atlas fact 10). Spoke a/b (reduced,
angle a/b of a turn): its numbers are N(t) = (b^2 t^2 - b t)/2 + a t, so
N1 = N(1), N2 = N(2) = 2*N1 + b^2 (the two "shots"; atlas: a channel carries
at most two primes). Atlas claim [S]: among spokes with denominators up to
2000, 10,062 have both shots prime.
Frozen mechanism: b even => N2 = 2*N1 + b^2 even > 2 => composite. So ALL
double-prime spokes have b ODD [F]. If the atlas count includes even-b
spokes, it is wrong by construction.
Frozen predictions (pre-registered, spokes 1 <= a <= b, gcd(a,b)=1,
b = 2..2000):
  P-naiive: E0 = sum 1/(ln N1 * ln N2) over b odd.
  P-BH:    EBH = sum 2*C2*prod_{l|b, l odd} (l-1)/(l-2) / (ln N1 * ln N2)
           over b odd, C2 = twin-prime constant ~ 0.6601618.
Convention variants reported to identify theirs: (i) 1 <= a <  b,
(ii) 1 <= a <= b (includes the seam spoke a = b).

LEG Q5 — Hooley 1965 [E]: gaps between integers coprime to the primorial
N_k = 2*3*...*p_k are exponential, CDF f(c) = (1+o(1))(1 - e^-c) with
c = gap / mean_gap, over one full period [1, N_k].
Frozen PASS: for k = 7 (N = 510510) and k = 8 (N = 9699690), KS distance
between empirical CDF of normalized gaps and 1 - e^-c is < 2/sqrt(n).
This is the [E] benchmark the dial-census / Jacobsthal gap work compares
against; it was MISSING from lab/LITERATURE_SWEEP_2026-10-10.md.

Output: prints a leg-by-leg report, writes lab/ARCHIVE_Q_2026-10-12.json.
"""
import json
import math
import time
from math import gcd, isqrt, log

t_start = time.time()
OUT = {}


def sieve(n):
    """bytearray composite sieve, slice-assignment style (house convention)."""
    comp = bytearray(n + 1)
    if n >= 0:
        comp[0] = 1
    if n >= 1:
        comp[1] = 1
    for p in range(2, isqrt(n) + 1):
        if not comp[p]:
            comp[p * p::p] = b'\x01' * (((n - p * p) // p) + 1)
    return comp


# ---------------------------------------------------------------- Q1
print("=" * 70)
print("LEG Q1 — Echo Cascade audit (2p±1 adjacency, primes to 5e7)")
LIMIT_Q1 = 50_000_000
comp = sieve(LIMIT_Q1)
D = 2 * LIMIT_Q1 + 2
comp2 = sieve(D)

primes = [p for p in range(2, LIMIT_Q1 + 1) if not comp[p]]
n_primes = len(primes)
m1 = sum(1 for p in primes if p >= 3 and not comp2[2 * p - 1])
p1 = sum(1 for p in primes if not comp2[2 * p + 1])
both = sum(1 for p in primes if p >= 3 and not comp2[2 * p - 1] and not comp2[2 * p + 1])
either = m1 + p1 - both
print(f"pi(5e7)            = {n_primes}   (their claim: 3,001,134)")
print(f"2p-1 prime count   = {m1}   (their claim: 229,551)")
print(f"2p+1 prime count   = {p1}   (their claim: 229,566)")
print(f"balance (2p+1)/(2p-1) = {p1/m1:.6f}   (their claim: 1.000065)")
print(f"both prime         = {both}   either = {either}")
print("per-decade table (p in [10^k, 10^(k+1)) ):")
dec = {}
for p in primes:
    if p < 10:
        continue
    k = int(math.log10(p))
    e = dec.setdefault(k, [0, 0, 0])
    e[0] += 1
    if p >= 3 and not comp2[2 * p - 1]:
        e[1] += 1
    if not comp2[2 * p + 1]:
        e[2] += 1
for k in sorted(dec):
    n, a, b = dec[k]
    print(f"  1e{k:<2}: primes {n:>9,} | 2p-1 {a:>8,} ({a/n:.4f}) | "
          f"2p+1 {b:>8,} ({b/n:.4f}) | balance {b/a if a else 0:.5f}")
# mod-3 forced-composite accounting (frozen mechanism)
forced_m1 = sum(1 for p in primes if p > 3 and p % 6 == 5)   # 3 | 2p-1
forced_p1 = sum(1 for p in primes if p > 3 and p % 6 == 1)   # 3 | 2p+1
print(f"mod-3 forced composites: 2p-1 side {forced_m1:,}, 2p+1 side {forced_p1:,}")
print("(their per-decade 'stability' metric is undefined in the corpus [G];")
print(" our table above is the auditable content; decay exponent 0.085 UNCHECKABLE)")
OUT["Q1_echo_cascade"] = {
    "pi_5e7": n_primes, "claim_pi": 3001134,
    "count_2pm1": m1, "claim_2pm1": 229551,
    "count_2pp1": p1, "claim_2pp1": 229566,
    "balance": p1 / m1, "claim_balance": 1.000065,
    "both": both, "either": either,
    "forced_composites_mod3": {"2pm1": forced_m1, "2pp1": forced_p1},
    "per_decade": {str(k): dec[k] for k in sorted(dec)},
}
del comp, comp2, primes

# ---------------------------------------------------------------- Q2
print("=" * 70)
print("LEG Q2 — PRIME^2 isolated-prime census (kernel real, paper falsified)")
L2 = 10_000_000
comp = sieve(2 * L2 + 2)
seq_expect = [17, 43, 67, 71, 101, 103, 109, 127, 137]


def isolated(p):
    return (comp[(p - 1) // 2] and comp[(p + 1) // 2]
            and comp[2 * p - 1] and comp[2 * p + 1])


seq = [p for p in range(5, 1034) if not comp[p] and isolated(p)]
print(f"sequence below 1033: {seq}")
print(f"matches triage hand-check {seq_expect}: {seq[:len(seq_expect)] == seq_expect}")
dens = {}
for k in range(3, 8):
    lo, hi = 10 ** k, 10 ** (k + 1)
    if hi > L2:
        break
    ps = [p for p in range(max(lo, 5), hi) if not comp[p]]
    iso = sum(1 for p in ps if isolated(p))
    mid = (lo + hi) / 2
    dens[k] = [len(ps), iso, iso / len(ps), 1 - 4 / log(mid)]
    print(f"  below 1e{k+1}: primes {len(ps):>8,} isolated {iso:>8,} "
          f"density {iso/len(ps):.4f} | heuristic 1-4/ln p = {1-4/log(mid):.4f}")
OUT["Q2_isolated_primes"] = {"sequence_below_1033": seq,
                             "matches_triage": seq[:len(seq_expect)] == seq_expect,
                             "density": {str(k): dens[k] for k in dens}}
del comp

# ---------------------------------------------------------------- Q3
print("=" * 70)
print("LEG Q3 — knockout wall profile (re-running probes/knockout_test.py, M=3000)")
import statistics as st
M = 3000
spf = list(range(M * (M + 1) // 2 + 1))
for i in range(2, int((M * (M + 1) // 2 + 1) ** 0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, M * (M + 1) // 2 + 1, i):
            if spf[j] == j:
                spf[j] = i
PR = [p for p in range(2, M) if spf[p] == p]
rows = []
for m in range(10, M + 1):
    base = (m - 1) * m // 2
    top = base + m
    r = isqrt(top)
    seats = [base + k for k in range(1, m + 1)
             if (gcd(k, m) == 1 and m % 4 != 2) or (gcd(k, m) == 2 and (m // 2) % 2 == 1)]
    needed = {spf[x] for x in seats if spf[x] != x}
    allp = [p for p in PR if p <= r]
    rows.append((m, len(allp), len(needed), max(needed) / r if needed else 0))
q3 = {}
for lo, hi in [(10, 100), (100, 500), (500, 1000), (1000, 2000), (2000, 3001)]:
    sel = [x for x in rows if lo <= x[0] < hi]
    line = (f"layers {lo:>4}-{hi-1:<4}: gears to sqrt {st.mean(x[1] for x in sel):6.1f} | "
            f"needed {st.mean(x[2] for x in sel):6.1f} | share "
            f"{st.mean(x[2]/x[1] for x in sel):.2f} | biggest needed / sqrt "
            f"{st.mean(x[3] for x in sel):.3f} (lowest {min(x[3] for x in sel):.3f})")
    print("  " + line)
    q3[f"{lo}-{hi-1}"] = {"gears_to_sqrt": st.mean(x[1] for x in sel),
                          "needed": st.mean(x[2] for x in sel),
                          "share": st.mean(x[2] / x[1] for x in sel),
                          "biggest_over_sqrt": st.mean(x[3] for x in sel),
                          "lowest_biggest_over_sqrt": min(x[3] for x in sel)}
OUT["Q3_knockout_wall"] = q3

# ---------------------------------------------------------------- Q4
print("=" * 70)
print("LEG Q4 — chained double-shot census (Atlas fact 10, claim: 10,062)")
BMAX = 2000
top4 = 2 * ((BMAX * BMAX - BMAX) // 2 + BMAX) + BMAX * BMAX + 4
comp = sieve(top4)
C2 = 0.6601618158468696  # twin-prime constant


def sing_series(b):
    s = 2.0 * C2
    for l in PR:
        if l > b:
            break
        if b % l == 0:
            s *= (l - 1) / (l - 2)
    return s


counts = {"a_lt_b": 0, "a_le_b": 0, "odd_b_only": 0}
pred_naiive = 0.0
pred_bh = 0.0
for b in range(2, BMAX + 1):
    ss = sing_series(b) if b % 2 == 1 else 0.0
    for a in range(1, b + 1):
        if gcd(a, b) != 1:
            continue
        n1 = (b * b - b) // 2 + a
        n2 = 2 * n1 + b * b
        if not comp[n1] and not comp[n2]:
            counts["a_le_b"] += 1
            if b % 2 == 1:
                counts["odd_b_only"] += 1
            if a < b:
                counts["a_lt_b"] += 1
        if b % 2 == 1:
            w = 1.0 / (log(n1) * log(n2))
            pred_naiive += w
            pred_bh += ss * w
print(f"double-prime spokes, conventions: {counts}")
print(f"atlas claim: 10,062 (denominators up to 2,000)")
print(f"frozen BH predictions: naiive E0 = {pred_naiive:,.0f} | singular-series EBH = {pred_bh:,.0f}")
OUT["Q4_double_shot"] = {"counts": counts, "claim": 10062,
                         "pred_naiive": pred_naiive, "pred_bh": pred_bh}

# ---------------------------------------------------------------- Q5
print("=" * 70)
print("LEG Q5 — Hooley 1965 exponential gap law for primorial-coprime integers")
PRIMES_SMALL = [p for p in range(2, 30) if all(p % q for q in range(2, isqrt(p) + 1))]
q5 = {}
for k in [6, 7, 8]:
    pk = PRIMES_SMALL[k - 1]
    N = 1
    for l in PRIMES_SMALL[:k]:
        N *= l
    phi = 1
    for l in PRIMES_SMALL[:k]:
        phi *= l - 1
    cop = bytearray(N + 1)
    cop[:] = b'\x01' * (N + 1)
    cop[0] = 0
    for l in PRIMES_SMALL[:k]:
        cop[::l] = b'\x00' * (N // l + 1)
    res = [i for i in range(1, N + 1) if cop[i]]
    gaps = [res[i + 1] - res[i] for i in range(len(res) - 1)]
    gaps.append(res[0] + N - res[-1])  # wrap gap across the period
    mean = N / phi
    n = len(gaps)
    cg = sorted(g / mean for g in gaps)
    # KS distance vs 1 - e^-c
    ks = max(max(i / n - (1 - math.exp(-c)), (1 - math.exp(-c)) - (i - 1) / n)
             for i, c in enumerate(cg, start=1))
    thr = 2 / math.sqrt(n)
    print(f"  k={k} N_k={N:,} phi={phi:,} mean_gap={mean:.3f} n={n:,}")
    for c0 in [0.25, 0.5, 1.0, 2.0]:
        emp = sum(1 for c in cg if c <= c0) / n
        print(f"    c={c0:>4}: empirical {emp:.5f} | Hooley 1-e^-c {1-math.exp(-c0):.5f}")
    print(f"    KS = {ks:.5f} | threshold 2/sqrt(n) = {thr:.5f} -> "
          f"{'PASS' if ks < thr else 'FAIL'}")
    q5[f"k{k}"] = {"N": N, "phi": phi, "mean_gap": mean, "n_gaps": n,
                   "ks": ks, "ks_threshold": thr, "pass": bool(ks < thr)}
OUT["Q5_hooley"] = q5

print("=" * 70)
print(f"total wall time {time.time() - t_start:.1f}s")
with open("lab/ARCHIVE_Q_2026-10-12.json", "w") as f:
    json.dump(OUT, f, indent=1)
print("wrote lab/ARCHIVE_Q_2026-10-12.json")
