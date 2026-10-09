# Prime wheel handoff: the Claude session

Oct 8, 2026 · @obi

This hands off the prime-wheel work done in the Claude session of October 6 to 8, 2026: the frame, what has been checked, ten predictions written down before checking (nine held, one failed), the exact methods, the code, and what is still open.

## The picture

The wheel rolls the counting numbers onto rings that each grow by one tick. Layer m holds the m numbers after the triangular number T(m−1), with T(m) = m(m+1)/2, and tick k sits k/m of the way around. Everything below is a part of that one picture or a test of it. The triangle law ties it together: a layer is only √2 times as wide as the biggest ring that decides it, which is why our wheel sits on the square-root wall.

| Word | What it means here |
| --- | --- |
| Layer m | The m numbers T(m−1)+1 to T(m). Each layer is one full lap of remainders mod m, shifted half a turn when m is even |
| Seam | Angle 0, where every layer starts. It holds the triangular numbers |
| Tick, visit, spoke | Tick k of layer m is visit g = gcd(k, m) to its angle. Third and later visits are always composite (the visit lock). Primes sit on fresh ticks, or on second visits when m ≡ 2 mod 4. A layer has φ(m) seats a prime can take. A spoke is the straight line of one fraction a/b; its first two visits, its two shots, are the only ones that can hold primes, and the second shot is twice the first plus b² |
| Ring p (gear) | Marks every multiple of p. Every number sits on every ring (the Platonic Map). Ring p decides layer m when p² ≤ T(m), so the deciding rings reach about m/√2: the rings inside the half-area circle judge the outer layer |
| Mirror | Ring 2, the even axis. In every free-phase test it stays on the evens, because no even past 2 is prime |
| Free phases | Each odd ring turned to any phase instead of its real one. The most the rings can cover in a row is h(k) − 1, the Jacobsthal number of the first k primes, which is the same quantity as Erdős's Y(x) |
| Wipe, safe by width | A wipe is a turning that covers a whole layer. A layer is safe by width when no turning can cover it, so a prime must land there whatever the real alignment |
| CRT lock | Every turning of rings 2 to p shows up exactly once per lap of 2·3·5·…·p numbers on the real line |
| Seam lane c | The column c ticks after the seam: T(m−1)+c, a quadratic in m. Columns a triangular number before the seam are always composite |
| Gear rule | A lane's prime richness from how many seats each ring can land on in it: the Bateman–Horn constant, the product over odd p of (1 − w/p)/(1 − 1/p), with w = 1 + (D/p) and D = 1 − 8c |
| Clocks (higher dimensions) | Every two dimensions add one turning plane. k clocks with periods m to m+k−1 give layers of m(m+1)…(m+k−1) numbers. In 4D the clocks make a donut and the count is a knot wound on it |

## Findings

The strongest result: primes in the seam lanes are calmer than coin flips, and the calm is made by rings finishing their laps (the same law is known for plain primes). Everything else here either feeds that picture or marks where it stops. The earlier catalog (the visit theorem, the seam's quadratic lanes, the squares' √2 spin and Pell landings, mirror pairs summing to m², the Mertens balance) is in the Wheel Atlas and the repo paper.

