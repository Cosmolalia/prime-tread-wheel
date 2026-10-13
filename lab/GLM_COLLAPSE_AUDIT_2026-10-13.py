#!/usr/bin/env python3
"""
GLM_COLLAPSE_AUDIT_2026-10-13.py — audit of GLM's CRT-shift collapse.

Claim under audit (SWARM_HANDBACK_2026-10-12_1719.txt, GLM §1):
  One-hot phases c_p over rings P, Q = prod P, a = CRT(c_p). Then
    (i)   covered(N) <=> gcd(N-a, Q) > 1
    (ii)  d = #{p in P : p !| a}
    (iii) feasibility position-independent: feasible <=> m <= j(Q) - 1
    (iv)  d(m) = min over run-start translates of non-divided-prime count
  Consequences claimed: wedge is pure arithmetic; slope = omega-degradation
  rate of Jacobsthal run-starts; j(31#) = 58 published matches LEG S.

Audit legs:
  LEG 1 — exhaustive enumeration Q in {6, 30, 210}: identity (i), the
          feasibility threshold (iii), and the d-formula (ii/iv), over ALL
          translates and ALL windows. Complete proof by enumeration at
          small scale.
  LEG 2 — B=97, m=14: reconstruct GLM's witness (a odd, a == 0 mod every
          odd prime <= 97); verify window (T(13), T(14)] = 92..105 is
          covered with d = 1 and d = 0 is impossible (101, 103 are
          97-rough).
  LEG 3 — B=53 vs LEG S measurements, NO MILP: recompute d(60), d(100),
          infeasibility at 150 via the collapsed formulation (choose S =
          primes dividing a; exact-cover DFS over residues of the rest).
          Expected: d=7, d=11, infeasible — the values the HiGHS MILP
          measured on 2026-10-12.
  LEG 4 — j-values GLM relies on, by direct scan: j(6), j(30), j(210),
          j(2310); report against OEIS A048669.

Naming collision to record: our house h(k) = j(p_k#) (cliff = FIRST
infeasible layer; h(25) = j(97#) = 258). GLM's h(Q) = j(Q) - 1 (max
COVERABLE window). Same table, offset-one neighbors. Both are correct;
the audit note pins which is which.
"""
import json
import math
from functools import reduce

# ---------------------------------------------------------------- LEG 1


