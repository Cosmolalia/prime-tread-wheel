# GLM CRT-shift collapse — audit, 2026-10-13 (morning)

Claim under audit: `handoffs/SWARM_HANDBACK_2026-10-12_1719.txt`, GLM §1.
Probe: `lab/GLM_COLLAPSE_AUDIT_2026-10-13.py` (all legs, ~16 s total).

**Verdict: the collapse STANDS — all four legs PASS [E].** The wedge is
now exact arithmetic at the feasibility level everywhere, and the
distance level is a small prime-set search instead of an m-tick MILP.

## What GLM claimed, and what each leg found

The theorem: one-hot phases c_p over rings P, Q = ∏P, a = CRT(c_p).
(i) covered(N) ⟺ gcd(N−a, Q) > 1; (ii) d = #{p ∤ a}; (iii) feasibility
is position-independent: feasible ⟺ m ≤ j(Q) − 1; (iv) d(m) = min over
run-start translates of the non-divided-prime count.

- **LEG 1 — exhaustive enumeration, Q ∈ {6, 30, 210}.** Every translate a
  (mod Q), every window: identity (i) holds exactly; the feasibility
  threshold (iii) holds exactly (feasible ⟺ m ≤ j(Q)−1, with j verified
  by scan: j(6)=4, j(30)=6, j(210)=10 — matching OEIS A048669); the
  d-formula (ii) equals the brute-force minimum on every tested window.
  This is a complete proof by enumeration at small scale, and the
  identity itself is CRT — the bijection between phase tuples and
  residues mod Q is exact because the moduli are pairwise copime.
- **LEG 2 — GLM's m=14 witness, reconstructed.** a = Q_odd (≡ 0 mod
  every odd prime ≤ 97, odd ⇒ ring 2 displaced, d = 1) covers the whole
  window 92..105; d = 0 impossible since 101 and 103 are 97-rough.
  Matches the measured d(14) = 1 exactly. The construction is the
  parity mechanism (GLM's parity wedge theorem) seen through the
  collapse: one displaced ring (2) covers the entire odd class.
- **LEG 3 — B=53 recomputed WITHOUT a MILP.** The collapsed search
  (choose S = primes dividing a; exact-cover DFS over residues of the
  rest, with an optimistic-bound prune) reproduces the 2026-10-12 HiGHS
  measurements to the unit: **d(60) = 7, d(100) = 11, infeasible at
  150** — in 16 seconds of Python. Feasibility at 150 also follows
  instantly from (iii): j(53#) = 106, so no 150-window can ever be
  covered at any displacement. LEG S's MILP runs are now reproducible
  from arithmetic alone.
- **LEG 4 — j-values GLM relied on.** j(2#)=2, j(6)=4, j(30)=6,
  j(210)=10 by direct scan (match OEIS A048669), and A048670 confirms
  **j(31#) = 58** exactly as GLM stated — so the B=31 infeasibility at
  m = 60 (60 > 58 − 1) is now explained by table lookup, and our
  earlier "j(31#) ≤ 60 bracket" is resolved to the exact published
  value 58.

## What the collapse actually buys (honest ledger)

1. **Feasibility is closed everywhere, no solver, ever.** m ≤ j(Q) − 1.
   This subsumes N1 (the Jacobsthal-window theorem is the native-schedule
   slice of (iii)) and both LEG S cliffs. [E]
2. **d(m) is reformulated, not eliminated.** d(m) = |P| − max |S| over
   S ⊆ P such that the window's S-non-multiples are coverable by one
   residue class per remaining prime. Still combinatorial — a small
   exact-cover/SAT over the primes (16 primes: seconds; the native
   m = 1000 case: 127 primes, needs real SAT machinery, as GLM said).
   GLM's "enumerate Jacobsthal run-starts" route is cheap only near
   m ≈ j(Q) where runs are forced; for m ≪ j(Q) the S-search is the
   instrument.
3. **"Why m/13.5" is now a well-posed ω-law.** The slope question
   becomes: how does max |S|(m) degrade as m → j(Q)? ω of the optimal
   shift falls from 24 (m = 14) to 3 (m = 257) at B = 97 — GLM's
   numbers, and the LEG 3 machinery can now measure this curve
   MILP-free, which makes the **slope-universality** attack
   (why ≈ 0.074 in two objects) a pure-arithmetic census.
4. **Position-independence is for FREE rings** (the wedge instrument).
   The realized turning — the one quadratic curve the wheel actually
   rolls — is untouched by the collapse. The instrument and the
   realization remain two different objects; the collapse lives on the
   instrument side.

## Naming collision — pinned

House usage: **h(k) = j(p_k#)** — the cliff, i.e. the FIRST infeasible
layer (h(25) = j(97#) = 258). GLM's handback uses **h(Q) = j(Q) − 1** —
the max COVERABLE window. Offset-one neighbors of the same table.
Standardized going forward: the house h(k) keeps its meaning; "max
coverable window" is written j(Q) − 1, never h(Q).

## Queue consequences

- m = 1000 proven optimum: attackable via the collapsed SAT (127
  primes) instead of a 40k-variable MILP — cheaper, and the incumbent
  d = 38 / bound 32 bracket can be closed by the same route.
- The alternatives pass (dial theorem, slope universality,
  native-schedule law) now runs on arithmetic-first instruments.
- GPT's d_home vs d_flip conditional split (queue #6) gains a clean
  form: d = #{p ∤ a} splits into p ∤ a with r_p free vs forced.
