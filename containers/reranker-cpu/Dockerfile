# ghcr.io/chatpanel/reranker-cpu — a CPU, multi-arch reranking server: BAAI/bge-reranker-v2-m3
# behind the same `/rerank` wire Text Embeddings Inference speaks.
#
# WHY THIS EXISTS. Hugging Face's Text Embeddings Inference and Infinity both publish
# amd64-only CPU images (re-checked 2026-09-22: ghcr.io/huggingface/text-embeddings-inference
# :cpu-latest is linux/amd64 alone), so neither runs on an arm64 laptop. This image is
# linux/amd64 + linux/arm64. On amd64, prefer the official TEI image — this one is the arm64
# answer, not a replacement.
#
# NOT AFFILIATED with Hugging Face, the TEI project, or BAAI. The model is BAAI/bge-reranker-v2-m3
# (its own licence); server.py is ChatPanel's, and small on purpose.
#
#   podman build -t ghcr.io/chatpanel/reranker-cpu:latest containers/reranker-cpu
#   podman run -d --name chatpanel-reranker -p 127.0.0.1:8889:8000 \
#     -v ~/.chatpanel/runtime/hf-cache:/data -e HF_HOME=/data ghcr.io/chatpanel/reranker-cpu
#   curl -s http://127.0.0.1:8889/rerank -H 'content-type: application/json' \
#     -d '{"query":"deep learning","texts":["cats","neural networks"]}'
FROM python:3.13-slim

LABEL org.opencontainers.image.source="https://github.com/chatpanel/chatpanel" \
      org.opencontainers.image.description="CPU (amd64+arm64) reranking server — BAAI/bge-reranker-v2-m3 behind the TEI /rerank wire. Unofficial; not affiliated with Hugging Face, TEI or BAAI." \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.vendor="ChatPanel"


ARG MODEL_ID=BAAI/bge-reranker-v2-m3

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/* \
 && useradd --create-home --uid 10001 reranker

WORKDIR /app
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch \
 && pip install --no-cache-dir "transformers>=4.45,<6" "fastapi>=0.115" "uvicorn>=0.30" huggingface_hub sentencepiece protobuf

ENV MODEL_ID=${MODEL_ID} \
    HF_HOME=/data \
    HF_HUB_DISABLE_TELEMETRY=1 \
    TOKENIZERS_PARALLELISM=false \
    PYTHONUNBUFFERED=1

COPY server.py entrypoint.sh /app/
RUN chmod 0755 /app/entrypoint.sh && mkdir -p /data && chown reranker:reranker /data

USER reranker
EXPOSE 8000
VOLUME ["/data"]
ENTRYPOINT ["/app/entrypoint.sh"]
