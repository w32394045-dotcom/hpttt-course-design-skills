# HPTTT 课程设计技能包 · Course Design Skills

> 从《换种教法：高绩效培训师精进之道》(HPTTT) 第七章「课程设计四步骤」蒸馏出的 4 个可执行 Agent Skill。

## 这是什么

培训师设计课程时最常卡在四个地方：不知从何开始、内容太多砍不动、知识点串不成模型、课名起得不吸引人。这个仓库把王志刚《换种教法：高绩效培训师精进之道》（电子工业出版社, 2019）第七章的方法论，蒸馏成 4 个**可被 AI Agent 直接调用**的技能，在工作坊带教和课程开发场景中即装即用。

## 四个技能

| Skill | 解决什么问题 | 一句话说明 |
|---|---|---|
| [`plan-course-4-steps`](knowledge-structuring/plan-course-4-steps/SKILL.md) | 要设计新课，不知从何开始 | 课程设计总流程：定目标 → 罗列 → 筛选 → 结构化+命名 |
| [`key-knowledge-filter`](knowledge-structuring/key-knowledge-filter/SKILL.md) | 内容太多，不知道砍哪些 | MECE 罗列 + 颗粒度校准 + 重要性/难度/频率三指标打分，收敛到 ≤6 个关键知识点 |
| [`knowledge-modeling`](knowledge-structuring/knowledge-modeling/SKILL.md) ★ | 关键知识点串不成模型 | 四种结构化方式（字母/流程/金字塔/公式）+ 选择地图 + 目标校验 |
| [`course-title-naming`](knowledge-structuring/course-title-naming/SKILL.md) | 课设计完了，想起个好名字 | 好莱坞大片式命名：痛点/焦点/利益点三点式 |

★ knowledge-modeling 已经过两轮优化迭代（检查点显性标记 + 异常 fallback 速查表，记录见 [results.tsv](results.tsv)）。

---

## ⚠️ 实测报告：这 4 个 skill 相对「不给 skill」没有优势

2026-09-27 用独立子 agent 做了盲评对照。**结果与仓库原先的宣称不符，如实记录如下。**

### 方法

同一个用户请求，在**同一次运行内**生成四种产物，打乱顺序后交独立进程评委盲评——评委不知道哪份对应哪种做法，也不知道哪份带了 skill。每个变体 2 位评委。

| 变体 | 说明 |
|---|---|
| `original` | 本仓库上一版（RIA++ 六段结构，方法论在前） |
| `mine` | 中途一轮「补检查点 / 补 fallback 表 / 补审计字段」的改动 |
| `restructured` | **本版**（步骤前置 + 方法论下沉 `references/`） |
| `baseline` | **不提供任何 skill**，把同一请求直接交给模型 |

### 结果

| Skill | original | mine | restructured | baseline |
|---|---|---|---|---|
| plan-course-4-steps | 7.0 | 1.5 | 7.5 | **9.0** |
| key-knowledge-filter | 7.5 | 6.0 | 8.5 | **9.0** |
| knowledge-modeling | 4.0 | 3.0 | 9.0 | **9.0** |
| course-title-naming | 3.0 | 5.0 | **10.0** | 9.5 |
| **平均** | 5.38 | **3.88** | 8.75 | **9.12** |

### 三条结论

1. **本版重构显著优于上一版**：+0.5 / +1.0 / +5.0 / +7.0，平均 **+3.38**。这次改动本身是有效的。
2. **中途那轮「补结构」的改动是有害的**：`mine` 在 4/4 个 skill 上都是最差或次差（平均 3.88，全场最低）。
3. **但没有任何版本打赢「不给 skill」**：8.75 vs 9.12。这四个任务（设计课程、砍知识点、串模型、起课名）本就在模型原生能力范围内。

具体证据：`key-knowledge-filter` 那一测里，**baseline 自己就用了「重要性 / 难度 / 频率」三指标打分**——这部分方法论属于模型的原生能力，不需要 skill 来教。

### 本版改了什么（为什么它比上一版好）

上一版把方法论放在前面（R 原文 / I 骨架 / A1 案例 / A2 场景 四章合起来占全文九成），真正的执行步骤 `E` 只占末尾 20 行。模型读完一大篇方法论后，会**抄 I 段那张「四种结构化方式」表格当答案，跳过流程**。

实测里 `mine` 版输出的是「**CHAIN 成交链**」——硬凑英文缩写，正是这个 skill 自己写在第 B 段警告要避免的坑。

本版把结构改成 `交付物 → 完成判据 → 执行步骤 → 边界 → 背景指针`，方法论下沉到 `references/method-context.md`，并把「凑不出与主题吻合的词就换方式」这类警告**从 B 段搬到决策点旁边**。改完后同一个请求，模型写出的是：

> 字母式已尝试并**放弃**：取首字、拼音首字母、英文首字母都拼不出与销售主题吻合的词。硬拼一个无意义缩写，比没有结构更糟，故换流程式。

### 局限（别把这组数字当定论）

