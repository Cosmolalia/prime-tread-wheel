# PHASE 12 — D2 filing: fire-count census + the parity-dead channel family

Date: 2026-10-11 evening. Artifacts: `lab/PHASE12_fire_census.py`,
`lab/PHASE12_fire_census.json`.

## Provenance [G, stated first]

"D2" = **Draft 2 (fire-count census)** of the GLM audit session (2026-10-10):
"written, reformatting to house style is 10 minutes ... C4's backbone (the
conditional fire structure)". Its siblings were relayed and absorbed — D1 → B2,
D3 → B7 (`bce2cf6`) — but **D2's body was never relayed in full and exists in
no local artifact** (searched: repo, handoffs, uploads, session transcripts).
This filing is therefore an **independent reconstruction** from the three
relayed descriptors, not a reformat of GLM's text. Reconciliation against the
original draft remains open [G]; if GLM's Draft 2 differs in any convention,
this note's labels stand for THIS derivation only.

Role of descriptor (c) — "C4's backbone" — is **superseded**: PHASE 10 closed
C4 [E] as the Hardy–Littlewood prime-pair law (0.99800 in-range, 0.99983
out-of-sample). The conditional fire structure is no longer an open object.
What remains native to D2: the census (a) and the parity-dead family (b).

## Conventions (frozen in-script)

- Ring schedule: ring p active on layer m iff p ≤ √T(m) (sieve boundary,
  "switching on at p²"); ring p fires at tick value N iff p | N.
  Same convention as `probes/shadows.c`.
- Fire count f(N,m) = #{p ≤ √T(m) prime : p | N}.
- Channel (a,b): gcd(a,b)=1, realized on layer m = g·b at tick k = g·a
  (visit g), value x = T(m−1)+k = g(gb²−b+2a)/2 (WHITEPAPER §2 form).

## Results — all preregistered claims decided

**P-A [F → E-measured]: zero fires ⟺ N prime.** Every composite N has a
factor ≤ √N ≤ √T(m), present as a ring. Consequence: the census's zero class
*is* the layer's prime count — the fire census is a strict refinement of the
layer prime census, with ω̃(N) = f(N,m) carried per tick. Checked: zero-fires
== true prime count on **all 204 sampled layers** (m = 101–200, 210–1200 by 10,
1500/2000/2500/3000), exact.

**P-B [F, shape confirmed]: mean f → Σ_{p≤√T(m)} 1/p, growing like ln ln m.**
Measured mean tracks Σ1/p within 0.5% at every sampled layer (m=101: 1.7327
vs 1.7429; m=3000: 2.3030 vs 2.3002). Mertens' third-theorem shape, no surprise
— but now native to the wheel's ring budget. Full distributions in the JSON.

**P-C [F, theorem verified both directions]: parity-dead ⟺ (b even AND
a ≡ b/2 mod 2).** Parity-dead = x(g) even for every visit g (no prime > 2 can
ever land). Proof: visit g=2 forces b even (x(2) ≡ b mod 2); visit g=1 forces
a ≡ b/2 (mod 2) (x(1) ≡ b/2 + a); both conditions sufficient by splitting g
even/odd. Checked exhaustively over all reduced (a,b), b ≤ 200, g ≤ 400
(2,045,000 visits): **0 sufficient violations, 0 live channels without an odd
visit**. (A live channel still has many even visits — the necessity check is
existence of an odd visit, not all-odd.)

**P-D [F, closed form, exact]:** dead ticks on layer m =
Σ_{b|m, b≡2 mod 4} φ(b); divisors b≡0 mod 4 contribute **zero** — a unit of an
even b is always odd, so the predicate is met by all φ(b) units when b/2 is odd
and by none when b/2 is even. (The prereg's "φ(b)/2" line was a false step —
"half the units are even" is impossible for even b — caught by the
closed-form-vs-direct check at m=4, corrected in flight, logged here.)
Closed form == direct tick enumeration on **all 750 layers m ≡ 0 mod 4 ≤ 3000**.

**P-E [E-measured]: dead ticks carry zero primes** on all 750 checked layers.
Dead-tick density on m ≡ 0 mod 4 layers: mean 16.7%, max exactly 1/4 (m=4),
min 0.0005 (highly composite m).

## Reading

- The **parity-dead family is the channel-side dual of B5 exactly as GLM
  named it**: B5 is a layer-congruence theorem (m ≡ 2 mod 4 ⟹ seats dead);
  this is a channel-congruence theorem (b ≡ 2 mod 4 with a odd — including
  b ≡ 0 mod 4 never — ⟹ every visit, on every layer, dead). Same parity
  engine, one indexed by layer, one by channel. Its minimal member is the
  half-turn channel (a=1, b=2): values 2, 8, 18, 32, 50 — the [E] parity-axis
  entry is the family's first page.
