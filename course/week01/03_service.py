"""第 3 课：把检索做成服务。这才是算法工程的日常形态。

数据（CSV）→ 检索函数 → HTTP 接口 → 日志。
前端叫 /ask，车机以后也可以叫同一个接口。

在 PyCharm 里直接运行本文件即可，控制台需保持不关。
或在终端：python -m uvicorn 03_service:app --reload --port 8000
然后浏览器打开 http://127.0.0.1:8000/docs
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from search_lib import search

DATA_DIR = Path(__file__).parent / "data"
FAQ_PATH = DATA_DIR / "manual_faq.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("cockpit-faq")

faq = pd.read_csv(FAQ_PATH)
app = FastAPI(title="座舱手册问答 · 第 1 周基线", version="0.1.0")


class AskRequest(BaseModel):
    query: str
    top_k: int = 3


@app.get("/health")
def health() -> dict:
    return {"ok": True, "docs": int(len(faq))}


@app.post("/ask")
def ask(body: AskRequest) -> dict:
    started = time.perf_counter()
    ranked = search(faq, body.query, top_k=body.top_k)
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    top = ranked.iloc[0].to_dict() if not ranked.empty else None
    logger.info(
        "query=%s top_id=%s score=%s latency_ms=%s",
        body.query,
        None if top is None else top["id"],
        None if top is None else top["score"],
        elapsed_ms,
    )
    return {
        "query": body.query,
        "latency_ms": elapsed_ms,
        "results": ranked.to_dict(orient="records"),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
