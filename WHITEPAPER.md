# The Prime Tread Wheel — White Paper

**Counting numbers on a wheel that grows by one tick per layer, and what the stagger of that growth knows about the primes.**

Obi (Sylvan Gaskin), with Claude, Argon (Gemini), Kimi, GPT, and GLM. 2026-10-10; updated through
2026-11-15 (§16.3/§18.9–§18.10: the CBB solver-free certification era —
bracket [42, 45] both ends solver-free, LB 42 unconditional via §18.9
Thm 9 CBB hybrid t42 tree, 2026-10-27; LB 41 via Thm 8, 2026-10-26;
§16.8 Three-Primitive Theorem + independence witnesses and §18.11
2026-10-28 structural ledger: Fock/SU(2) multiplets, L4 lattice-ray
dissolution 5-for-5, §2b unpriced-vs-priced Φ reconciliation, C1/C2
windows, L3 ring-role audit; §18.9's d(1000)=37 deficit-leaf resolution (2026-10-28);
10-25 multi-agent handback fold:
native-schedule law refuted §13, §17.2 P4 hatch-plug closure, §19.2
inequality repair, nine verify_dual theorems, reproduce block completed;
2026-10-30 §18.12: the Erdős #7 certificate era — unit-capacity + max-forest
solver-free certificates, the 5M→1B fleet scan (3,355 survivors; every odd
L < 6,891,885 settled solver-free except 4,729,725), two independent cold
audits PASS, and the §18.12 debt-hunt harvest: ~1.05 B annealing moves × 8
seeds found no covering at 4,729,725 — min D certified band [118,108, 442,687],
a 3.2× plateau above the covering line (suggestive, not settling)).
Status pass 2026-11-14 (no change to the certified d(1500) bracket since 2026-10-27 — the Erdős #7 certificates continued through 2026-10-30, §18.12; campaign
endgame lives in the project handoff record — campaign compute exited 2026-11-11): §16.7
Item 4 below is dead (→§15.8/§16.6); §18.12 extension-probe status
noted in place.

Release-staging pass 2026-11-15: §14 independent-convergence block rewritten as an
exact credit demarcation — Tucker's archive credited item-by-item; the continuous
spiral, the guarantee-zone wedge, the solver-free dual-certificate stack, and the
Lean 4 formalization explicitly claimed as ours; dating facts unchanged; zero
certified mathematics touched.

Zenodo release deposit: DOI 10.5281/zenodo.24266492, PUBLISHED 2026-11-16.
Related-identifier link to the Tucker article record (22912558) is in the
deposit metadata; §14 carries the full itemized demarcation.

Correction pass 2026-11-16 (post-release, v1.0.1): the Erdős #7 comparison in §14 and
§18.12 is corrected in place by dated blocks; refs. 39–42 added; nothing deleted;
zero certified mathematics touched.

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
  and its second visit when b is odd. Proven; verified for every visit to
  layer 5000. The divisibility is noted in Math::PlanePath's GcdRationals
  documentation (after Fortnow 2004); the two-prime and φ(m) corollaries we have
  not found stated.
- **[F] Seats.** A prime can sit only on a coprime tick (gcd(k, m) = 1) — one
  line from the B2 eligibility law — so the generic lap offers exactly φ(m)
  candidate ticks (count verified to layer 800; the deeper invariants below run to 5000+). **Parity caveat (B5/B6):** on
  laps m ≡ 2 (mod 4), T(m−1) is odd and every coprime k is odd, so every
  seat value is even — no prime ever sits on a seat there; those laps' primes
  all sit on the even gcd = 2 ticks at 2.00× density. "φ(m) seats" is the
  generic-lap count; the parity-escape laps re-allocate them.
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
- **[F] Parabolic confinement.** Each o_p(m) = −T(m−1) (mod p) is periodic in m
  with exact period p (period 4 for p = 2), and for odd p visits exactly
  (p+1)/2 of p phases: T(m−1) = ((2m−1)² − 1)/8 is a quadratic image, which
  takes (p+1)/2 values mod p. Each arc sweeps a discrete palindromic parabola
  across laps and is forever confined away from (p−1)/2 of its phases. Proven
  in two lines; the former "zero violations, p < 200" is now a certificate,
  not the evidence.
