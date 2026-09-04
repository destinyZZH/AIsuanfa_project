"""第 2 课：读手册 CSV，做关键词检索，并打分。

算法工程的第一天不是训练模型，是：
数据进来 → 规则/模型处理 → 给出可对比的结果。

这里的检索很笨（关键词重叠），但它是后面 Embedding 检索的基线。
没有基线，后面说「效果好了」就是空话。

运行：python 02_search_faq.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from search_lib import search

DATA_DIR = Path(__file__).parent / "data"
FAQ_PATH = DATA_DIR / "manual_faq.csv"
EVAL_PATH = DATA_DIR / "eval_set.json"


def evaluate(faq: pd.DataFrame, eval_set: list[dict]) -> dict:
    """命中率：评测集里，第一条结果是否落在标注的 relevant_ids。"""
    hits = 0
    rows = []
    for item in eval_set:
        ranked = search(faq, item["query"], top_k=1)
        top_id = ranked.iloc[0]["id"] if not ranked.empty else None
        ok = top_id in item["relevant_ids"]
        hits += int(ok)
        rows.append(
            {
                "qid": item["qid"],
                "query": item["query"],
                "top_id": top_id,
                "ok": ok,
            }
        )
    total = len(eval_set)
    return {
        "hit_rate": hits / total if total else 0.0,
        "hits": hits,
        "total": total,
        "detail": rows,
    }


def main() -> None:
    faq = pd.read_csv(FAQ_PATH)
    print(f"手册条数: {len(faq)}")
    print(faq[["id", "module", "question"]].to_string(index=False))
    print()

    demo_query = "玻璃起雾了怎么处理"
    print(f"示例查询: {demo_query}")
    print(search(faq, demo_query).to_string(index=False))
    print()

    eval_set = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    report = evaluate(faq, eval_set)
    print(
        f"基线命中率: {report['hits']}/{report['total']} = {report['hit_rate']:.0%}"
    )
    for row in report["detail"]:
        mark = "OK" if row["ok"] else "MISS"
        print(f"  [{mark}] {row['qid']} {row['query']} -> {row['top_id']}")

    print()
    print("记住这个命中率。第 5 周用 Embedding 时，必须超过它才算进步。")


if __name__ == "__main__":
    main()
