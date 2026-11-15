#!/usr/bin/env python3
"""Solver-free, exact-integer dual certificate verifier for Prime Tread Wheel m=1500.

Uses ONLY the Python 3 standard library and exact arbitrary-precision integer
arithmetic (zero floating-point operations in the verification path, zero solver
in the trusted computing base).

Mathematical Certificate Identity [F]:
--------------------------------------
Fix window m = 1500, T = m(m-1)/2 = 1,124,250, and the 177 prime rings
p <= floor(sqrt(T)) = 1060. Suppose a subset of rings P_fixed has fixed phases
c_p in {0, 1, ..., p-1}, and let P_free be the remaining unpinned rings.

For any valid covering (c_p) agreeing with P_fixed, let y_p in {0, 1} indicate
whether ring p in P_free rotates to a nonzero phase c_p in {1, ..., p-1}.
Every tick k in {1, ..., m} NOT already covered by P_fixed must satisfy:

    sum_{p in F_free(k)} (1 - y_p) + sum_{p in P_free \ F_free(k)} x_{p, (T+k) mod p} >= 1

where F_free(k) = {p in P_free : p | (T+k)} and f_free(k) = |F_free(k)|.

Multiplying each uncovered tick k by a non-negative integer weight u_k >= 0
(and setting u_k = 0 on ticks already covered by P_fixed), summing over k,
and using the exact integer identity valid for all y_p in {0, 1} and D > 0:

    D * y_p + max(0, max_{c=1..p-1} W_p(c) - W_p(0) - D) >= (W_p(c_p) - W_p(0)) * y_p

where W_p(c) = sum_{k: (T+k) == c (mod p)} u_k, yields the exact integer bound:

    D * (sum_{p in P_fixed, c_p != 0} 1 + sum_{p in P_free} y_p) >= TotalNum(u, D)

where:
    TotalNum(u, D) = D * |{p in P_fixed : c_p != 0}|
                     + sum_{k=1}^m (1 - f_free(k)) * u_k
                     - sum_{p in P_free} max(0, max_{c=1..p-1} W_p(c) - W_p(0) - D).

Since the total number of rotated rings is an integer, ceiling division
    LB = (TotalNum(u, D) + D - 1) // D
is a 100% solver-free, exact-integer lower bound on that branch.
"""

import json
import math
import pathlib
import sys


def sieve(n: int) -> list[int]:
    s = [True] * (n + 1)
    s[0] = s[1] = False
    for i in range(2, math.isqrt(n) + 1):
        if s[i]:
            for j in range(i * i, n + 1, i):
                s[j] = False
    return [i for i, v in enumerate(s) if v]


def verify_branch(m: int, T: int, primes: list[int], branch: dict) -> tuple[int, int, int]:
    D = int(branch["D"])
    if D <= 0:
        raise ValueError("Scale factor D must be a positive integer")

    fixed_phases = {int(k): int(v) for k, v in branch["fixed_phases"].items()}
    prime_set = set(primes)
    for p, c in fixed_phases.items():
        if p not in prime_set:
            raise ValueError(f"Fixed prime {p} is not in the 177-ring wheel")
        if not (0 <= c < p):
            raise ValueError(f"Invalid phase {c} for prime {p}")

    u_int = [0] * m
    for k_str, val in branch["u_sparse"].items():
        k = int(k_str)
        v = int(val)
        if not (1 <= k <= m):
            raise ValueError(f"Tick index {k} out of range 1..{m}")
        if v < 0:
            raise ValueError(f"Negative dual weight u[{k}] = {v}")
        u_int[k - 1] = v

    free_primes = [p for p in primes if p not in fixed_phases]
    base_cost = sum(1 for c in fixed_phases.values() if c != 0)

    # 1. Verify no positive weight u_k sits on a tick already covered by fixed_phases,
    #    and accumulate sum_{k=1}^m (1 - f_free(k)) * u_k in exact integer arithmetic.
    rhs_num = 0
    for k in range(1, m + 1):
        uk = u_int[k - 1]
        if uk == 0:
            continue
        val = T + k
        for p, c in fixed_phases.items():
            if val % p == c:
                raise AssertionError(
                    f"Tick k={k} (T+k={val}) has u_k={uk} > 0 but is already covered by fixed p={p}, c={c}"
                )
        f_free_k = sum(1 for p in free_primes if val % p == 0)
        rhs_num += (1 - f_free_k) * uk

    # 2. For each free prime p, compute residue weights W_p(c) and surplus penalty.
    penalty_num = 0
    for p in free_primes:
        W = [0] * p
        for k in range(1, m + 1):
            uk = u_int[k - 1]
            if uk:
                W[(T + k) % p] += uk
        max_nonzero = max(W[1:])
        surplus = max_nonzero - W[0] - D
        if surplus > 0:
            penalty_num += surplus

    total_num = base_cost * D + rhs_num - penalty_num
    cert_lb = (total_num + D - 1) // D
    return cert_lb, total_num, D


