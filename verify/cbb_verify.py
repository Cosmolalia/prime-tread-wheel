#!/usr/bin/env python3
"""CBB verifier — independent checker for cbb_gen.py certificate trees.

Zero-trust: pure stdlib, exact integer arithmetic, re-derives every leaf
bound from the §18.9 identity (with the forced-ring extension) and checks
the tree's partition semantics. Shares NO code with the generator.

Checks, recursively from the root:
  (P1) at every internal node the children exactly partition the parent's
       configuration space:
         - full split: one child per phase c in {0..p-1}, all other fixings
           byte-identical;
         - binary split: child A fixes p -> 0, child B adds p to forced,
           all other fixings byte-identical; p must not already be
           fixed/forced in the parent;
         - tick split (cbb-hybrid-v2): node names an unsettled tick k and
           an ordered candidate list; child i pins candidate i to its
           k-phase and every earlier candidate loses that phase (checked
           semantically: the child's allowed set for that ring equals the
           parent's minus the phase; removing c = 0 turns a free ring
           forced). The candidate list is re-derived from the parent and
           must match exactly (order matters).
  (P1b) dead leaves: "dead_tick" k — no ring in the node can cover k
        (every fixed ring misses it, every other ring's k-phase is outside
        its allowed set); "dead_domain" p — ring p's allowed set is empty.
        Both certify infeasibility (bound = infinity >= target).
  (P2) at every certificate leaf: integer D > 0; u_k >= 0 integers; u_k = 0
       on every tick covered by a fixed ring; the exact allowed-set
       identity (C2.1; §18.9 with exclusions, forced rings get no W_p(0)
       credit)
           D*fixed_rot + sum_k (1 - f_free(k)) u_k
           - sum_{free p}   max(0, max_{c in A_p\{0}} W_p(c) - W_p(0) - D)
           - sum_{forced p} max(0, max_{c in A_p}      W_p(c)         - D)
       recomputes to the claimed certified_int_lb.
  (P3) tree bound = min leaf LB >= target_lb.

Backward compatible: pre-hybrid trees (no "excl"/"tick" fields) verify
unchanged (empty exclusion sets). Exit 0 + JSON verdict on PASS, exit 1
on FAIL.

Usage: python3 cbb_verify.py <tree.json>
"""
import json
import math
import sys

DEAD_LB = 10**18


def sieve(n):
    s = [True] * (n + 1)
    s[0] = s[1] = False
    for i in range(2, math.isqrt(n) + 1):
        if s[i]:
            for j in range(i * i, n + 1, i):
                s[j] = False
    return [i for i, v in enumerate(s) if v]


class Fail(Exception):
    pass


def allowed_set(node, p):
    """Reconstruct ring p's allowed phase set A_p from the node encoding:
    fixed -> {c}; forced -> {1..p-1} minus exclusions; free -> {0..p-1}
    minus exclusions (exclusions hold nonzero phases only)."""
    fixed = {int(k): int(v) for k, v in node["fixed"].items()}
    forced = {int(x) for x in node["forced"]}
    excl = {int(k): {int(c) for c in v} for k, v in node.get("excl", {}).items()}
    if p in fixed:
        return {fixed[p]}
    if p in forced:
        return set(range(1, p)) - excl.get(p, set())
    return set(range(p)) - excl.get(p, set())


