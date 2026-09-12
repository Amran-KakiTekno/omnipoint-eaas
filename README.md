# OmniPoint AI — Endpoint as a Service (EaaS)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Cloudflare%20Edge-blue?style=for-the-badge&logo=cloudflare)](https://omnipoint-eaas.muhammadamran40.workers.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Amran--KakiTekno-181717?style=for-the-badge&logo=github)](https://github.com/Amran-KakiTekno/omnipoint-eaas)

> **Live Production Edge Deployment:** [https://omnipoint-eaas.muhammadamran40.workers.dev](https://omnipoint-eaas.muhammadamran40.workers.dev)

A zero-cost, edge-deployed **Endpoint as a Service (EaaS)** platform that delivers **55+ specialized, deterministic AI microservices** across 5 core real-world sectors:
1. **Everyday Individuals, Families & Consumers** (Lab explainer, scam shield, lease audit, parking tickets, allergen alerts)
2. **Non-Profits (NPOs), NGOs & Charities** (Grant RFP matcher, donor storytelling, Form 990 audit, disaster triage)
3. **Solopreneurs, Creators & Freelancers** (Scope creep defense, 1-to-10 content repurposer, brand pitching, timestamps)
4. **Local Small Businesses & Trades** (Review de-escalator, voice-to-job estimate, POS slip parser, shift swap arbiter)
5. **Education, Healthcare & Civic Life** (Differentiated homework, rubric critique, clinical SOAP notes, council digests)

---

## 🚀 Live Interactive Features

- **Global Edge Routing**: Deployed across 300+ Cloudflare data centers using Cloudflare Workers with sub-millisecond overhead.
- **Deterministic Schema Validation**: Every endpoint takes raw, messy, unstructured input (text, PDF, audio notes, photos) and enforces **100% strict JSON schema compliance**.
- **Model Flexibility (`rootsys.cloud`)**:
  - `deepseek-v4.1-flash`: Ultra-fast (<400ms) execution for real-time text parsing and classification.
  - `kimi-k3`: Multimodal reasoning with native vision support for receipts, food labels, and medical test photos.
  - `deepseek-v4-pro` & `glm-5.3`: High-depth analytical reasoning for legal leases and municipal RFPs.
- **Built-in UI Playground**: Includes an interactive web dashboard with pre-loaded sample data, live latency timers, and one-click cURL / Zapier snippet generators.

---

## 📱 4 Delivery Surfaces (For Non-Developers)

```
[User Touchpoint]                [OmniPoint EaaS Edge Worker]          [Output Value]
WhatsApp / Telegram / SMS   -->                                   --> Plain-Language Safety Alert
Google Sheets Formula       -->   https://omnipoint-eaas...       --> Populated Grid Cell
Zapier / Make.com Webhook   -->   (Prompt + Schema Validation)    --> Automated Slack / CRM Entry
Web Dashboard Playground    -->                                   --> Copyable JSON / cURL
```

1. **WhatsApp & SMS Bot**: Users forward photos or text messages (e.g. suspicious texts, lab reports) to receive instant, reassuring breakdowns.
2. **Google Sheets / Excel Functions**: Custom formula `=AI_GRANT_MATCH(A2, B2)` or `=AI_DIFF_HOMEWORK(A2)` for educators and non-profit coordinators.
3. **No-Code Webhooks (Zapier & Make)**: Plug endpoints directly between Google Maps, Typeform, Stripe, and Slack.
4. **Interactive Web Portal**: Direct cURL and REST endpoints for developers and agencies.

---

## 🛠️ Quick Start & API Usage

### Example 1: Scam & Phishing Defender
\`\`\`bash
curl -X POST "https://omnipoint-eaas.muhammadamran40.workers.dev/v1/safety/scam-detector" \\
  -H "Content-Type: application/json" \\
  -d '{"input": "URGENT: Your Netflix membership is frozen. Click http://netflix-pay-verify81.com within 1 hour."}'
\`\`\`

**Response:**
\`\`\`json
{
  "is_scam": true,
  "confidence_score": 0.99,
  "scam_type": "Brand Impersonation / Urgency Phishing",
  "red_flags": [
    "Urgent threat: 'membership is frozen'",
    "Artificial 1-hour deadline",
    "Suspicious unofficial domain 'netflix-pay-verify81.com'"
  ],
  "plain_language_verdict": "This is a scam. Netflix would never send a text like this. Do not click it.",
  "safe_action_steps": [
    "DO NOT click the link or reply.",
    "Delete the text message immediately.",
    "Block the sender's phone number."
  ]
}
\`\`\`

### Example 2: Medical Lab Report Explainer
\`\`\`bash
curl -X POST "https://omnipoint-eaas.muhammadamran40.workers.dev/v1/health/explain-lab" \\
  -H "Content-Type: application/json" \\
  -d '{"input": "Fasting Glucose: 118 mg/dL (Ref: 70-99). Total Cholesterol: 224 mg/dL."}'
\`\`\`

---

## 💡 Zero-Cost Deployment Architecture

- **Cloudflare Workers**: Free tier provides 100,000 requests/day at \$0.00/month.
- **Cloudflare R2**: S3-compatible storage for temporary PDF and audio uploads (10 GB free, 0 egress fees).
- **GitHub**: Source code hosting and automated continuous deployment.
- **Upstream LLM**: `https://rootsys.cloud/v1` powered by DeepSeek and Kimi engines.

---

## 📄 License
MIT License. Built with passion for open-source AI microservices.
