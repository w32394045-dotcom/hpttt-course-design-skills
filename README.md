# HPTTT 课程设计技能包 · Course Design Skills

> 从《换种教法：高绩效培训师精进之道》(HPTTT) 第七章「课程设计四步骤」蒸馏出的 4 个可执行 Agent Skill。
> 蒸馏流水线: [cangjie-skill](https://github.com/kangarooking/cangjie-skill) | 自动进化: [darwin-skill](https://github.com/alchaincyf/darwin-skill)

## 这是什么

培训师设计课程时最常卡在四个地方：不知从何开始、内容太多砍不动、知识点串不成模型、课名起得不吸引人。这个仓库把王志刚《换种教法：高绩效培训师精进之道》（电子工业出版社, 2019）第七章的方法论，蒸馏成 4 个**可被 AI Agent 直接调用**的技能，在工作坊带教和课程开发场景中即装即用。

## 四个技能

| Skill | 解决什么问题 | 一句话说明 |
|---|---|---|
| [`plan-course-4-steps`](knowledge-structuring/plan-course-4-steps/SKILL.md) | 要设计新课，不知从何开始 | 课程设计总流程：定目标 → 罗列 → 筛选 → 结构化+命名 |
| [`key-knowledge-filter`](knowledge-structuring/key-knowledge-filter/SKILL.md) | 内容太多，不知道砍哪些 | MECE 罗列 + 颗粒度校准 + 重要性/难度/频率三指标打分，收敛到 ≤6 个关键知识点 |
| [`knowledge-modeling`](knowledge-structuring/knowledge-modeling/SKILL.md) ★ | 关键知识点串不成模型 | 四种结构化方式（字母/流程/金字塔/公式）+ 选择地图 + 目标校验 |
| [`course-title-naming`](knowledge-structuring/course-title-naming/SKILL.md) | 课设计完了，想起个好名字 | 好莱坞大片式命名：痛点/焦点/利益点三点式 |

★ knowledge-modeling 已经过 darwin-skill 两轮自动进化（检查点显性标记 + 异常 fallback 速查表，进化记录见 [results.tsv](results.tsv)）。

## 安装

把整个 skill 目录复制到宿主的 skills 目录即可：

```bash
# WorkBuddy（用户级）
cp -r knowledge-structuring/plan-course-4-steps ~/.workbuddy/skills/
cp -r knowledge-structuring/key-knowledge-filter ~/.workbuddy/skills/
cp -r knowledge-structuring/knowledge-modeling ~/.workbuddy/skills/
cp -r knowledge-structuring/course-title-naming ~/.workbuddy/skills/

# Claude Code（用户级）
cp -r knowledge-structuring/<skill-slug> ~/.claude/skills/

# 项目级
cp -r knowledge-structuring/<skill-slug> <your-project>/.claude/skills/
```

装完后，对 agent 说一句触发场景即可，例如：
- "我想做一门给新经理的课，不知从何下手" → 触发 plan-course-4-steps
- "我筛出了 5 个关键知识点，怎么串成模型？" → 触发 knowledge-modeling

## 仓库结构

```
knowledge-structuring/          # 蒸馏工作区（含完整审计轨迹）
├── INDEX.md                    # 技能总览 + 引用关系图 + 学习顺序
├── DIGEST.md                   # 第七章精华长文（约 6500 字，不读原书看这篇）
├── GLOSSARY.md                 # 18 条共享术语词典
├── BOOK_OVERVIEW.md            # 整章理解（骨架/批判/应用潜力）
├── verified.md                 # 三重验证记录（哪些方法论值得做成技能）
├── candidates/                 # 原始候选池（89 条：框架/原则/案例/反例/术语）
├── rejected/                   # 未独立成技能的单元及原因
├── source_text.txt             # 第七章全文（蒸馏源文本）
├── result-card.html            # darwin 进化成果卡片
├── <skill-slug>/
│   ├── SKILL.md                # 技能本体（RIA++ 六段结构）
│   ├── test-prompts.json       # 压力测试用例（darwin 兼容格式）
│   └── test-results.md         # 盲测通过率与失败分析
└── results.tsv                 # darwin 进化日志
```

## 质量标准

每个技能都过了三道关：

1. **三重验证**（跨域佐证 / 预测力 / 独特性）——筛掉常识和空话
2. **压力测试**（独立 sub-agent 盲测，含跨技能诱饵）——4 个技能全部 100% 通过
3. **darwin 进化**（9 维 rubric + paired 盲评投票 + git 棘轮）——核心技能 knowledge-modeling 两轮优化全保留

## 作者与版权

- 原书作者：王志刚，绩效改进专家，《换种教法：高绩效培训师精进之道》(HPTTT)，电子工业出版社，2019
- 本仓库为作者本人对其著作方法论的 Agent 化蒸馏成果
- 蒸馏工具链：[cangjie-skill](https://github.com/kangarooking/cangjie-skill)（拆书蒸馏）× [darwin-skill](https://github.com/alchaincyf/darwin-skill)（技能进化）
