#!/usr/bin/env python3
"""
PHASE 17 — #18 prime-layer seam-lock check (Claude's insights handoff #18).

Mechanism (decompressed 2026-10-13, [F] from audited wheel rules):
  Native 1:1 wheel: layer m = ticks T(m-1)+1 .. T(m-1)+m, T = triangular.
  Ring q occupies positions ≡ j_q (mod q); the L-build seam-locks ring q to
  its own layer: j_q = T(q-1) ≡ 0 (mod q).
  Ring q therefore "hits tick 1 of layer m"  <=>  T(m-1)+1 ≡ 0 (mod q)
                                            <=>  m^2 - m + 2 ≡ 0 (mod q).
  Discriminant = 1 - 8 = -7  =>  #roots mod q  r_q = 1 + (-7|q)  (odd q).
  => over all layers, P(hit) = r_q / q.
  On a PRIME layer m: m mod q is uniform over the q-1 NONZERO classes
  (m prime > q excludes 0); 0 is never a root of m^2-m+2 (evaluates to 2),
  so all r_q roots live in nonzero classes
  => predicted P(hit | m prime) = r_q / (q-1)  >  r_q / q.

Frozen predictions [S], written before the run:
  P1: over composite layers m > q, empirical hit-rate -> r_q/q within
      binomial 3-sigma.
  P2: over prime layers q < m, empirical hit-rate -> r_q/(q-1) within
      binomial 3-sigma.
  P3: prime/composite lift ratio -> q/(q-1) (e.g. 7/6 at q=7 — if that
      number appears it is a statistical lift, NOT dial evidence; noted in
      advance so nobody overreads it).
  P4 (exploratory, [H]): per-layer tick-1 hit-count correlates NEGATIVELY
      with the layer's prime content (more rings claiming tick 1 -> tick 1
      more composite -> fewer surviving primes on the layer).
Artifacts: lab/PHASE17_primetick1.{json,md}
"""
import json
import math

import numpy as np

M_HI = 300_000          # layer census range (hit rates)
Q_MAX = 97              # odd primes q <= Q_MAX
P4_HI = 20_000          # layer range for the prime-content correlation


def sieve_np(n):
    s = np.ones(n + 1, dtype=bool)
    s[0] = s[1] = False
    s[4::2] = False
    for p in range(3, int(n ** 0.5) + 1, 2):
        if s[p]:
            s[p * p::2 * p] = False
    return s


def primes_upto(n):
    s = sieve_np(n)
    return [i for i in range(2, n + 1) if s[i]]


def kronecker_minus7(q):
    """(-7|q) for odd prime q: 0 if q=7 (degenerate, 7 | disc);
    else =1 iff q ≡ 1,2,4 mod 7 (disc -7 form)."""
    if q == 7:
        return 0
    return 1 if q % 7 in (1, 2, 4) else -1


