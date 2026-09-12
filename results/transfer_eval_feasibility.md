# Zero-touch transfer evaluation feasibility audit (2026-08-30)

This audit follows `docs/transfer_eval_plan_20260824.md` after the formal-RL
round-three judgment was frozen. It does not alter any frozen result.

## ToolBench-X

- Public paper: arXiv:2606.25819.
- Public implementation: `Foreverskyou/ToolBench-X`.
- Published data: 1,106 tasks, 31.5 MB; 378 sequential, 358 parallel, and
  370 mixture tasks across five reliability-hazard categories.
- Runtime fit: the implementation uses the standard OpenAI chat-completions
  tool-call interface and a light dependency set. A local OpenAI-compatible
  Qwen3.5 service could therefore be connected without changing task data.
- Blocking condition: the dataset card explicitly prohibits copying,
  distribution, or modification without prior approval, including for the
  otherwise permitted academic-use setting. No author approval is available
  in the project record. The data was not downloaded.

## ToolMaze

- Public paper: arXiv:2606.05806 (CC BY 4.0 paper).
- Public implementation: `Zhudongsheng75/ToolMaze`.
- Published data: 119 MB, with C1-C4 DAG complexity and P0-P4 perturbation
  modes. The framework reports task success rate, perturbation recovery rate,
  and recovery cost.
- Runtime fit: the implementation advertises OpenAI, Anthropic, VLLM, and MCP
  agents, so a local Qwen3.5 backend is technically feasible.
- Blocking condition: the code repository exposes no LICENSE file and the
  Hugging Face dataset card declares no dataset license. The paper's CC BY
  license does not automatically license the code or task data. The code and
  data were not downloaded.

## Decision

The approved plan permits downgrading external transfer to citation-only when
the engineering path cannot be completed within one day. Here the blocker is
stronger than engineering effort: neither candidate can be copied into the
cluster under a clearly applicable license without additional author
permission. A partial reimplementation or hand-transcribed task subset would
not be a valid zero-touch benchmark evaluation and would violate the intended
protocol.

Accordingly, no external transfer score is reported. The paper must state the
licensing limitation explicitly, cite ToolBench-X and ToolMaze as evaluation
frameworks, and avoid implying that the controlled-environment findings have
been externally validated. If author permission or an explicit ToolMaze
software/data license is later obtained, the frozen final adapters may be
evaluated once without training or tuning on either benchmark.
