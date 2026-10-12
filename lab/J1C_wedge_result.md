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