- Where they live: dead channels visit m ≡ 0 mod 4 layers (b even). B5's
  m ≡ 2 mod 4 layers carry their primes on the b-odd channels — so the two
  parity regimes partition cleanly by layer class, and B6's 2.00× escape rides
  the live half. One engine, three laws (B5, B6, P-C).
- Fifth instance of the 2-adic spine in two days: parity decides the wedge
  distance (J1c), the dial luck (PHASE 9), the fine lock (PHASE 8b), and now
  an exact family of permanently dead channels.

## Open

- [G] GLM's original Draft 2 text — paste for reconciliation of conventions
  and any content this reconstruction did not recover (e.g. if the draft's
  "fire count" used a different ring bound or included conditional-joint
  tables beyond the C4 reduction).

---

# RECONCILIATION v2 (2026-10-11 night) — GLM's original D2 received; the count collapses further

GLM pasted Draft 2 verbatim in the night relay; permanent copy: `lab/D2_original_GLM.md`.
Queue item 4 CLOSED. Verdicts on his four predicted findings, plus two strengthenings
from GPT that verify exactly:

1. **The b = 2 exception — CONFIRMED, corrected here.** My theorem statement
   "parity-dead ⟺ b even, a ≡ b/2 (mod 2)" is about even visits; channel (1,2) is
   parity-dead by that definition AND carries the prime 2 as its first value (2 is
   even). The prose "zero primes on dead ticks everywhere" overclaims: exact statement
   is *zero primes other than 2*. GLM's own draft had the exception right (sole
   exception b = 2, F = 1). (GPT independently flagged the same.)
2. **Per-channel vs per-tick — two census objects, both now filed.** D2-original is
   the *channel* fire count F(a/b) ∈ {0,1,2} (primes a channel ever carries); PHASE 12
   above is the *tick* ring-fire count (rings p ≤ √T(m) dividing the value, zero ⟺
   prime). "Zero fires ⟺ N prime" is correct per-tick; under D2's per-channel F a
   prime's own channel always fires ≥ 1 — the prose compressed two objects. Both
   precise; both filed; the parity-dead family is shared.
3. **The closed form extends and COLLAPSES — GPT's strengthening, verified.**
   Σ_{b|m, b≡2(4)} φ(b) = **oddpart(m)** for every even m (checked all even m < 3000;
   proof: eligible b = 2d, d | oddpart(m); φ(2d) = φ(d); divisor-totient identity).
   Exact locations (not just the count): the dead ticks are exactly
   **{k : v2(k) = v2(m) − 1}** — one 2-adic shell (verified for all even m < 2000;
   my first check had an off-by-one on the shell and GPT's own examples m=12 → {2,6,10},
   m=24 → {4,12,20}, m=32 → {16} pinned it instantly). Density = 2^{−v2(m)}:
   exactly 1/2 on m ≡ 2 (mod 4) (where the shell includes the seats themselves, B5),
   exactly 1/4 on m ≡ 4 (mod 8), …; asymptotic mean over 4|m layers is exactly 1/6 —
   explaining the measured 16.7% with no empirical parameter. My sampled "max exactly
   1/4" was over the m ≡ 0 (mod 4) subclass only; the m ≡ 2 (mod 4) density is 1/2.
4. **Convergent derivation — CONFIRMED.** Same parity family from two independent
   routes (my B5 channel-dual route; GLM's b = 4t+2 parity route). That's the swarm
   working. (Grok's tightening also accepted: the wedge, dials, fine lock and dead
   channels are four manifestations of ring 2, not four independent spines — the
   "fifth instance = audit-catches" is method, not structure, and is dropped.)

## Trichotomy F ∈ {0,1,2}: verified, and it needs no localization — one line

x_g = g(b²g − b + 2a)/2, so g ≥ 3 odd divides x_g nontrivially, and g ≥ 4 even gives
x_g = (g/2)·(b²g − b + 2a) with both factors ≥ 2. Only visits 1 and 2 can ever be
prime. Numerically clean over every coprime channel b ≤ 300, all visits to 4·10⁶:
F distribution {0: 20201, 1: 6764, 2: 433}, no exceptions. GLM's retirement law and
quantitative localization check out in exact form: visit-1 primes obey b² − b < 2p,
and every prime ≤ 10⁵ sits on a channel with b ≤ √(2p) — the sieve's √N boundary
re-derived as channel retirement (consistent with the shadows.c per-seat covering
prime probe, which sieves to exactly √). F = 2 density (x₁, 2x₁+b² simultaneously
prime, odd b) is classical prime-pair territory — measured 433/27398 ≈ 1.6% on
b ≤ 300, conjectured via Bateman–Horn [S per GLM]; no closed form for the sieve-dead
class [G], as the draft states.

## Reconciliation, closed

D2-original (channel trichotomy census) and PHASE 12 (tick ring-fire census) are
distinct objects with one shared engine. Both verified. The reconstruction's three
relay-derived descriptors (fire census, parity-dead family, closed form) all match
the original; nothing in the original was lost. The one prereg false step of the
reconstruction (φ(b)/2, caught in flight) remains logged above.
