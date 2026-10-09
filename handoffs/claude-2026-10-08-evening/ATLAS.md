# The Wheel Atlas

Oct 6, 2026 · @obi

## At a glance

Everything placed so far lives in three worlds on one wheel, joined by four bridges, with the gears adding the local picture underneath.

&#91;embedded content: the wheel's three worlds and four bridges\]

The angles are the skeleton. Every ring is one lap of remainders that starts at the seam or half a turn from it, which is why the ticks inherit the angles' divisibility. The Riemann Hypothesis shows up on both sides.

## The skeleton is forced

Counting onto Gauss's rings in order leaves exactly one possible wheel, and it's ours.

Start with the rings alone. Ring m is m evenly spaced points on a circle, one ring for every whole number. Mathematicians call these points the roots of unity, and since Gauss they have been the home of fractions and of the Möbius balance.

Now count onto them: 1, 2, 3 and on, one number per point. Fill the rings smallest first, and go around each ring starting just past the seam. There is exactly one way to do that: ring m receives the m numbers after the triangular number T(m−1), which is our wheel.

So the wheel isn't one design among many. It is the counting order of a skeleton that was already there. What the counting adds is the tick side: visits that lock composites, the even/odd axis, and the lanes at the seam.

## Change one piece

Only our wheel keeps all eight facts. Every other winding breaks at least two, checked on every number up to 3 million.

| Winding | Spokes | Visit lock | Two per spoke | Even axis | Mertens | Seam composite | Rich lane | Aligned laps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Our wheel: sizes 1, 2, 3 … | yes | yes | yes | yes | yes | yes | yes | yes |
| Even sizes 2, 4, 6 … | yes | yes | yes | no | no | yes | yes | yes |
| Fixed circle of 12 | no | yes | no | yes | no | yes | yes | yes |
| Skip repeat points | no | no repeats | no repeats | no | yes | no seam tick | yes | no |
| Same points, renumbered along diagonals | yes | no | no | no | yes | yes | yes | no |
| Every other layer counted backwards | yes | no | no | no | yes | no | no | no |
| Odd sizes 1, 3, 5 … (layers end at squares) | no | no | no | yes | no | yes | no | no |
| Doubling sizes 1, 2, 4, 8 … | no | no | no | no | no | no | no | no |

The columns: every fraction draws a line (spokes); third visits are never prime (visit lock); no spoke holds more than two primes; the half-turn tick is always even (even axis); the running balance equals the Mertens function; the closing tick is composite; the opening tick is at least 1.5 times as prime-rich as chance; every lap starts at the seam or half a turn from it (aligned laps).

The visit lock survives exactly where the laps are aligned. The triangular numbers do that for free, because T(m−1) is always a multiple of half of m. The Mertens column needs every ring size once, in order. Only sizes 1, 2, 3 give both.

The fixed circle keeps the lock but loses the two-prime limit: there, one open spoke carried 54,271 primes, which is Dirichlet's theorem at work. The doubling wheel loses everything, including the seam, where its closing ticks are the Mersenne numbers.

## New fits found while checking

Ten links between pieces turned up while placing the facts, each checked by computer here. Most are classical facts seen in a new place, and each says which.

