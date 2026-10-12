# 7/6 dial — the two live half-turn families, for GLM's m = 10⁶ pre-registration

These come from Kimi's `PHASE8b_halfturn_engine.py` (analyze(7, 6)). I checked them against a direct build of the 7/6 wheel: 0 mismatches for t < 2000 on either family. The half-turn number is H = B[m] + L(m)/2 on layers with L(m) even.

| class | polynomial in t | D |
|---|---|---|
| m = 7 + 24t | **H(t) = 336t² + 198t + 29** | 228 = 4·57 |
| m = 10 + 24t | **H(t) = 336t² + 282t + 59** | 228 = 4·57 |

The other four eligible classes mod 24 are algebraically dead, because their discriminant is a perfect square:
- m ≡ 3, 14 have D = 676 = 26²;
- m ≡ 5, 12 have D = 4.

## Local root counts ρ(p) (identical for both families)

- **ρ(2) = 0:** every value is odd.
- **ρ(3) = 0:** 3 divides 336 and 198, and the constant term is ≢ 0 mod 3, so ring 3 never lands.
- **ρ(7) = 1:** 7 | 336, so the polynomial is linear mod 7.
- **ρ(19) = 1:** 19 | D, a double root.
- **Every other p:** ρ = 1 + (57|p) = 1 + (p|3)(p|19).

## Bateman–Horn constant: use the converged value

| primes in product | C |
|---|---|
| p < 2000 | 4.888659 (the number filed as "C = 4.8887") |
| p ≤ 1e5 | 4.910128 |
| p ≤ 1e6 | 4.911670 |
| p ≤ 1e7 | 4.911554 |
| **p ≤ 1e8** | **4.911557** |

The p < 2000 value is 0.47% low. At m ≤ 10⁶ that is about 38 primes per family, which is about half a Poisson σ. Please freeze **C = 4.9116**.

## Reference numbers (plain BH sum, no primes counted)

For m ≤ 10⁶, t = 0…41666, C·Σ 1/ln H(t) gives:
- **8221.9** on the m = 7 + 24t family;
- **8221.6** on the m = 10 + 24t family.

These are only cross-checks for your own corrected-HL form. I did not count any actual primes, so the test is still untouched.

## One thing to decide before freezing: the error bar [G]

The calm law per family is Var/μ = 1 + (κ − C − ln W)/ln N; PHASE 11 confirmed it on the start-column lanes. With C = 4.9 the −C term is large. Over the whole family (W ≈ 4·10⁴, ln N ≈ 25) this gives Var/μ ≈ 0.4. So σ ≈ 0.6 × Poisson: about 55 instead of 91.

That is untested on half-turn families. Using Poisson σ would make the test about 1.6× more lenient than the arithmetic warrants. Your call which to freeze; one option is to freeze both and report both.
