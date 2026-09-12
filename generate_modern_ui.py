import json
import subprocess
import os

# Complete prompts dictionary from index.js
ENDPOINT_PROMPTS = {
  "explain-lab": {
    "name": "Medical Lab Report Explainer",
    "route": "/v1/health/explain-lab",
    "category": "Individuals & Consumers",
    "systemPrompt": """You are a medical diagnostics communication specialist. 
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
}""",
    "defaultSample": """Comprehensive Metabolic Panel & CBC:
- Fasting Glucose: 118 mg/dL (Reference: 70-99 mg/dL) [HIGH]
- Hemoglobin A1c: 5.9% (Reference: < 5.7%) [HIGH]
- Total Cholesterol: 224 mg/dL (Reference: < 200 mg/dL) [HIGH]
- LDL Cholesterol: 142 mg/dL (Reference: < 100 mg/dL) [HIGH]
- Triglycerides: 165 mg/dL (Reference: < 150 mg/dL) [HIGH]
- ALT (Liver enzyme): 38 U/L (Reference: 7-56 U/L) [NORMAL]
- Creatinine: 0.9 mg/dL (Reference: 0.6-1.2 mg/dL) [NORMAL]"""
  },

  "lease-check": {
    "name": "Apartment Lease Red-Flag Auditor",
    "route": "/v1/legal/lease-check",
    "category": "Individuals & Consumers",
    "systemPrompt": """You are a tenant rights attorney auditor. 
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
}""",
    "defaultSample": """Section 9. Maintenance and Repairs:
"Tenant shall be responsible for all repairs under $350, including plumbing clogs, HVAC filter servicing, electrical switches, and appliance maintenance. Landlord shall not be liable for lack of heating during winter months if maintenance parts are on backorder."

Section 14. Entry & Inspection:
"Landlord reserves the right to enter the leased premises at any time without advance written notice for routine inspections, showing to prospective buyers, or general premises auditing."

Section 22. Security Deposit:
"A non-refundable refurbishment and administrative fee of $500 will be deducted from the security deposit upon vacancy, irrespective of apartment condition."""
  },

  "scam-detector": {
    "name": "Elder Scam & Phishing Defender",
    "route": "/v1/safety/scam-detector",
    "category": "Individuals & Consumers",
    "systemPrompt": """You are a cybersecurity and fraud defense investigator.
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
}""",
    "defaultSample": """URGENT NOTICE FROM CHASE FRAUD ALERT:
Your online access has been temporarily restricted due to 3 suspicious transactions totaling $1,420.89 in Chicago, IL.
If you did not authorize these charges, you must immediately verify your identity and debit card PIN within 15 minutes by clicking:
https://chase-security-resolver-update82.com/login?token=92842
Failure to respond will result in immediate permanent account suspension and police filing."""
  },

  "review-reply": {
    "name": "Google Business Review De-escalator",
    "route": "/v1/smb/review-reply",
    "category": "Local Small Businesses",
    "systemPrompt": """You are a high-end customer relations and brand PR director.
Generate a public response to a customer review that validates their frustration, preserves brand reputation, avoids admitting legal liability, and moves resolution offline.
CRITICAL: Output strictly valid JSON.
Format:
{
  "sentiment": "negative|neutral|positive",
  "urgency": "low|medium|high",
  "primary_complaint": "...",
  "recommended_public_reply": "...",
  "internal_process_fix": "What the staff should fix behind the scenes"
}""",
    "defaultSample": """1-Star Review on Google Maps for "Mario's Wood-Fired Pizzeria":
"Waited 55 minutes for two pizzas on a Tuesday night. When they finally arrived, the crust was burnt on the bottom and cold on top. The waiter never checked on our drinks and when I asked for the manager, he acted like I was bothering him. Overpriced garbage. Will never come back with my family."""
  },

  "grant-match": {
    "name": "Grant RFP Criteria Matcher",
    "route": "/v1/ngo/grant-match",
    "category": "Non-Profits & NGOs",
    "systemPrompt": """You are a seasoned non-profit foundation grant evaluation officer.
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
}""",
    "defaultSample": """GRANT RFP:
Funder: The Global Green Community Trust
Grant Size: $50,000 - $120,000
Eligibility Requirements: Must be a registered 501(c)(3) operating for at least 3 years. Focus must be urban agricultural education or youth-led local food justice. Overhead/indirect administrative costs capped at 10%. Projects must track number of youth trained and pounds of fresh produce distributed.

APPLICANT NGO PROFILE:
Organization: CityRoots Community Gardens (501c3 founded 2021)
Annual Budget: $320,000
Mission: Transforming vacant municipal lots into community micro-farms in underserved food deserts, providing after-school apprenticeships to high schoolers."""
  },

  "scope-defense": {
    "name": "Client Scope Creep Defense Assistant",
    "route": "/v1/freelance/scope-defense",
    "category": "Creators & Solopreneurs",
    "systemPrompt": """You are a freelance contract strategist and client diplomacy expert.
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
}""",
    "defaultSample": """ORIGINAL CONTRACT SCOPE:
"Design and build a 5-page responsive marketing website (Home, About, Services, Case Studies, Contact) in Webflow. Includes 2 rounds of design revisions. CMS integration for 10 case studies."

INCOMING CLIENT MESSAGE:
"Hi Alex! Love the progress on the site. Since we have a couple days before launch, could you also quickly hook up a multi-step user registration portal where clients can log in to upload PDF files and view their invoice history? It shouldn't take too long since it's just adding an account button. Thanks!"""
  },

  "differentiate": {
    "name": "Differentiated Homework Generator",
    "route": "/v1/edu/differentiate",
    "category": "Education & Public Service",
    "systemPrompt": """You are a master pedagogical curriculum designer.
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
}""",
    "defaultSample": """Grade Level: 7th Grade Science
Topic: Ecosystems & Food Webs
Learning Goal: Students must demonstrate understanding of how energy flows through trophic levels (producers, primary consumers, secondary consumers, apex predators) and what happens when an invasive species disrupts the balance."""
  },

  "invoice-extract": {
    "name": "Universal Invoice & Receipt to JSON",
    "route": "/v1/extract/invoice",
    "category": "Data Extraction & OCR",
    "systemPrompt": """You are an automated document parsing and accounting data extraction engine.
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
}""",
    "defaultSample": """INVOICE #INV-884920
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
Payment: Net 30 days. Wire to Bank of America Acct ending in 4921."""
  }
}

