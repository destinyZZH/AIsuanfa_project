"""第 1 周检索实现，给脚本和服务共用。"""

from __future__ import annotations

import pandas as pd


def tokenize(text: str) -> set[str]:
    cleaned = (
        text.lower()
        .replace("?", "")
        .replace("？", "")
        .replace("。", " ")
        .replace(",", " ")
        .replace("，", " ")
    )
    parts = [p for p in cleaned.split() if p]
    grams: set[str] = set(parts)
    compact = "".join(parts)
    for i in range(len(compact) - 1):
        grams.add(compact[i : i + 2])
    return grams


def search(faq: pd.DataFrame, query: str, top_k: int = 3) -> pd.DataFrame:
    q_grams = tokenize(query)
    scored = []
    for row in faq.itertuples(index=False):
        doc_grams = tokenize(f"{row.question} {row.answer} {row.keywords}")
        overlap = q_grams & doc_grams
        scored.append(
            {
                "id": row.id,
                "module": row.module,
                "question": row.question,
                "answer": row.answer,
                "score": len(overlap),
                "overlap": " ".join(sorted(overlap)),
            }
        )
    result = pd.DataFrame(scored).sort_values("score", ascending=False)
    return result.head(top_k).reset_index(drop=True)
