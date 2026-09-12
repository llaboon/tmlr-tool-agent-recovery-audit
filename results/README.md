# curriculum_results/ — r5-r10 curriculum supplement (P1 paper products)

Everything here is generated from episode-level artifacts (paper README rule: no
hand-copied numbers). Frozen MRPO skeleton (../main.tex, ../sections/) is NOT
modified; this directory is a standalone supplement.

## Files
- `main_results_table.tex` / `.md` — main r5-r10 table with 95% percentile
  bootstrap CIs + paired transitions (exact McNemar / paired bootstrap).
- `failure_mode_evolution.tex` / `.md` — per-task success matrix, four failure
  classes (A partition/arithmetic, B B3 recovery, C distractor trial-and-error,
  D fault-transcription), chronic dossiers c80b3e80 / aa74fc8e / f842c82ad with
  episode-level evidence.
- `dilution_ablation.tex` / `.md` — r9 dilution regression vs r10 rebalance
  (`sec:dilution`); recovery dose beats dataset size; generator geometry lockout.
- `curriculum_supplement.tex` — standalone wrapper that inputs the three .tex
  fragments so cross-references resolve (build with latexmk/pdflatex).
- `extracted/node01_eval_extract.json` (r8/r9/r10) and
  `extracted/node03_eval_extract.json` (r6/r7/r8) — intermediate extraction
  results; r8 asserted cross-node identical. r5: archived point estimates only
  (episodes lost 2026-08-20), dagger-marked, no CI claimed.

## Regeneration
On node01 (paths relative to /workspace/agent_rl_paper_blueprint):
```
python3 paper/scripts_extract_eval_results.py outputs/experiments/d4-no-sha-20260819-node05 extracted/node01_eval_extract.json   # node01: r8/r9/r10
# node03 same command over its outputs dir -> node03_eval_extract.json (r6/r7/r8)
python3 paper/scripts_gen_results_table.py <node01.json> <node03.json> paper/curriculum_results/main_results_table
python3 paper/scripts_dump_pertask.py <node01.json> <node03.json>          # matrix for failure doc
python3 paper/scripts_dump_episode.py <episodes.jsonl> <task_id_substr>    # dossiers
```
Methodology mirrors src/mrpo/evaluation.py verbatim (percentile bootstrap, exact
McNemar, crc32-derived RNG seeds; crc32 here is RNG seed derivation, not a digest
check). Single-model CIs computed from paired.jsonl because the harness emits
comparisons only for multi-model runs.

## Provenance summary
- Episode artifacts: outputs/experiments/d4-no-sha-20260819-node05/eval-*
  (node01: r8/r9/r10; node03: r6/r7/r8; node02: r9/r10 backup).
- r5 point estimates: docs/experiment_archive_20260819.md + handoff r10.
- Qualitative failure narratives: archive §8-13, handoff 20260820.
