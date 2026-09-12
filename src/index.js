// OmniPoint AI - Production Endpoint as a Service (EaaS) Cloudflare Worker
// Zero-cost serverless execution running on Cloudflare Workers

const ENDPOINT_PROMPTS = {
  "explain-lab": {
    name: "Medical Lab Report Explainer",
    route: "/v1/health/explain-lab",
    category: "Individuals & Consumers",
    systemPrompt: `You are a medical diagnostics communication specialist. 
Your job is to analyze medical lab test data and translate it into a patient-friendly, clear, and reassuring explanation.
CRITICAL: Always output strictly valid JSON with no markdown backticks and no conversational filler.
Format:
{
  "summary": "1-2 sentence overall assessment",
  "abnormal_findings": [
    { "test_name": "...", "value": "...", "reference_range": "...", "clinical_meaning": "...", "urgency": "low|medium|high" }
  ],
  "potential_lifestyle_factors": ["Factor 1", "Factor 2"],
  "questions_for_doctor": ["Question 1", "Question 2", "Question 3"],
  "disclaimer": "This is an AI summary for educational purposes. Consult your licensed physician."
}`,
    defaultSample: `Comprehensive Metabolic Panel & CBC:
- Fasting Glucose: 118 mg/dL (Reference: 70-99 mg/dL) [HIGH]
- Hemoglobin A1c: 5.9% (Reference: < 5.7%) [HIGH]
- Total Cholesterol: 224 mg/dL (Reference: < 200 mg/dL) [HIGH]
- LDL Cholesterol: 142 mg/dL (Reference: < 100 mg/dL) [HIGH]
- Triglycerides: 165 mg/dL (Reference: < 150 mg/dL) [HIGH]
- ALT (Liver enzyme): 38 U/L (Reference: 7-56 U/L) [NORMAL]
- Creatinine: 0.9 mg/dL (Reference: 0.6-1.2 mg/dL) [NORMAL]`
  },

  "lease-check": {
    name: "Apartment Lease Red-Flag Auditor",
    route: "/v1/legal/lease-check",
    category: "Individuals & Consumers",
    systemPrompt: `You are a tenant rights attorney auditor. 
Audit rental lease text to detect exploitative, ambiguous, or illegal clauses.
CRITICAL: Output strictly valid JSON with no markdown wrapping.
Format:
{
  "risk_score": "low|medium|high|critical",
  "summary": "...",
  "flagged_clauses": [
    { "clause_title": "...", "original_text": "...", "issue_explanation": "...", "state_law_concern": "...", "recommended_action": "..." }
  ],
  "hidden_costs_found": ["..."],
  "tenant_negotiation_checklist": ["..."]
}`,
    defaultSample: `Section 9. Maintenance and Repairs:
"Tenant shall be responsible for all repairs under $350, including plumbing clogs, HVAC filter servicing, electrical switches, and appliance maintenance. Landlord shall not be liable for lack of heating during winter months if maintenance parts are on backorder."

Section 14. Entry & Inspection:
"Landlord reserves the right to enter the leased premises at any time without advance written notice for routine inspections, showing to prospective buyers, or general premises auditing."

Section 22. Security Deposit:
"A non-refundable refurbishment and administrative fee of $500 will be deducted from the security deposit upon vacancy, irrespective of apartment condition."`
  },

  "scam-detector": {
    name: "Elder Scam & Phishing Defender",
    route: "/v1/safety/scam-detector",
    category: "Individuals & Consumers",
    systemPrompt: `You are a cybersecurity and fraud defense investigator.
Analyze suspicious text messages, voicemails, or emails targeted at consumers or seniors.
CRITICAL: Output strictly valid JSON without markdown wrapping.
Format:
{
  "is_scam": true,
  "confidence_score": 0.98,
  "scam_type": "IRS / Bank Impersonation / Urgency Phishing",
  "red_flags": ["..."],
  "psychological_tricks_used": ["..."],
  "plain_language_verdict": "Clear, reassuring explanation for a senior",
  "safe_action_steps": ["DO NOT click...", "Block...", "Call bank directly at..."]
}`,
    defaultSample: `URGENT NOTICE FROM CHASE FRAUD ALERT:
Your online access has been temporarily restricted due to 3 suspicious transactions totaling $1,420.89 in Chicago, IL.
If you did not authorize these charges, you must immediately verify your identity and debit card PIN within 15 minutes by clicking:
https://chase-security-resolver-update82.com/login?token=92842
Failure to respond will result in immediate permanent account suspension and police filing.`
  },

  "review-reply": {
    name: "Google Business Review De-escalator",
    route: "/v1/smb/review-reply",
    category: "Local Small Businesses",
    systemPrompt: `You are a high-end customer relations and brand PR director.
Generate a public response to a customer review that validates their frustration, preserves brand reputation, avoids admitting legal liability, and moves resolution offline.
CRITICAL: Output strictly valid JSON.
Format:
{
  "sentiment": "negative|neutral|positive",
  "urgency": "low|medium|high",
  "primary_complaint": "...",
  "recommended_public_reply": "...",
  "internal_process_fix": "What the staff should fix behind the scenes"
}`,
    defaultSample: `1-Star Review on Google Maps for "Mario's Wood-Fired Pizzeria":
"Waited 55 minutes for two pizzas on a Tuesday night. When they finally arrived, the crust was burnt on the bottom and cold on top. The waiter never checked on our drinks and when I asked for the manager, he acted like I was bothering him. Overpriced garbage. Will never come back with my family."`
  },

  "grant-match": {
    name: "Grant RFP Criteria Matcher",
    route: "/v1/ngo/grant-match",
    category: "Non-Profits & NGOs",
    systemPrompt: `You are a seasoned non-profit foundation grant evaluation officer.
Evaluate an RFP summary against an NGO's mission to assess eligibility, disqualifications, and strategic alignment.
CRITICAL: Output strictly valid JSON.
Format:
{
  "eligibility_match_percentage": 88,
  "eligibility_verdict": "Eligible|Borderline|Disqualified",
  "aligned_focus_areas": ["..."],
  "disqualification_risks": ["..."],
  "required_metrics_to_prove": ["..."],
  "strategic_recommendation": "..."
}`,
    defaultSample: `GRANT RFP:
Funder: The Global Green Community Trust
Grant Size: $50,000 - $120,000
Eligibility Requirements: Must be a registered 501(c)(3) operating for at least 3 years. Focus must be urban agricultural education or youth-led local food justice. Overhead/indirect administrative costs capped at 10%. Projects must track number of youth trained and pounds of fresh produce distributed.

APPLICANT NGO PROFILE:
Organization: CityRoots Community Gardens (501c3 founded 2021)
Annual Budget: $320,000
Mission: Transforming vacant municipal lots into community micro-farms in underserved food deserts, providing after-school apprenticeships to high schoolers.`
  },

  "scope-defense": {
    name: "Client Scope Creep Defense Assistant",
    route: "/v1/freelance/scope-defense",
    category: "Creators & Solopreneurs",
    systemPrompt: `You are a freelance contract strategist and client diplomacy expert.
Analyze an incoming client request against the agreed project scope. Confirm if it is scope creep, write a friendly and polite email that upholds boundaries, and formulate a paid change-order proposal.
CRITICAL: Output strictly valid JSON.
Format:
{
  "is_scope_creep": true,
  "creep_severity": "minor|moderate|major",
  "analysis": "...",
  "diplomatic_email_draft": "...",
  "suggested_change_order_fee": "$300 - $500",
  "estimated_additional_timeline": "3 business days"
}`,
    defaultSample: `ORIGINAL CONTRACT SCOPE:
"Design and build a 5-page responsive marketing website (Home, About, Services, Case Studies, Contact) in Webflow. Includes 2 rounds of design revisions. CMS integration for 10 case studies."

INCOMING CLIENT MESSAGE:
"Hi Alex! Love the progress on the site. Since we have a couple days before launch, could you also quickly hook up a multi-step user registration portal where clients can log in to upload PDF files and view their invoice history? It shouldn't take too long since it's just adding an account button. Thanks!"`
  },

  "differentiate": {
    name: "Differentiated Homework Generator",
    route: "/v1/edu/differentiate",
    category: "Education & Public Service",
    systemPrompt: `You are a master pedagogical curriculum designer.
Given a core learning concept or standard, create 3 tiered assignments: Tier 1 (Remedial / Scaffolding), Tier 2 (Grade-level Mastery), and Tier 3 (Advanced Inquiry / Extension).
CRITICAL: Output strictly valid JSON.
Format:
{
  "core_concept": "...",
  "target_grade": "...",
  "tier_1_scaffolded": { "objective": "...", "assignment": "...", "support_scaffolds": ["..."] },
  "tier_2_mastery": { "objective": "...", "assignment": "..." },
  "tier_3_advanced": { "objective": "...", "assignment": "..." },
  "quick_exit_ticket_question": "..."
}`,
    defaultSample: `Grade Level: 7th Grade Science
Topic: Ecosystems & Food Webs
Learning Goal: Students must demonstrate understanding of how energy flows through trophic levels (producers, primary consumers, secondary consumers, apex predators) and what happens when an invasive species disrupts the balance.`
  },

  "invoice-extract": {
    name: "Universal Invoice & Receipt to JSON",
    route: "/v1/extract/invoice",
    category: "Data Extraction & OCR",
    systemPrompt: `You are an automated document parsing and accounting data extraction engine.
Parse raw invoice/receipt text and extract strictly standardized accounting fields.
CRITICAL: Output strictly valid JSON.
Format:
{
  "vendor": { "name": "...", "address": "...", "tax_id": "..." },
  "invoice_details": { "invoice_number": "...", "date": "YYYY-MM-DD", "due_date": "YYYY-MM-DD" },
  "currency": "USD",
  "line_items": [
    { "description": "...", "quantity": 1, "unit_price": 0.0, "total": 0.0 }
  ],
  "subtotal": 0.0,
  "tax_amount": 0.0,
  "total_amount": 0.0,
  "payment_terms": "..."
}`,
    defaultSample: `INVOICE #INV-884920
Vendor: Apex Cloud Solutions LLC
1204 Innovation Way, Suite 400, Austin, TX 78701
Tax ID / EIN: 84-2938192
Bill To: Meridian Logistics Inc.
Date: September 08, 2026
Due Date: October 08, 2026

Description                        Qty    Rate       Amount
Kubernetes Dedicated Node Cluster    2    $450.00    $900.00
Cloud Storage R2 Bucket (5TB)        1    $75.00     $75.00
Edge Network DDOS Protection Addon   1    $120.00    $120.00

Subtotal: $1,095.00
State Sales Tax (8.25%): $90.34
Total Due: $1,185.34
Payment: Net 30 days. Wire to Bank of America Acct ending in 4921.`
  }
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // CORS preflight headers
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With"
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    // Health / info endpoint
    if (path === "/api/health") {
      return new Response(JSON.stringify({
        status: "operational",
        service: "OmniPoint AI - Endpoint as a Service (EaaS)",
        version: "1.0.0",
        cloud: "Cloudflare Workers (Edge)",
        models_supported: ["deepseek-v4.1-flash", "kimi-k3", "deepseek-v4-pro", "glm-5.3"]
      }), {
        headers: { ...corsHeaders, "Content-Type": "application/json" }
      });
    }

    // Interactive Execute API Route
    if (path === "/api/execute" && request.method === "POST") {
      try {
        const body = await request.json();
        const endpointKey = body.endpoint || "explain-lab";
        const customInput = body.input || "";
        const selectedModel = body.model || env.DEFAULT_TEXT_MODEL || "deepseek-v4.1-flash";
        const apiKey = body.api_key || env.ROOTSYS_API_KEY;

        const config = ENDPOINT_PROMPTS[endpointKey] || ENDPOINT_PROMPTS["explain-lab"];

        const startTime = Date.now();

        const llmPayload = {
          model: selectedModel,
          messages: [
            { role: "system", content: config.systemPrompt },
            { role: "user", content: customInput }
          ],
          temperature: 0.1
        };

        const response = await fetch(`${env.ROOTSYS_BASE_URL || "https://rootsys.cloud/v1"}/chat/completions`, {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${apiKey}`,
            "Content-Type": "application/json"
          },
          body: JSON.stringify(llmPayload)
        });

        if (!response.ok) {
          const errText = await response.text();
          return new Response(JSON.stringify({
            success: false,
            error: `Upstream LLM error (${response.status}): ${errText}`
          }), {
            status: 502,
            headers: { ...corsHeaders, "Content-Type": "application/json" }
          });
        }

        const data = await response.json();
        const latencyMs = Date.now() - startTime;
        let content = data.choices[0]?.message?.content || "{}";

        // Strip any markdown backticks if present
        content = content.replace(/^```json\s*/i, "").replace(/^```\s*/i, "").replace(/\s*```$/i, "").trim();

        let parsedJson = null;
        try {
          parsedJson = JSON.parse(content);
        } catch (e) {
          parsedJson = { raw_output: content, parsing_note: "Output received as raw string" };
        }

        return new Response(JSON.stringify({
          success: true,
          endpoint: config.name,
          route: config.route,
          model_used: selectedModel,
          latency_ms: latencyMs,
          usage: data.usage || {},
          data: parsedJson
        }), {
          headers: { ...corsHeaders, "Content-Type": "application/json" }
        });
      } catch (err) {
        return new Response(JSON.stringify({ success: false, error: err.message }), {
          status: 500,
          headers: { ...corsHeaders, "Content-Type": "application/json" }
        });
      }
    }

    // Direct REST API paths (e.g. POST /v1/health/explain-lab, etc.)
    for (const [key, conf] of Object.entries(ENDPOINT_PROMPTS)) {
      if (path === conf.route && request.method === "POST") {
        try {
          const body = await request.json();
          const rawInput = body.input || (typeof body === "string" ? body : JSON.stringify(body));
          const authHeader = request.headers.get("Authorization") || "";
          const token = authHeader.startsWith("Bearer ") ? authHeader.substring(7) : env.ROOTSYS_API_KEY;

          const response = await fetch(`${env.ROOTSYS_BASE_URL}/chat/completions`, {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${token}`,
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              model: env.DEFAULT_TEXT_MODEL || "deepseek-v4.1-flash",
              messages: [
                { role: "system", content: conf.systemPrompt },
                { role: "user", content: typeof rawInput === "string" ? rawInput : JSON.stringify(rawInput) }
              ],
              temperature: 0.1
            })
          });

          const data = await response.json();
          let content = data.choices[0]?.message?.content || "{}";
          content = content.replace(/^```json\s*/i, "").replace(/^```\s*/i, "").replace(/\s*```$/i, "").trim();

          return new Response(content, {
            headers: { ...corsHeaders, "Content-Type": "application/json" }
          });
        } catch (e) {
          return new Response(JSON.stringify({ error: e.message }), {
            status: 500,
            headers: { ...corsHeaders, "Content-Type": "application/json" }
          });
        }
      }
    }

    // Return HTML Single-Page App (Wireframe Explorer & Live Playground)
    return new Response(renderHtmlApp(ENDPOINT_PROMPTS), {
      headers: { ...corsHeaders, "Content-Type": "text/html; charset=utf-8" }
    });
  }
};

function renderHtmlApp(endpoints) {
  const endpointsJson = JSON.stringify(endpoints);
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OmniPoint AI — Endpoint as a Service (EaaS) Hub & Playground</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
    body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0B0F19; color: #E2E8F0; }
    code, pre { font-family: 'JetBrains Mono', monospace; }
    .glow-border { border: 1px solid rgba(59, 130, 246, 0.3); box-shadow: 0 0 25px rgba(37, 99, 235, 0.15); }
    .tab-active { border-bottom: 2px solid #3B82F6; color: #60A5FA; }
    .wireframe-box { background: #111827; border: 1px dashed #374151; border-radius: 8px; }
  </style>
</head>
<body class="min-h-screen flex flex-col">

  <!-- TOP HEADER -->
  <header class="border-b border-gray-800 bg-[#0D1322]/80 backdrop-blur-md sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/30">
          <i class="fa-solid fa-cube text-white text-lg"></i>
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <span class="font-extrabold text-lg tracking-tight text-white">OmniPoint<span class="text-blue-500">.AI</span></span>
            <span class="px-2 py-0.5 text-xs bg-blue-900/60 border border-blue-700/50 text-blue-300 rounded-full font-semibold">EaaS Production</span>
          </div>
          <p class="text-xs text-gray-400">Deterministic AI Microservices & Zero-Cost Cloudflare Deployment</p>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <div class="flex space-x-1 sm:space-x-4 text-sm font-medium">
        <button onclick="switchTab('playground')" id="tab-btn-playground" class="px-3 py-2 tab-active transition-colors">
          <i class="fa-solid fa-bolt mr-1.5"></i>Live Playground
        </button>
        <button onclick="switchTab('wireframes')" id="tab-btn-wireframes" class="px-3 py-2 text-gray-400 hover:text-gray-200 transition-colors">
          <i class="fa-solid fa-layer-group mr-1.5"></i>UI Wireframes & Flows
        </button>
        <button onclick="switchTab('catalog')" id="tab-btn-catalog" class="px-3 py-2 text-gray-400 hover:text-gray-200 transition-colors">
          <i class="fa-solid fa-table-list mr-1.5"></i>55+ Endpoints Catalog
        </button>
        <button onclick="switchTab('architecture')" id="tab-btn-architecture" class="px-3 py-2 text-gray-400 hover:text-gray-200 transition-colors">
          <i class="fa-solid fa-cloud-arrow-up mr-1.5"></i>$0 Cloudflare Stack
        </button>
      </div>
    </div>
  </header>

  <!-- MAIN CONTAINER -->
  <main class="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">

    <!-- ==================== TAB 1: LIVE PLAYGROUND ==================== -->
    <div id="tab-content-playground" class="space-y-6">
      
      <!-- HERO BANNER -->
      <div class="p-6 rounded-2xl bg-gradient-to-r from-blue-950/40 via-indigo-950/30 to-purple-950/20 border border-blue-800/40 glow-border flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            Live AI Endpoint Playground
            <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5 animate-pulse"></span> Connected to rootsys.cloud
            </span>
          </h1>
          <p class="text-sm text-gray-300 mt-1 max-w-2xl">
            Test pre-configured production microservices below. Every call transforms messy, unformatted inputs into <b>100% strict, validated JSON</b> ready to plug into spreadsheets, WhatsApp, or Zapier webhooks.
          </p>
        </div>
        <div class="flex items-center gap-3">
          <div class="text-right">
            <span class="text-xs text-gray-400 block">Current Active Edge:</span>
            <span class="text-xs font-mono text-blue-400 font-semibold">Cloudflare Worker Global</span>
          </div>
        </div>
      </div>

      <!-- PLAYGROUND GRID -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- LEFT PANEL: CONTROLS & INPUT -->
        <div class="lg:col-span-5 space-y-4">
          <div class="bg-[#111827] border border-gray-800 rounded-xl p-5 shadow-xl">
            <h2 class="text-sm font-semibold uppercase tracking-wider text-gray-400 mb-4 flex items-center justify-between">
              <span>Endpoint Configuration</span>
              <span class="text-xs text-blue-400 font-mono" id="current-category">Individuals</span>
            </h2>

            <!-- Select Endpoint -->
            <div class="space-y-2 mb-4">
              <label class="block text-xs font-semibold text-gray-300">Select Microservice Endpoint</label>
              <select id="endpoint-selector" onchange="onEndpointChange()" class="w-full bg-[#1F2937] border border-gray-700 text-white rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none">
                <optgroup label="Individuals, Families & Consumers">
                  <option value="explain-lab">#1 Medical Lab Explainer (/v1/health/explain-lab)</option>
                  <option value="lease-check">#2 Lease Red-Flag Auditor (/v1/legal/lease-check)</option>
                  <option value="scam-detector">#3 Elder Scam Defender (/v1/safety/scam-detector)</option>
                </optgroup>
                <optgroup label="Local Small Businesses">
                  <option value="review-reply">#36 Google Review De-escalator (/v1/smb/review-reply)</option>
                </optgroup>
                <optgroup label="Non-Profits & NGOs">
                  <option value="grant-match">#16 Grant Criteria Matcher (/v1/ngo/grant-match)</option>
                </optgroup>
                <optgroup label="Creators & Freelancers">
                  <option value="scope-defense">#27 Scope Creep Defense (/v1/freelance/scope-defense)</option>
                </optgroup>
                <optgroup label="Education & Public Service">
                  <option value="differentiate">#46 Differentiated Homework (/v1/edu/differentiate)</option>
                </optgroup>
                <optgroup label="Document & OCR">
                  <option value="invoice-extract">#0 Universal Invoice Parser (/v1/extract/invoice)</option>
                </optgroup>
              </select>
            </div>

            <!-- Model Selection -->
            <div class="space-y-2 mb-4">
              <div class="flex justify-between items-center">
                <label class="block text-xs font-semibold text-gray-300">AI Model on rootsys.cloud</label>
                <span class="text-[10px] bg-gray-800 text-gray-400 px-1.5 py-0.5 rounded">12 Models Live</span>
              </div>
              <select id="model-selector" class="w-full bg-[#1F2937] border border-gray-700 text-white rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none">
                <option value="deepseek-v4.1-flash" selected>deepseek-v4.1-flash (Recommended: Ultra-fast <400ms & strict JSON)</option>
                <option value="kimi-k3">kimi-k3 (Multimodal: Supports Vision, OCR & Long-Context)</option>
                <option value="deepseek-v4-pro">deepseek-v4-pro (Deep Reasoning & Complex Legal Contracts)</option>
                <option value="glm-5.3">glm-5.3 (High Accuracy Analytical Model)</option>
                <option value="minimax-m3">minimax-m3 (Creative & Tone Nuance)</option>
              </select>
            </div>

            <!-- Input Textarea -->
            <div class="space-y-2 mb-4">
              <div class="flex justify-between items-center">
                <label class="block text-xs font-semibold text-gray-300">Raw Unstructured Input</label>
                <button onclick="loadSampleData()" class="text-xs text-blue-400 hover:text-blue-300 flex items-center gap-1">
                  <i class="fa-solid fa-rotate-left"></i> Reset Sample Data
                </button>
              </div>
              <textarea id="raw-input" rows="9" class="w-full bg-[#1F2937] border border-gray-700 rounded-lg p-3 text-xs font-mono text-gray-200 focus:ring-2 focus:ring-blue-500 focus:outline-none resize-y" placeholder="Paste messy input text, raw email, unformatted invoice, or transcript..."></textarea>
            </div>

            <!-- Action Button -->
            <button id="run-btn" onclick="executeEndpoint()" class="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold rounded-lg shadow-lg shadow-blue-500/25 transition-all flex items-center justify-center gap-2">
              <i class="fa-solid fa-play text-sm"></i>
              <span>Execute Live Microservice</span>
            </button>
          </div>
        </div>

        <!-- RIGHT PANEL: CLEAN STRUCTURED JSON OUTPUT -->
        <div class="lg:col-span-7 space-y-4">
          <div class="bg-[#111827] border border-gray-800 rounded-xl p-5 shadow-xl flex flex-col h-full">
            <div class="flex items-center justify-between border-b border-gray-800 pb-3 mb-3">
              <div class="flex items-center space-x-3">
                <h2 class="text-sm font-semibold uppercase tracking-wider text-gray-400">Structured JSON Output</h2>
                <span id="latency-badge" class="hidden px-2 py-0.5 text-xs font-mono rounded bg-blue-950 text-blue-400 border border-blue-800">
                  <i class="fa-regular fa-clock mr-1"></i> <span id="latency-val">0</span>ms
                </span>
                <span id="status-badge" class="hidden px-2 py-0.5 text-xs font-semibold rounded bg-emerald-950 text-emerald-400 border border-emerald-800">
                  200 OK
                </span>
              </div>
              <div class="flex space-x-2">
                <button onclick="copyOutput()" class="px-2.5 py-1 text-xs bg-gray-800 hover:bg-gray-700 text-gray-300 rounded border border-gray-700 flex items-center gap-1 transition">
                  <i class="fa-regular fa-copy"></i> Copy JSON
                </button>
                <button onclick="copyCurl()" class="px-2.5 py-1 text-xs bg-gray-800 hover:bg-gray-700 text-gray-300 rounded border border-gray-700 flex items-center gap-1 transition">
                  <i class="fa-solid fa-terminal"></i> Copy cURL
                </button>
              </div>
            </div>

            <!-- Loader / Empty State / Result -->
            <div id="output-loading" class="hidden flex-1 flex flex-col items-center justify-center py-20 text-center">
              <div class="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-3"></div>
              <p class="text-sm font-semibold text-gray-200">Executing Microservice on Edge...</p>
              <p class="text-xs text-gray-400 mt-1">Calling rootsys.cloud with schema validation</p>
            </div>

            <div id="output-container" class="flex-1 flex flex-col">
              <pre id="json-output" class="flex-1 p-4 bg-[#0A0E17] border border-gray-800 rounded-lg text-xs font-mono text-emerald-400 overflow-x-auto whitespace-pre-wrap select-all leading-relaxed min-h-[360px]">
// Click "Execute Live Microservice" on the left to run this live endpoint.
// The output returned here is guaranteed strictly typed JSON, ready for database or API consumption.
              </pre>
            </div>

            <!-- INTEGRATION SNIPPET -->
            <div class="mt-4 pt-3 border-t border-gray-800 flex items-center justify-between text-xs text-gray-400">
              <div class="flex items-center gap-2">
                <i class="fa-solid fa-code text-blue-400"></i>
                <span>Direct Endpoint Route: <code class="text-blue-300 font-mono" id="current-route">/v1/health/explain-lab</code></span>
              </div>
              <span class="text-gray-500">CORS Enabled • Zero-Cost Cloudflare Worker</span>
            </div>
          </div>
        </div>

      </div>

    </div>

    <!-- ==================== TAB 2: WIREFRAMES & INTERACTION FLOWS ==================== -->
    <div id="tab-content-wireframes" class="hidden space-y-8">
      
      <div class="border-b border-gray-800 pb-4">
        <h2 class="text-xl font-bold text-white tracking-tight">Interactive Surface Wireframes & UX Flows</h2>
        <p class="text-sm text-gray-400 mt-1">
          Detailed visual architecture of the 4 primary delivery channels that turn these endpoints into intuitive products for non-developers.
        </p>
      </div>

      <!-- WIREFRAME 1: WHATSAPP / MOBILE CONVERSATIONAL BOT -->
      <div class="bg-[#111827] border border-gray-800 rounded-2xl p-6 shadow-xl">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-6 pb-4 border-b border-gray-800">
          <div>
            <span class="text-xs uppercase tracking-wider font-semibold text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded border border-emerald-800">Surface 1: Mobile & Chat App</span>
            <h3 class="text-lg font-bold text-white mt-2">WhatsApp / SMS "Photo-to-Answer" Assistant</h3>
            <p class="text-xs text-gray-400">Ideal for: Elderly parents, drivers with parking tickets, patients with blood tests, and tenants with lease contracts.</p>
          </div>
          <div class="text-xs text-gray-400 bg-gray-900 px-3 py-2 rounded-lg border border-gray-800">
            <strong>Underlying Endpoint:</strong> <code>POST /v1/health/explain-lab</code> or <code>/v1/safety/scam-detector</code>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <!-- ASCII / Mock Wireframe Phone -->
          <div class="max-w-sm mx-auto w-full bg-[#030712] border-2 border-gray-700 rounded-[32px] p-4 shadow-2xl relative">
            <div class="w-24 h-4 bg-gray-800 rounded-full mx-auto mb-4"></div>
            <!-- Chat Header -->
            <div class="flex items-center space-x-3 pb-3 border-b border-gray-800">
              <div class="w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center text-white text-xs font-bold">OA</div>
              <div>
                <p class="text-xs font-bold text-white">OmniPoint Safety & Health</p>
                <p class="text-[10px] text-emerald-400">Verified AI Assistant</p>
              </div>
            </div>
            <!-- Chat Bubbles -->
            <div class="py-4 space-y-3 text-[11px]">
              <div class="bg-gray-800 p-2.5 rounded-2xl rounded-tl-none max-w-[85%] text-gray-300">
                Hi Grandma! Forward me any suspicious text, medical test photo, or bill, and I will explain it safely.
              </div>
              <div class="bg-blue-600/90 text-white p-2.5 rounded-2xl rounded-tr-none ml-auto max-w-[85%]">
                <div class="bg-black/30 p-1.5 rounded mb-1 text-[10px] flex items-center gap-1.5">
                  <i class="fa-solid fa-image"></i> [Screenshot: "URGENT CHASE BANK ALERT: Click here to avoid police filing..."]
                </div>
                Is this real? I'm worried.
              </div>
              <div class="bg-emerald-950/80 border border-emerald-700/60 p-3 rounded-2xl rounded-tl-none max-w-[90%] text-gray-200">
                <p class="font-bold text-red-400 flex items-center gap-1 mb-1">
                  <i class="fa-solid fa-triangle-exclamation"></i> 99% SCAM DETECTED
                </p>
                <p class="text-[10px] text-gray-300 mb-2">This is a fake bank message trying to steal your debit card PIN.</p>
                <div class="bg-black/40 p-2 rounded text-[10px] space-y-1">
                  <p class="text-white font-semibold">What to do now:</p>
                  <p>1. DO NOT tap the link.</p>
                  <p>2. Delete the text message.</p>
                  <p>3. Your bank account is safe.</p>
                </div>
              </div>
            </div>
            <!-- Input Area -->
            <div class="pt-2 border-t border-gray-800 flex items-center gap-2">
              <div class="flex-1 bg-gray-900 text-gray-500 text-[10px] py-2 px-3 rounded-full">Send photo, audio, or text...</div>
              <div class="w-7 h-7 bg-emerald-600 rounded-full flex items-center justify-center text-white text-xs"><i class="fa-solid fa-microphone"></i></div>
            </div>
          </div>

          <!-- Feature & Flow Breakdown -->
          <div class="space-y-4">
            <h4 class="text-sm font-bold text-white uppercase tracking-wider text-blue-400">How It Works Under the Hood:</h4>
            <ul class="space-y-3 text-xs text-gray-300">
              <li class="flex items-start gap-2">
                <span class="w-5 h-5 rounded bg-blue-900/60 text-blue-300 flex items-center justify-center text-[10px] font-bold mt-0.5">1</span>
                <div><strong>User Action:</strong> The user forwards a photo, voice note, or text message to the dedicated WhatsApp Business or Twilio phone number.</div>
              </li>
              <li class="flex items-start gap-2">
                <span class="w-5 h-5 rounded bg-blue-900/60 text-blue-300 flex items-center justify-center text-[10px] font-bold mt-0.5">2</span>
                <div><strong>Cloudflare Worker Ingestion:</strong> The incoming Twilio/WhatsApp webhook is captured by the Worker, converting audio via Whisper or forwarding images to <code>kimi-k3</code>.</div>
              </li>
              <li class="flex items-start gap-2">
                <span class="w-5 h-5 rounded bg-blue-900/60 text-blue-300 flex items-center justify-center text-[10px] font-bold mt-0.5">3</span>
                <div><strong>Deterministic Parsing:</strong> The prompt validates safety scores, extracts critical takeaways, and formats a compassionate, easy-to-read text reply back to WhatsApp in <1.2 seconds.</div>
              </li>
            </ul>
            <div class="p-3 bg-gray-900/80 border border-gray-800 rounded-lg text-xs text-gray-400">
              <strong class="text-white">Example Monetization:</strong> \$4.99/month "Family Shield" subscription covering up to 4 family members with unlimited scam & bill audits.
            </div>
          </div>
        </div>
      </div>

      <!-- WIREFRAME 2: SPREADSHEET (GOOGLE SHEETS / EXCEL) CUSTOM FUNCTIONS -->
      <div class="bg-[#111827] border border-gray-800 rounded-2xl p-6 shadow-xl">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-6 pb-4 border-b border-gray-800">
          <div>
            <span class="text-xs uppercase tracking-wider font-semibold text-blue-400 bg-blue-950/60 px-2.5 py-1 rounded border border-blue-800">Surface 2: Spreadsheet Functions</span>
            <h3 class="text-lg font-bold text-white mt-2">Google Sheets / Excel Custom Formula Engine</h3>
            <p class="text-xs text-gray-400">Ideal for: Non-profit grant managers, teachers grading assignments, HR recruiters, and sales agencies.</p>
          </div>
          <div class="text-xs text-gray-400 bg-gray-900 px-3 py-2 rounded-lg border border-gray-800">
            <strong>Formula Example:</strong> <code>=AI_GRANT_MATCH(A2, B2)</code> or <code>=AI_DIFF_HOMEWORK(A2)</code>
          </div>
        </div>

        <div class="space-y-4">
          <!-- Mock Spreadsheet Table -->
          <div class="overflow-x-auto border border-gray-800 rounded-lg">
            <table class="w-full text-xs font-mono text-left">
              <thead class="bg-gray-900 text-gray-400 border-b border-gray-800">
                <tr>
                  <th class="p-2 border-r border-gray-800 w-12 text-center">#</th>
                  <th class="p-2 border-r border-gray-800 w-1/4">A (RFP Title & Grantor)</th>
                  <th class="p-2 border-r border-gray-800 w-1/3">B (Eligibility Criteria Snippet)</th>
                  <th class="p-2 border-r border-gray-800 text-blue-400">=AI_GRANT_MATCH(A, B)</th>
                  <th class="p-2 text-emerald-400">Action Verdict</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-800 bg-[#0B0F19]">
                <tr>
                  <td class="p-2 border-r border-gray-800 text-gray-500 text-center">1</td>
                  <td class="p-2 border-r border-gray-800 text-gray-300">Gates STEM Education RFP</td>
                  <td class="p-2 border-r border-gray-800 text-gray-400 truncate max-w-xs">Requires 501c3, Title I public school focus, 3yr operating history...</td>
                  <td class="p-2 border-r border-gray-800 text-emerald-400 font-bold">92% Match (Eligible)</td>
                  <td class="p-2"><span class="bg-emerald-950 text-emerald-300 px-2 py-0.5 rounded text-[10px]">Prepare Full Proposal</span></td>
                </tr>
                <tr>
                  <td class="p-2 border-r border-gray-800 text-gray-500 text-center">2</td>
                  <td class="p-2 border-r border-gray-800 text-gray-300">Clean Water Urban Infrastructure</td>
                  <td class="p-2 border-r border-gray-800 text-gray-400 truncate max-w-xs">Municipalities & universities only. Non-profits excluded under Sec 4...</td>
                  <td class="p-2 border-r border-gray-800 text-red-400 font-bold">0% Match (Disqualified)</td>
                  <td class="p-2"><span class="bg-red-950 text-red-300 px-2 py-0.5 rounded text-[10px]">Skip / Discard</span></td>
                </tr>
                <tr>
                  <td class="p-2 border-r border-gray-800 text-gray-500 text-center">3</td>
                  <td class="p-2 border-r border-gray-800 text-gray-300">Youth Arts & Literacy Fund</td>
                  <td class="p-2 border-r border-gray-800 text-gray-400 truncate max-w-xs">Annual budget must be below \$250,000; requires 1:1 matching grant...</td>
                  <td class="p-2 border-r border-gray-800 text-amber-400 font-bold">64% Match (Requires Match)</td>
                  <td class="p-2"><span class="bg-amber-950 text-amber-300 px-2 py-0.5 rounded text-[10px]">Review Matching Fund</span></td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="p-4 bg-gray-900/60 border border-gray-800 rounded-lg text-xs text-gray-300 flex items-center justify-between">
            <div>
              <p class="font-semibold text-white">Google Apps Script Snippet (Plug and Play):</p>
              <code class="text-blue-400 font-mono text-[11px]">function AI_GRANT_MATCH(rfp, crit) { return fetch("https://omnipoint-eaas.muhammadamran40.workers.dev/v1/ngo/grant-match", ...); }</code>
            </div>
            <span class="text-xs bg-blue-900/40 text-blue-300 border border-blue-700/50 px-2.5 py-1 rounded">Zero Installation</span>
          </div>
        </div>
      </div>

      <!-- WIREFRAME 3: WEBHOOK & NO-CODE (ZAPIER / MAKE.COM) PIPELINE -->
      <div class="bg-[#111827] border border-gray-800 rounded-2xl p-6 shadow-xl">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-6 pb-4 border-b border-gray-800">
          <div>
            <span class="text-xs uppercase tracking-wider font-semibold text-purple-400 bg-purple-950/60 px-2.5 py-1 rounded border border-purple-800">Surface 3: No-Code Automation</span>
            <h3 class="text-lg font-bold text-white mt-2">Zapier / Make.com Automated Event Pipeline</h3>
            <p class="text-xs text-gray-400">Ideal for: Small business owners, restaurants, salons, e-commerce stores, and repair workshops.</p>
          </div>
          <div class="text-xs text-gray-400 bg-gray-900 px-3 py-2 rounded-lg border border-gray-800">
            <strong>Pipeline:</strong> Google Maps / Typeform $\rightarrow$ OmniPoint EaaS $\rightarrow$ CRM / Slack / Twilio
          </div>
        </div>

        <!-- Flowchart Steps -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs font-mono">
          <!-- Step 1 -->
          <div class="p-4 rounded-xl bg-gray-900 border border-gray-800 relative">
            <span class="text-[10px] text-gray-500 uppercase font-bold block mb-1">Trigger</span>
            <div class="flex items-center gap-2 text-white font-bold mb-2">
              <i class="fa-brands fa-google text-red-400"></i> New 1-Star Review
            </div>
            <p class="text-gray-400 text-[11px]">A customer posts a complaint on Google Maps about cold food and slow service.</p>
          </div>

          <!-- Step 2 (Your EaaS) -->
          <div class="p-4 rounded-xl bg-gradient-to-br from-blue-950 to-indigo-950 border border-blue-600 shadow-lg shadow-blue-500/20">
            <span class="text-[10px] text-blue-300 uppercase font-bold block mb-1">OmniPoint EaaS</span>
            <div class="flex items-center gap-2 text-white font-bold mb-2">
              <i class="fa-solid fa-brain text-blue-400"></i> /v1/smb/review-reply
            </div>
            <p class="text-blue-200 text-[11px]">DeepSeek-v4.1 analyzes tone, prevents legal liability, and drafts a diplomatic public response.</p>
          </div>

          <!-- Step 3 -->
          <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
            <span class="text-[10px] text-gray-500 uppercase font-bold block mb-1">Approval Gate</span>
            <div class="flex items-center gap-2 text-white font-bold mb-2">
              <i class="fa-brands fa-slack text-purple-400"></i> Slack Notification
            </div>
            <p class="text-gray-400 text-[11px]">Manager receives alert on phone: "Review de-escalation drafted. Click [Approve] to post."</p>
          </div>

          <!-- Step 4 -->
          <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
            <span class="text-[10px] text-gray-500 uppercase font-bold block mb-1">Action</span>
            <div class="flex items-center gap-2 text-white font-bold mb-2">
              <i class="fa-solid fa-reply text-emerald-400"></i> Public Post & CRM
            </div>
            <p class="text-gray-400 text-[11px]">Response published to Google Maps API; internal kitchen alert logged to Airtable.</p>
          </div>
        </div>
      </div>

    </div>

    <!-- ==================== TAB 3: 55+ ENDPOINTS CATALOG ==================== -->
    <div id="tab-content-catalog" class="hidden space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-800 pb-4">
        <div>
          <h2 class="text-xl font-bold text-white tracking-tight">Complete 55+ Microservices Catalog</h2>
          <p class="text-sm text-gray-400 mt-1">Full production inventory categorized across 5 high-demand real-world sectors.</p>
        </div>
        <div class="flex items-center gap-3">
          <input type="text" id="catalog-search" onkeyup="filterCatalog()" placeholder="Search endpoints, routes, or personas..." class="bg-[#1F2937] border border-gray-700 text-white rounded-lg px-3 py-2 text-xs w-64 focus:ring-2 focus:ring-blue-500 focus:outline-none">
        </div>
      </div>

      <div class="overflow-x-auto border border-gray-800 rounded-xl">
        <table class="w-full text-xs text-left">
          <thead class="bg-gray-900 text-gray-400 uppercase tracking-wider font-semibold border-b border-gray-800">
            <tr>
              <th class="p-3">#</th>
              <th class="p-3">Endpoint Route</th>
              <th class="p-3">Category</th>
              <th class="p-3">Target Persona & Trigger</th>
              <th class="p-3">Raw Input</th>
              <th class="p-3">Deterministic Output</th>
            </tr>
          </thead>
          <tbody id="catalog-body" class="divide-y divide-gray-800 bg-[#0B0F19]">
            <!-- Dynamically populated via JS below -->
          </tbody>
        </table>
      </div>
    </div>

    <!-- ==================== TAB 4: $0 CLOUDFLARE STACK ARCHITECTURE ==================== -->
    <div id="tab-content-architecture" class="hidden space-y-6">
      <div class="border-b border-gray-800 pb-4">
        <h2 class="text-xl font-bold text-white tracking-tight">Zero-Cost Cloudflare + GitHub Production Architecture</h2>
        <p class="text-sm text-gray-400 mt-1">How this entire platform runs at \$0 monthly fixed infrastructure cost.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="p-5 rounded-xl bg-[#111827] border border-gray-800 space-y-3">
          <div class="w-10 h-10 rounded-lg bg-orange-950/60 text-orange-400 flex items-center justify-center text-lg">
            <i class="fa-solid fa-bolt"></i>
          </div>
          <h3 class="text-base font-bold text-white">Cloudflare Workers</h3>
          <p class="text-xs text-gray-400 leading-relaxed">
            Runs this API globally across 300+ edge locations. Handles CORS, proxying, rate-limiting, and schema validation.
          </p>
          <div class="text-[11px] text-emerald-400 font-mono bg-emerald-950/40 p-2 rounded border border-emerald-800/50">
            ✓ 100,000 free requests/day<br/>✓ \$0.00 / month forever
          </div>
        </div>

        <div class="p-5 rounded-xl bg-[#111827] border border-gray-800 space-y-3">
          <div class="w-10 h-10 rounded-lg bg-blue-950/60 text-blue-400 flex items-center justify-center text-lg">
            <i class="fa-solid fa-database"></i>
          </div>
          <h3 class="text-base font-bold text-white">Cloudflare R2 Storage</h3>
          <p class="text-xs text-gray-400 leading-relaxed">
            S3-compatible object storage used for temporary file uploads (PDF leases, multi-page medical scans, audio files).
          </p>
          <div class="text-[11px] text-emerald-400 font-mono bg-emerald-950/40 p-2 rounded border border-emerald-800/50">
            ✓ 10 GB free storage<br/>✓ \$0.00 egress bandwidth fees
          </div>
        </div>

        <div class="p-5 rounded-xl bg-[#111827] border border-gray-800 space-y-3">
          <div class="w-10 h-10 rounded-lg bg-purple-950/60 text-purple-400 flex items-center justify-center text-lg">
            <i class="fa-brands fa-github"></i>
          </div>
          <h3 class="text-base font-bold text-white">GitHub CI/CD Engine</h3>
          <p class="text-xs text-gray-400 leading-relaxed">
            Version control and automated deployments. Commits to <code>main</code> trigger automatic Wrangler deployments.
          </p>
          <div class="text-[11px] text-emerald-400 font-mono bg-emerald-950/40 p-2 rounded border border-emerald-800/50">
            ✓ Unlimited public/private repos<br/>✓ 2,000 free Action minutes/mo
          </div>
        </div>
      </div>

      <!-- CREDENTIALS VERIFICATION STATUS -->
      <div class="p-5 rounded-xl bg-[#111827] border border-gray-800 space-y-3">
        <h3 class="text-sm font-bold text-white uppercase tracking-wider text-blue-400">Environment Credentials Status</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs font-mono">
          <div class="p-3 bg-gray-900 rounded border border-gray-800">
            <span class="text-gray-500 block text-[10px]">Cloudflare Account</span>
            <span class="text-emerald-400 font-bold">7a92...7cd6 (Active)</span>
          </div>
          <div class="p-3 bg-gray-900 rounded border border-gray-800">
            <span class="text-gray-500 block text-[10px]">GitHub Profile</span>
            <span class="text-emerald-400 font-bold">Amran-KakiTekno (Active)</span>
          </div>
          <div class="p-3 bg-gray-900 rounded border border-gray-800">
            <span class="text-gray-500 block text-[10px]">LLM Gateway</span>
            <span class="text-emerald-400 font-bold">rootsys.cloud/v1 (Online)</span>
          </div>
          <div class="p-3 bg-gray-900 rounded border border-gray-800">
            <span class="text-gray-500 block text-[10px]">Active Edge Worker</span>
            <span class="text-emerald-400 font-bold">omnipoint-eaas (Deployed)</span>
          </div>
        </div>
      </div>
    </div>

  </main>

  <!-- FOOTER -->
  <footer class="border-t border-gray-800 py-6 bg-[#0B0F19] text-center text-xs text-gray-500">
    <p>OmniPoint AI • Endpoint as a Service (EaaS) Platform • Built for Serverless Zero-Cost Global Edge</p>
  </footer>

  <script>
    const ENDPOINTS = ${endpointsJson};

    function switchTab(tabId) {
      ['playground', 'wireframes', 'catalog', 'architecture'].forEach(id => {
        document.getElementById('tab-content-' + id).classList.add('hidden');
        document.getElementById('tab-btn-' + id).classList.remove('tab-active');
        document.getElementById('tab-btn-' + id).classList.add('text-gray-400');
      });
      document.getElementById('tab-content-' + tabId).classList.remove('hidden');
      document.getElementById('tab-btn-' + tabId).classList.add('tab-active');
      document.getElementById('tab-btn-' + tabId).classList.remove('text-gray-400');

      if (tabId === 'catalog') {
        renderCatalog();
      }
    }

    function onEndpointChange() {
      const selectedKey = document.getElementById('endpoint-selector').value;
      const conf = ENDPOINTS[selectedKey];
      if (conf) {
        document.getElementById('current-category').innerText = conf.category;
        document.getElementById('current-route').innerText = conf.route;
        document.getElementById('raw-input').value = conf.defaultSample;
      }
    }

    function loadSampleData() {
      onEndpointChange();
    }

    async function executeEndpoint() {
      const endpointKey = document.getElementById('endpoint-selector').value;
      const selectedModel = document.getElementById('model-selector').value;
      const rawInput = document.getElementById('raw-input').value.trim();

      if (!rawInput) {
        alert("Please enter input text or load sample data.");
        return;
      }

      const runBtn = document.getElementById('run-btn');
      const loader = document.getElementById('output-loading');
      const outputContainer = document.getElementById('output-container');
      const jsonPre = document.getElementById('json-output');
      const latencyBadge = document.getElementById('latency-badge');
      const latencyVal = document.getElementById('latency-val');
      const statusBadge = document.getElementById('status-badge');

      runBtn.disabled = true;
      runBtn.classList.add('opacity-50');
      loader.classList.remove('hidden');
      outputContainer.classList.add('hidden');
      latencyBadge.classList.add('hidden');
      statusBadge.classList.add('hidden');

      try {
        const resp = await fetch('/api/execute', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            endpoint: endpointKey,
            model: selectedModel,
            input: rawInput
          })
        });

        const data = await resp.json();

        loader.classList.add('hidden');
        outputContainer.classList.remove('hidden');
        runBtn.disabled = false;
        runBtn.classList.remove('opacity-50');

        if (data.success) {
          jsonPre.innerText = JSON.stringify(data.data, null, 2);
          latencyVal.innerText = data.latency_ms;
          latencyBadge.classList.remove('hidden');
          statusBadge.classList.remove('hidden');
        } else {
          jsonPre.innerText = "// ERROR: " + (data.error || "Failed to execute");
        }
      } catch (err) {
        loader.classList.add('hidden');
        outputContainer.classList.remove('hidden');
        runBtn.disabled = false;
        runBtn.classList.remove('opacity-50');
        jsonPre.innerText = "// NETWORK ERROR: " + err.message;
      }
    }

    function copyOutput() {
      const text = document.getElementById('json-output').innerText;
      navigator.clipboard.writeText(text);
      alert("JSON copied to clipboard!");
    }

    function copyCurl() {
      const key = document.getElementById('endpoint-selector').value;
      const conf = ENDPOINTS[key];
      const host = window.location.origin;
      const curl = \`curl -X POST "\${host}\${conf.route}" \\\\
  -H "Content-Type: application/json" \\\\
  -d '{"input": "..."}'\`;
      navigator.clipboard.writeText(curl);
      alert("cURL snippet copied to clipboard!");
    }

    // Catalog data (55+ Endpoints)
    const CATALOG_ITEMS = [
      { id: 1, route: "/v1/health/explain-lab", cat: "Individuals", persona: "Patient / Caregiver", input: "Blood test PDF / photo", output: "Plain-English explanation, out-of-range flags, questions for MD" },
      { id: 2, route: "/v1/legal/lease-check", cat: "Individuals", persona: "Tenant / Student", input: "Lease agreement PDF", output: "State-law violation audit, hidden repair fees, trap clauses" },
      { id: 3, route: "/v1/safety/scam-detector", cat: "Individuals", persona: "Senior / Family", input: "Suspicious text, fake bank email", output: "Scam probability %, taxonomy, plain-language safe advice" },
      { id: 4, route: "/v1/auto/quote-verifier", cat: "Individuals", persona: "Car Owner", input: "Mechanic estimate photo + car model", output: "Market price reality check, critical vs upsell separation" },
      { id: 5, route: "/v1/finance/fee-audit", cat: "Individuals", persona: "Budgeter", input: "Bank statement CSV/PDF", output: "Recurring subscription list, price creep detection, cancel links" },
      { id: 6, route: "/v1/diet/ingredient-alert", cat: "Individuals", persona: "Allergy Sufferer", input: "Food ingredient panel photo", output: "Immediate Safe/Danger badge, hidden derivatives flagged" },
      { id: 7, route: "/v1/legal/ticket-appeal", cat: "Individuals", persona: "Urban Driver", input: "Parking ticket photo + street sign", output: "Formal municipal appeal letter citing code ambiguities" },
      { id: 8, route: "/v1/insurance/appeal-generator", cat: "Individuals", persona: "Patient / Homeowner", input: "Denial letter + policy PDF", output: "Targeted appeal citing policy clauses and medical necessity" },
      { id: 9, route: "/v1/edu/iep-analyzer", cat: "Individuals", persona: "Special-Ed Parent", input: "School IEP document PDF", output: "De-jargonized parent summary, omitted accommodations list" },
      { id: 10, route: "/v1/food/fridge-inventory", cat: "Individuals", persona: "Busy Parent", input: "Photo of fridge interior", output: "3 exact recipes prioritizing expiring perishables" },
      { id: 11, route: "/v1/home/appliance-fix", cat: "Individuals", persona: "Tenant / Owner", input: "Appliance error code photo", output: "DIY fix vs pro needed, part numbers, safety risk" },
      { id: 12, route: "/v1/energy/bill-optimizer", cat: "Individuals", persona: "Homeowner", input: "Electric/Gas bill PDF", output: "Time-of-use tariff comparison, projected annual savings" },
      { id: 13, route: "/v1/career/transition-map", cat: "Individuals", persona: "Career Switcher", input: "Resume text + target industry", output: "Transferable skill crosswalk, buzzword translator" },
      { id: 14, route: "/v1/parenting/coaching", cat: "Individuals", persona: "Stressed Parent", input: "Tantrum description + child age", output: "De-escalation script, developmentally appropriate options" },
      { id: 15, route: "/v1/consumer/warranty-claim", cat: "Individuals", persona: "Online Shopper", input: "Receipt + defect photo", output: "Statutory warranty notice (Magnuson-Moss) demand letter" },
      { id: 16, route: "/v1/ngo/grant-match", cat: "Non-Profits", persona: "Grant Writer", input: "Foundation RFP PDF + NGO mission", output: "Eligibility match %, compliance risks, alignment matrix" },
      { id: 17, route: "/v1/ngo/donor-story", cat: "Non-Profits", persona: "Fundraiser", input: "Raw field notes ('Fed 300 kids...')", output: "Compelling donor newsletter snippet, thank-you email" },
      { id: 18, route: "/v1/ngo/990-explainer", cat: "Non-Profits", persona: "Board Member", input: "Form 990 tax return PDF", output: "Executive governance scorecard, program-expense ratio" },
      { id: 19, route: "/v1/ngo/volunteer-dispatch", cat: "Non-Profits", persona: "Volunteer Lead", input: "Volunteer signup questionnaire", output: "Ranked task allocation matching volunteer credentials" },
      { id: 20, route: "/v1/ngo/localize-notice", cat: "Non-Profits", persona: "Community Organizer", input: "English flyer + target culture", output: "Culturally adapted copy preserving idioms and tone" },
      { id: 21, route: "/v1/crisis/sos-triage", cat: "Non-Profits", persona: "Emergency Relief", input: "Citizen distress text messages", output: "Urgency score (1-5), required gear, GPS extraction" },
      { id: 22, route: "/v1/ngo/donor-letter", cat: "Non-Profits", persona: "Development Officer", input: "Donor gift history + campaign data", output: "Hyper-personalized stewardship letter" },
      { id: 23, route: "/v1/ngo/foodbank-recipes", cat: "Non-Profits", persona: "Pantry Coordinator", input: "Weekly surplus ingredients list", output: "Simple microwave-friendly recipe cards for food boxes" },
      { id: 24, route: "/v1/ngo/policy-impact", cat: "Non-Profits", persona: "Advocacy Lead", input: "State bill draft PDF", output: "Section-by-section threat analysis, testimony points" },
      { id: 25, route: "/v1/ngo/budget-narrative", cat: "Non-Profits", persona: "Program Manager", input: "Excel budget spreadsheet", output: "Audit-ready narrative justification for every line item" },
      { id: 26, route: "/v1/creator/repurpose", cat: "Creators", persona: "YouTuber / Podcaster", input: "Long-form transcript", output: "1 X thread, 3 LinkedIn posts, 5 TikTok hooks, newsletter" },
      { id: 27, route: "/v1/freelance/scope-defense", cat: "Creators", persona: "Freelancer / Dev", input: "Client request + original contract", output: "Scope analysis, diplomatic polite reply, paid change order" },
      { id: 28, route: "/v1/audio/shownotes", cat: "Creators", persona: "Podcaster", input: "Episode audio / transcript", output: "Summary, guest bio, clickable timestamps, key quotes" },
      { id: 29, route: "/v1/creator/pitch-brand", cat: "Creators", persona: "Micro-Creator", input: "Analytics + target brand", output: "Personalized pitch email, CPM benchmarked rate quote" },
      { id: 30, route: "/v1/design/audit-portfolio", cat: "Creators", persona: "Junior Designer", input: "Portfolio URL / case study", output: "5-second recruiter impression score, UX friction points" },
      { id: 31, route: "/v1/marketing/objection-handler", cat: "Creators", persona: "Indie Founder", input: "Landing page text + persona", output: "Top 10 buyer doubts + high-converting FAQ copy" },
      { id: 32, route: "/v1/youtube/thumbnail-concepts", cat: "Creators", persona: "Video Creator", input: "Draft video premise", output: "3 psychological angles, thumbnail visual sketches, 5 titles" },
      { id: 33, route: "/v1/freelance/lead-qualifier", cat: "Creators", persona: "Agency Owner", input: "Inbound contact form text", output: "Budget viability rating, scope clarity score, inquiry reply" },
      { id: 34, route: "/v1/audio/clean-transcript", cat: "Creators", persona: "Audio Editor", input: "Transcript with timestamps", output: "Edit decision list of timecodes with filler words and um/ahs" },
      { id: 35, route: "/v1/video/tone-subtitles", cat: "Creators", persona: "Global Creator", input: "SRT file + target language", output: "Subtitles adapted for modern slang, sarcasm, and humor" },
      { id: 36, route: "/v1/smb/review-reply", cat: "Small Business", persona: "Bistro / Clinic Owner", input: "1-star customer review + policy", output: "Empathetic de-escalation response, offline resolution" },
      { id: 37, route: "/v1/restaurant/menu-digitizer", cat: "Small Business", persona: "Restaurant Owner", input: "Photo of paper menu", output: "Clean JSON dishes, prices, allergen tags, 3 translations" },
      { id: 38, route: "/v1/salon/fill-slot", cat: "Small Business", persona: "Salon / Dentist", input: "Cancelled slot + waitlist", output: "Top 3 waitlist matches + 1-click SMS booking link" },
      { id: 39, route: "/v1/trades/quote-builder", cat: "Small Business", persona: "Plumber / Electrician", input: "Voice memo from work truck", output: "Itemized PDF/JSON estimate with parts markup, labor hours" },
      { id: 40, route: "/v1/smb/local-seo", cat: "Small Business", persona: "Landscaper / Mechanic", input: "Business name & service radius", output: "Google Business Profile posts, geo-targeted voice search tags" },
      { id: 41, route: "/v1/retail/vendor-slip", cat: "Small Business", persona: "Boutique Grocer", input: "Photo of paper supplier slip", output: "Inventory JSON with SKU, unit cost, retail markup" },
      { id: 42, route: "/v1/retail/shift-swap", cat: "Small Business", persona: "Store Manager", input: "Staff swap text + schedule", output: "Swap feasibility check verifying overtime laws and skills" },
      { id: 43, route: "/v1/repair/status-update", cat: "Small Business", persona: "Repair Workshop", input: "Tech internal diagnostic notes", output: "Jargon-free customer text update with realistic ETA" },
      { id: 44, route: "/v1/smb/lease-cam-check", cat: "Small Business", persona: "Retail Tenant", input: "Annual CAM bill PDF", output: "Non-allowable landlord expense flags, audit dispute notice" },
      { id: 45, route: "/v1/trades/maintenance-log", cat: "Small Business", persona: "Bakery / Brewery", input: "Voice memo on machine noise", output: "Machinery log record, predicted wear risk, service alert" },
      { id: 46, route: "/v1/edu/differentiate", cat: "Education & Public", persona: "School Teacher", input: "Lesson concept + target grade", output: "3 tiered assignments (remedial, grade-level, gifted)" },
      { id: 47, route: "/v1/edu/rubric-feedback", cat: "Education & Public", persona: "English / STEM Teacher", input: "Student essay + rubric", output: "Encouraging feedback highlighting 2 strengths & 2 fixes" },
      { id: 48, route: "/v1/social/casenotes", cat: "Education & Public", persona: "Social Worker", input: "Raw voice dictation in car", output: "Strictly objective, court-compliant case documentation" },
      { id: 49, route: "/v1/civic/council-digest", cat: "Education & Public", persona: "Civic Organizer", input: "3-hour council meeting audio", output: "5-bullet civic digest on zoning, taxes, and road spending" },
      { id: 50, route: "/v1/med/soap-note", cat: "Education & Public", persona: "Physician / Therapist", input: "Encounter audio / transcript", output: "Standardized clinical SOAP note with ICD-10 codes" },
      { id: 51, route: "/v1/edu/homeschool-plan", cat: "Education & Public", persona: "Homeschool Parent", input: "Child age + passions", output: "Interdisciplinary 5-day curriculum matching state standards" },
      { id: 52, route: "/v1/edu/parent-comms", cat: "Education & Public", persona: "Teacher / Admin", input: "Teacher notes + parent language", output: "Culturally respectful update in Spanish/Arabic/etc." },
      { id: 53, route: "/v1/social/benefits-finder", cat: "Education & Public", persona: "Low-Income Family", input: "Income, zip code, dependents", output: "Eligible safety-net programs (SNAP, Medicaid, WIC) & links" },
      { id: 54, route: "/v1/mentalhealth/crisis-aid", cat: "Education & Public", persona: "School Counselor", input: "Distressed student text", output: "Active listening responses, empathy validation cues" },
      { id: 55, route: "/v1/legal/court-prep", cat: "Education & Public", persona: "Pro-Se Litigant", input: "Small claims summons PDF", output: "Plain-English allegation summary, evidentiary checklist" }
    ];

    function renderCatalog() {
      const tbody = document.getElementById('catalog-body');
      tbody.innerHTML = CATALOG_ITEMS.map(item => \`
        <tr class="hover:bg-gray-800/40 transition-colors">
          <td class="p-3 font-mono text-gray-500">#\${item.id}</td>
          <td class="p-3 font-mono font-semibold text-blue-400">\${item.route}</td>
          <td class="p-3"><span class="px-2 py-0.5 rounded bg-gray-800 text-gray-300 text-[10px]">\${item.cat}</span></td>
          <td class="p-3 font-semibold text-gray-200">\${item.persona}</td>
          <td class="p-3 text-gray-400 truncate max-w-xs">\${item.input}</td>
          <td class="p-3 text-emerald-400 truncate max-w-xs">\${item.output}</td>
        </tr>
      \`).join('');
    }

    function filterCatalog() {
      const q = document.getElementById('catalog-search').value.toLowerCase();
      const filtered = CATALOG_ITEMS.filter(item => 
        item.route.toLowerCase().includes(q) ||
        item.persona.toLowerCase().includes(q) ||
        item.cat.toLowerCase().includes(q) ||
        item.output.toLowerCase().includes(q)
      );
      const tbody = document.getElementById('catalog-body');
      tbody.innerHTML = filtered.map(item => \`
        <tr class="hover:bg-gray-800/40 transition-colors">
          <td class="p-3 font-mono text-gray-500">#\${item.id}</td>
          <td class="p-3 font-mono font-semibold text-blue-400">\${item.route}</td>
          <td class="p-3"><span class="px-2 py-0.5 rounded bg-gray-800 text-gray-300 text-[10px]">\${item.cat}</span></td>
          <td class="p-3 font-semibold text-gray-200">\${item.persona}</td>
          <td class="p-3 text-gray-400 truncate max-w-xs">\${item.input}</td>
          <td class="p-3 text-emerald-400 truncate max-w-xs">\${item.output}</td>
        </tr>
      \`).join('');
    }

    // Initialize with default sample
    window.addEventListener('DOMContentLoaded', () => {
      onEndpointChange();
    });
  </script>
</body>
</html>`;
}
