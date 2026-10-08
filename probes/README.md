# Probes

Python 3 + numpy for the `.py` files; C (`gcc -O3 -march=native -fopenmp`) for
`layer_gap.c` and `boundary.c`. Run each from this folder.

The wheel: layer m holds the m numbers T(m−1)+1 .. T(m), with T(m) = m(m+1)/2, and tick k sits at angle k/m.

| File | What it does | Result to reproduce |
| --- | --- | --- |
| `verify.py` | Recomputes every number in PAPER.md | All checks print `ok`; Mertens max 0.5657 at n = 200; lane 9,863 / 9,836 / 4,986 |
| `gear_net.py` | A network built by hand whose weights are the wheel's gears (circles for the primes 2 to 31) | Exact up to 961; after that it never misses a prime, but its "prime" calls dilute (about 32% right near 10⁹) |
| `snake_net.py` | A network that starts empty and plants each prime it outputs as a new gear, switched on at p² | Exact to 300,000 (25,997 primes, none wrong, none missed); its active gears grow like √x |
| `knockout_test.py` | Which gears each layer needs to clear its composite seats | About half the gears below √ are needed (the same share as any interval that short); the biggest one needed reaches 98% of √ by layer 3,000 |
| `lane_test.py` | The two lanes at the seam: closing tick T(m) and opening tick T(m−1)+1 | Opening lane: 9,863 primes to layer 100,000 vs 9,836 predicted by open seats and about 4,986 by chance |
| `layer_gap.c` | Full-range sieve, two independent modes (`stats` walks primes in order and records every layer's largest internal composite run; `verify` marks occupied layers order-free in parallel) | To layer 30,000: 0 empty; largest prime gap 282; both modes and an independent numpy sieve agree on every statistic |
| `boundary.c` | Per layer, locate the first prime above T(m−1): 65,536-wide odd sieve plus deterministic 12-base Miller–Rabin (exact below 3.3·10²⁴) | To layer 1,000,000,000: 0 empty; max bottom margin 766 at layer 264,800,157; 3.13B Miller–Rabin tests; cross-validated against `sympy.nextprime` to layer 30,000 |

`primes_util.py` holds the shared sieve and a deterministic primality test.

**What the two "nets" are.** `gear_net.py` and `snake_net.py` are not trained approximations. A gear p fires exactly when cos(2πx/p) > cos(π/p), which for integers is precisely p | x — so the nets are residue-class detectors, i.e. the sieve of Eratosthenes restated in the wheel's geometry. The switching on at p² is the sieve's square-root boundary, not something the net discovered. What they demonstrate is that the wheel's circles can carry the sieve's mechanism exactly, and where a fixed gear set stops following the primes (past 31² = 961, prime density drops below the fixed residue classes' survivor rate).

## Open questions worth probing

1. Can every seat on some layer be composite at once? This is the open conjecture that a prime lies between any two consecutive triangular numbers (OEIS A066888). Directly checked to layer 1,000,000,000 (`boundary.c`: no empty layer, worst bottom margin 766 at layer 264,800,157); by extension through the exhaustive prime-gap data below 4·10¹⁸ (max gap 1476), verified through layer 2,828,427,124. The early-layer worst case remains the run 114–126 against layer 15.
2. Do spokes carry 0, 1 or 2 primes at the rates their seat counts predict? Write the predictions down before checking.
3. Train a small network on wheel coordinates versus raw numbers (labels: prime, divisibility, twin, parity of the number of prime factors). Train near 10⁶, test near 10⁹, and compare the geometry it learns with `gear_net.py`.