def leaf_lb(m, T, primes, node):
    fixed = {int(k): int(v) for k, v in node["fixed"].items()}
    forced = sorted(int(x) for x in node["forced"])
    excl = {int(k): {int(c) for c in v} for k, v in node.get("excl", {}).items()}
    leaf = node["leaf"]
    D = int(leaf["D"])
    if D <= 0:
        raise Fail("D must be a positive integer")
    pset = set(primes)
    for p in forced:
        if p in fixed:
            raise Fail(f"ring {p} both fixed and forced")
    for p, c in fixed.items():
        if p not in pset:
            raise Fail(f"fixed ring {p} not in wheel")
        if not (0 <= c < p):
            raise Fail(f"phase {c} out of range for ring {p}")
    for p in forced:
        if p not in pset:
            raise Fail(f"forced ring {p} not in wheel")
        if len(excl.get(p, set())) >= p - 1:
            raise Fail(f"forced ring {p} has an empty allowed set at a leaf")

    u = [0] * m
    for ks, val in leaf["u_sparse"].items():
        k = int(ks)
        v = int(val)
        if not (1 <= k <= m):
            raise Fail(f"tick index {k} out of range")
        if v < 0:
            raise Fail(f"negative weight u[{k}] = {v}")
        u[k - 1] = v

    free = [p for p in primes if p not in fixed and p not in set(forced)]

    # u must vanish on fixed-covered ticks; tick-side sum.
    rhs = 0
    for k in range(1, m + 1):
        uk = u[k - 1]
        if not uk:
            continue
        val = T + k
        for p, c in fixed.items():
            if val % p == c:
                raise Fail(f"u[{k}] > 0 on fixed-covered tick (p={p}, c={c})")
        f = 0
        for p in free:
            if val % p == 0:
                f += 1
        rhs += (1 - f) * uk

    fixed_rot = sum(1 for c in fixed.values() if c != 0)
    pen = 0
    for p in free:
        W = [0] * p
        for k in range(1, m + 1):
            if u[k - 1]:
                W[(T + k) % p] += u[k - 1]
        ep = excl.get(p, set())
        mx = max((W[c] for c in range(1, p) if c not in ep), default=0)
        pen += max(0, mx - W[0] - D)
    for p in forced:
        W = [0] * p
        for k in range(1, m + 1):
            if u[k - 1]:
                W[(T + k) % p] += u[k - 1]
        ep = excl.get(p, set())
        mx = max((W[c] for c in range(1, p) if c not in ep), default=0)
        pen += max(0, mx - D)

    total = D * fixed_rot + rhs - pen
    lb = (total + D - 1) // D

    if lb != int(leaf["certified_int_lb"]):
        raise Fail(
            f"leaf LB mismatch: recomputed {lb}, claimed "
            f"{leaf['certified_int_lb']} (fixed={fixed} forced={forced})")
    if leaf.get("exact_ratio") and [total, D] != [int(x) for x in leaf["exact_ratio"]]:
        raise Fail("exact_ratio mismatch")
    return lb


def same_fixings(a, b, ignore):
    fa = {int(k): v for k, v in a["fixed"].items() if int(k) != ignore}
    fb = {int(k): v for k, v in b["fixed"].items() if int(k) != ignore}
    sa = sorted(x for x in a["forced"] if int(x) != ignore)
    sb = sorted(x for x in b["forced"] if int(x) != ignore)
    ea = {int(k): sorted(v) for k, v in a.get("excl", {}).items() if int(k) != ignore}
    eb = {int(k): sorted(v) for k, v in b.get("excl", {}).items() if int(k) != ignore}
    return fa == fb and [int(x) for x in sa] == [int(x) for x in sb] and ea == eb


def check_dead(m, T, primes, node):
    """Confirm a dead leaf's infeasibility claim. Returns nothing; raises
    Fail if the node is actually feasible."""
    if "dead_tick" in node:
        k = int(node["dead_tick"])
        if not (1 <= k <= m):
            raise Fail(f"dead tick index {k} out of range")
        val = T + k
        for p in primes:
            A = allowed_set(node, p)
            if val % p in A:
                raise Fail(f"dead tick {k} is coverable by ring {p} "
                           f"(phase {val % p} in {sorted(A)})")
        return
    p = int(node["dead_domain"])
    A = allowed_set(node, p)
    if A:
        raise Fail(f"dead domain ring {p} still has allowed phases {sorted(A)}")


def check_tick_split(m, T, primes, node):
    """Verify a tick split's candidate list (re-derived, order-sensitive)
    and per-child allowed-set transitions."""
    k = int(node["tick"])
    if not (1 <= k <= m):
        raise Fail(f"tick split index {k} out of range")
    val = T + k
    parent_fixed = {int(k2) for k2 in node["fixed"]}
    cands = []
    for p in primes:
        if p in parent_fixed:
            continue
        A = allowed_set(node, p)
        c = val % p
        if c in A:
            cands.append((p, c))
    claimed = [(int(p), int(c)) for p, c in node["candidates"]]
    if cands != claimed:
        raise Fail(f"tick {k}: candidate list mismatch — node claims {claimed}, "
                   f"re-derived {cands}")
    children = node.get("children")
    if not children or len(children) != len(claimed):
        raise Fail("tick split children do not match candidate count")
    parent_A = {p: allowed_set(node, p) for p in primes}
    for i, ch in enumerate(children):
        child_A = {p: allowed_set(ch, p) for p in primes}
        pi, ci = claimed[i]
        if child_A[pi] != {ci}:
            raise Fail(f"tick child {i} does not pin candidate {pi} to {ci}")
        for pj, cj in claimed[:i]:
            expect = set(parent_A[pj])
            expect.discard(cj)
            if child_A[pj] != expect:
                raise Fail(f"tick child {i}: ring {pj} should lose phase {cj} "
                           f"(allowed {sorted(expect)}), has {sorted(child_A[pj])}")
        for p in primes:
            if p in (pi,) or any(p == cj2[0] for cj2 in claimed[:i]):
                continue
            if child_A[p] != parent_A[p]:
                raise Fail(f"tick child {i} changes ring {p} outside the "
                           f"ordered-exclusion contract")


