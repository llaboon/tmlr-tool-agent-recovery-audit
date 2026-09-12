# Failure-Mode Evolution Across the Curriculum (r5-r10)

Generated from episode-level artifacts (`eval-*/paired.jsonl`, `*.episodes.jsonl`) via
`paper/scripts_extract_eval_results.py` + `paper/scripts_dump_pertask.py` +
`paper/scripts_dump_episode.py`. No numbers hand-copied from logs. r5 failure-set
membership is **not** asserted (episode artifacts lost in the 2026-08-20 node01
container reset; only archived point estimates survive).

## 1. Per-task success matrix (r6-r10, merged from node01 + node03 extracts)

Columns are rounds; 1 = task success, 0 = failure. Only tasks with at least one
observed flip or failure are listed; all omitted tasks pass in every round.

| Suite | Task (short id) | r6 | r7 | r8 | r9 | r10 | Pattern |
|---|---|---|---|---|---|---|---|
| B1-selection | (all 8 tasks) | 1 | 1 | 1 | 1 | 1 | perfect from r6 |
| B1-fault | 426ecaf9 | 1 | 1 | 1 | 1 | 1 | stable |
| B1-fault | a334f9e4 | 1 | 1 | 1 | **0** | 1 | r9-only failure (fault rows side-effect) |
| B1-fault | f842c82ad | **0** | **0** | **0** | 1 | **0** | chronic; r9 fix reverts in r10 |
| B2-dev | 8c53cbe8 | **0** | 1 | 1 | 1 | 1 | fixed by r7 expert rows, never regresses |
| B2-dev | aa74fc8e | **0** | **0** | **0** | **0** | **0** | chronic, never solved |
| B2-test | 08e7548c | **0** | **0** | 1 | **0** | 1 | fixed by r8 recovery rows; r9 dilution regression; r10 restored |
| B2-test | c80b3e80 | **0** | **0** | **0** | **0** | **0** | chronic, never solved |
| B3-holdout | (all 16 tasks) | 1 | 1 | 1 | 1 | 1 | perfect from r6; 0 discordant in every pairwise comparison, all four fault groups |

Every aggregate movement in the main results table is accounted for by exactly these
six tasks. There are no other flips anywhere in the matrix (verified: all pairwise
comparisons with c_only=b_only=0 in the paired table).

## 2. Evolution by failure class

### Class A — partition / arithmetic violations (r5-r6 era → eliminated at r7)
Archived r5-era B2 failures were semantic: safety-stock violations, invalid transfer
totals, insufficient source diversity. r6 still carried one recoverable instance
(B2-dev 8c53cbe8). The r7 dataset added 20 B2 expert rows, 12 of them *small-first*
corrections targeting the "lower id = larger stock" prior. Effect in the matrix:
8c53cbe8 flips r6→r7 and stays solved through r10 (paired r7_vs_r6 B2-dev
+0.125 [0.000,+0.375], c_only=1, b_only=0). Partition and arithmetic behavior is
perfect in all rounds r7-r10.

### Class B — injected-fault recovery on B3 (r5 → eliminated at r6, never regressed)
r5 scored 0.8125 on B3-holdout; r6's dataset raised the B3 dose (duplicate rows)
and B3 has been 16/16 in every round since. Group-level paired stats show **zero
discordant tasks across all round pairs and all four fault groups**
(timeout+schema_drift, auth_expired+truncated_response, malformed_redirect,
rate_limit+stale_response). Recovery behavior, once installed, was robust to every
subsequent dataset change (r8 recovery rows, r9 dilution+fault rows, r10 rebalance).

### Class C — order-reference trial-and-error (chronic; partially resolved)
The model spends early turns preparing distractor orders, receives
`invalid_transfer_total`, finds the correct order, then runs out of the 8-call
budget before `verify`. Evidence chain:
- **08e7548c**: fails r6/r7, fixed at r8 by the 10 reference-recovery rows (real
  env replays of wrong-order→error→correct-order→completion within 8 calls);
  regresses at r9 (dilution, §see dilution_ablation), restored at r10. Paired:
  r8_vs_r7 +0.125 c_only=1; r9_vs_r8 −0.125 b_only=1; r9_vs_r10 −0.125.
