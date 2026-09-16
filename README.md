# ChatPanel

[<img src="https://chatpanel.net/assets/chrome-web-store-badge.png" alt="Available in the Chrome Web Store" height="56">](https://chromewebstore.google.com/detail/icemacffhbgnfoofclgdbcdmnlkkklem)
[<img src="https://chatpanel.net/assets/edge-badge.svg" alt="Get it from Microsoft Edge Add-ons" height="56">](https://microsoftedge.microsoft.com/addons/detail/jkmmbleapaognlonbnllpaoeibmfkjmp)
[<img src="https://chatpanel.net/assets/firefox-badge.svg" alt="Get the add-on for Firefox" height="56">](https://addons.mozilla.org/en-US/firefox/addon/chatpanel-privacy-first-ai/)

A **privacy-first AI side panel** for Firefox / Chrome / Edge / Brave / Arc — and a
desktop app — that lets you chat with **multiple AI agents from any tab**: the coding
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

## Where the source is

The parts that run on your machine with access to your data are **source-available**
under the [PolyForm Shield 1.0.0](https://polyformproject.org/licenses/shield/1.0.0/)
license, so you can read exactly what they do:

| Component | Repo | What it is |
|---|---|---|
| **Local bridge** | [chatpanel/chatpanel-bridge](https://github.com/chatpanel/chatpanel-bridge) | The localhost process that talks to your coding agents. Listens on `127.0.0.1` only; uses your existing logins; no telemetry. |
| **Redaction engine** | [chatpanel/chatpanel-pii](https://github.com/chatpanel/chatpanel-pii) | Strips personal data before anything reaches a cloud model. Runs client-side. |
| **Privacy gateway** | [chatpanel/chatpanel-gateway](https://github.com/chatpanel/chatpanel-gateway) | Optional localhost proxy for routing and redaction across clients. |

The extension itself ships as ordinary, minified JavaScript: unpack it from
`chrome://extensions` and every network call it *can* make is there to see; the browser's
DevTools shows every one it *does* make. What it promises is in the
[privacy policy](https://chatpanel.net/privacy.html), which each store reviews against the
package.

## Bugs, ideas, questions

- **Bug or feature request:** [open an issue](../../issues/new/choose).
- **Security:** please do **not** open a public issue — see [SECURITY.md](SECURITY.md).
- **Privacy questions:** privacy@chatpanel.net · [FAQ](https://chatpanel.net/faq.html)

## Trademarks

"ChatPanel" and the ChatPanel logo are trademarks and are **not** licensed for use in
forks, repackaged builds or competing products.