def generate_html():
    prompts_json = json.dumps(ENDPOINT_PROMPTS)
    html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Smart EaaS — The Deterministic AI Microservice Directory</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">

  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Inter', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          }},
          colors: {{
            brand: {{
              50: '#eef2ff',
              100: '#e0e7ff',
              400: '#818cf8',
              500: '#6366f1',
              600: '#4f46e5',
            }}
          }}
        }}
      }}
    }}
  </script>

  <style>
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: #09090b; }}
    ::-webkit-scrollbar-thumb {{ background: #27272a; border-radius: 9999px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: #3f3f46; }}

    .grid-bg {{
      background-image: radial-gradient(rgba(255, 255, 255, 0.07) 1px, transparent 1px);
      background-size: 24px 24px;
    }}
    .card-hover {{
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .card-hover:hover {{
      transform: translateY(-2px);
      border-color: rgba(255, 255, 255, 0.22);
      box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.6);
    }}
  </style>
</head>
<body class="bg-[#09090b] text-[#f4f4f5] antialiased min-h-screen flex flex-col font-sans selection:bg-indigo-500/30 selection:text-indigo-200">

  <!-- TOP NAVIGATION (skills.sh style) -->
  <header class="sticky top-0 z-40 border-b border-white/[0.08] bg-[#09090b]/80 backdrop-blur-xl">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
      
      <!-- Brand -->
      <div class="flex items-center space-x-3">
        <a href="#" class="flex items-center space-x-2.5 group">
          <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-indigo-500 via-indigo-600 to-purple-600 flex items-center justify-center text-white text-xs font-bold shadow-md shadow-indigo-500/20 group-hover:scale-105 transition-transform">
            <i class="fa-solid fa-bolt"></i>
          </div>
          <span class="font-semibold text-sm tracking-tight text-white flex items-center gap-1.5">
            Smart EaaS
            <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-white/[0.06] text-zinc-400 border border-white/[0.08]">v2.0</span>
          </span>
        </a>

        <div class="hidden sm:flex items-center gap-2 pl-3 border-l border-white/[0.08]">
          <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            Edge Ready (Cloudflare)
          </span>
        </div>
      </div>

      <!-- Center Links -->
      <nav class="hidden md:flex items-center space-x-1 text-xs font-medium text-zinc-400">
        <button onclick="scrollToSection('directory')" class="px-3 py-1.5 rounded-md hover:text-white hover:bg-white/[0.04] transition">Directory</button>
        <button onclick="openStudio()" class="px-3 py-1.5 rounded-md hover:text-white hover:bg-white/[0.04] transition flex items-center gap-1.5 text-indigo-400">
          <i class="fa-solid fa-play text-[10px]"></i> Live Studio
        </button>
        <button onclick="scrollToSection('surfaces')" class="px-3 py-1.5 rounded-md hover:text-white hover:bg-white/[0.04] transition">UI Wireframes</button>
        <button onclick="scrollToSection('architecture')" class="px-3 py-1.5 rounded-md hover:text-white hover:bg-white/[0.04] transition">$0 Stack</button>
      </nav>

      <!-- Right Action -->
      <div class="flex items-center space-x-2.5">
        <a href="https://github.com/Amran-KakiTekno/omnipoint-eaas" target="_blank" class="h-8 px-3 rounded-lg border border-white/[0.08] bg-white/[0.03] hover:bg-white/[0.08] hover:border-white/[0.15] text-xs font-medium text-zinc-300 flex items-center gap-1.5 transition">
          <i class="fa-brands fa-github text-sm"></i>
          <span class="hidden sm:inline">GitHub</span>
        </a>
        <button onclick="openStudio()" class="h-8 px-3.5 rounded-lg bg-white text-black hover:bg-zinc-200 text-xs font-semibold flex items-center gap-1.5 transition shadow-sm">
          <span>Open Studio</span>
          <i class="fa-solid fa-arrow-right text-[10px]"></i>
        </button>
      </div>

    </div>
  </header>

  <!-- HERO SECTION (recent.design inspiration) -->
  <section class="relative pt-16 pb-12 overflow-hidden border-b border-white/[0.08]">
    <div class="absolute inset-0 grid-bg opacity-40 pointer-events-none"></div>
    <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-indigo-600/10 blur-[120px] rounded-full pointer-events-none"></div>

    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
      
      <!-- Eyebrow Pill -->
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/[0.04] border border-white/[0.08] text-xs text-zinc-300 mb-6 backdrop-blur-md">
        <span class="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>
        <span>55+ Deterministic Microservices</span>
        <span class="text-zinc-600">•</span>
        <span class="text-zinc-400">No Hallucinations</span>
      </div>

      <!-- Headline -->
      <h1 class="text-3xl sm:text-5xl lg:text-6xl font-extrabold text-white tracking-tight leading-[1.1] mb-5">
        Endpoint as a Service. <br/>
        <span class="bg-gradient-to-r from-zinc-200 via-zinc-400 to-zinc-600 bg-clip-text text-transparent">
          Messy in, strictly typed JSON out.
        </span>
      </h1>

      <!-- Description -->
      <p class="max-w-2xl mx-auto text-sm sm:text-base text-zinc-400 font-normal leading-relaxed mb-8">
        Single-purpose microservices built for WhatsApp bots, Google Sheets formulas, and Zapier webhooks. Decipher lab results, audit rental leases, detect elder scams, and quote trades jobs with zero prompt friction.
      </p>

      <!-- Key Metrics Strip (recent.design minimalist stats) -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-3xl mx-auto pt-2">
        <div class="p-3 rounded-xl bg-white/[0.02] border border-white/[0.06] backdrop-blur-sm">
          <div class="text-xl font-bold font-mono text-white tracking-tight">55+</div>
          <div class="text-[11px] text-zinc-500 mt-0.5">Specialized Endpoints</div>
        </div>
        <div class="p-3 rounded-xl bg-white/[0.02] border border-white/[0.06] backdrop-blur-sm">
          <div class="text-xl font-bold font-mono text-emerald-400 tracking-tight">&lt;400ms</div>
          <div class="text-[11px] text-zinc-500 mt-0.5">Edge Response Time</div>
        </div>
        <div class="p-3 rounded-xl bg-white/[0.02] border border-white/[0.06] backdrop-blur-sm">
          <div class="text-xl font-bold font-mono text-indigo-400 tracking-tight">100%</div>
          <div class="text-[11px] text-zinc-500 mt-0.5">Strict Schema Validity</div>
        </div>
        <div class="p-3 rounded-xl bg-white/[0.02] border border-white/[0.06] backdrop-blur-sm">
          <div class="text-xl font-bold font-mono text-white tracking-tight">$0.00</div>
          <div class="text-[11px] text-zinc-500 mt-0.5">Fixed Monthly Cost</div>
        </div>
      </div>

    </div>
  </section>

  <!-- DIRECTORY SECTION (skills.sh find-skills layout) -->
  <section id="directory" class="py-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full flex-1">
    
    <!-- Controls Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
      <div>
        <h2 class="text-xl font-bold text-white tracking-tight">Microservices Directory</h2>
        <p class="text-xs text-zinc-400 mt-0.5">Click any endpoint to launch the live execution studio or copy the curl snippet.</p>
      </div>

      <!-- Search Bar -->
      <div class="relative w-full md:w-80">
        <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-500 text-xs"></i>
        <input 
          type="text" 
          id="search-input" 
          onkeyup="filterCards()" 
          placeholder="Search endpoints, personas, routes..." 
          class="w-full bg-[#121215] border border-white/[0.08] hover:border-white/[0.15] focus:border-indigo-500/70 rounded-xl pl-9 pr-8 py-2 text-xs text-white placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-indigo-500/50 transition-all font-sans"
        />
        <button id="clear-search" onclick="clearSearch()" class="hidden absolute right-3 top-1/2 -translate-y-1/2 text-zinc-500 hover:text-zinc-300 text-xs">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
    </div>

    <!-- Category Filter Pills (skills.sh style) -->
    <div class="flex items-center gap-2 overflow-x-auto pb-3 mb-6 no-scrollbar text-xs font-medium">
      <button onclick="setCategory('all')" id="pill-all" class="cat-pill active-pill px-3 py-1.5 rounded-full border border-white/[0.12] bg-white text-black transition whitespace-nowrap">
        All Endpoints <span class="ml-1 text-[10px] opacity-70 font-mono">55</span>
      </button>
      <button onclick="setCategory('individuals')" id="pill-individuals" class="cat-pill px-3 py-1.5 rounded-full border border-white/[0.08] bg-[#121215] text-zinc-400 hover:text-white hover:border-white/[0.15] transition whitespace-nowrap">
        Individuals & Family <span class="ml-1 text-[10px] font-mono text-zinc-500">15</span>
      </button>
      <button onclick="setCategory('non-profits')" id="pill-non-profits" class="cat-pill px-3 py-1.5 rounded-full border border-white/[0.08] bg-[#121215] text-zinc-400 hover:text-white hover:border-white/[0.15] transition whitespace-nowrap">
        Non-Profits & NGOs <span class="ml-1 text-[10px] font-mono text-zinc-500">10</span>
      </button>
      <button onclick="setCategory('creators')" id="pill-creators" class="cat-pill px-3 py-1.5 rounded-full border border-white/[0.08] bg-[#121215] text-zinc-400 hover:text-white hover:border-white/[0.15] transition whitespace-nowrap">
        Creators & Solos <span class="ml-1 text-[10px] font-mono text-zinc-500">10</span>
      </button>
      <button onclick="setCategory('smbs')" id="pill-smbs" class="cat-pill px-3 py-1.5 rounded-full border border-white/[0.08] bg-[#121215] text-zinc-400 hover:text-white hover:border-white/[0.15] transition whitespace-nowrap">
        Local SMBs & Trades <span class="ml-1 text-[10px] font-mono text-zinc-500">10</span>
      </button>
      <button onclick="setCategory('education')" id="pill-education" class="cat-pill px-3 py-1.5 rounded-full border border-white/[0.08] bg-[#121215] text-zinc-400 hover:text-white hover:border-white/[0.15] transition whitespace-nowrap">
        Education & Civic <span class="ml-1 text-[10px] font-mono text-zinc-500">10</span>
      </button>
      <button onclick="setCategory('vision')" id="pill-vision" class="cat-pill px-3 py-1.5 rounded-full border border-white/[0.08] bg-[#121215] text-zinc-400 hover:text-white hover:border-white/[0.15] transition whitespace-nowrap flex items-center gap-1.5">
        <i class="fa-solid fa-eye text-[10px] text-purple-400"></i> Vision / OCR <span class="ml-1 text-[10px] font-mono text-zinc-500">Kimi-k3</span>
      </button>
    </div>

    <!-- Cards Grid -->
    <div id="cards-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"></div>

    <!-- Empty State -->
    <div id="empty-state" class="hidden py-16 text-center border border-dashed border-white/[0.08] rounded-2xl">
      <div class="w-10 h-10 rounded-full bg-white/[0.03] text-zinc-500 flex items-center justify-center mx-auto mb-3 text-sm">
        <i class="fa-solid fa-filter"></i>
      </div>
      <p class="text-sm font-medium text-white">No matching endpoints found</p>
      <p class="text-xs text-zinc-500 mt-1">Try refining your search keyword or clearing the category filter.</p>
      <button onclick="resetFilters()" class="mt-4 px-3 py-1.5 text-xs bg-white/[0.06] hover:bg-white/[0.1] text-zinc-300 rounded-lg transition">Reset Filters</button>
    </div>

  </section>

  <!-- WIREFRAME INTERACTIVE SURFACES SECTION (recent.design inspiration) -->
  <section id="surfaces" class="py-16 border-t border-white/[0.08] bg-[#0c0c0e]/60">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="max-w-2xl mb-10">
        <span class="text-[11px] font-mono uppercase tracking-wider text-indigo-400 font-semibold">User Experience Wireframes</span>
        <h2 class="text-2xl sm:text-3xl font-bold text-white tracking-tight mt-1">Four Native Surfaces for Non-Developers</h2>
        <p class="text-xs sm:text-sm text-zinc-400 mt-2">
          End users don't run cURL scripts. Here is how these endpoints manifest inside the real everyday interfaces they already use.
        </p>
      </div>

      <!-- Tabs for Surface Mockups -->
      <div class="flex space-x-2 border-b border-white/[0.08] mb-8 text-xs font-medium">
        <button onclick="switchSurface('whatsapp')" id="surface-btn-whatsapp" class="pb-3 text-white border-b-2 border-indigo-500 font-semibold px-2 transition">
          <i class="fa-brands fa-whatsapp text-emerald-400 mr-1.5"></i> 1. WhatsApp & SMS Bot
        </button>
        <button onclick="switchSurface('sheets')" id="surface-btn-sheets" class="pb-3 text-zinc-400 hover:text-white px-2 transition">
          <i class="fa-solid fa-table text-emerald-500 mr-1.5"></i> 2. Google Sheets Formula
        </button>
        <button onclick="switchSurface('zapier')" id="surface-btn-zapier" class="pb-3 text-zinc-400 hover:text-white px-2 transition">
          <i class="fa-solid fa-diagram-project text-orange-400 mr-1.5"></i> 3. Zapier / Make Pipeline
        </button>
      </div>

      <!-- SURFACE 1: WHATSAPP PHONE SIMULATOR -->
      <div id="surface-whatsapp" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        <!-- Phone Device Frame -->
        <div class="lg:col-span-5 flex justify-center">
          <div class="w-full max-w-[320px] bg-[#020408] border-4 border-zinc-800 rounded-[40px] p-3 shadow-2xl relative">
            <div class="w-20 h-4 bg-zinc-800 rounded-full mx-auto mb-3"></div>
            <!-- Chat Header -->
            <div class="flex items-center gap-2.5 pb-2.5 border-b border-zinc-800/80">
              <div class="w-7 h-7 rounded-full bg-emerald-600 flex items-center justify-center text-[10px] text-white font-bold">
                <i class="fa-solid fa-shield-halved"></i>
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-xs font-bold text-white truncate">Smart Family Shield</div>
                <div class="text-[9px] text-emerald-400 flex items-center gap-1">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> Verified Assistant
                </div>
              </div>
            </div>

            <!-- Messages Stream -->
            <div class="py-3 space-y-2.5 text-[11px] min-h-[300px] flex flex-col justify-end" id="chat-stream">
              <div class="bg-zinc-800/90 text-zinc-300 p-2.5 rounded-2xl rounded-tl-none max-w-[85%] text-[10px] leading-relaxed">
                Hi! Forward any suspicious SMS, blood test photo, or mechanic bill here.
              </div>
              <div class="bg-indigo-600 text-white p-2.5 rounded-2xl rounded-tr-none ml-auto max-w-[85%] text-[10px] leading-relaxed">
                <div class="bg-black/30 p-1 rounded mb-1 text-[9px] flex items-center gap-1">
                  <i class="fa-solid fa-image"></i> [SMS: "Chase fraud alert: Account frozen. Click chase-verify82.com"]
                </div>
                Is this real? I was scared to click.
              </div>
              <div class="bg-emerald-950/70 border border-emerald-500/30 p-2.5 rounded-2xl rounded-tl-none text-[10px] text-zinc-200 space-y-1">
                <div class="font-bold text-red-400 flex items-center gap-1">
                  <i class="fa-solid fa-triangle-exclamation"></i> 99% SCAM CONFIRMED
                </div>
                <p class="text-zinc-300 text-[9.5px]">This is an urgency phishing trap trying to steal your card PIN.</p>
                <div class="bg-black/40 p-1.5 rounded text-[9px] space-y-0.5 text-zinc-300">
                  <p class="text-emerald-400 font-semibold">Steps to take:</p>
                  <p>1. Do not tap the link.</p>
                  <p>2. Delete the message.</p>
                  <p>3. Your account is completely safe.</p>
                </div>
              </div>
            </div>

            <!-- Bottom Input Mock -->
            <div class="pt-2 border-t border-zinc-800 flex items-center gap-2">
              <div class="flex-1 bg-zinc-900 text-zinc-500 text-[10px] py-1.5 px-3 rounded-full">Send photo or voice...</div>
              <div class="w-6 h-6 rounded-full bg-emerald-600 flex items-center justify-center text-white text-[10px]">
                <i class="fa-solid fa-paper-plane"></i>
              </div>
            </div>
          </div>
        </div>

        <!-- Explanatory Details -->
        <div class="lg:col-span-7 space-y-4">
          <div class="inline-flex items-center gap-1.5 text-xs font-mono text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-md border border-emerald-500/20">
            <span>Powered by:</span> <code>POST /v1/safety/scam-detector</code>
          </div>
          <h3 class="text-xl font-bold text-white tracking-tight">Zero Learning Curve for Elderly Parents & Families</h3>
          <p class="text-xs sm:text-sm text-zinc-400 leading-relaxed">
            By connecting the Cloudflare Worker to the Twilio / WhatsApp Cloud API, users never see an API key, JSON, or code. They simply forward a photo or voice note and receive compassionate, actionable protection within 1.2 seconds.
          </p>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
            <div class="p-3.5 rounded-xl bg-[#121215] border border-white/[0.08]">
              <div class="text-xs font-semibold text-white mb-1">Interactive Simulation</div>
              <div class="flex flex-wrap gap-1.5 text-[10px]">
                <button onclick="setSimScenario('scam')" class="px-2 py-1 rounded bg-zinc-800 text-zinc-300 hover:text-white">Scam Alert</button>
                <button onclick="setSimScenario('lab')" class="px-2 py-1 rounded bg-zinc-800 text-zinc-300 hover:text-white">Blood Test</button>
                <button onclick="setSimScenario('lease')" class="px-2 py-1 rounded bg-zinc-800 text-zinc-300 hover:text-white">Lease Clause</button>
              </div>
            </div>
            <div class="p-3.5 rounded-xl bg-[#121215] border border-white/[0.08]">
              <div class="text-xs font-semibold text-white mb-1">Monetization</div>
              <p class="text-[11px] text-zinc-400">\$4.99/mo subscription for up to 4 family members with unlimited audits.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- SURFACE 2: GOOGLE SHEETS SIMULATOR -->
      <div id="surface-sheets" class="hidden space-y-6">
        <div class="p-5 rounded-2xl bg-[#121215] border border-white/[0.08]">
          <div class="flex items-center justify-between pb-3 mb-4 border-b border-white/[0.08] text-xs font-mono">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold">fx</span>
              <span class="text-indigo-400">=AI_GRANT_MATCH(A2, B2)</span>
            </div>
            <span class="text-zinc-500">Google Apps Script Connector</span>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-xs font-mono text-left">
              <thead class="bg-zinc-900 text-zinc-400 border-b border-zinc-800">
                <tr>
                  <th class="p-2.5 w-12 text-center text-zinc-500">#</th>
                  <th class="p-2.5 w-1/3">A (Foundation RFP)</th>
                  <th class="p-2.5 w-1/3">B (Eligibility Criteria)</th>
                  <th class="p-2.5 text-indigo-400">C (=AI_GRANT_MATCH)</th>
                  <th class="p-2.5 text-emerald-400">Action Status</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-zinc-800/80 bg-zinc-950/40 text-[11px]">
                <tr>
                  <td class="p-2.5 text-center text-zinc-600">2</td>
                  <td class="p-2.5 text-zinc-200">Gates STEM Education Initiative</td>
                  <td class="p-2.5 text-zinc-400 truncate max-w-xs">Requires 501(c)(3), Title I school focus, 3yr operating history...</td>
                  <td class="p-2.5 text-emerald-400 font-semibold">92% Match (Eligible)</td>
                  <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Draft Stage 1 LOI</span></td>
                </tr>
                <tr>
                  <td class="p-2.5 text-center text-zinc-600">3</td>
                  <td class="p-2.5 text-zinc-200">Clean Water Infrastructure Fund</td>
                  <td class="p-2.5 text-zinc-400 truncate max-w-xs">Municipalities & universities only. Non-profit entities excluded under Sec 4...</td>
                  <td class="p-2.5 text-red-400 font-semibold">0% Match (Disqualified)</td>
                  <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] bg-red-500/10 text-red-400 border border-red-500/20">Skip / Reject</span></td>
                </tr>
                <tr>
                  <td class="p-2.5 text-center text-zinc-600">4</td>
                  <td class="p-2.5 text-zinc-200">Youth Arts & Community Literacy</td>
                  <td class="p-2.5 text-zinc-400 truncate max-w-xs">Budget must be below \$250,000; requires 1:1 matching cash grant...</td>
                  <td class="p-2.5 text-amber-400 font-semibold">65% Match (Review Match)</td>
                  <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20">Verify Cash Match</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- SURFACE 3: ZAPIER / MAKE AUTOMATION PIPELINE -->
      <div id="surface-zapier" class="hidden space-y-6">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs font-mono">
          <div class="p-4 rounded-xl bg-[#121215] border border-white/[0.08] relative">
            <span class="text-[10px] text-zinc-500 font-bold uppercase block mb-1">Step 1 • Trigger</span>
            <div class="text-sm font-bold text-white flex items-center gap-2 mb-2">
              <i class="fa-brands fa-google text-red-400"></i> New 1-Star Review
            </div>
            <p class="text-zinc-400 text-[11px] font-sans">Customer posts complaint on Google Business Profile regarding cold pizza.</p>
          </div>

          <div class="p-4 rounded-xl bg-indigo-950/40 border border-indigo-500/50 shadow-lg shadow-indigo-500/10 relative">
            <span class="text-[10px] text-indigo-400 font-bold uppercase block mb-1">Step 2 • Smart EaaS</span>
            <div class="text-sm font-bold text-white flex items-center gap-2 mb-2">
              <i class="fa-solid fa-bolt text-indigo-400"></i> /v1/smb/review-reply
            </div>
            <p class="text-zinc-300 text-[11px] font-sans">DeepSeek analyzes sentiment, validates policy, and drafts empathetic public reply.</p>
          </div>

          <div class="p-4 rounded-xl bg-[#121215] border border-white/[0.08] relative">
            <span class="text-[10px] text-zinc-500 font-bold uppercase block mb-1">Step 3 • Gate</span>
            <div class="text-sm font-bold text-white flex items-center gap-2 mb-2">
              <i class="fa-brands fa-slack text-purple-400"></i> Slack Approval
            </div>
            <p class="text-zinc-400 text-[11px] font-sans">Manager receives push notification on mobile: "Tap to approve reply".</p>
          </div>

          <div class="p-4 rounded-xl bg-[#121215] border border-white/[0.08] relative">
            <span class="text-[10px] text-zinc-500 font-bold uppercase block mb-1">Step 4 • Action</span>
            <div class="text-sm font-bold text-white flex items-center gap-2 mb-2">
              <i class="fa-solid fa-reply text-emerald-400"></i> Auto-Published
            </div>
            <p class="text-zinc-400 text-[11px] font-sans">Approved response posted directly to Google Maps; incident logged to Airtable.</p>
          </div>
        </div>
      </div>

    </div>
  </section>

  <!-- ZERO COST ARCHITECTURE BREAKDOWN -->
  <section id="architecture" class="py-16 border-t border-white/[0.08] max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="max-w-2xl mb-10">
      <span class="text-[11px] font-mono uppercase tracking-wider text-indigo-400 font-semibold">Infrastructure</span>
      <h2 class="text-2xl sm:text-3xl font-bold text-white tracking-tight mt-1">Zero-Cost Global Edge Architecture</h2>
      <p class="text-xs sm:text-sm text-zinc-400 mt-2">
        How this entire platform runs at \$0.00 fixed monthly cost using your Cloudflare and GitHub setup.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="p-5 rounded-2xl bg-[#121215] border border-white/[0.08] space-y-3">
        <div class="w-8 h-8 rounded-lg bg-orange-500/10 text-orange-400 flex items-center justify-center text-sm">
          <i class="fa-solid fa-bolt"></i>
        </div>
        <h3 class="text-sm font-bold text-white">Cloudflare Workers</h3>
        <p class="text-xs text-zinc-400 leading-relaxed">
          Stateless edge functions running globally in 300+ cities. Handles routing, Pydantic/JSON validation, and upstream model failover.
        </p>
        <div class="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded border border-emerald-500/20">
          100,000 free requests/day • \$0/mo
        </div>
      </div>

      <div class="p-5 rounded-2xl bg-[#121215] border border-white/[0.08] space-y-3">
        <div class="w-8 h-8 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center text-sm">
          <i class="fa-solid fa-database"></i>
        </div>
        <h3 class="text-sm font-bold text-white">Cloudflare R2 Storage</h3>
        <p class="text-xs text-zinc-400 leading-relaxed">
          S3-compatible bucket used for temporary file payloads (multi-page PDF lease agreements, raw audio clips, receipt photos).
        </p>
        <div class="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded border border-emerald-500/20">
          10 GB free storage • Zero egress fees
        </div>
      </div>

      <div class="p-5 rounded-2xl bg-[#121215] border border-white/[0.08] space-y-3">
        <div class="w-8 h-8 rounded-lg bg-purple-500/10 text-purple-400 flex items-center justify-center text-sm">
          <i class="fa-brands fa-github"></i>
        </div>
        <h3 class="text-sm font-bold text-white">GitHub CI/CD Deployment</h3>
        <p class="text-xs text-zinc-400 leading-relaxed">
          Automated edge pipeline. Any push to <code>main</code> triggers Wrangler deployments directly to both Workers and Pages.
        </p>
        <div class="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded border border-emerald-500/20">
          2,000 free runner minutes/mo
        </div>
      </div>
    </div>
  </section>

  <!-- ==================== STUDIO DRAWER / MODAL (skills.sh workbench inspired) ==================== -->
  <div id="studio-drawer" class="fixed inset-0 z-50 hidden">
    <!-- Backdrop -->
    <div onclick="closeStudio()" class="absolute inset-0 bg-black/80 backdrop-blur-sm transition-opacity"></div>

    <!-- Panel -->
    <div class="absolute right-0 top-0 bottom-0 w-full max-w-4xl bg-[#0c0c0e] border-l border-white/[0.1] shadow-2xl flex flex-col z-10">
      
      <!-- Studio Header -->
      <div class="h-14 px-5 border-b border-white/[0.08] flex items-center justify-between bg-[#121215]/80 backdrop-blur-md">
        <div class="flex items-center space-x-2.5">
          <span class="w-2.5 h-2.5 rounded-full bg-indigo-500"></span>
          <span class="text-xs font-bold text-white uppercase tracking-wider">Live Execution Studio</span>
          <span class="text-zinc-600">|</span>
          <span id="studio-route-pill" class="text-xs font-mono text-indigo-400 font-semibold">/v1/health/explain-lab</span>
        </div>
        
        <div class="flex items-center space-x-2">
          <button onclick="closeStudio()" class="w-8 h-8 rounded-lg bg-white/[0.04] hover:bg-white/[0.08] text-zinc-400 hover:text-white flex items-center justify-center text-xs transition">
            <i class="fa-solid fa-xmark text-sm"></i>
          </button>
        </div>
      </div>

      <!-- Studio Body (Split view) -->
      <div class="flex-1 grid grid-cols-1 lg:grid-cols-12 overflow-hidden">
        
        <!-- LEFT: INPUT & CONFIG -->
        <div class="lg:col-span-6 p-5 border-b lg:border-b-0 lg:border-r border-white/[0.08] flex flex-col space-y-4 overflow-y-auto">
          
          <!-- Select Endpoint -->
          <div class="space-y-1.5">
            <label class="text-[11px] font-semibold text-zinc-300 uppercase tracking-wider">Target Microservice</label>
            <select id="studio-endpoint-select" onchange="onStudioEndpointChange()" class="w-full bg-[#16161a] border border-white/[0.08] text-white rounded-lg p-2.5 text-xs focus:ring-1 focus:ring-indigo-500 focus:outline-none">
              <option value="explain-lab">#1 Medical Lab Explainer (/v1/health/explain-lab)</option>
              <option value="lease-check">#2 Lease Red-Flag Auditor (/v1/legal/lease-check)</option>
              <option value="scam-detector">#3 Elder Scam Defender (/v1/safety/scam-detector)</option>
              <option value="review-reply">#36 Google Review De-escalator (/v1/smb/review-reply)</option>
              <option value="grant-match">#16 Grant Criteria Matcher (/v1/ngo/grant-match)</option>
              <option value="scope-defense">#27 Scope Creep Defense (/v1/freelance/scope-defense)</option>
              <option value="differentiate">#46 Differentiated Homework (/v1/edu/differentiate)</option>
              <option value="invoice-extract">#0 Universal Invoice to JSON (/v1/extract/invoice)</option>
            </select>
          </div>

          <!-- Select Model -->
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
          </div>

          <!-- Input Box -->
          <div class="flex-1 flex flex-col space-y-1.5 min-h-[220px]">
            <div class="flex justify-between items-center text-[11px]">
              <label class="font-semibold text-zinc-300 uppercase tracking-wider">Raw Input Payload</label>
              <button onclick="resetStudioSample()" class="text-[10px] text-indigo-400 hover:text-indigo-300 flex items-center gap-1">
                <i class="fa-solid fa-rotate-left"></i> Reload Preset
              </button>
            </div>
            <textarea id="studio-input" class="flex-1 w-full bg-[#16161a] border border-white/[0.08] rounded-lg p-3 text-xs font-mono text-zinc-200 focus:ring-1 focus:ring-indigo-500 focus:outline-none resize-none leading-relaxed" placeholder="Enter messy input text..."></textarea>
          </div>

          <!-- Execute Button -->
          <button id="studio-run-btn" onclick="runStudioExecution()" class="w-full py-2.5 px-4 bg-white text-black hover:bg-zinc-200 font-semibold rounded-lg text-xs transition flex items-center justify-center gap-2 shadow-sm">
            <i class="fa-solid fa-play text-[10px]"></i>
            <span>Execute Live Endpoint</span>
          </button>
        </div>

        <!-- RIGHT: RESULTS & INTEGRATION CODE -->
        <div class="lg:col-span-6 p-5 flex flex-col space-y-4 bg-[#09090b] overflow-hidden">
          
          <!-- Tabs: JSON Result vs cURL vs Zapier -->
          <div class="flex items-center justify-between border-b border-white/[0.08] pb-2 text-xs">
            <div class="flex space-x-2">
              <button onclick="switchOutputTab('json')" id="tab-out-json" class="font-semibold text-white border-b-2 border-indigo-500 pb-2 px-1">JSON Output</button>
              <button onclick="switchOutputTab('curl')" id="tab-out-curl" class="text-zinc-400 hover:text-white pb-2 px-1">cURL</button>
              <button onclick="switchOutputTab('zapier')" id="tab-out-zapier" class="text-zinc-400 hover:text-white pb-2 px-1">Zapier / Make</button>
            </div>

            <div class="flex items-center gap-2">
              <span id="studio-latency" class="hidden text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-800 text-zinc-300 border border-zinc-700">0ms</span>
              <button onclick="copyStudioOutput()" class="text-zinc-400 hover:text-white text-xs px-2 py-1 rounded bg-white/[0.04] hover:bg-white/[0.08] transition">
                <i class="fa-regular fa-copy"></i>
              </button>
            </div>
          </div>

          <!-- View 1: JSON Output -->
          <div id="view-out-json" class="flex-1 flex flex-col overflow-hidden relative">
            <div id="studio-loader" class="hidden absolute inset-0 bg-[#09090b]/90 backdrop-blur-sm flex flex-col items-center justify-center z-10">
              <div class="w-6 h-6 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin mb-2"></div>
              <p class="text-xs font-semibold text-white">Running on Edge...</p>
              <p class="text-[10px] text-zinc-500">Calling rootsys.cloud with strict schema</p>
            </div>
            <pre id="studio-json-pre" class="flex-1 p-3.5 bg-[#0e0e11] border border-white/[0.06] rounded-lg text-xs font-mono text-emerald-400 overflow-auto whitespace-pre-wrap select-all leading-relaxed">
// Click "Execute Live Endpoint" to test.
// Guaranteed strictly typed JSON response will appear here.
            </pre>
          </div>

          <!-- View 2: cURL snippet -->
          <div id="view-out-curl" class="hidden flex-1 flex flex-col overflow-hidden">
            <pre id="studio-curl-pre" class="flex-1 p-3.5 bg-[#0e0e11] border border-white/[0.06] rounded-lg text-xs font-mono text-indigo-300 overflow-auto whitespace-pre-wrap select-all leading-relaxed"></pre>
          </div>

          <!-- View 3: Zapier Guide -->
          <div id="view-out-zapier" class="hidden flex-1 overflow-auto p-3.5 bg-[#0e0e11] border border-white/[0.06] rounded-lg text-xs text-zinc-300 space-y-2">
            <p class="font-bold text-white">How to connect to Zapier / Make.com in 60 seconds:</p>
            <ol class="list-decimal list-inside space-y-1 text-zinc-400 text-[11px]">
              <li>Add a <strong>"Webhooks by Zapier"</strong> action in your Zap.</li>
              <li>Choose <strong>"Custom Request"</strong> with method <code>POST</code>.</li>
              <li>Set URL to <code class="text-indigo-400" id="zapier-url">https://smart-eaas.muhammadamran40.workers.dev/...</code></li>
              <li>Set Data to <code>{{"input": "..."}}</code> mapping your trigger fields.</li>
              <li>Zapier automatically maps each returned JSON field into following actions!</li>
            </ol>
          </div>

        </div>

      </div>

    </div>
  </div>

  <!-- FOOTER -->
  <footer class="border-t border-white/[0.08] py-8 bg-[#09090b] text-center text-xs text-zinc-500">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div class="flex items-center space-x-2">
        <span class="font-bold text-white">Smart EaaS</span>
        <span>•</span>
        <span>Deterministic AI Microservices</span>
      </div>
      <div class="flex items-center space-x-4 text-zinc-400">
        <a href="https://smart-eaas.pages.dev" class="hover:text-white transition">smart-eaas.pages.dev</a>
        <a href="https://github.com/Amran-KakiTekno/omnipoint-eaas" target="_blank" class="hover:text-white transition">GitHub Source</a>
        <a href="/api/health" target="_blank" class="hover:text-white transition">Edge Health</a>
      </div>
    </div>
  </footer>

  <!-- CORE CLIENT-SIDE SCRIPT -->
  <script>
    const ENDPOINT_CONFIGS = {prompts_json};

    // Full 55+ endpoint catalog data
    const ALL_ENDPOINTS = [
      {{ id: 1, route: "/v1/health/explain-lab", cat: "individuals", title: "Medical Lab Report Explainer", persona: "Patient / Caregiver", desc: "Translates cryptic blood panels and metabolic tests into plain language with out-of-range highlights and doctor questions.", key: "explain-lab", tags: ["Health", "Safe"] }},
      {{ id: 2, route: "/v1/legal/lease-check", cat: "individuals", title: "Apartment Lease Red-Flag Auditor", persona: "Tenant / Student", desc: "Detects exploitative repair clauses, illegal entry rights, and hidden deposit deduction traps in rental contracts.", key: "lease-check", tags: ["Legal", "Tenant"] }},
      {{ id: 3, route: "/v1/safety/scam-detector", cat: "individuals", title: "Elder Scam & Phishing Defender", persona: "Senior / Family", desc: "Analyzes suspicious texts, fake bank warnings, and urgency phishing with reassurance and safe next steps.", key: "scam-detector", tags: ["Security", "Family"] }},
      {{ id: 4, route: "/v1/auto/quote-verifier", cat: "individuals", title: "Car Mechanic Quote Sanity Checker", persona: "Car Owner", desc: "Cross-checks repair estimates against market labor rates and flags unnecessary upsells vs critical safety fixes.", key: "explain-lab", tags: ["Auto", "Consumer"] }},
      {{ id: 5, route: "/v1/finance/fee-audit", cat: "individuals", title: "Subscription & Hidden Fee Hunter", persona: "Budgeter", desc: "Audits bank and card statements to flag stealth price increases, forgotten SaaS, and one-click cancel links.", key: "explain-lab", tags: ["Finance"] }},
      {{ id: 6, route: "/v1/diet/ingredient-alert", cat: "individuals", title: "Allergen & Additive Scanner", persona: "Allergy Sufferer", desc: "Deciphers food ingredient photos to flag hidden dairy derivatives, gluten, and dangerous E-numbers.", key: "explain-lab", tags: ["Health", "Vision"] }},
      {{ id: 7, route: "/v1/legal/ticket-appeal", cat: "individuals", title: "Parking Ticket & Tow Appeal Drafter", persona: "Urban Driver", desc: "Drafts formal municipal appeals citing signage ambiguities, curb markings, and local traffic codes.", key: "explain-lab", tags: ["Legal"] }},
      {{ id: 8, route: "/v1/insurance/appeal-generator", cat: "individuals", title: "Insurance Claim Denial Fighter", persona: "Homeowner / Patient", desc: "Generates structured rebuttal letters citing policy declaration clauses and statutory prompt-pay rules.", key: "explain-lab", tags: ["Insurance"] }},
      {{ id: 9, route: "/v1/edu/iep-analyzer", cat: "individuals", title: "Special-Ed IEP Document Decoder", persona: "Parent of Neurodivergent Child", desc: "Translates 40-page school IEPs into clear checklists, missing accommodations, and legal IDEA rights.", key: "explain-lab", tags: ["Education"] }},
      {{ id: 10, route: "/v1/food/fridge-inventory", cat: "individuals", title: "Zero-Waste Fridge-to-Meal Chef", persona: "Busy Parent", desc: "Turns a photo of your fridge interior into 3 exact meals utilizing only expiring perishables.", key: "explain-lab", tags: ["Vision", "Food"] }},
      {{ id: 11, route: "/v1/home/appliance-fix", cat: "individuals", title: "Appliance Error Code Decryptor", persona: "Homeowner", desc: "Decodes flashing dishwasher/boiler error codes, rating DIY repair feasibility and replacement part numbers.", key: "explain-lab", tags: ["DIY"] }},
      {{ id: 12, route: "/v1/energy/bill-optimizer", cat: "individuals", title: "Utility Tariff Optimizer", persona: "Household Manager", desc: "Audits electric bill usage against alternative time-of-use tariffs to calculate annual shifting savings.", key: "explain-lab", tags: ["Energy"] }},
      {{ id: 13, route: "/v1/career/transition-map", cat: "individuals", title: "Career Switcher Skill Crosswalk", persona: "Laid-Off Worker", desc: "Maps legacy job experience into modern tech & green economy roles with tailored resume narratives.", key: "explain-lab", tags: ["Career"] }},
      {{ id: 14, route: "/v1/parenting/coaching", cat: "individuals", title: "Child Behavioral De-escalator", persona: "Stressed Parent", desc: "Provides gentle, developmentally attuned verbal scripts during high-stress toddler tantrums or teen defiance.", key: "explain-lab", tags: ["Parenting"] }},
      {{ id: 15, route: "/v1/consumer/warranty-claim", cat: "individuals", title: "Statutory Warranty Dispute Writer", persona: "Online Shopper", desc: "Drafts formal demand letters invoking statutory implied warranties (Magnuson-Moss / EU Directives).", key: "explain-lab", tags: ["Consumer"] }},

      // Category 2: Non-Profits
      {{ id: 16, route: "/v1/ngo/grant-match", cat: "non-profits", title: "Grant RFP Criteria Matcher", persona: "Grant Writer", desc: "Evaluates 50-page foundation RFPs against NGO missions, calculating eligibility match % and disqualifiers.", key: "grant-match", tags: ["Grants", "NPO"] }},
      {{ id: 17, route: "/v1/ngo/donor-story", cat: "non-profits", title: "Raw Field Impact-to-Story Engine", persona: "Fundraiser", desc: "Converts messy field notes into emotional donor newsletters, impact metrics, and thank-you cards.", key: "grant-match", tags: ["Donors"] }},
      {{ id: 18, route: "/v1/ngo/990-explainer", cat: "non-profits", title: "Form 990 Non-Profit Tax Simplifier", persona: "Board Trustee", desc: "Simplifies complex annual Form 990 filings into program-expense ratios, liquidity reserves, and audits.", key: "grant-match", tags: ["Finance"] }},
      {{ id: 19, route: "/v1/ngo/volunteer-dispatch", cat: "non-profits", title: "Volunteer Skill Matcher & Dispatcher", persona: "Volunteer Coordinator", desc: "Triages volunteer questionnaire skills to urgent operational shifts with automated SMS onboarding.", key: "grant-match", tags: ["Volunteers"] }},
      {{ id: 20, route: "/v1/ngo/localize-notice", cat: "non-profits", title: "Community Flyer Cultural Localizer", persona: "Organizer", desc: "Adapts announcements into Spanish, Arabic, or Vietnamese preserving cultural idioms and reading levels.", key: "grant-match", tags: ["Community"] }},
      {{ id: 21, route: "/v1/crisis/sos-triage", cat: "non-profits", title: "Disaster Crisis SOS Triage", persona: "Emergency Response", desc: "Extracts GPS, urgency scores (1-5), and required medical/rescue gear from incoming crisis texts.", key: "grant-match", tags: ["Emergency"] }},
      {{ id: 22, route: "/v1/ngo/donor-letter", cat: "non-profits", title: "Major Donor Stewardship Drafter", persona: "Development Director", desc: "Crafts bespoke cultivation letters referencing past personal gifts and tangible program outcomes.", key: "grant-match", tags: ["Fundraising"] }},
      {{ id: 23, route: "/v1/ngo/foodbank-recipes", cat: "non-profits", title: "Pantry Surplus Recipe Creator", persona: "Food Pantry Lead", desc: "Generates no-oven recipe cards for odd surplus donations (lentils, squash) to include in food boxes.", key: "grant-match", tags: ["Food"] }},
      {{ id: 24, route: "/v1/ngo/policy-impact", cat: "non-profits", title: "Legislative Bill Impact Digest", persona: "Advocacy Director", desc: "Section-by-section breakdown of state omnibus bills highlighting community threats and testimony points.", key: "grant-match", tags: ["Policy"] }},
      {{ id: 25, route: "/v1/ngo/budget-narrative", cat: "non-profits", title: "Grant Budget Narrative Writer", persona: "Program Manager", desc: "Writes comprehensive, audit-ready narrative justifications for every mathematical row in a budget.", key: "grant-match", tags: ["Grants"] }},

      // Category 3: Creators & Solopreneurs
      {{ id: 26, route: "/v1/creator/repurpose", cat: "creators", title: "Long-Form to Multi-Platform Repurposer", persona: "YouTuber / Podcaster", desc: "Turns 1 video transcript into 1 X thread, 3 LinkedIn posts, 5 TikTok hooks, and 1 email newsletter.", key: "scope-defense", tags: ["Content", "Social"] }},
      {{ id: 27, route: "/v1/freelance/scope-defense", cat: "creators", title: "Client Scope Creep Defense Assistant", persona: "Freelancer / Designer", desc: "Identifies scope breaches, drafting diplomatic boundary-holding emails with paid change orders.", key: "scope-defense", tags: ["Freelance", "Contracts"] }},
      {{ id: 28, route: "/v1/audio/shownotes", cat: "creators", title: "Podcast Show Notes & Timestamps", persona: "Audio Producer", desc: "Generates clickable chapter timestamps, guest bios, key discussion points, and quote summaries.", key: "scope-defense", tags: ["Audio"] }},
      {{ id: 29, route: "/v1/creator/pitch-brand", cat: "creators", title: "Sponsorship Pitch & Rate Matrix", persona: "Micro-Creator", desc: "Formulates brand outreach emails with CPM-benchmarked pricing quotes based on view analytics.", key: "scope-defense", tags: ["Sponsors"] }},
      {{ id: 30, route: "/v1/design/audit-portfolio", cat: "creators", title: "Portfolio First-Impression Audit", persona: "Junior Designer", desc: "Provides a 5-second visual clarity audit, UX friction points, and recruiter readability scoring.", key: "scope-defense", tags: ["Design"] }},
      {{ id: 31, route: "/v1/marketing/objection-handler", cat: "creators", title: "Landing Page Objection Buster", persona: "Indie Founder", desc: "Extracts top 10 hidden buyer hesitation fears from draft sales copy and writes punchy FAQ rebuttals.", key: "scope-defense", tags: ["Marketing"] }},
      {{ id: 32, route: "/v1/youtube/thumbnail-concepts", cat: "creators", title: "YouTube Thumbnail & Title Angle Engine", persona: "Video Creator", desc: "Generates 3 psychological framing angles (curiosity, contrarian, mistake) with thumbnail sketch prompts.", key: "scope-defense", tags: ["YouTube"] }},
      {{ id: 33, route: "/v1/freelance/lead-qualifier", cat: "creators", title: "Inbound Client Lead Qualifier", persona: "Agency Owner", desc: "Assesses prospective client inquiries for budget viability, project clarity, and red-flag traps.", key: "scope-defense", tags: ["Leads"] }},
      {{ id: 34, route: "/v1/audio/clean-transcript", cat: "creators", title: "Audio Filler Word & Glitch Cleaner", persona: "Audio Editor", desc: "Generates automated timecoded cut-lists for 'um', 'ah', mouth clicks, and repeated hesitations.", key: "scope-defense", tags: ["Audio"] }},
      {{ id: 35, route: "/v1/video/tone-subtitles", cat: "creators", title: "Nuanced Subtitle Slang Adapter", persona: "Global Creator", desc: "Localizes video subtitles preserving conversational internet slang, humor, and timing.", key: "scope-defense", tags: ["Video"] }},

      // Category 4: Small Business & Trades
      {{ id: 36, route: "/v1/smb/review-reply", cat: "smbs", title: "Google Business Review De-escalator", persona: "Bistro / Clinic Owner", desc: "Drafts empathetic public responses that validate customer frustration, prevent PR damage, and move dialogue offline.", key: "review-reply", tags: ["Reputation", "SMB"] }},
      {{ id: 37, route: "/v1/restaurant/menu-digitizer", cat: "smbs", title: "Menu Allergen & Digitize Engine", persona: "Cafe Owner", desc: "Converts smartphone photos of paper menus into structured JSON with allergen badges and translations.", key: "review-reply", tags: ["Restaurant", "Vision"] }},
      {{ id: 38, route: "/v1/salon/fill-slot", cat: "smbs", title: "Last-Minute Cancellation Slot Filler", persona: "Salon / Clinic", desc: "Matches sudden cancelled slots against client waitlists, drafting personalized 1-click SMS offers.", key: "review-reply", tags: ["Booking"] }},
      {{ id: 39, route: "/v1/trades/quote-builder", cat: "smbs", title: "Voice-to-Trades Job Estimate", persona: "Plumber / Electrician", desc: "Translates voice memos recorded in work trucks into itemized estimates with parts markup and terms.", key: "review-reply", tags: ["Trades", "Audio"] }},
      {{ id: 40, route: "/v1/smb/local-seo", cat: "smbs", title: "Local Search SEO Optimizer", persona: "Contractor", desc: "Generates geo-targeted Google Business Profile updates targeting voice search ('plumber near me').", key: "review-reply", tags: ["SEO"] }},
      {{ id: 41, route: "/v1/retail/vendor-slip", cat: "smbs", title: "Supplier Slip to POS Normalizer", persona: "Boutique Grocer", desc: "Scans wrinkled paper wholesale delivery slips into clean inventory imports with SKUs and unit costs.", key: "review-reply", tags: ["Retail", "Vision"] }},
      {{ id: 42, route: "/v1/retail/shift-swap", cat: "smbs", title: "Employee Shift Swap Arbiter", persona: "Store Manager", desc: "Verifies shift swap requests against weekly overtime thresholds, certifications, and labor laws.", key: "review-reply", tags: ["Staff"] }},
      {{ id: 43, route: "/v1/repair/status-update", cat: "smbs", title: "Repair Status Customer Bot", persona: "Repair Workshop", desc: "Converts cryptic internal technician bench notes into friendly, reassuring customer SMS updates.", key: "review-reply", tags: ["Service"] }},
      {{ id: 44, route: "/v1/smb/lease-cam-check", cat: "smbs", title: "Commercial Lease CAM Auditor", persona: "Storefront Tenant", desc: "Scans annual Common Area Maintenance bills to detect unauthorized landlord management surcharges.", key: "review-reply", tags: ["Lease"] }},
      {{ id: 45, route: "/v1/trades/maintenance-log", cat: "smbs", title: "Equipment Maintenance Voice Logger", persona: "Bakery / Brewery", desc: "Logs machinery noise and service voice notes, calculating predicted component wear and service dates.", key: "review-reply", tags: ["Machinery"] }},

      // Category 5: Education & Public Service
      {{ id: 46, route: "/v1/edu/differentiate", cat: "education", title: "Differentiated Homework Generator", persona: "School Teacher", desc: "Creates 3 tiered assignments (Tier 1 Remedial/ESL, Tier 2 Grade Mastery, Tier 3 Extension) from one lesson.", key: "differentiate", tags: ["Teaching", "Edu"] }},
      {{ id: 47, route: "/v1/edu/rubric-feedback", cat: "education", title: "Student Rubric Feedback Drafter", persona: "High School Teacher", desc: "Generates constructive feedback for student essays highlighting 2 strengths and 2 concrete revision steps.", key: "differentiate", tags: ["Grading"] }},
      {{ id: 48, route: "/v1/social/casenotes", cat: "education", title: "Objective Social Work Case Note Distiller", persona: "Caseworker", desc: "Converts rambling home-visit voice notes into legally objective, court-compliant case files.", key: "differentiate", tags: ["Social Work"] }},
      {{ id: 49, route: "/v1/civic/council-digest", cat: "education", title: "City Council & Zoning Digest", persona: "Civic Organizer", desc: "Distills 3-hour municipal council broadcasts into 5 key votes impacting zoning, taxes, and road spending.", key: "differentiate", tags: ["Civic"] }},
      {{ id: 50, route: "/v1/med/soap-note", cat: "education", title: "Clinical SOAP Note from Ambient Audio", persona: "Physician / Therapist", desc: "Formats ambient doctor-patient encounter audio into structured medical SOAP notes with ICD-10 codes.", key: "differentiate", tags: ["Medical"] }},
      {{ id: 51, route: "/v1/edu/homeschool-plan", cat: "education", title: "Homeschool Interdisciplinary Planner", persona: "Homeschool Parent", desc: "Designs a 5-day interdisciplinary curriculum integrating a child's passions into core standards.", key: "differentiate", tags: ["Homeschool"] }},
      {{ id: 52, route: "/v1/edu/parent-comms", cat: "education", title: "Bilingual Parent-Teacher Bridge", persona: "Teacher / Admin", desc: "Drafts culturally respectful updates in Spanish/Arabic/etc. framing behavioral feedback constructively.", key: "differentiate", tags: ["Comms"] }},
      {{ id: 53, route: "/v1/social/benefits-finder", cat: "education", title: "Social Safety-Net Benefit Matcher", persona: "Low-Income Advocate", desc: "Calculates eligible federal/state programs (SNAP, Medicaid, WIC, LIHEAP) from household demographics.", key: "differentiate", tags: ["Benefits"] }},
      {{ id: 54, route: "/v1/mentalhealth/crisis-aid", cat: "education", title: "Youth Crisis Text De-escalator", persona: "School Counselor", desc: "Provides active listening phrasing, empathy validation, and safety triage cues for youth distress texts.", key: "differentiate", tags: ["Mental Health"] }},
      {{ id: 55, route: "/v1/legal/court-prep", cat: "education", title: "Pro-Se Court Hearing Companion", persona: "Self-Represented Litigant", desc: "Translates small claims summons into plain English allegations, evidence checklists, and court decorum.", key: "differentiate", tags: ["Legal"] }}
    ];

    let currentCategory = 'all';

    function renderCards(endpoints) {{
      const grid = document.getElementById('cards-grid');
      const emptyState = document.getElementById('empty-state');

      if (endpoints.length === 0) {{
        grid.innerHTML = '';
        emptyState.classList.remove('hidden');
        return;
      }}

      emptyState.classList.add('hidden');
      grid.innerHTML = endpoints.map(function(ep) {{
        const tagsHtml = ep.tags.map(function(t) {{
          return '<span class="text-[9px] px-1.5 py-0.5 rounded bg-zinc-800/80 text-zinc-400 font-mono">' + t + '</span>';
        }}).join('');

        return '<div class="card-hover p-4 rounded-xl bg-[#121215] border border-white/[0.08] flex flex-col justify-between group cursor-pointer" onclick="openStudioWithKey(\\'' + ep.key + '\\')">' +
          '<div>' +
            '<div class="flex items-center justify-between mb-2.5">' +
              '<div class="flex items-center gap-1.5">' +
                '<span class="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">POST</span>' +
                '<span class="text-[10px] font-mono text-zinc-500">#' + ep.id + '</span>' +
              '</div>' +
              '<span class="text-[10px] font-medium text-zinc-400 bg-white/[0.04] px-2 py-0.5 rounded-full border border-white/[0.06] truncate max-w-[130px]">' + ep.persona + '</span>' +
            '</div>' +
            '<h3 class="text-sm font-semibold text-white group-hover:text-indigo-400 transition tracking-tight">' + ep.title + '</h3>' +
            '<div class="text-[11px] font-mono text-zinc-500 truncate mt-0.5">' + ep.route + '</div>' +
            '<p class="text-xs text-zinc-400 mt-2.5 line-clamp-2 leading-relaxed font-normal">' + ep.desc + '</p>' +
          '</div>' +
          '<div class="mt-4 pt-3 border-t border-white/[0.06] flex items-center justify-between text-xs">' +
            '<div class="flex gap-1">' + tagsHtml + '</div>' +
            '<div class="flex items-center gap-2">' +
              '<button onclick="event.stopPropagation(); copyDirectCurl(\\'' + ep.route + '\\')" class="p-1 rounded text-zinc-500 hover:text-white transition" title="Copy cURL">' +
                '<i class="fa-solid fa-terminal text-[11px]"></i>' +
              '</button>' +
              '<span class="text-indigo-400 text-[11px] font-semibold flex items-center gap-1 group-hover:translate-x-0.5 transition-transform">' +
                'Test <i class="fa-solid fa-arrow-right text-[9px]"></i>' +
              '</span>' +
            '</div>' +
          '</div>' +
        '</div>';
      }}).join('');
    }}

    function filterCards() {{
      const query = document.getElementById('search-input').value.toLowerCase().trim();
      const clearBtn = document.getElementById('clear-search');
      
      if (query) {{
        clearBtn.classList.remove('hidden');
      }} else {{
        clearBtn.classList.add('hidden');
      }}

      let filtered = ALL_ENDPOINTS;

      if (currentCategory !== 'all') {{
        if (currentCategory === 'vision') {{
          filtered = filtered.filter(function(ep) {{ return ep.tags.includes('Vision'); }});
        }} else {{
          filtered = filtered.filter(function(ep) {{ return ep.cat === currentCategory; }});
        }}
      }}

      if (query) {{
        filtered = filtered.filter(function(ep) {{ 
          return ep.title.toLowerCase().includes(query) ||
                 ep.route.toLowerCase().includes(query) ||
                 ep.persona.toLowerCase().includes(query) ||
                 ep.desc.toLowerCase().includes(query);
        }});
      }}

      renderCards(filtered);
    }}

    function setCategory(cat) {{
      currentCategory = cat;
      document.querySelectorAll('.cat-pill').forEach(function(btn) {{
        btn.classList.remove('active-pill', 'bg-white', 'text-black', 'border-white/[0.12]');
        btn.classList.add('bg-[#121215]', 'text-zinc-400', 'border-white/[0.08]');
      }});

      const activeBtn = document.getElementById('pill-' + cat);
      if (activeBtn) {{
        activeBtn.classList.remove('bg-[#121215]', 'text-zinc-400', 'border-white/[0.08]');
        activeBtn.classList.add('active-pill', 'bg-white', 'text-black', 'border-white/[0.12]');
      }}

      filterCards();
    }}

    function clearSearch() {{
      document.getElementById('search-input').value = '';
      filterCards();
    }}

    function resetFilters() {{
      document.getElementById('search-input').value = '';
      setCategory('all');
    }}

    function scrollToSection(id) {{
      document.getElementById(id).scrollIntoView({{ behavior: 'smooth' }});
    }}

    // Studio Drawer Controls
    function openStudio() {{
      document.getElementById('studio-drawer').classList.remove('hidden');
      document.body.classList.add('overflow-hidden');
      onStudioEndpointChange();
    }}

    function openStudioWithKey(key) {{
      const select = document.getElementById('studio-endpoint-select');
      if (select) {{
        select.value = key;
      }}
      openStudio();
    }}

    function closeStudio() {{
      document.getElementById('studio-drawer').classList.add('hidden');
      document.body.classList.remove('overflow-hidden');
    }}

    window.addEventListener('keydown', function(e) {{
      if (e.key === 'Escape') closeStudio();
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {{
        e.preventDefault();
        document.getElementById('search-input').focus();
      }}
    }});

    function onStudioEndpointChange() {{
      const select = document.getElementById('studio-endpoint-select');
      const key = select.value;
      const conf = ENDPOINT_CONFIGS[key] || ENDPOINT_CONFIGS['explain-lab'];
      
      document.getElementById('studio-route-pill').innerText = conf.route;
      document.getElementById('studio-input').value = conf.defaultSample;
      document.getElementById('zapier-url').innerText = window.location.origin + conf.route;
      updateCurlPreview();
    }}

    function resetStudioSample() {{
      onStudioEndpointChange();
    }}

    function updateCurlPreview() {{
      const select = document.getElementById('studio-endpoint-select');
      const conf = ENDPOINT_CONFIGS[select.value] || ENDPOINT_CONFIGS['explain-lab'];
      const host = window.location.origin;
      const curl = 'curl -X POST "' + host + conf.route + '" \\\\\n' +
        '  -H "Content-Type: application/json" \\\\\n' +
        '  -d \\'{"input": "..."}\\'' ;
      document.getElementById('studio-curl-pre').innerText = curl;
    }}

    async function runStudioExecution() {{
      const select = document.getElementById('studio-endpoint-select');
      const model = document.getElementById('studio-model-select').value;
      const input = document.getElementById('studio-input').value.trim();
      const loader = document.getElementById('studio-loader');
      const jsonPre = document.getElementById('studio-json-pre');
      const latencyBadge = document.getElementById('studio-latency');
      const runBtn = document.getElementById('studio-run-btn');

      if (!input) {{
        alert("Please enter input text or reload the preset sample.");
        return;
      }}

      loader.classList.remove('hidden');
      latencyBadge.classList.add('hidden');
      runBtn.disabled = true;
      runBtn.classList.add('opacity-50');

      try {{
        const targetUrl = window.location.hostname.includes('pages.dev')
          ? 'https://smart-eaas.muhammadamran40.workers.dev/api/execute'
          : '/api/execute';

        const resp = await fetch(targetUrl, {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            endpoint: select.value,
            model: model,
            input: input
          }})
        }});

        const data = await resp.json();
        loader.classList.add('hidden');
        runBtn.disabled = false;
        runBtn.classList.remove('opacity-50');

        if (data.success) {{
          jsonPre.innerText = JSON.stringify(data.data, null, 2);
          latencyBadge.innerText = data.latency_ms + 'ms';
          latencyBadge.classList.remove('hidden');
        }} else {{
          jsonPre.innerText = '// Error: ' + (data.error || 'Execution failed');
        }}
      }} catch (err) {{
        loader.classList.add('hidden');
        runBtn.disabled = false;
        runBtn.classList.remove('opacity-50');
        jsonPre.innerText = '// Network Error: ' + err.message;
      }}
    }}

    function switchOutputTab(tab) {{
      ['json', 'curl', 'zapier'].forEach(function(t) {{
        document.getElementById('view-out-' + t).classList.add('hidden');
        document.getElementById('tab-out-' + t).classList.remove('text-white', 'border-b-2', 'border-indigo-500', 'font-semibold');
        document.getElementById('tab-out-' + t).classList.add('text-zinc-400');
      }});

      document.getElementById('view-out-' + tab).classList.remove('hidden');
      document.getElementById('tab-out-' + tab).classList.add('text-white', 'border-b-2', 'border-indigo-500', 'font-semibold');
      document.getElementById('tab-out-' + tab).classList.remove('text-zinc-400');
    }}

    function copyStudioOutput() {{
      const text = document.getElementById('studio-json-pre').innerText;
      navigator.clipboard.writeText(text);
      alert('JSON output copied to clipboard!');
    }}

    function copyDirectCurl(route) {{
      const curl = 'curl -X POST "' + window.location.origin + route + '" \\\\\n' +
        '  -H "Content-Type: application/json" \\\\\n' +
        '  -d \\'{"input": "..."}\\'' ;
      navigator.clipboard.writeText(curl);
      alert('cURL command copied to clipboard!');
    }}

    // Surface Switcher
    function switchSurface(surface) {{
      ['whatsapp', 'sheets', 'zapier'].forEach(function(s) {{
        document.getElementById('surface-' + s).classList.add('hidden');
        document.getElementById('surface-btn-' + s).classList.remove('text-white', 'border-b-2', 'border-indigo-500', 'font-semibold');
        document.getElementById('surface-btn-' + s).classList.add('text-zinc-400');
      }});

      document.getElementById('surface-' + surface).classList.remove('hidden');
      document.getElementById('surface-btn-' + surface).classList.add('text-white', 'border-b-2', 'border-indigo-500', 'font-semibold');
      document.getElementById('surface-btn-' + surface).classList.remove('text-zinc-400');
    }}

    function setSimScenario(scenario) {{
      const chat = document.getElementById('chat-stream');
      if (scenario === 'scam') {{
        chat.innerHTML = 
          '<div class="bg-zinc-800/90 text-zinc-300 p-2.5 rounded-2xl rounded-tl-none max-w-[85%] text-[10px]">Forward any suspicious SMS or email here.</div>' +
          '<div class="bg-indigo-600 text-white p-2.5 rounded-2xl rounded-tr-none ml-auto max-w-[85%] text-[10px]">' +
            '<div class="bg-black/30 p-1 rounded mb-1 text-[9px] flex items-center gap-1"><i class="fa-solid fa-image"></i> [SMS: "Chase Fraud Alert: Account frozen..."]</div>' +
            'Is this real?' +
          '</div>' +
          '<div class="bg-emerald-950/70 border border-emerald-500/30 p-2.5 rounded-2xl rounded-tl-none text-[10px] text-zinc-200 space-y-1">' +
            '<div class="font-bold text-red-400 flex items-center gap-1"><i class="fa-solid fa-triangle-exclamation"></i> 99% SCAM CONFIRMED</div>' +
            '<p class="text-[9.5px]">This is an urgency phishing trap trying to steal your card PIN.</p>' +
          '</div>';
      }} else if (scenario === 'lab') {{
        chat.innerHTML = 
          '<div class="bg-zinc-800/90 text-zinc-300 p-2.5 rounded-2xl rounded-tl-none max-w-[85%] text-[10px]">Forward any lab test photo here.</div>' +
          '<div class="bg-indigo-600 text-white p-2.5 rounded-2xl rounded-tr-none ml-auto max-w-[85%] text-[10px]">' +
            '<div class="bg-black/30 p-1 rounded mb-1 text-[9px] flex items-center gap-1"><i class="fa-solid fa-file-medical"></i> [Photo: Fasting Glucose 118, A1c 5.9%]</div>' +
            'Doctor is busy until Friday. What does this mean?' +
          '</div>' +
          '<div class="bg-blue-950/70 border border-blue-500/30 p-2.5 rounded-2xl rounded-tl-none text-[10px] text-zinc-200 space-y-1">' +
            '<div class="font-bold text-blue-400 flex items-center gap-1"><i class="fa-solid fa-heart-pulse"></i> PRE-DIABETES MARKER DETECTED</div>' +
            '<p class="text-[9.5px]">Fasting glucose is slightly elevated above 99 mg/dL. This indicates early insulin resistance.</p>' +
          '</div>';
      }} else if (scenario === 'lease') {{
        chat.innerHTML = 
          '<div class="bg-zinc-800/90 text-zinc-300 p-2.5 rounded-2xl rounded-tl-none max-w-[85%] text-[10px]">Send lease agreement clause photo or text.</div>' +
          '<div class="bg-indigo-600 text-white p-2.5 rounded-2xl rounded-tr-none ml-auto max-w-[85%] text-[10px]">' +
            '<div class="bg-black/30 p-1 rounded mb-1 text-[9px] flex items-center gap-1"><i class="fa-solid fa-file-contract"></i> [Clause: "Tenant pays all repairs under $350..."]</div>' +
            'Can the landlord make me pay this?' +
          '</div>' +
          '<div class="bg-amber-950/70 border border-amber-500/30 p-2.5 rounded-2xl rounded-tl-none text-[10px] text-zinc-200 space-y-1">' +
            '<div class="font-bold text-amber-400 flex items-center gap-1"><i class="fa-solid fa-triangle-exclamation"></i> UNLAWFUL CLAUSE WARNING</div>' +
            '<p class="text-[9.5px]">Most states hold landlords legally responsible for habitability repairs regardless of lease clauses.</p>' +
          '</div>';
      }}
    }}

    // Init
    window.addEventListener('DOMContentLoaded', function() {{
      renderCards(ALL_ENDPOINTS);
      onStudioEndpointChange();
    }});
  </script>