1. **Every layer is one lap of a fixed circle.** Layer m holds exactly one number of each remainder mod m. On odd layers each tick is its number's remainder; on even layers the remainders are rotated half a turn, because T(m−1) is always a multiple of half of m. So the wheel stacks one lap of every fixed circle, and a layer's seats are simply its numbers that share no factor with m. *Simple; checked to layer 5,000.*
2. **Each ring is one polynomial, and its values name primes.** Ring m's fresh ticks are the roots of the cyclotomic polynomial Φm, whose degree is φ(m) and whose roots sum to μ(m). Φm(1) is the prime p when m is a power of p, and 1 otherwise, which is the von Mangoldt function behind the prime number theorem. At 2, the rings multiply out to 2^m − 1, and every ring but 1 and 6 adds a brand-new prime factor (Zsigmondy). A ring can be drawn with compass and straightedge exactly when φ(m) is a power of 2, which is where the Fermat primes come in. *Classical; checked to ring 300.*
3. **The Riemann Hypothesis shows up on both sides.** On the angle side, the arrows of every fresh tick on rings 1 to n add up to exactly M(n). RH says those spokes spread around the circle evenly to within about √n (Franel–Landau). On the tick side, RH says the count of primes stays within about √x·log x of its smooth estimate (von Koch). *Classical; checked to ring 1,600, where the spread error grows like n^0.36.*
4. **The seam is a catalog of quadratic lanes.** Every column near the seam is a quadratic. Columns a triangular number of ticks before the seam (0, 1, 3, 6, 10 …) are always composite, because they hold sums of runs of consecutive numbers, which factor. Columns after the seam all stay alive, and quadratic residues set each one's richness, which is where reciprocity enters. The first (discriminant −7, a Heegner number) runs 1.97 times richer than chance. The richest of the first 4,000 (c = 586) runs 3.32 times richer and, per odd value, ties Euler's n² + n + 41. *Simple; checked on layers 200 to 5,000, and on 100,000 layers per lane.*
5. **A quadratic draws a straight line here only when twice its lead coefficient is a square.** A sequence At² + … turns √(2A) of a turn per step on the wheel. When 2A is a perfect square it locks onto a straight row; otherwise it circles forever. So Euler's n² + n + 41, n² + 1 and Ulam's diagonals are curves on this wheel, and its straight rows are a different family. *Simple; checked on eight quadratics.*
6. **The squares ride a √2 spin, and Pell's equation is where they land on the seam.** n² sits at angle √2·n − 1/2 (in turns) to within 0.09/n. It lands exactly on the seam only at n = 1, 6, 35, 204, 1189 …, the square triangular numbers 1, 36, 1225, 41616 …, which come from Pell's equation. *Classical numbers, new placement; checked to n = 2 million.*
7. **Layers with many small factors are richest per seat.** A seat on layer m holds a prime about m/φ(m) times as often as a random number its size. On layer 9,240 (2³·3·5·7·11), 27% of its 1,920 seats hold primes; on the prime layer 7,919, under 6% of 7,918 do. *Checked on layers 1,000 to 10,000, to within 1%.*
8. **The sieve's local picture overcounts.** Multiplying the open-seat fraction of every wheel up to the square root predicts 6% more primes than exist at 100 million. The gap grows toward 12% (2e^−γ), so the local picture alone can't get the count right: the same wall the knockout test hit. *Classical (Mertens); checked to 10^8.*
9. **Mirror pairs add up to the layer's square.** Tick k and tick m − k of layer m always sum to m², so every layer comes folded the way Goldbach's problem is: on layer 6, 17 + 19 = 36. Neighboring seam numbers do the same: T(m−1) + T(m) = m². *Simple; checked to layer 3,000.*
10. **Each spoke's two shots are chained.** The second shot is twice the first plus b², where b is the spoke's denominator: a cousin of the Sophie Germain pairs (p, 2p + 1). Among spokes with denominators up to 2,000, 10,062 have both shots prime. *Simple; checked.*

## The atlas

79 prime facts, theorems and mysteries, each placed where it lives on the wheel. 41 are native (they fall out of the rule), 32 translate (they can be said on the wheel, but it adds no structure), and 6 are foreign so far.

### Rings and angles

