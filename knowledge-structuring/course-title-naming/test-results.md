# test-results — course-title-naming

> 阶段 4 压力测试结果 | 测试时间: 2026-08-04 | 方式: 独立 sub-agent 盲测（非 fallback）

## 结果: 6/6 通过 (100%) ✅ 接受

| id | type | 预期 | 盲测结果 | 判定 |
|---|---|---|---|---|
| should-trigger-01 课成了要起名 | should_trigger | 调用本 skill, 时机检查→三点式→终检 | chosen=course-title-naming, 动作=时机三项检查→痛点/利益/焦点判断→候选→名实一致终检 | ✅ |
| should-trigger-02 课名太平没人报名 | should_trigger | 调用本 skill, 三点式重构 | chosen=course-title-naming, 动作同上(含时机检查) | ✅ |
| should-not-trigger-01 (跨skill诱饵: 模型名) | should_not_trigger | 应触发 knowledge-modeling | chosen=knowledge-modeling | ✅ |
| should-not-trigger-02 (写课程简介) | should_not_trigger | none | chosen=none | ✅ |
| edge-01 (内容没想先要名) | edge_case | 拒绝命名+引导回 plan-course-4-steps | chosen=plan-course-4-steps ("命名时机未到, 应回到设计流程") | ✅ |
| edge-02 (强制合规培训要炸裂名) | edge_case | 提示边界: 清晰大于吸引 | chosen=none, 理由命中 B 段"强制参加的合规培训, 清晰大于吸引" | ✅ |

## 失败分析

无。"模型名 vs 课程名"这条最易混淆的跨 skill 诱饵正确分流; 两条 edge 的判停/边界理由均与 B 段一致。
