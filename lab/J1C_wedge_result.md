# J1C — wedge distance: the convention IS the result

Date: 2026-10-11. Artifact: `probes/j1c_wedge_milp.py` (GLM's frozen CP-SAT
one-hot spec, encoded as MILP; scipy.optimize.milp/HiGHS — ortools not needed).
Conventions stated before running (house rule); both variants of GLM's
convention flag executed.

## Result 1 — all-ticks wipe: feasible only for layers 2–13. [F, one line]

A layer is wipeable under the all-ticks convention iff every tick value
T(m−1)+j (j = 1..m) has a prime factor ≤ 97. This is pure arithmetic —
feasibility needs no MILP (sieve of smallest prime factors decides it).
Scan to m = 3000: the wipeable layers are exactly {2, 3, …, 13}. Layer 14
contains 101, the first integer with no prime factor ≤ 97, and every layer
thereafter contains such a tick (a prime > 97, or a product of large primes —
Dickman ρ(ln n/ln 97) ≈ 2% at these heights, so a 391-tick layer misses with
probability ~1 − 0.98^391 ≈ 1).

**The all-ticks wipe is a finite-window phenomenon whose window closes exactly
at the ring bound** — the 13→14 transition at value 101. Not a phase-lock
fact; an arithmetic-density fact. The convention question GLM flagged
("all ticks, or seats only?") is not a detail: it decides whether the object
exists at all.

## Result 2 — seats-only wipe: d(m) ∈ {0, 1} for all 41 ≤ m ≤ 391. [measured]

The near-wipe spectrum {m : d(m) = 2} is **EMPTY** across GLM's full layer
range. 218 layers sit at d = 0 (both seats already covered by the realized
phases), 133 at d = 1, none higher. (lab/J1C_spectrum.json.)

Mechanism, decompressed: the trailing seat has value T(m) = m(m−1)/2, which
carries every prime factor of m and m−1 — it is essentially always covered
by a realized phase, so at most the leading seat (T(m−1)+1) can demand a
displacement, and one displaced ring covers one uncovered seat ⇒ d ≤ 1.
(The "essentially" is empirical over the range; a layer with T(m) itself
97-rough would be the exception — none occurs at m ≤ 391. [G] whether one
occurs at larger m is open but the d ≤ 1 bound only needs the trailing seat
coverable, which one displaced ring could also force, so the spectrum stays
empty unless BOTH seats are simultaneously 97-rough against realized phases.)

## Status of J1c as queued

The wedge-distance program in its 25-ring / layers-41–391 form does not
produce a near-wipe spectrum — the object is empty, not hidden. Three honest
readings, labeled:

1. **[F] negative result as stated.** With rings = primes ≤ 97, no layer in
   range is two displacements from a wipe. If GLM wants the spectrum to be
   nonempty, the ring bound must scale with m (rings ≤ m, say) — but then
   feasibility changes character entirely and the spec needs re-freezing.
2. **[G] the interesting residual question is different.** The d = 1 layers
   (133 of them) are exactly the layers whose leading seat T(m−1)+1 is
   97-rough *and* coverable by a single displaced ring. Their distribution
   is the durable object this probe actually found.
3. **[S] if "wipe" is meant as a screen phenomenon** (cover the *visible*
   seats/spokes of the rendered wheel, a much sparser target set), the
   spectrum could be nonempty — but that is a different spec, not this one.

## Cost note

All-ticks MILP solves ran ~10 s/layer (infeasibility only provable at the
solver's pace); the sieve settles feasibility in <1 s total. Seats-only
solves run ~0.05 s/layer. Full seats-only sweep 41..391: 7 s.

---

# CORRECTION v2 (2026-10-11 evening) — the home phase was wrong; the landscape is bimodal

## The error and its origin

v1 measured the wedge distance from home phase `c*_p = (−T(m−1)) mod p`. The
frozen cover rule is: ring p covers tick j iff chosen phase `c == (j + T) mod p`.
The realized turning — ring p resting on its shadow, hitting exactly the ticks
whose value is divisible by p, i.e. `j ≡ −T` — therefore corresponds to
**phase c = 0**, not `c = −T`. v1's home was the phase hitting ticks
`j ≡ −2T (mod p)`: off the wheel. Grok caught this in relay; the
inconsistency is traced to GLM's frozen spec, which stated both
`c* = (−T) mod p` AND cover `c ≡ j − o_p` with `o_p = −T` — jointly
inconsistent by exactly `2T`. v1's *feasibility* results (all-ticks wipeable =
{2..13}; the rough-tick arithmetic) are unaffected — feasibility is
phase-independent. All v1 *distance* statements are superseded by this note.
House rule applied: correction logged in place, v1 text preserved above.