| Fact | Where it lives | How it shows up | Fit | Status |
| --- | --- | --- | --- | --- |
| Fractions | Spokes | Each fraction a/b is a straight spoke, first visited on ring b | Native | Proven |
| Euler's φ(m) | Ring m | The count of fresh ticks on ring m, and of its prime seats | Native | Proven |
| φ(d) summed over the divisors of m is m | Ring m | Each tick on ring m is a fresh tick of exactly one ring d that divides m | Native | Proven |
| Möbius function μ(m) | Ring m | The fresh arrows of ring m sum to μ(m) | Native | Proven |
| Ramanujan sums | Ring q | The fresh arrows spun n times; at n = 1 this is μ(q) | Native | Proven |
| Cyclotomic polynomials | Ring m | Ring m's fresh ticks are the roots of Φm: degree φ(m), root sum μ(m) | Native | Proven |
| Von Mangoldt function | Ring m | Φm(1) is p on rings that are powers of a prime p, and 1 otherwise | Native | Proven |
| Mersenne numbers | Rings at 2 | 2^m − 1 is the product of Φd(2) over the d dividing m, so a Mersenne prime needs m prime | Native | Proven |
| Zsigmondy's theorem | Rings at 2 | Every ring except 1 and 6 brings 2^m − 1 a brand-new prime factor | Native | Proven |
| Constructible polygons, Fermat primes | Ring m | Ring m can be drawn with compass and straightedge exactly when φ(m) is a power of 2; only five Fermat primes are known | Native | Proven |
| Decimal periods | Spokes 1/p | 1/p repeats every d digits, where d is the first ring at which p divides 10^d − 1 | Translates | Proven |
| Fermat's little theorem | Rings at a | p divides a^(p−1) − 1, so p first shows up as a factor on a ring that divides p − 1 | Translates | Proven |
| Artin's primitive root conjecture | Rings at 2 | 2 is a primitive root mod p when p first divides 2^d − 1 at d = p − 1 | Translates | Open |
| Farey sequences | Spokes | The spokes born on rings 1 to n, in order around the circle | Native | Proven |
| Farey neighbors, mediants, Stern–Brocot tree | Spokes | Neighbors a/b and c/d satisfy bc − ad = 1; the next spoke born between them is the mediant | Native | Proven |
| Ford circles | Drum | The empty zone around each column: no other tick of ring m comes within 1/(bm) of a/b | Native | Proven |
| Dirichlet approximation, continued fractions | Slip | Every angle has near-miss spokes, and its best ones are its continued fraction | Native | Proven |
| Hurwitz's theorem, the golden ratio | Slip | The golden angle is the hardest angle to approximate with spokes | Translates | Proven |
| Three-gap theorem | Curves, fixed circles | Ticks at an irrational step leave at most three gap sizes | Translates | Proven |
| Circle method (Hardy–Littlewood) | Wedges | Major arcs are the wedges around low-denominator spokes; minor arcs are the shimmer between | Native | Proven |
| Weyl equidistribution | Curves | A quadratic whose 2A is not a square spins evenly around the wheel | Translates | Proven |

### The running balance and the Riemann Hypothesis

| Fact | Where it lives | How it shows up | Fit | Status |
| --- | --- | --- | --- | --- |
| Mertens function M(n) | Running balance | The running sum of the ring balances, which is also the sum of every fresh arrow on rings 1 to n | Native | Proven |
| Prime number theorem | Running balance | Equivalent to the balance growing slower than the ring count: M(n) = o(n) | Native | Proven |
| Riemann Hypothesis | Running balance | Equivalent to M(n) staying within n^(1/2 + ε) | Native | Open |
| Franel–Landau | Spokes | RH is equivalent to the spokes born on rings 1 to n spreading evenly to within about √n | Native | Open |
| Von Koch's form of RH | Ticks | RH is equivalent to the prime count staying within about √x·log x of li(x) | Translates | Open |
| Mertens conjecture | Running balance | The guess that the balance never passes √n; disproved in 1985 | Native | False |
| Redheffer matrix | Ring divisibility table | Which ring revisits which, plus a column of ones; its determinant is M(n) | Native | Proven |
| Sarnak's conjecture (Möbius randomness) | Ring balances | The balances should not correlate with any simple pattern | Translates | Open |
| Pólya conjecture | Ring balances | The Liouville version of the lean; it first fails at 906,150,257 | Translates | False |
| Robin's criterion | Nowhere yet | RH as a bound on divisor sums | Foreign | Open |
| Zeta zeros, explicit formula | Problem Wheels | Zeros as spinning wheels that add up to the prime count | Translates | Open |
| Montgomery's pair correlation | Nowhere yet | The zeros space out like eigenvalues of random matrices | Foreign | Open |
| Skewes's number | Ticks | The prime count crosses li(x) infinitely often, but not below 10^19 | Translates | Proven |

