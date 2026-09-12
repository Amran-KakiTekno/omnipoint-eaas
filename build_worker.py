import json
import subprocess

with open("public/index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Read the prompts from public/index.html or definition
from generate_modern_ui import ENDPOINT_PROMPTS

prompts_js = "const ENDPOINT_PROMPTS = " + json.dumps(ENDPOINT_PROMPTS, indent=2) + ";"
escaped_html = json.dumps(html_content)

worker_code = f"""// Smart EaaS — Production Endpoint as a Service (Cloudflare Worker)
// Engineered with inspiration from recent.design and skills.sh

{prompts_js}

const APP_HTML = {escaped_html};

export default {{
  async fetch(request, env, ctx) {{
    const url = new URL(request.url);
    const path = url.pathname;

    const corsHeaders = {{
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With"
    }};

    if (request.method === "OPTIONS") {{
      return new Response(null, {{ headers: corsHeaders }});
    }}

    if (path === "/api/health") {{
      return new Response(JSON.stringify({{
        status: "operational",
        service: "Smart EaaS - Production AI Microservices",
        version: "2.0.0",
        cloud: "Cloudflare Workers (Edge)",
        models_supported: ["deepseek-v4.1-flash", "kimi-k3", "deepseek-v4-pro", "glm-5.3"]
      }}), {{
        headers: {{ ...corsHeaders, "Content-Type": "application/json" }}
      }});
    }}

    if (path === "/api/execute" && request.method === "POST") {{
      try {{
        const body = await request.json();
        const endpointKey = body.endpoint || "explain-lab";
        const customInput = body.input || "";
        const selectedModel = body.model || env.DEFAULT_TEXT_MODEL || "deepseek-v4.1-flash";
        const apiKey = body.api_key || env.ROOTSYS_API_KEY || "fiq-c05ed74847755db048eef8038724c336";

        const config = ENDPOINT_PROMPTS[endpointKey] || ENDPOINT_PROMPTS["explain-lab"];
        const startTime = Date.now();

        const llmPayload = {{
          model: selectedModel,
          messages: [
            {{ role: "system", content: config.systemPrompt }},
            {{ role: "user", content: customInput }}
          ],
          temperature: 0.1
        }};

        const response = await fetch(`${{env.ROOTSYS_BASE_URL || "https://rootsys.cloud/v1"}}/chat/completions`, {{
          method: "POST",
          headers: {{
            "Authorization": `Bearer ${{apiKey}}`,
            "Content-Type": "application/json"
          }},
          body: JSON.stringify(llmPayload)
        }});

        if (!response.ok) {{
          const errText = await response.text();
          return new Response(JSON.stringify({{
            success: false,
            error: `Upstream LLM error (${{response.status}}): ${{errText}}`
          }}), {{
            status: 502,
            headers: {{ ...corsHeaders, "Content-Type": "application/json" }}
          }});
        }}

        const data = await response.json();
        const latencyMs = Date.now() - startTime;
        let outputContent = data.choices[0]?.message?.content || "{{}}";

        outputContent = outputContent.replace(/^```json\\s*/i, "").replace(/^```\\s*/i, "").replace(/\\s*```$/i, "").trim();

        let parsedJson = null;
        try {{
          parsedJson = JSON.parse(outputContent);
        }} catch (e) {{
          parsedJson = {{ raw_output: outputContent, parsing_note: "Output received as raw string" }};
        }}

        return new Response(JSON.stringify({{
          success: true,
          endpoint: config.name,
          route: config.route,
          model_used: selectedModel,
          latency_ms: latencyMs,
          usage: data.usage || {{}},
          data: parsedJson
        }}), {{
          headers: {{ ...corsHeaders, "Content-Type": "application/json" }}
        }});
      }} catch (err) {{
        return new Response(JSON.stringify({{ success: false, error: err.message }}), {{
          status: 500,
          headers: {{ ...corsHeaders, "Content-Type": "application/json" }}
        }});
      }}
    }}

    // Direct REST API paths
    for (const [key, conf] of Object.entries(ENDPOINT_PROMPTS)) {{
      if (path === conf.route && request.method === "POST") {{
        try {{
          const body = await request.json();
          const rawInput = body.input || (typeof body === "string" ? body : JSON.stringify(body));
          const authHeader = request.headers.get("Authorization") || "";
          const token = authHeader.startsWith("Bearer ") ? authHeader.substring(7) : (env.ROOTSYS_API_KEY || "fiq-c05ed74847755db048eef8038724c336");

          const response = await fetch(`${{env.ROOTSYS_BASE_URL || "https://rootsys.cloud/v1"}}/chat/completions`, {{
            method: "POST",
            headers: {{
              "Authorization": `Bearer ${{token}}`,
              "Content-Type": "application/json"
            }},
            body: JSON.stringify({{
              model: env.DEFAULT_TEXT_MODEL || "deepseek-v4.1-flash",
              messages: [
                {{ role: "system", content: conf.systemPrompt }},
                {{ role: "user", content: typeof rawInput === "string" ? rawInput : JSON.stringify(rawInput) }}
              ],
              temperature: 0.1
            }})
          }});

          const data = await response.json();
          let rawRes = data.choices[0]?.message?.content || "{{}}";
          rawRes = rawRes.replace(/^```json\\s*/i, "").replace(/^```\\s*/i, "").replace(/\\s*```$/i, "").trim();

          return new Response(rawRes, {{
            headers: {{ ...corsHeaders, "Content-Type": "application/json" }}
          }});
        }} catch (e) {{
          return new Response(JSON.stringify({{ error: e.message }}), {{
            status: 500,
            headers: {{ ...corsHeaders, "Content-Type": "application/json" }}
          }});
        }}
      }}
    }}

    // Serve HTML
    return new Response(APP_HTML, {{
      headers: {{ ...corsHeaders, "Content-Type": "text/html; charset=utf-8" }}
    }});
  }}
}};
"""

with open("src/index.js", "w", encoding="utf-8") as f:
    f.write(worker_code)

print("src/index.js created. Validating with node...")
res = subprocess.run(["node", "--check", "src/index.js"], capture_output=True, text=True)
if res.returncode == 0:
    print("[SUCCESS] src/index.js passed syntax check!")
else:
    print("[ERROR] node syntax check failed:", res.stderr)
    raise SystemExit(1)
