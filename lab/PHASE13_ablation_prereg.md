# Pre-registration — GPT's mean-preserving common-root ablation, reproduction

Date: 2026-10-11 (night). Filed BEFORE running `lab/PHASE13_ablation.py`.

Source: GPT-6 relay §6 (swarm.handoff.number.wheel.001.md), exploratory result
on c=14, odd primes p<=1000, W<=1e6, three variants:
A full common-root model; B common-root factors removed, normalization
unchanged; C = B divided by the exact per-prime mean product mu.

GPT's reported S(W) (c=14):
W=1e2: A=-6.119  B=-35.571   C=-8.599
W=1e3: A=-9.285  B=-306.957  C=-12.690
W=1e4: A=-11.520 B=-2994.624 C=-16.267
W=1e5: A=-13.073 B=-29847.870 C=-18.647
W=1e6: A=-13.951 B=-298364.652 C=-20.094
mu = 0.7016491483 (claimed product); measured B mean 0.7016421204.

FROZEN PREDICTIONS (mine, before running):
- P1 (machinery agreement): my S_A matches GPT's A within 0.05 at every W.
  (Same singular-series conventions as PHASE11, which Claude's 11d audit
  matched to 8e-9; cutoff 1000 is the only difference.)
- P2 (raw collapse is linear): S_B(1e6)/S_B(1e5) in [9.7, 10.3].
- P3 (mean product): my computed mu (product over split p<=1000 of
  (1 - 2/(p-2)^2), the corrected per-prime factor) agrees with 0.7016491483
  within 1e-4; band-mean of F_B agrees with mu within 1e-3.
- P4 (renormalized growth is sublinear): |S_C(1e6) - S_C(1e5)| <
  0.75 * |S_C(1e4) - S_C(1e3)|  (a linear law would give ratio 10; GPT's
  numbers give ~7.0/4.08 = 1.7... using his numbers: d(1e5->1e6)=1.447,
  d(1e3->1e4)=3.577, ratio 0.405. I freeze: ratio < 0.75.)
- P5 (log-like vs linear, the load-bearing discriminator): on W in
  [1e3, 1e6], fit S_C ~ a + b*ln W and S_C ~ a + b*W by least squares;
  frozen: ln-fit residual SS < W-fit residual SS  <=>  GPT's "qualitatively
  logarithmic" claim PASSES; else FAILS.

Interpretation frozen in advance:
- If P4/P5 pass: PHASE 11(b) as filed overclaims. Correct statement: the
  mean-1 normalization is load-bearing for the log-law; the common-root
  terms are the physically correct mean-1 construction, not the unique one.
  (Consistent with Claude 11d fix 3: one-signed mean deficit -> linear S,
  in miniature. Same artifact class.)
- If P4/P5 fail: GPT's variant C is not log-like either; the common-root
  terms are genuinely load-bearing as filed; GPT's exploratory result was
  cutoff artifact (p<=1000). Then rerun at cutoff 1e7 before concluding.