### Ticks: the counting numbers

| Fact | Where it lives | How it shows up | Fit | Status |
| --- | --- | --- | --- | --- |
| Floyd's triangle | Layers | Its rows are the layers | Native | Proven |
| Visit lock | Spokes | The g-th visit holds a multiple of g (odd g) or of g/2 (even g) | Native | Proven |
| Each layer is one lap mod m | Layers | The seats are the numbers coprime to m, exactly φ(m) of them | Native | Proven |
| Two shots per spoke, chained | Spokes | At most two primes per spoke; the second shot is 2 × the first + b² | Native | Proven |
| Parity axis | Half-turn | Evenness is pinned to the half-turn on every layer | Native | Proven |
| Triangular numbers | Seam | The seam holds T(m), and neighboring seam numbers sum to squares | Native | Proven |
| Mirror pairs | Layers | Ticks k and m − k of layer m sum to m² | Native | Proven |
| Gauss's Eureka theorem | Seam | Every number is a sum of three or fewer seam numbers | Translates | Proven |
| Polite numbers | Columns before the seam | Columns a triangular distance before the seam hold sums of consecutive runs, so they are always composite | Native | Proven |
| Lazy caterer primes | First column after the seam | Discriminant −7; never blocked by wheels that are 3, 5 or 6 mod 7; 1.97 times chance | Native | Open |
| Quadratic reciprocity | Seam columns | Turns “is −D a square mod p” into “what is p mod D”, which picks each column's blocking wheels | Native | Proven |
| Heegner numbers, Euler's n² + n + 41 | Seam columns, curves | The first column's −7 is a Heegner number; Euler's polynomial is a curve here; column 586 ties it per odd value | Translates | Checked |
| Bateman–Horn conjecture | Every straight row | A row's prime density is its open-seat product, matched within 0.3% on seven columns | Native | Open |
| Bunyakovsky conjecture | Every live row | Each live row should hold endless primes; no quadratic case is proven | Native | Open |
| Landau's fourth problem (n² + 1) | Curves | A curve on this wheel, since 2A = 2 | Translates | Open |
| Ulam spiral | Curves | Its diagonals (4n² + bn + c) are curves here; each winding straightens its own family | Translates | Checked |
| Sacks spiral | Seam | Sacks puts one square on each turn, all on one ray; the wheel puts one triangular number on each turn, all on the seam | Translates | Proven |
| Pell's equation, square triangular numbers | Squares' curve | The squares spin by √2 per step and hit the seam at Pell solutions | Native | Proven |
| Prime in every layer | Layers | A prime between neighboring triangular numbers (OEIS A066888) | Native | Open |
| Legendre's conjecture | Squares' curve | A prime between neighboring squares, about √2 layers apart; open even assuming RH | Translates | Open |
| Oppermann's and Andrica's conjectures | Layers | Andrica: consecutive primes are always less than about √2 rings apart | Translates | Open |
| Bertrand's postulate | Rings | A prime in every band from radius r to √2·r | Translates | Proven |
| Prime gaps | Layers | Cramér's guess would put a prime in every large layer; the proven x^0.525 and RH's √x·log x are too coarse | Translates | Open |
| Seats by layer | Layers | A seat holds a prime m/φ(m) times as often as chance | Native | Checked |

### Gears: the local picture

| Fact | Where it lives | How it shows up | Fit | Status |
| --- | --- | --- | --- | --- |
| Sieve of Eratosthenes | Gears | Each wheel p takes out every p-th number | Native | Proven |
| Chinese remainder theorem | Gears | The wheels mesh independently | Translates | Proven |
| Mertens' third theorem | Gears | The open-seat product up to √x overcounts primes, heading to 2e^−γ ≈ 1.12 | Native | Proven |
| Parity problem | The wall | Sieves can't tell an odd count of prime factors from an even one: the knockout wall | Native | Proven |
| Twin primes, twin prime constant | Neighbor seats | Seat pairs two ticks apart; the constant is the product of the open pair fractions | Native | Open |
| Prime k-tuples | Gears | A pattern is admissible when no wheel blocks all of its seats | Native | Open |
| Bounded gaps (Zhang, Maynard) | Neighbor seats | Infinitely many prime pairs at most 246 apart | Translates | Proven |
| Brun's theorem | Neighbor seats | The reciprocals of the twin primes add up to a finite sum | Translates | Proven |
| Chen's theorem | Neighbor seats | Infinitely many p with p + 2 prime or a product of two primes | Translates | Proven |
| Sophie Germain primes | Spokes | Chained shots (p, 2p + b²) are a cousin of (p, 2p + 1) | Translates | Open |

