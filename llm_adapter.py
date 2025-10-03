# backend/app/llm_adapter.py
"""
Pluggable adapter for LLM. Two modes:
- "api": call remote API (e.g., OpenAI) using env vars.
- "local": run llama.cpp binary (assumes installed on host) via subprocess.
"""
import os
import subprocess
import json
from typing import List, Dict, Optional

MODE = os.getenv("LLM_MODE", "api")  # "api" or "local"

# Simple API adapter (example: OpenAI)
def call_api(prompt: str, max_tokens=512) -> str:
    import requests
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}"}
    data = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }
    r = requests.post(url, headers=headers, json=data, timeout=60)
    r.raise_for_status()
    j = r.json()
    return j["choices"][0]["message"]["content"]

# Simple local llama.cpp adapter (needs llama.cpp + model)
def call_local(prompt: str, max_tokens=512) -> str:
    # assumes `llama.cpp` 'main' binary accessible as "llama"
    # and model path set in LLM_LOCAL_MODEL
    model = os.getenv("LLM_LOCAL_MODEL")
    if not model:
        raise RuntimeError("LLM_LOCAL_MODEL not set for local mode")
    cmd = ["./llama", "-m", model, "-p", prompt, "-n", str(max_tokens)]
    # run subprocess; for real usage consider streaming
    p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if p.returncode != 0:
        raise RuntimeError(f"llama failed: {p.stderr}")
    return p.stdout

def generate_reply(prompt: str) -> str:
    if MODE == "local":
        return call_local(prompt)
    else:
        return call_api(prompt)