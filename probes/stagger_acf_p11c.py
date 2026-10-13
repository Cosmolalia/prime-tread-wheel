#!/usr/bin/env python3
"""
stagger_acf_p11c.py — P11 re-adjudication after the frozen-text conflict (GLM flag).

Conflict found in the record:
  INSIGHTS pre-reg (queued entry): "mean ACF diff at lags == 2 mod 4 is NEGATIVE,
      each at >= 3 SE"  -> under this reading the measured -0.0073 PASSES (sign
      matches; |mean| ~4.6 sigma under lag-independence).
  Frozen script decision rule: "REAL if mh_all > 4 * mr_all (mr_all = mean of
      ABSOLUTE diffs, always positive) AND same sign in both halves" -> this
      formulation can only fire on a POSITIVE mean; measured is negative, so
      the coded rule FAILED P11 regardless of effect size.

This probe does NOT pick a winner. It runs the correct null first
(null-before-signal, per relay): is the stable negative lag-(2 mod 4) ACF diff
an artifact of deterministic ring-2 phase-class mean differences leaking into
same-class lags, or does it survive parity stratification?

Outputs (logs/stagger_acf_p11c.json):
  - reproduction of the P11 headline numbers from the same deterministic quad arm
  - parity-stratified null: 200 surrogates = independent within-mod-4-class shuffle
    (preserves phase-class marginals, destroys within-class serial structure)
  - plain shuffle null for reference
Verdict logic: report where the observed mh sits in each null distribution.
No PASS/FAIL label imposed; the relay decides.
"""

import math, os, random, json, time
from array import array

M_LO, M_HI = 21, 500000
WMAX = 300
PSTRIKE = 2000
LAGS = list(range(1, 31))
HINT = [l for l in LAGS if l % 4 == 2]
REST = [l for l in LAGS if l % 4 != 2]
OUT = os.path.join(os.path.dirname(__file__), "logs", "stagger_acf_p11c.json")

def primes_upto(n):
    s = bytearray([1]) * (n + 1); s[:2] = b"\0\0"
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i*i::i] = b"\0" * (((n - i*i) // i) + 1)
    return [i for i in range(2, n + 1) if s[i]]

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

def mh_stat(series, iid_avg):
    diffs = [acf(series, l) - iid_avg[l] for l in LAGS]
    mh = sum(diffs[l - 1] for l in HINT) / len(HINT)
    mr = sum(abs(diffs[l - 1]) for l in REST) / len(REST)
    return mh, mr

if __name__ == "__main__":
    t0 = time.time()
    quad = w_series(False, M_LO, M_HI, None)
    n = len(quad)
    print(f"quad W series: {n} laps, mean={sum(quad)/n:.2f} ({time.time()-t0:.0f}s)", flush=True)

    R_IID = 4
    iid_acfs = {l: 0.0 for l in LAGS}
    for r in range(R_IID):
        rng = random.Random(7000 + r)
        s = w_series(True, M_LO, M_HI, rng)
        for l in LAGS:
            iid_acfs[l] += acf(s, l) / R_IID
    print(f"iid baseline done ({time.time()-t0:.0f}s)", flush=True)

    mh_obs, mr_obs = mh_stat(quad, iid_acfs)
    # phase-class marginals (m mod 4) of the quad arm
    classes = [[quad[i] for i in range(c, n, 4)] for c in range(4)]

    # null 1: parity-stratified shuffle — permute independently inside each mod-4 class
    rng = random.Random(424242)
    mh_strat, mh_plain = [], []
    idx_by_class = [list(range(c, n, 4)) for c in range(4)]
    for rep in range(200):
        sur = array("H", quad)  # copy
        for c in range(4):
            vals = [quad[i] for i in idx_by_class[c]]
            rng.shuffle(vals)
            for i, v in zip(idx_by_class[c], vals):
                sur[i] = v
        mh_s, _ = mh_stat(sur, iid_acfs)
        mh_strat.append(mh_s)
        # null 2: plain global shuffle
        vals = list(quad)
        rng.shuffle(vals)
        mh_p, _ = mh_stat(array("H", vals), iid_acfs)
        mh_plain.append(mh_p)
        if (rep + 1) % 50 == 0:
            print(f"  surrogates {rep+1}/200 ({time.time()-t0:.0f}s)", flush=True)

    def summarize(null):
        null_sorted = sorted(null)
        mean = sum(null) / len(null)
        sd = math.sqrt(sum((x - mean) ** 2 for x in null) / len(null))
        # two-sided empirical p for the observed mh
        p = sum(1 for x in null if abs(x) >= abs(mh_obs)) / len(null)
        return {"null_mean": mean, "null_sd": sd, "obs": mh_obs,
                "z": (mh_obs - mean) / sd if sd else None,
                "two_sided_emp_p": p,
                "q025": null_sorted[len(null)//40], "q975": null_sorted[-len(null)//40]}

    res = {
        "m_lo": M_LO, "m_hi": M_HI, "wmax": WMAX,
        "mh_observed": mh_obs, "mr_observed": mr_obs,
        "class_means": [sum(c)/len(c) for c in classes],
        "class_sds": [math.sqrt(sum((v-sum(c)/len(c))**2 for v in c)/len(c)) for c in classes],
        "null_parity_stratified": summarize(mh_strat),
        "null_plain_shuffle": summarize(mh_plain),
        "frozen_rule_coded": {"requires": "positive (mh_all > 4*mr_all, mr_all>0)", "fires_on_negative": False},
        "frozen_rule_insights_prereg": {"requires": "negative, >= 3 SE"},
        "seconds": round(time.time() - t0, 1),
    }
    json.dump(res, open(OUT, "w"), indent=1)
    print(json.dumps(res["null_parity_stratified"], indent=1))
    print(json.dumps(res["null_plain_shuffle"], indent=1))
    print("wrote", OUT)