### Other windings, and what doesn't fit yet

| Fact | Where it lives | How it shows up | Fit | Status |
| --- | --- | --- | --- | --- |
| Dirichlet's theorem | Fixed circle, and every layer | Each open spoke of a fixed circle carries endless primes, shared evenly | Translates | Proven |
| Chebyshev's bias, prime races | Fixed circle of 4 | Primes that are 3 mod 4 usually lead; the size of the lead is known only under RH-type guesses | Translates | Open |
| Green–Tao theorem | Fixed circles | Some fixed circle has a spoke with any number of primes in a row | Translates | Proven |
| Mersenne seam | Doubling wheel | The doubling wheel's closing ticks are the Mersenne numbers | Translates | Proven |
| Collatz | Doubling wheel | Explored on Problem Wheels' doubling wheel | Translates | Open |
| Goldbach's conjecture | Mirror pairs, folded wheel | Each layer folds onto m²; the local constraints show, the global claim is open | Translates | Open |
| Ternary Goldbach | Wedges | Proved with the circle method (Helfgott, 2013; widely accepted) | Translates | Proven |
| Unique factorization | Nowhere yet | The wheel shows only the factors a number shares with its own layer | Foreign | Proven |
| Wilson's theorem | Nowhere yet | A product over a whole fixed circle; the wheel adds, it doesn't multiply | Foreign | Proven |
| Sums of two squares | Fixed circle of 4 | The 4-circle says which primes qualify; the two squares need a second dimension | Foreign | Proven |
| Erdős–Kac theorem | Nowhere yet | The count of prime factors is bell-shaped | Foreign | Proven |

## What doesn't fit yet

The six foreign pieces share one reason: the wheel adds, and they need multiplying, a second dimension, or the zeros themselves.

- **Multiplying.** Unique factorization, Wilson's theorem and Erdős–Kac are about whole products. The wheel only shows the factors a number shares with its own layer, never its full factorization. A home for them would need the gears running alongside, each number lit on every gear that divides it.
- **A second dimension.** Sums of two squares live on a flat grid of points, not on a line wound around circles. The 4-circle sorts which primes qualify, but the two squares need a wheel in two dimensions.
- **The zeros.** Montgomery's pair correlation and Robin's criterion talk about the zeta zeros and divisor sums directly. Problem Wheels draws the zeros as spinning wheels, but their spacing has no picture here yet.

The big open problems (Goldbach, twin primes, a prime in every layer, Legendre) do fit, but only locally. The wheel shows every constraint each gear puts on a seat. What's missing is always the last step, from "this seat is open" to "this seat holds a prime", which is the wall.

## What to probe next

Five probes would test the map rather than decorate it.

- **Push the seam catalog.** Search columns past 4,000, and around the other spokes, for the richest lanes. Then check whether their richness tracks class numbers the way Euler's polynomial does.
- **Count the double shots.** Predict from the open-seat products how many spokes should get both shots prime, write the prediction down, then count.
- **Watch the Riemann Hypothesis from both sides.** Draw the spoke spread (angles) and the prime count's error (ticks) on the same wheel, and see whether they move together ring by ring.
- **Build the second dimension.** A wheel for points on a flat grid would give sums of two squares and the Gaussian primes a home.
- **Train a small network on wheel coordinates,** then compare the geometry it builds with this map.

The scripts behind every check here are knockout\_rule.py and atlas\_checks.py, alongside the other probes.

## Predictions log

