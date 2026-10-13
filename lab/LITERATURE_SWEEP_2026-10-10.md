# Literature sweep — 2026-10-10 (deep pass, four angles)

Purpose: pre-christening collision check for the wheel's claimed mechanisms, plus
positioning for the newly landed column engine. Four parallel search agents, ~40
refined query rounds across arXiv, MathOverflow, OEIS, Wikipedia/MathWorld, AMS/JSTOR,
and sieve-theory primary literature. Not a MathSciNet/Zentralblatt full-text scan —
absence results below carry that caveat.

Classification: EXACT INSTANCE / PARTIAL MECHANISM / STRUCTURAL ANALOGY /
POSSIBLE FORMAL HOME / CONFLICT.

---

## Angle 1 — wheel-sieve / additive-sieve lineage vs. the column engine

- The column engine's inner loop (solve f(m) ≡ 0 mod p once, strike m ≡ r (mod p))
  is the canonical sieving step of the quadratic sieve — **EXACT INSTANCE as a
  component** (Pomerance, "A Tale of Two Sieves", 1996). Every QS implementation
  does exactly this hop.
- Nearest published prime-listing sieve: **Atkin & Bernstein 2004**, "Prime sieves
  using binary quadratic forms", Math. Comp. 73, 1023–1030 — quadratic-congruence
  based but form-driven, not per-prime root-solving of one fixed quadratic.
  **PARTIAL MECHANISM.**
- Pritchard's wheel sieve (CACM 1981; Acta Informatica 1982; SCP 1987 family tree):
  wheels skip residue classes (the lane test is spiritually this) but striking is
  per-prime linear. **STRUCTURAL ANALOGY.** Also a **naming collision**: "wheel
  sieve" is taken. "Prime tread wheel" as a full name: no hit, low risk.
- Streaming/low-memory enumeration: Bengelloun 1986 (incremental sieve); Sorenson
  pseudosquares sieve; Galway; primesieve (Walisch) as state of practice — all
  per-prime striking with a held prime list. The column engine's divergence
  (memory = 1 byte per layer, no composite table, no ring list, primes streamed
  and dropped) appears **unpublished as an assembly**. Collision risk for the
  assembly: LOW–MEDIUM. A reviewer maps it to QS + wheel sieve in one paragraph,
  so position against Atkin–Bernstein and Pomerance explicitly.

## Angle 2 — the lane test and C(k): confirmed Bateman–Horn singular series

- **EXACT INSTANCE, both of them.** For f(m) = am²+bm+c, p ∤ a: the standard
  Hardy–Littlewood local factor is ω(p) = number of roots mod p = 1 + (D|p),
  D = b²−4ac. The column 2N(m) = m²−m+2k has D = 1−8k, so the lane test
  (1−8k non-residue ⇒ p never lands) and richest.py's
  C(k) = ∏_p (1−ω(p)/p)/(1−1/p) are the textbook formulas with zero modification.
- Canonical citations: Hardy & Littlewood, *Partitio Numerorum III*, Acta Math. 44
  (1923), Conjecture F; Bateman & Horn, Math. Comp. 16 (1962), 363–367.
- The lane test in print, verbatim: Zomlefer–Garcia–Fukshansky, "The Bateman–Horn
  conjecture: heuristic, history, and applications", Expo. Math. 38 (2020), §6.4.2
  (works the identical (2t+1)² ≡ 1−4k congruence).
- "Half of all primes never land" = Dirichlet/Chebotarev on Q(√D). Standard remark.
- "Richest columns" by singular series: **mechanism known** — Jacobson & Williams,
  Math. Comp. 72 (2003), 499–519 search for quadratics with extremal prime density
  (the Euler n²+n+41 lineage; Beeger/Poletti, Klauber 1932 earlier). The lab's
  k-parametrized table is a specific instance; the ranking mechanism is published.
- Rigorous landscape: nothing unconditional about prime values of any single
  quadratic. Best: Iwaniec 1978 (n²+1 infinitely often prime-or-semiprime);
  Friedlander–Iwaniec 1998 (x²+y⁴); Heath-Brown 2001 (x³+2y³ — note: HB's cubic
  is x²+3y³ per agent disagreement; check before citing in a paper);
  Brun sieve gives the conjectured upper-bound order.

## Angle 3 — triangular columns, Rabinowitsch, prime deserts

- No dedicated paper or OEIS entry for "primes T(n)+k, fixed k" — **reportable
  absence, medium confidence**.
- The substitution p = T(m)+k ⟺ 4p + 1 − 8k = (2m+1)² is the classic
  n²+n+A shape with A = 2k (Fung & Williams 1990, Math. Comp. 55, 345–353).
  Same counting problem in halved form. **EXACT INSTANCE.**
