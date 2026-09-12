import json
import re
import os
import subprocess

from generate_all_endpoints import ENDPOINTS_DATA

# Friendly Metadata for all 56 Endpoints (Non-Developer, Human-First)
FRIENDLY_METADATA = {
    # 1-15: Health, Family & Consumers
    "explain-lab": {
        "title": "Medical Lab Report Explainer",
        "human_desc": "Translates frightening blood test numbers into simple, reassuring explanations with 3 questions to ask your doctor.",
        "icon": "fa-heart-pulse",
        "color": "rose",
        "tag": "Health & Body",
        "badge": "Patient Peace of Mind",
        "action": "Explain My Blood Test",
        "human_cat": "health"
    },
    "lease-check": {
        "title": "Apartment Lease Red-Flag Auditor",
        "human_desc": "Scans your rental lease for unfair repair fees, illegal eviction rules, and hidden move-out penalty traps.",
        "icon": "fa-file-contract",
        "color": "amber",
        "tag": "Tenant Rights",
        "badge": "Save Security Deposit",
        "action": "Audit My Rental Lease",
        "human_cat": "legal"
    },
    "scam-detector": {
        "title": "Elder Scam & Phishing Defender",
        "human_desc": "Checks suspicious text messages, fake bank alerts, and urgent emails to tell you immediately if it is a scam.",
        "icon": "fa-shield-halved",
        "color": "red",
        "tag": "Scam Defense",
        "badge": "99% Fraud Protection",
        "action": "Check If This Is A Scam",
        "human_cat": "safety"
    },
    "auto-quote": {
        "title": "Car Mechanic Quote Sanity Checker",
        "human_desc": "Identifies price gouging and flags unnecessary fluid flushes so you only pay for what your car actually needs.",
        "icon": "fa-wrench",
        "color": "blue",
        "tag": "Consumer Protection",
        "badge": "Avoid Mechanic Rip-Offs",
        "action": "Verify Mechanic Quote",
        "human_cat": "legal"
    },
    "fee-audit": {
        "title": "Subscription & Hidden Fee Hunter",
        "human_desc": "Scans bank statements for forgotten gym memberships, quiet price hikes, and sneaky recurring charges.",
        "icon": "fa-receipt",
        "color": "emerald",
        "tag": "Money Saver",
        "badge": "Save $300+/Year",
        "action": "Find Hidden Subscriptions",
        "human_cat": "safety"
    },
    "ingredient-alert": {
        "title": "Food Allergen & Additive Scanner",
        "human_desc": "Identifies hidden dairy, gluten, nuts, and hazardous chemicals disguised under confusing chemical food codes.",
        "icon": "fa-bowl-food",
        "color": "orange",
        "tag": "Allergy Safety",
        "badge": "Family Allergy Shield",
        "action": "Scan Food Ingredients",
        "human_cat": "health"
    },
    "ticket-appeal": {
        "title": "Parking Ticket & Tow Appeal Drafter",
        "human_desc": "Drafts formal municipal dispute letters citing ambiguous street signs, broken meters, or unclear curb paint.",
        "icon": "fa-square-parking",
        "color": "indigo",
        "tag": "Dispute Fines",
        "badge": "Beat Unfair Tickets",
        "action": "Draft Ticket Appeal",
        "human_cat": "legal"
    },
    "insurance-appeal": {
        "title": "Insurance Denial Fighter",
        "human_desc": "Generates forceful appeal letters citing clinical policy clauses and prompt-pay laws when insurance denies your claim.",
        "icon": "fa-hand-holding-medical",
        "color": "purple",
        "tag": "Insurance Claims",
        "badge": "Overturn Claim Denials",
        "action": "Fight Insurance Denial",
        "human_cat": "legal"
    },
    "iep-analyzer": {
        "title": "Special-Ed IEP Plan Decoder",
        "human_desc": "Breaks down 40-page school special-education accommodations so parents know exactly what support their child is owed.",
        "icon": "fa-graduation-cap",
        "color": "cyan",
        "tag": "Child Education",
        "badge": "Parent Advocacy",
        "action": "Decode IEP Document",
        "human_cat": "health"
    },
    "fridge-chef": {
        "title": "Zero-Waste Fridge-to-Dinner Chef",
        "human_desc": "Turns whatever random leftovers and half-empty veggies are sitting in your fridge into an easy, delicious dinner.",
        "icon": "fa-kitchen-set",
        "color": "lime",
        "tag": "Zero Waste",
        "badge": "Stop Food Waste",
        "action": "Make Dinner From Fridge",
        "human_cat": "health"
    },
    "appliance-fix": {
        "title": "Appliance Error Code Decryptor",
        "human_desc": "Translates cryptic washing machine and dishwasher error beeps into plain DIY fixes before calling a $200 repairman.",
        "icon": "fa-screwdriver-wrench",
        "color": "teal",
        "tag": "Home DIY",
        "badge": "Save Repair Callout",
        "action": "Fix Appliance Error",
        "human_cat": "business"
    },
    "bill-optimizer": {
        "title": "Home Electricity Bill Optimizer",
        "human_desc": "Compares peak and off-peak energy rates to show you the cheapest hours to run heavy laundry and heating.",
        "icon": "fa-bolt",
        "color": "amber",
        "tag": "Energy Bills",
        "badge": "Cut Electric Bill",
        "action": "Optimize Electric Bill",
        "human_cat": "health"
    },
    "transition-map": {
        "title": "Career Switcher Skill Crosswalk",
        "human_desc": "Translates your past work experience into modern resume buzzwords for high-growth tech or green industry roles.",
        "icon": "fa-compass",
        "color": "blue",
        "tag": "Career Switch",
        "badge": "Career Upgrade",
        "action": "Map My Career Switch",
        "human_cat": "business"
    },
    "parenting-coach": {
        "title": "Child Tantrum & Conflict Coach",
        "human_desc": "Gives stressed parents calm, gentle phrasing to de-escalate toddler tantrums and bedtime battles without yelling.",
        "icon": "fa-children",
        "color": "pink",
        "tag": "Parenting",
        "badge": "Calm Household",
        "action": "Get Parenting Advice",
        "human_cat": "health"
    },
    "warranty-claim": {
        "title": "Statutory Warranty Dispute Drafter",
        "human_desc": "Drafts assertive consumer demand letters when a seller refuses to replace or refund a defective product.",
        "icon": "fa-scale-balanced",
        "color": "indigo",
        "tag": "Consumer Rights",
        "badge": "Get Your Refund",
        "action": "Demand Warranty Replacement",
        "human_cat": "legal"
    },

    # 16-25: Non-Profits, NGOs & Community
    "grant-match": {
        "title": "Non-Profit Grant Criteria Matcher",
        "human_desc": "Screens 50-page foundation grant RFPs in seconds to verify if your charity qualifies before you waste weeks applying.",
        "icon": "fa-handshake-angle",
        "color": "indigo",
        "tag": "Grants & NPO",
        "badge": "Save 40+ Staff Hours",
        "action": "Check Grant Eligibility",
        "human_cat": "community"
    },
    "donor-story": {
        "title": "Field Impact Story Engine",
        "human_desc": "Turns raw staff field notes and messy quotes into moving, emotional stories that inspire donors to give.",
        "icon": "fa-heart",
        "color": "rose",
        "tag": "Fundraising",
        "badge": "Boost Donations",
        "action": "Create Donor Story",
        "human_cat": "community"
    },
    "ngo-990": {
        "title": "Charity Tax Form 990 Simplifier",
        "human_desc": "Translates confusing non-profit tax disclosures into clear board summaries showing overhead and program ratios.",
        "icon": "fa-file-invoice",
        "color": "slate",
        "tag": "Charity Audit",
        "badge": "Board Governance",
        "action": "Explain Form 990",
        "human_cat": "community"
    },
    "volunteer-dispatch": {
        "title": "Volunteer Skill Matcher",
        "human_desc": "Instantly matches community volunteers to specific tasks based on their schedules, languages, and driving abilities.",
        "icon": "fa-users-gear",
        "color": "emerald",
        "tag": "Volunteer Ops",
        "badge": "Seamless Coordination",
        "action": "Match Volunteers",
        "human_cat": "community"
    },
    "localize-notice": {
        "title": "Community Flyer Cultural Localizer",
        "human_desc": "Adapts neighborhood clinic and food bank notices into culturally respectful Spanish, Vietnamese, or Arabic.",
        "icon": "fa-language",
        "color": "cyan",
        "tag": "Community Outreach",
        "badge": "Cultural Empathy",
        "action": "Localize Community Notice",
        "human_cat": "community"
    },
    "sos-triage": {
        "title": "Disaster Relief SOS Triage",
        "human_desc": "Categorizes emergency flood or storm citizen text messages by urgency, required rescue gear, and GPS locations.",
        "icon": "fa-truck-medical",
        "color": "red",
        "tag": "Emergency Relief",
        "badge": "Fastest Dispatch",
        "action": "Triage Emergency Messages",
        "human_cat": "community"
    },
    "donor-letter": {
        "title": "Major Donor Thank-You Drafter",
        "human_desc": "Drafts deeply personal stewardship letters celebrating major benefactors without sounding like a robotic form letter.",
        "icon": "fa-envelope-open-text",
        "color": "amber",
        "tag": "Stewardship",
        "badge": "Donor Retention",
        "action": "Draft Thank-You Letter",
        "human_cat": "community"
    },
    "foodbank-recipes": {
        "title": "Pantry Surplus Recipe Creator",
        "human_desc": "Creates simple, microwave-friendly recipes in multiple languages using bulk surplus foods like beans and squash.",
        "icon": "fa-wheat-awn",
        "color": "emerald",
        "tag": "Food Pantry",
        "badge": "Dignified Nutrition",
        "action": "Generate Pantry Recipe",
        "human_cat": "community"
    },
    "policy-impact": {
        "title": "Legislative Bill Impact Digest",
        "human_desc": "Summarizes 200-page state and city bills into 3 talking points for community leaders giving public hearing testimony.",
        "icon": "fa-landmark",
        "color": "blue",
        "tag": "Civic Voice",
        "badge": "Civic Transparency",
        "action": "Digest Policy Bill",
        "human_cat": "community"
    },
    "budget-narrative": {
        "title": "Grant Budget Narrative Writer",
        "human_desc": "Translates numbers on an Excel budget sheet into an audit-ready, compelling narrative for federal grant applications.",
        "icon": "fa-calculator",
        "color": "purple",
        "tag": "Grant Accounting",
        "badge": "Win Institutional Funding",
        "action": "Write Budget Narrative",
        "human_cat": "community"
    },

    # 26-35: Freelance, Work & Creators
    "creator-repurpose": {
        "title": "1-to-10 Content Repurposer",
        "human_desc": "Takes one long YouTube video or podcast transcript and transforms it into Twitter threads, LinkedIn posts, and newsletter tips.",
        "icon": "fa-share-nodes",
        "color": "indigo",
        "tag": "Solo Work",
        "badge": "10x Reach",
        "action": "Repurpose Content",
        "human_cat": "business"
    },
    "scope-defense": {
        "title": "Freelance Scope-Creep Defense",
        "human_desc": "Politely and firmly reminds demanding clients that extra work requires an added fee without ruining the relationship.",
        "icon": "fa-shield-cat",
        "color": "amber",
        "tag": "Freelance",
        "badge": "Protect Your Rates",
        "action": "Draft Scope Defense",
        "human_cat": "business"
    },
    "audio-shownotes": {
        "title": "Podcast Timestamps & Show Notes",
        "human_desc": "Creates clickable episode timestamps, guest takeaways, and sponsor links from rough audio recordings in seconds.",
        "icon": "fa-microphone-lines",
        "color": "purple",
        "tag": "Podcasting",
        "badge": "Save 2 Hours Per Episode",
        "action": "Generate Show Notes",
        "human_cat": "business"
    },
    "creator-pitch": {
        "title": "Brand Sponsorship Pitch & Rates",
        "human_desc": "Calculates fair CPM sponsorship pricing and drafts compelling pitch emails to landing lucrative brand deals.",
        "icon": "fa-bullhorn",
        "color": "pink",
        "tag": "Brand Deals",
        "badge": "Get Paid What You're Worth",
        "action": "Calculate Sponsorship Rate",
        "human_cat": "business"
    },
    "portfolio-audit": {
        "title": "Design Portfolio 5-Second Audit",
        "human_desc": "Reviews your freelance portfolio from a hiring manager's perspective to fix weak case studies and missing callouts.",
        "icon": "fa-laptop-code",
        "color": "blue",
        "tag": "Freelance Design",
        "badge": "Land More Clients",
        "action": "Audit My Portfolio",
        "human_cat": "business"
    },
    "objection-buster": {
        "title": "Website Sales Objection Buster",
        "human_desc": "Finds customer hesitation points ('Too expensive', 'No time') and rewrites your landing page to answer them effortlessly.",
        "icon": "fa-crosshairs",
        "color": "emerald",
        "tag": "Conversions",
        "badge": "Double Sales Conversion",
        "action": "Bust Customer Objections",
        "human_cat": "business"
    },
    "thumbnail-concepts": {
        "title": "YouTube Title & Thumbnail Engine",
        "human_desc": "Generates 5 curiosity-piquing title angles and visual thumbnail concepts to dramatically increase your clicks.",
        "icon": "fa-photo-film",
        "color": "red",
        "tag": "YouTube Growth",
        "badge": "Higher Click-Through",
        "action": "Generate Video Angles",
        "human_cat": "business"
    },
    "lead-qualifier": {
        "title": "Inbound Client Lead Qualifier",
        "human_desc": "Screens client inquiry emails to separate high-paying dream clients from tire-kickers with zero budget.",
        "icon": "fa-filter-circle-dollar",
        "color": "teal",
        "tag": "Client Sales",
        "badge": "Stop Wasting Discovery Calls",
        "action": "Qualify Inbound Lead",
        "human_cat": "business"
    },
    "filler-cleaner": {
        "title": "Voice Memo & Filler Word Cleaner",
        "human_desc": "Cleans 'um', 'uh', false starts, and rambling sentences from speech transcripts into crisp, polished writing.",
        "icon": "fa-wand-magic-sparkles",
        "color": "cyan",
        "tag": "Voice Notes",
        "badge": "Instant Polished Writing",
        "action": "Clean Voice Transcript",
        "human_cat": "business"
    },
    "tone-subtitles": {
        "title": "Video Slang & Humor Subtitle Adapter",
        "human_desc": "Adapts colloquial jokes, idioms, and slang in video subtitles so international viewers actually understand the humor.",
        "icon": "fa-closed-captioning",
        "color": "violet",
        "tag": "Global Subtitles",
        "badge": "Global Engagement",
        "action": "Adapt Video Subtitles",
        "human_cat": "business"
    },

    # 36-45: Local Small Businesses & Trades
    "review-reply": {
        "title": "Google 1-Star Review De-escalator",
        "human_desc": "Turns furious 1-star restaurant or clinic complaints into calm, professional public replies that protect your business reputation.",
        "icon": "fa-star-half-stroke",
        "color": "amber",
        "tag": "Local Business",
        "badge": "Save Your Reputation",
        "action": "De-escalate Negative Review",
        "human_cat": "business"
    },
    "menu-digitizer": {
        "title": "Paper Menu Allergen & Price Scanner",
        "human_desc": "Converts photos of handwritten café boards into digital POS menus with vegan, gluten, and nut allergen tags.",
        "icon": "fa-utensils",
        "color": "orange",
        "tag": "Cafes & Bistros",
        "badge": "Menu in Minutes",
        "action": "Digitize Café Menu",
        "human_cat": "business"
    },
    "salon-fill": {
        "title": "Last-Minute Cancellation Filler",
        "human_desc": "Drafts friendly SMS blasts to waitlisted clients offering a quick discount when a client cancels 2 hours before an appointment.",
        "icon": "fa-scissors",
        "color": "pink",
        "tag": "Salons & Spas",
        "badge": "Stop Lost Revenue",
        "action": "Fill Cancelled Slot",
        "human_cat": "business"
    },
    "trades-quote": {
        "title": "Voice-to-Trades Job Estimate",
        "human_desc": "Records a plumber or electrician rambling notes on-site and formats it into an itemized, professional customer quote.",
        "icon": "fa-faucet-drip",
        "color": "blue",
        "tag": "Plumbing & Electrical",
        "badge": "Quote On The Go",
        "action": "Create Trades Quote",
        "human_cat": "business"
    },
    "local-seo": {
        "title": "Google Maps Local Search Optimizer",
        "human_desc": "Rewrites your local shop's business description and service list to rank #1 when neighbors search for local help.",
        "icon": "fa-map-location-dot",
        "color": "emerald",
        "tag": "Google Maps",
        "badge": "Rank Higher Locally",
        "action": "Optimize Google Profile",
        "human_cat": "business"
    },
    "vendor-slip": {
        "title": "Supplier Invoice to Inventory Normalizer",
        "human_desc": "Converts messy wholesale supplier slips into standardized product codes and unit costs for boutique retail inventory.",
        "icon": "fa-boxes-stacked",
        "color": "purple",
        "tag": "Boutique Retail",
        "badge": "Inventory In Sync",
        "action": "Normalize Supplier Slip",
        "human_cat": "business"
    },
    "shift-swap": {
        "title": "Employee Shift Swap Arbiter",
        "human_desc": "Ensures employee shift trades don't trigger overtime violations, fatigue laws, or leave the store short-staffed.",
        "icon": "fa-calendar-days",
        "color": "indigo",
        "tag": "Store Manager",
        "badge": "Smooth Scheduling",
        "action": "Review Shift Swap",
        "human_cat": "business"
    },
    "repair-status": {
        "title": "Customer Repair Status Messenger",
        "human_desc": "Generates clear, reassuring SMS text updates when electronics or shoe repair parts are waiting on international shipping.",
        "icon": "fa-mobile-screen-button",
        "color": "cyan",
        "tag": "Repair Shops",
        "badge": "Zero Angry Phone Calls",
        "action": "Send Customer Update",
        "human_cat": "business"
    },
    "lease-cam": {
        "title": "Commercial Lease CAM Fee Auditor",
        "human_desc": "Audits unexpected retail mall common area maintenance charges to ensure your landlord isn't overbilling your shop.",
        "icon": "fa-building",
        "color": "rose",
        "tag": "Shop Lease",
        "badge": "Catch Landlord Overcharges",
        "action": "Audit CAM Fees",
        "human_cat": "legal"
    },
    "maintenance-log": {
        "title": "Equipment Maintenance Voice Logger",
        "human_desc": "Converts factory or bakery machinery noises and operator notes into predictive maintenance logs before a breakdown occurs.",
        "icon": "fa-gears",
        "color": "slate",
        "tag": "Equipment Ops",
        "badge": "Prevent Costly Breakdowns",
        "action": "Log Maintenance Note",
        "human_cat": "business"
    },

    # 46-55: School, Public Service & Legal
    "differentiate": {
        "title": "Differentiated Homework Creator",
        "human_desc": "Turns 1 classroom lesson into 3 reading tiers (Support, Grade Level, Advanced) so every child succeeds in class.",
        "icon": "fa-book-open-reader",
        "color": "indigo",
        "tag": "Teaching",
        "badge": "Save 3 Hours of Prep",
        "action": "Differentiate Lesson",
        "human_cat": "health"
    },
    "rubric-feedback": {
        "title": "Student Rubric Feedback Drafter",
        "human_desc": "Drafts encouraging, constructive essay feedback based on rubric criteria without grading papers late into the night.",
        "icon": "fa-pen-ruler",
        "color": "purple",
        "tag": "Grading",
        "badge": "Encouraging Feedback",
        "action": "Draft Student Feedback",
        "human_cat": "health"
    },
    "case-notes": {
        "title": "Social Work Objective Case Note Distiller",
        "human_desc": "Converts emotional client interview notes into compliant, court-admissible facts while removing subjective bias.",
        "icon": "fa-clipboard-user",
        "color": "teal",
        "tag": "Social Work",
        "badge": "Court-Ready Compliance",
        "action": "Distill Case Note",
        "human_cat": "community"
    },
    "council-digest": {
        "title": "City Council & Zoning Digest",
        "human_desc": "Summarizes lengthy municipal zoning hearings into clear alerts showing neighbors where new roads and high-rises are planned.",
        "icon": "fa-city",
        "color": "blue",
        "tag": "Neighborhood Civic",
        "badge": "Local Transparency",
        "action": "Digest Council Meeting",
        "human_cat": "community"
    },
    "soap-note": {
        "title": "Clinical SOAP Note from Ambient Audio",
        "human_desc": "Turns conversational patient-doctor dialogue into standardized medical SOAP chart notes with billing codes.",
        "icon": "fa-stethoscope",
        "color": "emerald",
        "tag": "Clinic Charting",
        "badge": "Reduce Doctor Burnout",
        "action": "Generate SOAP Note",
        "human_cat": "health"
    },
    "homeschool-plan": {
        "title": "Homeschool Lesson Plan Generator",
        "human_desc": "Builds a 5-day curriculum integrating a child's natural passions (e.g. sharks, space) into required math and reading standards.",
        "icon": "fa-shapes",
        "color": "amber",
        "tag": "Homeschooling",
        "badge": "Passionate Learning",
        "action": "Create Homeschool Week",
        "human_cat": "health"
    },
    "parent-comms": {
        "title": "Bilingual Parent-Teacher Bridge",
        "human_desc": "Drafts warm, culturally respectful letters to immigrant parents discussing classroom behavior constructively.",
        "icon": "fa-comments",
        "color": "rose",
        "tag": "Parent Liaison",
        "badge": "Family Trust",
        "action": "Draft Bilingual Note",
        "human_cat": "health"
    },
    "benefits-finder": {
        "title": "Public Safety-Net Benefits Matcher",
        "human_desc": "Calculates food assistance, heating aid, and healthcare program eligibility based on family size and household income.",
        "icon": "fa-hand-holding-dollar",
        "color": "emerald",
        "tag": "Safety Net",
        "badge": "Find Available Aid",
        "action": "Check Benefits Eligibility",
        "human_cat": "community"
    },
    "crisis-aid": {
        "title": "Youth Mental Health Text De-escalator",
        "human_desc": "Provides school counselors with gentle, active-listening responses that validate deep emotional pain without toxic positivity.",
        "icon": "fa-heart-circle-check",
        "color": "pink",
        "tag": "Youth Mental Health",
        "badge": "Compassionate Care",
        "action": "De-escalate Crisis Text",
        "human_cat": "health"
    },
    "court-prep": {
        "title": "Small Claims Court Hearing Companion",
        "human_desc": "Translates scary court summons into plain-English checklists of evidence, photos, and courtroom etiquette rules.",
        "icon": "fa-gavel",
        "color": "slate",
        "tag": "Self-Representation",
        "badge": "Courtroom Confidence",
        "action": "Prepare Court Evidence",
        "human_cat": "legal"
    },

    # 0: Universal Document OCR
    "invoice-extract": {
        "title": "Universal Receipt & Bill Reader",
        "human_desc": "Takes photos of wrinkled receipts or PDF bills and organizes every line item, tax, and total into clean records.",
        "icon": "fa-file-invoice-dollar",
        "color": "purple",
        "tag": "Receipt & Bill OCR",
        "badge": "Zero Typing Receipts",
        "action": "Read Receipt & Bill",
        "human_cat": "vision"
    }
}

print(f"Loaded friendly metadata for {len(FRIENDLY_METADATA)} endpoints.")