| Finding | How it's settled |
| --- | --- |
| Every layer holds a prime | Counted to 20 million in the 2D, 4D and 6D wheels. Open in general |
| The deciding rings reach m/√2, the half-area circle; the same √2 as the squares' spin | From the triangle law |
| Freely turned rings (ring 2 on the evens) can wipe every layer from 41 to 391. Layers 2–17, 21–23, 25, 26 and 40 are safe by width | Exact, from the Jacobsthal table |
| On the real line every wiping turning exists, but the first one sits 45 to 3 million times farther out than the layer, where layers are far wider (layers 18–63) | Exact: line scans, then CRT enumeration |
| The protection lives in the big rings: pin every ring up to 83 real and the 35 bigger rings turned freely still wipe layer 390; pin the big rings real and free the small ones and no layer is ever wiped | Exact: an explicit wiping turning for the first, an exhaustive check with free rings up to 19 for the second |
| Parity fold: the odd rings cover a run of odds exactly as well as all rings cover a run of numbers, j(2n) = 2j(n). Only layers 21 and 25 change | Exact for 2 to 9 rings |
| The seam doors are hot seats: the first odd after the seam is prime 1.97 times as often as a random odd (even total + 1) and 1.27 times (odd total + 2). A layer's first prime comes within 24% of the way in | Counted to layer 200,000 and 20,000 |
| Every seam lane matches its gear-rule richness to within 0.09%, and the lanes' rich-to-poor order matches in all 153 pairs | P2: 18 lanes, 100 million layers each |
| Lanes are calmer than coin flips: 45% of the coin-flip wobble over 100 million layers, 7.5 points calmer per tenfold longer stretch, on a straight line. Fake lanes with only rings up to 1,000 on schedule flatten near 70% | P9: 300 lanes. The same law is known for plain primes (Montgomery and Soundararajan) |
| The far jump is the earliest of many scattered landings: the first wiping stretch comes near the lap divided by the number of wiping turnings | 18 cases, then blind in P8 |
| A gear machine builds every prime to 20,000 with no division. A prime is where the machine runs out of gears; then it becomes one | Checked. Primes as a process, not a property (Eratosthenes in spirit) |
| Under free phases, the rings lose the power to wipe out every Goldbach pair as 2n grows | P4, by search only |
| A counter's own clocks flag composites with no division: our ring plus the mirror 64%, two clocks (4D) 72%, three clocks (6D) 80%. A clock for every period gives the Platonic Map | P5, P7 |
| Above 2D the layers are safe by width: no 4D layer from 2 to 60 and no 6D layer from 2 to 22 can be wiped. 2D is the only rung where the rings can aim at a whole layer | Counted as far as the Jacobsthal table goes. Beyond that it needs a ceiling nobody has proven (Erdős problem 687) |
| The mirror grows an axis in 4D: layers start at 0 or two thirds of a turn, when 3 divides the clock. 6D gives only halves, because four in a row always hold two evens | Proven from the offset formula. The quarters guess for 6D failed |
| Kimi's parabolas (each ring confined to the spots its parabola visits, which is the gear rule seen from the ring) prove a prime in every layer up to 26, and in 19 more up to 57, from structure alone. From layer 58 on, the structure always leaves room for a wipe, so only where the walk actually is protects a layer: her routing wall starts there | P10, exact; brute-force re-check for layers 18 to 35 |

## Predictions log

Every prediction was written down, with its pass line, before its check ran. Nine held, one of them by search rather than proof, and one failed; the failure's reason became P8. The live copy is the predictions log in the Wheel Atlas.

| # | Written before checking | What the check found | Outcome |
| --- | --- | --- | --- |
| P1 | **Two shots per spoke.** For odd denominators up to 5,000, the gear rule predicts 49,428 spokes with both shots prime, within 2% | 49,355, 0.15% under | Held |
| P2 | **Hot seats down the seam.** Past layer 100,000, every seam lane's richness matches the gear rule within a few percent, and the order holds | 18 lanes to layer 100 million: within 0.09%, order right in all 153 pairs | Held |
| P3 | **The far jump.** For rings up to 37 (layers 52 to 57), the first wiping stretch starts between 1 billion and 1 trillion | Layer 52 at 133 million, under the floor. Layers 53 to 57 inside, at 2.8 to 4.7 billion | Failed |
| P4 | **Goldbach under free phases.** Freely turned rings lose the power to wipe out every prime pair as 2n grows | Wipe-outs up to about 1,000, none from 2,000 to 32,000. Search, not proof | Held by search |
| P5 | **Composites by geometry alone.** The mirror plus the visit lock flag 60 to 65% of composites | 64.2%, and never a prime | Held |
| P6 | **4D is safe by width.** No turning of the rings can wipe a layer of the two-clock wheel | None from layer 2 to 60, as far as the table goes; at layer 60 the rings cover at most 26%. Beyond that it rests on an open problem | Held |
| P7 | **A 4D counter sees more.** Its two clocks flag about 70% of composites with no division | 72.4%; three clocks flag 80% | Held |
| P8 | **Count the turnings.** For rings up to 43, the first stretch of 63 covered numbers lands near 2.7 billion, between 0.14 and 10.8 billion | 3,732,574,514, 1.4 times the estimate | Held |
| P9 | **Calmer than coin flips.** Under 60% of coin-flip wobble over the whole run; calmer at every tenfold step from 100 layers (80% or more there); a straight line with a drop of 0.04 to 0.10 per tenfold; coin flips stay near 100% and rings up to 1,000 on schedule give only part of the calm (under 85%) | All four held: 45% over the whole run, 89% at 100 layers, 7.5 points per tenfold with no step more than 0.7 points off the line, coin flips 92 to 100%, schedule-to-1,000 flattening near 70% | Held |
| P10 | **Kimi's parabolas save layers.** With each ring confined to the spots its parabola visits, at least one layer free rings can wipe becomes safe; the first confined wipe comes after layer 18 and the unbroken wipeable stretch starts after 41; and from some layer at or before 100, every layer through 150 is wipeable again | All three held: 21 layers saved, the first confined wipe at layer 27, and every layer from 58 through 256 wipeable again | Held |

