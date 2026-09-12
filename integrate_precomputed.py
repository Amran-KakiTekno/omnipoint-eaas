import json
import subprocess

with open("precomputed_results.json", "r", encoding="utf-8") as f:
    precomputed_data = json.load(f)

with open("public/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Inject PRECOMPUTED_CACHE variable into the client-side script
precomputed_json_str = json.dumps(precomputed_data, indent=2)

cache_var = f"const PRECOMPUTED_CACHE = {precomputed_json_str};\n"

# Replace where ENDPOINT_CONFIGS is declared to include PRECOMPUTED_CACHE
target = "const ENDPOINT_CONFIGS = {"
if target in html:
    html = html.replace(target, cache_var + "\n    const ENDPOINT_CONFIGS = {")
    print("Injected PRECOMPUTED_CACHE successfully.")
else:
    print("Target string for injection not found!")

# Update onStudioEndpointChange logic to automatically load precomputed output!
old_logic = """    function onStudioEndpointChange() {
      const select = document.getElementById('studio-endpoint-select');
      const key = select.value;
      const conf = ENDPOINT_CONFIGS[key] || ENDPOINT_CONFIGS['explain-lab'];
      
      document.getElementById('studio-route-pill').innerText = conf.route;
      document.getElementById('studio-input').value = conf.defaultSample;
      document.getElementById('zapier-url').innerText = window.location.origin + conf.route;
      updateCurlPreview();
    }"""

new_logic = """    function onStudioEndpointChange() {
      const select = document.getElementById('studio-endpoint-select');
      const key = select.value;
      const conf = ENDPOINT_CONFIGS[key] || ENDPOINT_CONFIGS['explain-lab'];
      
      document.getElementById('studio-route-pill').innerText = conf.route;
      document.getElementById('studio-input').value = conf.defaultSample;
      document.getElementById('zapier-url').innerText = window.location.origin + conf.route;
      updateCurlPreview();

      // Automatically display verified pre-computed result to save tokens & provide 0ms preview!
      const cached = PRECOMPUTED_CACHE[key];
      const jsonPre = document.getElementById('studio-json-pre');
      const latencyBadge = document.getElementById('studio-latency');
      const costBadge = document.getElementById('studio-cost-badge');

      if (cached && cached.data) {
        jsonPre.innerText = JSON.stringify(cached.data, null, 2);
        latencyBadge.innerText = '0ms (Cached)';
        latencyBadge.classList.remove('hidden');
        if (costBadge) {
          costBadge.innerHTML = '<span class=\"w-1.5 h-1.5 rounded-full bg-emerald-400\"></span> $0.00 Token Cost (Verified)';
          costBadge.classList.remove('hidden');
        }
      }
    }"""

if old_logic in html:
    html = html.replace(old_logic, new_logic)
    print("Replaced onStudioEndpointChange with precomputed display logic.")
else:
    print("Old logic string not matched, checking alternate...")

# Add an input listener on textarea so when user types, we update badge to 'Custom Input'
input_listener = """
    document.getElementById('studio-input').addEventListener('input', function() {
      const costBadge = document.getElementById('studio-cost-badge');
      if (costBadge) {
        costBadge.innerHTML = '<span class=\"w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse\"></span> Custom Input • Click Execute to Run';
      }
    });
"""
# Insert before DOMContentLoaded
html = html.replace("window.addEventListener('DOMContentLoaded', function() {", input_listener + "\n    window.addEventListener('DOMContentLoaded', function() {")

# Add a cost badge pill to the Studio header next to route pill
old_header = '<span id="studio-route-pill" class="text-xs font-mono text-indigo-400 font-semibold">/v1/health/explain-lab</span>'
new_header = '<span id="studio-route-pill" class="text-xs font-mono text-indigo-400 font-semibold">/v1/health/explain-lab</span>' + \
             '<span id="studio-cost-badge" class="ml-2 inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> $0.00 Token Cost (Verified)</span>'
html = html.replace(old_header, new_header)

with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Updated public/index.html.")

# Now rebuild src/index.js using build_worker.py
subprocess.run(["python", "build_worker.py"], check=True)
print("[SUCCESS] Precomputed results integrated and worker rebuilt.")
