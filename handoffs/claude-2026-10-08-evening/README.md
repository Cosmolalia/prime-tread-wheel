# Prime wheel handoff: the Claude session (Oct 6-8, 2026)

Start with **HANDOFF.md**: the frame and its vocabulary, what is checked, the ten predictions written down before their checks (P1-P10: nine held, one failed), the exact methods, open threads, and how Obi likes the work done.

- **ATLAS.md** is a copy of the Wheel Atlas: 79 prime facts placed on the wheel, the knockout table, new fits, what doesn't fit, and the live predictions log.
- **notes/insights.md** is the running log, written as results came in. Each prediction appears there, with its time, before its check.

## Layout

| Folder | What's in it |
| --- | --- |
| `phase/` | Every script (Python and C) and its outputs (`.json`, `.jsonl`, `.txt`) |
| `platonic/` | The Platonic Map: open `platonic-map.html` in a browser; `build.py` rebuilds it from `../phase` data |
| `donut/` | The Donut View: open `donut-view.html`; `build.py` rebuilds it from `dims_compact.json` |
| `notes/` | The running insights log |

## Quick checks (from `phase/`)

Needs Python 3 with numpy, and gcc. The exact Goldbach solvers also need `pulp` and `python-sat`.

```bash
python3 gear_machine.py                                    # builds every prime to 20,000 with no division
gcc -O3 -o p3_far p3_far.c && ./p3_far 12 53 53            # first run of 53 covered numbers, rings to 37: 132966024
gcc -O3 -o p3_count p3_count.c && ./p3_count 12 53         # 30476 such runs per lap -> first expected near 2.4e8
python3 p3_count_check.py                                  # brute force over whole laps: all OK
gcc -O3 -o p2_seam p2_seam.c -lm && ./p2_seam 100000 100000000 586 1 2    # lane counts vs the gear rule (~8 s per lane)
gcc -O3 -o p9_calm p9_calm.c -lm && ./p9_calm 100000 100100000 9 14 313 > p9.jsonl   # the calm test (~11 s per lane)
python3 p9_judge.py p9.jsonl                               # judges the four P9 calls
python3 p2_judge.py                                        # judges P2 from p2_a.jsonl + p2_b.jsonl
gcc -O3 -o p10_parabola p10_parabola.c && ./p10_parabola free 2 100 && ./p10_parabola conf 2 256   # P10: wipe test with each ring free vs confined to its parabola
```

Made by Obi (Sylvan Gaskin), with Claude.
