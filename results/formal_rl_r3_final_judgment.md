# Formal RL 第三轮冻结终判（2026-08-30）

本记录依照 `docs/formal_rl_prereg_v6_20260824.md` 第 5 节，在 seed 23、29、43
四臂训练及九套冻结评测全部完成后生成。所有分数和逐任务差值只读取各评测目录的
`paired.jsonl`；未使用 `summary.json` 的 comparisons 字段，也未计算或校验任何密码学摘要。

## 1. 完整性

- 三个种子仅使用 23、29、43；seed 17 未使用。
- 12 个训练 run 均完成 10/10 updates。
- 复制段 s29、s43 共 8 个评测 run 均出现 `ARM_EVAL_DONE`。
- 冻结评测没有传 `--max-turns`；b2dev 使用 split=dev，其余使用冻结 split。
- 终判脚本：容器 `/tmp/r3_final_judgment.py`，默认 seeds 23、29、43，paired bootstrap 2000 次、seed 7。

## 2. dsweep-L1 主量具

| Seed | mrpo | grpo-static-dr | no-fission | no-minimax | r10 |
|---:|---:|---:|---:|---:|---:|
| 23 | 16/32 | 17/32 | 16/32 | 21/32 | 15/32 |
| 29 | 15/32 | 14/32 | 18/32 | 21/32 | 15/32 |
| 43 | 17/32 | 17/32 | 16/32 | 20/32 | 15/32 |

## 3. H1-H3 冻结判定

预注册验收要求为三个种子方向一致，且合并逐任务 paired bootstrap 95% CI 不含 0。

| 假设 | 三种子差值（mrpo - 对照） | 合并差值 | 95% CI | 判定 |
|---|---|---:|---:|---|
| H1: mrpo > grpo-static-dr | -1, +1, 0 | 0 | [-0.0938, +0.0938] | FAIL |
| H2: mrpo > no-minimax | -5, -6, -3 | -14 | [-0.2604, -0.0312] | FAIL |
| H3: mrpo > no-fission | 0, -3, +1 | -2 | [-0.1042, +0.0625] | FAIL |

H2 不只是未通过：三个种子均为负向，合并 CI 完全低于 0。冻结证据显示移除 minimax
后性能更高。H1 与 H3 均无跨种子一致方向，合并 CI 包含 0。

## 4. 守门

旧五套件与 faultv2 两套件相对 r10 的合并 paired CI 均未出现完全低于 0 的显著回退，
因此守门通过，不触发一票否决。观察到的非零负向项均以 0 为 CI 上界：

- mrpo：fv2seen -2，CI [-0.1042, 0]；fv2held -1，CI [-0.0625, 0]。
- grpo-static-dr：fv2seen -4，CI [-0.1875, 0]；fv2held -1，CI [-0.0625, 0]。
- no-fission：fv2seen -1，CI [-0.0625, 0]。
- no-minimax：fv2seen -1，CI [-0.0625, 0]；fv2held -2，CI [-0.1042, 0]。
- no-minimax 在 b1fault 为 +1，CI [0, +0.3333]，不构成显著上行主张。

## 5. dsweep-L1 heldout

相对 r10 的三种子合并结果如下，此项按预注册单独报告，不并入 H1：

- mrpo：每种子 +3、+2、+2，CI [-0.0104, +0.1562]。
- grpo-static-dr：+3、+2、+5，CI [+0.0104, +0.1979]。
- no-fission：+3、+3、+5，CI [+0.0312, +0.1979]。
- no-minimax：+4、+5、+3，CI [+0.0521, +0.1979]。

MRPO 的 heldout CI 仍包含 0；其他三臂相对 r10 为正向，但这不是预注册的 MRPO
方法假设，也不改变 H1-H3 判定。

## 6. 冻结结论

H1、H2、H3 均不成立。依预注册诚实条款，本轮记录为：estimator-matched 后，MRPO
机制仍未产生可复现的行为优势；minimax 组件的三种子证据反而稳定负向。论文维持方法学
与负结果定位，不开启第四轮，不再通过更换量具寻找正结果。

后续工作限定为预注册后的收官项目：按 `docs/transfer_eval_plan_20260824.md` 执行零接触
迁移评测，并完成 Related Work，其中明确引用和对比 FISSION-GRPO（ACL 2026）。
