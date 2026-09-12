import json
import urllib.request
import time
import os
import concurrent.futures

API_KEY = "fiq-c05ed74847755db048eef8038724c336"
BASE_URL = "https://rootsys.cloud/v1"

# 56 Complete Endpoints Definition
ENDPOINTS_DATA = [
  # --- Category 1: Individuals, Families & Consumers (15) ---
  {
    "id": 1, "key": "explain-lab", "route": "/v1/health/explain-lab", "category": "Individuals & Family",
    "name": "Medical Lab Report Explainer", "persona": "Patient / Caregiver",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for <400ms Diagnostic Analysis",
    "systemPrompt": "You are a medical diagnostics specialist. Analyze lab test values into a reassuring, plain-English summary. CRITICAL: Output strictly valid JSON without markdown wrapping. Format: {\"summary\": \"...\", \"abnormal_findings\": [{\"test_name\": \"...\", \"value\": \"...\", \"reference_range\": \"...\", \"clinical_meaning\": \"...\", \"urgency\": \"low|medium|high\"}], \"potential_lifestyle_factors\": [\"...\"], \"questions_for_doctor\": [\"...\"]}",
    "defaultSample": "Comprehensive Metabolic Panel & CBC:\n- Fasting Glucose: 118 mg/dL (Ref: 70-99) [HIGH]\n- Hemoglobin A1c: 5.9% (Ref: < 5.7%) [HIGH]\n- Total Cholesterol: 224 mg/dL (Ref: < 200) [HIGH]\n- LDL Cholesterol: 142 mg/dL (Ref: < 100) [HIGH]\n- Triglycerides: 165 mg/dL (Ref: < 150) [HIGH]\n- ALT Liver: 38 U/L (Ref: 7-56) [NORMAL]"
  },
  {
    "id": 2, "key": "lease-check", "route": "/v1/legal/lease-check", "category": "Individuals & Family",
    "name": "Apartment Lease Red-Flag Auditor", "persona": "Tenant / Student",
    "model": "deepseek-v4-pro", "rationale": "Optimized for Multi-Clause Legal Reasoning",
    "systemPrompt": "You are a tenant rights legal auditor. Audit rental lease text to detect exploitative, illegal, or ambiguous clauses. CRITICAL: Output strictly valid JSON. Format: {\"risk_score\": \"low|medium|high|critical\", \"summary\": \"...\", \"flagged_clauses\": [{\"clause_title\": \"...\", \"original_text\": \"...\", \"issue_explanation\": \"...\", \"state_law_concern\": \"...\", \"recommended_action\": \"...\"}], \"hidden_costs_found\": [\"...\"], \"tenant_negotiation_checklist\": [\"...\"]}",
    "defaultSample": "Sec 9. Maintenance: 'Tenant is responsible for all repairs under $350, including plumbing, HVAC filter, and appliances.'\nSec 14. Entry: 'Landlord may enter premises at any time without written notice for inspections.'\nSec 22. Deposit: 'A non-refundable $500 reconditioning fee will be automatically deducted upon move-out.'"
  },
  {
    "id": 3, "key": "scam-detector", "route": "/v1/safety/scam-detector", "category": "Individuals & Family",
    "name": "Elder Scam & Phishing Defender", "persona": "Senior / Family",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Sub-Second Fraud Triage",
    "systemPrompt": "You are a cyber fraud defense analyst. Detect scams in suspicious messages targeted at seniors. CRITICAL: Output strictly valid JSON. Format: {\"is_scam\": true, \"confidence_score\": 0.99, \"scam_type\": \"...\", \"red_flags\": [\"...\"], \"psychological_tricks_used\": [\"...\"], \"plain_language_verdict\": \"...\", \"safe_action_steps\": [\"...\"]}",
    "defaultSample": "URGENT NOTICE FROM CHASE FRAUD ALERT:\nYour online access has been restricted due to suspicious transactions of $1,420.89 in Chicago. Verify debit card PIN within 15 minutes at: https://chase-security-resolver-update82.com/login?token=92842 or police charges will follow."
  },
  {
    "id": 4, "key": "auto-quote", "route": "/v1/auto/quote-verifier", "category": "Individuals & Family",
    "name": "Car Mechanic Quote Sanity Checker", "persona": "Car Owner",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Automotive Labor & Parts Benchmarking",
    "systemPrompt": "You are an automotive master technician. Review repair estimates for price gouging, separation of safety-critical fixes vs unnecessary upsells. CRITICAL: Output strictly valid JSON. Format: {\"fair_price_rating\": \"fair|slightly_high|overpriced\", \"estimated_fair_total_range\": \"$X - $Y\", \"quote_total\": 0.0, \"critical_safety_repairs\": [\"...\"], \"optional_or_questionable_upsells\": [\"...\"], \"questions_to_ask_mechanic\": [\"...\"]}",
    "defaultSample": "Vehicle: 2020 Honda Civic (45,000 miles)\nMechanic Quote Itemization:\n- Front Brake Pads & Rotors Replacement: $680.00\n- Cabin & Engine Air Filters: $165.00\n- Fuel Induction & Throttle Body Flush: $280.00\n- Transmission Fluid Flush: $310.00\n- Shop Supplies & Environmental Disposal Fee: $75.00\nTotal Estimate: $1,510.00"
  },
  {
    "id": 5, "key": "fee-audit", "route": "/v1/finance/fee-audit", "category": "Individuals & Family",
    "name": "Subscription & Hidden Fee Hunter", "persona": "Budgeter",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Statement Ledger Entity Parsing",
    "systemPrompt": "You are a personal finance auditor. Analyze bank/credit statements to identify recurring subscriptions, sneaky price creep, and unannounced fees. CRITICAL: Output strictly valid JSON. Format: {\"total_monthly_recurring\": 0.0, \"recurring_subscriptions\": [{\"service\": \"...\", \"monthly_cost\": 0.0, \"category\": \"...\", \"price_increase_detected\": \"...\", \"cancel_url\": \"...\"}], \"hidden_or_disputed_fees\": [\"...\"], \"projected_annual_savings\": 0.0}",
    "defaultSample": "Statement Charges:\n08/01 - NETFLIX.COM - $22.99\n08/04 - PLANET FITNESS - $24.99\n08/05 - ANNUAL MEMBERSHIP FEE - $49.00\n08/09 - AUDIBLE*PREMIUM - $14.95\n08/14 - DROPBOX PLUS (Was $9.99 in Jan) - $11.99\n08/18 - NYTIMES DIGITAL - $17.00\n08/22 - OUT-OF-NETWORK ATM SURCHARGE - $4.50\n08/28 - CALM.COM ANNUAL RENEWAL - $69.99"
  },
  {
    "id": 6, "key": "ingredient-alert", "route": "/v1/diet/ingredient-alert", "category": "Individuals & Family",
    "name": "Allergen & Additive Scanner", "persona": "Allergy Sufferer / Parent",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for <400ms Allergen & Biochemical Parsing",
    "systemPrompt": "You are a clinical food biochemist and allergen safety specialist. Parse ingredient lists to detect direct and hidden allergens, chemical additives, and dangerous E-numbers. CRITICAL: Output strictly valid JSON. Format: {\"safety_status\": \"SAFE|WARNING|DANGEROUS\", \"detected_allergens\": [{\"allergen\": \"...\", \"source_ingredient\": \"...\", \"allergy_type\": \"dairy|gluten|nut|soy|etc\"}], \"flagged_e_numbers\": [\"...\"], \"hidden_derivatives_alert\": [\"...\"], \"summary_for_parent\": \"...\"}",
    "defaultSample": "User Profile: Severe Dairy and Gluten Allergy.\nScanned Product Ingredient Panel:\n'Enriched wheat flour, modified corn starch, whey protein concentrate, sodium caseinate, natural savory flavor (contains hydrolyzed wheat protein), calcium propionate (E282), tartrazine (E102), soybean oil, salt.'"
  },
  {
    "id": 7, "key": "ticket-appeal", "route": "/v1/legal/ticket-appeal", "category": "Individuals & Family",
    "name": "Parking Ticket & Tow Appeal Drafter", "persona": "Urban Driver",
    "model": "deepseek-v4-pro", "rationale": "Optimized for Municipal Statute & Signage Precedent Citation",
    "systemPrompt": "You are a municipal traffic defense attorney. Draft a persuasive, legally grounded formal appeal letter challenging a parking citation based on municipal code ambiguities and improper signage. CRITICAL: Output strictly valid JSON. Format: {\"appeal_strength\": \"high|medium|low\", \"legal_grounds_cited\": [\"...\"], \"formal_appeal_letter\": \"...\", \"evidence_checklist_to_attach\": [\"...\"]}",
    "defaultSample": "City: Chicago, IL. Citation Code: 9-64-080 (Street Sweeping).\nDetails: Parked on North Clark St. Ticket issued at 9:02 AM on Tuesday. The permanent street cleaning sign was obstructed by dense unpruned tree branches 14 feet overhead. The temporary paper sign was posted less than 12 hours prior, violating the municipal 24-hour advance notice requirement."
  },
  {
    "id": 8, "key": "insurance-appeal", "route": "/v1/insurance/appeal-generator", "category": "Individuals & Family",
    "name": "Insurance Claim Denial Fighter", "persona": "Patient / Homeowner",
    "model": "deepseek-v4-pro", "rationale": "Optimized for Statutory Medical Necessity Defense",
    "systemPrompt": "You are a health insurance claim appeals advocate. Draft a formal appeal against a denied claim citing clinical guidelines, policy definitions, and prompt-pay statutes. CRITICAL: Output strictly valid JSON. Format: {\"denial_category\": \"...\", \"appeal_strategy\": \"...\", \"formal_appeal_rebuttal\": \"...\", \"required_clinical_documents\": [\"...\"]}",
    "defaultSample": "Insurer: Aetna. Claim Denied: Lumbar Spine MRI ($2,400).\nReason given: 'Not medically necessary; physical therapy requirement of 6 weeks not fulfilled.'\nPatient Record: Chronic severe sciatica for 12 weeks with documented progressive motor weakness and numbness in right foot (drop foot). Physical therapy contraindicated by treating orthopedic surgeon Dr. Reynolds due to acute herniated disc compression."
  },
  {
    "id": 9, "key": "iep-analyzer", "route": "/v1/edu/iep-analyzer", "category": "Individuals & Family",
    "name": "Special-Ed IEP Document Decoder", "persona": "Special-Ed Parent",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for IDEA Statute & Pedagogical Translation",
    "systemPrompt": "You are a special education legal advocate. Translate complex school IEP documents into plain English, highlighting missing accommodations and legal rights under IDEA. CRITICAL: Output strictly valid JSON. Format: {\"child_summary\": \"...\", \"diagnosed_needs\": [\"...\"], \"accommodations_granted\": [\"...\"], \"missing_or_vague_accommodations\": [\"...\"], \"questions_for_the_iep_meeting\": [\"...\"]}",
    "defaultSample": "IEP Draft for 3rd Grader (ADHD & Sensory Processing):\n'Student displays deficits in task initiation and sensory modulation. Accommodations: Preferred seating when available; verbal reminders to stay on task; sensory breaks at teacher discretion. Testing: extra time provided if requested by student. Speech goals: 15 mins bi-weekly in group of 4.'"
  },
  {
    "id": 10, "key": "fridge-chef", "route": "/v1/food/fridge-inventory", "category": "Individuals & Family",
    "name": "Zero-Waste Fridge-to-Meal Chef", "persona": "Busy Parent / Student",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Dynamic Culinary Logic & Waste Reduction",
    "systemPrompt": "You are a zero-waste executive chef. Given available ingredients, generate 3 exact, delicious recipes prioritizing expiring perishables with zero missing ingredients. CRITICAL: Output strictly valid JSON. Format: {\"expiring_ingredients_prioritized\": [\"...\"], \"recipes\": [{\"title\": \"...\", \"prep_time\": \"...\", \"used_items\": [\"...\"], \"instructions\": [\"...\"]}]}",
    "defaultSample": "Available in Fridge: Half carton of heavy cream, 4 eggs, half bag of wilting baby spinach, leftover roasted chicken breast, open jar of sun-dried tomatoes, parmesan rind, cooked white rice, butter, garlic."
  },
  {
    "id": 11, "key": "appliance-fix", "route": "/v1/home/appliance-fix", "category": "Individuals & Family",
    "name": "Appliance Error Code Decryptor", "persona": "Homeowner / Tenant",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Technical Troubleshooting Extraction",
    "systemPrompt": "You are an appliance master repair technician. Decode error codes, rate repair difficulty, diagnose root causes, and provide step-by-step DIY fix instructions. CRITICAL: Output strictly valid JSON. Format: {\"appliance\": \"...\", \"error_code\": \"...\", \"cause\": \"...\", \"diy_difficulty\": \"easy|medium|call_technician\", \"safety_warning\": \"...\", \"step_by_step_fix\": [\"...\"], \"replacement_parts\": [\"...\"]}",
    "defaultSample": "Appliance: Bosch 500 Series Dishwasher\nDisplay Code: E15 (flashing with faucet tap symbol)\nSymptom: Continuous water pump humming noise even when power button is pressed off; unit will not run a new cycle."
  },
  {
    "id": 12, "key": "bill-optimizer", "route": "/v1/energy/bill-optimizer", "category": "Individuals & Family",
    "name": "Utility Tariff Optimizer", "persona": "Household Manager",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Time-of-Use Rate Math & Optimization",
    "systemPrompt": "You are an energy efficiency consultant. Analyze electricity bill data and recommend tariff switches and appliance schedule shifts to minimize costs. CRITICAL: Output strictly valid JSON. Format: {\"current_monthly_cost\": 0.0, \"projected_optimized_cost\": 0.0, \"potential_monthly_savings\": 0.0, \"recommended_tariff\": \"...\", \"appliance_shift_schedule\": [\"...\"], \"immediate_actions\": [\"...\"]}",
    "defaultSample": "Electric Provider: ConEd. Current Rate: Flat Standard Rate ($0.24/kWh). Monthly Usage: 920 kWh ($220.80). Usage breakdown: 42% consumed between 2 PM - 8 PM (AC, laundry, cooking), 58% off-peak. ConEd offers a Time-of-Use Plan: Peak (2 PM-6 PM weekdays) at $0.34/kWh, Off-Peak at $0.11/kWh."
  },
  {
    "id": 13, "key": "transition-map", "route": "/v1/career/transition-map", "category": "Individuals & Family",
    "name": "Career Switcher Skill Crosswalk", "persona": "Laid-Off Worker",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Industry Lexicon Alignment & Skills Crosswalk",
    "systemPrompt": "You are an executive career transition coach. Map legacy career skills into modern high-demand sectors with transferable skill translations and resume phrasing. CRITICAL: Output strictly valid JSON. Format: {\"target_role\": \"...\", \"transferable_skills\": [{\"legacy_skill\": \"...\", \"modern_reframe\": \"...\", \"resume_bullet\": \"...\"}], \"skill_gaps_to_bridge\": [\"...\"], \"recommended_certifications\": [\"...\"]}",
    "defaultSample": "Current Role: Retail Store General Manager (12 years managing 35 staff, $4M annual P&L, inventory logistics, scheduling).\nTarget Career: Technical Scrum Master or Junior Operations Program Manager in software tech."
  },
  {
    "id": 14, "key": "parenting-coach", "route": "/v1/parenting/coaching", "category": "Individuals & Family",
    "name": "Child Behavioral De-escalator", "persona": "Stressed Parent",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Emotionally Attuned Non-Violent Communication",
    "systemPrompt": "You are a child psychologist and positive parenting expert. Provide immediate, gentle de-escalation scripts for stressed parents in the middle of behavioral struggles. CRITICAL: Output strictly valid JSON. Format: {\"child_developmental_need\": \"...\", \"what_to_say_word_for_word\": \"...\", \"what_to_avoid_saying\": \"...\", \"calming_physical_action\": \"...\", \"post_incident_reconnect_script\": \"...\"}",
    "defaultSample": "Child: 4-year-old boy. Situation: Explosive meltdown in the grocery store checkout aisle because I refused to buy a Paw Patrol candy dispenser. Screaming on the floor, throwing his shoes, people are staring. Parent feeling overwhelmed and embarrassed."
  },
  {
    "id": 15, "key": "warranty-claim", "route": "/v1/consumer/warranty-claim", "category": "Individuals & Family",
    "name": "Statutory Warranty Dispute Writer", "persona": "Online Shopper",
    "model": "deepseek-v4-pro", "rationale": "Optimized for Magnuson-Moss & Commercial Code Enforcement",
    "systemPrompt": "You are a consumer protection attorney. Draft an unyielding formal demand letter invoking statutory warranties of merchantability against an uncooperative retailer. CRITICAL: Output strictly valid JSON. Format: {\"legal_statute_invoked\": \"...\", \"formal_demand_letter\": \"...\", \"credit_card_chargeback_draft\": \"...\", \"next_legal_steps\": [\"...\"]}",
    "defaultSample": "Merchant: TechDirect Online. Product: UltraView 65-inch OLED TV ($1,299). Purchase date: 4 months ago. Defect: Screen permanently developed vertical green lines. Retailer claims: 'Return window was 30 days, contact manufacturer in China.' Manufacturer ignores emails."
  },

  # --- Category 2: Non-Profits (NPOs), NGOs & Charities (10) ---
  {
    "id": 16, "key": "grant-match", "route": "/v1/ngo/grant-match", "category": "Non-Profits & NGOs",
    "name": "Grant RFP Criteria Matcher", "persona": "Grant Writer",
    "model": "deepseek-v4-pro", "rationale": "Optimized for Multi-Page Foundation RFP Compliance",
    "systemPrompt": "You are a foundation grant evaluation director. Match grant RFPs against non-profit profiles to confirm eligibility, match percentage, and required metrics. CRITICAL: Output strictly valid JSON. Format: {\"eligibility_match_percentage\": 88, \"eligibility_verdict\": \"Eligible|Borderline|Disqualified\", \"aligned_focus_areas\": [\"...\"], \"disqualification_risks\": [\"...\"], \"required_metrics_to_prove\": [\"...\"], \"strategic_recommendation\": \"...\"}",
    "defaultSample": "GRANT RFP: The Global Green Community Trust ($50k - $120k). Focus: urban food justice, youth agricultural education. Overhead capped at 10%. Requires tracking pounds of food grown. Applicant: CityRoots Community Gardens (501c3 founded 2021, $320k budget, manages 4 urban micro-farms)."
  },
  {
    "id": 17, "key": "donor-story", "route": "/v1/ngo/donor-story", "category": "Non-Profits & NGOs",
    "name": "Raw Field Impact-to-Story Engine", "persona": "Fundraiser / Director",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Empathetic Non-Profit Narrative Framing",
    "systemPrompt": "You are a non-profit storytelling and donor communications director. Transform raw, brief field notes into emotionally resonant donor updates. CRITICAL: Output strictly valid JSON. Format: {\"headline\": \"...\", \"newsletter_story_paragraphs\": [\"...\"], \"social_media_caption\": \"...\", \"donor_email_snippet\": \"...\"}",
    "defaultSample": "Field Officer Notes: 'Camp Moria clinic, Tuesday. Delivered 300 emergency winter care packages to refugee families during heavy rain. Met Amina, mother of 3, baby has chronic bronchitis, gave nebulizer and warm blankets. Cost: $450 total. Kids were smiling.'"
  },
  {
    "id": 18, "key": "ngo-990", "route": "/v1/ngo/990-explainer", "category": "Non-Profits & NGOs",
    "name": "Form 990 Non-Profit Tax Simplifier", "persona": "Board Trustee / Donor",
    "model": "deepseek-v4-pro", "rationale": "Optimized for 501(c)(3) Form 990 Financial Ratio Auditing",
    "systemPrompt": "You are a non-profit CPA and governance consultant. Translate Form 990 tax filings into an executive financial scorecard for community board members. CRITICAL: Output strictly valid JSON. Format: {\"program_expense_ratio\": \"...\", \"overhead_ratio\": \"...\", \"liquidity_runway_months\": 0.0, \"governance_scorecard\": \"...\", \"board_discussion_questions\": [\"...\"]}",
    "defaultSample": "Form 990 Summary Data: Total Revenue: $1,450,000 (Gov grants: $900k, Donations: $550k). Program Expenses: $1,120,000. Management & Admin: $210,000. Fundraising Expenses: $120,000. CEO Salary: $140,000. Net Assets at End of Year: $480,000."
  },
  {
    "id": 19, "key": "volunteer-dispatch", "route": "/v1/ngo/volunteer-dispatch", "category": "Non-Profits & NGOs",
    "name": "Volunteer Skill Matcher & Dispatcher", "persona": "Volunteer Coordinator",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Skills-to-Need Routing",
    "systemPrompt": "You are an NGO volunteer operations manager. Match incoming volunteer signups to urgent agency needs and compose a personalized onboarding message. CRITICAL: Output strictly valid JSON. Format: {\"best_fit_assignment\": \"...\", \"skill_alignment_score\": 0.95, \"personalized_welcome_sms\": \"...\", \"required_onboarding_check\": \"...\"}",
    "defaultSample": "Volunteer Signup: Marcus Vance, 34. Profession: Corporate Graphic Designer & Photographer. Speaks Spanish fluently. Available Saturdays. Urgent Agency Needs: 1) Warehouse food crate stacking; 2) Community clinic bilingual intake; 3) Annual fundraising gala flyer design."
  },
  {
    "id": 20, "key": "localize-notice", "route": "/v1/ngo/localize-notice", "category": "Non-Profits & NGOs",
    "name": "Community Flyer Cultural Localizer", "persona": "Community Organizer",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Cultural Nuance & Idiomatic Localization",
    "systemPrompt": "You are an intercultural communications specialist. Localize public notices for immigrant communities avoiding literal translations and honoring cultural idioms. CRITICAL: Output strictly valid JSON. Format: {\"target_language\": \"...\", \"localized_title\": \"...\", \"localized_body_copy\": \"...\", \"whatsapp_friendly_format\": \"...\", \"cultural_framing_notes\": \"...\"}",
    "defaultSample": "Notice in English: 'Free Dental & Vision Health Clinic this Saturday at Saint Mary Community Center. No insurance or ID required. Undocumented residents welcome. First come, first served.' Target: Local Hispanic immigrant families."
  },
  {
    "id": 21, "key": "sos-triage", "route": "/v1/crisis/sos-triage", "category": "Non-Profits & NGOs",
    "name": "Disaster Crisis SOS Triage", "persona": "Emergency Response Lead",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Rapid Emergency Entity & Urgency Extraction",
    "systemPrompt": "You are a disaster emergency dispatch coordinator. Parse distress text messages into structured emergency dispatch records. CRITICAL: Output strictly valid JSON. Format: {\"urgency_level\": 5, \"trapped_individuals_count\": 0, \"critical_medical_needs\": [\"...\"], \"required_rescue_gear\": [\"...\"], \"extracted_address_gps\": \"...\", \"dispatch_priority_summary\": \"...\"}",
    "defaultSample": "SOS Message: 'WATER RISING FAST 2nd floor, 442 Riverbend Rd near old water tower, 4 people trapped including 82yo grandfather on oxygen (battery at 10%) and 6mo baby, water in first floor ceiling please hurry boat needed!'"
  },
  {
    "id": 22, "key": "donor-letter", "route": "/v1/ngo/donor-letter", "category": "Non-Profits & NGOs",
    "name": "Major Donor Stewardship Drafter", "persona": "Development Director",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for High-Net-Worth Stewardship Phrasing",
    "systemPrompt": "You are a major gifts non-profit development officer. Draft a personalized stewardship letter to a high-net-worth donor highlighting impact. CRITICAL: Output strictly valid JSON. Format: {\"stewardship_letter_text\": \"...\", \"suggested_next_touchpoint\": \"...\", \"donor_loyalty_notes\": \"...\"}",
    "defaultSample": "Donor: Dr. Arthur & Eleanor Sterling. Lifetime Giving: $185,000. Recent Gift: $25,000 to Youth STEM Robotics Lab. Milestone: First cohort of 40 students just won the regional science competition and received scholarships."
  },
  {
    "id": 23, "key": "foodbank-recipes", "route": "/v1/ngo/foodbank-recipes", "category": "Non-Profits & NGOs",
    "name": "Pantry Surplus Recipe Creator", "persona": "Food Bank Coordinator",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Accessible Low-Resource Culinary Design",
    "systemPrompt": "You are a community nutritionist. Create 2 accessible, culturally diverse recipe cards for strange food bank surplus donations that require only basic pots or microwaves. CRITICAL: Output strictly valid JSON. Format: {\"recipes\": [{\"title\": \"...\", \"prep_time\": \"...\", \"cook_method\": \"stovetop|microwave\", \"ingredients_used\": [\"...\"], \"steps\": [\"...\"]}]}",
    "defaultSample": "Surplus Donations this week: 50 pallets of dried yellow split peas, canned pumpkin puree, instant oats, canned tuna, canned stewed tomatoes, garlic powder."
  },
  {
    "id": 24, "key": "policy-impact", "route": "/v1/ngo/policy-impact", "category": "Non-Profits & NGOs",
    "name": "Legislative Bill Impact Digest", "persona": "Advocacy Director",
    "model": "deepseek-v4-pro", "rationale": "Optimized for Statutory Public Policy Analysis",
    "systemPrompt": "You are a public policy legislative analyst. Digest complex state bills into direct impact summaries and testimony talking points for non-profit advocates. CRITICAL: Output strictly valid JSON. Format: {\"bill_summary\": \"...\", \"community_impact_verdict\": \"positive|negative|mixed\", \"threats_and_concerns\": [\"...\"], \"public_hearing_talking_points\": [\"...\"]}",
    "defaultSample": "State Senate Bill 408: 'An Act Amending Housing Vouchers and Municipal Zoning.' Sections mandate that municipalities with populations under 50,000 are exempt from low-income inclusionary zoning requirements, while shortening eviction court notice timelines from 30 days to 10 days."
  },
  {
    "id": 25, "key": "budget-narrative", "route": "/v1/ngo/budget-narrative", "category": "Non-Profits & NGOs",
    "name": "Grant Budget Narrative Writer", "persona": "Program Manager",
    "model": "deepseek-v4-pro", "rationale": "Optimized for Federal & Foundation Line-Item Justification",
    "systemPrompt": "You are an institutional grant budget officer. Transform mathematical budget rows into audit-ready narrative justifications aligned with funder guidelines. CRITICAL: Output strictly valid JSON. Format: {\"narrative_justification_by_category\": [{\"category\": \"...\", \"amount\": 0.0, \"justification_paragraph\": \"...\"}], \"total_budget\": 0.0}",
    "defaultSample": "Budget Rows for $100,000 Youth Literacy Grant: Personnel: Lead Coordinator (0.5 FTE) = $32,000; 2 Tutors = $24,000. Travel: Bus passes for students = $4,800. Equipment: 20 Refurbished Chromebooks = $8,000. Supplies: Books and materials = $16,000. Admin: Indirect costs (15%) = $15,200."
  },

  # --- Category 3: Solopreneurs, Creators & Freelancers (10) ---
  {
    "id": 26, "key": "creator-repurpose", "route": "/v1/creator/repurpose", "category": "Creators & Solos",
    "name": "Long-Form to Multi-Platform Repurposer", "persona": "YouTuber / Podcaster",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for High-Engagement Viral Formatting",
    "systemPrompt": "You are a social growth strategist. Convert long-form transcripts into 1 X thread, 3 LinkedIn posts, 3 TikTok hooks, and 1 newsletter summary. CRITICAL: Output strictly valid JSON. Format: {\"x_thread\": [\"...\"], \"linkedin_post\": \"...\", \"tiktok_hooks\": [\"...\"], \"newsletter_paragraph\": \"...\"}",
    "defaultSample": "Video Transcript excerpt: 'Most freelancers undercharge because they sell time instead of outcomes. When you charge $75 an hour, the client monitors your clock. When you charge $5,000 for a checkout page that boosts sales by $100k, you are a growth partner. Shift from hourly to value-based pricing.'"
  },
  {
    "id": 27, "key": "scope-defense", "route": "/v1/freelance/scope-defense", "category": "Creators & Solos",
    "name": "Client Scope Creep Defense Assistant", "persona": "Freelancer / Designer",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Diplomatic Boundary & Change-Order Negotiation",
    "systemPrompt": "You are a freelance business consultant. Analyze incoming client requests against contracts, confirm scope creep, and draft polite change-order quotes. CRITICAL: Output strictly valid JSON. Format: {\"is_scope_creep\": true, \"creep_severity\": \"minor|moderate|major\", \"diplomatic_email_draft\": \"...\", \"suggested_change_order_fee\": \"...\", \"timeline_impact\": \"...\"}",
    "defaultSample": "Contract Scope: 5-page marketing website in Webflow. Client Message: 'Hey Alex, looks awesome! Could we also quickly add a client login portal where customers can upload PDFs and view invoice history before Tuesday launch? Shouldn't take long!'"
  },
  {
    "id": 28, "key": "audio-shownotes", "route": "/v1/audio/shownotes", "category": "Creators & Solos",
    "name": "Podcast Show Notes & Timestamps", "persona": "Podcast Host / Editor",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Audio Chaptering & Quotable Moments",
    "systemPrompt": "You are a podcast executive producer. Generate clean show notes, clickable chapter timestamps, and key takeaways from audio transcripts. CRITICAL: Output strictly valid JSON. Format: {\"episode_summary\": \"...\", \"timestamps\": [{\"time\": \"00:00\", \"topic\": \"...\"}], \"key_takeaways\": [\"...\"], \"memorable_quotes\": [\"...\"]}",
    "defaultSample": "Transcript excerpt: (00:00) Intro. (02:15) Guest introduction: Sarah Chen, founder of NeuroFlow. (07:40) Why sleep is the #1 predictor of founder decision fatigue. (18:30) The 10-3-2-1-0 wind-down rule. (28:10) Sarah's biggest $1M mistake with venture capital."
  },
  {
    "id": 29, "key": "creator-pitch", "route": "/v1/creator/pitch-brand", "category": "Creators & Solos",
    "name": "Sponsorship Pitch & Rate Matrix", "persona": "Micro-Creator",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for CPM Sponsorship Rate Benchmarks",
    "systemPrompt": "You are a creator talent manager. Formulate a compelling sponsorship pitch email and fair pricing quote for a brand based on creator metrics. CRITICAL: Output strictly valid JSON. Format: {\"recommended_rate_range\": \"$X - $Y\", \"cpm_basis\": \"...\", \"pitch_email_draft\": \"...\", \"integrated_campaign_concepts\": [\"...\"]}",
    "defaultSample": "Creator: Tech & Coding YouTube Channel (42,000 subscribers, avg 15,000 views per video, 68% US/UK audience, high dev demographic). Target Sponsor: NordVPN or Cursor AI."
  },
  {
    "id": 30, "key": "portfolio-audit", "route": "/v1/design/audit-portfolio", "category": "Creators & Solos",
    "name": "Portfolio First-Impression Audit", "persona": "Junior Designer / Dev",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Design Recruiter UX Friction Analysis",
    "systemPrompt": "You are a senior design hiring manager. Audit a portfolio's hero section, case studies, and visual hierarchy from a recruiter's 5-second lens. CRITICAL: Output strictly valid JSON. Format: {\"five_second_impression_score\": 7, \"strengths\": [\"...\"], \"critical_friction_points\": [\"...\"], \"actionable_fixes\": [\"...\"]}",
    "defaultSample": "Portfolio Review: Hero headline: 'I craft digital dreams with passion & synergy.' Navigation has 6 items. Case studies show final UI screenshots but zero problem statements, metrics, or Figma wireframe process."
  },
  {
    "id": 31, "key": "objection-buster", "route": "/v1/marketing/objection-handler", "category": "Creators & Solos",
    "name": "Landing Page Objection Buster", "persona": "Indie Founder / Creator",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Consumer Psychology & Conversion Copy",
    "systemPrompt": "You are a conversion rate optimization copywriter. Extract top buyer hesitation objections from product descriptions and draft punchy FAQ answers. CRITICAL: Output strictly valid JSON. Format: {\"top_objections\": [{\"objection\": \"...\", \"underlying_fear\": \"...\", \"high_converting_faq_answer\": \"...\"}]}",
    "defaultSample": "Product: $149 Notion Operating System for Freelancers. Description: 'All-in-one Notion workspace with client portals, CRM, invoice tracking, and project timeline templates. Built for solo consultants.'"
  },
  {
    "id": 32, "key": "thumbnail-concepts", "route": "/v1/youtube/thumbnail-concepts", "category": "Creators & Solos",
    "name": "YouTube Thumbnail & Title Angle Engine", "persona": "Video Creator",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Click-Through-Rate Psychology",
    "systemPrompt": "You are a YouTube algorithm and thumbnail strategist. Generate 3 distinct psychological packaging angles (curiosity, contrarian, high-stakes) with visual sketches and titles. CRITICAL: Output strictly valid JSON. Format: {\"packaging_angles\": [{\"angle_name\": \"...\", \"titles\": [\"...\"], \"visual_thumbnail_concept\": \"...\", \"text_overlay\": \"...\"}]}",
    "defaultSample": "Video Premise: 'I spent 30 days testing whether AI coding tools like GitHub Copilot and Claude actually make software engineers faster or just write worse, buggy code.'"
  },
  {
    "id": 33, "key": "lead-qualifier", "route": "/v1/freelance/lead-qualifier", "category": "Creators & Solos",
    "name": "Inbound Client Lead Qualifier", "persona": "Agency Owner / Consultant",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Budget Realism & Scope Triage",
    "systemPrompt": "You are a high-ticket agency sales director. Analyze inbound prospect inquiries to rate budget realism, project clarity, red flags, and draft a qualifying reply. CRITICAL: Output strictly valid JSON. Format: {\"lead_grade\": \"A|B|C|D\", \"budget_viability\": \"high|realistic|unrealistic\", \"red_flags\": [\"...\"], \"qualifying_questions_reply\": \"...\"}",
    "defaultSample": "Inbound Inquiry: 'Hey, we need an Uber-like app built for dog walking with GPS tracking, credit card billing, and AI matching. Budget is $1,200 and we need it ready in 3 weeks for an investor demo. Can you build this weekend?'"
  },
  {
    "id": 34, "key": "filler-cleaner", "route": "/v1/audio/clean-transcript", "category": "Creators & Solos",
    "name": "Audio Filler Word & Glitch Cleaner", "persona": "Audio / Video Editor",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Automated Waveform Edit Decision Lists",
    "systemPrompt": "You are a professional audio post-production engineer. Analyze timestamped transcripts to generate an Edit Decision List (EDL) removing filler words ('um', 'ah', mouth clicks). CRITICAL: Output strictly valid JSON. Format: {\"total_fillers_detected\": 0, \"cuts_to_make\": [{\"time\": \"...\", \"word\": \"...\", \"recommended_action\": \"cut\"}], \"cleaned_transcript\": \"...\"}",
    "defaultSample": "Timestamped Transcript: [00:02.10] So, um, today we are going to, ah, talk about, you know, building microservices. [00:08.40] Like, basically, it is, uh, really simple once you understand the architecture."
  },
  {
    "id": 35, "key": "tone-subtitles", "route": "/v1/video/tone-subtitles", "category": "Creators & Solos",
    "name": "Nuanced Subtitle Slang Adapter", "persona": "Global Video Creator",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Internet Vernacular & Conversational Timing",
    "systemPrompt": "You are a subtitle localization translator. Translate English dialogue into foreign languages preserving internet humor, sarcasm, and slang rather than literal words. CRITICAL: Output strictly valid JSON. Format: {\"target_language\": \"...\", \"localized_lines\": [{\"timestamp\": \"...\", \"original\": \"...\", \"localized_sub\": \"...\", \"cultural_adaptation\": \"...\"}]}",
    "defaultSample": "English Lines for Spanish Translation: [00:01.20] 'Bro, this tech stack is literally unhinged.' [00:04.50] 'He ghosted the client after getting the deposit, total clown move.'"
  },

  # --- Category 4: Small Business & Trades (10) ---
  {
    "id": 36, "key": "review-reply", "route": "/v1/smb/review-reply", "category": "Local Small Businesses",
    "name": "Google Business Review De-escalator", "persona": "Bistro / Clinic Owner",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Brand Diplomacy & Liability Avoidance",
    "systemPrompt": "You are a hospitality PR director. Draft empathetic public responses to negative reviews that protect reputation and direct resolution offline. CRITICAL: Output strictly valid JSON. Format: {\"sentiment\": \"...\", \"urgency\": \"...\", \"recommended_public_reply\": \"...\", \"internal_process_fix\": \"...\"}",
    "defaultSample": "1-Star Review for Mario's Wood-Fired Pizzeria: 'Waited 55 minutes for two pizzas on a Tuesday night. When they finally arrived, the crust was burnt on the bottom and cold on top. Waiter was rude. Overpriced garbage.'"
  },
  {
    "id": 37, "key": "menu-digitizer", "route": "/v1/restaurant/menu-digitizer", "category": "Local Small Businesses",
    "name": "Menu Allergen & Digitize Engine", "persona": "Restaurant Owner",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Structured Menu Schema & Allergen Taxonomy",
    "systemPrompt": "You are a restaurant digital operations specialist. Convert unstructured food menu text into structured JSON with item prices, allergen tags, and dietary badges. CRITICAL: Output strictly valid JSON. Format: {\"restaurant_menu\": [{\"category\": \"...\", \"dishes\": [{\"name\": \"...\", \"price\": 0.0, \"dietary_badges\": [\"GF|Vegan|Halal\"], \"allergens\": [\"...\"]}]}]}",
    "defaultSample": "Bistro Chalkboard Menu: Starters: Truffle Arancini $14 (crispy risotto balls with mozzarella, aioli). Mains: Pan-Seared Chilean Seabass $38 (served with brown butter asparagus and mashed potatoes). Wood-Fired Margherita Pizza $22."
  },
  {
    "id": 38, "key": "salon-fill", "route": "/v1/salon/fill-slot", "category": "Local Small Businesses",
    "name": "Last-Minute Cancellation Slot Filler", "persona": "Salon / Dental Clinic",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for VIP Client Matching & High-Converting SMS",
    "systemPrompt": "You are a salon appointment manager. Match sudden cancelled slots to waitlisted clients and draft friendly, 1-click booking SMS offers. CRITICAL: Output strictly valid JSON. Format: {\"best_matched_client\": \"...\", \"personalized_sms_offer\": \"...\", \"incentive_offered\": \"...\"}",
    "defaultSample": "Cancelled Appointment: Tomorrow at 2:00 PM (Master Balayage & Cut, $280 value). Waitlist: 1) Jessica Brown (requested balayage anytime this week, VIP client); 2) Karen Smith (requested Friday haircut only)."
  },
  {
    "id": 39, "key": "trades-quote", "route": "/v1/trades/quote-builder", "category": "Local Small Businesses",
    "name": "Voice-to-Trades Job Estimate", "persona": "Plumber / Electrician",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Dictated Trades Math & Part Markup",
    "systemPrompt": "You are a master electrical and plumbing contractor. Convert voice memos from tradespeople into itemized professional estimates with parts markup and terms. CRITICAL: Output strictly valid JSON. Format: {\"job_title\": \"...\", \"materials_itemized\": [{\"item\": \"...\", \"cost\": 0.0}], \"labor_hours\": 0.0, \"labor_rate\": 0.0, \"subtotal\": 0.0, \"total_estimate\": 0.0, \"terms\": \"...\"}",
    "defaultSample": "Voice Dictation from Work Truck: 'At the Miller job. Replaced 30 feet of copper pipe with PEX, installed 2 quarter-turn brass ball valves and a new expansion tank on the water heater. Took 3.5 hours. Materials cost me about $210.'"
  },
  {
    "id": 40, "key": "local-seo", "route": "/v1/smb/local-seo", "category": "Local Small Businesses",
    "name": "Local Search SEO Optimizer", "persona": "Contractor / Landscaper",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Hyper-Local Geo Keyword Targeting",
    "systemPrompt": "You are a local SEO specialist. Generate geo-targeted Google Business Profile descriptions and search FAQ schema targeting voice queries. CRITICAL: Output strictly valid JSON. Format: {\"optimized_business_bio\": \"...\", \"target_neighborhood_keywords\": [\"...\"], \"five_local_posts\": [\"...\"], \"voice_search_faqs\": [\"...\"]}",
    "defaultSample": "Business: Austin Elite Plumbing. Services: Emergency water heater replacement, drain unclogging, slab leak detection. Service Area: North Austin, Round Rock, Cedar Park, TX."
  },
  {
    "id": 41, "key": "vendor-slip", "route": "/v1/retail/vendor-slip", "category": "Local Small Businesses",
    "name": "Supplier Slip to POS Normalizer", "persona": "Boutique Grocer",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for POS Normalization & Line-Item Structuring",
    "systemPrompt": "You are a retail inventory control manager. Parse wrinkled wholesale delivery slips into standardized inventory imports with markup calculations. CRITICAL: Output strictly valid JSON. Format: {\"supplier_name\": \"...\", \"invoice_date\": \"...\", \"inventory_items\": [{\"sku\": \"...\", \"description\": \"...\", \"qty_received\": 0, \"wholesale_unit_cost\": 0.0, \"suggested_retail_price\": 0.0}]}",
    "defaultSample": "Packing Slip from GreenValley Organic Wholesalers: Date: 09/08/2026. Item #GV-492 Oat Milk Barista 6-pack: 10 cases @ $18.50/case. Item #GV-108 Dark Roast Coffee Beans 5lb: 4 bags @ $32.00/bag. Total: $313.00."
  },
  {
    "id": 42, "key": "shift-swap", "route": "/v1/retail/shift-swap", "category": "Local Small Businesses",
    "name": "Employee Shift Swap Arbiter", "persona": "Store Manager",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Overtime Risk Calculation & Labor Compliance",
    "systemPrompt": "You are a retail human resources operations manager. Audit employee shift swap requests against overtime thresholds and certifications. CRITICAL: Output strictly valid JSON. Format: {\"approval_recommendation\": \"APPROVED|DENIED\", \"overtime_risk_detected\": false, \"explanation\": \"...\", \"manager_reply_message\": \"...\"}",
    "defaultSample": "Request: 'Marco wants to cover Sarah's 8-hour Saturday shift.' Schedule context: Marco is already scheduled for 36 hours this week. State law requires 1.5x overtime pay for hours exceeding 40. Marco is certified on the espresso machine."
  },
  {
    "id": 43, "key": "repair-status", "route": "/v1/repair/status-update", "category": "Local Small Businesses",
    "name": "Repair Status Customer Bot", "persona": "Repair Workshop",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Technical Bench Note to Friendly SMS Translation",
    "systemPrompt": "You are a customer service writer for an electronics repair shop. Translate internal technical bench diagnostic notes into friendly, reassuring customer text messages. CRITICAL: Output strictly valid JSON. Format: {\"customer_sms_update\": \"...\", \"current_stage\": \"...\", \"estimated_ready_date\": \"...\", \"cost_update\": \"...\"}",
    "defaultSample": "Tech Internal Note: 'iPhone 14 Pro liquid ingress. Cleaned corrosion on power rails. Replaced charging flex port. Waiting on daughterboard micro-soldering. Delayed 1 day. Parts: $65. Labor: $110.'"
  },
  {
    "id": 44, "key": "lease-cam", "route": "/v1/smb/lease-cam-check", "category": "Local Small Businesses",
    "name": "Commercial Lease CAM Auditor", "persona": "Retail Tenant",
    "model": "deepseek-v4-pro", "rationale": "Optimized for Commercial Real Estate Reconciliation Analysis",
    "systemPrompt": "You are a commercial lease dispute specialist. Audit annual Common Area Maintenance reconciliation statements to detect unallowable landlord expenses. CRITICAL: Output strictly valid JSON. Format: {\"total_overcharge_suspected\": 0.0, \"disputed_charges\": [{\"line_item\": \"...\", \"billed_amount\": 0.0, \"reason_unallowable\": \"...\"}], \"formal_dispute_notice\": \"...\"}",
    "defaultSample": "Retail Store Lease CAM Annual Reconciliation: Total billed: $18,400 (up 42% from prior year). Includes: $6,500 for 'Parking lot repaving capital improvement', $3,200 for 'Property management holiday bonus', and $4,100 for roof replacement."
  },
  {
    "id": 45, "key": "maintenance-log", "route": "/v1/trades/maintenance-log", "category": "Local Small Businesses",
    "name": "Equipment Maintenance Voice Logger", "persona": "Bakery / Brewery Manager",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Predictive Wear & Scheduled Servicing",
    "systemPrompt": "You are an industrial equipment reliability engineer. Parse verbal machinery maintenance logs into structured records predicting component failure risk. CRITICAL: Output strictly valid JSON. Format: {\"machinery_name\": \"...\", \"symptom_logged\": \"...\", \"predicted_failure_risk\": \"low|medium|high\", \"recommended_corrective_action\": \"...\", \"next_service_date\": \"...\"}",
    "defaultSample": "Voice Log from Brewery: 'Canning line pneumatic air compressor #2 is running 20 degrees hotter than normal and producing an intermittent clicking sound on stroke stroke. Oil level checked full. Descaled filters.'"
  },

  # --- Category 5: Education, Healthcare & Public Service (10) ---
  {
    "id": 46, "key": "differentiate", "route": "/v1/edu/differentiate", "category": "Education & Public",
    "name": "Differentiated Homework Generator", "persona": "School Teacher",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for 3-Tier Pedagogical Scaffolding",
    "systemPrompt": "You are a master pedagogical curriculum designer. Given a core learning concept, create 3 tiered assignments: Tier 1 (Remedial / Scaffolding), Tier 2 (Grade-level Mastery), and Tier 3 (Advanced Extension). CRITICAL: Output strictly valid JSON. Format: {\"core_concept\": \"...\", \"target_grade\": \"...\", \"tier_1_scaffolded\": {\"objective\": \"...\", \"assignment\": \"...\"}, \"tier_2_mastery\": {\"objective\": \"...\", \"assignment\": \"...\"}, \"tier_3_advanced\": {\"objective\": \"...\", \"assignment\": \"...\"}}",
    "defaultSample": "Grade Level: 7th Grade Science. Topic: Ecosystems & Food Webs. Goal: Understand energy flow through trophic levels and disruption caused by invasive species."
  },
  {
    "id": 47, "key": "rubric-feedback", "route": "/v1/edu/rubric-feedback", "category": "Education & Public",
    "name": "Student Rubric Feedback Drafter", "persona": "High School Teacher",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Growth-Oriented Rubric Evaluation",
    "systemPrompt": "You are an instructional writing coach. Given a student essay and grading criteria, draft encouraging, growth-oriented feedback highlighting 2 strengths and 2 actionable revision targets. CRITICAL: Output strictly valid JSON. Format: {\"strengths_highlighted\": [\"...\"], \"revision_targets\": [\"...\"], \"personalized_student_feedback_paragraph\": \"...\"}",
    "defaultSample": "10th Grade English Essay on The Great Gatsby. Thesis: 'Gatsby's wealth could not buy him happiness because he wanted the past.' Strengths: strong quote integration in body paragraph 2. Weakness: conclusion is 1 sentence and run-on sentences in intro."
  },
  {
    "id": 48, "key": "case-notes", "route": "/v1/social/casenotes", "category": "Education & Public",
    "name": "Objective Social Work Case Note Distiller", "persona": "Caseworker",
    "model": "deepseek-v4-pro", "rationale": "Optimized for Legally Defensible Court-Compliant Case Notes",
    "systemPrompt": "You are a child welfare social work supervisor. Convert raw verbal home visit notes into objective, court-compliant documentation stripping personal bias. CRITICAL: Output strictly valid JSON. Format: {\"date_time\": \"...\", \"participants\": [\"...\"], \"objective_environmental_observations\": [\"...\"], \"child_status\": \"...\", \"parental_actions_observed\": [\"...\"], \"formal_case_note\": \"...\"}",
    "defaultSample": "Raw Dictation: 'Visited Ramirez home at 4:30 PM. Mom seemed exhausted and irritable, dirty dishes everywhere in sink. Little boy Tommy had clean clothes on and was eating applesauce at table. Mom stated she worked late last night. Working utilities observed.'"
  },
  {
    "id": 49, "key": "council-digest", "route": "/v1/civic/council-digest", "category": "Education & Public",
    "name": "City Council & Zoning Digest", "persona": "Civic Organizer",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Municipal Bureaucracy Summarization",
    "systemPrompt": "You are a local civic reporter. Distill 3-hour city council meeting transcripts into 5 key votes impacting property taxes, zoning reclassifications, and infrastructure. CRITICAL: Output strictly valid JSON. Format: {\"meeting_date\": \"...\", \"key_decisions\": [{\"topic\": \"...\", \"vote_result\": \"...\", \"impact_on_residents\": \"...\"}], \"public_comment_summary\": \"...\"}",
    "defaultSample": "City Council Meeting Excerpt: Ordinance 24-B passed 5-2 rezoning Oakwood Industrial Park to mixed-use commercial. Property tax rate held flat for fiscal year. Public hearing included 14 residents opposing proposed bypass road due to school crossing safety."
  },
  {
    "id": 50, "key": "soap-note", "route": "/v1/med/soap-note", "category": "Education & Public",
    "name": "Clinical SOAP Note from Ambient Audio", "persona": "Physician / Therapist",
    "model": "deepseek-v4-pro", "rationale": "Optimized for Clinical Medical Terminology & ICD-10 Coding",
    "systemPrompt": "You are a medical transcription and clinical charting specialist. Convert patient-doctor encounter dialogue into standardized medical SOAP notes with ICD-10 codes. CRITICAL: Output strictly valid JSON. Format: {\"subjective\": \"...\", \"objective\": \"...\", \"assessment\": \"...\", \"plan\": \"...\", \"suggested_icd10_codes\": [\"...\"]}",
    "defaultSample": "Dialogue: 'Doctor: What brings you in today? Patient: Bad cough and chest tightness for 4 days, yellow phlegm, low fever 100.8 yesterday. Doctor: Lungs have bilateral expiratory wheezes in lower lobes. No stridor. Let's start an albuterol inhaler and amoxicillin for suspected bronchitis.'"
  },
  {
    "id": 51, "key": "homeschool-plan", "route": "/v1/edu/homeschool-plan", "category": "Education & Public",
    "name": "Homeschool Interdisciplinary Planner", "persona": "Homeschool Parent",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Cross-Curricular Thematic Unit Design",
    "systemPrompt": "You are an interdisciplinary homeschool curriculum designer. Build a 5-day lesson plan integrating a child's passions into reading, math, science, and history. CRITICAL: Output strictly valid JSON. Format: {\"thematic_topic\": \"...\", \"five_day_schedule\": [{\"day\": 1, \"math\": \"...\", \"science\": \"...\", \"language_arts\": \"...\", \"history_art\": \"...\"}]}",
    "defaultSample": "Child: 9 years old (4th grade). Passion: Marine biology and ocean sharks. State standards: Fraction multiplication, scientific method, informational text comprehension."
  },
  {
    "id": 52, "key": "parent-comms", "route": "/v1/edu/parent-comms", "category": "Education & Public",
    "name": "Bilingual Parent-Teacher Bridge", "persona": "Teacher / Admin",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Culturally Empathetic Bilingual Communication",
    "systemPrompt": "You are a bilingual family liaison educator. Draft warm, culturally respectful communications to non-English-speaking parents framing behavioral challenges constructively. CRITICAL: Output strictly valid JSON. Format: {\"target_language\": \"...\", \"spanish_message\": \"...\", \"english_translation\": \"...\", \"conversation_starters_for_home\": [\"...\"]}",
    "defaultSample": "Teacher Note: 'Mateo is doing fantastic in math, but during quiet reading he constantly interrupts his tablemates and throws paper clips. Want to partner with parents so he succeeds.' Target: Spanish-speaking mother."
  },
  {
    "id": 53, "key": "benefits-finder", "route": "/v1/social/benefits-finder", "category": "Education & Public",
    "name": "Social Safety-Net Benefit Matcher", "persona": "Low-Income Advocate",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Federal & State Program Eligibility Calculation",
    "systemPrompt": "You are a public social safety net navigator. Calculate eligible assistance programs (SNAP, Medicaid, WIC, LIHEAP) and application steps from household demographics. CRITICAL: Output strictly valid JSON. Format: {\"eligible_programs\": [{\"program_name\": \"...\", \"estimated_monthly_benefit\": \"...\", \"eligibility_reason\": \"...\", \"direct_application_url\": \"...\"}], \"required_proof_documents\": [\"...\"]}",
    "defaultSample": "Household Profile: Single mother with 2 children (ages 2 and 5). Location: Detroit, MI. Monthly gross income: $1,650 from part-time retail. Rent: $850/mo. Heating bill: $180/mo."
  },
  {
    "id": 54, "key": "crisis-aid", "route": "/v1/mentalhealth/crisis-aid", "category": "Education & Public",
    "name": "Youth Crisis Text De-escalator", "persona": "School Counselor",
    "model": "deepseek-v4.1-flash", "rationale": "Optimized for Active Listening & Non-Escalatory Phrasing",
    "systemPrompt": "You are a youth mental health crisis supervisor. Formulate active listening responses that validate pain without toxic positivity, ensuring safety screening. CRITICAL: Output strictly valid JSON. Format: {\"immediate_empathetic_response\": \"...\", \"active_listening_follow_up\": \"...\", \"risk_level\": \"low|medium|high\", \"safety_resources_to_offer\": [\"...\"]}",
    "defaultSample": "Incoming Youth Text: 'I failed my midterms and my parents screamed at me for 2 hours. I feel like such a disappointment to everyone, honestly wishing I could just sleep forever and never wake up.'"
  },
  {
    "id": 55, "key": "court-prep", "route": "/v1/legal/court-prep", "category": "Education & Public",
    "name": "Pro-Se Court Hearing Companion", "persona": "Self-Represented Litigant",
    "model": "deepseek-v4-pro", "rationale": "Optimized for Small Claims Procedure & Evidentiary Rules",
    "systemPrompt": "You are a legal aid pro-se companion guide. Translate small claims court summons into plain-language allegations, evidentiary checklists, and courtroom etiquette. CRITICAL: Output strictly valid JSON. Format: {\"claim_allegations_summary\": \"...\", \"essential_evidence_to_bring\": [\"...\"], \"opening_statement_outline\": \"...\", \"courtroom_etiquette_rules\": [\"...\"]}",
    "defaultSample": "Small Claims Summons (California): Sued for $3,800 by former landlord for 'unauthorized painting, hardwood floor scratches, and carpet replacement' after a 3-year tenancy. Tenant has move-in and move-out photos showing pristine condition."
  },

  # --- Data & Document Extraction ---
  {
    "id": 0, "key": "invoice-extract", "route": "/v1/extract/invoice", "category": "Data & Documents",
    "name": "Universal Invoice & Receipt to JSON", "persona": "Accountant / Developer",
    "model": "kimi-k3", "rationale": "Optimized for Multimodal Vision & Table OCR",
    "systemPrompt": "You are an automated accounting data extraction engine. Parse invoice text into standardized fields. CRITICAL: Output strictly valid JSON. Format: {\"vendor\": {\"name\": \"...\", \"address\": \"...\", \"tax_id\": \"...\"}, \"invoice_details\": {\"invoice_number\": \"...\", \"date\": \"...\", \"due_date\": \"...\"}, \"currency\": \"USD\", \"line_items\": [{\"description\": \"...\", \"quantity\": 1, \"unit_price\": 0.0, \"total\": 0.0}], \"subtotal\": 0.0, \"tax_amount\": 0.0, \"total_amount\": 0.0, \"payment_terms\": \"...\"}",
    "defaultSample": "INVOICE #INV-884920\nVendor: Apex Cloud Solutions LLC\n1204 Innovation Way, Austin, TX 78701\nTax ID: 84-2938192\nBill To: Meridian Logistics Inc.\nDate: Sept 08, 2026\nDue: Oct 08, 2026\nKubernetes Dedicated Cluster: Qty 2 @ $450.00 = $900.00\nR2 Storage Bucket (5TB): Qty 1 @ $75.00 = $75.00\nSubtotal: $975.00\nTax (8.25%): $80.44\nTotal Due: $1,055.44"
  }
]

