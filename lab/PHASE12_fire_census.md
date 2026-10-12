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
