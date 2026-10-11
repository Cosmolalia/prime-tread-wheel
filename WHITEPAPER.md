# The Prime Tread Wheel — White Paper

**Counting numbers on a wheel that grows by one tick per layer, and what the stagger of that growth knows about the primes.**

Obi (Sylvan Gaskin), with Claude and Kimi. 2026-10-10.

Standalone summary of the full project: the construction, the classical layer,
the stagger field, the exact theorems, the measured statistics, the closed
routes, the held claims, the ratio-dial era, the deadness engine, the quadratic
rhyme probe, the standing wall, and the method. Everything below is cross-checked
against `INSIGHTS.md` (the lab notebook), `PAPER.md` (the short paper), the
`lab/PHASE*` artifacts, and the probe suite. Where those files and this document
disagree, the files win.

---

## 0. Epistemic labels (the contract this paper runs on)

Every claim carries one of four labels:

- **[S] — STATED.** A premise or proposed mechanism. Not derived, not proved by
  plausibility.
- **[F] — FOLLOWS.** Actually entailed by preceding statements.
- **[G] — GAP.** Resolution stops here; the missing piece is named, not filled
  with an adjacent theory.
- **[E] — ESTABLISHED.** Proved here, or machine-verified by a probe whose exact
  command and expected output are on record.

Rules that govern the whole document: never increase the resolution of a claim
beyond what the mechanism specifies; attack connectors, not endpoints; honest
negatives are load-bearing and are kept in writing; superseded readings are
marked, not erased; use the smallest sufficient claim.

---

## 1. The construction — one rule

**[S]** Layer *m* of the wheel holds the *m* numbers T(m−1)+1 … T(m), where
T(m) = m(m+1)/2 is the *m*-th triangular number. Tick *k* of layer *m* sits at
angle 2π·k/m. The wheel grows by one tick per layer while the tick never changes
size. Laid flat, the layers are the rows of Floyd's triangle; rolled onto polar
coordinates, every rational angle in (0,1] owns exactly one spoke, and
irrationals own none.

From this one rule, with nothing added:

- **[F] Ratio as slip.** Adjacent layers misalign by the fractional part of the
  running count. A spoke a/b re-opens every *b* layers, exactly when *b* divides
  the layer index. At the seam the slip is zero and layers stack in straight
  columns; at the half-turn the slip is one half and the stack forms bricks.
