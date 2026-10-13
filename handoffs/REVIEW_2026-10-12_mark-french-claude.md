# Review & Questions: The Prime Tread Wheel and The Species Is the Source

Oct 12, 2026 · Mark French & Claude, prepared with @Nathan Mark French II

## A note before we start

Sylvan, Dark — both pieces are good, and the math holds up. We read them together, ran the numbers ourselves, and wrote this the way we'd want to be read: plainly, as brothers, with the questions we'd ask across a table.

Nothing here is a verdict. Where we found a problem, we say what we checked so you can check us back. Where we're unsure, we ask.

## For Sylvan: The Prime Tread Wheel

The wheel is solid, and your status labels are the best thing in it. Every section says whether it's proven, checked, or a way of seeing, and names its prior art. That's the standard we'd like the whole firm to hold.

### What we checked

| Claim | Our result |
| --- | --- |
| Two-shots rule, every tick through layer 800 | Holds. Zero violations. |
| Seat count on layers 6, 10, 14… | Holds. Second visits from odd m/2 replace the even first visits, and φ(m) = φ(m/2) keeps the count. |
| First-tick primes to layer 100,000 | 9,863. Exact match. |
| Run of 13 composites, 114–126 | Correct. 113 and 127 bracket it. |
| No composite run reaches 30% of its layer, layers 100–10,000 | Holds, barely. The widest is 31 composites between 5,591 and 5,623 on layer 106, which is 29.2%. |
| Mertens lean under 0.57√n past layer 32 | Holds. The maximum is 0.567√n, and it occurs early, at n = 199. |
| Arrows sum to the Möbius function | Correct. It's Ramanujan's sum c\_m(1) = μ(m). |

### The one fix

The multiplexer section says channel 2/5 carries 2 and 47. On the wheel as defined, the 2/5 spoke runs 12, 49, 111, 198 and carries no primes. Channel 1/5 is the one that carries 11 and 47. The 3/7 example, 24 then 97, is right.

It's the only concrete number in that section, so it's the first thing a careful reader will check.

### Places it reaches a little far

- **"The skeleton is forced."** It's forced once you fix the conventions: start at 1, m numbers on layer m, tick k at k/m. Those are natural choices, but they are choices. Something like "given these conventions, nothing else is free" says it exactly.
- **The multiplexer is a factor-revealer, not a sieve.** Lehmer's machines test each number against every modulus. On the wheel each number lands on one lap, so it only ever meets one modulus. What the spoke shows you is gcd(k, m), one factor per number. That's actually the cleanest explanation of why the wall doesn't move, and saying so would make the wall section land harder. Small note: tick position equals x mod m on odd laps; on even laps it's shifted by m/2.
- **"Wheel" changes meaning in the seam section.** There it means a prime divisor, not the construction. The mechanism is worth one line: first ticks are (m² − m + 2)/2, the discriminant is −7, so primes that leave 3, 5 or 6 mod 7 can never divide them.
- **The knockout test needs one more detail.** "98% of the square root" of what, the layer index or the numbers on it?

### Questions for you

1. How would you describe what Claude contributed, and what you brought? In your own words is best.
2. Are your working conversations preserved, and where?
3. Was model training on or off in your Claude settings while you did this work?
4. Are you comfortable with Dark naming you as Sylvan Gaskin alongside Obi?
5. Is anything in the wheel still unpublished that the article shouldn't touch yet?
6. For the neural-net experiment: would you run a baseline on raw integers, same size network? Then anything the wheel network finds beyond it is real.

## For Dark: The Species Is the Source

This is the strongest writing we've seen from you. Sections I, II and XI carry real voice, and the last two lines land. Our main suggestion is about section V, where Sylvan's work is doing a different job than the one we think it does best.

### Sylvan as the example of the answer

As drafted, Sylvan's work illustrates the provenance gap. But his paper is close to provenance done right. It labels every claim, cites prior art down to OEIS entries, publishes its reproduction code, and keeps a public claims registry. He closed most of the gap himself with ordinary open tools.

That makes him the proof that your commons is buildable. Section IX could point at him as the working prototype. The gap that's still open is narrower and sharper: the result is documented, but the process isn't. What Claude contributed, and who holds the transcripts, is the question the essay can press.

