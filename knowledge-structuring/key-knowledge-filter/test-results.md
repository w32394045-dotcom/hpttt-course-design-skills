# test-results — key-knowledge-filter

> 阶段 4 压力测试结果 | 测试时间: 2026-08-04 | 方式: 独立 sub-agent 盲测（非 fallback）

## 结果: 首轮 5/6 (83%) → 修 skill 后重测通过 → 最终 6/6 (100%) ✅ 接受

### 首轮

| id | type | 预期 | 盲测结果 | 判定 |
|---|---|---|---|---|
| should-trigger-01 15个点砍哪些 | should_trigger | 调用本 skill, MECE→颗粒度→三指标 | chosen=key-knowledge-filter, 动作全中(含例外判断) | ✅ |
| should-trigger-02 业务方都要讲 | should_trigger | 调用本 skill, 打分表顶住压力 | chosen=key-knowledge-filter, 动作=打分表作对齐证据 | ✅ |
| should-trigger-03 半天课拆很细求认可 | should_trigger | 调用本 skill 做颗粒度校准 | chosen=**none** (理由: 求认可型提问, 无取舍诉求) | ❌ |
| should-not-trigger-01 (跨skill诱饵: 串模型) | should_not_trigger | 应触发 knowledge-modeling | chosen=knowledge-modeling | ✅ |
| should-not-trigger-02 (MECE名词解释) | should_not_trigger | none | chosen=none | ✅ |
| edge-01 (SOP流程不可改) | edge_case | 识别流程类例外, 不强行打分 | chosen=none, 理由="流程类是本skill明确排除项, 直接按流程讲"——未触发但正确识别例外且未强行打分, 符合边界预期 | ✅ |

### 失败分析与修复 (should-trigger-03)

- **根因**: skill 的 description 语言信号只覆盖"明确喊砍内容"的场景, 未覆盖工作坊高发的"拆得很细来求认可"的颗粒度求诊场景——盲测 agent 的 none 判断暴露了真实歧义。**判定: 修 skill, 非修测试**
- **修复**: description 增补"颗粒度求诊场景"信号 ("我拆得很细, 够专业吧""内容很全了吧" → 判断颗粒度与课时匹配); A2 场景与语言信号同步增补
- **重测** (干净 sub-agent, 附对照组): 失败用例 → chosen=key-knowledge-filter, 动作=不附和"专业"评价, 先做颗粒度诊断(半天配大颗粒, 少就是多) ✅; 对照组 (润色逐字稿) → none ✅ (修复未引入误触发)

### 终轮: 6/6 (100%)
