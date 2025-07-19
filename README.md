#  Basic‑AI‑Agent

A minimal, end‑to‑end example of how to implement  **LLM function‑calling agent** (powered by Google Gemini) that can:

* list, read, write, and execute python codes inside an isolated *working directory*;
* iteratively refine a target codebase (in this demo: a CLI calculator);
* run its own tests to validate changes.

The goal is to show the smallest fully‑working agent.

---

##  Demo walk‑through

```bash
# 1  Clone & install
git clone https://github.com/meli-h/Basic-AI-Agent-.git
cd Basic-AI-Agent-
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # or  “uv pip install -r …”

# 2  Add your Gemini key
echo "GEMINI_API_KEY=YOUR_KEY_HERE" > .env

# 3  Ask the agent to improve the calculator
python main.py "Add exponentiation (^) support to the calculator and update tests"
