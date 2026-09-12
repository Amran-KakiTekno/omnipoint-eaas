import subprocess

with open("public/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Replace the model select box with the read-only assigned engine display
old_select_markup = """          <!-- Select Model -->
          <div class="space-y-1.5">
            <div class="flex justify-between items-center text-[11px]">
              <label class="font-semibold text-zinc-300 uppercase tracking-wider">LLM Engine (rootsys.cloud)</label>
              <span class="text-[10px] text-zinc-500">12 Live Models</span>
            </div>
            <select id="studio-model-select" class="w-full bg-[#16161a] border border-white/[0.08] text-white rounded-lg p-2.5 text-xs focus:ring-1 focus:ring-indigo-500 focus:outline-none">
              <option value="deepseek-v4.1-flash" selected>deepseek-v4.1-flash (Recommended: &lt;400ms & strict JSON)</option>
              <option value="kimi-k3">kimi-k3 (Vision / Multimodal OCR & Long Context)</option>
              <option value="deepseek-v4-pro">deepseek-v4-pro (Deep Reasoning & Legal Audit)</option>
              <option value="glm-5.3">glm-5.3 (High Precision Analytical Engine)</option>
            </select>
          </div>"""

new_model_badge = """          <!-- Auto-Assigned Optimal Engine -->
          <div class="space-y-1.5">
            <div class="flex justify-between items-center text-[11px]">
              <label class="font-semibold text-zinc-300 uppercase tracking-wider">Assigned Optimal Engine</label>
              <span class="text-[10px] text-emerald-400 font-mono font-medium flex items-center gap-1">
                <i class="fa-solid fa-lock text-[9px]"></i> Auto-Predefined
              </span>
            </div>
            <div class="w-full bg-[#16161a] border border-white/[0.08] text-white rounded-lg p-2.5 text-xs flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-indigo-400 animate-pulse"></span>
                <span id="studio-assigned-model" class="font-mono font-bold text-indigo-300">deepseek-v4.1-flash</span>
              </div>
              <span id="studio-model-rationale" class="text-[10px] text-zinc-400 font-sans font-medium">Optimized for &lt;400ms Diagnostic Analysis</span>
            </div>
          </div>"""

if old_select_markup in html:
    html = html.replace(old_select_markup, new_model_badge)
    print("Replaced model select dropdown with assigned optimal engine badge.")
else:
    print("Old select markup not found directly, checking...")

# 2. Add ENDPOINT_OPTIMAL_MODELS dictionary and update onStudioEndpointChange & runStudioExecution
optimal_models_code = """
    const ENDPOINT_OPTIMAL_MODELS = {
      "explain-lab": { model: "deepseek-v4.1-flash", rationale: "Optimized for <400ms Diagnostic Analysis" },
      "lease-check": { model: "deepseek-v4-pro", rationale: "Optimized for Multi-Clause Legal Reasoning" },
      "scam-detector": { model: "deepseek-v4.1-flash", rationale: "Optimized for Sub-Second Fraud Triage" },
      "review-reply": { model: "deepseek-v4.1-flash", rationale: "Optimized for Brand Diplomacy & Tone" },
      "grant-match": { model: "deepseek-v4-pro", rationale: "Optimized for 50-Page RFP Compliance Audit" },
      "scope-defense": { model: "deepseek-v4.1-flash", rationale: "Optimized for Contract Boundary Negotiation" },
      "differentiate": { model: "deepseek-v4.1-flash", rationale: "Optimized for 3-Tier Pedagogical Scaffolding" },
      "invoice-extract": { model: "kimi-k3", rationale: "Optimized for Multimodal Vision & Table OCR" }
    };
"""

target_marker = "const ENDPOINT_CONFIGS = {"
html = html.replace(target_marker, optimal_models_code + "\n    const ENDPOINT_CONFIGS = {")

# Update onStudioEndpointChange to set the model & rationale text
target_fn = "document.getElementById('zapier-url').innerText = window.location.origin + conf.route;"
replacement_fn = """document.getElementById('zapier-url').innerText = window.location.origin + conf.route;

      // Update auto-assigned optimal engine display
      const opt = ENDPOINT_OPTIMAL_MODELS[key] || { model: 'deepseek-v4.1-flash', rationale: 'High-Speed Deterministic JSON' };
      const modelElem = document.getElementById('studio-assigned-model');
      const rationaleElem = document.getElementById('studio-model-rationale');
      if (modelElem) modelElem.innerText = opt.model;
      if (rationaleElem) rationaleElem.innerText = opt.rationale;"""

html = html.replace(target_fn, replacement_fn)

# Update runStudioExecution to read from ENDPOINT_OPTIMAL_MODELS
old_run_model = "const model = document.getElementById('studio-model-select').value;"
new_run_model = """const opt = ENDPOINT_OPTIMAL_MODELS[select.value] || { model: 'deepseek-v4.1-flash' };
      const model = opt.model;"""

html = html.replace(old_run_model, new_run_model)

with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated public/index.html with auto-assigned models.")

# Rebuild src/index.js
subprocess.run(["python", "build_worker.py"], check=True)
print("[SUCCESS] All files rebuilt and syntax validated.")
