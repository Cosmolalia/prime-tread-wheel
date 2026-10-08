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
| `shadows.c` | Per layer, sieve EVERY tick value up to √T(m) and record the smallest covering prime per seat (no MR needed — sieved to √ is exact). Single mode dumps the full cover table + a binary head map; `-b` batches laps with mouth anatomy stats | Record layer 264,800,157: mouth held by 109 distinct outside primes, 100% of cover from primes NOT dividing m (routed primes close only their own non-seat ticks); two-stage conjunction anatomy below |

**Shadow anatomy of a near-miss mouth** (`shadows.c` + `shadow_anatomy.py` + `shadow_regularity.py`; layer 264,800,157, margin 766, full cover table regenerable via `./shadows 264800157`, ~24 s):

- The mouth is a two-stage conjunction. Small outside primes (2…331) shadow the first 766 ticks down to 57 holes — seats/ticks that dodged every small shadow. The margin is 766 because **all 57 holes are composite with every factor > 766** (43 semiprime, 14 factor further). Any one hole being prime breaks the mouth earlier. Lap interior is normal (max internal prime gap 544).
- The cover is a pile-up, not a fragile arrangement: 833 divisor-marks over 766 ticks (1.68×), but 270 ticks have exactly one covering prime among the mouth strikers.
- The lap's own machinery contributes nothing: m = 3·37·2385587, and routed primes (3, 37, …) strike only non-seat ticks. 100% of the mouth cover comes from outside primes.
- Slip alignment is not the mechanism: the 57 large one-off strikers' k0 = (−T(m−1)) mod p values are uniform; nothing in m's factorization or the alignments marks the lap in advance.
- Batch comparison (60 consecutive laps + 60 prime laps around the record; logs in `logs/shadows_batch_all2.log`, `logs/shadows_batch_prime.log`): median mouth ≈ 27, p95 ≈ 105–136, second-widest mouth 220 (prime lap 264,800,659). The record's 767 is rank 1/119 with a 3.5× gap to the nearest rival — and mouth width correlates with striker count at r = 0.981 across all laps. Widest mouths show no pattern in m mod 4 or factorization shape.
- Structural parity fact the probe exposed: for m ≡ 2 (mod 4), T(m−1) is odd, so every seat-value is even — seat-primes are identically zero there, and the layer's primes all sit on even-k (non-seat) ticks. Seat-prime statistics and interval-prime statistics must be kept separate (`ifirst_off` vs `first_off` in the output); `boundary.c`'s margin is interval-based.

Reading: the wheel renders the covering problem with perfect clarity — who kills whom, seat by seat — but the shadow arrangement shows no wheel-forbidden configuration. The near-miss is a generic-sieve pile-up rendered exactly, not a wheel-structural event. That is an honest negative for the "slip/balance constraints forbid full covers" route: empirically those constraints do not bind the shadows.

`primes_util.py` holds the shared sieve and a deterministic primality test.

**What the two "nets" are.** `gear_net.py` and `snake_net.py` are not trained approximations. A gear p fires exactly when cos(2πx/p) > cos(π/p), which for integers is precisely p | x — so the nets are residue-class detectors, i.e. the sieve of Eratosthenes restated in the wheel's geometry. The switching on at p² is the sieve's square-root boundary, not something the net discovered. What they demonstrate is that the wheel's circles can carry the sieve's mechanism exactly, and where a fixed gear set stops following the primes (past 31² = 961, prime density drops below the fixed residue classes' survivor rate).

## Open questions worth probing

1. Can every seat on some layer be composite at once? This is the open conjecture that a prime lies between any two consecutive triangular numbers (OEIS A066888). Directly checked to layer 1,000,000,000 (`boundary.c`: no empty layer, worst bottom margin 766 at layer 264,800,157); by extension through the exhaustive prime-gap data below 4·10¹⁸ (max gap 1476), verified through layer 2,828,427,124. The early-layer worst case remains the run 114–126 against layer 15.
2. Do spokes carry 0, 1 or 2 primes at the rates their seat counts predict? Write the predictions down before checking.
3. Train a small network on wheel coordinates versus raw numbers (labels: prime, divisibility, twin, parity of the number of prime factors). Train near 10⁶, test near 10⁹, and compare the geometry it learns with `gear_net.py`.
