#!/usr/bin/env python3
"""
PHASE 14 — 7/6 dial, independent reproduction of GPT's million-layer census.

Frozen BEFORE counting (claims under audit from swarm handback 10-12, GPT §5-7):
  Families:
    F1(u) = 336u^2 + 198u + 29   (laps m = 24u+7)
    F2(u) = 336u^2 + 282u + 59   (laps m = 24u+10)
    Both D = 228, non-square (live BH families per GPT + GLM derivation).
  Window: u = 0..41666 both families (m <= 1,000,000 inclusive; 41,667
    candidates each — GPT's exact window).
  Convention: L(m) = floor(7m/6 + 1/2), ties UP (GLM landmine; my
    PHASE8b engine uses (2*a*m+b)//(2*b) = same convention, verified).
  Singular constant: C = 4.9116695006 (GPT, product over p <= 1e6).
    Comparison value: C_2000 = 4.8886587389 (2,000-prime cutoff).
  Prediction (BH, discrete sieve form): sum_u C / ln(F(u)) per family.
    GPT's frozen predictions: P7 8222.1167, P10 8221.7768, total 16443.8935.
  Primality: deterministic Miller-Rabin, bases [2,3,5,7,11,13,17]
    (deterministic for n < 3.47e12; max value here ~5.84e11). Trial-
    division screen by primes <= 1000 first.
  F2 sanity [F]: F2(u) = F1(u - 1/8) rational translation — local factors
    identical; no separate structural check needed.

Claims to reproduce: P7 actual 8280, P10 actual 8180, total 16460,
observed/predicted 1.00098. Sub-window m <= 200k: P7 1871, P10 1905.
"""
import json
import math
import time

C = 4.9116695006
C2000 = 4.8886587389
BASES = [2, 3, 5, 7, 11, 13, 17]
U_MAX = 41666


def small_primes(n):
    s = bytearray(n + 1)
    for i in range(2, n + 1):
        if not s[i]:
            s[i * i::i] = b'\x01' * len(s[i * i::i])
    return [i for i in range(2, n + 1) if not s[i]]


SP = small_primes(1000)


def is_prime(n):
    if n < 2:
        return False
    for p in SP:
        if p * p > n:
            return True
        if n % p == 0:
            return n == p
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in BASES:
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def F1(u):
    return 336 * u * u + 198 * u + 29


def F2(u):
    return 336 * u * u + 282 * u + 59


def census(F, pred_c, umax=U_MAX):
    pred = sum(pred_c / math.log(F(u)) for u in range(umax + 1))
    t0 = time.time()
    primes = [u for u in range(umax + 1) if is_prime(F(u))]
    return pred, len(primes), primes, time.time() - t0


def main():
    out = {"conventions": "frozen in header; C=4.9116695006; u=0..41666; "
                          "MR bases [2,3,5,7,11,13,17]"}
    p7, n7, l7, t7 = census(F1, C)
    print(f"F1: predicted {p7:.4f} actual {n7} ({t7:.0f}s)", flush=True)
    p10, n10, l10, t10 = census(F2, C)
    print(f"F2: predicted {p10:.4f} actual {n10} ({t10:.0f}s)", flush=True)

    # m <= 200k sub-window: 24u+7 <= 200000 -> u <= 8333; 24u+10 -> u <= 8329
    n7_lo = sum(1 for u in l7 if 24 * u + 7 <= 200000)
    n10_lo = sum(1 for u in l10 if 24 * u + 10 <= 200000)

    # out-of-sample m > 200k slice (GLM prereg window spirit)
    n7_hi = n7 - n7_lo
    n10_hi = n10 - n10_lo

    out.update({
        "F1": {"pred_C": p7, "actual": n7, "m_le_200k": n7_lo,
               "m_gt_200k": n7_hi},
        "F2": {"pred_C": p10, "actual": n10, "m_le_200k": n10_lo,
               "m_gt_200k": n10_hi},
        "total": {"pred_C": p7 + p10, "actual": n7 + n10,
                  "ratio": (n7 + n10) / (p7 + p10)},
        "gpt_claim": {"F1": 8280, "F2": 8180, "total": 16460,
                      "ratio": 1.00098, "F1_lo": 1871, "F2_lo": 1905,
                      "pred_F1": 8222.1167, "pred_F2": 8221.7768,
                      "pred_total": 16443.8935},
        "prime_us_F1": l7,
        "prime_us_F2": l10,
    })
    with open('lab/PHASE14_dial76.json', 'w') as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "prime_us_F1"
                      and k != "prime_us_F2"}, indent=1), flush=True)
    # convention spot check: ties-up L(9) = 11 (not banker's 10)
    assert (2 * 7 * 9 + 6) // 12 == 11
    print("tie convention check: L(9) = 11 (ties-up) OK", flush=True)


if __name__ == '__main__':
    main()
