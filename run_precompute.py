import urllib.request
import json
import time
import os

API_KEY = "fiq-c05ed74847755db048eef8038724c336"
BASE_URL = "https://rootsys.cloud/v1"
MODEL = "deepseek-v4.1-flash"

# Import prompts from generate_modern_ui
from generate_modern_ui import ENDPOINT_PROMPTS

def call_llm(system_prompt, user_input, model=MODEL):
    url = f"{BASE_URL}/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.1
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("Content-Type", "application/json")
    
    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            elapsed_ms = int((time.time() - start_time) * 1000)
            content = res_data["choices"][0]["message"]["content"]
            
            # Clean markdown backticks if any
            content = content.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(content)
            return {
                "success": True,
                "latency_ms": elapsed_ms,
                "model_used": model,
                "tokens": res_data.get("usage", {}).get("total_tokens", 0),
                "data": parsed
            }
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def run_all_precomputed():
    results = {}
    print(f"Running 1-time precomputation for {len(ENDPOINT_PROMPTS)} use cases...")
    for key, conf in ENDPOINT_PROMPTS.items():
        print(f"-> Running #{conf['name']} ({key})...")
        # Use kimi-k3 for invoice/receipt OCR or vision, deepseek-v4.1-flash for others
        model_to_use = "kimi-k3" if key == "invoice-extract" else MODEL
        res = call_llm(conf["systemPrompt"], conf["defaultSample"], model=model_to_use)
        if res.get("success"):
            print(f"   [OK] {res['latency_ms']}ms | {res['tokens']} tokens")
            results[key] = res
        else:
            print(f"   [FAILED] {res.get('error')}")
        time.sleep(0.5) # Gentle pacing
    
    with open("precomputed_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[DONE] Saved {len(results)} precomputed use cases to precomputed_results.json")

if __name__ == "__main__":
    run_all_precomputed()
