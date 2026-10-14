# PHASE 18a — P-TRI reading adjudication: conventions CONFIRMED, P-TRI acquitted

Date: 2026-10-13 (night). Artifacts: `lab/PHASE18_ptri_reading.py`,
`lab/PHASE18_ptri_reading.json`. Companion: Claude's `dfs_check.py`
(evening zip), run side-by-side.

## The fork being adjudicated

GLM's evening §1 fork: the seam-anchor kill is reading-dependent.
**Reading A** (anchor +T(m−1)): test value 8T(m−1)+1 = (2m−1)² is a
literal square → passes every QR test → universal feasibility → published
infeasible set impossible. **Reading B** (anchor −T(m−1), honest
confined phases): test value 2−(2m−1)²−8j, infeasibility genuinely
possible. GLM asked us to recompute and match against both published
lists.

## What we ran

Exact-cover engines under Claude's now-stated conventions (window = ticks
1..m of layer m; rings = primes p ≤ isqrt(T(m−1)); one offset per ring;
feasible = every tick hit), for both offset families {−T(i) mod p}
(Reading B) and {+T(i) mod p} (Reading A), m ≤ 80. Two independent
implementations (ours, Claude's `dfs_check.py`) agree to the unit.

## Verdicts

**1. The conventions are CONFIRMED [E] — and the match is cleaner than
anyone stated.** Neither raw set equals the published list, but the
relationship is exact:

> **published P-TRI set = (tri-infeasible) ∖ (free-infeasible)**
> i.e. the layers where *triangular confinement* (not free displacement)
> causes infeasibility.

Checked m ≤ 60: tri∖free = {19,20,21,25,29,30,31,32,33,35,36,37,38,39,
42,43,44,52} = the published set **exactly**. Claude's claim of
"exact equality" was imprecise (his raw tri set carries extras 2–18,
22–24, 26, 27, 40, 41 — mostly small-m ring-poverty cases), but the
*content* is fully reproduced once the published set is read as the
confinement-delta. Two implementations, one relationship, zero
mismatches. P-TRI's engine is acquitted; our afternoon "[G]" filing is
upgraded — conventions answered and verified.

**2. GLM's Reading-A prediction is REFUTED as exact-cover semantics.**
With {+T(i) mod p} offsets and one offset per ring, infeasibility is
*worse*, not universal (infeasible 2–41, 44). GLM's "universal
feasibility" conclusion belongs to the per-ticket QR relaxation, which
is a different (weaker) semantics; it does not transfer to the
one-offset-per-ring engine. His QR criterion itself is confirmed as a
sound per-ticket *necessary* shadow of Reading B. Both facts reported
honestly; the fork resolves in Reading B's favor with the engine
semantics corrected.

**3. Frozen new prediction [S].** Under these conventions, our extension
to m ≤ 80 finds **no new tri∖free-infeasible layers in 61..80**
(the Oct-8 list's 53,56,57 belong to a different engine/conventions, as
GLM suspected). When P-TRI's jsonl for 61..80 arrives, this is
checkable to the unit.

## Consequences

- §4 of the day handoff (P-TRI blocked [G]) **closes**. Step 2
  (tie j ≡ m−1 mod small primes) is unblocked per Claude.
- Our afternoon "u=0 witness" refutation of the published set is itself
  retracted: it argued against the wrong reconstruction. The honest
  ledger gains one more self-kill.
- The small-m band 2–18 infeasible under BOTH modes is ring-poverty
  (ring set too small to cover the window), not confinement — P-TRI's
  report range starting at 19 was silently excluding it.
