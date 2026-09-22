# ghcr.io/chatpanel/vllm-cpu — vLLM's OpenAI-compatible server, built for CPU, amd64 + arm64.
#
# WHY THIS EXISTS. vLLM's official image (vllm/vllm-openai) is a CUDA build. It does publish an
# arm64 tag, but that is the Grace-Hopper/CUDA variant — ~9.7 GB compressed, re-checked
# 2026-09-22 — and it will not run on an arm64 laptop with no NVIDIA GPU. This is not a fork:
# it clones vLLM at a PINNED RELEASE TAG and follows vLLM's own CPU recipe
# (docker/Dockerfile.cpu) for the CPU backend — x86 with AVX-512, aarch64 with NEON.
#
# ON A GPU BOX, USE THE OFFICIAL IMAGE. Point the same Runtime service at vllm/vllm-openai
# (`runtime.services.vllm.image`). This image is the CPU/arm64 answer, not a replacement.
#
# NOT AFFILIATED with the vLLM project. Nothing of ChatPanel's runs inside — the entrypoint is
# vLLM's own API server, and the flags the gateway passes are vLLM's own (`vllm serve`).
#
#   podman build -t ghcr.io/chatpanel/vllm-cpu:latest containers/vllm-cpu   # long: torch + vLLM from source
#   podman run -d --name chatpanel-vllm -p 127.0.0.1:8891:8000 -v ~/.chatpanel/runtime/hf-cache:/data \
#     -e HF_HOME=/data -e VLLM_CPU_KVCACHE_SPACE=4 ghcr.io/chatpanel/vllm-cpu \
#     --model Qwen/Qwen3-0.6B --host 0.0.0.0 --port 8000
#   curl -s http://127.0.0.1:8891/v1/models
ARG VLLM_VERSION=v0.29.0
FROM python:3.12-slim AS build
ARG VLLM_VERSION
RUN apt-get update && apt-get install -y --no-install-recommends git build-essential cmake ninja-build libnuma-dev curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*
# Since 0.29 vLLM carries a Rust crate (vllm-rs) that setuptools-rust builds inside
# `pip install .`, so the build stage needs cargo — rustup pinned by the tree's own
# rust-toolchain.toml. The runtime image below carries none of this.
RUN curl -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path --profile minimal
ENV PATH=/root/.cargo/bin:$PATH CARGO_BUILD_JOBS=4
WORKDIR /src
RUN git clone --depth 1 --branch ${VLLM_VERSION} https://github.com/vllm-project/vllm.git .
# vLLM's own CPU recipe (docker/Dockerfile.cpu): the build requirements with CPU-only torch
# from PyTorch's CPU wheel index, the CPU runtime requirements, then vLLM for the CPU target.
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements/build/cpu.txt \
 && pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements/cpu.txt \
 && VLLM_TARGET_DEVICE=cpu pip install --no-cache-dir --no-build-isolation .

FROM python:3.12-slim
LABEL org.opencontainers.image.source="https://github.com/chatpanel/chatpanel" \
      org.opencontainers.image.description="vLLM OpenAI server built for CPU (amd64+arm64) from vLLM's own CPU recipe at a pinned tag. Unofficial; not affiliated with the vLLM project. On a GPU box use vllm/vllm-openai." \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.vendor="ChatPanel"
RUN apt-get update && apt-get install -y --no-install-recommends libnuma1 libgomp1 curl ffmpeg \
 && rm -rf /var/lib/apt/lists/* \
 && useradd --create-home --uid 10001 vllm
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /usr/local/bin/vllm /usr/local/bin/vllm
# The audio route needs the audio extras (librosa, soundfile); small, and only used by a whisper.
RUN pip install --no-cache-dir librosa soundfile
USER vllm
ENV HF_HOME=/data VLLM_CPU_KVCACHE_SPACE=4 VLLM_LOGGING_LEVEL=INFO
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=600s CMD curl -fsS http://127.0.0.1:8000/health || exit 1
ENTRYPOINT ["vllm", "serve"]
CMD ["Qwen/Qwen3-0.6B", "--host", "0.0.0.0", "--port", "8000"]
