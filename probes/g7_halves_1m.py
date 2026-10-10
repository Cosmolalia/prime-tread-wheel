#!/usr/bin/env python3
"""
g7_halves_1m.py — Phase 4a (probe G7): extend C1 (halves claim) evidence
from 120k laps to 1M laps.

Claim C1: for every lap m >= 21, the layer-m window values T(m-1)+1 .. T(m-1)+m
(T(m-1) = m(m-1)//2) contains at least one prime in the LEFT half
(ticks 1..floor(m/2)) AND at least one in the RIGHT half
(ticks floor(m/2)+1..m). Same midpoint convention as halves_struct.py.

For each lap m = 21..1_000_000:
  W_L(m) = distance (in ticks) from left window edge (value T(m-1)+1) to the
           nearest prime in the window; 0 means the prime sits exactly on the
           left edge. VIOLATION if the left half has no prime.
  W_R(m) = same from the right edge (value T(m-1)+m); VIOLATION if the right
           half has no prime.

Method: walk inward from each edge testing primality. DETERMINISTIC
Miller-Rabin with bases [2,3,5,7,11,13,17] — valid for n < 3.47e14
(our max value is T(10^6) ~ 5e11, far below). Pure Python, no sympy.
Composites are first rejected by trial division against small primes
(sieve up to 10000), which rejects the overwhelming majority before any
MR round. Each walk stops at the half's far edge (the midpoint side);
reaching it with no prime = C1 violation for that half.

Results flush every 10k laps to CSV (crash loses at most 10k laps).
Time wall: 90 minutes; on hitting it, analyze whatever laps are covered.
"""
import csv, math, os, sys, time

M_START, M_END = 21, 1_000_000
TIME_WALL_S = 90 * 60
SMALL_PRIME_LIMIT = 10_000
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "lab", "g7_halves_1m.csv")
MR_BASES = (2, 3, 5, 7, 11, 13, 17)


def small_primes(limit):
    s = bytearray(b"\x01") * (limit + 1)
    s[:2] = b"\x00\x00"
    for i in range(2, int(limit ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = b"\x00" * len(s[i * i::i])
    return [i for i in range(2, limit + 1) if s[i]]


SP = small_primes(SMALL_PRIME_LIMIT)
SP_SET = frozenset(SP)


def is_probable_prime(n):
    """Deterministic MR, exact for n < 3.47e14 given bases [2,3,5,7,11,13,17]."""
    if n < 2:
        return False
    if n in SP_SET:
        return True
    # trial division by small primes (covers 2,3,5,...): rejects most composites cheaply
    for p in SP:
        if p * p > n:
            return True
        if n % p == 0:
            return False
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in MR_BASES:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def walk_from_edge(base, k_start, k_end, step):
    """Ticks k_start..k_end inclusive (step=+1 from left, -1 from right).
    Returns (k of nearest prime, W) or (None, None) if no prime found."""
    k = k_start
    while (step > 0 and k <= k_end) or (step < 0 and k >= k_end):
        v = base + k
        if v & 1 and is_probable_prime(v):
            if step > 0:
                return k, k - 1
            return k, (k_start - k)  # distance in ticks from right edge
        k += step
    return None, None


def main():
    t0 = time.time()
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    resume_from = M_START
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH) as f:
            n_rows = sum(1 for _ in f) - 1  # minus header
        resume_from = M_START + max(0, n_rows)
        print(f"resuming at m={resume_from} ({n_rows} rows already present)", flush=True)

    fout = open(CSV_PATH, "a", newline="")
    w = csv.writer(fout)
    if resume_from == M_START:
        w.writerow(["m", "W_L", "W_R", "violation"])

    buffer = []
    violations = 0
    n_since_flush = 0
    for m in range(resume_from, M_END + 1):
        H = m // 2
        base = m * (m - 1) // 2
        kl, wl = walk_from_edge(base, 1, H, +1)
        kr, wr = walk_from_edge(base, m, H + 1, -1)
        viol = 0
        if kl is None:
            viol = 1
            wl = -1  # no prime in left half
        if kr is None:
            viol = 1
            wr = -1
        violations += viol
        buffer.append([m, wl, wr, viol])
        n_since_flush += 1
        if n_since_flush >= 10_000:
            w.writerows(buffer)
            fout.flush()
            os.fsync(fout.fileno())
            buffer.clear()
            n_since_flush = 0
            el = time.time() - t0
            rate = (m - M_START + 1) / el if el else 0
            print(f"m={m}  elapsed={el/60:.1f}min  {rate:.0f} laps/s  "
                  f"violations={violations}", flush=True)
        if time.time() - t0 > TIME_WALL_S:
            print(f"TIME WALL hit at m={m}", flush=True)
            break
    if buffer:
        w.writerows(buffer)
        fout.flush()
        os.fsync(fout.fileno())
    fout.close()
    el = time.time() - t0
    print(f"DONE: covered laps 21..{m}, {violations} violations, "
          f"{el/60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
