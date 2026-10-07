# The Prime Tread Wheel

**Ratio as slip on a growing wheel of counting**

Obi (Sylvan Gaskin), with Claude. October 2026.

## Abstract

We roll the counting numbers onto a wheel that grows by one unit per layer while the unit itself never changes size. From this one rule, ratio becomes spokes, divisibility becomes revisits, parity becomes a fixed axis, and the Möbius function becomes a balance of arrows on every layer. Placing a number on the wheel computes its remainder against the lap's own modulus, so the whole object is also a multiplexer whose frame enumerates the moduli. Most of these facts are classical. What the wheel adds is a single picture in which all of them are visible at once, plus interactive pages and scripts that reproduce every number below. Each claim is tagged **proven**, **checked** (by computer), **classical** (known before us) or **open**.

## 1. Construction

Layer m carries the m numbers that follow the triangular number T(m−1), where T(m) = m(m+1)/2. Tick k of layer m sits k/m of the way around. Every layer is one unit longer than the layer inside it, and every tick is one unit from its neighbors. Laid flat, the layers are the rows of Floyd's triangle [1].

## 2. The slip law

Each new layer adds exactly one unit, spread evenly around the turn. So at a fraction f of the turn, the ticks of one layer sit f of a unit off the ticks of the layer below. The stack lines up again after b layers exactly when b·f is a whole number. At the seam the slip is zero and the layers stack in straight columns; at the half-turn the slip is one half and the stack forms bricks.

Near the spoke of a fraction a/b, the ticks fall into rows that run parallel to the spoke, 1/b of a unit apart: a tick at angle a/b + j/(bm) on layer m sits exactly j/b of a unit from the spoke, measured along its ring, on every layer. That grain is what makes each spoke's wedge visible. Because every angle is an exact fraction, nothing drifts, and the picture is the same at every scale. Polar plots of the primes instead get their arms from near misses such as 44/7 ≈ 2π, which drift into spirals [2]. Ratio is not painted onto the wheel. Ratio is the slip. *(Elementary; a way of seeing.)*

## 3. The visit theorem

Tick k of layer m lies on the spoke a/b, where g = gcd(k, m), a = k/g and b = m/g. It is the g-th visit to that spoke, and its number is x = g(gb² − b + 2a)/2. So x is divisible by g when g is odd and by g/2 when g is even, which makes every third or later visit composite. Each spoke therefore carries at most two primes: its first visit, and its second visit when b is odd. Every layer m ≥ 3 offers exactly φ(m) seats where a prime can sit.

*Proven, and checked on every tick through layer 800.* The divisibility is already noted in the documentation of Math::PlanePath's GcdRationals path, which follows Lance Fortnow's 2004 gcd enumeration of the rationals [3]. The two-primes and φ(m) corollaries follow in a line; we have not found them stated.

## 4. The parity axis

T(m−1) and ⌊m/2⌋ always share parity, because the triangular numbers run odd, odd, even, even. So a number is even exactly when its tick lies an even number of steps from the halfway tick of its layer. The halfway tick holds ⌊m²/2⌋, which is always even, and the half-turn spoke holds twice the squares: 2, 8, 18, 32, 50. On every layer m ≡ 2 (mod 4) the fresh ticks are all even, so that layer's primes sit on second visits. *(Proven; checked on layers 1 to 5,000.)*

## 5. The layer balance

Point a unit arrow at each fresh tick of layer m (gcd(k, m) = 1). The arrows sum to exactly +1, −1 or 0: the Möbius value μ(m), because the fresh ticks are the primitive m-th roots of unity [4]. All m arrows of a layer cancel, and on a prime layer every tick is fresh except the junction at 1, so every prime layer balances to −1.

The running total of the balances is the Mertens function M(n). The Riemann Hypothesis is equivalent to M(n) = O(n^(1/2+ε)) for every ε > 0 [5]. From layer 33 through layer ten million, |M(n)| stays below 0.57·√n. Kotnik and van de Lune found the largest value of |M(x)|/√x for 10⁴ ≤ x ≤ 10¹⁴ to be 0.570591 [6]. *(Classical; our range checked.)*

## 6. The junction lanes

The closing tick of each layer holds T(m), composite for every m ≥ 3. The opening tick holds T(m−1) + 1, the lazy caterer numbers [7]. Since 8·(T(m−1) + 1) = (2m − 1)² + 7, an odd prime p divides a lane number only when −7 is a square mod p. So every prime p ≡ 3, 5 or 6 (mod 7) never blocks the lane: 3, 5, 13, 17, 19, 31, and so on.

Through layer 100,000 the lane holds 9,863 primes. The open-seat (Bateman–Horn) prediction is 9,836, and random numbers of the same size would give about 4,986. The primes of this form are listed as OEIS A055469 and conjectured infinite [8]. *(Known; checked.)*

## 7. The wall