## Methods worth reusing

The checks lean on a few exact tools. Each was matched against an independent count before it was trusted.

- **Free-phase capacity.** For k rings, the most they can cover in a row is h(k) − 1 (OEIS A048670, 58 terms known). With ring 2 held on the evens, a layer starting on an odd number gets one less: capacity = h − 1 − (lo mod 2). A layer can be wiped when it holds at most h/2 − 1 odd numbers.
- **First wiping stretch, exactly** (`p3_far.c`). Enumerate every turning of the first k rings that covers a window of L: cover the first uncovered spot with some unused ring, and prune when the unused rings can't cover what's left even at their best phase. Lock each turning to the line by CRT; rings a turning doesn't use can sit anywhere. The smallest position wins. Matches the line scans to the digit for rings up to 29 and 31. It slows down at 14 rings, where walking the line in numpy is faster.
- **Layer parity.** Covered stretches always start and end on an even number, so their length is odd. A layer that starts on an even needs a run at least its width long; a layer that starts on an odd needs one more number and starts one in.
- **Counting the turnings** (`p3_count.c`). The exact number of covered runs of length L or more per lap: position 0 uncovered, positions 1 to L covered, ring 2 on the odd positions, rings 3 to 13 brute-forced, bigger rings by recursion with a weighted "covers nothing needed" branch. Matches brute force over whole laps for 5 to 8 rings. The first wiping stretch then comes near the lap ÷ (count + 1), with exponential-style luck around it.
- **Exact lane counts** (`p2_seam.c`). Sieve the quadratic T(m−1)+c by every prime up to the square root of its largest value, using the two roots of m² − m + 2c mod p (Tonelli–Shanks on D = 1 − 8c). Evens drop out by parity, and values small enough to be sieving primes themselves are settled by trial division. The gear-rule constant comes from the same primes. About 8 seconds per lane for 100 million layers.
- **The calm test** (`p9_calm.c`). Three streams per lane: the real primes; pure coin flips, each odd value prime with the gear-rule chance q = 2C/ln(value); and fake lanes where rings up to 1,000 run on their real schedule and each survivor is a coin flip at q/s. The ratio is the sum of squared misses over the sum of coin-flip variance, pooled over windows of 100 to 100 million layers.
- **Dimension wheels** (`dims.py`). k clocks with periods m to m+k−1, totals m(m+1)…(m+k)/(k+1). For each layer: width, primes, longest composite run, deciding rings and free capacity.
- **Gear machine** (`gear_machine.py`). Gears only count forward and wrap at their size. A gear switches on when its seam visits equal its teeth, exactly at p². Where no live gear sits at zero, a prime is built and becomes a gear.
- **Discipline.** Write the prediction and its pass line in the notes, with the time, before the run. Log failures with their reason.

## Built here

Two pages and one doc came out of these days, all private to Obi. The code bundle sent with this doc (prime-wheel-claude-handoff.zip) holds every script, its outputs, both built pages, the running notes, and markdown copies of this handoff and the Atlas, so everything reruns without these links.

