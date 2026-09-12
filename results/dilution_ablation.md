# r9/r10 Data-Dilution Ablation (recovery-dose vs. dataset size)

Generated from episode-level artifacts (`curriculum_results/extracted/*.json`,
paired statistics) + dataset composition records
(docs/experiment_archive_20260819.md §12-13, handoff 20260820). This section is
referenced as `sec:dilution` by the main results table.

## 1. Setup: three datasets, one behavioral question

| Round | \|D\| | Composition (delta vs r8) | Recovery-row share | B2-test |
|---|---|---|---|---|
| r8 | 113 | baseline: 96 r7 + 10 reference-recovery rows + 5 B3dup + 2 first-try | 10/113 = 8.8% | 0.875 |
| r9 | 132 | +8 homogeneous first-try rows (all d4/pr3, 2 base recipes) + 6 fault rows + 5 B3dup | 10/132 = 7.6% | **0.750 (regression)** |
| r10 | 120 | r8 core (113) + 5 diverse first-try rows (deficit [3,4,5,3,5]) + 2 B3dup; fault rows and homogeneous rows removed | 10/120 = 8.3% | 0.875 |

r9 and r10 form a natural ablation: r9 is the *largest* dataset (132 rows) and the
only one that regresses; r10 is smaller than r9 (120 rows) and restores r8 exactly.

## 2. The paired evidence chain (B2-test, task-level)

| Transition | Gain | Paired 95% CI | Discordant | Interpretation |
|---|---|---|---|---|
| r8 vs r7 | +0.125 | [+0.000,+0.375] | c_only=1 | recovery rows install retry-after-error (08e7548c fixed) |
| r9 vs r8 | −0.125 | [−0.375,+0.000] | b_only=1 | **dilution regression** (08e7548c re-fails) |
| r9 vs r10 | −0.125 | [−0.375,+0.000] | b_only=1 | r10 restores 08e7548c with fewer rows |
| r8 vs r10 | +0.000 | [+0.000,+0.000] | c_only=0, b_only=0 | **perfect behavioral tie** on all five suites |

The single discordant task in each nonzero transition is the same task (08e7548c,
per-task matrix), i.e. the whole regression is one mechanism, not noise. No other
suite moves between r8/r9/r10 except the B1-fault swap
(f842c82ad↔a334f9e4, c_only=1/b_only=1, net 0), which is attributable to the 6
fault rows, not dilution, and reverts in r10.

## 3. Mechanism

- The r9 addition of 8 homogeneous first-try rows (all deficit-4 / prio-rank-3 —
  the exact geometry of the failing task c80b3e80, from only 2 base recipes)
  did two things at once: (i) it diluted the reference-recovery exemplar share
  (10/113 → 10/132), and (ii) it taught first-try ordering on precisely the
  geometry where the model needed to keep its retry-after-error behavior. The
  previously-fixed task 08e7548c regressed; c80b3e80 behaved identically to r8.
- r10 replaced those 8 rows with 5 diverse first-try rows (deficit spread
  [3,4,5,3,5] via the `target_deficit` spec knob) — a *smaller* dataset with a
  *restored* effective recovery dose — and 08e7548c recovered, with zero
  behavioral difference from r8 on all suites (no discordant task anywhere).
- Conclusion: **composition beats size**. Recovery behavior is dose-sensitive;
  adding 19 rows (132 vs 113) with the wrong geometry destroyed one installed
  recovery and taught nothing usable, while a 7-row rebalance (120 rows) fully
  restored the r8 policy. Under a fixed SFT recipe, dataset growth without
  exemplar-diversity control is not merely neutral but actively risky.

## 4. Why the diluting rows could not be made diverse: generator geometry lockout

Attempts to generate diverse first-try rows for the failing geometry are blocked
by the task generator (recorded exhaustively in the r10 handoff; do not re-explore):
- deficit=4 is hardcoded (workflow.py ~632); the largest-deficit base pool has only
  2 rows and is seed-invariant;
- distractor order quantities 9/8 vs target 5 lock the prio-rank-3 structure;
  validation requires ≥3 candidate order ids (pr2 unreachable);
- 24,000 seed samples produced 0 acceptable variants;
- the only geometry knob is `target_deficit` (domain [2, target_qty)); the failing
  task's base is outside the fixed-deficit-2 set.
This is why r10 diversified *across* deficits ([3,4,5]) rather than within d4/pr3.

## 5. Limitations

Single seed (23), single training run per dataset, and the regression is a single
task — the mechanism is identified at task level (08e7548c) and corroborated by
the perfect r8≡r10 tie, but the dose response is not mapped beyond three points
(113/120/132 rows; 8.8%/8.3%/7.6% recovery share). CIs are wide at n=8 per suite;
the claim rests on the paired per-task chain, not on the marginal intervals.
