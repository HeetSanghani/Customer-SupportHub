# 11. Quick Reply Architecture

## Quick Reply Engine
Instant deterministic lookup for generic questions (e.g. *"What payment methods do you support?"*).
- Prevents unnecessary LLM calls.
- Matches regex patterns before passing query to AI Router.
