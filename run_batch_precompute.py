import json
import urllib.request
import urllib.error
import time
import os
import sys

from generate_all_endpoints import ENDPOINTS_DATA

API_KEY = "fiq-c05ed74847755db048eef8038724c336"
BASE_URL = "https://rootsys.cloud/v1"

RESULTS_FILE = "precomputed_results.json"

def load_results():
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_results(results):
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

def call_endpoint(ep, max_retries=3):
    url = f"{BASE_URL}/chat/completions"
    model_to_use = ep["model"]
    
    for attempt in range(max_retries):
        payload = {
            "model": model_to_use,
            "messages": [
                {"role": "system", "content": ep["systemPrompt"]},
                {"role": "user", "content": ep["defaultSample"]}
            ],
            "max_tokens": 800,
            "temperature": 0.1
        }
        data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Authorization", f"Bearer {API_KEY}")
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

        start_time = time.time()
        try:
            with urllib.request.urlopen(req, timeout=50) as resp:
                elapsed_ms = int((time.time() - start_time) * 1000)
                res_data = json.loads(resp.read().decode("utf-8"))
                choice = res_data["choices"][0]["message"]
                content = choice.get("content") or choice.get("reasoning_content") or ""
                content = content.replace("```json", "").replace("```", "").strip()
                
                # Attempt to parse json
                try:
                    parsed = json.loads(content)
                except Exception:
                    parsed = {"output": content}
                
                tokens = res_data.get("usage", {}).get("total_tokens", 0)
                return {
                    "success": True,
                    "latency_ms": elapsed_ms,
                    "model_used": model_to_use,
                    "tokens": tokens,
                    "data": parsed
                }
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_time = 62
                print(f" [Rate limit 429: waiting {wait_time}s] ", end="", flush=True)
                time.sleep(wait_time)
                continue
            elif e.code == 403:
                body = e.read().decode("utf-8", errors="ignore")
                print(f" [403: {body[:60]}] ", end="", flush=True)
                # If quota issue, try lower tokens or switch to flash
                model_to_use = "deepseek-v4.1-flash"
                time.sleep(3)
                continue
            else:
                body = e.read().decode("utf-8", errors="ignore")
                print(f" [HTTP {e.code}: {body[:60]}] ", end="", flush=True)
                model_to_use = "deepseek-v4.1-flash"
                time.sleep(2)
        except Exception as e:
            print(f" [{e}] ", end="", flush=True)
            # Switch to flash if kimi hung
            if model_to_use == "kimi-k3":
                model_to_use = "deepseek-v4.1-flash"
            time.sleep(2)
    
    return {"success": False, "error": "Max retries exceeded"}

def main():
    results = load_results()
    print(f"Starting precomputation for {len(ENDPOINTS_DATA)} endpoints.")
    print(f"Currently successfully completed: {sum(1 for v in results.values() if v.get('success'))}")

    completed_count = 0
    for idx, ep in enumerate(ENDPOINTS_DATA, 1):
        key = ep["key"]
        if key in results and results[key].get("success") is True:
            # Already completed
            completed_count += 1
            print(f"[{idx}/{len(ENDPOINTS_DATA)}] Already cached: #{ep['id']} {key}")
            continue

        print(f"[{idx}/{len(ENDPOINTS_DATA)}] Precomputing #{ep['id']} {key} ({ep['model']})...", end="", flush=True)
        res = call_endpoint(ep)
        if res.get("success"):
            print(f" -> OK ({res['latency_ms']}ms, {res.get('tokens', 0)} tokens)")
            completed_count += 1
        else:
            print(f" -> FAILED: {res.get('error')}")

        results[key] = res
        save_results(results)

        # Respect 30 req/min limit: 2.2 second pause
        time.sleep(2.2)

    print(f"\nFinished! Total successful: {sum(1 for v in results.values() if v.get('success'))} / {len(ENDPOINTS_DATA)}")

if __name__ == "__main__":
    main()
