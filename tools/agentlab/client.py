#!/usr/bin/env python3
"""Minimal client for the one endpoint that answers without credentials (measured 2026-10-02)."""
import json, time, urllib.request, urllib.error

URL = "https://opencode.ai/zen/v1/chat/completions"
MODEL = "space-bunny-free"

def chat(messages, max_tokens=2000, temperature=0, timeout=120, retries=4):
    body = {"model": MODEL, "messages": messages, "max_tokens": max_tokens,
            "temperature": temperature}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, method="POST")
    last = None
    for attempt in range(retries):
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                d = json.loads(r.read())
            ms = round((time.time() - t0) * 1000)
            ch = (d.get("choices") or [{}])[0].get("message", {})
            return {"ok": True, "content": ch.get("content") or "", "usage": d.get("usage") or {},
                    "ms": ms, "model": d.get("model"), "attempts": attempt + 1}
        except urllib.error.HTTPError as e:
            last = {"ok": False, "error": f"HTTP {e.code}",
                    "body": e.read(400).decode("utf-8", "replace"),
                    "ms": round((time.time() - t0) * 1000)}
        except Exception as e:
            last = {"ok": False, "error": type(e).__name__, "ms": round((time.time() - t0) * 1000)}
        time.sleep(2 * (attempt + 1))   # linear backoff: 2s, 4s, 6s, 8s
    return last

if __name__ == "__main__":
    r = chat([{"role": "user", "content": "Reply with exactly: READY"}], max_tokens=10)
    print(json.dumps(r, indent=2)[:600])
