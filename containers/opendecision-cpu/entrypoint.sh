#!/bin/sh
# Fetch the model into the shared cache first (idempotent — a second start finds it), then
# serve. Inside the container the bind is 0.0.0.0; the HOST binding is 127.0.0.1 only.
set -eu
python - <<'PY'
import os
from huggingface_hub import snapshot_download
model = os.environ.get("MODEL_ID", "MoritzLaurer/ModernBERT-large-zeroshot-v2.0")
print(f"[opendecision] ensuring {model} is in {os.environ.get('HF_HOME', '~/.cache')}", flush=True)
snapshot_download(model, allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model"])
PY
exec uvicorn opendecision.api.app:app --app-dir /app/src-repo/src --host 0.0.0.0 --port 8000