</body>
</html>"""
    return html_content

def build_all():
    # 1. Generate HTML
    html = generate_html()
    os.makedirs("public", exist_ok=True)
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated public/index.html:", len(html), "bytes")

    # 2. Generate src/index.js embedding the HTML safely via json.dumps
    prompts_code = "const ENDPOINT_PROMPTS = " + json.dumps(ENDPOINT_PROMPTS, indent=2) + ";"
    escaped_html = json.dumps(html)

    worker_code = f"""// Smart EaaS — Production Endpoint as a Service
// Engineered with inspiration from recent.design and skills.sh

{prompts_code}

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

    // Return HTML Application
    return new Response(APP_HTML, {{
      headers: {{ ...corsHeaders, "Content-Type": "text/html; charset=utf-8" }}
    }});
  }}
}};
"""
    with open("src/index.js", "w", encoding="utf-8") as f:
        f.write(worker_code)
    print("Generated src/index.js:", len(worker_code), "bytes")

    # 3. Check with node
    res = subprocess.run(["node", "--check", "src/index.js"], capture_output=True, text=True)
    if res.returncode == 0:
        print("[SUCCESS] node --check passed with 0 errors!")
    else:
        print("[ERROR] node --check failed:", res.stderr)
        raise SystemExit(1)

if __name__ == "__main__":
    build_all()