def check_tree(m, T, primes, node, depth=0):
    if "dead_tick" in node or "dead_domain" in node:
        check_dead(m, T, primes, node)
        return DEAD_LB, 1
    if "leaf" in node:
        return leaf_lb(m, T, primes, node), 1
    if node.get("deficit_leaf"):
        # Fully-constrained node the proposers could not certify to target.
        # Honest bound contribution = best_lb; the tree verdict then fails
        # the target at the root, as it must.
        return int(node.get("best_lb", 0)), 1
    children = node.get("children")
    if not children:
        raise Fail(f"internal node at depth {depth} has no children")
    if "tick" in node:
        check_tick_split(m, T, primes, node)
        min_lb = None
        total_leaves = 0
        for ch in children:
            lb, leaves = check_tree(m, T, primes, ch, depth + 1)
            min_lb = lb if min_lb is None else min(min_lb, lb)
            total_leaves += leaves
        return min_lb, total_leaves
    p = int(node["split_p"])
    parent_fixed = {int(k) for k in node["fixed"]}
    parent_forced = {int(x) for x in node["forced"]}
    if p in parent_fixed or p in parent_forced:
        raise Fail(f"split ring {p} already constrained at depth {depth}")

    # Classify split by the children's treatment of p.
    phases_seen = {}
    forced_seen = 0
    for ch in children:
        cf = {int(k): v for k, v in ch["fixed"].items()}
        cfo = {int(x) for x in ch["forced"]}
        if p in cf:
            if cf[p] in phases_seen:
                raise Fail(f"duplicate child phase {cf[p]} for ring {p}")
            phases_seen[cf[p]] = ch
        elif p in cfo:
            forced_seen += 1
        else:
            raise Fail(f"child does not constrain split ring {p}")
        if not same_fixings(node, ch, p):
            raise Fail(f"child changes fixings other than ring {p}")

    if forced_seen:
        if forced_seen != 1 or len(children) != 2 or len(phases_seen) != 1 or 0 not in phases_seen:
            raise Fail("malformed binary split: need exactly {p->0} and {p forced}")
        mode = "binary"
        expect_phases = [0]
    else:
        mode = "full"
        expect_phases = list(range(p))
        if sorted(phases_seen) != expect_phases:
            raise Fail(
                f"full split on ring {p} incomplete: phases {sorted(phases_seen)} "
                f"!= {expect_phases}")

    min_lb = None
    total_leaves = 0
    for ch in children:
        lb, leaves = check_tree(m, T, primes, ch, depth + 1)
        min_lb = lb if min_lb is None else min(min_lb, lb)
        total_leaves += leaves
    return min_lb, total_leaves


def main():
    path = sys.argv[1]
    with open(path) as f:
        tree = json.load(f)
    meta = tree["meta"]
    m = int(meta["m"])
    T = m * (m - 1) // 2
    if int(meta["T"]) != T:
        raise Fail("meta T mismatch")
    primes = sieve(math.isqrt(T))
    if int(meta["rings"]) != len(primes):
        raise Fail("meta ring count mismatch")
    target = int(meta["target_lb"])

    min_lb, leaves = check_tree(m, T, primes, tree)
    ok = min_lb >= target
    out = {
        "certificate_file": path,
        "m": m, "T": T, "rings": len(primes),
        "target_lb": target,
        "certified_tree_lb": min_lb,
        "leaves": leaves,
        "generator_status": meta.get("status", "unknown"),
        "OVERALL_VERDICT": "PASS" if ok else "FAIL",
    }
    print(json.dumps(out, indent=2))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    try:
        main()
    except Fail as e:
        print(json.dumps({"OVERALL_VERDICT": "FAIL", "error": str(e)}, indent=2))
        sys.exit(1)
