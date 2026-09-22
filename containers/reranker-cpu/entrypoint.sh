#!/bin/sh
# Fetch the model into the shared cache first (idempotent), then serve. The bind inside the
# container is 0.0.0.0; the HOST binding is 127.0.0.1 only.
set -eu
python - <<'PY'
import os
from huggingface_hub import snapshot_download
model = os.environ.get("MODEL_ID", "BAAI/bge-reranker-v2-m3")
print(f"[reranker] ensuring {model} is in {os.environ.get('HF_HOME', '~/.cache')}", flush=True)
snapshot_download(model, allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model", "sentencepiece*"])
PY
exec uvicorn server:app --app-dir /app --host 0.0.0.0 --port 8000
