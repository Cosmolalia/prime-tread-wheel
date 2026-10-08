#!/usr/bin/env python3
"""
stagger_acf_p11.py — P11: pre-registered replication of P10 at 500k laps.

Pre-registration (INSIGHTS, cross-session bridge): the only P10 signal was a
2-4 sigma hint at lags == 2 mod 4 (ring 2's parity flip couples to mouth
width). Replication doubles the lap range to 500k and widens WMAX 150 -> 300
(max W at 50k laps was 112; censoring must not fake a null). iid arm reduced
to 4 replicates (it is only a noise baseline). Everything else identical to
stagger_acf.py so the comparison is clean.

Decision rule (written before running): the hint is REAL if the mean quad-iid
diff over lags == 2 mod 4 in {2,6,10,...,30} is > 4x the mean absolute diff
over the other lags in 1..30, AND the same sign in both halves of the lap
range. Otherwise P11 closes as NULL like P10.
"""

import math, os, random
from array import array

M_LO, M_HI = 21, 500000
HALF = (M_LO + M_HI) // 2
WMAX = 300
PSTRIKE = 2000
R_IID = 4
LAGS = list(range(1, 31))

OUT = os.path.join(os.path.dirname(__file__), "logs", "stagger_acf_p11.json")

def primes_upto(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = b"\x00" * (((n - i*i) // i) + 1)
    return [i for i in range(2, n + 1) if sieve[i]]

PRIMES = primes_upto(PSTRIKE)

def w_series(rand_offsets, m_lo, m_hi, rng):
    out = array("H", bytes(2 * (m_hi - m_lo + 1)))
    for i, m in enumerate(range(m_lo, m_hi + 1)):
        base = m * (m - 1) // 2
        cov = bytearray(WMAX + 1)
        for p in PRIMES:
            o = rng.randrange(p) if rand_offsets else (-base) % p
            q = o if o else p
            while q <= WMAX:
                cov[q] = 1
                q += p
        w = 0
        for k in range(1, WMAX + 1):
            if not cov[k]:
                w = k
                break
        out[i] = w
    return out

def acf(series, lag):
    n = len(series) - lag
    if n < 100:
        return 0.0
    mx = sum(series[:n]) / n
    my = sum(series[lag:]) / n
    num = sum((series[i] - mx) * (series[i + lag] - my) for i in range(n))
    denx = sum((series[i] - mx) ** 2 for i in range(n))
    deny = sum((series[i + lag] - my) ** 2 for i in range(n))
    return num / math.sqrt(denx * deny) if denx * deny > 0 else 0.0

def lag_stats(series, iid_avg):
    diffs = {}
    for l in LAGS:
        diffs[l] = acf(series, l) - iid_avg[l]
    hint = [l for l in LAGS if l % 4 == 2]
    rest = [l for l in LAGS if l % 4 != 2]
    m_hint = sum(diffs[l] for l in hint) / len(hint)
    m_rest = sum(abs(diffs[l]) for l in rest) / len(rest)
    return diffs, m_hint, m_rest

if __name__ == "__main__":
    import json, time
    t0 = time.time()
    print(f"P11 replication: laps {M_LO}..{M_HI}  strikers p<={PSTRIKE} ({len(PRIMES)})  WMAX={WMAX}")
    quad = w_series(False, M_LO, M_HI, None)
    print("quad W: mean=%.2f max=%d  zeros(WMAX)=%d  (%.0fs)" %
          (sum(quad)/len(quad), max(quad), sum(1 for w in quad if w == 0), time.time()-t0))

    iid_acfs = {l: 0.0 for l in LAGS}
    for r in range(R_IID):
        rng = random.Random(7000 + r)
        s = w_series(True, M_LO, M_HI, rng)
        for l in LAGS:
            iid_acfs[l] += acf(s, l) / R_IID
        print(f"  iid rep {r+1}/{R_IID} done ({time.time()-t0:.0f}s)", flush=True)

    qa = {l: acf(quad, l) for l in LAGS}
    d_all, mh_all, mr_all = lag_stats(quad, iid_acfs)
    q1 = quad[:HALF - M_LO + 1]
    q2 = quad[HALF - M_LO + 1:]
    # iid halves: reuse full-range iid avg as baseline for both halves (baseline is smooth)
    d_h1, mh1, mr1 = lag_stats(q1, iid_acfs)
    d_h2, mh2, mr2 = lag_stats(q2, iid_acfs)

    print("\nlag  quadACF   iidACF    diff   note")
    for l in LAGS:
        note = ""
        if l % 4 == 2: note = " ring2-parity <<<" if d_all[l] > 0 else " ring2-parity"
        print("%3d  %+0.4f  %+0.4f  %+0.4f %s" % (l, qa[l], iid_acfs[l], d_all[l], note))

    real = (mh_all > 4 * mr_all) and (mh1 > 0) and (mh2 > 0)
    print(f"\nP11 verdict: mean diff at lags==2 mod 4: {mh_all:+.4f} (half1 {mh1:+.4f}, half2 {mh2:+.4f})")
    print(f"  vs mean |diff| other lags: {mr_all:.4f}  ->  {'REAL (pre-registered rule met)' if real else 'NULL (rule not met)'}")

    json.dump({"laps": [M_LO, M_HI], "wmax": WMAX, "pstrike": PSTRIKE, "r_iid": R_IID,
               "quad_acf": qa, "iid_acf": iid_acfs, "diff": d_all,
               "mean_hint_lags": mh_all, "mean_abs_other": mr_all,
               "half1_hint": mh1, "half2_hint": mh2, "verdict": "REAL" if real else "NULL"},
              open(OUT, "w"), indent=1)
    print("wrote", OUT)
