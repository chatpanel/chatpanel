# Security policy

Please report vulnerabilities **privately** to **security@chatpanel.net** — not in a
public issue. Include the component (extension, bridge, gateway, desktop, redaction
engine), the version (`chrome://extensions` shows the extension's; `chatpanel-gateway
--version` / `GET http://127.0.0.1:4320/health` the gateway's), steps to reproduce, and
what you believe the impact is.

You will get an acknowledgement within 3 business days and a fix or a clear answer as
fast as the severity warrants. Reports that lead to a fix are credited in the release
notes if you wish.

**In scope:** anything that lets a web page, another extension or a remote party reach
the bridge or gateway, read conversations, notes or meetings, bypass redaction, escalate
what an agent is allowed to do, or exfiltrate data. Both the bridge and the gateway are
source-available (see the README) so you can read what you are reporting against.

**Out of scope:** issues in the third-party models or agents you connect (report those
upstream), and rate limits or availability of `api.chatpanel.net`.
