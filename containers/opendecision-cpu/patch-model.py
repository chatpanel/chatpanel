# Upstream hardcodes its model; the gateway's Runtime picks one from a catalogue (or a
# Hugging Face id) and passes it as MODEL_ID — the one-line patch that makes that real.
# Fails the build loudly when upstream moves the line, so a re-pin is deliberate.
import re
import pathlib

p = pathlib.Path("/app/src-repo/src/opendecision/engine.py")
s = p.read_text()
s2 = re.sub(r'^DEFAULT_MODEL = "([^"]+)"$', r'import os\nDEFAULT_MODEL = os.environ.get("MODEL_ID", "\1")', s, count=1, flags=re.M)
assert s2 != s, "DEFAULT_MODEL line not found in engine.py — upstream moved; re-pin deliberately"
p.write_text(s2)
print("[opendecision] DEFAULT_MODEL now reads MODEL_ID")
