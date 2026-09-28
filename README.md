# Chap by ChatPanel

[<img src="https://chatpanel.net/assets/chrome-web-store-badge.png" alt="Available in the Chrome Web Store" height="56">](https://chromewebstore.google.com/detail/icemacffhbgnfoofclgdbcdmnlkkklem)
[<img src="https://chatpanel.net/assets/edge-badge.svg" alt="Get it from Microsoft Edge Add-ons" height="56">](https://microsoftedge.microsoft.com/addons/detail/jkmmbleapaognlonbnllpaoeibmfkjmp)
[<img src="https://chatpanel.net/assets/firefox-badge.svg" alt="Get the add-on for Firefox" height="56">](https://addons.mozilla.org/en-US/firefox/addon/chatpanel-privacy-first-ai/)

**Chap** ("Hey Chap") is your AI agent for work, from **ChatPanel**: a **privacy-first AI side
panel** for Firefox / Chrome / Edge / Brave / Arc — and a desktop app, a terminal client and
phone apps — that lets you chat with **multiple AI agents from any tab**: the coding
agents already on your machine (**Claude Code**, **Codex**, **Antigravity CLI**) *and*
**any model or API you bring** (local Ollama / LM Studio, or a hosted OpenAI-/Anthropic-
compatible endpoint). Full chat history, tab/URL context, notes, meetings, custom agents
& skills — all local-first, with on-device redaction before anything reaches a cloud model.

**This is the home for issues, feature requests and release notes.**

## Install

| | |
|---|---|
| **Firefox** | [addons.mozilla.org](https://addons.mozilla.org/en-US/firefox/addon/chatpanel-privacy-first-ai/) |
| **Chrome**, Brave, Arc | [Chrome Web Store](https://chromewebstore.google.com/detail/icemacffhbgnfoofclgdbcdmnlkkklem) |
| **Edge** | [Edge Add-ons](https://microsoftedge.microsoft.com/addons/detail/jkmmbleapaognlonbnllpaoeibmfkjmp) |
| **Local agents** (Claude Code, Codex, …) | `curl -fsSL https://dl.chatpanel.net/install.sh \| sh` — see [chatpanel.net/#install](https://chatpanel.net/#install) |

## What we guarantee — and how you check it

The code is not public: the extension, the bridge, the gateway and the desktop app ship as
ordinary, minified JavaScript. What is public is a set of guarantees you can verify on
your own machine, without trusting us:

| Guarantee | How to check it yourself |
|---|---|
| **The extension** talks only to the model endpoint you configured, your local bridge/gateway, and `api.chatpanel.net` for the licence check (never chat content). | DevTools on the side panel (right-click → Inspect → **Network**): every request it makes is listed. Any other host is a bug. |
| **The gateway** contacts only the hosts it declares — your model upstreams, `dl.chatpanel.net`/`huggingface.co` for model weights, `api.chatpanel.net` for the licence, the npm registry for the update check. | `chatpanel-gateway --audit` prints every host it has actually reached since it started **and** every host your config allows, with the reason, what is sent, and the switch that turns it off. Same data on the extension's Gateway tab. |
| **The bridge** listens on `127.0.0.1` only and sends nothing anywhere itself — it drives the coding agents you already have, with your own logins. | `lsof -i -P \| grep chatpanel` shows one loopback listener. Every outbound connection belongs to your agent, not the bridge. |
| **Redaction runs on your machine** before anything reaches a cloud model. | The engine is the one readable piece, on purpose: [chatpanel/chatpanel-pii](https://github.com/chatpanel/chatpanel-pii) ([PolyForm Shield](https://polyformproject.org/licenses/shield/1.0.0/)), and it is vendored unchanged into the extension. |
| **No telemetry.** | The [privacy policy](https://chatpanel.net/privacy.html) is what each store reviews the package against. |

If any of these is ever untrue on your machine, that is a security bug — see
[SECURITY.md](SECURITY.md).

## Bugs, ideas, questions

- **Bug or feature request:** [open an issue](../../issues/new/choose).
- **Security:** please do **not** open a public issue — see [SECURITY.md](SECURITY.md).
- **Privacy questions:** privacy@chatpanel.net · [FAQ](https://chatpanel.net/faq.html)

## Trademarks

"ChatPanel" and the ChatPanel logo are trademarks and are **not** licensed for use in
forks, repackaged builds or competing products.