- **样本很小**：每个 skill 只测了 1 个请求 × 2 位评委；同一变体跨轮次波动可达 2 分。
- **评分标准偏「通用质量」**，没有严格考核「是否照王志刚特有的步骤走」。换一套考方法一致性的题，结论可能不同。
- 因此：**「本版优于上一版」可信度较高**（4/4 一致）；**「打不过 baseline」要打折扣**。

### 复现

评测脚本 [`eval_compare.py`](knowledge-structuring/eval-2026-09-27/eval_compare.py)、配置 [`config.json`](knowledge-structuring/eval-2026-09-27/config.json)、以及**全部原始产出**（四变体并排，可自行核对评委有没有判错）都在 [`knowledge-structuring/eval-2026-09-27/`](knowledge-structuring/eval-2026-09-27/)。逐条评分记录见 [`results.tsv`](results.tsv)。

---

## 安装

把整个 skill 目录复制到**你所用的 skills-compatible runtime** 的 skills 目录即可：

```bash
# 用户级（把 <skills-dir> 换成下表里你的 runtime 对应目录）
cp -r knowledge-structuring/plan-course-4-steps \
      knowledge-structuring/key-knowledge-filter \
      knowledge-structuring/knowledge-modeling \
      knowledge-structuring/course-title-naming <skills-dir>/

# 只装单个
cp -r knowledge-structuring/<skill-slug> <skills-dir>/
```

常见 runtime 的用户级 skills 目录：

| Runtime | 用户级 skills 目录 |
|---|---|
| Claude Code | `~/.claude/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` |
| 其他 skills-compatible runtime (Codex / Cursor / OpenClaw / Hermes 等) | 见该 runtime 文档；只要目标目录内含 `SKILL.md`，即可被加载 |

项目级：把 `<skill-slug>/` 放进 `<your-project>/.<runtime>/skills/`（如 `<your-project>/.claude/skills/`）。

> 四个 skill 都是自包含的：术语定义、检查点、fallback 路径全部内联在各自 `SKILL.md` 里。`GLOSSARY.md` / `verified.md` / `candidates/` 是蒸馏审计产物，仅供追溯，**不是运行依赖**，无需一并复制。

装完后，对 agent 说一句触发场景即可，例如：
- "我想做一门给新经理的课，不知从何下手" → 触发 plan-course-4-steps
- "我筛出了 5 个关键知识点，怎么串成模型？" → 触发 knowledge-modeling

## 仓库结构

```
hpttt-course-design-skills/
├── README.md                   # 本文件
├── results.tsv                 # 优化日志 + 实测评分记录（全仓库共用一份）
└── knowledge-structuring/      # 蒸馏工作区（含完整审计轨迹）
    ├── INDEX.md                # 技能总览 + 引用关系图 + 学习顺序
    ├── DIGEST.md               # 第七章精华长文（约 6500 字，不读原书看这篇）
    ├── GLOSSARY.md             # 18 条共享术语词典（审计用，非运行依赖）
    ├── BOOK_OVERVIEW.md        # 整章理解（骨架/批判/应用潜力）
    ├── verified.md             # 三重验证记录（哪些方法论值得做成技能）
    ├── candidates/             # 原始候选池（89 条：框架/原则/案例/反例/术语）
    ├── rejected/               # 未独立成技能的单元及原因
    ├── source_text.txt         # 第七章全文（蒸馏源文本）
    ├── result-card.html        # 优化成果卡片
    ├── eval-2026-09-27/        # 实测原始产出（四变体并排）+ 评测脚本，可复现
    └── <skill-slug>/           # 四个 skill，每个目录可独立复制安装
        ├── SKILL.md            # 技能本体：交付物 → 完成判据 → 执行步骤 → 边界
        ├── references/
        │   └── method-context.md  # 方法论原文、书中案例、作者盲点（执行时不必读）
        ├── test-prompts.json   # 测试用例（标准格式：对象 + test_cases）
        └── test-results.md     # 触发/路由盲测结果与失败分析
```

## 质量标准

| 关 | 测什么 | 方式 | 结果 |
|---|---|---|---|
| 三重验证 | 这条方法论值不值得做成技能 | 跨域佐证 / 预测力 / 独特性 | 通过 |
| 触发测试 | **该不该调用这个 skill**（路由是否走对） | 独立 sub-agent 盲测，含跨技能诱饵 | 4 个 skill 均 100% 通过，明细见各目录 `test-results.md` |
| 产出质量实测 | **调用之后，产出是否真的更好** | 四变体同轮盲评，对照「不给 skill」 | ⚠️ **未打赢 baseline，见上方实测报告** |

> 请注意区分第二关和第三关：**触发测试 100% 通过，只说明「该调用的时候调用对了」，不代表产出的质量比不调用更好。** 本仓库此前把两者混为一谈，现已分开列出。

## 作者与版权

- 原书作者：王志刚，绩效改进专家，《换种教法：高绩效培训师精进之道》(HPTTT)，电子工业出版社，2019
- 本仓库为作者本人对其著作方法论的 Agent 化蒸馏成果
