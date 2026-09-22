# Container images

Three small images ChatPanel's local gateway can start for you. They are **unofficial CPU
builds of other people's software**, published here because the official images do not cover
every machine — chiefly arm64 laptops.

**None of these is a fork.** Each is a build recipe: it fetches upstream at a pinned version
and packages it. The only code of our own is `reranker-cpu/server.py`, about a hundred lines.

| Image | What it is | Why it exists | Prefer the official image when… |
|---|---|---|---|
| `ghcr.io/chatpanel/reranker-cpu` | [BAAI/bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3) behind the `/rerank` wire that [Text Embeddings Inference](https://github.com/huggingface/text-embeddings-inference) speaks | TEI and Infinity publish **amd64-only** CPU images (re-checked 2026-09-22), so neither runs on arm64 | you are on amd64 → use `ghcr.io/huggingface/text-embeddings-inference:cpu-latest` |
| `ghcr.io/chatpanel/opendecision-cpu` | [OpenDecision](https://github.com/deepanwadhwa/OpenDecision) (Apache-2.0) as an HTTP service | upstream publishes **no image at all** | — there is no official image |
| `ghcr.io/chatpanel/vllm-cpu` | [vLLM](https://github.com/vllm-project/vllm)'s OpenAI server, built from vLLM's own CPU recipe | the official `vllm/vllm-openai` is a CUDA build; its arm64 tag is the Grace-Hopper/CUDA variant (~9.7 GB, re-checked 2026-09-22) and will not run without an NVIDIA GPU | you have a GPU → use `vllm/vllm-openai` and point `runtime.services.vllm.image` at it |

All are `linux/amd64` + `linux/arm64`, CPU-only, non-root, and published by
[`capability-images.yml`](../.github/workflows/capability-images.yml) on any change here.

**Not affiliated** with Hugging Face, BAAI, the OpenDecision project or the vLLM project. Each
image keeps its upstream licence; the recipes here are ours. Bugs in the underlying model or
library belong upstream — bugs in the *packaging* belong here.

## Build one yourself

```bash
podman build -t ghcr.io/chatpanel/reranker-cpu:latest containers/reranker-cpu
podman run -d --name chatpanel-reranker -p 127.0.0.1:8889:8000 \
  -v ~/.chatpanel/runtime/hf-cache:/data -e HF_HOME=/data ghcr.io/chatpanel/reranker-cpu
curl -s http://127.0.0.1:8889/rerank -H 'content-type: application/json' \
  -d '{"query":"deep learning","texts":["cats","neural networks"]}'
```

Each `Dockerfile` header carries its own build and run lines, and what the gateway does with
it. The gateway runs exactly those commands — nothing here is a second way to do it.

## Contributing

**Upstream moved and the pin is stale** is the most useful kind of PR, and the most common.
Every image pins its upstream deliberately — a moving `main` inside an image is a
supply-chain hole — so bumping one is a real change with a real diff:

- `vllm-cpu` → `ARG VLLM_VERSION` (a vLLM release tag)
- `opendecision-cpu` → `ARG OPENDECISION_REF` (a commit SHA, not a branch)
- `reranker-cpu` → `ARG MODEL_ID`, and the pinned ranges in the `pip install` line

Please say in the PR **which upstream version you moved to and that you built it locally** on
at least one architecture. CI builds both, so an arm64-only or amd64-only fix will show up.

Also welcome: a smaller image, a fix for a build that breaks on a new base image, a
`HEALTHCHECK` that reflects readiness better, or an official upstream image gaining arm64 —
in which case the right change may be **deleting one of these** and pointing the gateway at
the official one. That is a good outcome, not a loss.

Please do not add anything ChatPanel-specific to these images. They stay generic and useful on
their own; the gateway's opinions live in the gateway.