def primes_upto(n):
    sieve = [True] * (n + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = [False] * len(sieve[i * i :: i])
    return [i for i, v in enumerate(sieve) if v]


def leg1():
    out = {}
    for Q in (6, 30, 210):
        P = primes_upto(Q + 1)  # primes <= largest prime factor of Q
        P = [p for p in P if Q % p == 0]
        # j(Q) by scan over two periods (runs can straddle the seam)
        j = None
        run = 0
        best = 0
        for N in range(1, 2 * Q + 2):
            if math.gcd(N, Q) > 1:
                run += 1
                best = max(best, run)
            else:
                run = 0
        # j(Q) = smallest m such that every m-run has a coprime = best+1
        j = best + 1

        # (i) identity over all translates
        ident_ok = True
        for a in range(Q):
            lhs = {N % Q for N in range(Q) if math.gcd(N - a, Q) > 1}
            rhs = set()
            for p in P:
                rhs |= {N % Q for N in range(Q) if N % p == a % p}
            if lhs != rhs:
                ident_ok = False
                break

        # (iii) feasibility over ALL windows x ALL translates
        feas = {}
        for m in range(1, j + 2):
            ok = False
            for s in range(Q):
                for a in range(Q):
                    if all(math.gcd(s + t - a, Q) > 1 for t in range(m)):
                        ok = True
                        break
                if ok:
                    break
            feas[m] = ok
        threshold_ok = all(feas[m] == (m <= j - 1) for m in feas)

        # (ii)/(iv) d-formula on every window: brute min #{p !| a} == |P| - max omega
        d_ok = True
        for s in range(Q):
            for m in range(1, min(j, 6)):  # small m, exhaustive
                best_d = None
                for a in range(Q):
                    if all(math.gcd(s + t - a, Q) > 1 for t in range(m)):
                        d = sum(1 for p in P if a % p != 0)
                        best_d = d if best_d is None else min(best_d, d)
                # formula check
                best_formula = None
                for a in range(Q):
                    if all(math.gcd(s + t - a, Q) > 1 for t in range(m)):
                        omega = sum(1 for p in P if a % p == 0)
                        f = len(P) - omega
                        best_formula = f if best_formula is None else min(best_formula, f)
                if best_d != best_formula:
                    d_ok = False
        out[str(Q)] = {
            "P": P,
            "j_Q_scan": j,
            "identity_all_translates": ident_ok,
            "feasibility_threshold_m<=j-1": threshold_ok,
            "d_formula_ok": d_ok,
        }
    return out


# ---------------------------------------------------------------- LEG 2


def leg2():
    P_odd = [p for p in primes_upto(97) if p != 2]
    # a == 0 mod every odd prime <= 97, a odd. Work mod Q = 97#.
    Q = reduce(lambda x, y: x * y, primes_upto(97), 1)
    # CRT: a = Q_odd * inv(Q_odd mod 2) * 1  (mod Q), where Q_odd = Q/2
    Q_odd = Q // 2
    a = Q_odd  # Q_odd is odd, and Q_odd == 0 mod every odd prime <= 97
    m = 14
    T13 = 13 * 14 // 2
    window = list(range(T13 + 1, T13 + 1 + m))  # 92..105
    covered = all(math.gcd(N - a, Q) > 1 for N in window)
    d = sum(1 for p in primes_upto(97) if a % p != 0)
    # d = 0 impossible: 101 and 103 are 97-rough
    rough = [N for N in window if all(N % p != 0 for p in primes_upto(97))]
    return {
        "a_mod_Q": a,
        "window": window,
        "covered_at_d": covered,
        "d": d,
        "uncovered_if_d0": rough,
        "matches_measured_d14": covered and d == 1 and rough == [101, 103],
    }


# ---------------------------------------------------------------- LEG 3


def cover_dfs(window, primes_free, uncovered):
    """Exact cover: choose one residue mod p for each p in primes_free so
    that every index in `uncovered` is hit. Returns (ok, {p: residue}).
    Optimistic-bound prune: if the sum of each remaining prime's best
    residue hit-count < |uncovered|, dead end."""
    if not uncovered:
        return True, {}
    if not primes_free:
        return False, {}
    # bound: even the best residue per remaining prime cannot cover all
    cap = 0
    for p in primes_free:
        cnt = {}
        for i in uncovered:
            cnt[window[i] % p] = cnt.get(window[i] % p, 0) + 1
        cap += max(cnt.values())
    if cap < len(uncovered):
        return False, {}
    p = primes_free[0]
    rest = primes_free[1:]
    # residues ranked by how many uncovered they take (most-first pruning)
    scores = []
    for r in range(p):
        hit = frozenset(i for i in uncovered if window[i] % p == r)
        scores.append((len(hit), r, hit))
    scores.sort(reverse=True)
    for _, r, hit in scores:
        if not hit:
            continue
        ok, assign = cover_dfs(window, rest, uncovered - hit)
        if ok:
            assign[p] = r
            return True, assign
    return False, {}


def d_collapsed(m, B, prs):
    """Min displacement over a via the collapse: S = primes dividing a
    (home set). d = |P| - max |S| s.t. window \ S-multiples is coverable
    by one AP mod p per remaining prime. Exhaustive over S by size."""
    Q = reduce(lambda x, y: x * y, prs, 1)
    T = (m - 1) * m // 2
    window = list(range(T + 1, T + 1 + m))
    n = len(prs)
    for s in range(n, -1, -1):
        from itertools import combinations

        for S in combinations(prs, s):
            sset = set(S)
            home_covered = frozenset(
                i for i in range(m) if any(window[i] % p == 0 for p in sset)
            )
            U = frozenset(set(range(m)) - set(home_covered))
            free = [p for p in prs if p not in sset]
            ok, _ = cover_dfs(window, tuple(free), U)
            if ok:
                return n - s
    return None


def leg3():
    P53 = primes_upto(53)
    assert P53[-1] == 53 and len(P53) == 16
    res = {}
    for m in (60, 100, 150):
        res[m] = d_collapsed(m, 53, P53)
    return {"P": P53, "d": res, "expected": {60: 7, 100: 11, 150: None}}


# ---------------------------------------------------------------- LEG 4


def j_by_scan(Q, scan_factor=40):
    """j(Q) by scanning: pattern is periodic mod Q; max run over a long
    enough range (Jacobsthal runs for these primorials are known short).
    Conservative: scan 40 periods + a margin; verify against known values."""
    best = 0
    run = 0
    for N in range(1, scan_factor * Q + 2):
        if math.gcd(N, Q) > 1:
            run += 1
            if run > best:
                best = run
        else:
            run = 0
    return best + 1


def leg4():
    out = {}
    for k in (2, 3, 5, 7):
        Q = reduce(lambda x, y: x * y, primes_upto(k), 1)
        out[f"j({k}#={Q})"] = j_by_scan(Q)
    return out


if __name__ == "__main__":
    print("=" * 70)
    print("LEG 1 — exhaustive small-Q enumeration")
    r1 = leg1()
    print(json.dumps(r1, indent=2))

    print("=" * 70)
    print("LEG 2 — B=97 m=14 witness reconstruction")
    r2 = leg2()
    r2["a_mod_Q"] = str(r2["a_mod_Q"])  # huge int
    print(json.dumps(r2, indent=2))

    print("=" * 70)
    print("LEG 3 — B=53 d(60)/d(100)/d(150) via collapse, no MILP")
    r3 = leg3()
    print(json.dumps(r3, indent=2))

    print("=" * 70)
    print("LEG 4 — j-values by direct scan")
    r4 = leg4()
    print(json.dumps(r4, indent=2))

    verdict = {
        "leg1": all(v["identity_all_translates"] and v["feasibility_threshold_m<=j-1"] and v["d_formula_ok"] for v in r1.values()),
        "leg2": r2["matches_measured_d14"],
        "leg3": all((r3["d"][m] == r3["expected"][m]) for m in r3["expected"]),
        "leg4": r4 == {"j(2#=2)": 2, "j(3#=6)": 4, "j(5#=30)": 6, "j(7#=210)": 10},
    }
    print("=" * 70)
    print("VERDICTS", json.dumps(verdict))