A knockout test hides each layer's primes and asks which smaller wheels are needed to recover them. About half of the wheels below the square root are needed, but the same share holds for any interval of that length, so this is not special to the wheel. The largest wheel needed climbs to 98% of the square root by layer 3,000. The wheel shows the sieve's boundary clearly. It does not move it. *(Checked.)*

## 8. The wheel as a multiplexer

A time-division multiplexer is a rotating switch: a frame of slots, one number per slot per lap. The wheel is a multiplexer whose frame gains one slot per lap. The number n = T(m−1) + k lands in slot k of lap m, so placing a number computes its remainder mod m, and no division is performed anywhere: the slot spacing is the operation. Each lap's frame is a complete residue system. One detail keeps the picture exact: for even m, T(m−1) ≡ m/2 (mod m), so the lap's origin sits a half-turn off — number 2 rides at the half-turn tick of layer 2. Slot means steps since the lap's own origin, and the origin rotates on even laps. *(Follows from the construction.)*

What survives frame growth is a channel. The spoke a/b keeps its identity while the frame lengthens and returns every b laps; that is the slip law of §2 in switching language. Its period is its denominator, and its visits are numbered by g = gcd(k, m): the rational is the invariant under change of lap, and the visit count is what accumulates. Section 3 now reads: every channel carries at most two primes, then composites only, and every lap offers exactly φ(m) channels that can carry a prime. *(Proven above.)*

Lehmer's mechanical and photoelectric sieves of the 1920s and 30s were fixed rings of this kind, spun together so that numbers with chosen remainders were caught by alignment [11]. The Chinese remainder theorem stacks fixed rings in parallel: operate on each separately and read the answer back. The wheel makes one change: the frame length is the lap index, so the set of moduli is the counting numbers themselves, one per lap, and no ring is built twice. Frame growth is the enumeration of moduli. *(Classical machines; the growing-frame observation is a way of seeing.)*

Held as one object, the wheel is a space-time ledger: laps accumulate, ticks cycle, and every number is a single event with one (lap, slot) coordinate. The space-time globes used to teach relativity make the same move — one object, a change of frame a rotation, the invariant what survives the rotation. Here the invariant under frame growth is the rational. This is a way of seeing, not an identification: the wheel carries no metric and no boost symmetry.

What a multiplexer does is route. Routing is answered exactly by the gears, and that exact answer is the sieve; the square of the largest gear is where a fixed channel map stops tracking the primes (§7). The wheel routes for free. Decoding remains the wall. *(The framing adds nothing to and takes nothing from §7.)*

## 9. Open question

Does every layer hold a prime? Since every prime on a layer sits on one of its φ(m) seats, the question is whether all the seats of some layer can be composite at once. This is the conjecture that a prime lies between any two consecutive triangular numbers [9], a triangular cousin of Sierpiński's 1958 hypothesis H1 for square tables [10]. No layer from 2 to 10,000 is empty. The closest call is the composite run 114–126: 13 numbers against layer 15's width of 15. From layer 100 on, no composite run reaches 30% of its layer's width. *(Open; checked to layer 10,000.)*

## Conclusion

One rule, counting onto a wheel that grows by a single unit, makes ratio, divisibility, parity and the Möbius balance visible as geometry. The primes are the seats this geometry leaves open. No result here is a new theorem. Where the picture goes next is the open part.

## Reproduce

`cd probes && python3 verify.py` reproduces every number above (Python 3 and numpy; about ten seconds).

## References

1. [Floyd's triangle](https://en.wikipedia.org/wiki/Floyd%27s_triangle), Wikipedia.
2. [Prime spirals](https://3blue1brown.com/lessons/prime-spirals), 3Blue1Brown.
3. [Math::PlanePath::GcdRationals](https://manpages.debian.org/testing/libmath-planepath-perl/Math::PlanePath::GcdRationals.3pm), after Lance Fortnow, "Counting rationals quickly" (2004).
4. [Möbius function](https://en.wikipedia.org/wiki/M%C3%B6bius_function), Wikipedia.
5. [Mertens function](https://en.wikipedia.org/wiki/Mertens_function), Wikipedia.
6. T. Kotnik and J. van de Lune, [On the order of the Mertens function](https://emis.univie.ac.at/journals/EM/expmath/volumes/13/13.4/Kotnik.pdf), Experimental Mathematics 13 (2004).
7. [OEIS A000124](https://oeis.org/A000124), the lazy caterer's sequence.
8. [OEIS A055469](https://oeis.org/A055469), primes of the form k(k+1)/2 + 1.
9. [OEIS A066888](https://oeis.org/A066888), primes between consecutive triangular numbers (conjecture by J. W. Nicholson, 2011).
10. M. Visser, [Sierpiński's Hypothesis H1](https://arxiv.org/html/2512.22413v1) (2025).
11. [Lehmer sieve](https://en.wikipedia.org/wiki/Lehmer_sieve), Wikipedia.