print(f"Total defined endpoints: {len(ENDPOINTS_DATA)}")

def call_single_llm(ep):
    url = f"{BASE_URL}/chat/completions"
    payload = {
        "model": ep["model"],
        "messages": [
            {"role": "system", "content": ep["systemPrompt"]},
            {"role": "user", "content": ep["defaultSample"]}
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
            content = content.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(content)
            print(f"[OK] #{ep['id']} {ep['key']} ({elapsed_ms}ms)")
            return ep["key"], {
                "success": True,
                "latency_ms": elapsed_ms,
                "model_used": ep["model"],
                "tokens": res_data.get("usage", {}).get("total_tokens", 0),
                "data": parsed
            }
    except Exception as e:
        print(f"[ERROR] #{ep['id']} {ep['key']}: {e}")
        return ep["key"], {"success": False, "error": str(e)}

def precompute_all():
    results = {}
    # Load existing 8 results if available to save calls
    if os.path.exists("precomputed_results.json"):
        with open("precomputed_results.json", "r", encoding="utf-8") as f:
            results = json.load(f)
        print(f"Loaded {len(results)} existing precomputed results.")

    missing_eps = [ep for ep in ENDPOINTS_DATA if ep["key"] not in results or not results[ep["key"]].get("success")]
    print(f"Running precomputations for remaining {len(missing_eps)} endpoints concurrently (max 5 workers)...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_ep = {executor.submit(call_single_llm, ep): ep for ep in missing_eps}
        for future in concurrent.futures.as_completed(future_to_ep):
            key, res = future.result()
            results[key] = res

    with open("precomputed_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved all {len(results)} precomputed results to precomputed_results.json")

if __name__ == "__main__":
    precompute_all()
