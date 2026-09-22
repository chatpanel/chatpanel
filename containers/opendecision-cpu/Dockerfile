# ghcr.io/chatpanel/opendecision-cpu — a CPU, multi-arch build of OpenDecision
# (github.com/deepanwadhwa/OpenDecision, Apache-2.0) as an HTTP service.
#
# WHY THIS EXISTS. Upstream publishes no container image at all. This is not a fork: it
# fetches upstream at a PINNED COMMIT and pip-installs it. What this adds is the packaging —
# CPU-only torch (the CUDA wheels are ~5 GB nobody on a laptop uses), a non-root user, and the
# model pre-fetched into the shared cache so the first decision loads from disk.
#
# NOT AFFILIATED with the OpenDecision project. Bugs in the model or the library belong
# upstream; bugs in this packaging belong here.
#
#   podman build -t ghcr.io/chatpanel/opendecision-cpu:latest containers/opendecision-cpu
#   podman run -d --name chatpanel-opendecision -p 127.0.0.1:8890:8000 \
#     -v ~/.chatpanel/runtime/hf-cache:/data -e HF_HOME=/data ghcr.io/chatpanel/opendecision-cpu
#   curl -s http://127.0.0.1:8890/health
FROM python:3.13-slim

LABEL org.opencontainers.image.source="https://github.com/chatpanel/chatpanel" \
      org.opencontainers.image.description="CPU (amd64+arm64) build of OpenDecision (deepanwadhwa/OpenDecision, Apache-2.0) as an HTTP service. Unofficial; not affiliated with the OpenDecision project." \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.vendor="ChatPanel"


ARG OPENDECISION_REPO=https://github.com/deepanwadhwa/OpenDecision.git
# Pinned to a commit: a moving `main` in an image is a supply-chain hole. Bump deliberately
# (upstream main on 2026-09-20, "readme update").
ARG OPENDECISION_REF=194dd112d5e52f5dfa35aeb43894303137cf5747
ARG MODEL_ID=MoritzLaurer/ModernBERT-large-zeroshot-v2.0

RUN apt-get update && apt-get install -y --no-install-recommends git curl && rm -rf /var/lib/apt/lists/* \
 && useradd --create-home --uid 10001 opendecision

WORKDIR /app
RUN git init -q src-repo && cd src-repo \
 && git fetch -q --depth 1 "${OPENDECISION_REPO}" "${OPENDECISION_REF}" && git checkout -q FETCH_HEAD && rm -rf .git && cd .. \
 && pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch \
 && pip install --no-cache-dir ./src-repo huggingface_hub
# The model is the gateway's choice (MODEL_ID), not upstream's constant — patch-model.py.
COPY patch-model.py /app/patch-model.py
RUN python /app/patch-model.py && pip install --no-cache-dir --no-deps ./src-repo

ENV MODEL_ID=${MODEL_ID} \
    HF_HOME=/data \
    HF_HUB_DISABLE_TELEMETRY=1 \
    TOKENIZERS_PARALLELISM=false \
    PYTHONUNBUFFERED=1

COPY entrypoint.sh /entrypoint.sh
RUN chmod 0755 /entrypoint.sh && mkdir -p /data && chown opendecision:opendecision /data

USER opendecision
EXPOSE 8000
VOLUME ["/data"]
HEALTHCHECK --interval=15s --timeout=5s --start-period=30s CMD curl -fsS http://127.0.0.1:8000/health || exit 1
ENTRYPOINT ["/entrypoint.sh"]
