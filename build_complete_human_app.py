import json
import os
import subprocess
from generate_all_endpoints import ENDPOINTS_DATA
from build_human_platform import FRIENDLY_METADATA

def build_human_app():
    print("Building Human-Centric Smart EaaS Platform...")

    if not os.path.exists("precomputed_results.json"):
        raise FileNotFoundError("precomputed_results.json not found!")

    with open("precomputed_results.json", "r", encoding="utf-8") as f:
        precomputed = json.load(f)

    print(f"Loaded {len(precomputed)} precomputed outputs.")

    endpoints = []
    for ep in ENDPOINTS_DATA:
        key = ep["key"]
        meta = FRIENDLY_METADATA.get(key, {
            "title": ep["name"],
            "human_desc": ep["systemPrompt"].split(".")[0] + ".",
            "icon": "fa-sparkles",
            "color": "indigo",
            "tag": "General",
            "badge": "Instant Solution",
            "action": "Solve This Problem",
            "human_cat": "business"
        })
        
        merged = {
            "id": ep["id"],
            "key": key,
            "route": ep["route"],
            "category": ep["category"],
            "persona": ep["persona"],
            "model": ep["model"],
            "rationale": ep["rationale"],
            "systemPrompt": ep["systemPrompt"],
            "defaultSample": ep["defaultSample"],
            "title": meta["title"],
            "human_desc": meta["human_desc"],
            "icon": meta["icon"],
            "color": meta["color"],
            "tag": meta["tag"],
            "badge": meta["badge"],
            "action": meta["action"],
            "human_cat": meta["human_cat"]
        }
        endpoints.append(merged)

    print(f"Merged {len(endpoints)} endpoints with human-friendly metadata.")

    # Load template.html
    with open("template.html", "r", encoding="utf-8") as f:
        template_html = f.read()

    # Substitute JSON payloads
    final_html = template_html.replace(
        "__ALL_ENDPOINTS_JSON__",
        json.dumps(endpoints, indent=2)
    ).replace(
        "__PRECOMPUTED_CACHE_JSON__",
        json.dumps(precomputed, indent=2)
    )

    # Save to public/index.html
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"public/index.html written successfully ({len(final_html)} bytes).")

    # Rebuild worker bundle with build_worker.py
    subprocess.run(["python", "build_worker.py"], check=True)
    print("[SUCCESS] Complete Human-First Platform rebuilt and validated!")

if __name__ == "__main__":
    build_human_app()
