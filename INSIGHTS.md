# INSIGHTS — Prime Tread Wheel lab notebook

Cumulative. Newest at the bottom. Nothing here is deleted; superseded
readings are marked. Epistemic labels: [S] stated by Sylvan, [F] follows,
[G] gap, [E] externally established / machine-verified here.

---

## 2026-10-08 — The stagger is the primary object

**Reframing (Sylvan):** the wheel's primary object is not primes. It is the
*stagger of the numberline* as the wheel grows relative to prior layers.
Primes fall out of reading the stagger; the scaling can be seen at each
step in the count. Probes should measure the stagger itself.

**Stagger field (definition).** For prime p, its shadow on lap m sits at tick
k ≡ o_p(m) = −T(m−1) (mod p), o in 1..p. The stagger field at step m is the
tuple {o_p(m)} over all prior primes. (probes/stagger.py)

### Verified this run

1. **[F] The whole numberline's stagger at step m is the single counter m,
   read in every prime modulus at once.** Lap-to-lap, the entire field shifts
   by o_p(m+1) − o_p(m) = −m (mod p). One tick mark advances every layer's
   fractional offset simultaneously. This is the precise form of "a running
   tick mark counter with aperiodic scaling traversal": the counter IS m;
   each prime reads a different base-p digit of it.

2. **[E] Parabolic confinement.** Each o_p(m) is periodic in m with exact
   period p for odd primes (0 violations, p<200, m<400); p=2 has period 4
   (the parity axis runs on the 4-lap cycle — §4's mirror operator). Over one
   period, o_p visits exactly (p+1)/2 residues — the triangular numbers mod p.
   The arcs do NOT sweep their circles uniformly; each sweeps a discrete
   parabola and is forever confined away from (p−1)/2 of its phases.
   Example, p=11 one period: [10,8,5,1,7,1,5,8,10,11,11] — palindromic
   parabola, symmetric about its vertex, exactly as the scaling picture
   (right before midpoint, left after, meeting at 1) predicts at the level
   of individual primes.

3. **[F] Exact aperiodicity of the joint field.** The combined configuration
   over the first r primes recurs with period lcm(2..p_r) ≈ e^{p_r}:
   first 25 primes → ~10^36 laps; first 30 → ~10^59. The full stagger never
   repeats within any physical horizon. Aperiodicity is proved, not observed.

4. **[E] Stagger-determinism (the platonic map, exact form).** Computing the
   arc cover from {o_p(m)} alone — no values, no arithmetic on values —
   reproduces the actual first-prime offset of EVERY lap m=4..5000
   (4,997 laps, 0 mismatches, widest stagger-open mouth: 100 ticks).
   "Primes fall out of the stagger" is literally true at tick resolution:
   the first-prime function is a pure function of the stagger configuration.
   The wheel contains the complete answer to prime placement in uncompressed
   form. Decoding = compression, and §8's wall ("routes for free, decoding
   is the wall") is now precisely: *the stagger field is computable in O(m)
   but no compressed law of the field is known.*

### Reconciliation with the earlier negative result

5. **[F] The wheel constrains the movie, not the frame.** The regularity
   probes found o_p uniform in k within a fixed lap (no per-lap constraint
   on where shadows land). The parabolic confinement lives in the
   m-direction — how each prime's stagger evolves across laps. So:
   - k-direction (within a lap): shadows arrange freely → covers can pile
     up (record mouth = generic tail). [E, established]
   - m-direction (across laps): each arc's orbit is a confined parabola,
     joint field exactly aperiodic. [E, established]
   Any wheel-native proof must therefore be a LAW ON STAGGER ORBITS — a
   statement about the sequence {o_p(m)}_m — not a statement about
   per-lap covers. [G: no such law connecting orbit structure to
   "a lap's arcs cannot cover all candidate ticks" is known.]

6. Record-layer tie-in: m=264800157's mouth was built by small-prime arcs at
   stagger positions 2(2),3(3),4(5),6(7),7(11),10(13),11(17),17(19),2(23),
   23(29),19(31),37(37),28(41),15(43),32(47),22(53),13(59)... — every odd
   tick < 767 caught. p=2 striking tick 2 means even ticks carry even values
   (m even ⇒ T(m−1) odd), so all candidate ticks were odd from the start.

### Standing claims inventory (unchanged status)

- [E] m ≡ 2 (mod 4): seat-primes identically zero; all primes on non-seat
  ticks; seat test misaligned from value-divisibility by exactly m/2.
- [S, empirically held, unproven] From m=21 up, every lap has ≥1 interval
  prime strictly each side of the midpoint. Verified m=21..20,000
  exhaustively + record layer + m≡2 mod 4 laps + laps at 10^6. Stronger
  than no-empty-layer (record mouth shows 766 shut ticks inside one half
  are possible; "both halves nonempty" forbids more).
- [E] gcd(k,m)=gcd(m−k,m): the seat pattern is a palindrome about the
  midpoint. Pattern-symmetry proved; value-side inherits nothing yet. [G]
- [G] The routing wall, restated in stagger language: the stagger field
  determines everything (insight 4) but the only known reading of it is
  the uncompressed O(m) simulation. A compressed wheel-native law of the
  field is the whole game.

### Next probes suggested

- **Orbit-law search:** the stagger orbits o_p(m) are parabolas with
  palindromic structure. Test whether joint orbit coincidences are
  constrained: e.g., for pairs (p,q), how often do two arcs land on the
  same tick in a given lap window, vs independence? Any correlation here
  is a wheel-native covering constraint the sieve does not see.
- **Scale-invariance of the stagger signature:** does the sorted fractional
  profile {o_p/p} have a stable shape across lap sizes (cups picture)?
- **Mirror-compensation at height** (needs k₀-per-striker dump from
  shadows.c): do late-opening mouths compensate on the mirror side?
