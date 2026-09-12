import json
import re
import os
import subprocess

from generate_all_endpoints import ENDPOINTS_DATA

def build():
    print(f"Building platform with {len(ENDPOINTS_DATA)} endpoints...")

    # Load precomputed results
    if not os.path.exists("precomputed_results.json"):
        raise FileNotFoundError("precomputed_results.json not found!")

    with open("precomputed_results.json", "r", encoding="utf-8") as f:
        precomputed = json.load(f)
    
    successful_count = sum(1 for v in precomputed.values() if v.get("success"))
    print(f"Loaded {len(precomputed)} precomputed entries ({successful_count} successful).")

    with open("public/index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Build ALL_ENDPOINTS array for JS
    cat_slug_map = {
        "Individuals & Family": "individuals",
        "Non-Profits & NGOs": "non-profits",
        "Creators & Solos": "creators",
        "Local Small Businesses": "smbs",
        "Education & Public": "education",
        "Data & Documents": "vision"
    }

    tag_map = {
        "invoice-extract": ["Vision", "OCR", "Finance"],
        "explain-lab": ["Health", "Safe"],
        "lease-check": ["Legal", "Tenant"],
        "scam-detector": ["Security", "Family"],
        "auto-quote": ["Auto", "Consumer"],
        "fee-audit": ["Finance", "SaaS"],
        "ingredient-alert": ["Health", "Allergy"],
        "ticket-appeal": ["Legal", "Transit"],
        "insurance-appeal": ["Insurance", "Claims"],
        "iep-analyzer": ["Education", "IDEA"],
        "fridge-chef": ["Food", "Zero-Waste"],
        "appliance-fix": ["DIY", "Hardware"],
        "bill-optimizer": ["Energy", "Tariff"],
        "transition-map": ["Career", "Skills"],
        "parenting-coach": ["Parenting", "Psychology"],
        "warranty-claim": ["Consumer", "Dispute"],
        "grant-match": ["Grants", "NPO"],
        "donor-story": ["Donors", "Impact"],
        "ngo-990": ["Finance", "Audit"],
        "volunteer-dispatch": ["Volunteers", "Operations"],
        "localize-notice": ["Community", "Language"],
        "sos-triage": ["Emergency", "Crisis"],
        "donor-letter": ["Fundraising", "Stewardship"],
        "foodbank-recipes": ["Food", "Nutrition"],
        "policy-impact": ["Policy", "Civic"],
        "budget-narrative": ["Grants", "Accounting"],
        "creator-repurpose": ["Content", "Social"],
        "scope-defense": ["Freelance", "Contracts"],
        "audio-shownotes": ["Audio", "Podcast"],
        "creator-pitch": ["Sponsors", "Rates"],
        "portfolio-audit": ["Design", "UX"],
        "objection-buster": ["Marketing", "Conversion"],
        "thumbnail-concepts": ["YouTube", "CTR"],
        "lead-qualifier": ["Sales", "Inbound"],
        "filler-cleaner": ["Audio", "Editing"],
        "tone-subtitles": ["Video", "Subtitles"],
        "review-reply": ["Reputation", "SMB"],
        "menu-digitizer": ["Restaurant", "Menu"],
        "salon-fill": ["Booking", "SMS"],
        "trades-quote": ["Trades", "Estimates"],
        "local-seo": ["SEO", "Google Maps"],
        "vendor-slip": ["Retail", "Inventory"],
        "shift-swap": ["HR", "Scheduling"],
        "repair-status": ["Service", "SMS"],
        "lease-cam": ["Real Estate", "Audit"],
        "maintenance-log": ["Machinery", "Predictive"],
        "differentiate": ["Teaching", "Edu"],
        "rubric-feedback": ["Grading", "Feedback"],
        "case-notes": ["Social Work", "Compliance"],
        "council-digest": ["Civic", "Zoning"],
        "soap-note": ["Medical", "Clinical"],
        "homeschool-plan": ["Homeschool", "Curriculum"],
        "parent-comms": ["Comms", "Bilingual"],
        "benefits-finder": ["Benefits", "Safety-Net"],
        "crisis-aid": ["Mental Health", "Crisis"],
        "court-prep": ["Legal", "Pro-Se"]
    }

    js_endpoints = []
    for ep in ENDPOINTS_DATA:
        key = ep["key"]
        cat_slug = cat_slug_map.get(ep["category"], "individuals")
        tags = tag_map.get(key, ["AI", "API"])
        
        # Clean description from systemPrompt
        clean_desc = ep["systemPrompt"].split(".")[0] + "."
        if len(clean_desc) > 130:
            clean_desc = clean_desc[:127] + "..."

        item_str = (
            f"      {{ id: {ep['id']}, route: {json.dumps(ep['route'])}, "
            f"cat: {json.dumps(cat_slug)}, title: {json.dumps(ep['name'])}, "
            f"persona: {json.dumps(ep['persona'])}, desc: {json.dumps(clean_desc)}, "
            f"key: {json.dumps(key)}, tags: {json.dumps(tags)}, model: {json.dumps(ep['model'])} }}"
        )
        js_endpoints.append(item_str)

    all_endpoints_js = "const ALL_ENDPOINTS = [\n" + ",\n".join(js_endpoints) + "\n    ];"

    html = re.sub(r'const ALL_ENDPOINTS = \[.*?\];', lambda m: all_endpoints_js, html, flags=re.DOTALL)
    print(f"Updated ALL_ENDPOINTS with all {len(js_endpoints)} items.")

    # 2. Build Studio select options grouped by category
    category_groups = {
        "Data & Document Extraction (Universal)": [],
        "Individuals, Families & Consumers (1-15)": [],
        "Non-Profits, NGOs & Community (16-25)": [],
        "Freelancers & Solopreneurs (26-35)": [],
        "Local Small Businesses & Trades (36-45)": [],
        "Education, Healthcare & Civic (46-55)": []
    }

    for ep in ENDPOINTS_DATA:
        cat = ep["category"]
        if cat == "Data & Documents":
            category_groups["Data & Document Extraction (Universal)"].append(ep)
        elif cat == "Individuals & Family":
            category_groups["Individuals, Families & Consumers (1-15)"].append(ep)
        elif cat == "Non-Profits & NGOs":
            category_groups["Non-Profits, NGOs & Community (16-25)"].append(ep)
        elif cat == "Creators & Solos":
            category_groups["Freelancers & Solopreneurs (26-35)"].append(ep)
        elif cat == "Local Small Businesses":
            category_groups["Local Small Businesses & Trades (36-45)"].append(ep)
        elif cat == "Education & Public":
            category_groups["Education, Healthcare & Civic (46-55)"].append(ep)

    select_inner_html = ""
    for group_name, eps in category_groups.items():
        select_inner_html += f'              <optgroup label="{group_name}">\n'
        for ep in eps:
            select_inner_html += f'                <option value="{ep["key"]}">#{ep["id"]} {ep["name"]} ({ep["route"]})</option>\n'
        select_inner_html += '              </optgroup>\n'

    new_select = f"""<select id="studio-endpoint-select" onchange="onStudioEndpointChange()" aria-label="Select target microservice" class="w-full bg-[#16161a] border border-white/[0.08] text-white rounded-lg p-2.5 text-xs focus:ring-1 focus:ring-indigo-500 focus:outline-none">
{select_inner_html.rstrip()}
            </select>"""

    html = re.sub(r'<select id="studio-endpoint-select"[^>]*>.*?</select>', lambda m: new_select, html, flags=re.DOTALL)
    print("Updated studio-endpoint-select with all 56 options inside <optgroup>.")

    # 3. Build ENDPOINT_OPTIMAL_MODELS dictionary
    optimal_models_dict = {}
    for ep in ENDPOINTS_DATA:
        optimal_models_dict[ep["key"]] = {
            "model": ep["model"],
            "rationale": ep["rationale"]
        }
    optimal_models_js = f"const ENDPOINT_OPTIMAL_MODELS = {json.dumps(optimal_models_dict, indent=2)};"

    if "const ENDPOINT_OPTIMAL_MODELS = " in html:
        html = re.sub(r'const ENDPOINT_OPTIMAL_MODELS = \{.*?\};', lambda m: optimal_models_js, html, flags=re.DOTALL)
    else:
        html = html.replace("const ENDPOINT_CONFIGS = {", optimal_models_js + "\n    const ENDPOINT_CONFIGS = {")
    print("Updated ENDPOINT_OPTIMAL_MODELS for all 56 endpoints.")

    # 4. Build ENDPOINT_CONFIGS dictionary
    configs_dict = {}
    for ep in ENDPOINTS_DATA:
        configs_dict[ep["key"]] = {
            "id": ep["id"],
            "name": ep["name"],
            "route": ep["route"],
            "category": ep["category"],
            "persona": ep["persona"],
            "model": ep["model"],
            "rationale": ep["rationale"],
            "systemPrompt": ep["systemPrompt"],
            "defaultSample": ep["defaultSample"]
        }
    configs_js = f"const ENDPOINT_CONFIGS = {json.dumps(configs_dict, indent=2)};"
    html = re.sub(r'const ENDPOINT_CONFIGS = \{.*?\};', lambda m: configs_js, html, flags=re.DOTALL)
    print("Updated ENDPOINT_CONFIGS with all 56 configurations.")

    # 5. Build PRECOMPUTED_CACHE dictionary
    precomputed_cache_js = f"const PRECOMPUTED_CACHE = {json.dumps(precomputed, indent=2)};"
    if "const PRECOMPUTED_CACHE = " in html:
        html = re.sub(r'const PRECOMPUTED_CACHE = \{.*?\};', lambda m: precomputed_cache_js, html, flags=re.DOTALL)
    else:
        html = html.replace("const ENDPOINT_CONFIGS = {", precomputed_cache_js + "\n    const ENDPOINT_CONFIGS = {")
    print(f"Updated PRECOMPUTED_CACHE with all {len(precomputed)} precomputed outputs.")

    # 6. Update counts and labels in HTML
    html = html.replace('All Endpoints <span class="ml-1 text-[10px] opacity-70 font-mono">55</span>', 'All Endpoints <span class="ml-1 text-[10px] opacity-70 font-mono">56</span>')
    html = html.replace('<span>55+ Deterministic Microservices</span>', '<span>56 Deterministic Microservices</span>')
    html = html.replace('font-bold font-mono text-white tracking-tight">55+</div>', 'font-bold font-mono text-white tracking-tight">56</div>')

    # Update filterCards for vision tag
    old_vision_filter = "filtered = filtered.filter(function(ep) { return ep.tags.includes('Vision'); });"
    new_vision_filter = "filtered = filtered.filter(function(ep) { return ep.tags.includes('Vision') || ep.cat === 'vision'; });"
    html = html.replace(old_vision_filter, new_vision_filter)

    # Save public/index.html
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved public/index.html successfully.")

    # 7. Update Worker src/index.js and validate
    subprocess.run(["python", "build_worker.py"], check=True)
    print("[SUCCESS] All files rebuilt and validated successfully!")

if __name__ == "__main__":
    build()