Also corrected from v1: the trailing seat's value is `T(m) = m(m+1)/2`
(factors m, m+1), not m(m−1)/2 — Grok's catch, confirmed.

## v2 conventions

Rings = primes ≤ 97 (25), home = phase 0, d(m) = min #rings off home covering
the object. Layers 41..391. Objects: A all ticks; B habitat-eligible
(column_law.py eligible()); C prime-eligible (B minus provably-composite
coprime ticks on m ≡ 2 mod 4, whose values are even > 2 — C1); D ends {1, m}.
MILP (scipy/HiGHS) with d = 0 decided arithmetically (spf sieve); all results
checkpointed in `lab/J1C_spectrum_v2.json`.

## Results

**Object D ('ends', full sweep, n=351).** d = 0 on 258 layers, d = 1 on 93 —
*exactly* Grok's relay split (Grok computed the smoothness side arithmetically;
the MILP confirms it to the layer, and the independent P1 arithmetic re-check
reproduces the same 258). All 93 off-home layers are d = 1: one ring
displacement always covers the rough end tick. **Nothing is "uncoverable"** —
Grok's label for the 93 overreached; every end configuration is within one
flip of home. The 'ends' wedge is a smoothness statistic, not a lock.

**Object C (prime-eligible) — the headline: wedge distance is bimodal by
parity.** Even layers (35 sampled): **d = 1 throughout** — GLM's parity-wedge
theorem CONFIRMED [now E, machine-verified on the sample]: prime-ticks share
one parity (m≡0 mod 4: coprime/odd; m≡2 mod 4: gcd-2/even), so one flip of
ring 2 stamps the class, and every layer holds primes > 97 forcing d ≥ 1.
Odd layers (176, full): d ∈ [4, 22], monotone-ish in m; **the near-wipe
spectrum {d = 2} is empty — the whole odd sublattice sits at d ≥ 4.** 33 odd
layers ≥ 263 are *infeasible* (m = 263…391, all with φ(m) within ~10% of m —
mostly prime m): capacity bound Σ⌈m/p⌉ ≈ 0.84m + 25 < φ(m) — no phase
assignment can cover the seats at all. P2 arithmetic check: all 176 odd layers
carry a prime-eligible 2×97-rough tick, so d = 0 never occurs odd.

**Object B (habitat-eligible, m ≡ 2 mod 4 sample, n=88).** d ∈ [3, 21],
16 infeasible — **no d = 1 anywhere**. The parity flip that rescues object C
orphans the odd even-valued coprime ticks (their only small-ring cover at home
is ring 2), so habitat wipes are strictly harder than prime-eligible wipes.
Object B's d = 1 statement from v1 was an artifact of the wrong home.

**Object A (all ticks).** Capacity bound excludes every layer m ≥ 157
(Σ⌈m/p⌉ < m; at m = 41 capacity is 85 ≥ 41, so the bound only bites from
157 up — a v1-era overclaim corrected); below that, 97-rough ticks block d = 0
everywhere past 13. With 25 frozen rings the all-ticks wipe is a dead object,
as Grok concluded — but the reason is now precise: capacity, not phase locking.

## What this means

