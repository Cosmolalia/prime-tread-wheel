#!/usr/bin/env python3
"""
stagger_acf.py — P10: the quadratic counter's fingerprint in mouth width.

Cross-session probe (Kimi x Claude handoff). The stagger law says every
ring's realized phase across laps is o_p(m) = -T(m-1) mod p, period p.
So laps m and m+p share ring p's phase EXACTLY; under an iid-lap null
(no counter; each lap's phases rolled independently) no lag shares
anything. The mouth width W(m) (first candidate tick from the seam) is
the value side's response to the cover. Question: does W(m) keep a
lagged memory of the shared phases — excess autocorrelation at prime
lags (and 4, ring 2's period) — and does an iid-lap null show none?

Model per lap m: candidate k  <=>  k mod p != base mod p for all
striker primes p <= PSTRIKE, where base = T(m-1).
W(m) = first candidate k >= 1 (0 if none in window).

NOTE: no seat test (gcd(k,m)==1). The seat test is wheel PATTERN,
not value compositeness; applying it to a value-side model blinds it
exactly on m = 2 mod 4 laps (see INSIGHTS: seat-primes identically
zero there). This probe discriminates stagger laws, so both arms must
differ ONLY in the offset law.

Two series, same laps, same seat test:
  quad: offsets from the real counter  o_p = (-base) mod p
  iid : offsets rolled uniform per lap
If quad ACF(lag) > iid ACF(lag) at prime lags, the single counter is
visible in the value-side response; the routing wall is then "how the
cover memory survives contact with hole compositeness", not "whether
the cover has memory".
"""

import math
from array import array

M_LO, M_HI = 21, 50000
WMAX = 150
PSTRIKE = 2000
R_IID = 8          # iid replicates, averaged
LAGS = list(range(1, 31))

def primes_upto(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = b"\x00" * (((n - i*i) // i) + 1)
    return [i for i in range(2, n + 1) if sieve[i]]

PRIMES = [p for p in primes_upto(PSTRIKE)]

def w_series(rand_offsets):
    """W(m) for m in [M_LO, M_HI]. rand_offsets=None -> real counter."""
    import random
    rng = random.Random(20261008)
    out = array("H", bytes(2 * (M_HI - M_LO + 1)))
    marks = []
    for i, m in enumerate(range(M_LO, M_HI + 1)):
        base = m * (m - 1) // 2
        cov = bytearray(WMAX + 1)
        for p in PRIMES:
            if rand_offsets:
                o = rng.randrange(p)
            else:
                o = (-base) % p
            q = o if o else p          # tick positions o, o+p, ... in [1, WMAX]
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

if __name__ == "__main__":
    print(f"laps {M_LO}..{M_HI}  strikers p<={PSTRIKE} ({len(PRIMES)})  WMAX={WMAX}")
    quad = w_series(False)
    print("quad W: mean=%.2f max=%d  zeros(WMAX)=%d" %
          (sum(quad)/len(quad), max(quad), sum(1 for w in quad if w == 0)))
    iid_acfs = {l: 0.0 for l in LAGS}
    for r in range(R_IID):
        s = w_series(True)
        for l in LAGS:
            iid_acfs[l] += acf(s, l) / R_IID
    PR = set(primes_upto(29))
    print("\nlag  quadACF   iidACF    diff   note")
    for l in LAGS:
        q = acf(quad, l)
        d = q - iid_acfs[l]
        note = ""
        if l in PR: note += " PRIME"
        if l == 4:  note += " ring2-period"
        if l in PR or l == 4:
            note += "  <<<" if d > 0.01 else ""
        print("%3d  %+0.4f  %+0.4f  %+0.4f %s" % (l, q, iid_acfs[l], d, note))