- **[F] The multiplexer reading.** Placing *n* on layer *m* computes *n* mod *m*
  spatially: each lap is a complete residue system, and the frame length equals
  the lap index, so frame growth *is* the enumeration of moduli. No division is
  performed anywhere; the slot spacing is the operation. (Caveat recorded in
  PAPER.md §8: on even laps the origin sits a half-turn off, since
  T(m−1) ≡ m/2 mod m; "slot" means steps since the lap's own origin.)

## 2. The classical layer — what was already known, made visible

- **[E] Channel capacity is two.** Tick *k* of layer *m* lies on spoke a/b with
  g = gcd(k,m), a = k/g, b = m/g, and its number is x = g(gb² − b + 2a)/2. For
  g ≥ 3 the visit number divides its occupant (g odd → g|x; g even → (g/2)|x
  with cofactor > 1). Every spoke carries at most two primes: its first visit,
  and its second visit when b is odd. Proven; verified for every visit to layer
  5000. The divisibility is noted in Math::PlanePath's GcdRationals
  documentation (after Fortnow 2004); the two-prime and φ(m) corollaries we have
  not found stated.
- **[E] Seats.** Every layer m ≥ 3 offers exactly φ(m) ticks where a prime can
  sit (gcd(k,m) = 1), checked to layer 800.
- **[E] The parity axis.** T(m−1) and ⌊m/2⌋ share parity (triangular numbers run
  odd, odd, even, even), so evenness is pinned to the half-turn axis. The
  half-turn spoke holds 2, 8, 18, 32, 50. Checked to layer 5000.
- **[E, classical] The layer balance.** Unit arrows at the fresh ticks sum to
  μ(m) — the fresh ticks are the primitive m-th roots of unity — and the running
  total is the Mertens function M(n), tied to RH by M(n) = O(n^(1/2+ε)).
- **[E, known] Junction lanes.** The opening tick T(m−1)+1 is the lazy caterer
  number; 8(T(m−1)+1) = (2m−1)² + 7, so an odd prime p divides a lane number
  only when −7 is a square mod p. Through layer 100,000 the lane holds 9,863
  primes vs the Bateman–Horn prediction 9,836 (OEIS A055469).
- **[E, checked] The wall (PAPER.md §7).** A knockout test hides each layer's
  primes and asks which smaller wheels recover them: about half the wheels below
  the square root, the same share as for any interval of that length. The wheel
  shows the sieve's boundary clearly. It does not move it.

## 3. The reframe — the stagger is the primary object

Sylvan's framing, now the project's: **the wheel's primary object is not the
primes. It is the stagger of the number line as the wheel grows relative to all
prior layers. Primes fall out of reading the stagger.**

- **[S] The stagger field.** For prime p, its shadow on lap *m* lands at tick
  k ≡ o_p(m) = −T(m−1) (mod p). The stagger field at step *m* is the tuple
  {o_p(m)} over all prior primes.
- **[F] The whole number line's stagger at step m is the single counter m, read
  in every prime modulus at once.** Each prime reads a different base-p digit of
  the one counter. The field's lap-to-lap shift is o_p(m+1) − o_p(m) = −m (mod p).
- **[E] Parabolic confinement.** Each o_p(m) is periodic in m with exact period
  p (period 4 for p = 2) and visits exactly (p+1)/2 of p phases — the triangular
  numbers mod p. Each arc sweeps a discrete palindromic parabola across laps and
  is forever confined away from (p−1)/2 of its phases. Zero violations, p < 200.
- **[F] Exact aperiodicity.** The joint field over the first r primes recurs
  with period lcm(2…p_r) ≈ e^{p_r}: the first 25 primes give ~10³⁶ laps.
  Aperiodicity is proved, not observed.
- **[E] Stagger-determinism (the platonic map).** Computing the arc cover from
  {o_p(m)} alone — no values, no arithmetic on values — reproduces the actual
  first-prime offset of every lap m = 4…5000 (4,997 laps, 0 mismatches;
  re-validated 400/400 at m ≤ 2·10⁴ and 4,997/4,997 against the shadow map with
  the exact witness rule). The first-prime function is a pure function of the
  stagger configuration. The wheel contains the complete answer to prime
  placement in uncompressed form.
- **[F] The movie, not the frame.** Within a lap, shadows arrange freely (no
  k-direction constraint; covers can pile up). Across laps, orbits are confined
  parabolas. Any wheel-native proof must be a **law on stagger orbits**, not a
  per-lap covering constraint.
- **[E] The exact composite-ness rule.** Tick *k* on lap *m* is shut iff ∃ prime
  p ≤ √(T(m−1)+k) with k ≡ −T(m−1) (mod p). Arcs from p > √v never witness
  compositeness. The √T(m) sieve limit is the exact witness bound. With the
  per-lap limit restored, the stagger model IS exact primality (63/63 laps,
  model W == nextprime(T(m−1)) − T(m−1)). Two sessions of probes got this limit
  right; the one probe that dropped it watched the model eat the primes it was
  supposed to locate. The limit is load-bearing, demonstrated from both sides.
- **[E] Zero internal field correlation (the CRT lock, N1).** The joint orbit
  over a finite prime set is the full Cartesian product of the individual
  triangular images with multiplicity, by the Chinese remainder theorem —
  verified exactly on (5,7), (3,5,7), (5,11). The stagger field has **no**
  internal correlations to exploit. Its entire law is the single quadratic
  counter s(m) = −T(m−1). The wall is located to one point: one quadratic walk
  interacting with the compositeness of the values it walks over.

## 4. The exact-theorem cluster — the wheel's own certificates

- **[F] B1 — the visible set is exactly the primes.** Tick *k* at layer *m* is
  covered iff N = T(m−1)+k is divisible by some prime p ≤ m. Any composite
  N ≤ T(m) has a factor ≤ √N ≤ √(T(m)) < m. Therefore uncovered ⟹ N is
  m-rough ⟹ N is prime. The wheel at layer *m* is the √N sieve rendered as
  occlusion; each layer certifies primality of numbers up to ~m²/2 using
  witnesses ≤ m, with no value-side act needed within the lap. Audited on laps
  2…2000 (149,001 uncovered ticks): zero non-primes uncovered, zero primes
  covered except the trivial self-cover of p ≤ m. Sylvan: "it IS a physical
  geometric sieve" — confirmed.
- **[F] B2 — the column law.** A prime N = T(m−1)+k can occur only if
  gcd(k,m) = 1, or gcd = 2 with m ≡ 2 (mod 4) (the parity escape). Audited
  m = 2…3000: 100% of 316,048 primes in eligible columns, zero violations.
  Eligibility is a free gcd certificate, forever. Every rational pole is
  composite at all depths beyond its innermost point with no occlusion needed;
  "the 2-prime rows bottom" is exact algebra.
- **[F] B3 — the triangular-offset theorem.** A dot recurs every layer with a
  closed-form factorization iff its offset is triangular: N = T(m−1) + m − c
  factors as (m−j)(m+j+1)/2 exactly when c = T(j). Audited m = 20…1500: all
  five triangular offsets are pure-dead with zero exceptions; every
  non-triangular offset tested carries primes. The predictable positions are
  the dead ones, and their addresses are the triangular numbers.
- **[F] B4 — forced-composite endpoints.** T(m) is composite for all m ≥ 3 and
  T(m)−1 for all m ≥ 4: the lap's last two ticks are arithmetically forbidden
  primes. Identities, not geometry.
- **[E] B5 — the m ≡ 2 (mod 4) theorem.** Seat-primes are identically zero on
  these laps; all primes sit on non-seat (non-coprime) ticks. The seat test is
  misaligned from value-divisibility by exactly m/2.
- **[E] B6 — the parity escape.** The eligible even-k ticks on m ≡ 2 (mod 4)
  laps carry exactly 2.00× the prime density of coprime columns (0.1734 vs
  0.0866, laps 3…3000). Mechanism: pure parity filter.
- **[E] C4 (relocation anti-correlation).** Followed every prime to the next
  layer's same angular column: 0.1413 vs 0.2289 random expectation. The prime
  does NOT follow its column. What is predictable is where the shadows will be;
  the primes are the negative space of a predictable moiré. Mechanism open,
  descriptive only.

## 5. The measured statistics — what the field does at scale

- **[E] The width–strikers invariant.** Mouth width W (the initial run of shut
  ticks at a lap's left edge) tracks the number of distinct outside primes
  jointly holding it: spearman(W, mouth_distinct) = 0.995 at m ~ 10⁴,
  0.981–0.992 at m ~ 2.6·10⁸. Scale-stable across eight orders of magnitude.
  The distribution *shape* is not scale-invariant; this identity is.
- **[E] All aggregate value-side statistics tested are iid-indistinguishable.**
  Quad-counter vs iid-lap nulls: mouth marginals (KS gap 0.060), lagged
  fingerprints (P10, P11 — the pre-registered ring-2 parity hint failed
  replication and is closed). The law that drives everything is invisible in
  every aggregate W-statistic. **[F] Reason (P12):** with the sieve limit
  restored, the stagger model is exact primality, so every aggregate value-side
  statistic of the real wheel is ordinary prime-gap statistics. The wheel's
  lawful geometry lives on the pattern side only.
- **[E] The clash factor (Obi's bet).** Layer counts sit a fixed ~11% above
  the independent-rings guess ∏(1−1/p), converging to e^γ/2 = 0.89054 from
  above (0.89092 at 1e5, 0.89064 at 1e6, 0.89060 at 1.8M layers; numbers to
  1.62e12). Mechanism: rings p, q clash every pq ticks; the independent guess
  books phantom clashes at distances longer than the number line, and dropping
  them is the haircut. **Pre-registered replication (PHASE7):** nine frozen
  predictions scored 8/9 on a cross-machine run; the one miss (sparsest-layer
  count 36,720 vs 35,300±700) is upward — layer counts are more uniform than
  an iid-style tail model allows. Full scorecard: `lab/PHASE7_prereg_scorecard.md`.
- **[E] U(m)/m tracks Mertens.** The realized arcs thin each lap ~4% more than
  independent sieve (median ratio 0.961 against e^-γ/ln m), with large per-lap
  fluctuations. The quadratic alignment is sieve-equivalent in aggregate,
  lap-specific in detail.
- **[E] The record layer.** Layer m = 264,800,157: first prime 766 ticks above
  the floor (ifirst_off = 767), trailing shut-run 15 — the record's right edge
  is nearly shut too. Anatomy: small outside primes (2…331) shadow 766 ticks
  down to 57 holes; all 57 holes composite with both factors > 766. 100% of the
  cover is from outside primes; routed primes contribute nothing. The record
  mouth is a generic-sieve pile-up, fully explained by striker count.

## 6. Honest negatives — closed routes, load-bearing, do not reopen blind

1. **[E] Orbit correlations: none exist** (CRT, exact factorization, N1).
2. **[E] Hole co-factor structure: nothing wheel-native** — holes are exactly
   W-rough numbers; the 74% semiprime fraction is the Mertens rough-density
   prediction, matched per-W-bucket.
3. **[E] Mirror compensation: dead at both scales** (r = −0.07 at 10⁴, +0.02 at
   2.6·10⁸). The seat palindrome does not propagate to value-side mouth geometry.
4. **[E] The per-arc thinning law: refuted by test** (N8) — the parabolic image
   selects which phases an arc visits, but its landing distribution over [1,p]
   is ~uniform.
5. **[E] Lagged fingerprints of the counter: null** (P10, P11 closed).
6. **[E] C4 anti-follow (0.62×): mechanism open, descriptive only.**
7. **[E] Strip enrichment: 1.09× lean, real but small** — the strips' visual
   dominance is candidate density, not prime concentration. Strip hearts (the
   exact poles) are 100% dead.
8. **[E] Census axis: closed by MATCH** — certified bands match
   Hardy–Littlewood/Cramér (−0.25σ, −1.16σ; max gap 274 vs the 540 record below
   10¹²). The wheel natively counts a one-witness hardness class (N = pᵃ·q,
   p ≤ bound < q) that classical π₂ undercounts by ~92×; the exact Lehmer
   enumeration reproduces a dumped band's count to 0.000σ.
9. **[E] ω-map spatial structure: NULL** vs honest nulls (the naive iid null is
   decisively rejected — small-prime determinism lives in the base, not the
   null).
10. **[E] Retained ring-phase structure: NULL** across 16 layers vs
    alignment-matched nulls. A lag-0 excursion was root-caused as
    sieve-lattice self-alignment (fixed layer spacing shares small factors) —
    standing lesson: periodically-spaced samples need alignment-matched nulls.

**Consequence:** "a massive wheel reveals new statistics" is dead by
measurement. All three statistics axes are measured-closed.

## 7. The held claims

- **[S] C1 — the halves-claim.** From m = 21 up, every lap has ≥ 1 interval
  prime strictly each side of the midpoint. Verified with zero violations over
  999,980 laps (m = 21…1,000,000, N to ~5×10¹¹, MR cross-validated); plus the
  record layer and height families. Margins: med 15/16, max 300/299, lap-level
  correlation 0.011. Worst-margin trend: log(max W) vs log(ln N) has slope
  2.19 ± 0.08 — the claim gets *safer* with scale (beyond 10⁴ laps the nearest
  prime stays ≥ 0.99·H from the midpoint). **[F] The proof door closes by
  reduction (PHASE4b):** B1 says the wheel IS the √N sieve, so C1 ⟺ "∃ prime in
  [T(m−1)+1, T(m−1)+⌊m/2⌋]" — an interval of length ≈ 0.7√N at height
  N ≈ m²/2, about 3× shorter than Legendre's conjecture at comparable height.
  A wheel-native proof is impossible in principle; "zero structural support" is
  now explained, not just observed (free rings can cover either half of every
  layer 21–60; the width bound never obstructs a half-cover anywhere in the
  A048670 range). Status: **[S, Legendre-hard by reduction, empirically
  bulletproof to 1M laps]**. Paper value migrates from the claim to the
  instrument (the wedge, §10).
- **[S] C2 — no-empty-layer** (the parent conjecture, OEIS A066888: every lap
  holds a prime). Directly verified to layer 10⁹ (3.13 billion Miller–Rabin
  tests, exact below 3.3·10²⁴), extended through exhaustive prime-gap data to
  layer 2,828,427,124. Structure-supported to layer 57 (confined rings; free
  rings wipe every layer 41–391, so structure alone proves a prime only to 57),
  walk-protected beyond. Baker–Harman–Pintz (x^0.525) covers all sufficiently
  large layers non-effectively; the open residue is finite but unreachable.
  Worst known bottom margin: 766 ticks at layer 264,800,157.

## 8. The ratio-dial era — the variable tread

The canonical wheel scales 1:1 (lap *m* brings *m* ticks). The variable tread
(variable.html) sets lap length to L(m) = max(1, round(m·r)) for any ratio r —
numbers keep their order, only the lattice reflows. What survives, what doesn't,
and what new laws appear:

- **[E] L1 — no all-prime line exists anywhere in ratio space.** 165 ratios ×
  ~1400 families ≈ 230k family scans: zero families with ≥ 8 samples 100%
  prime. At rational r the obstruction is exact (N(m) is a quadratic
  quasi-polynomial; a nonconstant such sequence takes composite values).
- **[E] L2 — rational ⟺ has dead lines.** Pure-dead families at every rational
  a/b tested (always including rim families), at zero irrationals. r = 1's
  triangular offsets are one instance; every rational has its own. The exact
  indexing formula for dead offsets at general a/b was the D8 question, closed
  in §9.
- **[E] L3 — the parity escape is universal at exactly 2.00×.** At every ratio,
  the (m mod 4 × k-parity) classes where N is forced odd carry exactly 2.00×
  prime density; forced-even classes are prime-deserts. An apparent "diluted
  escape" at non-1:1 ratios was an aliasing artifact: re-scanning at resolution
  m mod 4b shows every rational has the same pure lock as 1:1 — deadness of an
  odd-k tick is decided purely by B[m] mod 2, periodic with period dividing
  ~4b. The 1:1 wheel is not special; it is just legible.
- **[F+E] L4 — seam laws.** Integer r: base(m) = r·T(m−1) exactly, seam
  composite ∀m ≥ 3. Non-exceptional rationals: seam prime-normal ~7%.
- **[F] D5 — the clean-lap law.** A lap closes clean (starts at the seam or a
  half-turn from it) with fraction exactly 1/b at reduced a/b; the lap-start
  leftover hops among finitely many phases — the partial lock is periodic,
  never chaotic.
- **[E] D7 — r = 2 is the Ulam spiral, verified exactly.** Squares sit at frac
  1/2; Euler's n²−n+41 is the fixed tick k = 41 and breaks at m = 41 exactly as
  the theorem says; Ulam's prime-rich diagonals are constant seam offsets
  k = 2m + c converging on the square ray.
- **[E] The census — 9,216 integer-ratio offset forms + 176 seam classes.**
  Dead ⟺ square discriminant, past the unit boundary (0/9,216 square-D forms
  contain a prime; the 41/176 square-D seam classes showing 1–2 primes are
  unit-factor leaks at t = 0…1 only). Euler is champion but not unique:
  N = 3m²−3m+23 (D = −267, h = 2) has streak 19 and density 0.430.
  Heegner reachability is ratio-gated: all twelve class-number-1 |D| occur
  somewhere in range, but the champions −43, −67, −163 occur at fixed offsets
  ONLY at a = 2 — 2:1 is the complete Heegner host. Where the wheel's algebra
  is strongest (the seam), survival is marginal.
- **[E] G5 closed — the irrational substrate is Sturmian.** At r = √2, φ, π, e
  the lap word has factor complexity p(n) = n+1 through n = 12; rational
  controls saturate as theory demands. The sieve still holds at irrational
  ratios (zero gold ticks violate the forced residue exclusions), and beyond the
  sieve: nothing detectable (χ² ordinary, lag-1 autocorrelation ≤ 2.3σ,
  sign-inconsistent). Ordered floor, sieve furniture, no deed to the land.
- **[E] The GPU frontier.** The roll engine (one ring per GPU lane, closed-form
  jump seeding, stamp kernel with reciprocal-estimate first-stamp indexing) runs
  ~33M certified numbers/s at layer 6·10⁹, ~100M/s at 282M; verified exactly
  against CPU span sieves and deterministic MR (6,002/6,002 primes, 1,952/1,952
  composites at a layer-6e9 dump-band, N ~ 1.8·10¹⁹). Bottleneck story, three
  times corrected: bandwidth → issue-rate → **critical-path serialization** —
  one thread per ring, and the p = 2 thread walks the full window in W/2
  sequential iterations. A window-parallel kernel prototype (Phase 0.6) is
  bit-exact vs production and recovers ~95.6% of kernel time (18.2 → 0.77 ms/layer
  under live-window co-tenancy, 24×); integration into the production engine is
  queued as a user decision.
- **[F, certified exact] The witness layer.** stamp_kernel atomicAdds a
  per-tick ω_small(N) alongside the bool: every certified tick carries its
  small-prime witness count. Semantics certified deterministically: the exact
  Lehmer enumeration of the one-witness class N = pᵃ·q (p ≤ bound < q) or prime
  power reproduces a dumped band's count exactly (165,861 = 165,861, 0.000σ).
  The first audit caught a duplicated prime 2 in every prime-table cache —
  counts exposed instantly what the boolean engine was blind to.

## 9. The deadness engine — one engine behind every dead line

Three layers, in order of consultation:

1. **Content (Layer 1).** Within a constant-L block the seam values are an
   arithmetic progression with difference L; if gcd(first, L) > 1 the whole
   block is composite. Universal, exact, sieve-free.
2. **Quasi-polynomial factorization (Layer 2).** On each residue class
   m = R·t + r (R = 2b·2^ν), the seam N(t) is an exact quadratic in t. If the
   discriminant is a perfect square, N factors over ℚ and the class is
   identically composite. Exhibit, 3:8, m = 16t+2: N = 48t² + 16t + 1 =
   (4t+1)(12t+1). 3:8 has all 16 classes factorable — fully dead by algebra
   alone. Euler's n²−n+41 is a NON-factorable quadratic (D = −163) living on a
   live class at 2:1.
3. **The sieve (Layer 3)** — only after layers 1–2 pass does arithmetic get
   consulted.

**[F→E] D8 — the closed form (PHASE5).** Writing L[m] = (a·m + c(m))/b with
c(j) periodic mod b, the r²-terms of B² and 4AC in Δ(r) = B² − 4AC cancel
identically for every coprime (a,b): the seam discriminant is a quasi-polynomial
of polynomial degree ≤ 1, period b (pairing law proved: P = 0 iff b odd, P = b/2
iff b even; 0 violations over coprime b ≤ 12, a ≤ 15). Consequence: r ranges
over a residue system mod b, so y² = Δ(r) is a finite union of b exact square
tests — no Pell, no elliptic curve; the expected genus obstruction never
materializes. **Dead classes = {r mod b : Δ(r) square} ∪ {content-killed
classes}, computable in O(b) exact arithmetic with no sieve.** All landmarks
pass (3:8 fully dead; 5:8 half/half; 7:4 content-dead; b = 4 ⟺ a ≡ ±1 mod 8),
and the formula predicted and confirmed 9 dead pairs not on the published seam
map (3:2, 5:2, 7:2, 8:3, 8:5, 9:2, 9:5, 10:3, 11:2) — the map is extended.
Residual openness, stated honestly: (a,b)-parameterized compression of the
square tests (the sum is Dedekind-sum-like; no simpler form known) and Layer-1
one-sidedness (content-1 ≠ live; the sieve owns that territory).

**Unification:** this one engine sits behind L2's dead lines, the seam map, and
the Ulam connection. The dead/live boundary everywhere is: **square
discriminant (factors identically) vs not (can be prime).**

## 10. The quadratic rhyme probe (PHASE6, 2026-10-10) — checked and closed

A March 2026 study (three independent Claude instances) had found a spectral
universality across self-similar graphs: the Menger sponge's Laplacian carries
the factor x² − (d+2)x + 2 with multiplicity locked to dimension d, irrational
spectrum since (d+2)² − 8 is not a square. Both sides of the lab had
square-discriminant classifiers — the wheel's deadness engine and the fractal's
spectral lock — and the question was whether the rhyme is a corridor.

- **[E] The universality, extended into new territory.** Re-derived all three
  doc cases exactly (characteristic-polynomial factorization over ℚ). Menger
  d = 4 (new): predicted factor x² − 6x + 2, roots 3 ± √7, multiplicity
  exactly 4 — the conjecture now has d = 2, 3, 4. Carpet level 2 (new): the
  factor persists at multiplicity 2. Vicsek d = 3 (new): all-integer spectrum
  (the K₁,₈ star). **Proof upgrade:** D(d) = (d+2)² − 8 is a perfect square
  only at d = 1 (factor-pair argument, two lines; exhaustively checked d ≤
  2000) — irrationality of the spectral roots is proved universal for
  remove-center d ≥ 2. It remains a conjecture that the factor appears at
  multiplicity d in general.
- **[E] Surprise rule, against the doc itself:** the doc's "spectrum symmetric
  about S/2" claim is false as a multiset statement at Menger level 1 (mult(2)
  = 5 vs mult(3) = 1, exact). Carpet L1 is exactly symmetric; sponge L1 only
  partially. Logged as a doc correction, alongside two smaller ones (the
  P²·S = cell-count encoding works only at d = 3; the universality is
  contact-convention-dependent — Vicsek pieces touch at points, and the
  junction graph is the right object, not face contact).
- **[F→E, closed] The corridor verdict: wallpaper, closed by sign.** All 271
  wheel seam quadratics sampled have non-negative coefficients (C = 0 in 16
  classes, never negative) — a counter polynomial with non-negative
  coefficients has no strictly positive root. The fractal spectral factor has
  both roots strictly positive. The two polynomial families are provably
  disjoint: no wheel class polynomial can *be* the fractal factor. The shared
  classifier — perfect-square discriminant of an integer quadratic ⟺ ℚ-
  factorability — is the quadratic formula, genus 0, ancient. **Analogy, not
  identity.** Labeled as such.
- **[E] The result that survives on its own — the dead/live boundary is
  sawtooth-carried.** Strip the sawtooth (the periodic rounding corrections
  c(j), a Dedekind-sum-like object) out of Δ(r) and keep only the ratio-side
  ramp: it agrees with the true dead/live classification on 135/271 classes —
  49.8%, a coin flip. The sawtooth flips the other half; 47 of 57 ratios change
  their dead-class set entirely. The all-dead a = 1 row is invisible to ratio
  geometry (the ramp predicts almost nothing dead; truth says everything dead).
  The ratio sets the scale; the wheels write the law. And the sawtooth is the
  same object PHASE5 pinned as D8's true obstruction — one object, two roles.

## 11. The standing wall, precisely located

**[G] The routing wall.** The stagger field determines everything
(stagger-determinism), but the only known reading is the uncompressed O(m)
simulation. No compressed wheel-native law of the field is known. The within-lap
instance is closed by B1 (the wheel IS the sieve); the mouth/window instance at
W ≪ m stands. The wall's true name, from the roll-engine analysis: holding every
prime up to √N is the information price of an exact certificate — any
deterministic exact sieve must pay it. The doors past it are different
mechanisms, not optimizations: probabilistic certificates (Miller–Rabin) and
structure (decoding the stagger field).

**[G→ measurable] The wedge (F2).** Free rings wipe every layer 41–391; the
realized turning never does. The realized turning is not a random point in
turning-space — it is one quadratic curve (the stagger law, proved). So the
parent conjecture reads: *the quadratic curve never enters the wipe set.* The
wipe set is characterized; the curve is characterized; the per-lap distance
between them has never been measured. That distance is the conjecture's true
object. One-flip wipe distance: every realized turning in scope is ≥ 2 moves
from every wipe turning (consistency, entailed by the verified conjecture to
layer 2.8B). The true Hamming-distance instrument (J1c) needs SAT/anneal
machinery — jointly queued with the second lab session.

## 12. The method — what this project is besides its theorems

The wheel project runs **mechanism-first theoretical science** as an operating
procedure, and the procedure itself is a deliverable:

1. **Epistemic labels on every claim** ([S]/[F]/[G]/[E]), with the rule that
   [F] must actually follow — a gap left honestly open beats an elegant theorem
   pasted over the wrong mechanism.
2. **Predictions pre-registered before checks**, with binding stop conditions
   (the AUTONOMY chain of 2026-10-10 ran seven phases on this rule; its most
   spectacular deviation, +3,869σ, was root-caused as a prediction-specification
   error, not a discovery — huge σ-deviations are more often spec errors than
   physics).
3. **Honest negatives as load-bearing closures.** Ten closed routes (§6) are
   kept in writing with their refutations; the territory map (INSIGHTS.md
   2026-10-09 dusk) organizes every standing claim so closed routes cannot be
   reopened blind.
4. **Instrument before theorem.** The wedge distance, the witness layer, the
   ratio dial, the GPU frontier: where a claim cannot be proved, the project
   builds the instrument that would measure it.
5. **Corrections published in place.** The bandwidth-wall claim, the thinning
   law, the "semiprime channel," the 2.000 parity lift, the fractal symmetry
   claim — five superseded readings, each retracted in the same document that
   carried it, each retraction load-bearing.

Two falsified priors produced standing method lessons: huge σ-deviations are
more often specification errors than discoveries; and when a "hard problem"
smells like Diophantine genus, first check whether the variable is free or
periodic — periodicity trivializes curves.

## 13. Open problems (the standing queue)

- **[G] F2/J1c** — the wedge distance: per-lap Hamming distance from the
  realized stagger point to the nearest wipe turning. The conjecture's true
  object; needs SAT/anneal machinery.
- **[S] C1** — halves-claim: machine-checkable instance of a sub-Legendre
  short-interval conjecture; zero violations to 1M laps; proof out of reach by
  reduction.
- **[G] D8 residuals** — (a,b)-parameterized compression of the square tests;
  Layer-1 one-sidedness.
- **[G] F3** — the transformer-bridge connector: what, if anything, plays
  residue-class periodicity in a real network's address system? A system with
  residue-class-like addresses should show Mertens-shaped decay of its
  surprise rate. Left open, not renamed.
- **[G] G-queue survivors** — Ulam-diagonal overlay instrument; Farey walk
  movie; prime-rich quadratic hunt at other integer ratios (mechanism now
  known: enumerate non-factorable classes, rank by yield); C4 anti-correlation
  mechanism; calm-slope derivation pre-registered from gear-rule luck shares.
- **[user decision]** Phase 0.6 kernel-v2 integration into the production GPU
  engine (bit-exact prototype verified 24×; engine surgery is Sylvan's call).

## 14. Relation to existing work (deep sweep, 2026-10-10)

Full ledger: `lab/LITERATURE_SWEEP_2026-10-10.md` (four search agents, ~40 query
rounds). Verdicts, compressed:

**What is classical and now cited, not claimed.** The lane test and the column
density constant C(k) are exactly the Hardy–Littlewood Conjecture F singular
series for the quadratic m²−m+2k (D = 1−8k, ω(p) = 1+(D|p)): Hardy &
Littlewood 1923, Bateman & Horn 1962, written verbatim in
Zomlefer–Garcia–Fukshansky 2020. The "dead class ⟺ square discriminant"
criterion is reducibility over ℚ — textbook (Boston & Greenwood 1995). The
wheel's [F] derivations were never claimed as new theorems and stand unchanged.

**What the sweep did not find, anywhere indexed.** The triangular-tick wheel
enumeration with visibility rules; the two-prime channels / φ(m) seats theorem;
the dead-class taxonomy applied as an organized classification of a ratio
family; and the column engine as an assembly (solve-once + hop, one byte per
layer, no ring list, deterministic-MR certified at 20 digits). Components are
standard (the hop is the quadratic sieve's inner loop — Pomerance 1996); the
assembly appears unpublished. Caveat: web-scale sweep, not a MathSciNet
full-text scan; one more pass is owed before any external submission.

**A collision worth noting.** The Rabinowitsch criterion (1913; class number
one settled by Heegner 1952 / Baker 1966 / Stark 1967) governs column
discriminants D = 1−8k = 1−4A with A = 2k. Among integer start-columns the
only class-number-one hit is k=1 (D=−7, checked arithmetically: of the six
Heegner discriminants, only −7 ≡ 1 mod 8). The prime-richness ranking of
columns (richest.py) is a k-parametrized instance of the Jacobson–Williams
2003 extremal-density program. Both connections are formal homes, labeled as
such — they deepen the columns; they do not touch the wheel theorems.

**Naming.** "Prime tread wheel" carries no indexed collision; "wheel sieve"
alone is taken (Pritchard 1981) and is never used here.

## Reproduce

```
cd probes && python3 verify.py    # every number in PAPER.md, ~10 s
cd lab  && python3 PHASE5_d8.py   # the D8 closed form, landmarks + 9 predicted dead pairs
cd lab  && python3 PHASE6_quadratic_rhyme.py  # the quadratic rhyme probe (fractal side + wheel side)
```

Probe-by-probe reproduce commands: `probes/README.md`. Full dated ledger:
`INSIGHTS.md`. Pre-registered chain plan and rulings: `AUTONOMY_2026-10-10.md`.
Session-state map: `HANDOFF.md`.

## Instruments (live pages)

| Page | What it is |
| --- | --- |
| wheel.html | The 1:1 canonical wheel — scrub laps, watch the sieve occlude |
| variable.html | The ratio dial — lap length scaled by any ratio |
| globe.html | The §2/§8 multiplexer — channels opening and closing over a frame |
| living-prime-map.html | The roll engine — jump to any layer and draw it from rings |
| problem-wheels.html | Collatz, Goldbach, twins, prime races on wheels |
| field-notes.html / night-shift.html | The articles: the stagger field; the witness layer and the night's closures |

## References

1. [Floyd's triangle](https://en.wikipedia.org/wiki/Floyd%27s_triangle), Wikipedia.
2. [Math::PlanePath::GcdRationals](https://manpages.debian.org/testing/libmath-planepath-perl/Math::PlanePath::GcdRationals.3pm), after L. Fortnow, "Counting rationals quickly" (2004).
3. [OEIS A066888](https://oeis.org/A066888) — primes between consecutive triangular numbers (J. W. Nicholson, 2011).
4. [OEIS A055469](https://oeis.org/A055469) — primes of the form k(k+1)/2 + 1.
5. [OEIS A048670](https://oeis.org/A048670) — Jacobsthal function values (the capacity table).
6. T. Kotnik and J. van de Lune, [On the order of the Mertens function](https://emis.univie.ac.at/journals/EM/expmath/volumes/13/13.4/Kotnik.pdf), Experimental Mathematics 13 (2004).
7. R. Baker, G. Harman, J. Pintz, *The difference between consecutive primes, II*, Proc. London Math. Soc. 83 (2001) — the x^0.525 short-interval result.
8. T. Oliveira e Silva, S. Herzog, S. Pardi, *Empirical verification of the even Goldbach conjecture and computation of prime gaps up to 4·10¹⁸*, Math. Comp. 83 (2014).
9. M. Visser, [Sierpiński's Hypothesis H1](https://arxiv.org/html/2512.22413v1) (2025).
10. [Lehmer sieve](https://en.wikipedia.org/wiki/Lehmer_sieve), Wikipedia.
11. G. H. Hardy & J. E. Littlewood, *Partitio Numerorum III*, Acta Math. 44 (1923) — Conjecture F and its singular series.
12. P. T. Bateman & R. A. Horn, *A heuristic asymptotic formula concerning the distribution of prime numbers*, Math. Comp. 16 (1962), 363–367.
13. D. Zomlefer, S. Garcia, L. Fukshansky, *The Bateman–Horn conjecture: heuristic, history, and applications*, Expo. Math. 38 (2020) — the lane test in print.
14. M. Jacobson Jr. & H. C. Williams, *New quadratic polynomials with high densities of prime values*, Math. Comp. 72 (2003), 499–519 — the richest-columns mechanism.
15. G. W. Fung & H. C. Williams, *Quadratic polynomials which have a high density of prime values*, Math. Comp. 55 (1990), 345–353.
16. G. Rabinowitsch, *Eindeutigkeit der Zerlegung in Primzahlfaktoren in quadratischen Zahlkörpern*, J. Reine Angew. Math. 142 (1913) — the class-number criterion for column discriminants.
17. H. Iwaniec, *Almost-primes represented by quadratic polynomials*, Invent. Math. 47 (1978), 171–188 — strongest rigorous anchor for quadratic prime values.
18. K. Ford & R. Gabdullin, *Prime avoidance of polynomial values* (arXiv:2310.20449, 2023) — rigorous prime deserts.
19. A. O. L. Atkin & D. J. Bernstein, *Prime sieves using binary quadratic forms*, Math. Comp. 73 (2004), 1023–1030 — nearest published quadratic-congruence sieve.
20. P. Pritchard, *A sublinear additive sieve for finding prime numbers*, CACM 24 (1981), 18–23 — the wheel-sieve lineage and the naming collision.

---

*Text: CC BY 4.0. Code: MIT. The notebook never deletes; it only labels.*