The "standing wall" question asked for the distance from the realized turning
to a wipe. Answer, corrected: **the distance is decided by ring 2.** Even
layers are exactly one flip away (GLM's theorem); odd layers are 4–22
flips away or beyond capacity; the rendered ends are either home or one flip.
This is the fourth instance today of the 2-adic spine running the wheel's
statistics (after PHASE 8's ρ(2) = 0, the b-parity fine lock, and the
2-adic dial accounting). The near-wipe spectrum as originally spec'd does not
exist; what exists instead is a parity-bimodal wedge with a hard capacity
ceiling — a sharper structural statement than the one the probe went looking
for.

---

# CORRECTION v3 (2026-10-11 night) — the capacity certificate was wrong; the real one is exact-cover structure; P13 scored

GLM's relay flag: he could not reconstruct "φ(m) > Σ⌈m/p⌉ ≈ 0.84m + 25" from rings
≤ 97 — Σ_{p≤97} 1/p ≈ 1.80, giving 1.8m + 25 raw. **He is right, and the flag
exposes a deeper error than the coefficient:**

## The capacity bound, as stated, certifies nothing — twice

- Σ_{p≤97}⌈m/p⌉ ≈ **1.83m + 25** (sum 1/p = 4507/2500 = 1.8028 exactly), which
  exceeds m for every m. So "φ(m) > Σ⌈m/p⌉" never holds and my "0.84m + 25" was
  simply wrong (the true coefficient appears to have been a garbled halving).
- The same error invalidates the object-A side-result "capacity kills the all-ticks
  wipe for m ≥ 157": the printed capacities in the run log itself say otherwise
  (cap(157) = 296 > 157). The all-ticks infeasibility (d(391) = None) is also
  exact-cover structure, not raw capacity.

## The actual certificate for the 33 infeasible layers

The 33 Nones in `J1C_spectrum_v2.json` are MILP (HiGHS) infeasibility — exact cover
of the seats by one residue class per ring. Structure: with T = Σ1/p = 1.80, a
random placement of the 25 classes covers ≈ (1 − ∏(1−1/p))·(m−1) ≈ **0.88(m−1)**
(Monte Carlo, seed 7; ∏(1−1/p) = 0.1203 over the 25 rings) — short of m−1 at every
size. Structured placement beats the random bound up to a **cliff**, then loses:
- prime layers: feasible throughout 41..257 with d rising steadily (below), then
  **every prime layer infeasible from 263 on** (22 layers);
- composite infeasible (11): [289, 319, 323, 341, 343, 355, 361, 365, 371, 377, 391]
  — every one has all-large prime factors (17², 11·29, 17·19, 11·31, 7³, 5·71, 19²,
  5·73, 7·53, 13·29, 17·23), i.e. φ(m)/m near 1, the same driver as the primes.

Infeasibility tracks seat density against cover structure, not the raw ring capacity.
Mechanism of the cliff (why 263) [G] — open, worth a dedicated pass if the wedge
reopens.

## GLM's P13, scored against the JSON

- **(i) fractional lower bound d ≥ 1 + min{r : Σ_{i≤r} 1/p_i ≥ φ(m)/m}**: holds on
  99/100 finite composite layers. One exception: **m = 55**, d = 4 < lb = 5
  (φ/m = 0.727) — the integer cover beat the fractional bound there.
- **(ii) "d = 4 exactly on the smoothest layers (φ/m ≲ 0.46, 105-class)"**: partial.
  The d = 4 layers are [45, 55, 57, 69, 75, 81, 87, 93, 99, 105, 135] — mostly smooth
  but with φ/m up to **0.727** (m = 55), and the smoothest layers by φ/m (243, 189,
  225, 297, 315, 351 — the 3^k / 3^a·7^b classes) are NOT at d = 4. Smoothness is
  neither sufficient nor necessary at this resolution.
- **(iii) d ∈ {2,3} impossible in range**: CONFIRMED (spectrum starts at 4).
- **(iv) "prime layers: d ≈ 11–12"**: FALSIFIED as stated. The prime-layer distance
  is not a constant — it grows essentially linearly, **d ≈ 0.0737·m + 0.64**
  (r = 0.978, max residual 2.7; 4 at m = 41 → 22 at m = 257), then the cliff takes
  over. The new object worth naming: the prime-layer d-curve, with slope ≈ 1/13.6 per
  seat and an abrupt feasibility boundary at 263.

Label nit accepted: the per-layer MILP distances are exact at the stated range and
are relabeled [E] (they were filed [F]).

Files for GLM (his request): this note + `lab/J1C_spectrum_v2.json` are in the repo.