def verify_exhaustive_partition(branches: list[dict]) -> tuple[dict[int, int], list[int]]:
    """Verify that a multi-branch theorem forms a complete Cartesian partition
    over the branched primes on top of a single identical baseline of pinned rings."""
    key_sets = [set(int(k) for k in b["fixed_phases"].keys()) for b in branches]
    common_keys = set.intersection(*key_sets)
    all_keys = set.union(*key_sets)
    if common_keys != all_keys:
        raise AssertionError("Branches do not fix the same set of primes")

    varying_primes = []
    common_baseline = {}
    for p in sorted(all_keys):
        vals = {int(b["fixed_phases"][str(p)]) for b in branches}
        if len(vals) == 1:
            common_baseline[p] = next(iter(vals))
        else:
            varying_primes.append(p)

    # Every varying prime p must cover all residue classes {0, 1, ..., p-1}
    # in a full Cartesian product of size prod(p for p in varying_primes).
    expected_tuples = 1
    for p in varying_primes:
        expected_tuples *= p

    seen_tuples = set()
    for b in branches:
        tup = tuple(int(b["fixed_phases"][str(p)]) for p in varying_primes)
        for p, c in zip(varying_primes, tup):
            if not (0 <= c < p):
                raise AssertionError(f"Out of range branch phase c={c} for p={p}")
        seen_tuples.add(tup)

    if len(seen_tuples) != expected_tuples or len(branches) != expected_tuples:
        raise AssertionError(
            f"Incomplete case split on {varying_primes}: expected {expected_tuples} distinct tuples, got {len(seen_tuples)}"
        )
    return common_baseline, varying_primes


def main() -> None:
    cert_path = (
        pathlib.Path(sys.argv[1])
        if len(sys.argv) > 1
        else pathlib.Path(__file__).with_name("dual_certificates_m1500.json")
    )
    data = json.loads(cert_path.read_text())

    m = 1500
    T = m * (m - 1) // 2
    primes = sieve(math.isqrt(T))
    assert T == 1124250 and len(primes) == 177, "Canonical m=1500 wheel check failed"

    all_passed = True
    summary = {}

    for thm_name, thm in data["theorems"].items():
        target_lb = int(thm["target_lb"])
        branches = thm["branches"]
        baseline, varying = verify_exhaustive_partition(branches)

        branch_results = []
        min_lb = None
        for idx, b in enumerate(branches):
            lb, total_num, D = verify_branch(m, T, primes, b)
            min_lb = lb if min_lb is None else min(min_lb, lb)
            var_assign = {p: int(b["fixed_phases"][str(p)]) for p in varying}
            branch_results.append(
                {
                    "branch": idx,
                    "varying": var_assign,
                    "exact_ratio": f"{total_num}/{D}",
                    "decimal_approx": round(total_num / D, 6),
                    "certified_int_lb": lb,
                }
            )

        passed = min_lb is not None and min_lb >= target_lb
        if not passed:
            all_passed = False

        summary[thm_name] = {
            "pinned_rotated_rings": sum(1 for c in baseline.values() if c != 0),
            "pinned_home_rings": sum(1 for c in baseline.values() if c == 0),
            "free_rings": len(primes) - len(baseline),
            "exhaustive_case_split_primes": varying,
            "num_branches": len(branches),
            "target_lb": target_lb,
            "certified_min_lb": min_lb,
            "VERDICT": "PASS" if passed else "FAIL",
            "branches": branch_results,
        }

    out = {
        "certificate_file": str(cert_path),
        "m": m,
        "T": T,
        "wheel_rings": len(primes),
        "OVERALL_VERDICT": "PASS" if all_passed else "FAIL",
        "theorems": summary,
    }
    print(json.dumps(out, indent=2))
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
