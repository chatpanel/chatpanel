# The reranker the gateway's Runtime starts (docs/capability-endpoints.md §4.7): a cross-encoder
# behind Text Embeddings Inference's wire — `POST /rerank { query, texts, raw_scores? }` →
# `[{ index, score }]` — so the gateway's `tei` adapter, and a user's real TEI box, are the
# same thing to a client. Exists because TEI and Infinity publish amd64-only CPU images and
# the owner's machines are arm64; this is the smallest server that speaks the shape.
import os
import threading
import time

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_ID = os.environ.get("MODEL_ID", "BAAI/bge-reranker-v2-m3")
MAX_LENGTH = int(os.environ.get("MAX_LENGTH", "512"))
BATCH = int(os.environ.get("BATCH", "16"))
torch.set_num_threads(int(os.environ.get("THREADS", str(max(1, (os.cpu_count() or 2) - 1)))))

app = FastAPI(title="chatpanel-reranker", version="0.1.0")
_state = {"ready": False, "error": None, "loaded_ms": None}
_lock = threading.Lock()
_model = {}


def _load():
    t0 = time.time()
    try:
        tok = AutoTokenizer.from_pretrained(MODEL_ID)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
        model.eval()
        _model["tok"], _model["model"] = tok, model
        _state["ready"], _state["loaded_ms"] = True, int((time.time() - t0) * 1000)
        print(f"[reranker] {MODEL_ID} ready in {_state['loaded_ms']} ms", flush=True)
    except Exception as e:  # noqa: BLE001 — the reason is what /health reports
        _state["error"] = f"{type(e).__name__}: {e}"
        print(f"[reranker] load failed: {_state['error']}", flush=True)


# Load in the background so the process answers /health at once — TEI reports 503 until
# the model is in; so do we, and the gateway's runtime waits on exactly that.
threading.Thread(target=_load, daemon=True).start()


class RerankRequest(BaseModel):
    query: str = Field(min_length=1)
    texts: list[str] = Field(min_length=1, max_length=1000)
    raw_scores: bool = False
    return_text: bool = False
    truncate: bool = True


@app.get("/health")
def health():
    if _state["error"]:
        raise HTTPException(status_code=500, detail=_state["error"])
    if not _state["ready"]:
        raise HTTPException(status_code=503, detail="model loading")
    return {"status": "ok"}


@app.get("/info")
def info():
    return {"model_id": MODEL_ID, "model_type": {"reranker": {}}, "max_input_length": MAX_LENGTH, "ready": _state["ready"], "loaded_ms": _state["loaded_ms"]}


@app.post("/rerank")
def rerank(req: RerankRequest):
    if _state["error"]:
        raise HTTPException(status_code=500, detail=_state["error"])
    if not _state["ready"]:
        raise HTTPException(status_code=503, detail="model loading")
    tok, model = _model["tok"], _model["model"]
    scores: list[float] = []
    with _lock, torch.inference_mode():
        for i in range(0, len(req.texts), BATCH):
            chunk = req.texts[i:i + BATCH]
            enc = tok([req.query] * len(chunk), chunk, padding=True, truncation=req.truncate, max_length=MAX_LENGTH, return_tensors="pt")
            logits = model(**enc).logits.view(-1).float()
            scores.extend((logits if req.raw_scores else torch.sigmoid(logits)).tolist())
    out = [{"index": i, "score": s, **({"text": t} if req.return_text else {})} for i, (s, t) in enumerate(zip(scores, req.texts))]
    out.sort(key=lambda r: r["score"], reverse=True)
    return out
