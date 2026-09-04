"""第 2 周第 1 课：错误分析。

不改打分规则。把每道评测题的第一名、重叠词、错误类型打出来。
你会看到：近义词对不上、万能词抢分、两条手册互相抢。

运行（解释器仍用 week01 的 .venv）：
  打开本文件，运行。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

WEEK01 = Path(__file__).resolve().parent.parent / "week01"
sys.path.insert(0, str(WEEK01))

from search_lib import search, tokenize

DATA_DIR = Path(__file__).parent / "data"
FAQ_PATH = DATA_DIR / "manual_faq.csv"
EVAL_PATH = DATA_DIR / "eval_set.json"


def guess_error_type(query: str, expected, got, score: int) -> str:
    if expected is None or got is None:
        return "手册缺失"
    q = tokenize(query)
    exp = tokenize(f"{expected.question} {expected.answer} {expected.keywords}")
    got_g = tokenize(f"{got.question} {got.answer} {got.keywords}")
    if not (q & exp) and (q & got_g):
        return "近义词 / 字面不对齐"
    if "怎么" in query and score <= 2:
        return "万能词抢分"
    if got.module != expected.module:
        return "模块抢答"
    return "其他字面重合"


def main() -> None:
    faq = pd.read_csv(FAQ_PATH)
    eval_set = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    faq_by_id = {row.id: row for row in faq.itertuples(index=False)}

    hits = 0
    print(f"手册 {len(faq)} 条，评测 {len(eval_set)} 题")
    print()

    for item in eval_set:
        ranked = search(faq, item["query"], top_k=3)
        top = ranked.iloc[0]
        ok = top["id"] in item["relevant_ids"]
        hits += int(ok)
        expected_id = item["relevant_ids"][0]
        expected = faq_by_id.get(expected_id)
        got = faq_by_id.get(top["id"])
        mark = "OK" if ok else "MISS"
        print(f"[{mark}] {item['qid']}  {item['query']}")
        print(f"      期望 {expected_id} {'' if expected is None else expected.question}")
        print(f"      实际 {top['id']} score={top['score']} overlap=[{top['overlap']}]")
        if not ok:
            print(f"      类型 {guess_error_type(item['query'], expected, got, int(top['score']))}")
            print(f"      备注 {item.get('note', '')}")
        print()

    print(f"第2周命中率: {hits}/{len(eval_set)} = {hits / len(eval_set):.0%}")
    print("第1周旧8题基线仍是 6/8 = 75%。对照的是同一套打分，只是手册和题变多了。")


if __name__ == "__main__":
    main()