| Thing | What it is |
| --- | --- |
| [The Platonic Map](https://claude.ai/artifact/N9XsAbV1xQ1gopzUGYjZiS) | Every number on every ring. Real phases against free phases (ring 2 held on the evens), the wipe test for each layer, the pin demo on layer 390, and the far-jump chart for layers 18 to 51. Source in `platonic/` |
| [The Donut View](https://claude.ai/artifact/2XFxKDVWSaJhxzqdxzNQrs) | What a 4D counter sees: two clocks as a donut with the count as a knot, the unrolled grid beside one ring (the scatter as a shadow), the 4D layers, and whether the rings could wipe a layer with 1, 2 and 3 clocks. Source in `donut/` |
| [The Wheel Atlas](https://claude.ai/code/artifact/c2510419-6c5b-454d-82aa-953d5e06e4b0) | The catalog: the skeleton, the knockout table, new fits, 79 prime facts placed on the wheel, what doesn't fit, what to probe, and the live predictions log |
| Earlier pages | The wheel, the problem wheels and the globe, with the paper and the first probes, are in the repo bundle Kimi already has |

The scripts live in `phase/`:

| Script | What it gives |
| --- | --- |
| `primes_util.py` | A sieve and a deterministic primality test, used by everything else |
| `jacobsthal_scan.py`, `first_far.py`, `margin.py` | Jacobsthal values and first wiping runs by walking the line; real against free coverage for every layer |
| `pin_test.py`, `pin_more.py`, `parity_pin.py` | Which rings protect a layer, and the parity fold |
| `seam_odd.py` | The seam doors and how early each layer's first prime arrives |
| `p1_estimate.py`, `p1_count.py`, `p5_geometry.py` | P1 and P5 |
| `p4_goldbach.py`, `p4_sat.py`, `p4_anneal.py` and helpers | Goldbach under free phases: exact solvers for small 2n, annealing beyond |
| `gear_machine.py` | The division-free prime machine, to 20,000 |
| `dims.py` | The 2D, 4D and 6D wheels to 20 million: P6 and P7 |
| `p2_seam.c`, `p2_judge.py` | P2 |
| `p3_far.c`, `p3_count.c` and the `p3_scan` checks | P3, P8 and the counting rule |
| `p9_calm.c`, `p9_judge.py` | P9 |

To rerun the headline checks, from `phase/` (Python 3 with numpy, and gcc; the exact Goldbach solvers also need pulp and python-sat):

```bash
python3 gear_machine.py                 # built 2262 primes up to 20000 ... identical to the primes: True
gcc -O3 -o p3_far p3_far.c && ./p3_far 12 53 53          # 53 132966024 ... (rings up to 37)
gcc -O3 -o p3_count p3_count.c && ./p3_count 12 53       # 30476 runs per lap, estimate 2.43e8
python3 p3_count_check.py               # brute force over whole laps: all OK
gcc -O3 -o p2_seam p2_seam.c -lm && ./p2_seam 100000 100000000 586 1 2   # about 8 s per lane
gcc -O3 -o p9_calm p9_calm.c -lm && ./p9_calm 100000 100100000 9 14 313 > p9.jsonl   # about 11 s per lane
python3 p9_judge.py p9.jsonl            # the four P9 calls, judged
```

## Open threads

The first is the natural next prediction; the rest run from nearest to a test to furthest.

- **Why 7.5 points per tenfold?** The calm's slope isn't derived yet. Write a prediction for it from the gear rule (the lane version of the Montgomery–Soundararajan law, where each decade of rings takes an equal slice of luck), then measure it on new lanes. Also check whether richer lanes calm faster: 43% against 49% over the whole run so far, inside the noise.
- **4D past layer 60.** "Safe by width forever" needs the rings' longest covered run to grow no faster than the biggest ring to the 4/3 power. The best proven ceiling is the biggest ring squared, and even beating the square is open (Erdős problem 687). Every count says it holds; a wheel-side argument would be new.
- **Goldbach under free phases (P4).** Held by search only. The range Goldbach needs grows like the square of the ring reach, a layer only like the reach. A strong two-seam covering bound would close it; the route may already be in the literature, so check before claiming it.
- **The far jump's saw-tooth.** Each new ring pulls the first wiping stretch in, and wider layers push it back out. Use the counting rule to predict it blind for 15 or more rings before walking the line.
- **The seam catalog.** Search lanes past c = 4,000, and around other spokes, for the richest ones, and check whether their richness tracks class numbers the way Euler's polynomial does (lane 586 ties n² + n + 41 per odd value).
- **Layers 52 to 63 on the map.** The Platonic Map's far-jump chart stops at layer 51; the exact firsts now reach layer 63.

## Working with Obi

- Explain the mechanism first: what does what. He keeps the picture, not the names, numbers or dates.
- Restate his chain at its current resolution, name the links nobody has tested, and land on a claim. No hedging, and hold your ground honestly when he pushes back.
- When he runs a chain to see where it goes, he is probing, not asserting. Treat it that way.
- Write insights down as they come, and predictions before their checks, so nothing depends on context that can be lost.
- Code edits can just be done. Ask him first before dropping an idea, changing the research direction, publishing, or contacting anyone; publishing goes through him.
- He thinks in pictures. A visual that matches the mechanism lands better than a paragraph.
- Keep ring 2 on the evens in every free-phase test, because no even past 2 is prime. An early test here let ring 2 turn, and he caught it.

## Sources

- [OEIS A048670: the Jacobsthal function of the primorials](https://oeis.org/A048670), the free-phase capacity table
- [Short intervals containing primes (CNRS)](https://tme-emt-1f5ce3.pages.math.cnrs.fr/Art09.html), what is proven about primes in short stretches
- [Erdős problem 687](https://www.erdosproblems.com/687), the proven ceiling and the open question behind P6
- [Montgomery and Soundararajan, Primes in short intervals](https://arxiv.org/abs/math/0409258), the calm law for plain primes