Each prediction is written down before its check, then checked. Nine have held so far, one of them by search rather than proof. One failed: the far jump came in closer than predicted on layer 52, and the reason became P8.

| # | Written | Prediction, before checking | What the check found | Outcome |
| --- | --- | --- | --- | --- |
| P1 | Oct 8, 2026 | **Two shots per spoke.** For odd denominators up to 5,000, the gear rule predicts 49,428 spokes with both shots prime. The count lands within 2%. | 49,355 spokes, 0.15% under the prediction. | Held |
| P2 | Oct 8, 2026 | **Hot seats down the seam.** On layers past 100,000, each seam column's measured boost matches its gear-rule boost within a few percent, and the ranking holds. | Layers 100,001 to 100 million, every value settled exactly, judged by criteria written down before the run. All 18 columns tested (the first 12 after the seam and the six richest of the first 4,000) land within 0.09% of their gear-rule boosts. The measured order matches the gear-rule order in all 153 pairs. The misses are smaller than pure chance would make them. | Held |
| P3 | Oct 8, 2026 | **The far jump.** For rings up to 37 (layers 52 to 57), the first stretch that could wipe out a layer starts between 1 billion and 1 trillion. | Failed at layer 52. Found exactly (every turning that wipes the window, locked to the line by CRT), then confirmed by walking the line to 4.7 billion. Layer 52 first comes at 133 million, about 7 times under the floor; layers 53 to 57 land inside, at 2.8 to 4.7 billion. Why: each wiping turning lands once per lap, scattered, so the first comes near the lap divided by their count, about 240 million here. P8 tests that rule. | Failed |
| P4 | Oct 8, 2026 | **Goldbach under free phases.** Goldbach's search range grows like the square of the ring reach; a layer grows only like the reach. So freely turned rings (ring 2 on the evens, every other ring with its real number of seams) lose the power to wipe out every prime pair, and the share of even numbers they can wipe heads toward zero. Unsure below the low thousands. | Exact solver: up to 400, most even numbers not divisible by 3 can be wiped; near 700, 4 of 11 can. A hard search finds wipe-outs up to about 1,000 and none from 2,000 to 32,000. There the best turning found removes about three quarters of the real pairs near 2,000 but only half near 32,000. Search, not proof. | Held |
| P5 | Oct 8, 2026 | **Composites by geometry alone.** With no division, the mirror (evens) plus the visit lock (third or later visits) flag 60 to 65% of composites on their own layers. | 64.2% of 1.85 million composites on layers 3 to 2,000: the mirror catches 54.0%, the visit lock 10.2% more. No prime is ever flagged. | Held |
| P6 | Oct 8, 2026 | The 4D wheel is safe by width. In a tread wheel with two turning planes, where layer m holds m × (m+1) numbers, no turning of the rings can wipe out any layer. Our 2D wheel is the only rung where the rings can aim at a whole layer. | No 4D layer from 2 to 60 can be wiped, as far as the most-in-a-row values are known. At layer 60 the rings cover at most 26% of the layer; ours reach 244% at layer 391. With three clocks (6D): 8% at layer 22. Past layer 60 it is unproven: the most the rings can cover in a row would have to grow no faster than the biggest ring to the 4/3 power, and the best proven ceiling is the biggest ring squared ([Erdős problem 687](https://www.erdosproblems.com/687)). | Held |
| P7 | Oct 8, 2026 | A 4D creature sees more on its own layer. With no division, its two clocks flag about 70% of composites, against 64% for our single ring with the mirror. | 72.4%, because one of its clocks is always even, so every even is caught for free. Three clocks flag 80.0%. | Held |
| P8 | Oct 8, 2026 | **Count the turnings.** For rings up to 43 (layers 61 to 63), the first stretch of 63 covered numbers lands near the lap divided by the number of wiping turnings: about 2.7 billion, between 0.14 and 10.8 billion. | 3,732,574,514, found by walking the line: 1.4 times the estimate. | Held |
| P9 | Oct 8, 2026 | **Calmer than coin flips.** Across 300 fresh lanes to layer 100 million, the misses against the gear rule wobble less than 60% as much as coin flips over the whole run. The calm grows at every tenfold longer stretch, by a steady amount (a straight line against the log of the stretch, 0.04 to 0.10 per tenfold), starting at 80% or more for 100-layer stretches. Pure coin flips stay near 100%, and putting only the rings up to 1,000 on their real schedule gives part of the calm (under 85%). | All four held, on 30 billion values settled exactly. Whole run 45%; 100-layer stretches 89%, falling 7.5 points per tenfold on a line that misses no step by more than 0.7 points. Coin flips 92 to 100%. Rings up to 1,000 on schedule track the real lanes for short stretches, then flatten near 70% past about 10,000 layers: the calm grows only while rings are finishing their laps. Plain primes follow the same straight-line law ([Montgomery and Soundararajan](https://arxiv.org/abs/math/0409258)). | Held |
| P10 | Oct 8, 2026 | **Kimi's parabolas save layers.** Confine each ring to the landing spots its parabola visits (the gear rule's lane test, seen from the ring), with ring 2 on the evens. Then at least one layer that freely turned rings can wipe becomes safe; the first layer confined rings can wipe comes after 18, and the unbroken wipeable stretch starts after 41; and confinement only delays, so from some layer at or before 100, every layer through 150 can be wiped again. | All three held, exactly: the free version reproduces the known list, and small layers were re-checked by brute force over every confined turning. The parabolas save 21 layers, so every layer up to 26 and 19 more up to 57 hold a prime from structure alone. The first confined wipe is layer 27, and from layer 58 through 256 every layer can be wiped. Every layer whose wipe had almost no slack was saved. From 58 on, only where the walk actually is protects a layer: Kimi's routing wall starts there. | Held |

## Sources

The pages behind the classical claims, each opened while building this.

- Farey sequences and Franel–Landau: [Farey sequence](https://en.wikipedia.org/wiki/Farey_sequence), [Farey neighbors](https://proofwiki.org/wiki/Difference_between_Adjacent_Terms_of_Farey_Sequence), [Stern–Brocot tree](https://en.wikipedia.org/wiki/Stern%E2%80%93Brocot_tree), [Ford circles](https://mathworld.wolfram.com/FordCircle.html)
- Rings as polynomials: [cyclotomic polynomial](https://proofwiki.org/wiki/Definition:Cyclotomic_Polynomial), [product over divisors](https://proofwiki.org/wiki/Product_of_Cyclotomic_Polynomials), [values at 1 (OEIS A020500)](https://oeis.org/A020500), [Möbius as a root sum (OEIS A008683)](https://oeis.org/A008683), [Ramanujan's sum](https://en.wikipedia.org/wiki/Ramanujan%27s_sum), [totient sum](https://proofwiki.org/wiki/Sum_of_Euler_Phi_Function_over_Divisors)
- Values at 2 and 10: [Zsigmondy's theorem](https://proofwiki.org/wiki/Zsigmondy%27s_Theorem), [Mersenne primes](https://en.wikipedia.org/wiki/Mersenne_prime), [Fermat numbers](https://en.wikipedia.org/wiki/Fermat_number), [constructible polygons](https://en.wikipedia.org/wiki/Constructible_polygon), [repeating decimals](https://en.wikipedia.org/wiki/Repeating_decimal), [Artin's conjecture](https://en.wikipedia.org/wiki/Artin%27s_conjecture_on_primitive_roots)
- The balance and RH: [Mertens function](https://en.wikipedia.org/wiki/Mertens_function), [Möbius function and the prime number theorem](https://en.wikipedia.org/wiki/M%C3%B6bius_function), [Redheffer matrix](https://mathworld.wolfram.com/RedhefferMatrix.html), [von Koch's form](https://aimath.org/WWN/rh/articles/html/92a), [Robin's theorem](https://mathworld.wolfram.com/RobinsTheorem.html), [Pólya conjecture](https://en.wikipedia.org/wiki/P%C3%B3lya_conjecture), [Liouville function](https://en.wikipedia.org/wiki/Liouville_function), [Sarnak's conjecture](https://ar5iv.labs.arxiv.org/html/2308.11114), [Skewes's number](https://en.wikipedia.org/wiki/Skewes%27s_number), [li(x) above π(x) to 10^19](https://ar5iv.arxiv.org/html/1511.02032), [Montgomery's pair correlation](https://en.wikipedia.org/wiki/Montgomery%27s_pair_correlation_conjecture)
- Approximation: [Hurwitz's theorem](<https://en.wikipedia.org/wiki/Hurwitz%27s_theorem_(number_theory)>), [three-gap theorem](https://en.wikipedia.org/wiki/Three-gap_theorem), [circle method](https://en.wikipedia.org/wiki/Hardy%E2%80%93Ramanujan%E2%80%93Littlewood_circle_method)
- Quadratics and the seam: [Floyd's triangle](https://en.wikipedia.org/wiki/Floyd%27s_triangle), [visit divisibility (Math::PlanePath)](https://manpages.debian.org/testing/libmath-planepath-perl/Math::PlanePath::GcdRationals.3pm), [lazy caterer primes (OEIS A055469)](https://oeis.org/A055469), [Bateman–Horn conjecture](https://en.wikipedia.org/wiki/Bateman%E2%80%93Horn_conjecture), [Bunyakovsky conjecture](https://en.wikipedia.org/wiki/Bunyakovsky_conjecture), [Heegner numbers](https://en.wikipedia.org/wiki/Heegner_number), [quadratic reciprocity](https://mathworld.wolfram.com/QuadraticReciprocityTheorem.html), [Ulam and Sacks spirals](https://en.wikipedia.org/wiki/Ulam_spiral), [square triangular numbers](https://en.wikipedia.org/wiki/Square_triangular_number), [Gauss's Eureka theorem](https://en.wikipedia.org/wiki/Fermat_polygonal_number_theorem), [polite numbers](https://en.wikipedia.org/wiki/Polite_number)
- Gaps and layers: [prime in every layer (OEIS A066888)](https://oeis.org/A066888), [Landau's problems](https://en.wikipedia.org/wiki/Landau%27s_problems), [Legendre is open even under RH](https://arxiv.org/pdf/2309.02325), [Oppermann's conjecture](https://arxiv.org/pdf/1310.1323), [Andrica's conjecture](https://mathworld.wolfram.com/AndricasConjecture.html), [Cramér's conjecture and the RH gap bound](https://arxiv.org/pdf/1908.08613), [Baker–Harman–Pintz](https://sugaku.net/oa/W2094054391), [prime gaps and bounded gaps](https://en.wikipedia.org/wiki/Prime_gap)
- Sieves and pairs: [Mertens' third theorem](https://proofwiki.org/wiki/Mertens%27_Third_Theorem), [the sieve's 2e^−γ overcount](https://sites.math.rutgers.edu/~alexk/files/BrunSelberg.pdf), [parity problem](https://en.wikipedia.org/wiki/Sieve_theory), [prime k-tuples](https://en.wikipedia.org/wiki/First_Hardy%E2%80%93Littlewood_conjecture), [twin prime constant](https://t5k.org/glossary/xpage/TwinPrimeConstant.html), [Brun's theorem](https://en.wikipedia.org/wiki/Brun%27s_theorem), [Chen's theorem](https://en.wikipedia.org/wiki/Chen%27s_theorem), [Helfgott and ternary Goldbach](https://en.wikipedia.org/wiki/Harald_Helfgott)
- Fixed circles and the rest: [Dirichlet's theorem](https://en.wikipedia.org/wiki/Dirichlet%27s_theorem_on_arithmetic_progressions), [Chebyshev's bias](https://en.wikipedia.org/wiki/Chebyshev%27s_bias), [Green–Tao theorem](https://en.wikipedia.org/wiki/Green%E2%80%93Tao_theorem), [sums of two squares](https://mathworld.wolfram.com/Fermats4nPlus1Theorem.html), [Wilson's theorem](https://en.wikipedia.org/wiki/Wilson%27s_theorem), [Erdős–Kac theorem](https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93Kac_theorem)