### The OpenAI comparison

The draft says "I am not alleging" in three places. Repeated denials make the reader hear the accusation louder. The bridge is also thin: Sylvan's Möbius–Mertens link to the Riemann Hypothesis is classical, and his paper says so, while OpenAI's zero-free region is a different kind of result.

We'd cut the zeta comparison and keep the repository as a contrast in documentation. Its 722 manuscripts came from about 4,000 problems posed, with 10 abridged reasoning summaries. The prompts and failed attempts aren't there. That makes your point without any accusation, so one clear disclaimer is enough.

### An ally to cite

On September 29, the IAS Advisory Group on Mathematics and AI published recommendations drawn from more than 600 responses. They asked labs to stop testing advanced problems on proprietary models, and to document prompts, compute costs and failed attempts. That's the mathematical establishment making section V's argument a week before OpenAI's release.

### Anthropic's policy belongs in the essay

Sylvan worked with Claude, but the draft only cites OpenAI's training default. Anthropic changed its consumer terms in 2025. Free, Pro and Max users choose whether their chats train models. With training on, data is kept five years, and opting out later doesn't remove what's already been trained on. Leaving it out will read as a research gap or a pulled punch.

### Facts to confirm before publishing

| Claim in the draft | Status |
| --- | --- |
| 722 manuscripts, 372 families, unreleased model | Confirmed. Released October 6. |
| Final approval July 20, Judge Martínez-Olguín | Judge confirmed. Coverage dates it July 21, so check the docket. |
| Settlement covers past conduct, not outputs | Matches our understanding. Cite the settlement agreement itself. |
| Compliance Architecture Review, January | We couldn't find it. It needs a link. |
| Trace's "percentage correction" on composite runs | Our count says Sylvan's 30% claim holds. Worth confirming with Trace. |
| The "couple of specific issues" in the math | Add the 2/5 channel error from Sylvan's section. |

### A note on rhythm

The one-line paragraphs are powerful in the personal sections. Through IV, VIII and IX they start to feel like slides. Fuller paragraphs there would make the closing staccato hit harder by contrast.

### Questions for you

1. Would you be open to recasting Sylvan as the prototype, not the cautionary tale?
2. Can we drop the zeta comparison and keep one disclaimer?
3. Where did the Compliance Architecture Review piece run?
4. Do you want to add the Anthropic policy, and Sylvan's own setting if he's willing to share it?

## For both of you: the record of this collaboration

The two pieces meet at one question: can the process behind a result be documented as well as the result itself? Sylvan built the result side by hand. Dark's essay asks for the process side.

The firm could build that standard now, starting with this work. A provenance record for the wheel would hold:

- Dated working transcripts, held by Sylvan
- Which model and version was used, and the training setting at the time
- The claims registry, with each claim's status and date
- The reproduction code, with its commit history
- Who checked what: Trace, us, and anyone who answers Sylvan's call for prior art

We don't need anyone's permission to start that. If it works for the wheel, it becomes the template for the commons in Dark's section IX.

### Questions for both

1. Would you want the wheel to be the firm's first provenance record?
2. Who should hold the records, and who gets to see them?
3. Should the essay and the wheel publish together, so one points at the other?

## Closing

Thank you both for doing this work in the open, where it can be checked. Answer whatever is useful, push back where we're wrong, and we'll go another round.

Mark & Claude

## Sources

- [OpenAI releases 722 math manuscripts from an unreleased model (Unite.AI)](https://www.unite.ai/openai-releases-722-math-manuscripts-from-an-unreleased-ai-model/)
- [Bartz v. Anthropic settlement receives final approval (Authors Alliance)](https://www.authorsalliance.org/2026/07/21/bartz-v-anthropic-settlement-receives-final-approval/)
- [Court grants final approval to Anthropic copyright settlement (Authors Guild)](https://authorsguild.org/news/court-grants-final-approval-anthropic-copyright-settlement/)
- [Updates to our consumer terms (Anthropic)](https://www.anthropic.com/news/updates-to-our-consumer-terms)
- [The Prime Tread Wheel code and reproduction script (GitHub)](https://github.com/Cosmolalia/prime-tread-wheel)