- **Rabinowitsch collision, REAL:** n²+n+A is prime for 0 ≤ n ≤ A−2 iff h(1−4A)=1
  (Rabinowitsch 1913; class number one settled by Heegner 1952/Baker 1966/Stark
  1967). Column k has A = 2k, D = 1−8k. Among integer start-columns, the only
  class-number-one hit is k=1 (D=−7): 1−8k ∈ {−7,−11,−19,−43,−67,−163} is
  divisible-by-8 only for −7. (Checked arithmetically, one line.)
- Even-k columns are provably prime-poor: fixed divisor 2. One-line remark,
  folklore — consistent with the wheel's dead-class language but not novel.
- Prime deserts: Ford & Gabdullin (arXiv:2310.20449) — for any irreducible
  polynomial, composite runs of ≫ (log x)(log log x)^{1/835} exist. **POSSIBLE
  FORMAL HOME** for any desert claim. Predicted desert sizes under Conjecture F
  and records: Jacobson–Lukes–Williams 2003.
- Dead classes = square discriminant ⟺ reducible over ℚ: textbook
  (Boston & Greenwood, Amer. Math. Monthly 102 (1995), 595–599 state the
  criterion in exactly this context). **EXACT INSTANCE — the criterion is not
  new. The lab's own results only ever claimed it as derived [F], which stands.**

## Angle 4 — the wheel's specific ratio structure

- Wheel enumeration (m ticks/layer, N = T(m−1)+k, visibility): closest object is
  the Ulam spiral — its diagonals are quadratic progressions, folklore since 1963.
  The wheel is the same phenomenon on a triangular shell. **STRUCTURAL ANALOGY.**
  No indexed source for the triangular-tick wheel with visibility rules.
- Two-prime channels / φ(m) seats / visibility theorem: **no match found** in any
  phrasing, after dedicated searching. Absence of evidence, not proof of absence.
- round(am/b) accumulations: Beatty/Rayleigh sequences (Beatty 1926); cumulative
  rounding governed by Ehrhart quasi-polynomials (Beck–Robins 2007). Formal home
  exists; the prime-lane application looks untaken. **PARTIAL MECHANISM.**
- Dead-class taxonomy as an organized classification of a ratio family by
  squareness of class-polynomial discriminants: **no match found**. The criterion
  is classical; the systematic taxonomy appears unindexed.

---

## Verdicts (what changes because of this sweep)

**Must cite (whitepaper references updated same day):**
HL 1923 Conjecture F; Bateman–Horn 1962; Zomlefer–Garcia–Fukshansky 2020;
Jacobson & Williams 2003; Fung & Williams 1990; Rabinowitsch 1913 + Mollin 1997;
Iwaniec 1978; Ford & Gabdullin 2023; Atkin & Bernstein 2004; Pomerance (QS);
Pritchard 1981; Bengelloun 1986; Ulam spiral; Beatty 1926 / Beck–Robins 2007;
Boston & Greenwood 1995.

**Survives as the lab's own (renamed honestly):**
1. The triangular-tick wheel enumeration and its visibility axiomatics — no
   indexed precedent.
2. The two-prime channels / φ(m) seats theorem — no indexed precedent.
3. The column engine as an assembly (solve-once + hop, 1 byte/layer, no ring
   list, MR-certified at 20 digits) — unpublished as a system; components standard.
4. The dead-class taxonomy applied to the ratio family — unindexed as an
   organized classification.
5. All derived [F] theorems stay derived; nothing in the sweep refutes any wheel
   theorem. The exact-theorem cluster (B1, column law, triangular-offset, etc.)
   had no collision at all — the agents specifically hunted for it.

**Naming:** "prime tread wheel" — LOW risk, keep. Never "wheel sieve" alone
(Pritchard). Lane test / dead classes / richest columns — safe as lab vocabulary
only if always footnoted to Bateman–Horn; never as results.

**Open caveat:** this was a web-scale sweep (~40 query rounds, four agents), not a
MathSciNet full-text scan. Before any external submission, one more pass against
MR/Zentralblatt is still owed.

## Addendum 2026-10-12 — Hooley 1965 (the one gap the archive triage surfaced)

**Hooley, "On the difference between consecutive numbers prime to n", I–III
(1965).** Gaps between consecutive integers coprime to n, normalized by
n/φ(n), converge to the exponential distribution 1−e^{−c} **as n → ∞ with
n/φ(n) → ∞**. Direct [E] law about exactly the wheel's reduced-residue (tick)
gap structure. Finite-k status measured in `lab/ARCHIVE_Q_2026-10-12.md` (Q5):
at primorials k=6,7,8 (n/φ ≈ 5.2–5.9, enumeration cap) the one-period law is
NOT yet exponential (KS 0.29–0.32); deviation mechanism = lattice floor
(c ≥ 2φ/N) + Jacobsthal cap (max gap = j(N_k), measured 22/26/34), both
receding only in Hooley's regime. Use as the asymptotic anchor for all
dial-census / Jacobsthal gap work, with the finite-k correction noted.