def main():
    primes = primes_upto(M_HI)
    is_p = sieve_np(M_HI)
    qs = [q for q in primes if q <= Q_MAX and q != 2]

    # T(m-1) mod each q, incremental: T(m) = T(m-1) + m. Loop starts at
    # m=2, which reads T(1) = 1 — NOT 0 (the m=2 iteration advanced past
    # T(0) before the first read).
    tmod = {q: 1 % q for q in qs}
    per_q = {q: {"comp_hits": 0, "comp_n": 0, "prime_hits": 0, "prime_n": 0}
             for q in qs}
    # P4: per-layer hit count vs "layer holds >= 1 prime" (layers 3..P4_HI)
    T_P4 = P4_HI * (P4_HI + 1) // 2 + 1
    is_p4 = sieve_np(T_P4)

    p4_buckets = {}  # hit_count -> [layers, layers_with_prime]

    for m in range(2, M_HI + 1):
        hit_qs = [q for q in qs
                  if m > q and (tmod[q] + 1) % q == 0]
        m_prime = bool(is_p[m])
        for q in hit_qs:
            d = per_q[q]
            if m_prime:
                d["prime_hits"] += 1
            else:
                d["comp_hits"] += 1
        for q in qs:
            if m > q:
                d = per_q[q]
                if m_prime:
                    d["prime_n"] += 1
                else:
                    d["comp_n"] += 1
        if 3 <= m <= P4_HI:
            base = m * (m - 1) // 2
            npr = int(is_p4[base + 1: base + 1 + m].sum())
            h = len(hit_qs)
            b = p4_buckets.setdefault(h, [0, 0, 0])
            b[0] += 1
            b[1] += 1 if npr > 0 else 0
            b[2] += npr
        for q in qs:
            tmod[q] = (tmod[q] + m) % q

    out = {"M_HI": M_HI, "Q_MAX": Q_MAX, "P4_HI": P4_HI, "per_q": {},
           "P4": {}, "frozen": ["P1 r_q/q on composite", "P2 r_q/(q-1) on prime",
                                "P3 lift -> q/(q-1)",
                                "P4 exploratory negative correlation"]}
    max_abs_z = 0.0
    for q in qs:
        r = 1 + kronecker_minus7(q)
        d = per_q[q]
        ch, cn = d["comp_hits"], d["comp_n"]
        ph, pn = d["prime_hits"], d["prime_n"]
        comp_rate, prime_rate = ch / cn, ph / pn
        exp_comp, exp_prime = r / q, r / (q - 1)
        sig_c = math.sqrt(exp_comp * (1 - exp_comp) / cn)
        sig_p = math.sqrt(exp_prime * (1 - exp_prime) / pn)
        # r_q = 0 (q ≡ 3,5,6 mod 7): expected rate exactly 0 — the check is
        # exact match (empirical must be 0), not a z-score.
        zc = (comp_rate - exp_comp) / sig_c if sig_c > 0 else (
            0.0 if comp_rate == 0 else float("inf"))
        zp = (prime_rate - exp_prime) / sig_p if sig_p > 0 else (
            0.0 if prime_rate == 0 else float("inf"))
        max_abs_z = max(max_abs_z, abs(zc), abs(zp))
        out["per_q"][q] = {
            "r_q": r, "exp_comp": exp_comp, "emp_comp": comp_rate,
            "z_comp": zc, "exp_prime": exp_prime, "emp_prime": prime_rate,
            "z_prime": zp,
            "lift": (prime_rate / comp_rate) if comp_rate > 0 else None,
            "exp_lift": q / (q - 1), "n_comp": cn, "n_prime": pn,
        }
    tot_l = tot_p = 0
    for h, (layers, withp, prsum) in sorted(p4_buckets.items()):
        out["P4"][h] = {"layers": layers, "with_prime": withp,
                        "frac_with_prime": withp / layers,
                        "mean_primes": prsum / layers}
        tot_l += layers
        tot_p += withp
    out["P4_overall_frac_with_prime"] = tot_p / tot_l

    json.dump(out, open("lab/PHASE17_primetick1.json", "w"), indent=1)

    print(f"M_HI={M_HI}  P4 layers 3..{P4_HI}  odd primes q <= {Q_MAX}")
    print(f"{'q':>4} {'r_q':>3} {'exp_c':>8} {'emp_c':>8} {'z_c':>6} "
          f"{'exp_p':>8} {'emp_p':>8} {'z_p':>6} {'lift':>6} {'exp_lift':>8}")
    for q in qs:
        d = out["per_q"][q]
        lift = f"{d['lift']:>6.3f}" if d["lift"] is not None else "   n/a"
        print(f"{q:>4} {d['r_q']:>3} {d['exp_comp']:>8.5f} "
              f"{d['emp_comp']:>8.5f} {d['z_comp']:>6.2f} "
              f"{d['exp_prime']:>8.5f} {d['emp_prime']:>8.5f} "
              f"{d['z_prime']:>6.2f} {lift} {d['exp_lift']:>8.4f}")
    print(f"\nmax |z| over all (q, bucket): {max_abs_z:.2f}")
    print("P4 (tick-1 hit_count -> layer prime content):")
    for h, d in out["P4"].items():
        print(f"  hits={h:>2}: frac_with_prime={d['frac_with_prime']:.4f} "
              f"mean_primes={d['mean_primes']:.3f} ({d['layers']} layers)")
    print(f"  overall: {out['P4_overall_frac_with_prime']:.4f}")


if __name__ == "__main__":
    main()