- **[F] Exact aperiodicity.** The joint field over the first r primes recurs
  with period lcm(2…p_r) ≈ e^{θ(p_r)} (θ = Chebyshev's prime sum — e^{97} alone would give 10⁴²): the first 25 primes give ~10³⁶ laps.
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
  *Epistemic note 2026-11-14:* the factorization identity (offset
  triangular ⟹ closed-form factorization, hence dead past the innermost
  layer) is exact [F] — the classical T_a − T_b = (a−b)(a+b+1)/2 identity.
  The universal converse — *every* non-triangular offset carries a prime at
  every layer — is a quadratic prime-values claim of Landau type (cf.
  infinitely many n²+1 primes, open) and is NOT proved; the audited range
  m = 20…1500 stands as [E], not [F].
- **[F] B4 — forced-composite endpoints.** T(m) is composite for all m ≥ 3 and
  T(m)−1 for all m ≥ 4: the lap's last two ticks are arithmetically forbidden
  primes. Identities, not geometry.
- **[E] B5 — the m ≡ 2 (mod 4) theorem.** Seat-primes are identically zero on
  these laps; all primes sit on non-seat (non-coprime) ticks. The seat test is
  misaligned from value-divisibility by exactly m/2.
- **[E] B6 — the parity escape.** The eligible even-k ticks on m ≡ 2 (mod 4)
  laps carry exactly 2.00× the prime density of coprime columns (0.1734 vs
  0.0866, laps 3…3000). Mechanism: pure parity filter. *Reframe note
  2026-11-14:* the 2.00× is parity-conditioning arithmetic (escape columns
  are conditioned on odd N while the coprime base is half-dead by parity),
  not a discovered equilibrium — no prime-race literature can corroborate
  or conflict with it, since Dirichlet gives the races equal asymptotic
  density. The measured content is L3's cross-ratio universality.
- **[F] B7 — the mirror lift.** T(m−1) + T(m) = m², so the tick involution
  k ↔ m − k pairs values summing to exactly m²: the seat palindrome lifts to
  values as v ↔ m² − v. Eligibility is preserved exactly (gcd(k, m) =
  gcd(m − k, m), including the gcd = 2 parity escape), and the map is a
  bijection on ticks. Two measured closures fall out of the one identity.
  For odd m no mirror prime pair can exist — m² is odd, so one of v, m² − v
  is an even number ≥ 4 — and on even m a mirror pair is exactly a Goldbach
  representation of m² with both summands in the layer window: a rare
  coincidence, which is §6 item 3's mirror-compensation null in one line, while the
  exact bijection is why the seat palindrome stays perfect on the pattern side
  precisely where value-side compensation is dead. (Verified: zero odd-m
  pairs over m < 3000; 11,085 even-m pairs, every one summing to m².) The
  mirror probe was the wrong instrument for a per-lap law and the right one
  for the Goldbach window. *Formalization note 2026-11-14:* "bijection on
  ticks" is exact on cyclic ticks (the involution is a ZMod m bijection,
  kernel-certified) but loose on the linear set {1,…,m}, where k ↦ m − k
  sends m ↦ 0 (not a tick of layer m); the endpoint pairing works across
  layers (m² − T(m) = T(m−1)). The Lean development states each layer
  precisely; no theorem here changes, only the wording "bijection on ticks."
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
  replication and is closed as a hint (§15.4's phase-stratified residual carries no weight pending its own pre-registered replication). The law that drives everything is invisible in
  every aggregate W-statistic. **[F] Reason (P12):** with the sieve limit
  restored, the stagger model is exact primality, so every aggregate value-side
  statistic of the real wheel is ordinary prime-gap statistics. The wheel's
  lawful geometry lives on the pattern side only.
- **[E] The clash factor (Obi's bet).** Layer counts sit a fixed ~11% below
  the independent-rings guess ∏(1−1/p), converging down to e^γ/2 = 0.89054
  (0.89092 at 1e5, 0.89064 at 1e6, 0.89060 at 1.8M layers; numbers to
  1.62e12). Mechanism: rings p, q clash every pq ticks; the independent guess
  books phantom clashes at distances longer than the number line, and dropping
  them is the haircut. The classical identification: true survivor density is
  1/ln N ≈ 1/(2 ln m) (N ≈ m²/2), while the Mertens product over p ≤ m is
  e^(−γ)/ln m — their ratio is exactly e^γ/2. The clash mechanism is the
  wheel-native account of Mertens' third theorem: the identity is [E], the
  phantom-clash reading [S]. **Pre-registered replication (PHASE7):** nine frozen
  predictions scored 8/9 on a cross-machine run; the one miss (sparsest-layer
  count 36,720 vs 35,300±700) is upward — layer counts are more uniform than
  an iid-style tail model allows. Full scorecard: `lab/PHASE7_prereg_scorecard.md`.
- **[E] U(m)/m tracks Mertens.** The realized arcs thin each lap ~4% more than
  independent sieve (median ratio 0.961 against e^-γ/ln m), with large per-lap
  fluctuations. The quadratic alignment is sieve-equivalent in aggregate,
  lap-specific in detail.
- **[E] The record layer.** Layer m = 264,800,157: first prime 766 ticks above
  the floor (ifirst_off = 767), trailing shut-run 15 — the record's right edge
  is nearly shut too. Anatomy (field notes, the primary record): 109 outside
  strikers — arcs from primes above the seat threshold — redundantly hold the
  mouth shut (1.68× cover — ~1,287 arc landings across the 766 shut ticks; 270 of its 497 mouth seats carry exactly one arc).
  57 of the 766 shut ticks are holes: no striker arc lands on them, yet every
  one is composite with both factors > 766 — invisible to every prime ≤ 766,
  covered by inside primes in (766, m]. No B1 tension: B1's witness set is
  p ≤ m, and these ticks have their witnesses; the measured invariant is the
  striker count, not a prime range (width–strikers, above). The record mouth
  is a generic-sieve pile-up, fully explained by striker count.

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
5. **[E] Lagged fingerprints of the counter: null** (P10;
   P11 → record-repair saga, §15.4 — two frozen texts disagreed on the
   predicted sign; the honest phase-stratified null leaves a 2.2σ residual
   carrying no weight pending pre-registered replication).
6. **[E] C4 anti-follow (0.62×): mechanism open, descriptive only.**
7. **[E] Strip enrichment: 1.09× lean, real but small** — the strips' visual
   dominance is candidate density, not prime concentration. Strip hearts (the
   exact poles) are 100% dead.
8. **[E] Census axis: closed by MATCH** — certified bands match
   Hardy–Littlewood/Cramér (−0.25σ, −1.16σ; max gap 274 vs the 540 record below
   10¹²; the census band reaches N ≈ 4×10¹⁸). The wheel natively counts a one-witness hardness class (N = pᵃ·q,
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
  record layer and height families. Margins (ticks, lower/upper, m = 21…10⁶): med 15/16, max 300/299; lap-level
  correlation 0.011. Worst-margin trend: log(max margin) vs log(ln N) has slope
  2.19 ± 0.08 — the claim gets *safer* with scale (beyond 10⁴ laps the nearest
  prime stays ≥ 0.99·(mean gap H) from the midpoint). **[F] The proof door closes by
  reduction (PHASE4b):** B1 says the wheel IS the √N sieve, so C1 ⟺ "∃ prime in [T(m−1)+1, T(m−1)+⌊m/2⌋] and symmetrically in the upper half" — an interval of length ≈ 0.7√N at height
  N ≈ m²/2, about 3× shorter than Legendre's conjecture at comparable height.
  A wheel-native proof is impossible on the stagger-orbit thesis of §3 [S]; "zero structural support" is
  now explained, not just observed (free rings can cover either half of every
  layer 21–60; the width bound never obstructs a half-cover anywhere in the
  A048670 range). Status: **[S, Legendre-hard by reduction, empirically
  bulletproof to 1M laps]**. Paper value migrates from the claim to the
  instrument (the wedge, §10).
- **[S] C2 — no-empty-layer** (the parent conjecture, OEIS A066888: every lap
  holds a prime). Directly verified to layer 10⁹ (3.13 billion Miller–Rabin
  tests, exact below 3.3·10²⁴), extended through exhaustive prime-gap data to
  layer 2,828,427,124. Structure-supported to layer 57 (confined-ring search evidence — the confined-N1 record, INSIGHTS; free
  rings wipe every layer 42–391 — layer 41 is a dark row, in the
  infeasible set {2–18, 22–24, 26, 27, 40, 41}, so the wipeable range
  starts at 42 under the pinned seam convention (§15.6) — so structure
  alone proves a prime only to 57),
  walk-protected beyond. Baker–Harman–Pintz guarantees primes only in windows
  of length N^0.525 around N — wider than the layer width √(2N) for large N,
  so the promised prime can sit past the layer it was invoked to save: BHP
  settles no layer, even non-effectively, and the RH-class O(√N log N) bound
  fails the same width comparison. The verified residue is finite (layers ≤
  2,828,427,124 by the gap tables); the open residue is infinite. Cramér-grade
  gap heuristics imply the claim trivially — which is why the trend is visible
  and the proof isn't.
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
  N = 3m²−3m+23 (D = −267, h = 2) has streak 19 and density 0.430; the line
  exists only from m = 4 (the lap length must reach its constant 23), so the
  streak runs from line onset, not from m = 1.
  Heegner reachability is ratio-gated: twelve of the thirteen known
  class-number-one orders occur somewhere in range (nine fundamental Heegner
  discriminants plus four non-fundamental orders make thirteen; "twelve" is
  the census's reach, not a canonical count), but the champions −43, −67, −163 occur at fixed offsets
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
  bit-exact vs production and recovers ~95.6% of kernel time (18.2 → 0.77 ms/layer, ≈24×); integration into the production engine is
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
   m = R·t + r (R = 2b·2^ν, ν = ν₂(b) the 2-adic valuation), the seam N(t) is an exact quadratic in t. If the
   discriminant is a perfect square, N factors over ℚ and the class is
   identically composite. Exhibit, 3:8, m = 16t+2: N = 48t² + 16t + 1 =
   (4t+1)(12t+1). 3:8 has all 16 classes factorable — fully dead by algebra
   alone. Euler's n²−n+41 is a NON-factorable quadratic (D = −163) living on a
   live class at 2:1.
3. **The sieve (Layer 3)** — only after layers 1–2 pass does arithmetic get
   consulted.

**[F→E] D8 — the closed form (PHASE5).** Writing L[m] = (a·m + c(m))/b with
c(j) periodic mod b, the r²-terms of B² and 4AC in Δ(r) = B² − 4AC (the seam polynomial's discriminant; letters local to D8) cancel
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
  (the K₁,₈ star — convention-dependent; see the caveat below). **Proof upgrade:** D(d) = (d+2)² − 8 is a perfect square
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

**[G→ measurable] The wedge (F2).** Free rings wipe every layer 42–391 (41 is a dark row — §6); the
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
   law, the "semiprime channel," the "parity lift" reading of the 2.000 constant (the value stands, §8 L3), the fractal symmetry
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
  short-interval conjecture; [E] zero violations to 1M laps; [S] proof out of reach by
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

### Queue updates, 2026-10-13 (everything below is post-§13; full detail §15)

**Closed since this queue was written:** the 7/6 dial census (PHASE 14,
reproduced to the unit, Bateman–Horn pooled measured/predicted ratio 1.00098 — §15.2); the P11 verdict
(repaired, §15.4); convention standardization — the lab now pins the seam
as window (T(m−1), T(m)] and rings ≤ ⌊√T(m−1)⌋; the sparse MILP removed the
memory wall (m = 1000 matrix ≈ 2 MB).

**Still standing:** F2/J1c true Hamming instrument; C1; D8 residuals; F3;
G-queue survivors; GLM's C(X) truncation prereg; GPT's conditional
ring-2 split (d_home vs d_flip); Gemini's spacing-variance dump at the
three witness boundaries (primes 11, 97, 257 entering √T); the ω-map
~2σ clustering hint (parked, needs ≥100-window null ensemble).

**New, from the wedge era:**
- **[G] The dial theorem — sharpened 2026-10-13 (evidence swarm).** (The census task above is closed; the selection question it exposed remains open.) "7/6
  is the wheel's modal ratio" was naming, not a measured mode: the
  measured content is argmax of the live-family singular series C over
  the 20-ratio b ≤ 8 sweep (7/6 at 4.89, 5/4 at 4.50, all else ≤ 3.8)
  [E]. At finer resolution the argmax is NOT 7/6 — 14/11 reaches C ≈ 5.13
  at b = 11, and at b ≤ 60 ratios like 59/46 reach ≈ 6.64 — but max-C
  confounds denominator size with live-family count (lottery tickets).
  Arithmetically 7/6 is not unique: 5/4, 9/7, 6/5 share its full profile
  (h = 1 real-quadratic kernel, identically-odd families, bad-prime
  losses). The surplus mechanism is decomposed [S on measured inputs]:
  2-adic ×4 (b-even dial deletes ring 2 where 2 splits) + bad-prime root
  losses (at 7/6: with ρ(p) := number of kernel roots mod p: ρ(3)=0 ×1.5, ρ(7)=1 ×7/6); the small-L(1,χ) guess was
  refuted. The sharpened open question: **what selects the winning field
  club, and at what resolution is argmax-C a stable statistic** — the
  next instrument is a C-decomposition census across a wide ratio grid
  (C = (4/L)·bad-prime product·inert corrections vs kernel data alone).
- **[G] Slope universality.** Objects A and C (§15.5's two displacement-curve objects) both gave displacement slope
  ≈ 0.074 at their own scales; two points do not make a constant. What,
  if anything, pins the shared value?
- **[REFUTED 2026-10-25 — Claude's native-schedule law, certified-bracket arithmetic] The
  native-schedule law.** d ≈ 0.5·m/(2 ln m): the ratio on certified
  points ran 1.27 → 1.22 → 1.14 → 1.11 → 1.02 → **[0.78, 0.88]** at
  m = 1500, where the law predicts 51.3 against a certified bracket
  [40, 45] *(since tightened to [42, 45] — §18.9)* whose incumbent 45 alone sits 12% below. Not converging;
  no replacement form until layer-to-layer spread is measured. Corollary
  casualty: the m/ln²m form held flat at 1.77 across 263–1000 and also
  breaks at 1500 ([1.43, 1.60]). Selection-bias flag [E]: every law
  point except m = 263 is a locked seam (T(m−1) ≡ 0 mod 30, a
  round-number artifact) — the "law" was fit almost entirely on locked
  layers. **[E] CLOSED 2026-11-17 — P3: the neighbor scan.** Two instruments
  (2026-10-24 unpinned 60 s/layer, lab/p3_1490_1510.jsonl; 2026-11-17
  pinned-pillar 30 s/layer, lab/p3_neighbor_scan_1490_1510.json): frozen
  rule [S] passes on BOTH — spread 16 and 12 (≥ 3); unlocked − locked
  +4.26 and +2.50 (≥ 2). Direction concordant: the 30-locked seams are
  the EASIEST layers in the window (locked means 54.0 / 54.5 vs unlocked
  58.3 / 57.0). Consequence: the selection-bias flag on the refuted
  native-schedule law above is decisive — its points were fit almost
  entirely on the easiest layers, so no single-layer law was ever being
  measured. Ledger: INSIGHTS Add.40 (10-24 verdict recovered), Add.41
  (concordance + pi_m = π(m) correction). Original frozen text preserved:
  a neighbor spread ≥ 3 means one layer per scale cannot pin a law; a
  locked-vs-unlocked mean difference ≥ 2 means the lock matters and
  every past law point gets relabeled.
  **Guard 2026-11-17 (Add.43–44): the "lock discount" generalization is
  killed; the P3 closure and the selection-bias consequence survive in
  sharpened form.** Argon's Rule-v3 null check on the frozen JSON showed
  the in-window dip is NOT prime-density confounded (locked P = 105/106
  vs unlocked 107.6 ± 6.0) and survives d/P normalization in both
  instruments — but the extension scan over ALL 8 CRT lock classes mod 60
  (m ∈ {1456, 1461, 1465, 1476, 1480, 1485, 1500, 1501}, n = 8, plus an
  unlocked band 1450–1486, n = 10, matched P to 0.2%) REVERSES the sign:
  d 55.13 vs 54.40 (+0.73), d/P 0.5231 vs 0.5170, dual_lb 39.25 vs 39.0 —
  all noise-level, none ≥ any threshold. What died: "30 ∣ T(m−1) ⇒
  discounted d(m)" as a mechanism (reopen: the dip replicated in ≥ 2
  disjoint m-windows at matched P — the CRT family itself is the test and
  it flipped). What survives [E]: (i) the frozen rules and P3 closure —
  spread is real and the native-schedule law stays refuted; (ii) the
  selection-bias flag, now sharper — the law's points sat on layers that
  are *locally* easy, and that easiness is window-local fluctuation, not
  lock structure; (iii) the open object is the 0.47–0.57 d/P band itself
  (P-structure plus per-layer covering geometry), not any lock effect.
- **[REFUTED, PHASE30 — see §15.8 & §16.6] GLM's CRT-shift collapse.** If covered(N) ⟺
  gcd(N−a, Q) > 1 with d = #{p ∤ a}, the wedge is pure arithmetic at
  every m and "why m/13.5" becomes the ω-degradation rate of Jacobsthal
  run-starts. Audit is queue item #1 for 2026-10-13 (§15.8).
- **[E] CLOSED 2026-10-14 — m = 1000 proven optimum: d(1000) = 37.**
  The 3 h run returned d = 38 incumbent, bound 32; the overnight 12 h
  rerun closed in 4h57m with objective 37 = bound 37, gap 0 (lab/
  PHASE19_sparse_m1000_overnight.md). Law prediction 36.19 — ratio on
  proven points 1.26 → 1.22 → 1.14 → 1.11 → 1.02 (the series' last
  reading: at the certified 1500 bracket the ratio falls to [0.78, 0.88]
  and the law is refuted — §13, 2026-10-25). GLM's frozen d-band
  [37, 43] PASSES at the low edge, fully tested; his d/P companion band
  FAILS (P(1000) = 82, d/P = 0.4512 ∉ [0.49, 0.56] — the asymptotic
  "→ ½" survives, the band doesn't; INSIGHTS 2026-10-14).
- **[G] P11 replication** at a different M_HI, pre-registered, before the
  2.2σ residual carries any weight.
- **[G] The famous fence, in wheel language.** Twin primes = infinitely
  many pair ticks at gap 2; Polignac generalizes to every even gap. The
  structural read (2026-10-12): every solved wheel problem controls one
  number's factorization at a time; twin primes require forcing a second
  number (+2) whose factors nobody controls. A construction that
  manufactures a pair, not a single survivor, is the missing machine.

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
assembly appears unpublished. **Caveat, closed by dated pass.** The sweep's own caveat ("one more pass is owed
before any external submission") was discharged on 2026-11-14 (theorem-audit day,
INSIGHTS Addendum 22): Theorem I's recurrence repositioned against segmented-sieve
prior art (refs. 33–35, §19.1); the §19.4 additive mechanism identified with the
classical covering-systems density theorems (Mirsky–Newman / Filaseta–Kalogirou,
refs. 36–37); the Three-Primitive Theorem positioned against Fueter–Pólya 1923
(ref. 28); the Erdős #7 line repositioned against McNew–Setty (ref. 30) — our
solver-free certificates extend the published odd-moduli classification ≈6.9× past
its bound (same-day repair of an initially inverted comparison; v1+v2 full texts
verified). Öztürk (ref. 32) remains flagged unverified.

**Correction 2026-11-16 (post-release; appended, nothing deleted).** The "≈6.9×"
comparison above does not stand as a statement about the frontier. McNew–Setty
classify covering numbers below 10⁶ and state no odd bound. The odd-covering lcm
line has been carried further by work the 11-14 sweep missed because it is posted
on Zenodo, ResearchGate, the problem's forum and GitHub, not arXiv: Hackmon
(ref. 39, 2026-04); Öztürk (ref. 32, 2026-08, lcm ≥ 11,486,475); Schroeder
(ref. 40, 2026-09, claims lcm ≥ 9,704,539,845 with a Lean package); Wu (ref. 41,
2026-11-02, lcm ≥ 1,527,701,175, stated as Lean-kernel-only). Our settled line
(6,891,885, written 2026-10-30) was behind Öztürk's claim on the day it was
written and is behind ref. 41 now. Item-by-item standing: §18.12, correction
block. Sweep rule added: Zenodo, GitHub and the problem's forum page are searched
in every novelty pass.

**Independent convergence — exact demarcation (located 2026-11-15; credit
boundary fixed same day, pre-release).** D. C. Tucker, *The Atlas of Maximal
Gaps: Exact Covering Enumeration for Primorial Sieves* (Zenodo v2 2026-09-23,
ref. 38; code + certificates: Zenodo DOI 10.5281/zenodo.22865056) is an
independent derivation in the classical primorial-sieve covering family
(Jacobsthal; Hagedorn; Ziller–Morack 2017). His atlas runs a **frozen discrete
gear**: layer {2,3,5,7,11}, period 11# = 2,310 held fixed throughout the
twin-desert table while the covering set grows {13} → {13,…,31} (prime-gap
rows advance to 13# = 30,030 once, at p = 37), computed by a Python
CSP/backtracking solver (`atlas_csp.py`) that stalls at covering-set size 7
(p = 41) — a budget wall his own text flags in the solver section.

Credited to the archive, exactly: the finite Prime/Twin Atlas position
bijection (smallest-prime minimal atlas ↔ position); the Symmetry Theorem
(kill-set palindrome ⟺ layer-prime-divisible center); certified Jacobsthal
values g(p#) for 13 ≤ p ≤ 37 with new first-occurrence positions; and the
empirical twin-desert width table W(p) through p = 31 (66, 108, 150, 204,
258, 348), W(37) ≥ 462 with maximality open at his own budget wall.

Precedence, stated plainly and unchanged: his public record (2026-09-23)
pre-dates this project's public instruments (2026-10-07, privatized
2026-10-19 by directive) and its first wheel run (2026-10-01 09:59 HST,
testimony recorded 2026-11-15); development was bilateral-independent (zero
contact; his v1 ≤ 09-23 either way). The (phase, covering) enumeration over a
primorial sieve is the classical Jacobsthal object — instantiated
independently on both sides — so no formulation priority is conceded or
claimed by either side on that axis.

Claimed here, each verified against the archive by full-text read of its TeX
source (2026-11-15): **(a) the continuous spiral.** One concentric wheel
growing one unit per layer — period T(m) = m(m+1)/2 — collapsing the discrete
primorial gear train (2, 6, 30, 210, 2,310, 30,030, …) into a single
continuous geometry. His text carries no spiral/roll/wrap/concentric geometry
and no zone/wedge language (zero occurrences on full-text grep); the gear
never turns. **(b) the guarantee-zone wedge.** The pair-wedge measurement:
twins structure-forced by wheel resolution alone on 8 zones through p = 31
(d₂ = ∞; exact enumeration certificates through p = 19, Tier-0 solver
witnesses at 23, 31), with the walk-protected regime split measured past
them — zones tested to p = 97, full-wipe d(Z) infeasible on every zone
tested p ≤ 43. A positional-zone object; his nearest notion is per-phase
"defect stratification", not zones. **(c) the solver-free dual-certificate
stack.** Pure-integer dual certificates with no solver in the trusted base,
carrying the certified problem nearly three orders of magnitude past his CSP
wall in period scale (frozen 2,310 → T(1499) = 1,124,250, ≈487×):
d(1500) ∈ [42, 45], both ends solver-free — LB 42 from a 13,740-leaf CBB
tree (verifier PASS, 180 s pure integer, §18.9), UB 45 at 177 rings = primes
p ≤ ⌊√T(1499)⌋ = 1060 (§16.3). **(d) the machine-checked formalization.**
83 theorems, zero `sorry`, Lean 4 + mathlib, axiom footprints ⊆ {propext,
Classical.choice, Quot.sound} — `MainTheorems.lean` + `Sanity.lean`,
9,071-job build green (formalization release 2026-11-15).

We claim certified scale, the solver-free line, the geometric synthesis, and
the formalization — not public priority of the classical formulation.
Convention-level reconciliation of his W(p)/g(p#) tables against §15.2/§18.12
stays an open read-pass (queued in §18.12); his certificates are public (DOI
10.5281/zenodo.22865056), so an independent cross-run is possible.

**Naming.**

**A collision worth noting.** The Rabinowitsch criterion (1913; class number
one settled by Heegner 1952 / Baker 1966 / Stark 1967) governs column
discriminants D = 1−8k = 1−4A with A = 2k. Among integer start-columns the
only class-number-one hit is k=1 (D=−7, checked arithmetically: of the six
Heegner discriminants D ≡ 1 (mod 4), only −7 ≡ 1 (mod 8)). The prime-richness ranking of
columns (richest.py) is a k-parametrized instance of the Jacobson–Williams
2003 extremal-density program. Both connections are formal homes, labeled as
such — they deepen the columns; they do not touch the wheel theorems.

**Naming.** "Prime tread wheel" carries no indexed collision; "wheel sieve"
alone is taken (Pritchard 1981) and is never used here.

## 15. The wedge era (2026-10-11 → 13) — the instrument earns its keep

Three days, six external model voices, one instrument. The wedge distance
of §11 stopped being a metaphor and became an exact MILP object; every
value-side "anomaly" met its correct null; and the displacement curve —
the closest thing the wheel has to a physics experiment — produced its
first theorem-shaped result. Detail: `lab/PHASE14_audit.md`,
`lab/J1C_wedge_result.md`, `lab/PHASE15_wedge_slope.md`,
`lab/PHASE15_dynrings.md`, `lab/RELAY_2026-10-12-evening.md`,
`lab/ARCHIVE_Q_2026-10-12.md`.

### 15.1 The J1c instrument and its conventions

Minimal displacements d of ring phases from home, subject to wiping a
layer's primes. The convention question GLM flagged is not a detail — it
decides whether the object exists. Under the **all-ticks** convention the
wipe is pure arithmetic (a sieve of smallest prime factors decides it;
no solver at any m): wipeable iff m ≤ 13, the window closing exactly at
the ring bound — layer 14 contains 101, the first 97-rough integer. [F]
Under the **seats-only** convention the near-wipe spectrum is empty:
d ∈ {0, 1} across 41 ≤ m ≤ 391 (218 layers at d = 0, 133 at d = 1),
because the trailing seat T(m) carries every prime factor of m(m−1) and
is essentially always home-covered. [measured; mechanism decompressed]

The seam convention is now pinned lab-wide: layer m is the window (T(m−1), T(m)],
rings = primes p ≤ ⌊√T(m−1)⌋. Two solver headers had silently disagreed by a
one-layer shift; the off-by-one evidence is filed and the standard is
set (GPT's "do not silently interchange schedules" warning, adopted).

### 15.2 The cliff is Jacobsthal [E]

The fixed-B cliff — last feasible layer 257 with rings ≤ 97 — is exactly
h(25) = j(97#) = 258, published (Hagedorn 2009; OEIS A048670;
Ziller–Morack 2016). The wheel's cliff is the Jacobsthal capacity of
the ring primorial: no more and no less. Cross-check the same week:
measured one-period tick-gap maxima at layers k = 6, 7, 8 equal j(N_k)
exactly — the cliff appears wherever the wheel touches Jacobsthal.

Positioning against the 2026 frontier: OpenAI's math-model dump (719
manuscripts, 372 families, machine-checked ~42%) contains nothing
wheel-shaped — no sieve arrangements, no covering-system questions — and
its single overlap is Jacobsthal itself, where the published program
proves asymptotic bounds while the wheel measures exact capacities.
Bound vs measurement; both needed; the wheel owns the measurement side.

Also closed [E]: the 7/6 dial census (GPT's PHASE 14 prereg) reproduced
to the unit — 8,280 / 8,180 F1/F2 primes at m ≤ 10⁶ against Bateman–Horn
predictions matching to 4 decimal places, pooled measured/predicted ratio 1.00098, a second
BH instance after 5:4. The dial era's flagship measurement is now a
closed check; the question it leaves — sharpened by the 2026-10-13
evidence swarm (§13 queue entry): not "why 7/6" but "what selects the
winning field club, at what resolution is argmax-C stable" — inherits
the dial theorem's place as the wheel's first theorem-shaped target.

### 15.3 The dissolution streak — 4 for 4 *(extended to 5 for 5 on 2026-10-28 — §18.11 L4)*

Every value-side anomaly the wheel ever produced dissolved into
Bateman–Horn under its correct null, in order: mirror pairs, C4, calm,
and now the archive corpus's double-shot census — 10,062 spokes with
both shots prime (b ≤ 2000, odd denominators only, forced by parity)
against the family-corrected singular series **10,138** (ratio 0.9925)
*(extended to **5 for 5** on 2026-10-28, §18.11: the L4 lattice-ray
probe across 201 live rays and 3,374 same-slope ray pairs in the
$(n_a, n_b)$ Fock lattice dissolves into single-ray Bateman–Horn and
pairwise Hardy–Littlewood 2-tuple singular series, 0 outliers passing
both decades)*.
The correction that closes it: a spoke a/b has both shots pre-sieved by
every prime dividing b, so the local factor at ℓ|b is (1 − 1/ℓ)⁻², not
(1 − 1/ℓ)⁻¹ — 𝔖_fam(b) = 2C₂·∏_{ℓ|b, ℓ odd} ℓ/(ℓ−2). The correction
chain is on record: 5,008 (generic) → 7,582 → 8,672 → 10,138 (exact).
Standing rule earned the hard way: before claiming a wheel anomaly
against Bateman–Horn, compute the BH prediction for the *actual induced
family* — the generic prediction underpredicts by 2×.

### 15.4 P11 — the record-repair saga (method load-bearing)

GLM flagged that the frozen probe header and the frozen INSIGHTS
pre-registration predicted **opposite signs** of the P11 effect. Confirmed
— and both verdicts were wrong. P11c reproduced the number (−0.0073,
stable across halves), then ran the honest null *first*: shuffling within
each ring-2 phase class (the forced arithmetic of the arm) explains ~85%
of it; the residual is a marginal 2.2σ negative hint (p = 0.015, 200
surrogates). Verdict as it stands: neither "PASS" (script text) nor
"clear pattern" (INSIGHTS text) — a marginal residual carrying no weight
until a pre-registered replication at a different M_HI. Standing lesson,
now in the method: when two frozen texts disagree, adjudicate against
the number, not the louder text; and an honest null is run before any
celebration, not after.

### 15.5 PHASE 15 — the displacement curve and its two loads

Object A (25 fixed rings ≤ 97, all 244 layers feasible at that fixed ring budget — the §11 wedge table): the displacement
d grows ~m/13.4 (≈ 13.5), and the constant is not free. Two-load decomposition,
exact predictors: **d ≈ 0.215·U + 0.051·m** (fit R² = 0.974), where U(m)
counts home-uncoverable rough ticks (density → e^(−γ)/ln 97 ≈ 0.123).
Displaced rings harvest rough ticks (~⅓ of the slope, several per ring
via mod-p collisions) and re-cover composite ticks whose home coverage
they broke (~⅔). The 1/13.5 arithmetic: 0.215·(e^(−γ)/ln 97) + 0.051
≈ 0.077 ≈ 1/13.0 against measured 1/13.4. [checked; mechanism reading S]

Two consequences, both confirmed in sign. **(a) The slope is
ring-budget-contingent.** At B = 53 the finite points sit a consistent
+2.2 above the B = 97 prediction (fewer rings, less collision freedom);
the B = 31 wheel cannot cover 60 ticks at any displacement — a new
Jacobsthal bracket, j(31#) ≤ 60. Constants calibrated at one B do not
transfer. **(b) Under the native schedule the linear law breaks.**
With rings = primes ≤ √T(m): d/P ≈ 0.49–0.59 stable across a 2.3×
m-range (harvest efficiency rises with ring density — d falls *below*
the fixed-B floor), d/m declines monotonically 0.0570 → 0.0533 → 0.0475
→ 0.0433 across m = 263…600, and the m = 1000 sparse MILP (2 MB matrix,
the dense build's 19.8 GB OOM is dead engineering) returned d = 38
incumbent against the law's prediction 36.2 — 5% above, inside the
historical scatter (overnight rerun 2026-10-14 closed d(1000) = 37
proven optimal, gap 0 — law ratio on proven points down to 1.02; the
era's incumbent readings were upper bounds, never proven points).
Sublinear: d ≈ 0.5·m/(2 ln m), i.e. d/m ~ 1/(4 ln m). *(Verdict
2026-10-25: refuted at the certified 1500 bracket — ratio [0.78, 0.88];
§13 carries the table, the seam-lock selection bias, and the P3
neighbor-scan obligation.)*

### 15.6 N1 — finiteness is Jacobsthal windows [F+E, convention-pinned]

With native rings, layer m is wipeable iff its width fits under the
Jacobsthal capacity of its ring primorial: the infeasible set is exactly
{2–18, 22–24, 26, 27, 40, 41}, every m ≥ 42 is wipeable, and every
non-edge layer matches the published table (A048669) under the pinned
seam convention. "Finite under native rings" is thereby promoted from
trend to theorem — the wheel's first theorem-shaped result, and honestly
labeled: it is contingent on the seam convention (now standardized), its
edge layers (2–4) are convention-dependent and flagged as such, and its
explicit construction (x ≡ 0 mod all primes ≤ p_{k−2}, x ≡ −1 mod
p_{k−1}, x ≡ 1 mod p_k, giving a covered run of 2p_{k−1} − 1) is
classical in method. [F + E]

### 15.7 Archive queue — the ancestral corpus, settled

The pre-reboot Downloads corpus (~830 files: prime whitepapers, Collatz,
Erdős) was triaged by five parallel agents; four items entered the lab
and all are now measured. Echo Cascade's 2p±1 doubling graph reproduces
exactly (π(5·10⁷) = 3,001,134; balance 1.00007 — forced by mod 3, and
p = 3 is the *only odd* prime with both 2p−1 and 2p+1 prime). The
isolated-prime census reproduces (density rising toward 1, tracking
1 − 4/ln p; the printed 15.4% stays falsified by its own data). The
knockout wall reproduces inside the reboot (biggest-needed gear → 98.1%
of √x by layers 2000–3000). Hooley's 1965 law is added to the literature
sweep: gaps between integers coprime to n are exponential in the limit
n/φ(n) → ∞; finite wheels show the truncated form, squeezed by the
lattice floor (min gap 2) and capped exactly at j(N_k) — the cliff
appearing a third time. Three pseudo-results killed in one line each and
filed so nobody resurrects them. [E] Full ledger:
`lab/ARCHIVE_TRIAGE_2026-10-12.md`.

### 15.8 GLM's CRT-shift collapse [audited DEAD 2026-10-16 — PHASE30, §16.6]

The claim, as handed back: a layer is covered at translate N iff
gcd(N−a, Q) > 1 (Q the ring primorial), so the displacement count is
d = #{p ∤ a} — the count of primes *not* dividing one CRT shift —
position-independent, and the wedge at every m becomes pure arithmetic
with no MILP at all. Hand-verifications quoted (B = 3, B = 5, m = 14,
m = 257/258, the 1/6 2-adic shell) are GLM's. **Verdict (PHASE30): dead.**
At the only pinned reading of the free variable (a = T(m−1)) it
contradicts the proven d-table 39/42; its two own formulas for d
disagree 3.4× at m = 1500; the ring-97 cliff is actually at m = 137.
Mechanism diagnosis in §16.6.

## 16. The covering-game era (2026-10-13 → 16) — the train, the campaign, four closures

The wedge era's cost question matured into an exact game, and the game
became the project's second certified object alongside the stagger field.
Full detail: lab/PHASE21–30, INSIGHTS entries 10-13 → 10-16.

### 16.1 The game, corrected [E]

d(m) is not "minimum unpainted ticks." The MILP makes full painting a
hard constraint and prices *dial rotations*: each ring's native phase
(paint multiples of p) is free; every rotated residue class costs 1.
d(m) = the minimum rotation bill to paint the whole layer. The native
stripes — zero rotations — always miss exactly the wheel-primes, so
free painting fails in exactly the layers that hold one: **[F]
d(m) ≥ 1 ⟺ layer m holds a prime**, A066888 restated as a price list
("protection is arithmetic, located, and priced" — the price is ≥ 1
rotation). The equivalence is by the game's definitions; the universal
"every layer" direction behind it is verified computationally per layer
(§16.2's table, A066888 directly to 2.8 × 10⁹ layers) and proven in
general nowhere — carried as observation, not theorem.

### 16.2 d(m) proven to 60 — feasibility has a geography [E]

Verified d(m) for all m ≤ 60 (enumeration ≤ 33, MILP 34–60, zero gap).
Rows 1–18 are unpaintable *at any price* (proven infeasible). The game
first opens at m = 19 — exactly where ring 13 first enters, 13² = 169 ≤
171 = T(18) (E5 errata: the native-from rule is p² ≤ T(m−1), not p² = T(m); for p = 13, 169 ≤ T(18)
= 171, native from layer 19), a prime square landing on a seam — at cost 3. Dark rows: 22–24,
26–27, 40–41 (the pair right before ring 29 arrives). Winnable rows
cluster on ring-arrival moments; past m = 34 nearly everything is
winnable and d wobbles in [5, 8] — no clean staircase on the incumbent
side. The staircase question survives on the dual side (§16.3).

### 16.3 The m = 1500 campaign: bracket [26, 49] at Phase-A close [E] — superseded; certified bracket [42, 45] with LB 42 unconditional and solver-free (§18.9 Thm 9, CBB, 2026-10-27)

Fourteen seeded lanes on a rented 56-core box (warm-start 6 h chunks,
8 chunks each, 62 h total; relaunched once after a billing stop).
Final harvest 2026-10-18: every lane's best vector independently
re-verified in pure Python — uncovered = 0, every phase in range, no
solver report trusted. Lanes 3/5/6/9 at exactly 49 nonzero phases, so
d(1500) ≤ 49 stands on recomputation; lanes at 50/51 are feasible
covers, not incumbents. Nothing beat 49 anywhere in the campaign; the
rig-era 47 went 62 h × 14 diverse seeds unreproduced and is filed as a
vectorless artifact — honest incumbent 49; 48 never appeared in any lane. Best dual bound found anywhere:
26 (lane 13). Final bracket: 26 ≤ d(1500) ≤ 49. Instance destroyed
after harvest (all value local: 156 files, 37 MB in
the archived lab record). Two measured regularities stand:
incumbents are found fast and freeze (12 lanes within 2 of each other —
a deep pit, no ladder found), while certified bounds climb slowly. The
difficulty of the question lives on the "no" side, not the "yes" side.
Queue: Phase B — one lane, all threads, uninterrupted, warm-started from
the verified 49-vectors — built to drive the bound up; if the bounds
ever meet the incumbent, d(1500) becomes a proven exact integer.
*(Bracket superseded 2026-10-20 — §18: Phase B closed it at [38, 48],
then [38, 47] with the incumbent witnessed, no longer just reported;
§18.4, §18.7 — and finally [40, 45] on 2026-10-25, both ends
solver-free: §18.9 Thm 7 CBB + §18.10 cleaned 45; tightened to **[41, 45]**
on 2026-10-26 — LB 41 unconditional and solver-free via the CBB hybrid
t41 tree (§18.9 Thm 8) — and to **[42, 45]** on 2026-10-27, LB 42
unconditional and solver-free via the CBB hybrid t42 tree (§18.9 Thm 9).
**Ring-set rule pinned explicitly [F + E]:** throughout the m = 1500
campaign, "177 rings" means all primes $p \le B = \lfloor\sqrt{T(m-1)}\rfloor = 1060$
($177$ primes up to $p = 1051$; using $\lfloor\sqrt{T(m)}\rfloor = 1061$
would admit a 178th ring $p = 1061$). Both the CBB engine (`cbb_gen.py`
/ `cbb_fast.py`) and every banked witness (`best48`, `best47`, `best46`,
`best45_argon_clean.json`) use this exact 177-ring rule and identical
rotation-count objective.
GLM's frozen F5 band $d(1500) \in [50, 57]$ (pred 53.8, fired
against 2026-10-14) died the day the campaign verified 49 and is
falsified by the upper bound alone: the verified 45-rotation witness
($d(1500) \le 45 < 50$, §18.10, same 177-ring rule and objective;
flagged by GLM against its own prediction and noted by GPT, 2026-10-28)
refutes the band five ladder-rungs deep (49, 48, 47, 46, 45) without
needing the CBB lower bound. Consequently, GLM's companion band F5-2000
$[64, 72]$ is downgraded to expected-falsified, and GLM's provisional
replacement $d(2000) \in [44, 56]$ is logged as **[S]** (not frozen
until a single predictor is committed). Recorded here because the
paper keeps its dead predictions, not only its live ones.)*

### 16.4 The carpet closes twice; F9 dies as preregistered [E]

The PHASE22 "uniform carpet" (prime pairs in even layers sitting oddly
flat) was closed two independent ways: by convention (PHASE24 — the
histogram credits both mirror members on an already-flat background,
near-entailed before data arrives) and per-factor (PHASE28 — splitting
even layers by small-prime divisibility, every local factor matches the
Hardy–Littlewood singular series to ~1–3 parts in 1000: 2.0053/2.0000,
1.3345/1.3333, 1.2024/1.2000). GLM's F9 edge-tilt froze and died on its
own preregistered decision rule (no tilt, all bins flat). Three
epiphanies buried by the lab's own null machine; the standing rule
(v3) is the product: no effect claim without a *complete* null.

### 16.5 The witness harness: j = m−1 is the load-bearing hinge [E]

Claude's P-TRI harness (457 windows): a machine generates all-composite
runs of length m sitting right after a triangular seam, with the native
ring bound — rows indistinguishable from wheel layers in every
measurable respect except one: in wheel layers the window length equals
the seam index plus one (j = m−1). Consequence, now house law: any
"two lines" deriving a prime from seam algebra alone dies 457 times
before it is written; a valid Item 4 must use the coupling. Ceiling
check: a wheel layer is 3–10× narrower than what RH guarantees primes
in, so two lines proving A066888 would outrun RH. Incoming lines get
run against the m = 28 witness first. Also relocated: the "+7"
obstruction lives on 8N = (2m−1)² + 7, D = −7 ⟺ k = 1 exactly, and
−3/−8 can never be native columns (PHASE6's sightings are dial-family).

### 16.6 GLM's CRT-shift collapse: dead on audit [E]

Gemini-relayed (§15.8's queue item), adjudicated in one hour against
§16.2's proven table. At the only pinned reading (a = T(m−1)) the
formula d = #{p ∤ a} predicts finite prices for rows the MILP proved
unpaintable at any price: 39/42 mismatch; the m = 20 "match" is
coincidence (m = 19: predicts 5, truth 3). At m = 1500 its two
formulas disagree 3.4× — #{p∤a} = 173 vs the §15.5 trend's 0.5·m/(2 ln m) = 51.3 (the trend law itself was refuted 2026-10-25, §13),
measured 49; the trend line only touches reality at the one scale where
a number already existed. The ring-97 "cliff" is at m = 137 under the collapse's formula, not 257 — the true cliff (§15.2) stands
(√T(257) = 182). Mechanism-level cause: the premise states when a
*single number* is caught by the sieve; the game asks whether *every
tick* can be hit by joint stripe placement. The connector was asserted,
never derived, and "position independence" is refuted by the dark rows
themselves (24 dark; 19, 20, 30 winnable — paintability depends on
where the seam sits). An identity with an unpinned input cannot be
falsified; this one was pinned anyway and failed at every reading. The
C-decomposition census queued behind the collapse stays gated (reconfirmed by the 2026-11-14 status pass — never reopened).

### 16.7 Standing rules and the queue after this era

Rule v3 (complete nulls) has now killed three of the lab's own
surprises. Item 4 (GLM's priced reduction) — dead 2026-10-16, the
CRT-shift collapse failed audit (§15.8, §16.6); Phase B on the m = 1500 bracket (single-lane all-threads
proof grind, launched 2026-10-18 — concluded 2026-10-20 at [38, 47],
tightened through 2026-10-27 to **[42, 45]** with both ends
solver-free, §18.9 Thm 9 + §18.10); the two wheel-native questions no
instrument answers — why
the native stripes always miss something, and why a fresh ring unlocks
a layer *(second question closed 2026-10-24 — §17.2 P4: a fresh ring
plugs the x ± 1 escape hatches flanking a locked primorial center,
stretching the covered run to 2p_{k−1} − 1)*.
Instrument for both: lab/train.html, the wheel laid flat.

### 16.8 The seam-lock retraction (2026-10-13 night, three-way verified) and the Three-Primitive Theorem [F + E — the retraction's E is three-way agent verification, INSIGHTS 2026-10-13; the theorem itself Lean-kernel-certified 2026-11-14]

The era's one retracted wheel-uniqueness claim, preserved with its
scope. Failed prediction (v2, item (c)): "among linear-turn spirals,
only turn length m phase-locks ring m to its own layer." The lock is in
fact generic to the whole affine class L(m) = a·m + b with b = 0 —
every such spiral locks its seams, Ulam (a = 8) locks identically to
the wheel, and Sacks (b = 1) misses the *phase-0* lock — locking instead
at phase ¼ — because of the constant,
not because of its geometry. Verified independently by GPT (exact plus
enumeration), Claude (direct check; retracted his own claim), and Grok
(same algebra). The prediction failed at the class level, not at the
wheel level; folded into the v2 spec as dated correction §10 with the
failed prediction kept beside its surviving scope. What survives is
theorem-grade [F]: GLM's lock+palindrome lemma — for quadratic counts
B(m) = (αm² + βm + γ)/2 with shadows o_q(m) = −B(m) mod q, the seam
lock (∀ odd m, q | m ⟹ o_q = 0) ⟺ γ = 0 (the count starts at the
origin), the lap palindrome B(m) = B(1−m) ⟺ α + β = 0, and both
together with the 1:1 turn condition L(m) = B(m+1) − B(m) = m force
α = 1: **B = T(m−1), uniquely.** The wheel keeps the lock — it just
no longer keeps it alone.

- **The Three-Primitive Theorem (`2026-10-28`, Claude + Argon + GLM) [F].**
  Among general discrete spirals $\Phi(m, k) = B(m) + k$ ($1 \le k \le L(m)$),
  consider five candidate structural primitives on the lap-start function
  $B : \mathbb{Z}_{\ge 1} \to \mathbb{Z}$ and lap-length function $L(m)$:
  - **$P_1$ (Origin & contiguity):** $B(1) = 0$ and $B(m+1) - B(m) = L(m)$ for all $m \ge 1$.
  - **$P_2$ (Affine lap growth):** $L(m) = a m + b$ for constants $a, b$.
  - **$P_3$ (Unit step):** $L(m+1) - L(m) = 1$ for all $m \ge 1$.
  - **$P_4$ (Odd-divisor seam lock):** for every odd $m \ge 1$ and every $q \mid m$, $B(m) \equiv 0 \pmod q$.
  - **$P_5$ (Lap palindrome):** the polynomial extension of $B$ satisfies $B(m) = B(1 - m)$.

  *Theorem & Proof [F]:* First, $P_3 \implies P_2$ immediately ($L(m) = m + b$
  with $a = 1$ and $b = L(1) - 1$), so $P_2$ is redundant. Combining
  $P_1$ and $P_3$ yields the one-parameter family
  $B(m) = \sum_{j=1}^{m-1}(j + b) = T(m-1) + b(m-1)$. Since
  $T(m-1) = \frac{m(m-1)}{2}$ satisfies both $q \mid T(m-1)$ for all odd
  $m$ with $q \mid m$ and $T(m-1) = T(-m)$, we have $B(m) \equiv b(m-1) \pmod m$
  for odd $m$ and $B(m) - B(1-m) = b(2m-1)$. Imposing $P_4$ even at a
  single odd $m > 1$ (e.g. $m = 3 \implies 2b \equiv 0 \pmod 3$, and
  across odd $m$, $\gcd(m, m-1) = 1 \implies m \mid b$ for all odd $m$)
  forces $b = 0$; imposing $P_5$ forces $b(2m-1) = 0 \implies b = 0$.
  Therefore **$P_4$ and $P_5$ are equivalent given $P_1 + P_3$, and
  either three-axiom set $\{P_1, P_3, P_4\}$ or $\{P_1, P_3, P_5\}$ is
  a minimal independent basis that uniquely forces $B(m) = T(m-1)$.** $\square$

  *Independence witnesses [F] (dropping each primitive from $\{P_1, P_3, P_4/P_5\}$):*
  1. **Drop $P_4 / P_5$ (keep $P_1, P_3$):** $B(m) = T(m-1) + (m-1) = \frac{(m-1)(m+2)}{2}$
     ($L(m) = m + 1$, $b = 1$) satisfies $B(1) = 0$ and $L(m+1) - L(m) = 1$,
     but fails $P_4$ ($B(3) = 5 \not\equiv 0 \pmod 3$) and $P_5$
     ($B(2) = 2 \ne -1 = B(-1)$).
  2. **Drop $P_3$ (keep $P_1, P_4, P_5$):** $B(m) = 2\,T(m-1) = m(m-1)$
     ($L(m) = 2m$) satisfies $B(1) = 0$, $B(1-m) = (1-m)(-m) = B(m)$,
     and $m \mid B(m)$ for all $m$, but has step $L(m+1) - L(m) = 2 \ne 1$.
     *Formalization note 2026-11-14:* witness (ii)'s $P_5$ is evaluated under
     its interpolating polynomial $x(x-1)$ (a palindrome — kernel-certified);
     under the $P_1 \wedge P_3$-family reading used in the main theorem it
     does not apply, since (ii) is not in the one-parameter family. The
     witness table silently mixes the two readings of $P_5$; both readings
     are now certified in `lean_wheel/Wheel/ThreePrimitive.lean`, and the
     main theorem is unaffected.
  3. **Drop $P_1$ (keep $P_3, P_4, P_5$):** Taking $B(m) = T(m-1) + c_0$
     with $c_0 \ne 0$ (and $L(m) = B(m+1) - B(m) = m$) satisfies $P_3$
     and $P_5$ ($B(1-m) = B(m)$) while violating $B(1) = 0$ and $P_4$;
     alternatively, decoupling $B(m) = 0$ from $L(m) = m$ satisfies
     $B(1) = 0, P_3, P_4, P_5$ while violating contiguity $B(m+1) - B(m) = L(m)$.

  *Positioning & scope note 2026-11-14 [E, external novelty audit].*
  (i) The uniqueness of the Cantor enumeration among *quadratic polynomial
  bijections* is classical — Fueter–Pólya 1923. The Three-Primitive
  Theorem is an elementary *alternative axiomatization* of the same object
  by divisibility/palindrome primitives, not a strengthening; cite and
  position against Fueter–Pólya or a reviewer will lead with it.
  (ii) $P_5$ presupposes $B$ has a polynomial extension and therefore
  restricts that branch to polynomial $B$; the $P_4$ branch is fully
  general over integer sequences ($P_1 + P_3$ force the quadratic family
  by summation alone).
  (iii) The "$P_4$ at a single odd $m$" phrasing is compressed: one $m$
  gives $m \mid b$ only; it is the universal quantifier over odd $m$
  that forces $b = 0$. Exact statement verified line-by-line; no defect.

### 16.9 P-SAX: the Sacks audit (2026-10-14 morning) [E]

Claude's P-SAX ran the Sacks spiral against every observable it froze
in advance — tick-1 Bateman–Horn counts, dead columns, locked-seam
profiles against the spiral's own seam polynomial — and all matched
within σ. Mechanism reading: each Sacks feature is explained by its
own seam polynomial; nothing structural is carried by the Sacks
geometry as such. His "Sacks loses nothing structural" therefore
stands, scope-limited to tested observables; the one self-caught
mis-specification (a 3σ profile freeze that omitted the p > 7 tail —
same error class as the #18 composite bucket) is logged as an erratum-class caveat. The
observable P-SAX did *not* test then landed: GLM's two-shot
localization — Sacks spokes carry primes at unbounded depth (in-table
to depth 148 at value bound 2 × 10⁵), because forced compositeness on
a spoke occurs only at depths g+1 with g | C(a,b) (the Sacks spoke constant; §16.9 audit, INSIGHTS 2026-10-14). Symmetric patch
filed to GLM's wheel side (the same free-parameter catch as Q1):
"forbids depth ≥ 3 absolutely" holds from depth 4 up; at depth 3 the
forcing value 2b² − b + 2a is prime on 14/28 spokes. Wheel caps at
depth 3 behind a primality window; Sacks is unbounded. Together §16.8
+ §16.9 answer the "is the geometry special?" question in the wheel's
own terms: the features are polynomial-explained on any spiral, and
the wheel's corner is the surviving lock's unique B = T(m−1) endpoint,
the stagger-field temporality, and the pairing — not any single
spiral's picture.

## 17. The wheel-native sieve session (2026-10-17) — primorial flanks, twins, the escape chain

A morning session with Sylvan, run entirely on the wheel toy's own language
(wheels = residue classes, landings = divisibility, layers = new wheels).
Every claim below was tested the same morning it was stated; full ledger:
INSIGHTS.md 2026-10-17 08:11 → 09:40.

### 17.1 The offset mirror: every landing guarantees a mirrored immune pair [F]

Wheel p's carve at address x leaves x±1 untouched by construction (x lands
exactly; its neighbors miss by exactly one tick each), so every landing
manufactures two immune addresses, mirrored across the landing, one on each
side. Twin *candidates* are thus guaranteed at formation, every wheel, every
time. What the mirror does not guarantee is survival: later wheels carve
one-sidedly (23 and 25 flank the same 24; wheel 5 kills 25 only), so
pair-formation is forced while pair-survival is not. This is the wheel-native
restating of why twin *existence* is unproblematic but twin *infinitude* is
the open problem.

### 17.2 Layer territory opens at p²; the +1 unit is untouchable past a finished base [F]

Below p², wheel p lights only on corpses (every multiple pq with q < p is
already killed by q's wheel); its first fresh kill is p·p. The √x boundary
falls out of the same remainder arithmetic — any composite has a factor ≤ its
square root, so wheels past √x are pure spectators near x. Past a completed
base P (product of all wheels ≤ l), the address P+1 is invisible to every
wheel in the base: they land dead-center on P, their next landing is a full
wheel away, so none can touch the +1. The same argument gives P−1. Every
completed base therefore manufactures a twin-*candidate* pair (P−1, P+1),
immune to the entire base. This is Euclid's escape restated on the wheel; it
also gives the double escape — (P·q₁)+1 forces a second prime beyond l, so at
least two primes beyond every layer exist unconditionally.
- **[F] Cross-link — the fresh-ring unlock is the hatch-plug, in Sylvan's
  picture (P4, 2026-10-24).** The open rows of the proven d(m) table
  (§16.2) sit exactly where the Jacobsthal capacity of the ring set
  outruns the layer width (§15.6, N1): ring 13 arrives at layer 19 with
  capacity 21 (rows 22–24 dark), 17 at 25 with 25, 19 at 28 with 33,
  23 at 34 with 39 just in time, 29 at 42 with 45 (rows 40–41 dark), 31
  at 45 with 57 — from there capacity always wins. Made exact: the
  extremal cover behind the capacity is a *locked center* x with every
  small ring home on it (x ≡ 0 mod all primes ≤ p_{k−2}); the whole run
  around x is covered except the two ticks on either side of the center,
  x − 1 and x + 1 — precisely the escape hatches of this section. The
  two freshest rings plug them: x ≡ −1 (mod p_{k−1}) and
  x ≡ +1 (mod p_k), giving a contiguous covered run of 2p_{k−1} − 1.
  **A fresh ring unlocks a layer by plugging one of the two escape
  hatches flanking a locked center** — Sylvan's "misaligned on both
  sides of ½" is the two-sided hatch. This closes the §16.7 standing
  question "why a fresh ring unlocks a layer" in the wheel's own terms:
  the construction is classical; the reading is wheel-native.

### 17.3 The dead-flank rule: a killed primorial flank always costs ≥2 primes [F → E]

Stated 09:02, proven from remainder arithmetic alone before testing: if
P±1 is composite, its smallest factor q cannot divide P (q ∤ P and q | P±1),
so q > l; the cofactor is ≥ q, so a dead flank certifies at least two primes
(strictly: Ω ≥ 2 with multiplicity; every prime factor > l, the smallest in the danger zone (l, √(P±1)]).

Confirmed by full factorization of all 13 primorial flanks to 41# (14 dead
flanks, every factor > l, Ω values mean ≈ 2.6, no prime-square flank
observed) and by the unconditional double-escape route. Every executioner
lives in the danger zone — the small wheels carve the candidates, the
mid-size wheels execute.

### 17.4 Two falsified predictions (kept, with their surviving weaker versions)

1. **"Twins after a point live only on primorial flanks"** — refuted by
   direct count: 14,871 twin pairs below 2×10⁶, exactly 3 of them primorial
   flanks ((5,7), (29,31), (2309,2311)). Twins per inter-primorial interval
   *grow* (10, 55, 398, 4,168) — the predicted desert between bases is the
   densest territory on the strip.
2. **"Primorial neighborhoods are twin-rich"** (the 08:58 salvage) —
   refuted by window test to 25M: twin density at primorials equals the
   global 2C₂/ln²x law to within 1% (ratios 0.99–1.01), and random windows
   match their own local prediction too. The +1 immunity is a *point*
   guarantee — two addresses per base — and dilutes to invisibility at
   window scale. What survives: flanks survive at ~46% (12 of 26) against a ~1%
   candidate-pair baseline, exactly as the immunity argument predicts
   (predicted 14.8 of 26 flanks, observed 12 — ≈1.1σ, consistent).

### 17.5 The escape chain: bag bases have holes, and the walk finds them [E, new observable]

New object, defined and run 09:40: start P = 1; each step read P+1; if
prime, q = P+1 (full escape), else q = spf(P+1) (spf = smallest prime factor); new base P′ = P·q. A
deterministic walk on the primes generated by the mechanism itself. First
run: 21 steps to a 79-digit base; 6 full escapes (each ≈ squaring the
base), 15 caught escapes — two growth regimes, one walk.

**The surprise.** 14 of 15 caught escapes were executed by wheels *smaller
than the largest wheel already in the base* — including q = 5. Cause: the
chain's base is a *bag* of collected wheels, not the primorial, and the +1
escape is only immune to wheels in the bag. Wheels never collected (5, 11,
17, 37…) stay live and execute escapes that the consecutive-base picture
calls already-covered territory. Only one kill in 15 was a true
danger-zone execution. The walk is therefore a machine for certifying holes
in any non-consecutive "covered" claim. Open: does the bag ever fill, and
how fast? Instrument: `lab/escape_chain.html` (built by
`lab/build_escape_chain_page.py`).

### 17.6 Standing after this session

Every measurable quantity the wheel toy produces now matches the sieve
bookkeeping within noise: candidate share per layer (∏(1−2/p) over odd
wheels: 11.69% → 7.81% across l = 11 → 19, the measured "less p between
gaps"), twin density at primorials and at random offsets (ratio ≈ 1.00),
flank survival (12 vs 14.8 predicted), executioner sizes (ordinary mid-size
wheels). The framework is closed at its own resolution. What remains open
is no longer a statistics question: the twin conjecture, the desert-growth
law, and the infinitude of primorial primes are single-configuration-at-
infinity questions the enumeration cannot vote on.

### 17.7 The exact parabolic multiplicity theorem (2026-11-17) [F + E]

The §13 selection-bias closure (2026-11-17, two instruments) left a smaller
question exposed: the seam-twin census showed twins forbidden at `k ≡ 0
(mod 3)` and the `(N, N+2, N+8)` triple forbidden at a unique residue mod 5,
but the *counts* across the surviving classes looked like "finite-k
Bateman–Horn noise" (25,339 vs 50,220, ratio 1.982). They are not noise.
The asymmetry is an exact phase-counting theorem, and it is now
Lean-kernel-certified (`LeanWheel/ParabolicConstellation.lean`,
FORMALIZATION_STATUS.md item 21).

**Setup [F].** A constellation `N + D` with `N = T(m−1) + k` meets the
residue class of `d ∈ D` at an odd prime `p` exactly when `T(m−1) ≡ −(k+d)
(mod p)`. Since `8·T(m−1) ≡ (2m−1)² − 1 (mod p)`, this reads

```
N + d ≡ 0 (mod p)  ⟺  (2m−1)² ≡ 1 − 8(k+d)   (mod p).
```

**Fiber lemma [F].** On a finite field of odd characteristic the squaring
fibers are `{x : x² = c}` of cardinality `1 + χ(c)`: 1 at `c = 0`, 2 at
nonzero squares, 0 at non-squares (each `c ≠ 0` has two roots `±x`, and
`x ≠ −x` because `2 ≠ 0`). Under `m ↦ 2m−1` — a bijection since `2 ≠ 0` —
the fiber count transports unchanged.

**Union law [F] — the mechanism that makes it exact.** Fibers at *distinct*
right-hand sides are disjoint (a function has one value per point), so the
killed m-phases form a disjoint union and there is nothing to subtract twice:

```
S_{p,D}(k) = p − Σ_{distinct c ∈ 1−8(k+D)} (1 + χ(c)).
```

This is a statement about *phases*, not densities: per `k`, every residue
class mod `p` is either fully open or fully closed to the constellation.
No Bateman–Horn input enters; the sieve density only weights the observed
counts across the `k`-range afterward.

**Exact splits.** Twins `D = {0,2}` at `p = 3`: `T(m−1) mod 3` visits
`[0, 0, 1]` (the vertex residue 1 once, the arm 0 twice), so survival needs
`T(m−1) ≡ 2 − k`, giving the exact `(0, 1, 2)` split across
`k ≡ (0, 1, 2)` — kernel-checked by `decide`
(`Wheel.twin_phase_count_mod3`, phase lists
`[] / [2] / [0,1]`). Triple `D = {0,2,8}` at `p = 5`: orbit
`[0, 0, 1, 3, 1]`, exact split `(2, 3, 0, 3, 2)`, with `k ≡ 2 (mod 5)` the
unique killing residue (0/5 phases) — kernel-checked
(`Wheel.triple_phase_count_mod5`). This also repairs the mod-5 prose table
circulating in the lab notes: the orbit is `{0,0,1,3,1}` with survival
`k+d ∈ {1,4}`, so the class weights are `(2,3,0,3,2)` — classes 3 and 4
were swapped in the handwritten table; both the probe's
`algebraic_certificate` and the empirical census agree on the corrected
values.

**Census [E].** `lab/probes/parabolic_obstruction.py` (output on record at
`parabolic_obstruction_2026-11-17.out`): over `m = 4..29,999`, `k ≤ 600`,
twins split `0 / 25,339 / 50,220` across `k ≡ (0,1,2) (mod 3)` — observed
ratio 1.982 against the exact phase ratio 2:1, the gap being density
weighting across the `k`-range (the `k ≡ 2` class samples slightly thinner
prime country), not phase noise; triple shares `0.1943 / 0.3016 / 0 /
0.3007 / 0.2034` against exact `(2,3,0,3,2)/5`. Seam-straddling twins: 0
(the §17.3 dead-flank rule at `p = 3`). Zero violations of any exact phase
prediction in 6× the earlier census depth.

**Axiom audit.** All five theorems (`sqr_fiber_card`,
`sqr_fiber_affine_ncard`, `surviving_phases_eq`, `twin_phase_count_mod3`,
`triple_phase_count_mod5`) carry the mathlib trio only, verified by
`#print axioms`; the two phase-count theorems are closed by kernel
reduction (`revert k; decide`), so the exact arithmetic is machine-checked
rather than hand-cased. 88 theorems, zero `sorry`, build 9072 jobs clean.

**Integer bridge [F] (2026-11-17, second pass — Add.44).**
`Wheel.twin_int_kill_mod3` (with the helper `eight_mul_T`, the doubling
identity scaled by 4): for every layer `m` and tick `k` with `3 ∣ k`, at
least one member of the integer twin pair `(T(m−1)+k, T(m−1)+k+2)` is
divisible by 3 — the `k ≡ 0` row of the table above on the wheel's
integer coordinate, no density input. The mechanism is period-3 in `m`:
`m ≡ 0, 1 (mod 3)` kills via the left member (`3 ∣ T(m−1)`), `m ≡ 2
(mod 3)` kills via the right (`T(m−1) ≡ 1`, so `T(m−1)+k+2 ≡ 0`). Cast
through `ZMod 3` (`CharP.cast_eq_zero_iff`), finite case table closed by
`decide`; mathlib-trio axiom footprint verified by `#print axioms`.
89 theorems, zero `sorry`, build 9072 jobs clean. (Note this bridge is a
fiber-count statement over all integer layers; it is neutral to — and was
motivated independently of — the §13 guard on the lock-discount
formulation, which lives on the covering-number side.)

## 18. The Phase B proof grind (2026-10-18 → 20) — the 48 banks

Phase B ran the §16.3 queue item: one lane, all threads, uninterrupted,
warm-started from the verified 49-vectors, built to drive the dual bound.
It delivered the bound (26 → 38) and, en route, closed the project's
recurring failure mode — the vectorless artifact — twice over. Full
ledger: INSIGHTS.md 2026-10-18 → 10-20; artifacts
lab/phaseb_2026-10-19/.

### 18.1 Run 1: the 48 exists, then dies vectorless [E]

24 h single-lane solve (seed 101, 28 threads, warm start from the
verified 49s) on a rented 28-core shared host. Console log: BestSol
reached 48 at ~13 h 50 m solve time (§18.3's clock correction) and held ~10 h straight; dual bound
climbed to 37.5564. At 82233 s of the 86400 s budget the process took an
external SIGKILL — no traceback, log truncated mid-line, 69 minutes
early. Host forensics (load average 42 on 28 cores, ~65 foreign python
processes) point at the shared host's OOM killer reclaiming the fattest
process; a second tenant's 48-worker fleet landing on the same box
mid-run is the leading suspect but is [S, unproven] — correlation, not
established causation.

The runner wrote solution vectors to disk only after the solve returned.
The kill landed first. So the 48 — true, held for ten hours — never
reached disk: the second vectorless artifact, after the rig-era 47.
The console log preserves bestSol = 48 and the full bound ladder, so the
*knowledge* survived; the *certificate* did not. Superseded readings
marked, not erased: the rig-era 47 stays filed as vectorless; run 1's 48
was re-derived and witnessed (§18.4), so the artifact record now reads
47 (vectorless, unreproduced), 48 (vectorless once, now banked).

### 18.2 The fix: certificates must outlive the process [E]

`lab/phaseb_2026-10-19/phaseB_ckpt.py` — the same sparse MILP driven
through HiGHS, plus one connector the old runner lacked: a
mip-solution callback that banks every improving solution to disk the
instant HiGHS accepts it, and a warm start read at launch. Verified
working: the warm-start 49 was banked 5.1 s after process start.
From this entry forward, no solution the campaign claims exists only in
process memory — house law for every rented-box solve, on the recorded
grounds that a shared host can die at any minute and the certificate
must not care.

### 18.3 Determinism confirmed as a numerical fact [E]

The rerun (same model, seed 101, 28 threads, same warm start) replayed
run 1's bound ladder bit-for-bit — 13.86 → 17.49 → 18.88 → 22.31 →
26.89 → 32.03 — including one replay executed *while the box was being
starved by the foreign fleet* (55% of one core). HiGHS's trajectory at
fixed seed and thread count does not depend on wall-clock timing, only
on being allowed to finish. Consequence: waypoint forecasts on the
trajectory are evidence-backed, not hopeful.

Honest correction to that forecast, recorded because it is the useful
part: the 48 itself reappeared at ~11 h solve time, not at run 1's
~13 h 50 m mark. The ladder's first half replayed identically; the
second half branched. Deterministic means the *path quality* repeats,
not the *clock* — trajectory forecasts should quote rungs, not hours.

### 18.4 The certified bracket: d(1500) ∈ [38, 48] [E]

*(Tightened to [38, 47] on 2026-10-20 — §18.7; to **[40, 45]** on
2026-10-25 — §18.9 Thm 7 CBB + §18.10 cleaned 45, both ends
solver-free; to **[41, 45]** on 2026-10-26 — §18.9 Thm 8 CBB hybrid t41
tree; and to **[42, 45]** on 2026-10-27 — §18.9 Thm 9 CBB hybrid t42
tree, LB 42 unconditional and solver-free.)*

The starved rerun could not be waited on: HiGHS's time limit is
wall-clock, and at 55% of a core the rerun would have expired before
reaching run 1's depth — a guaranteed second lost day. The grind moved
to a fresh, verified-empty 48-core remote box (the old box
kept as a free backup, never reached 48 (best bound 37.5564)).

Clean exit at 63601 s (~17.7 h) with `best_ckpt.json` on disk:
objective 48.000000000000036, dual bound 38.0, warm-start hint
consumed, checkpoint trail complete.

- [E] **48 is feasible, witnessed.** The banked vector was verified by
  `verify_best48.py` — an independent pure-Python recompute with no
  solver anywhere in the loop: the model rebuilt from scratch
  (m = 1500, T = 1124250, **177 rings** = all primes $p \le \lfloor\sqrt{T(m-1)}\rfloor = 1060$, up to $p = 1051$; using $\lfloor\sqrt{T(m)}\rfloor = 1061$ would admit a 178th ring $p = 1061$), every phase checked in range,
  48 nonzero phases counted, and all 1,124,250 ticks walked one by one:
  uncovered = 0. PASS.
- [E] **37 or fewer is impossible.** Dual bound 38.0 (better than run
  1's 37.5564 — the bound end also improved, which is what Phase B was
  built for). Not "we could not find one": no configuration, among any
  we did not try, covers m = 1500 with 37 phases.

The bracket tightened from §16.3's [26, 49] to **[38, 48]**, width 10,
and its upper end changed epistemic status: the incumbent is witnessed
on disk, not reported from a dead process. The wheel's covering number
at m = 1500 is now a fenced quantity — a certificate above, a proof
below — the structure §16.1 priced and §16.3 campaigned.

### 18.5 The hunt continues: 47 [S, in flight]

A 47-hunt launched 2026-10-20 12:39 HST on the same uncontended box
(seed 103, warm-started from the banked 48, 18 h budget): the solver
opens knowing 48 and spends the entire run hunting below it. Every
notch from either side — a 47, 46, … above, or 39, 40, … below — is
permanent and independently re-verified on harvest. The hunt is
expected to close its floor by ~01:39 HST 2026-10-21 (the 13 h mark of the 18 h budget); its result lands
in this section on arrival. If the two ends ever meet, d(1500) becomes
a proven exact integer at a scale where nobody has one.

→ *Landed 2026-10-20 22:43 HST — ahead of the box, by restricted-subspace
solve rather than B&B — and recorded in §18.7. The hunt continues for 46 and below on both sides. (The 46 fell 2026-10-23 with the banked 45 — §18.7 note; the certified floor reached 42 on 2026-10-27, §18.9.)*

### 18.6 The 48 decompressed: vector anatomy and local rigidity [F + E]

Banking the 48 made the vector itself available as an object of study
(`lab/phaseb_2026-10-19/anatomy_best48.py`, results in
`anatomy_best48_results.json`, 2026-10-20).

- [E] **The window holds P = 105 prime ticks**, so d/P = 48/105 = 0.4571 —
  the sub-1/2 descent of the native-schedule series (0.536 at m = 263 →
  0.451 at m = 1000) continues at m = 1500 *(extended 2026-10-27: the
  certified bracket puts d/P ∈ [42/105, 45/105] = [0.400, 0.429] — the descent steepens, and the d-law itself is refuted, §13)*. The 48 rings cannot be
  pairing primes off two at a time; the cover must be doing more per
  rotation. *(Correction 2026-10-20: the first anatomy pass reported
  P = 106, d/P = 0.4528 — its primality screen trial-divided only by
  primes ≤ B = ⌊√T(m−1)⌋ = 1060 [177 rings] and admitted the composite tick N = 1061² =
  1,125,721 (k = 1471), whose smallest factor exceeds B. The inflated
  H landed solely on ring 37, H = 6 → 5; its role and every other row
  are unchanged. ΣH below corrects to 109.)*
- [E] **Anatomy of the 48 rotated rings.** Each rotated ring p at phase c
  is scored by its prime harvest H (native-uncovered ticks it covers at
  c) and its collateral orphans O (composite ticks uniquely covered by p
  at home, hence exposed when p leaves c = 0). Partition: **20 Heavy
  Movers** (O > 0 — own collateral orphans), **16 Harvesters** (H ≥ 2, O = 0), **10
  Snipers** (H = 1, O = 0), and 2 Home-Patchers **113, 277** (H = 0, O = 0 —
  rotated solely to re-cover other movers' orphans; 113 alone patches 3
  orphan ticks; 397 rotates at H = 0 but carries O = 1 — a Heavy Mover per the JSON roles). Total harvest ΣH = 109 against 105 prime ticks.
- [E] **Mutual aid, zero slack.** The 20 movers orphan 42 composite
  ticks; every one is re-covered by another rotated ring (0 uncovered).
  Exhaustive scans of all 48 single-ring deletions (target 47) and all 45
  sniper-pair deletions (target 46) find **0 survivors**: the banked 48 is
  1-minimal. There are no clean guilds — the small rings absorb each
  other's collateral.

**The swap move that deletion testing pointed to [S → E].** A 1-out-0-in
deletion must break an irredundant cover; the candidate reduction move is
a 2-out-1-in swap among the zero-orphan rings. The one-second algebraic
test: a single home ring q can replace snipers A, B iff q divides
|k_A − k_B| (and orphans nothing itself). The scan found 28 candidate
pairs — every one with collateral (0 zero-collateral swaps; the q = 2
swap, the algebra's favorite, leaves 142 uncovered even ticks).

- [E] **Local Rigidity theorem (restricted subspace optimality).** The
  test was made decisive by solving the restricted MILP
  (`micro_swap47.py`): pin 40 of the 48 rotated rings at their
  banked phases and free the remaining 137-ring subspace (the 8
  zero-collateral rotated rings {263, 307, 419, 463, 467, 499, 521, 643} — 4 harvesters + 4 snipers per the anatomy roles — plus 129
  unrotated home rings). HiGHS returns **proven optimality at 8 free
  rotations — 40 + 8 = 48 total, 0.0% gap**. No rearrangement of the
  small-fry rings alone reaches 47.
- [F] **Why peripheral swaps die: the semiprime hyperedge mechanism.**
  Every composite tick N(k) = p·q in the layer is a hyperedge {p, q}
  over the wheel's rings: it stays covered at home iff at least one
  factor sits at c = 0. When 40 primes rotate away from home, a
  semiprime whose factor p rotated leaves q as its *sole remaining home
  cover*. A "zero-orphan" home ring is zero-orphan only at first order —
  rotating it off c = 0 abandons every such semiprime, producing
  second-order composite orphans no small-ring rearrangement can absorb.
- [F] **Consequence.** Deletion-LNS and peripheral swap-LNS are both
  closed as routes to 47. Any ≤ 47 solution must move at least one ring
  of the 40-ring heavy cluster — which is exactly what the global B&B of
  §18.5 is doing.

**Two MILP house laws** (earned by the failed first build; logged here so
the next model does not re-pay the tuition):

1. **Conditional home coverage.** A rotated ring *loses* its home-class
   free multiples: its home-tick coverage contribution is
   1 − Σ_{c ≠ 0} x_{q,c}, not a constant 1. Modeling it as a constant
   overstates coverage — the first build reported the warm-started 48 as
   infeasible (27 rows, e.g. tick 68) precisely because rotated rings'
   home classes were credited unconditionally. The same mechanism as the
   wheel itself: rotating a dial closes its home channel.
2. **Never clamp a negative RHS to 0 when rows carry negative
   coefficients.** With conditional coverage the true row RHS can be
   legitimately negative; clamping it to 0 makes every rotated ring's
   home-class loss infeasible and corrupts the model silently.

### 18.7 Breaking 48: the certified 47 [E]

2026-10-20, second working session on the banked 48. A 47-rotation
covering exists — `lab/phaseb_2026-10-19/best47_argon.json`, verified
solver-free by `verify_best47.py` (47 nonzero phases, 0 uncovered ticks).
The bracket closes to **d(1500) ∈ [38, 47]**.

*(Tightened to **[38, 45]** on 2026-10-23 — live B&B seed 105 banked
`best45_seed105_ckpt.json`, 45 nonzero phases, 0 uncovered, verified
solver-free by the same script; the 46-hunt question is settled, and the
45 settles that the Local Rigidity "heavy-cluster demolition" demand was
achievable, not hypothetical. Bracket finalized **[40, 45]** on
2026-10-25 — lower end then unconditional and solver-free via the CBB
tree, §18.9 Thm 7 — tightened to **[41, 45]** on 2026-10-26 via the
CBB hybrid t41 tree, §18.9 Thm 8 — and tightened to **[42, 45]** on
2026-10-27 via the CBB hybrid t42 tree, §18.9 Thm 9.)*

- [E] **The displacement is large.** Diffing the two verified witnesses
  (primary 48 vs 47): **34 of 177 ring positions change** (177 rings = primes $p \le \lfloor\sqrt{T(m-1)}\rfloor = 1060$). Nine rings
  stand down to home — including the home-bound 397 and 881 (Heavy Movers per the anatomy) — and eight
  previously unrotated rings are drafted (337, 347, 373, 389, 541, 569,
  593, 739). This is not the 48 with one dial turned; it is a different
  basin the deletion scans (§18.6) could never see, because every
  one-ring deletion of the 48 does break coverage.
- [E] **Only the O = 1 fringe of the heavy cluster moves.** Of the 48's
  20 collateral-bearing rings, 7 change position — four rephase in place
  (151, 179, 181, 193), three go home (397, 409, 881) — and every one of
  them had collateral O = 1. The high-collateral core (O ≥ 3: 19, 23, 37,
  43, …) holds its banked phases exactly. §18.6's stated consequence —
  any ≤ 47 must move at least one ring of the heavy cluster — survives,
  but the move is the cheapest possible membership of that class.
- [E] **The 48's sniper guild dissolves.** Of the eight zero-orphan
  snipers §18.6 pinned as the free subspace {263, 307, 419, 463, 467, 499,
  521, 643}, five stand down (419, 463, 467, 521, 643) and three rephase
  (263, 307, 499). The patcher class is eliminated outright: 113 and 277
  are promoted from H = 0 patch duty to genuine harvesters — verified
  H = 3 and H = 2 at their 47-phases. The refunded rotation is paid for
  by the periphery, exactly the region the anatomy flagged as
  load-bearing-but-cheap.
- [E] **Solver mechanisms that made 47 reachable** (Argon,
  2026-10-20 22:32 HST): (1) the T(m)^{1/4} = 32.57 phase-transition
  boundary plus the {2, 3, 5} harmonic LP smear (1/2 + 1/3 + 1/6 = 1 at LP
  cost 11/6 = 1.8333): pinning the small sub-$T^{1/4}$ primes home —
  single-pillar-rotation subspace MILP runs force cost ≥ 53..107
  [Tier 0 evidence, not certified] — collapses subspace MILP times from
  timeout to seconds; (2) unpinning p = 131
  together with all 35 H ≤ 2 rings solves to 47 in 6.08 s.
  (E1 errata, 2026-10-24: the then-believed "8 pillars p ≤ 31" are not
  all immovable — p = 19 rotates in the 48/47, p = 17 in the 46/45; the
  true immovable set across all four witnesses is {2,3,5,7,11,13,31}.)
- [E] **Disjoint Bipartite Subspace Rigidity at 47** (`demolition_47.py`).
  Pin the 8 apex rings (H ≥ 4) at their 47-phases, free the other 161 (the run home-locks the 8 pillars {2,3,5,7,11,13,17,31} — 8 pinned + 8 home + 161 free = 177):
  optimum exactly 47 (0.0 % gap). Independently pin the 15 clean O = 0
  harvesters (a set disjoint from the apex set; same 8 pillars home), free 154: optimum exactly
  47 (0.0 % gap). The 47 is as locally rigid as the 48 was — the new
  floor is a floor. Reproduced same day by Kimi: Cut II optimal in 51 s;
  Cut I optimal in 122 s once the 60 s limit was relaxed (at 60 s it sits
  on a knife-edge — treat narrow-limit "Optimal" claims on this model with
  a reproduction margin).
- [F] **Reading.** "Local rigidity" was always a statement about a phase
  vector, not about the covering number: the 48's vector is rigid in its
  137-ring neighborhood, and so is the 47's in its own. Between basins,
  d(1500) steps down by dissolving cheap-periphery structure and
  redistributing its cover onto freshly drafted rings. Each certified
  floor carries its own rigidity certificate; neither constrains where
  the next basin lies.

### 18.8 Standing lesson

Two vectorless artifacts, one mechanism: value existed only in process
memory, and process memory is not an archive. §18.2's
checkpoint-on-improvement rule is the fix, and this entry exists to
record that the fix was earned the expensive way — the 48 had to die
once unwitnessed before the pipeline treated disk as the only place a
solution exists.

### 18.9 Solver-free exact-integer dual certificates [F + E]

Up through §18.7, the upper bounds (48, 47 — and from 2026-10-23, 45) were certified by
solver-free integer scripts (`verify_best48.py`, `verify_best47.py`),
while the lower bounds and subspace rigidity proofs rested on HiGHS
floating-point branch-and-bound output (Tier-0 triage under the
campaign's certification standard). On 2026-10-21 (Argon), the dual side
was upgraded to the **exact same zero-solver, pure-stdlib integer trust
base** (`lab/phaseb_2026-10-19/verify_dual.py`, certificates in
`dual_certificates_m1500.json`).

- [F] **The Exact-Integer Dual Certificate Identity.** Fix any subset of
  rings $\mathcal{P}_{\text{fixed}}$ at phases $c_p \in \{0, 1, \dots, p-1\}$
  and let $\mathcal{P}_{\text{free}}$ be the remaining unpinned rings. For
  each tick $k \in \{1, \dots, m\}$ not covered by $\mathcal{P}_{\text{fixed}}$,
  let $F_{\text{free}}(k) = \{p \in \mathcal{P}_{\text{free}} : p \mid (T+k)\}$
  and $f_{\text{free}}(k) = |F_{\text{free}}(k)|$. Assign any non-negative
  integer weight $u_k \in \mathbb{Z}_{\ge 0}$ to each uncovered tick
  (with $u_k = 0$ on covered ticks), choose an integer scale $D > 0$
  ($D = 2520$), and define the residue-class load
  $W_p(c) = \sum_{k : (T+k) \equiv c \pmod p} u_k$. Because every valid
  integer cover $(c_p)$ satisfies
  $\sum_{p \in F_{\text{free}}(k)} (1 - y_p) + \sum_{p \in \mathcal{P}_{\text{free}} \setminus F_{\text{free}}(k)} x_{p, (T+k)\bmod p} \ge 1$
  and every binary indicator $y_p \in \{0, 1\}$ satisfies
  $D y_p + \max(0,\, \max_{1 \le c < p} W_p(c) - W_p(0) - D) \ge (W_p(c_p) - W_p(0)) y_p$,
  summing over $k = 1 \dots m$ yields the exact integer inequality:
  $$D \cdot |\{p : c_p \ne 0\}| \;\ge\; D \cdot |\{p \in \mathcal{P}_{\text{fixed}} : c_p \ne 0\}| + \sum_{k=1}^m (1 - f_{\text{free}}(k)) u_k - \sum_{p \in \mathcal{P}_{\text{free}}} \max\!\Bigl(0,\; \max_{1 \le c < p} W_p(c) - W_p(0) - D\Bigr).$$
  Because the rotation count $|\{p : c_p \ne 0\}|$ is an integer,
  ceiling division `(total_num + D - 1) // D` is a 100% solver-free
  lower bound verified using only Python `int` addition and integer
  division. *(2026-11-14: the identity itself — for arbitrary residue
  structure, weights, scale $D > 0$, and covers — is Lean-kernel-certified
  in `lean_wheel/LeanWheel/Dual.lean`, `Wheel.dual_certificate_identity`,
  with the solver-form `… // D` bound as `Wheel.dual_certificate_lb_floor`;
  the search trees remain computational, per
  `lean_wheel/FORMALIZATION_STATUS.md` §2.)*
- [E] **Nine Theorems Certified Solver-Free** (`verify_dual.py` PASS —
  items 1–6 below are the `verify_dual.py` originals, sub-second each; items 7–9 are the CBB trees (verifier 45–180 s after the search walls) via
  `cbb_verify.py`, and the three 45-era additions are recorded in
  §18.10):**
  1. **Unconditional 48-Rigidity on the 137-Ring Free Subspace (`PASS`, `LB = 48`):**
     Pinning 40 of the 48 rotated rings of `best48_primary.json`
     and **0 home rings** (137 free rings), a 2-branch exhaustive case
     split on $c_2 \in \{0, 1\}$ certifies $120618/2520 = 47.8643 \implies \mathbf{48}$
     on $c_2 = 0$ and $127367/2520 = 50.5425 \implies \mathbf{51}$ on
     $c_2 = 1$. The §18.6 Local Rigidity theorem is now solver-free
     certified.
  2. **Unconditional 47-Rigidity on the 143-Ring Free Subspace (`PASS`, `LB = 47`):**
     Pinning 34 rotated rings of `best47_argon.json` and **0 home rings**
     (143 free rings, including all 13 snipers and 130 home rings), a
     6-branch exhaustive partition on $(c_2, c_3) \in \{0,1\} \times \{0,1,2\}$
     certifies $118434/2520 = 46.9976 \implies \mathbf{47}$ on $(0,0)$
     and $\mathbf{66..71}$ on all 5 branches where $2$ or $3$ rotates.
  3. **Super-$T^{1/4}$ Mover Subspace Rigidity at 47 (`PASS`, `LB = 47`):**
     Pinning 18 rotated rings and the 8 sub-$T^{1/4}$ home pillars
     $\{2,3,5,7,11,13,17,31\}$ (151 free rings, unpinning 29 rotated
     rings), a single integer dual vector certifies
     $117220/2520 = 46.5159 \implies \mathbf{47}$.
  4. **Unconditional 47-Rigidity on the 159-Ring Free Subspace (`PASS`, `LB = 47`):**
     Pinning **only the 18 collateral-bearing Heavy Movers ($O_p > 0$)**
     of `best47_argon.json` and **0 home rings** (**159 free rings**:
     all 16 Clean Harvesters $H \ge 2, O=0$, all 13 Snipers $H=1, O=0$,
     and all 130 unrotated home rings), an exhaustive 30-branch
     Cartesian partition on $(c_2, c_3, c_5) \in \{0,1\} \times \{0,1,2\} \times \{0,1,2,3,4\}$
     certifies $116544/2520 = 46.2476 \implies \mathbf{47}$ on $(0,0,0)$
     and $\mathbf{55..65}$ across all 29 branches where $2, 3,$ or $5$
     rotates. (Two additional solver-free verified 47-witnesses from the
     live 46-hunt, `best47_witness2.json` and `best47_witness3.json`,
     confirm that the sole $H=1, O=1$ mover $p=739$ can return home
     $235 \to 0$ when zero-orphan ring $797 \to 426$ or $887 \to 277$
     snipes prime tick $k=743$, because $739$\x27s sole home multiple
     $k=1247$ is already covered as collateral by $p=19$.)
  5. **Regional Lower Bound $d(1500) \ge 39$ with $\{p \le 17\}$ Home (`PASS`, `LB = 39`):**
     With **0 rotated rings pinned** and only the 7 contiguous primes
     $p \le 17$ at home (170 free rings), a single integer dual vector
     certifies $98085/2520 = 38.9226 \implies \mathbf{39}$. **Regional,
     not global** (E2 errata, 2026-10-24): the canonical 45 has
     $c_{17} = 1$ and lies outside this region — do not quote LB 39 as
     unconditional.
  6. **Regional Lower Bound $d(1500) \ge 40$ with 8 Pillars Home (`PASS`, `LB = 40`) — SUPERSEDED:**
     With **0 rotated rings pinned** and the 8 sub-$T^{1/4}$ home pillars
     $\{2,3,5,7,11,13,17,31\}$ at home (169 free rings), a single
     integer dual vector certifies $99275/2520 = 39.3948 \implies \mathbf{40}$.
     Superseded by the §18.10 c₁₇-branched certificate (7 pillars home,
     c₁₇ free across 17 branches, 170 free rings): a strictly larger
     region that *contains* the canonical 45, at the same bound 40.
  7. **Unconditional Lower Bound $d(1500) \ge 40$ by Certified
     Branch-and-Bound (`PASS`, `LB = 40`) — 2026-10-25, supersedes the
     regional restriction [E]; SUPERSEDED by item 8 (LB 41,
     2026-10-26):**
     The CBB instrument (`lab/cbb/`: generator `cbb_gen.py`, independent
     verifier `cbb_verify.py`) searched the **full** configuration space
     — no pillar pinning — branching rings smallest-first and certifying
     leaves with the same §18.9 identity extended to forced (rotated,
     phase-free) rings. Emitted tree: `cbb_m1500_uncond_t40.json`,
     **3,370 leaves / 3,696 nodes / 2 h wall, verifier PASS in 45 s**
     (pure stdlib integers, zero solver trust). Every leaf certifies
     $\ge 40$; the tree's minimum is exactly $40$ on the all-pillars-home
     branch and $\ge 40$ (typically 41–43) on every pillar-rotated
     branch — the escape-chain prediction "rotating any pillar orphans
     many ticks, so those branches certify high fast" verified
     mechanically. The ladder that validated the instrument:
     $d(263)=15$ (13.5k leaves), $d(300)=16$ (59k), $d(400)=19$ (672),
     $d(600)=26$ (1,644 — the frozen decision gate, $10^6$-leaf budget
     untouched), then this rung. $d(1000)=37$ is **parked [G]**: at the
     exact-optimum boundary the search accumulates forced rings whose
     guaranteed rotations the §18.9 identity nets out of TotalNum
     — reproduced at scale 2026-10-26 (hybrid t37 run: 197k nodes /
     24,906 certifying leaves / **82,819 deficit leaves**, best leaf
     bound 36 vs target 37, depth $\sim$121 binary splits on large
     primes). The named next mechanism lever is forced-ring
     phase-resolution splitting; the sharpest next probe is exact MILP
     on a sample of the fully-determined deficit leaves (distinguishes
     "identity under-certifies" from "a real 36-configuration exists")
     *(resolved 2026-10-28, CBB Blitz Lane C [E]: `m1000_deficit_probe`
     solved $50/50$ sampled deficit leaves in 17.8 s MILP — $49$ feasible
     at $\ge 37$, $1$ infeasible, $0$ timeouts, $0$ below $37 \implies$
     `identity_under_certifies`, `refutes_d1000_ge_37 = false`; the
     parked [G] closes)*.
  8. **Unconditional Lower Bound $d(1500) \ge 41$ by Certified
     Branch-and-Bound (`PASS`, `LB = 41`) — 2026-10-26, supersedes
     item 7 [E]:**
     The CBB hybrid engine (allowed-phase-set identity + exclusions +
     tick-branch nodes + forced rings, `format: cbb-hybrid-v2`),
     re-vectorized for the campaign (exact-int64 numpy twins of every
     per-node loop, `cbb_fast.py`, commit `2c07dc6` — bound math
     bit-identical to the reference paths, frozen gates m263/m600
     byte-reproduced), closed target 41 at $m = 1500$: emitted tree
     `cbb_m1500_hybrid_t41_np.json`, **5,948 leaves / 6,466 nodes /
     4 h 15 m wall, verifier PASS in 80 s** (pure stdlib integers, zero
     solver trust; the solver float LP's 41.0 bound is now
     integer-certified). The certified bracket on $d(1500)$ tightens to
     $[41, 45]$, both ends solver-free. Zero deficit leaves: the
     forced-ring blindness that parks $d(1000)$ did not bite at
     $m = 1500$ target 41.
  9. **Unconditional Lower Bound $d(1500) \ge 42$ by Certified
     Branch-and-Bound (`PASS`, `LB = 42`) — 2026-10-27, supersedes
     item 8 [E]:**
     The first campaign tree of the fixed-ascent engine (propose_ascent
     `ep=None` repair, commit `4979ac2` — the latent TypeError of item 8's
     engine was real but never load-bearing in banked trees; the t41
     record stands), closed target 42 at $m = 1500$:
     `cbb_m1500_hybrid_t42_np.json`, **13,740 leaves / 14,770 nodes /
     9 h 31 m wall, verifier PASS in 180 s** (pure stdlib integers, zero
     solver trust). The certified bracket on $d(1500)$ tightens to
     $[42, 45]$, both ends solver-free. Zero deficit leaves again: the
     forced-ring blindness that parks $d(1000)$ did not bite at target
     42 either.

### 18.10 The 45 decompressed: the Apex Engine Swap, and rigidity at 45 [E]

2026-10-23 (Argon anatomy; independently re-verified by Kimi,
2026-10-24). The 46-hunt banked the whole descent chain, not just its
endpoint: four verified witnesses 48 → 47 → 46 → 45 (`verify_best47.py`
PASS on each, 0 uncovered ticks). Decompressed, the chain is one named
mechanism.

- [E] **The Apex Engine Swap.** The 48 and 47 are powered at the apex by
  p = 19 (c = 16, H = 7, O_1 = 7, plus 3 mutual semiprime orphans healed
  — Net +3). The 46 and 45 retire p = 19 to home and draft p = 17
  (phase 1), whose residue class heals 7 first-order orphans plus 3
  mutual orphans the retirement abandons. 55 of 177 rings (177 rings = primes $p \le \lfloor\sqrt{T(m-1)}\rfloor = 1060$; $\lfloor\sqrt{T(m)}\rfloor = 1061$ would add 1061) change role
  across the swap — including 7/8 of the §18.7 Cut I-A8 apex set and 14/15 of Cut
  II-B15. This is exactly the heavy-cluster demolition Local Rigidity
  said any ≤ 47 would have to perform: the prediction and the escape are
  the same object.
- [E] **The chain in numbers** (`demolition_45.py` §1): p17 phase
  0, 0, 1, 1 and p19 phase 16, 16, 0, 0 across 48, 47, 46, 45; orphan
  totals 47, 46, 47, 49 — and 44 in the cleaned 45
  (`best45_argon_clean.json`, which eliminates patcher 149 and the
  23↔409 orphan cycle; 45 nonzero phases, 0 uncovered, verify PASS;
  now the canonical 45).
- [E] **Disjoint Bipartite Rigidity at 45** (`demolition_45.py` §2,
  Kimi-reproduced 2026-10-24, 0.0 % gap): pin the 9 apex Heavy Movers,
  161 free → optimum exactly 45 (6.7 s); pin 10, 160 free → exactly 45
  (11.7 s); independently pin the 15 clean O = 0 harvesters, 155 free,
  a set disjoint from the apex set → exactly 45 (44.7 s). *(All three runs home-lock the 7 immovable pillars {2,3,5,7,11,13,31} — 9+161 = 10+160 = 15+155 = 170 = 177 − 7; demolition_45.py `home_pillars`.)* Each certified
  floor carries its own rigidity certificate, and the certificates keep
  agreeing with the banked vector: the 45 is as locally rigid as the 48
  and the 47.
- [E] **The dual side keeps pace.** `verify_dual.py` now reports OVERALL
  PASS on **nine** theorems (< 1 s, zero-solver, pure integer): the three
  added with the 45 (dual-side certificates — the 161/160/155-free figures above are the `demolition_45.py` MILP rigidity runs, same pinned sets, different instruments) are `rigidity_45_unconditional_144free` (LB 45),
  `rigidity_45_unconditional_155free` (LB 45), and
  `global_lb40_pillars7_c17_branched_170free` — seven pillars home with
  an exhaustive 17-branch split on c₁₇, every branch certifying ≥ 40
  (two branches certify ≥ 41).
- [F] **Bracket consequence (E1 errata, 2026-10-24; P1 upgrade,
  2026-10-25; tightened 2026-10-26; tightened 2026-10-27).** Upper
  bound 45 [E, solver-free witness]. The lower bound is
  **unconditional and solver-free**: d(1500) ≥ 42 [E, 2026-10-27,
  CBB hybrid t42 tree — `lab/cbb/cbb_m1500_hybrid_t42_np.json`,
  13,740 leaves / 14,770 nodes, 9 h 31 m to generate, 180 s to verify
  in pure-stdlib integer arithmetic, zero solver trust — the first
  campaign tree of the fixed-ascent engine, commit `4979ac2`]. The
  predecessors LB 41 (§18.9 Thm 8, 5,948-leaf t41 tree, 2026-10-26 —
  the first integer certification of the solver float LP's 41.0
  bound) and LB 40 (item 7, 3,370-leaf tree, 2026-10-25) are retained
  as history. The regional predecessors are retained as history: LB 40
  on the pillar-home region (verify_dual.py certificate
  `global_lb40_pillars7_c17_branched_170free`, the ninth banked
  theorem, superseding §18.9 Thm 6 which pinned c₁₇ = 0 and is
  retired), and the weaker LB 39 on {2,3,5,7,11,13,17} home (§18.9 Thm
  5 — retired as a *global* claim, since the canonical 45 has c₁₇ = 1).
  "Every minimum cover occupies the pillar-home region" is supported by
  subspace-MILP runs only [Tier 0], and is now *moot* for the public
  bracket: the CBB trees certify ≥ 42 over the full configuration
  space. The true immovable set across all four banked witnesses is
  {2,3,5,7,11,13,31}: p = 19 rotates in the 48/47 (c = 16) and p = 17
  rotates in the 46/45 (c = 1). Honest public statement:
  **d(1500) ≤ 45 [E, solver-free]; d(1500) ≥ 42 [E, solver-free,
  unconditional, CBB-verified 2026-10-27]; solver float LP lower bound
  41.0 [E, HiGHS] — integer-certified by the t41 tree, superseded by
  the t42 tree.**
  The 46-hunt closed with no 44 in 583,900 combined nodes: **≤ 44 is
  open [G]**. The target-42 rung closed 2026-10-27 (9 h 31 m, §18.9
  Thm 9; the float dual does not preclude 43): the next levers are a
  CBB target-43 run at $m = 1500$ or a fresh, deeper hunt.

### 18.11 The 2026-10-28 Structural Ledger: Fock/SU(2) Multiplets, L4 Lattice Dissolution (5 for 5), Unpriced-vs-Priced Φ, C1/C2, and the L3 Ring-Role Audit [F + E]

2026-10-28 (Obi, Claude, Argon, GPT, GLM, Kimi). Five structural audits
completed in a single multi-model pass (`INSIGHTS.md` 2026-10-28;
`lab/l4_probe.py`, `lab/l4_wipe_phi_probe.py`):

1. **Wheel laps are two-oscillator Fock diagonals and $SU(2)$ multiplets
   [F + E, textbook: Pauli 1926, Fock 1935, Haxel–Jensen–Suess 1949,
   Goeppert-Mayer 1949, Schwinger 1952].**
   - *Fock lattice bijection [F]:* Tick $(m, k)$ ($1 \le k \le m$)
     corresponds to sharing $N = m - 1$ quanta between two bosonic
     oscillators as $(n_a, n_b) = (k - 1, m - k)$. With Cantor pairing
     $\pi(x, y) = \frac{(x+y)(x+y+1)}{2} + y$, the wheel's integer address
     is $n(n_a, n_b) = \pi(n_b, n_a) + 1 = T(m-1) + k$: **the wheel is the
     two-oscillator Fock lattice counted diagonal by diagonal.** Raising
     operators step between laps via $a^\dagger : n \mapsto n + m + 1$
     ($(m, k) \mapsto (m+1, k+1)$) and $b^\dagger : n \mapsto n + m$
     ($(m, k) \mapsto (m+1, k)$).
   - *Schwinger $SU(2)$ multiplets & unique rotor tuning [F + E]:* By
     Schwinger's two-oscillator construction ($j = (n_a + n_b)/2 = (m-1)/2$,
     $m_z = (n_a - n_b)/2 = k - (m+1)/2$), lap $m$ is the angular-momentum
     multiplet of spin $j = (m-1)/2$ with $2j + 1 = m$ states: odd laps
     ($m = 1, 3, 5, \dots$) have integer $j$ and a center tick ($m_z = 0$);
     even laps ($m = 2, 4, 6, \dots$) have half-integer $j$ and no center
     tick (lap 2 has the two-state $j = 1/2$ doublet structure). Since
     $2j(j+1) + m_z + 1 = \frac{(m-1)(m+1)}{2} + k - \frac{m+1}{2} + 1 = T(m-1) + k$,
     the operator $\hat{A} = 2\mathbf{J}^2 + J_z + I$ on the full Schwinger
     space has the positive integers in exact wheel order as its spectrum,
     with intra-lap ladder relations $[\hat{A}, J_\pm] = \pm J_\pm$ ($J_+$
     annihilates $k = m$, $J_-$ annihilates $k = 1$). For a general
     rotor-plus-field spectrum $E = a\,j(j+1) + b\,m_z$, intra-lap spacing
     is $b$ while the inter-lap gap from $(j, +j)$ to $(j+1/2, -j-1/2)$ is
     $a(j + 3/4) - b(2j + 1/2)$; equating this to $b$ for all $j$ gives
     $a(j + 3/4) = 2b(j + 3/4) \implies \mathbf{b/a = 1/2}$ **uniquely**
     up to overall scale. *(2026-11-14: gap formula and tuning theorem are
     Lean-kernel-certified in `lean_wheel/LeanWheel/Rotor.lean`,
     `Wheel.rotor_inter_lap_gap` + `Wheel.schwinger_rotor_tuning`, with
     the $\hat{A}$ spectrum glue as `Wheel.wheel_spectrum_glue`.)*
   - *Atomic ($2n^2$) and nuclear magic numbers (`2, 8, 20, 28, 50, 82, 126`) [F + E]:*
     Hydrogen shell $n$ carries hidden $SO(4) \cong SU(2) \times SU(2)$
     symmetry [Pauli 1926, Fock 1935] with $j_L = j_R = (n-1)/2$, giving
     $\text{lap}(n) \times \text{lap}(n) \times \text{lap}(2) = 2n^2$ states,
     matching the wheel's half-turn spoke value $T(2n-1) + n = 2n^2$ (one
     full odd lap $2n-1$ plus the two flanking half even-laps $(n-1) + n = 2n-1$).
     In the 3D isotropic nuclear harmonic oscillator, shell $N$ holds
     $T(N+1)$ spatial states ($\times 2$ spin $\to 2, 8, 20, 40, 70, 112$
     cumulative), and the Haxel–Jensen–Suess / Goeppert-Mayer (1949)
     spin-orbit intruder level $j = N + 3/2$ from shell $N+1$ adds
     $2j + 1 = 2(N+2)$ states — literally **one even wheel lap $m = 2(N+2)$**
     dropping down to produce $20 + 8 = 28$, $40 + 10 = 50$, $70 + 12 = 82$,
     and $112 + 14 = 126$. *Scope guard [F]:* this link lives strictly in
     the wheel's **lap counting geometry** (which counts what $SU(2)$
     counts), not in the prime sieve.

2. **L4 Lattice-Ray Probe — The Dissolution Streak Reaches 5 for 5
   (`lab/l4_probe.py`, `lab/l4_results.json`) [F + E].**
   - *Ray polynomials & exact discriminant [F]:* A linear ray
     $(n_a, n_b) = (a_0 + u t, b_0 + v t)$ ($u + v \ne 0$) in the Fock
     lattice induces the quadratic polynomial $2n(t) = A t^2 + B t + C$
     with $A = (u+v)^2$, $B = (u+v)(2a_0 + 2b_0 + 1) + 2u$, $C = 2n(a_0, b_0)$,
     and exact discriminant
     $$\Delta = (u - v)^2 - 8(u + v)(v a_0 - u b_0 + v).$$
     For $(1,1)$ diagonals ($u = v = 1$, $d = n_a - n_b$), $N = (m^2 + d + 1)/2$
     and $\Delta = -16(d + 1)$: every diagonal has constant parity
     ($d \equiv 2, 3 \pmod 4$ all even and dead, containing all square-$\Delta$
     diagonals $d = -1 - s^2$ where $N = (m-s)(m+s)/2$; $d \equiv 0, 1 \pmod 4$
     all odd with $2.00\times$ parity factor, where $d = 0$ traces the odd-lap
     centers $j^2 + (j+1)^2$). *Norm-form note [F]:* live vs. dead is
     determined strictly by square discriminant ($\Delta = \square$,
     reducible) or a fixed prime divisor ($\omega_p = p$, computed mod 4 at
     $p = 2$ since odd-slope rays $u+v \equiv 1 \pmod 2$ have period-4
     parity), *not* by whether $\Delta$ is a fundamental discriminant
     (counterexample: the $(1,1)$ diagonal $d = 8$, $n(t) = 2t^2 + 18t + 45$,
     has non-fundamental $\Delta = -36$ and is live, producing primes
     $89, 149, 269, \dots$; likewise $d = 17, 24$).
   - *Pre-registered census & results [E]:* Across slopes
     $(u, v) \in \{(1,1), (1,2), (2,1), (1,3)\}$ and shift-canonical bases in
     $[0, 20]^2$, the committed family reproduces to the unit: **201 live
     single rays**, 5,691 same-slope pairs, 2,317 jointly dead pairs, and
     **3,374 live pairs** (3,575 scored tests = 201 singles + 3,374 pairs; jointly dead pairs carry no z-score), benchmarked against 200
     shuffled out-of-grid control rays (3,238 live control pairs) across
     disjoint decades $W_1 = (10^3, 10^4]$ and $W_2 = (10^4, 10^5]$.
     *(Instrument repair logged [F + E]: the draft §1.3b item 9 formula for
     $C_{\text{HL2}}$ at $p = 2$ wrote $(1 - |U|/4)/(1 - 1/2)$, omitting the
     2-tuple exponent $2$ on $(1 - 1/2)^2$ from §1.3 Null B and halving
     Null B on every pair; restoring $(1 - |U|/4)/(1 - 1/2)^2$ eliminates
     the artificial $2\times$ offset.)*
     All three sanity controls pass (`d = 0` diagonal obs/Null A $= 1.0046$ in $W_1$, $0.9926$ in $W_2$; all 21 live $(1,1)$ diagonals in $[0.9858, 1.0105]$; fixed-$n_a$ columns $k \in \{1,2,3,5,7\}$ in $[0.9923, 1.0111]$; all 43 dead single rays (the dead-ray class) yield **0 primes** for $t > 2$).
     Across all 3,575 tests:
     - **201 live singles:** $W_1$ mean $z = +0.013$ ($\text{sd } 0.642$, $\max |z| = 1.79$), $W_2$ mean $z = +0.017$ ($\text{sd } 0.604$, $\max |z| = 1.71$), max joint same-sign $\min(|z_{w1}|, |z_{w2}|) = \mathbf{0.95}$ (vs. control ceiling $1.02$).
     - **3,374 live pairs:** $W_1$ mean $z = +0.022$ ($\text{sd } 0.877$, $\max |z| = 3.48$), $W_2$ mean $z = +0.013$ ($\text{sd } 0.874$, $\max |z| = 3.20$), max joint same-sign $\min(|z_{w1}|, |z_{w2}|) = \mathbf{2.17}$ (vs. control ceiling $1.95$ and pre-registered threshold $3.5$).
     - **Outliers passing $|z| > 3.5$ in both decades:** **0** (and **0** even in the $[2.5, 3.5]$ gray zone across both decades; single-decade $|z| > 2.5$ counts are $12$ in $W_1$ and $15$ in $W_2$ vs. uncorrelated binomial $44.3$).
     - **Verdict [E, heuristic consistency with BH/HL]:** **L4 dissolves
       (5 for 5 on the value side).** Closed with reopen condition:
       *non-linear paths in the $(n_a, n_b)$ lattice*.

3. **C1 (Odd-Lap vs. Even-Lap Goldbach Windows) and C2 (Rows vs. Columns) [F + E].**
   - *C1 [F + E]:* Full-lap reflection $k \leftrightarrow m + 1 - k$
     (oscillator swap $n_a \leftrightarrow n_b$) pairs values summing to
     $m^2 + 1$; together with B7's seat reflection $k \leftrightarrow m - k$
     (sum $m^2$), the two reflections one tick apart generate $D_\infty$ on
     $\mathbb{Z}$, while on a finite lap each $m \ge 3$ has **exactly one**
     non-trivial Goldbach window: $2n = m^2$ on even laps and $2n = m^2 + 1$
     on odd laps (0 odd-lap B7 pairs and 0 even-lap $m^2+1$ pairs through
     $m = 2999$ [E]). Across laps $3 \le m \le 2999$, odd laps yield **8,464**
     prime pairs (first at $m = 17$: $139 + 151 = 290$; excluding 324 prime
     odd-lap self-paired centers $j^2 + (j+1)^2$) *(counts: `lab/PHASE22_parity_census.py`; the even-lap reference 11,085 is printed in-source)* vs. **11,085** on even laps
     $m \le 2998$ (lap $3000$ adds $29$). The observed odd/even ratio
     $8464 / 11085 = \mathbf{0.7636}$ matches the weighted Hardy–Littlewood
     prediction **0.7722** ($1.1\sigma$): the deficit comes entirely from
     primes $p \equiv 3 \pmod 4$, which can divide $m$ (boosting even-lap
     singular series) but never divide $m^2 + 1$. *(Note: for odd $m > 1$,
     $m^2 + 1$ is even, so odd-lap windows do not test Landau's $n^2 + 1$
     prime problem.)*
   - *C2 [F]:* Fixed-$n_b = c$ rows give $N = T(m) - c$ with discriminant
     $\Delta = 1 + 8c > 0$ (real-quadratic wing; Δ here is the row's form discriminant — local notation, not the §19.1 ray discriminant Δ_k), forming a single parabola
     across the seam ($k \mapsto -k$) with the fixed-$n_a = k - 1$ columns
     ($\Delta = 1 - 8k < 0$, Heegner imaginary-quadratic wing).

4. **§2b Unpriced-vs-Priced Reflection Involution $\Phi$ Reconciled
   (`lab/l4_wipe_phi_probe.py`, `lab/l4_wipe_phi_results.json`) [F + E].**
   - *Two involutions matched to their tick sets [F]:* On interior seats
     $k \in \{1, \dots, m-1\}$, $k \leftrightarrow m - k$ induces
     $\Phi_{\text{seat}}(d)_p = (m^2 - d_p) \bmod p$; on the full lap
     $k \in \{1, \dots, m\}$, $k \leftrightarrow m + 1 - k$ induces
     $\Phi_{\text{full}}(d)_p = (m^2 + 1 - d_p) \bmod p$.
   - *Why reflection cuts are killed on the priced CBB tree [F + E]:* In the
     priced covering game, only home phase $c_p = 0$ is free. At $m = 1500$,
     $m^2 + 1 = 2,250,001 = 13 \times 17 \times 10181$, so $\Phi_{\text{full}}$
     preserves the free phase on **only 2 of 177 rings (`13` and `17`)**,
     breaking cost invariance on **175 of 177 rings** (and $\Phi_{\text{seat}}$
     preserves it only for $p \mid 1500 \in \{2, 3, 5\}$, breaking **174 of
     177 rings**). Applied to the canonical 45-witness `best45_argon_clean.json`
     (priced cost **45**, uncovered **0**), $\Phi_{\text{full}}$ preserves
     feasibility (**0 uncovered ticks**) while blowing up the priced rotation
     bill from **45 to 176 out of 177 rings** (and $\Phi_{\text{seat}}$ blows
     it up to **173**).
   - *Why $\Phi$ works on the unpriced Jacobsthal wipe oracle [E]:* When
     phase choice is unpriced and the objective is ring cardinality, $\Phi$
     is an exact $\mathbb{Z}/2$ symmetry: across 2,000 random trials (`0`
     mismatches), fixed-point fraction is **0.0** (ring 2 flips
     $d_2 \mapsto 1 - d_2$ whenever the mirror sum is odd), minimum-cardinality
     solutions pair at rate **1.000**, and adding the canonical cut
     $d \le_{\text{lex}} \Phi(d)$ halves feasible solution counts (`4 → 2` at
     $m = 20$, `2 → 1` at $m = 21$) with a **1.60× – 2.00× B&B node
     speedup**.

5. **L3 Ring-Role Table Audit — Ring 2 Parity Is the Unique Multi-Role
   Mechanism [F + E].**
   Auditing every citation of small primes $p \in \{2, 3, 5, 7, 11, 13\}$
   across §15.7, §17.1–§17.5, §18.11, and §19.4 confirms the frozen
   prediction:
   - **Ring $p = 2$ (unique multi-role ring — all roles reduce to parity / the $\frac{1}{2}$ denominator in $T(m) = \frac{m(m+1)}{2}$):**
     (i) period-4 stagger `0, 1, 1, 0` (whereas every odd prime $p$ has
     stagger period $p$); (ii) period-4 parity of odd-slope lattice rays
     ($u + v \equiv 1 \pmod 2$) and constant parity of $(1,1)$ diagonals;
     (iii) zero fixed points under $\Phi$ whenever the mirror sum is odd;
     (iv) parity locking of primorial flanks (§17.3).
   - **Odd small primes ($p = 3, 5, 7, 11, 13$) — single-role boundary witnesses of uniform laws:**
     $p = 3$ in §15.7 (`Echo Cascade`) is the unique prime where $2p - 1 = 5$
     and $2p + 1 = 7$ are both prime because for $p > 3$, $3 \mid (2p-1)(2p+1)$;
     $p = 5$ in §19.4 completes the smallest Egyptian fraction
     $\frac{1}{2} + \frac{1}{3} + \frac{1}{6} = 1$ and in §17.5 is the first
     skipped prime in the non-consecutive bag walk; $p = 13$ in §17.2 is the
     first fresh ring ($13^2 = 169 \le T(18) = 171 < T(19) = 190$) that opens
     layer 19 after the $m = 2\dots 18$ infeasible block. None of the odd
     primes carries a separate multi-role mechanism.

---

### 18.12 The Erdős #7 certificate era (2026-10-24 → 30): capacity, forest, and the five-million-to-billion scan [F + E]

Erdős problem #7 asks for a covering system with all distinct odd moduli (or a
proof that none exists). Six days crossed three certificate generations, each
dissolving the previous generation's ceiling without solver trust. Every step
below was cold-audited by an independent agent re-deriving from the
mathematics alone; both audits PASS.

**Generation 1 — CRT exclusion ladder [E, 10-24].**
`verify_erdos7_crt.py` certifies all 992 ladder rungs infeasible in 1 s by
exact uncovered-residue counting (min 769 uncovered at N = 10395): every odd
N < 675,675 excluded, 67.5× past Mian's 10,000.

**Generation 2 — unit-capacity criterion [F → E, cold-audited 10-29].**
Reduction chain, each connector audited [F]: a distinct-odd covering exists
⟺ some odd L has its full divisor wheel set covering ℤ (adding wheels cannot
destroy coverage; divisors are distinct, odd, > 1); the mask is L-periodic;
prime wheels normalize to phase 0 by CRT and cover exactly the nonunits, so
composite wheels must cover all φ(L) units; a composite wheel m covers at
most φ(L)/φ(m) units (equal-fiber CRT count, verified on prime powers).
*(2026-11-14: the equal-fiber count — fiber·φ(m) = φ(L) for coprime
classes, ≤ in general, and the covering necessity Σ φ(L)/φ(m) ≥ φ(L) — is
Lean-kernel-certified in `lean_wheel/LeanWheel/ErdosFiber.lean`,
`Wheel.erdos_fiber_coprime` / `Wheel.erdos_fiber_le` /
`Wheel.erdos_covering_necessary`.)*
Necessary condition:

S(L) = Σ_{m | L, m composite} 1/φ(m) ≥ 1   ⟺   C(L) = φ(L)·S(L) ≥ φ(L).

Two independent scans to 5·10⁶ (φ-sieve accumulation and SPF exact-rational
formula) find exactly nine odd survivors; at the unique ≤ 10⁶ survivor
675675 the wheels 9, 25, 35 force D ≥ 3960 duplicate unit marks > surplus
3286, certifying it ineligible (direct enumeration over all 259,200 units for
representative phase triples: D ∈ {3960, 5760} only — the WLOG unit-phase
reduction is valid for the impossibility direction). Sole-survivor status and
the collision certificate reproduce exactly under independent re-derivation.
Instrument resonance observed [F-flavored]: the CRT recurrence — a different
instrument, no phase normalization — loses traction (u_min = the instrument's minimum-uncovered statistic; 0 here) at exactly
the signatures where C(L) ≥ φ(L).

**Generation 3 — max-forest certificate [F + E, cold-audited 10-30].**
A maximum-weight spanning forest over the wheel-intersection graph sharpens
the union bound (the complement form of the classical Hunter–Worsley
tree-Bonferroni bound with Maurer's 1983 bivalent-forest extension:
the shape is [E] classical; the CRT-exact covering instantiation is
the new content). Covering requires forest debt ≤ surplus,
so H = F − surplus ≥ 0 certifies noncovering. The 5M scan's forest bounds,
with a verified 15-edge hand certificate at 2,027,025 (debt 36,324 >
surplus 35,884, H ≥ 440), settled every odd L < 4,729,725 solver-free. The
bound is ≤ exact and tight on all 66 published OEIS values — the conjectured
identity u(M) = U − C + F_max (U = total unit marks Σ φ(L)/φ(m); C = capacity φ(L)) carries 66/66 evidence (extension probe
n = 65…1000 ended with the 2026-11 fleet compute exit, final status
unrecorded — the 66/66 evidence stands as of the probe's last checkpoint). The unsound cyclic all-pairs variant would falsely
certify exactly at 4,729,725, where the sound forest stays inconclusive: the
soundness warning is load-bearing, verified.

**The billion-scale scan [E, 10-30].** The fleet scan of all odd L in
(5·10⁶, 10⁹] completed 100/100 shards with zero errors: **3,355 capacity
survivors; 2,314 certified noncovering** by the forest bound; **1,041
forest-inconclusive** (smallest 6,891,885, H = −4,385). Cold-verify PASS: 25
survivors re-derived locally on an independent code path — φ, C, forest
weight, edge counts, and internal identities reproduce exactly. **Settled
line [F from E parts]: every odd L < 6,891,885 is settled solver-free —
capacity-infeasible or forest-certified — except 4,729,725** (inconclusive by
20,152). The debt-hunt annealer harvest (10-30; ~1.05 B moves × 8 seeds over
full 12 h walls, plus a ~77 M-move second attempt with zero improvement;
cold-audit PASS) found **no covering**: min D sits in the certified band
**[118,108, 442,687]** — a 3.2× plateau above the 138,260 covering line, the
annealer saturated. Suggestive of noncovering; does not settle the rung. Survivors
are smoothness-driven (~13–40 per 10M decade, roughly flat after 20M) —
consistent with C ≥ φ being a divisibility-dense condition; a matched-density
random-odd null crosses the screen with probability < 10⁻⁴ (the sieve
argument of the capacity audit).

**Standing [G].** (i) 4,729,725 — the one unsettled modulus below the line;
debt-hunt harvested with the annealer saturated (band [118,108, 442,687];
reopens only via a smarter covering-side encoding, or strata/collision
certificates proving D ≥ 138,261 for every assignment); (ii) the 1,041 inconclusive — any distinct-odd covering
with lcm ≤ 10⁹ hides only among these; the load-bearing next layer is
hypergraph-strata / phase-compatibility sharpening of the forest bound;
(iii) capacity alone can never close the universal conjecture (squarefree
primorials cross surplus ≥ 1 near 10¹⁹) — collision debt is the real wall.
Literature [E, external novelty audit 2026-11-14]: Erdős #7 remains
open. Published solver record: McNew–Setty (arXiv:2507.23041, v2
2026-02) determine every covering number < 10⁶ except the even 773,500
by MIP. *Same-day correction (verified against the v1 and v2 full
texts):* their line reaches 10⁶, so our solver-free settled line at
6,891,885 with one exception **extends the published line ≈ 6.9×** —
the audit's first pass had the comparison inverted. The settled line's
honest distinction is *solver-free, human-auditable certificates* plus
the billion-scale survivor census (the census itself is the genuinely
new object, not the line). The
capacity criterion was not found in accessible literature (Mian–Siddique,
arXiv:2607.25628, hold a weaker CRT-capacity certificate that stalls at
10⁴; novelty plausible, [S] until a specialist check AND until the
Öztürk-cluster full texts are in hand). Öztürk (Aug-2026 preprint,
ResearchGate-only, DOI 10.13140/RG.2.2.13216.55049, no arXiv record,
unrefereed, **unverified**) claims no distinct-odd covering has lcm
below 11,486,475 (i.e., lcm ≥ 11,486,475 — a transcription correction:
"below", not ">") — stronger, since it covers our exception 4,729,725,
and notably 11,486,475 itself sits in our inconclusive list. Two
companion RG-only preprints (a symmetry-reduced decision procedure,
Aug 18; a squarefree-moduli constant reduction, Aug 23) complete a
cluster this survey had not mapped. No record claim until a proof is in
hand; obtaining the full texts is now the highest-value literature
action.

**Correction 2026-11-16 (post-release; appended, nothing deleted).** Late
prior-art sweep, logged in INSIGHTS.md (Addendum 36).
Labels here: [E] recomputed by us; [S] as stated by the source, not rebuilt by us.

1. **Capacity criterion (Generation 2).** [E] The formula
   S(L) = Σ_{m | L, m composite} 1/φ(m) ≥ 1 is identical to the "φ-certificate" of
   ref. 41 (committed 2026-11-02; ours cold-audited 2026-10-29). [S] Per ref. 41's
   notes the same argument is Schroeder's squarefree corollary (ref. 40) and the
   same sieve family as Hackmon (ref. 39). Independent rediscovery; the
   "novelty plausible" reading above is withdrawn.
2. **The exception 4,729,725.** [E] Excluded by the tower certificate of ref. 41:
   T(4,729,725) = 0.9912 < 1 (own recomputation, exact rationals, `cert_check.py`;
   the same code gives T(6,891,885) = 1.0098, matching ref. 41's stated first
   failure). Settled, by a certificate that is not ours.
3. **Settled line.** [S] Passed: Öztürk at 11,486,475 (ref. 32, 2026-08), ref. 41 at
   1,527,701,175 (2026-11-02), Schroeder's claim at 9,704,539,845 (ref. 40, 2026-09).
   "Extends the published line ≈ 6.9×" is withdrawn as a frontier statement. What
   remains true: every odd L < 6,891,885 except one was settled here by
   solver-free certificates of our own construction.
4. **The 1,041 forest-inconclusive L.** [F] All lie at or below 10⁹, hence below
   1,527,701,175. If ref. 41's theorem stands, none of them is the lcm of an odd
   distinct covering, and Standing (ii) is closed from outside.
5. **Max-forest certificate (Generation 3).** [F] A different second-order
   certificate from the distortion (ref. 41) and inclusion–exclusion (ref. 30)
   routes; ours as a method. As a bound it is weaker: it is inconclusive at
   4,729,725, where the tower certificate succeeds.
6. **Conjectured identity u(M) = U − C + F_max.** [G] To be re-checked at
   L = 4,729,725 and L = 6,891,885 against the fact (items 2–3) that no covering
   exists there; the 66/66 evidence is on small M only. *(Closed 2026-11-17 —
   refuted as an exact identity at both scheduled loci; printed formula also
   transposed against these parentheticals. See Correction 2026-11-17 item 8.)*
7. **Coincidence of walls.** [E] Our instruments stalled at 675,675 and 6,891,885;
   ref. 41 reports its φ- and tower certificates first failing at the same two
   numbers. Same structure, reached independently, not reached first.

**Correction 2026-11-17 (post-release; appended, nothing deleted).**
Cross-model audit (carbon, relayed by obi) + independent in-window
verification, `lab/probes/carbon_audit_verify_2026-11-17.py` (zero project
imports; re-derived math). Logged in INSIGHTS.md Addendum 39.

8. **Standing (6) — CLOSED; the conjectured identity is REFUTED as an exact
   identity [F].** (a) *Transposition in the printed formula.* With this
   section's own parenthetical definitions (U = total unit marks
   Σ φ(L)/φ(m); C = capacity φ(L)), the bound the audit instrument verified
   tight on all 66 OEIS values is u(M) = max(0, C − U + F_max): the
   instrument computes max(0, φ(L) − marks + F)
   (`kimi_forest_audit_2026-10-30.py`, audits C/F — M = 225 → 71,
   441 → 173, 1225 → 731, all TIGHT), while the printed U − C + F_max
   gives −69 / −171 / −729 on the same inputs. The formula and its
   parenthetical definitions were transposed; the 66/66 evidence belongs to
   the transposed (corrected) reading. (b) *Refutation at the scheduled
   re-check loci.* The corrected identity predicts u = max(0, H); at
   L = 4,729,725 the sound forest gives H = −20,152, predicting u = 0, while
   item 2's tower certificate (T = 0.9912 < 1, own recomputation) certifies
   u ≥ 1 — an unconditional refutation, exactly at the first modulus this
   section scheduled for re-check. At L = 6,891,885 (H = −4,385) the same
   refutation holds conditionally on ref. 41's lcm bound (item 3). (c)
   *What survives.* The max-forest certificate is a lower bound,
   u ≥ max(0, C − U + F_max), sound by audits D/F and unaffected; it is now
   known to be slack ≥ 20,153 at 4,729,725. Reopen condition for an
   exact-identity successor: a second-order certificate class (hypergraph
   strata / collision certificates, Standing (i)) tight at 4,729,725.

---

## 19. The Rosetta Dictionary: Wheel-Train Geometry ↔ Formal Number Theory [F + E]

The Prime Tread Wheel originated as a physical mechanism (Sylvan Gaskin):
an infinite train of wheels of circumference $1, 2, 3, \dots, m$ rolling
forward together from a shared vertical $0$-line, where primes emerge
physically as the scaling/ratio remainders where no smaller wheel's
$0$-line aligns, and where rolling one full turn of each wheel $1 \dots m$
end-to-end lays the 1D number line flat into a minimal 2D spiral.

To ensure zero translation gap between the physical geometry and standard
analytic/combinatorial number theory, this section records the exact
side-by-side isomorphism (**Geometry = Formalism**) across the four
load-bearing mechanisms of the wheel.

| Physical Wheel-Train Mechanism (Geometry) | Formal Mathematical Object (Number Theory / Combinatorics) | Exact Connector & Theorem |
| :--- | :--- | :--- |
| **1. Spiral of consecutive wheel circumferences** ($1 + 2 + \dots + m$) | **Triangular coordinate bijection** $N = T(m-1) + k$, $T(m) = \frac{m(m+1)}{2}$ | Lap $m$ has length $m$ (one exact revolution of Wheel $m$); radial spokes are quadratic polynomials $N_k(m) = \frac{m(m-1)}{2} + k$ with discriminant $\Delta_k = 1 - 8k$ (**Theorem 19.1**). |
| **2. Accumulated gear-ratio slip at lap entry** | **Stagger residue field** $o_p(m) = (-T(m-1)) \bmod p$ | Rolling Wheel $p$ across prior laps $1 \dots m-1$ shifts its $0$-line by $o_p(m+1) \equiv o_p(m) - m \pmod p$; ticks where $k \not\equiv o_p(m) \pmod p$ for all $p \le B = \lfloor\sqrt{T(m-1)}\rfloor$ are exact primes (**Theorem 19.1**). |
| **3. "Something contained in nothing"** (in-wheel gear powers $p^a$ wrapping unwheeled primes $Q > B$) | **Geometric series vs. pigeonhole share** $\sum_{a \ge 1} p^{-a} = \frac{1}{p-1}$ and the **$T(m)^{1/4}$ Phase Transition** | A tick has $p$ as its *sole* wheel divisor $\le B$ iff $T+k = p^a Q$ with $Q > B$ prime. No $a \ge 2$ with $Q > B$ exists above $p \gtrsim (T(m)/B)^{1/2} \approx T(m)^{1/4}$; above the threshold $a_{\max}(p) = 1$ exactly [F] (existence below remains [G]; the $Q = 1$ prime-power case is included in §19.2) (E3 errata: the threshold does **not** "lock" rotation — 17, 19, 23, 29 all sit below it and all rotate in banked witnesses; home-vs-rotate is predicted by the P2 home-balance table, §19.2) (**Theorem 19.2**). |
| **4. Mutual-aid composite web & harmonic LP smear** | **Conditional hypergraph set cover** & **Egyptian fraction LP relaxation** ($\frac{1}{2}+\frac{1}{3}+\frac{1}{6}=1$) | Composite ticks are hyperedges $F(k) = \{p \le B : p \mid (T+k)\}$. Rotating $S$ creates conditional orphans whenever $F(k) \subseteq S$; continuous LP relaxation smears $x_{p,c} = 1/p$ across $\{2,3,5\}$ at cost $11/6 = 1.8333$ (**Theorems 19.3 & 19.4**). |

### 19.1 Theorem I — The Wheel-Circumference Spiral & Ratio-Slip Recurrence [F]

- **Geometric Mechanism.** Place wheels of circumference $j = 1, 2, 3, \dots$
  on a common axle with their $0$-marks aligned at $N = 0$. Unroll one
  complete revolution of Wheel $1$ ($1$ tick), followed by one complete
  revolution of Wheel $2$ ($2$ ticks), up to one complete revolution of
  Wheel $m$ ($m$ ticks). As every prime wheel $p < m$ rolls along this
  concatenated track, its $0$-mark slips relative to the lap boundary
  whenever $p \nmid m$. A tick on Lap $m$ where no prior wheel's $0$-mark
  lands cannot be built from smaller periods and is therefore prime.
- **Formal Statement & Proof [F].**
  1. *Bijection and zero-padding optimality:* The map
     $\Phi(m, k) = T(m-1) + k$ with $T(m-1) = \sum_{j=1}^{m-1} j = \frac{m(m-1)}{2}$
     and $1 \le k \le m$ is a bijection between $\{(m, k) \in \mathbb{Z}^2 : 1 \le k \le m\}$
     and $\mathbb{Z}_{\ge 1}$. Because the $m$-th row has cardinality $m$
     equal to the discrete circumference of period $m$, $\Phi$ embeds the
     period-$m$ residue classes into 2D with zero unoccupied cells.
  2. *Ratio-slip phase recurrence:* For any prime $p$ and layer $m \ge 1$,
     divisibility $p \mid \Phi(m, k)$ holds if and only if
     $k \equiv o_p(m) \pmod p$, where
     $$o_p(m) = (-T(m-1)) \bmod p \in \{0, 1, \dots, p-1\}$$
     evolves across layers by the first-order difference equation
     $o_p(m+1) \equiv o_p(m) - m \pmod p$.
  3. *Exact primality criterion:* Since every composite integer
     $N \in (T(m-1), T(m)]$ has least prime factor $\text{spf}(N) \le \lfloor\sqrt{N}\rfloor \le \lfloor\sqrt{T(m)}\rfloor$,
     an integer $N = T(m-1) + k > \lfloor\sqrt{T(m)}\rfloor$ is prime if
     and only if $k \not\equiv o_p(m) \pmod p$ for all primes
     $p \le \lfloor\sqrt{T(m)}\rfloor$. Throughout §19 the analysis
     horizon is pinned to $B = \lfloor\sqrt{T(m-1)}\rfloor$ ($1060$ at
     $m = 1500$; $\lfloor\sqrt{T(m)}\rfloor = 1061$ differs only by the
     $1061^2$ boundary tick admitted at seam layers, §18.6 — E5 errata,
     2026-10-24). $\square$
- *Prior-art note 2026-11-14 [E — external novelty audit on record, INSIGHTS Addendum 22].* The
  ratio-slip recurrence and the √-horizon criterion are classical in
  segmented-sieve form: per-prime offsets ≡ −block-start (mod p) updated
  by subtracting the block size (Bays–Hudson 1977, BIT 17; Brent 1973;
  Crandall–Pomerance 2005, Alg. 3.2.1) and Eratosthenes' stopping rule
  respectively. Theorem I as stated is an *isomorphism* between the
  wheel-train mechanism and the classical segmented sieve with block
  size := lap m and block start := T(m−1); claim novelty only in the
  triangular-lap parametrization and the gear-train rendering, and cite
  the sieve lineage.

### 19.2 Theorem II — "Something Contained in Nothing" and the $T(m)^{1/4}$ Phase Transition [F + E]

- **Geometric Mechanism.** On layer $m$ with wheel horizon
  $B = \lfloor\sqrt{T(m-1)}\rfloor$, a window prime tick has *zero*
  divisors among the wheel rings $p \le B$ ("nothing" inside the wheel's
  vocabulary). Conversely, what composite ticks rely *solely* on a
  single wheel ring $p \le B$ at home ($c_p = 0$)? If $p$ is the unique
  prime factor $\le B$ of $N = T(m-1) + k$, then $N = p^a \cdot Q$ where
  $a \ge 1$ and every prime factor of $Q$ exceeds $B$. Because
  $Q = N / p^a \le T(m) / 2 < (B+1)^2$, $Q$ cannot have two prime factors
  $> B$; hence **either $Q = 1$ (a pure prime power $N = p^a$) or $Q > B$
  is a single prime outside the wheel horizon**. Thus every unconditional
  home orphan of ring $p$ is literally an in-wheel prime power $p^a$
  ("something") multiplying an out-of-wheel prime $Q > B$ ("nothing").
- **Formal Statement & Proof [F].**
  (write $T$ for $T(m-1)$ and $\mathcal{P}$ for the wheel primes $\\{q \text{ prime} : q \le B\\}$ throughout this section) For each prime $p \le B$, let $U_0 = \{k \in \{1,\dots,m\} : \forall q \le B,\, q \nmid (T+k)\}$
  be the native uncovered set, and let
  $$T_p = \{k \in \{1,\dots,m\} : p \mid (T+k) \text{ and } \forall q \in \mathcal{P} \setminus \{p\},\, q \nmid (T+k)\}$$
  be the unconditional home-orphan set of ring $p$.
  1. *Exact Characterization of $T_p$:* Assume $m \ge 3$ so that
     $T(m) < 2 (B+1)^2$ *(2026-10-25 repair, GPT audit: the original
     sufficient condition $T(m) < 2B^2$ fails at m = 6, where
     T(6) = 21 ≥ 18 = 2·3² (B = ⌊√T(5)⌋ = 3); the corrected hypothesis holds for all
     $m \ge 3$, since $T(m) < (B+1)^2 + m$ and $m \le (B+1)^2$)*. Then
     $k \in T_p$ if and only if $T + k = p^a Q$ for
     some integer $a \ge 1$ and some $Q \in \{1\} \cup \{\text{primes } > B\}$.
     *Proof:* Write $T + k = p^a Q$ with $p \nmid Q$. By definition of
     $T_p$, no prime $q \le B$ divides $Q$. If $Q > 1$ were composite, its
     least prime factor would exceed $B$, forcing $Q \ge (B+1)^2 > T(m)/2 \ge (T+k)/p^a = Q$,
     a contradiction. Thus $Q = 1$ or $Q > B$ is prime.
  2. *The $\frac{1}{p-1}$ Duality:* Because $p \nmid (T+k)$ for every
     $k \in U_0$, the $|U_0|$ native uncovered ticks partition across the
     $p - 1$ nonzero residue classes $c \in \{1, \dots, p-1\}$ with mean
     harvest
     $$\bar{H}(p) = \frac{1}{p - 1} \sum_{c=1}^{p-1} H_p(c) = \frac{|U_0|}{p - 1} \approx \frac{1}{p - 1}\frac{m}{\ln T}.$$
     On the home side ($c_p = 0$), each power $p^a$ contributes ticks
     $T + k = p^a Q$ with $Q = (T+k)/p^a \in (T/p^a, (T+m)/p^a]$ prime.
     By the Prime Number Theorem on short intervals **[S, heuristic
     expectation]** (E4 errata, 2026-10-24: intervals of length $m/p^a$
     fall below 1 for large $a$, where the asymptotic has no content —
     the expectation is used only in the regime where the interval is
     long), the expected count of unconditional home orphans across all
     powers $a \ge 1$ is
     $$\mathbb{E}[|T_p|] \approx \sum_{a=1}^{a_{\max}(p)} \frac{m / p^a}{\ln(T / p^a)} > \left(\sum_{a=1}^{a_{\max}(p)} \frac{1}{p^a}\right) \frac{m}{\ln T} \quad\text{[F, conditional on the heuristic expectation].}$$
     In the infinite-horizon limit $a_{\max}(p) \to \infty$, the home
     series $\sum_{a=1}^\infty p^{-a} = \frac{1}{p-1}$ matches the nonzero
     pigeonhole factor $\frac{1}{p-1}$ identically, while the logarithmic
     denominator $\ln(T/p^a) < \ln T$ strictly favors the home side!
  3. *The $T(m)^{1/4}$ Phase-Transition Threshold:* Because every tick
     $k \in T_p$ with $Q > B$ satisfies $p^a = (T+k)/Q < T(m)/B \approx T(m)^{1/2}$,
     any prime with
     $$p > \bigl(T(m)/B\bigr)^{1/2} \approx T(m)^{1/4}$$
     satisfies $p^2 > T(m)/B$, so **all higher-power terms $a \ge 2$ with
     $Q > B$ vanish identically** ($a_{\max}(p) = 1$). Across the boundary
     $p = T(m)^{1/4}$ ($32.57$ at $m = 1500$), the home-orphan coefficient
     drops discontinuously from $\sum_{a \ge 1} p^{-a} \approx \frac{1}{p-1}$
     to $\frac{1}{p}$ — an exact statement about the *harvest ledger*, not
     a rotation law (E3 errata, 2026-10-24: the sub-threshold rings 17, 19,
     23, 29 all have $a_{\max} = 2$ and all rotate in banked witnesses).
     $\square$
- **What actually predicts rotation — the P2 Home-Balance Table (`[E]`).**
  Compute each ring's ledger in the all-home state *before* any solver
  run: $\text{Net}_0(p) = H_{\max}(p) - |T_p|$ (maximum nonzero-phase
  harvest minus unconditional home-orphan load; the duality is visible
  already at the big rings — $|T_2| = 134 > 106 = H_{\max}(2)$,
  $|T_3| = 69 > 56 = H_{\max}(3)$). At $m = 1500$:

  | $p$ | $H_{\max}$ | $|T_p|$ | $\text{Net}_0$ | banked behavior |
  |---|---|---|---|---|
  | 17 | 9 | 6 | **+3** | rotates in 46/45 (c = 1) |
  | 19 | 9 | 9 | **0** | rotates in 48/47 (c = 16); home in 46/45 |
  | 23 | 8 | 5 | **+3** | rotates in all four |
  | 29 | 7 | 3 | **+4** | rotates in all four |
  | 31 | 7 | 7 | **0** | home in all four (pillar) |

  *Pre-registered test result* (Claude, 2026-10-24; frozen threshold
  $\ge 80\%$): "$\text{Net}_0(p) > 0 \iff$ ring $p$ rotates" predicts
  $19/25$ ($76.0\%$) of primes $p \le 100$ in the 48/47 — below the frozen ≥ 80% threshold, witness superseded — and **$21/25$
  ($84.0\%$) in the 46/45 — passing the pre-registered threshold**; sharpened to $\text{Net}_0 \ge +2$
  (clearing second-order semiprime collisions) it predicts **$14/15$
  ($93.3\%$)** of the 15 primes $p \le 59$ present in `best45_argon_clean.json`.
  *The misses name the mechanism:* the deviations are exactly the two
  apex-engine rings (19 rotating in 48/47 at $\text{Net}_0 = 0$; 17 home
  in 48/47 at $\text{Net}_0 = +3$) — their value is healing *other*
  rings' orphans, a second-order mutual-aid term a first-order Net
  cannot see. That term **is** the Apex Engine Swap (§18.10).

### 19.3 Theorem III — Disjoint-Union Conservation Law on the Composite Hypergraph [F]

- **Geometric Mechanism.** Every composite tick $k$ is held up at home by
  the bundle of prime gears $F(k) = \{p \le B : p \mid (T+k)\}$. Rotating
  a subset $S \subseteq \mathcal{P}$ away from $c = 0$ severs every gear
  $p \in S$ from its home multiples. Any tick whose entire factor bundle
  lies inside $S$ ($F(k) \subseteq S$) falls through the floor and must be
  caught by the rotated stripes of $S$.
- **Formal Statement & Proof [F].**
  For every subset $E \subseteq \mathcal{P}$, define the exact factor-support
  stratum $C_E = \{k \in \{1, \dots, m\} : F(k) = E\}$ (so $C_\emptyset = U_0$
  and $C_{\{p\}} = T_p$). The strata $\{C_E\}_{E \subseteq \mathcal{P}}$
  partition $\{1, \dots, m\}$ into pairwise disjoint sets. For any valid
  phase vector $(c_p)_{p \in \mathcal{P}}$ with rotated support
  $S = \{p \in \mathcal{P} : c_p \ne 0\}$, a tick $k \in C_E$ loses all
  home covers if and only if $E \subseteq S$. Consequently, the nonzero
  phases $\{(p, c_p) : p \in S\}$ must cover the entire disjoint union
  $$W(S) = \bigsqcup_{E \subseteq S} C_E = U_0 \;\sqcup\; \bigsqcup_{p \in S} T_p \;\sqcup\; \bigsqcup_{\substack{E \subseteq S \\ |E| \ge 2}} C_E.$$
  In particular, summing the maximum nonzero-phase capacities over $p \in S$
  on any downward-closed family of strata yields a valid linear inequality
  on $S$. $\square$

### 19.4 Theorem IV — The $\{2, 3, 5\}$ Harmonic LP Smear [F]

- **Geometric Mechanism.** Why does the unguided LP relaxation of $d(m)$
  collapse to a small constant even as $m$ grows? Because a continuous
  relaxation allows a wheel $p$ to split itself into $p - 1$ ghost copies
  of weight $1/p$ on every nonzero phase simultaneously, turning a discrete
  gear with one tooth into a uniform fog of density $1/p$ across the entire
  lap.
- **Formal Statement & Proof [F].**
  In the continuous LP relaxation of the conditional-coverage MILP
  ($0 \le x_{p,c} \le 1$, $\sum_{c=1}^{p-1} x_{p,c} \le 1$), assign
  $x_{p,c} = \alpha_p / p$ for all $c \in \{1, \dots, p-1\}$ on a subset
  $K \subseteq \mathcal{P}$, and $x_{p,c} = 0$ for $p \notin K$. For every
  tick $k \in \{1, \dots, m\}$:
  - each $p \in K$ with $p \nmid (T+k)$ contributes $x_{p, (T+k)\bmod p} = \alpha_p / p$, and
  - each $p \in K$ with $p \mid (T+k)$ contributes home coverage
    $1 - \sum_{c=1}^{p-1} x_{p,c} = 1 - \frac{p-1}{p}\alpha_p \ge \alpha_p / p$
    (with equality when $\alpha_p = 1$).
  Hence every tick $k \in \{1, \dots, m\}$ — prime or composite — receives
  total fractional coverage at least $\sum_{p \in K} \alpha_p / p$. Choosing
  $K = \{2, 3, 5\}$ with $\alpha_2 = 1$, $\alpha_3 = 1$, $\alpha_5 = 5/6$
  yields
  $$\frac{1}{2} + \frac{1}{3} + \frac{1}{6} = 1$$
  on all $m$ ticks at total LP objective cost
  $$\frac{2-1}{2}(1) + \frac{3-1}{3}(1) + \frac{5-1}{5}\left(\frac{5}{6}\right) = \frac{1}{2} + \frac{2}{3} + \frac{2}{3} = \frac{11}{6} = 1.833\overline{3}.$$
  This proves that without branching or cutting on the sub-$T(m)^{1/4}$
  pillars, the continuous LP relaxation replaces the multiplicative
  Mertens sieve density $\prod (1 - 1/p)$ with the additive harmonic sum
  $\sum 1/p$. $\square$
- *Prior-art & scope note 2026-11-14 [E — external novelty audit on record, INSIGHTS Addendum 22].* 11/6
  is an exhibited feasible fractional point (LP optimum ≤ 11/6), not a
  proven LP optimum — claim the certificate, not the value. The additive
  mechanism — fractional coverings governed by Σ 1/n rather than
  ∏(1−1/p) — is the foundational density principle of covering-systems
  theory (Mirsky–Newman Σ 1/m > 1 for distinct coverings; Filaseta–
  Kalogirou 2024 for the general density bound); sieve theory proper
  keeps the Mertens product multiplicative throughout. The wheel's own
  content is the conditional-coverage MILP, the α₅ = 5/6 exact-cover
  calibration, the 11/6 certificate, and the branch-and-bound guard of
  Theorem V.

### 19.5 Theorem V — The Exact Harmonic Smear Threshold ($p - 1 < L$) [F + E]

- **Geometric Mechanism.** Which prime gears $p$ can profitably "cheat"
  in a continuous LP relaxation when the remaining uncovered window
  carries dual load $L$? Whether a gear smears $1/p$ across all $p$
  phases (First-Order Smear, $y_p$ fractional) or smears $1/(p-1)$
  across its $p-1$ nonzero phases (Second-Order Smear, $y_p = 1$ fixed
  but phase $c_p$ unbranched), it shaves a proportional slice off the
  dual load $L$ while paying for one rotation. The exact break-even
  horizon where fractional smearing ceases to be profitable is
  $p - 1 = L$.
- **Formal Statement & Proof [F, conditional on the equidistribution
  heuristic — E4 errata, 2026-10-24].**
  Let $u \in \mathbb{R}_{\ge 0}^m$ be any dual weight vector with total
  residual load $L = \frac{1}{D}\sum_{k=1}^m u_k$ ($D$ = the §18.9 integer scale, 2520 at $m = 1500$) approximately
  equidistributed modulo $p$ **[S, heuristic expectation]**
  ($W_p(c) \approx D L / p$ in the first-order
  regime, or $W_p(c) \approx D L / (p-1)$ on nonzero residues when
  $W_p(0) = 0$).
  1. *First-Order Smear ($x_{p,c} = 1/p$ for $1 \le c < p$, $y_p = (p-1)/p$):*
     Ring $p$ absorbs fraction $1/p$ of the dual load $L$ (saving $L / p$)
     at primal rotation cost $(p-1)/p$. The net LP objective reduction is
     $$\Delta_{\text{LP}}^{(1)}(p) = \frac{L}{p} - \frac{p - 1}{p} = \frac{L - (p - 1)}{p} > 0 \iff p - 1 < L.$$
  2. *Second-Order Smear ($y_p = 1$ fixed, $x_{p,c} = 1/(p-1)$ for $1 \le c < p$):*
     When ring $p$ is forced off home ($y_p = 1$, paying $+1$ rotation
     cost) without fixing its integer phase $c_p \in \{1, \dots, p-1\}$,
     it absorbs fraction $1/(p-1)$ of the non-home dual load $L$ (saving
     $L / (p-1)$). The net LP objective reduction is
     $$\Delta_{\text{LP}}^{(2)}(p) = \frac{L}{p - 1} - 1 = \frac{L - (p - 1)}{p - 1} > 0 \iff p - 1 < L.$$
  Thus **both** the first-order and second-order fractional smears share
  the identical critical prime threshold $p - 1 < L$. At $m = 1500$
  ($L \approx 39$), fractional smearing is profitable if and only if
  $p - 1 < 39 \iff p \le 37$. $\square$
- *Implementation guard (measured 2026-10-24, [E]) — for the P1
  certificate branch-and-bound:* never leave a small prime ($p - 1 < L$)
  as a single binary "rotated, phase-free" ($y_p = 1$) leaf. Theorem V
  Part 2 then lets ring $p$ absorb $\max_{c \ge 1} W_p(c) \ge
  \frac{1}{p-1}\sum_{c \ge 1} W_p(c)$ of dual weight for one rotation,
  collapsing the integer bound — measured on $p = 17$: LB 40 → 20 (`verify_dual.py` single-gear release experiments, 2026-10-24).
  Always branch small primes into all $p$ explicit phases
  $c_p \in \{0, 1, \dots, p-1\}$.

## Reproduce

```
cd probes && python3 verify.py    # every number in PAPER.md, ~10 s
cd lab  && python3 PHASE5_d8.py   # the D8 closed form, landmarks + 9 predicted dead pairs
cd lab  && python3 PHASE6_quadratic_rhyme.py  # the quadratic rhyme probe (fractal side + wheel side)
cd lab/phaseb_2026-10-19 && python3 verify_best48.py best48_primary.json  # the banked Phase B 48, independent of any solver
cd lab/phaseb_2026-10-19 && python3 verify_best47.py best47_argon.json    # the banked 47-witness, solver-free
cd lab/phaseb_2026-10-19 && python3 verify_dual.py                        # solver-free exact-integer dual & rigidity certificates (9 theorems)
cd lab/phaseb_2026-10-19 && python3 verify_best47.py best45_argon_clean.json  # the canonical cleaned 45-witness, solver-free
cd lab/phaseb_2026-10-19 && python3 verify_witness.py best45_argon_clean.json 45  # generic witness verifier (45/47/48 PASS, negative control FAIL)
cd lab/cbb && python3 cbb_verify.py cbb_m1500_uncond_t40.json                 # unconditional CBB LB 40 tree (2026-10-25), pure-integer, zero solver trust
cd lab/cbb && python3 cbb_verify.py cbb_m1500_hybrid_t41_np.json             # unconditional CBB LB 41 tree (2026-10-26), 80 s, bracket [41,45] (superseded)
cd lab/cbb && python3 cbb_verify.py cbb_m1500_hybrid_t42_np.json             # unconditional CBB LB 42 tree (2026-10-27), 180 s, bracket [42,45]
cd lab/erdos7 && python3 verify_erdos7_crt.py                                 # Erdős #7: all 992 rungs CRT-certified infeasible, 1 s
cd lab/erdos7 && python3 kimi_cold_audit_capacity_2026-10-29.py               # Erdős #7 gen 2: unit-capacity criterion, two independent scans + 9/25/35 collision cert
cd lab/erdos7 && python3 kimi_forest_audit_2026-10-30.py                      # Erdős #7 gen 3: max-forest certificate, 9 survivors to 5M under the stricter max-forest certificate (the 3,355-survivor figure is the wider capacity census) + tightness on 66/66 published values
#   fleet scan artifacts (100 shards, cold-verified, §18.12): lab/erdos7/fleet/es7_cap_*.json
cd lab/erdos7 && python3 hunt_cold_audit.py                                            # §18.12 debt-hunt harvest cold audit: re-derives covered/D at 4,729,725 from hunt_s*.jsonl, zero shared code
#   debt-hunt harvest artifacts (8 seeds, cold-audited, §18.12): lab/erdos7/fleet/hunt_s*.jsonl
cd lab && python3 l4_probe.py                                                 # L4 Fock-lattice ray & pair probe (3,575 tests + 200 controls, ~17 s)
cd lab && python3 l4_wipe_phi_probe.py                                        # §2b unpriced-vs-priced reflection involution Φ probe (~1 s)
cd lean_wheel && lake build && lake env lean PrintAxioms.lean                   # 2026-11-14: Lean 4 + mathlib kernel proofs — the full formalizable surface, closed (exact-theorem spine B3/B4/B7, Thms I–V, Three-Primitive + witnesses; plus B1/B2/B5 column law + seat-zero, GLM lock+palindrome lemma, Thm II.3 phase threshold, §19.3 capacity inequalities, §19.4 LP-feasibility point, §18.9 dual identity, §18.11 rotor tuning, §18.12 Erdős fiber count — per-file list: lean_wheel/FORMALIZATION_STATUS.md), 83 theorems, zero sorry, axioms = mathlib trio only; expected output: 0 sorry, axiom footprints ⊆ {propext, Classical.choice, Quot.sound} — formalizes the pre-2026-10-28 spine
```

Probe-by-probe reproduce commands: `probes/README.md`. Full dated ledger:
`INSIGHTS.md`. Pre-registered chain plan and rulings: `AUTONOMY_2026-10-10.md`.
Session-state map: the project handoff record.

## Instruments (live pages)

| Page | What it is |
| --- | --- |
| train.html (lab/) | The wheel laid flat: the number line with seam markers, the playable covering game (rotation-priced dials), and the proven d(m) chart to m = 60 |
| wheel.html | The 1:1 canonical wheel — scrub laps, watch the sieve occlude |
| variable.html | The ratio dial — lap length scaled by any ratio |
| globe.html | The §2/§8 multiplexer — channels opening and closing over a frame |
| living-prime-map.html | The roll engine — jump to any layer and draw it from rings |
| problem-wheels.html | Collatz, Goldbach, twins, prime races on wheels |
| field-notes.html / night-shift.html | The articles: the stagger field; the witness layer and the night's closures |

## References

1. [Floyd's triangle](https://en.wikipedia.org/wiki/Floyd%27s_triangle), Wikipedia.
2. [Math::PlanePath::GcdRationals](https://manpages.debian.org/testing/libmath-planepath-perl/Math::PlanePath::GcdRationals.3pm), after L. Fortnow, "Counting rationals quickly" (2004).
3. [OEIS A066888](https://oeis.org/A066888) — primes between consecutive triangular numbers (conjecture originating with W. Sierpiński, *Liczby trójkątne* 1962; OEIS entry attributes to J. W. Nicholson, 2011).
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
21. T. Hooley, *On the intervals between numbers that are coprime to n*, Acta Math. 111 (1964/65) — the gap law the finite wheel truncates (§15.7).
22. T. Hagedorn, *Computation of Jacobsthal's function h(n) for n < 50*, Math. Comp. 78 (2009) — the h(25) = 258 capacity the cliff equals (§15.2).
23. W. Pauli, *Über das Wasserstoffspektrum vom Standpunkt der neuen Quantenmechanik*, Z. Physik 36 (1926), 336–363; V. Fock, *Zur Theorie des Wasserstoffatoms*, Z. Physik 98 (1935), 145–154 — the hidden $SO(4) \cong SU(2) \times SU(2)$ hydrogen shell symmetry ($2n^2$, §18.11).
24. O. Haxel, J. H. D. Jensen, H. E. Suess, *On the "Magic Numbers" in Nuclear Structure*, Phys. Rev. 75 (1949), 1766; M. Goeppert-Mayer, *On Closed Shells in Nuclei. II*, Phys. Rev. 75 (1949), 1969 — spin-orbit intruder shells producing the nuclear magic numbers $2, 8, 20, 28, 50, 82, 126$ (§18.11).
25. J. Schwinger, *On Angular Momentum*, U.S. Atomic Energy Commission Report NYO-3071 (1952) — the two-oscillator bosonic construction of $SU(2)$ multiplets (§18.11).
26. M. Ziller & J. F. Morack, *Divisibility in paired progressions, Goldbach's conjecture, and the infinitude of prime pairs* (arXiv:1706.00317, 2017) — the paired Jacobsthal function $j_2$ whose capacity the §15.2 cliff equals.
27. M. Ziller & J. F. Morack, *A short note on the computation of the generalised Jacobsthal function for paired progressions* (arXiv:1706.03668, 2017) — $j_2(p\#)$ values computed to $p = 73$ (§15.2).
28. P. Fueter & G. Pólya, *Rationale Abzählung der Gitterpunkte*, Vierteljahrsschrift der Naturforschenden Gesellschaft in Zürich 58 (1923), 380–386 — uniqueness of the Cantor enumeration among quadratic polynomial bijections (§16.8).
29. Maurer, *Bivalent trees and forests or upper bounds for the probability of a union revisited*, Discrete Applied Mathematics 6 (1983), 157–171 — the bivalent-forest extension behind the Generation-3 union bound (§18.12).
30. N. McNew & J. Setty, *On the densities of covering numbers and abundant numbers* (arXiv:2507.23041, v2 2026-02) — the published covering-number classification to $10^6$ our solver-free settled line extends (§18.12).
31. I. Mian & S. Siddique, *Kernel-checked exclusions for the Erdős–Selfridge odd covering problem* (arXiv:2607.25628, 2026) — the Lean-4 kernel exclusion above $10^4$ (§18.12).
32. Öztürk (Aug-2026 preprint, ResearchGate-only, DOI 10.13140/RG.2.2.13216.55049, no arXiv record, **unverified**) with two companion RG-only preprints (Aug 18; Aug 23) — claims lcm ≥ 11,486,475 for any distinct-odd covering; full texts not yet in hand (§18.12).
33. C. Bays & R. H. Hudson, *The segmented sieve of Eratosthenes and primes in arithmetic progressions to $10^{12}$*, BIT 17 (1977), 121–127 — the prior-art form of Theorem I's recurrence (§19.1).
34. R. P. Brent, *The first occurrence of large gaps between successive primes*, Math. Comp. 27 (1973), 959–963 — the sieve lineage (§19.1).
35. R. Crandall & C. Pomerance, *Prime Numbers: A Computational Perspective*, 2nd ed., Springer (2005), Algorithm 3.2.1 — the segmented-sieve text (§19.1).
36. L. Mirsky & D. J. Newman — the distinct-covering reciprocal-sum theorem $\sum 1/m > 1$ (unpublished; circulated through P. Erdős's accounts) (§19.4).
37. M. Filaseta & A. Kalogirou, *Covering systems with the sum of the reciprocals of the moduli close to $1$*, Trans. Amer. Math. Soc. 379 (2026); arXiv:2407.15280 (2024) — the general density bound (§19.4).
38. D. C. Tucker, [*The Atlas of Maximal Gaps: Exact Covering Enumeration for Primorial Sieves*](https://doi.org/10.5281/zenodo.22912558) (Zenodo, v2 2026-09-23, CC BY 4.0; code + certificates: [Zenodo 10.5281/zenodo.22865056](https://doi.org/10.5281/zenodo.22865056)) — independent instance of the classical primorial-sieve covering enumeration on a pinned 11# layer via CSP solver; Prime/Twin Atlas position bijection, Symmetry Theorem, certified twin-desert widths W(p) and Jacobsthal values g(p#) overlapping §15.2/§18.12 (§14 demarcation note; table reconciliation read-pass open).
39. I. Hackmon, *On odd covering systems with few prime factors* (Zenodo, 2026-04-10, DOI 10.5281/zenodo.19495464) — tower/weight sieve; no odd distinct covering supported on at most four primes. Known to us through ref. 41's summary; not read in full (§18.12).
40. M. Schroeder, *Nine prime divisors in odd distinct covering systems* (Zenodo, 2026-09-13, DOI 10.5281/zenodo.22759614) — claims at least nine primes divide the lcm and lcm ≥ 9,704,539,845, with a Lean package. Known to us through ref. 41's summary; **unverified** (§18.12).
41. R. Wu, with Claude, *Odd covering systems: a distorted tower sieve, checked in Lean* (GitHub `rw762-sketch/Open-Math-problem`, 2026-11-02) — φ- and tower certificates; stated Lean-kernel-only bound lcm ≥ 1,527,701,175. Repository read; Lean build not re-run by us (§18.12).
42. *On the moduli of distinct covering systems* (arXiv:2611.15110, 2026-11) — 45 divides the lcm of any odd distinct covering; minimum modulus at most 9. Abstract read only (§18.12).

---

*Text: CC BY 4.0. Code: MIT. The notebook never deletes; it only labels.*