- **c80b3e80** (never solved, 0/5): double-distractor geometry (d4/pr3; distractor
  order quantities 9 and 8 vs target 5). r10 episode: `tool_calls=8`,
  `stop_reason=max_turns`, `parse_error_count=0`, `repeated_calls=0`, per-turn
  completion tokens 29/28/189/189/187/14/67/51 — two cheap probe calls, three full
  prepare-class calls, then short confirm calls: consistent with T2/T3 distractor
  attempts rejected by the environment, correct order reached at T4, `verify`
  falling one turn beyond budget (T9).
- **aa74fc8e** (B2-dev, never solved, 0/5): r10 episode shows a near-identical
  signature — same SKU ("SKU-GRINDER"), same termination
  (`max_turns` at 8 calls, 0 parse errors), per-turn tokens
  29/28/185/183/184/14/66/50 vs c80b3e80's 29/28/189/189/187/14/67/51. We classify
  it in the same distractor-trial-and-error class by episode signature (inference,
  not env-level verification).
This class is the residual failure mode of the final baseline: protocol-clean
(0 parse errors in all rounds) but budget-exhausting.

### Class D — fault-conditioned transcription precision (B1-fault, 0.667 in every round)
B1-fault injects timeout faults mid-episode. The suite shares task ids with
B1-selection: a334f9e4 and f842c82ad both pass selection 8/8-style in every round
but fail under fault injection — the deficit is fault-response, not task
comprehension.
- **f842c82ad**: chronic failure r6-r8. r9's 6 fault_first_try rows (8-call
  timeout→retry→first-correct-reference chains, d=2 matching the eval fault spec)
  fixed it — the only round it passes.
- **a334f9e4**: passes every round except r9, where it broke: T6 transaction_id
  transcription error (duplicated segment b0bd→b0bd0bd) → `transaction_not_found`
  → retry consumes the remaining budget → `verify` never runs. r9 episode:
  `fault_group=timeout`, `tool_calls=8`, `stop_reason=max_turns`,
  `repeated_calls=1`, tokens 29/29/28/184/14/65/51/49.
- Net effect: the fault rows produced a perfect swap (r9_vs_r8 c_only=1, b_only=1,
  net +0.000), so B1-fault stayed 0.667 in all six rounds. r10 removed the fault
  rows (id-transcription precision judged unteachable via expert trajectories
  under a zero-redundancy 8-call budget) and f842c82ad reverted as predicted.

## 3. Chronic-failure dossiers at the r10 baseline

| Task | Suite | Record | Termination | Signature | Diagnosis |
|---|---|---|---|---|---|
| c80b3e80 | B2-test | 0/5 | max_turns @ 8 calls, 0 parse err, 0 repeated | probes then 3 full calls; SKU-GRINDER | double distractors d4/pr3; verify 1 turn short |
| aa74fc8e | B2-dev | 0/5 | max_turns @ 8 calls, 0 parse err, 0 repeated | near-identical to c80b3e80 | same class (by signature) |
| f842c82ad | B1-fault | 0/5 except r9 | r6-r8/r10 budgets/fault-response | timeout group | fault-response coverage, removed with r10 fault rows |

Structural readout: at the final baseline, every remaining failure is (i) semantic,
not protocol (0 parse errors anywhere), (ii) budget-exhaustion-shaped
(max_turns at exactly 8 calls), and (iii) concentrated in distractor-dense B2
geometry plus the fault-transcription corner case. The two leverage points —
turn-allocation policy under distractor density, and id transcription under fault
— define the residual gap for any post-SFT (RL) stage.

## 4. Provenance
- Matrices: `curriculum_results/extracted/node01_eval_extract.json` (r8/r9/r10),
  `node03_eval_extract.json` (r6/r7/r8); r8 asserted cross-node identical.
- Episodes: `outputs/experiments/d4-no-sha-20260819-node05/eval-r10-B2-dev/r10.episodes.jsonl`,
  `eval-r10-B2-test/r10.episodes.jsonl`, `eval-r9-B1-fault/r9.episodes.jsonl`.
- Qualitative r5/r6/r7/r8 failure descriptions: docs/experiment_archive_20260819.md
  §8-13 + docs/agent_handoff_20260820_r10_final.md (archival records).
