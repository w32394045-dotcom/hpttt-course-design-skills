#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""四方对照评测：同一个 prompt，四种供给方式，一次盲评排名

变体：
  original      —— 上游原版 SKILL.md（未改）
  mine          —— 我的 P0+R2 优化版（已 push 的 30a7d88）
  restructured  —— 重构版（步骤前置 + 方法下沉 references/）
  baseline      —— 不给 skill

关键设计：
- 四种产物都在**同一次**运行里生成，避免跨轮次的随机性让结论不可比
- 每个变体起独立进程；产物打乱顺序后交给独立评委，评委不知道哪个是哪个
- 评委一次给出 4 个排名 + 分数 + 各自缺什么
"""
import json
import os
import random
import re
import subprocess
import sys

BASE = os.path.expanduser("~/skills-optimize")
OUT = os.path.join(BASE, "_eval_compare")
os.makedirs(OUT, exist_ok=True)

VARIANTS = ["original", "mine", "restructured", "baseline"]
VARIANT_DIR = {"original": "upstream", "mine": "before", "restructured": "restructured"}


def llm(prompt, timeout=600):
    r = subprocess.run(["deepcode", "-x", "-p", prompt],
                       capture_output=True, text=True, timeout=timeout)
    return (r.stdout or "").strip()


def gen(skill_md, user_prompt):
    if skill_md is None:
        p = ("【用户请求】\n" + user_prompt +
             "\n\n请直接给出最终交付物，不要解释你在做什么。")
    else:
        p = ("你现在加载了下面这份技能说明书（skill），请严格按它的流程执行。\n\n"
             "<SKILL>\n" + skill_md + "\n</SKILL>\n\n"
             "----------\n\n【用户请求】\n" + user_prompt +
             "\n\n请直接给出最终交付物，不要复述技能说明书，不要解释你在做什么。")
    return llm(p)


JUDGE = """你是独立评审。同一个用户请求，下面有四份 AI 回复（A/B/C/D）。它们来自四种不同的做法，你不知道哪份对应哪种做法，也不要去猜。

【用户请求】
{task}

【这份请求期望达到的效果（评审依据）】
{expected}

{answers}

请严格按"期望达到的效果"逐条核对，给每一份打分（0-10 整数），并按好坏排序。
注意：不要被篇幅长短、排版花哨、看起来更努力所影响；只看是否真正满足期望。
如果某一份明显是在介绍方法而不是交付成果，直接给低分并说明。

只输出一个 JSON 对象，不要任何其它文字：
{{"scores": {{"A": 0, "B": 0, "C": 0, "D": 0}},
  "ranking": ["最好的字母", "次好", "再次", "最差"],
  "missing": {{"A": ["A 没做到的点"], "B": [], "C": [], "D": []}},
  "reason": "一段话说明排序依据"}}"""


def main():
    cfg = json.load(open(os.path.join(BASE, "_eval_compare_config.json"), encoding="utf-8"))
    summary = []
    for case in cfg["cases"]:
        slug = case["skill"]
        print("=" * 72)
        print("[%s] 生成 4 个变体 ..." % slug, flush=True)
        outs = {}
        for v in VARIANTS:
            md = None
            if v != "baseline":
                md = open(os.path.join(BASE, "_snapshots", VARIANT_DIR[v], slug + ".md"), encoding="utf-8").read()
            print("   %-14s ..." % v, flush=True)
            outs[v] = gen(md, case["prompt"])

        d = os.path.join(OUT, slug)
        os.makedirs(d, exist_ok=True)
        for v in VARIANTS:
            open(os.path.join(d, v + ".txt"), "w", encoding="utf-8").write(outs[v])

        votes = []
        for j in range(case.get("judges", 2)):
            rnd = random.Random(hash((slug, j, "shuffle")) & 0xFFFF)
            labels = VARIANTS[:]
            rnd.shuffle(labels)
            letter2v = {chr(65 + i): labels[i] for i in range(4)}
            blocks = []
            for i, v in enumerate(labels):
                blocks.append("【回复 %s】\n%s" % (chr(65 + i), outs[v]))
            raw = llm(JUDGE.format(task=case["prompt"], expected=case["expected"],
                                   answers="\n\n".join(blocks)))
            m = re.search(r"\{.*\}", raw, re.S)
            if not m:
                print("    judge %d: 解析失败" % (j + 1), flush=True)
                continue
            try:
                o = json.loads(m.group(0))
            except json.JSONDecodeError:
                print("    judge %d: JSON 失败" % (j + 1), flush=True)
                continue
            sc = {letter2v[k]: v for k, v in o.get("scores", {}).items() if k in letter2v}
            rk = [letter2v[x] for x in o.get("ranking", []) if x in letter2v]
            ms = {letter2v[k]: v for k, v in (o.get("missing") or {}).items() if k in letter2v}
            votes.append({"scores": sc, "ranking": rk, "missing": ms, "reason": o.get("reason", "")})
            print("    judge %d: %s | rank=%s" % (j + 1, sc, ">".join(rk)), flush=True)

        if not votes:
            print("  !! 全部评委失败", flush=True)
            continue
        tot = {v: [] for v in VARIANTS}
        pos = {v: [] for v in VARIANTS}
        for vt in votes:
            for v in VARIANTS:
                if vt["scores"].get(v) is not None:
                    tot[v].append(vt["scores"][v])
                if v in vt["ranking"]:
                    pos[v].append(vt["ranking"].index(v) + 1)
        avg = {v: (round(sum(tot[v]) / len(tot[v]), 2) if tot[v] else None) for v in VARIANTS}
        avgpos = {v: (round(sum(pos[v]) / len(pos[v]), 2) if pos[v] else None) for v in VARIANTS}
        rec = {"skill": slug, "avg_score": avg, "avg_rank": avgpos,
               "votes": votes, "variants": VARIANTS}
        summary.append(rec)
        print("  ==> 平均分 %s" % avg, flush=True)
        print("      平均名次 %s  (1=最好)" % avgpos, flush=True)

    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 72)
    print("%-24s %10s %10s %12s %10s" % ("skill", "original", "mine", "restructured", "baseline"))
    for r in summary:
        a = r["avg_score"]
        print("%-24s %10s %10s %12s %10s" % (r["skill"], a["original"], a["mine"],
                                             a["restructured"], a["baseline"]))


if __name__ == "__main__":
    main()
