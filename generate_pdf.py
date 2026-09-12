import sys
import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print total page count: 'Page X of Y'
    along with running header and footer on landscape pages.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        width, height = self._pagesize
        self.saveState()
        
        # Cover page (page 1) doesn't need running header/footer
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#475569"))
            self.drawString(36, height - 24, "ENDPOINT AS A SERVICE (EaaS)")
            
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(175, height - 24, "|   The Comprehensive AI Microservice Playbook (55+ Specialized Endpoints)")
            
            # Header rule
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(36, height - 28, width - 36, height - 28)
            
            # Footer rule
            self.line(36, 28, width - 36, 28)
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(36, 17, "Confidential Strategy Playbook  •  Built for Multi-Persona AI Endpoint Deployment")
            page_str = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(width - 36, 17, page_str)
            
        self.restoreState()

def build_pdf(filename="AI_Endpoint_As_A_Service_Playbook.pdf"):
    # Target 11 x 8.5 inches landscape (792 x 612 pt)
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=38,
        bottomMargin=36
    )
    
    usable_width = 792 - 72  # 720 pt
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=12
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#64748B')
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=6,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyP',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#334155')
    )
    
    # Table typography styles
    th_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=0
    )

    td_num_style = ParagraphStyle(
        'TableNum',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#2563EB')
    )
    
    td_route_style = ParagraphStyle(
        'TableRoute',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#0F172A')
    )

    td_persona_style = ParagraphStyle(
        'TablePersona',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#1E293B')
    )

    td_sub_style = ParagraphStyle(
        'TableSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=6.8,
        leading=9,
        textColor=colors.HexColor('#64748B')
    )

    td_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor('#334155')
    )

    td_demand_style = ParagraphStyle(
        'TableDemand',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9.2,
        textColor=colors.HexColor('#475569')
    )

    story = []
    
    # --- PAGE 1: EXECUTIVE BRIEF & ARCHITECTURE ---
    story.append(Paragraph("ENDPOINT AS A SERVICE (EaaS)", title_style))
    story.append(Paragraph("The Comprehensive AI Microservice Playbook: 55+ Specialized Functions for Non-Devs, SMBs & NGOs", subtitle_style))
    story.append(Paragraph("<b>Author / Project:</b> AI Endpoint Initiative &nbsp;|&nbsp; <b>Release:</b> Strategy Guide & Catalog &nbsp;|&nbsp; <b>Architecture:</b> Stateless Deterministic AI Microservices", meta_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceBefore=2, spaceAfter=10))
    
    intro_p1 = (
        "<b>The Market Opportunity:</b> The broader market is fatigued by generic 'ChatGPT wrapper' interfaces. "
        "Everyday consumers, solopreneurs, local shop owners, and non-profit leaders do not want another conversational chat window. "
        "What they desperately need are <b>single-purpose, reliable micro-utilities</b>: automated endpoints that receive messy, unstructured "
        "inputs (wrinkled receipts, complex PDF leases, cryptic lab results, rambling audio notes, or disorganized spreadsheets) and return "
        "<b>100% clean, structured, and actionable outcomes</b> without requiring prompt engineering or technical expertise."
    )
    story.append(Paragraph(intro_p1, body_style))
    story.append(Spacer(1, 8))

    # 4 Delivery channels callout box
    channels_data = [
        [
            Paragraph("<b>Channel 1: Spreadsheet Functions</b><br/><font size=7 color='#475569'>Custom Google Sheets / Excel formulas (e.g. <code>=AUDIT_LEASE(A2)</code>). Non-profits, teachers, and shop owners run their operations in spreadsheets.</font>", body_style),
            Paragraph("<b>Channel 2: Chat App Ingestion</b><br/><font size=7 color='#475569'>WhatsApp & Telegram webhooks. Users simply forward a photo of a bill, an audio voice memo, or a document screenshot to receive instant answers.</font>", body_style),
            Paragraph("<b>Channel 3: Mobile Shortcuts</b><br/><font size=7 color='#475569'>iOS Shortcuts & Android Assistant integrations. One-tap triggers directly from lockscreens or camera shares to the EaaS endpoint.</font>", body_style),
            Paragraph("<b>Channel 4: No-Code Connectors</b><br/><font size=7 color='#475569'>Zapier, Make.com, & n8n drag-and-drop modules. Allows automated triggers from Typeform, Stripe, Gmail, or Airtable with zero coding.</font>", body_style),
        ]
    ]
    t_channels = Table(channels_data, colWidths=[180, 180, 180, 180])
    t_channels.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#BFDBFE')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DBEAFE')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_channels)
    story.append(Spacer(1, 10))

    # Key Architectural Principles
    arch_title = Paragraph("Core Architectural Pillars for Production-Grade EaaS", h2_style)
    story.append(arch_title)
    arch_p = (
        "<b>1. Guaranteed Schema Enforcement:</b> Use Pydantic and JSON Schema validators (e.g., Instructor) to ensure that the response strictly satisfies schema constraints without stray markdown or hallucinated keys.<br/>"
        "<b>2. Low-Latency Tiering:</b> Route simple classifications and entity extractions through sub-second models (e.g., Gemini 1.5 Flash, Claude 3.5 Haiku, Llama 3 via Groq) to maintain response times under 1 second.<br/>"
        "<b>3. Dual Monetization:</b> Provide both a 'Managed Tier' (flat \$0.01 – \$0.05 per request with bundled compute) and a 'BYOK Tier' (users provide their own OpenAI/Gemini keys for a recurring platform subscription)."
    )
    story.append(Paragraph(arch_p, body_style))
    story.append(Spacer(1, 12))
    
    # Overview Table of Categories
    cat_summary = [
        [
            Paragraph("<b>Category</b>", th_style),
            Paragraph("<b>Target Audience / Personas</b>", th_style),
            Paragraph("<b>Endpoint Count</b>", th_style),
            Paragraph("<b>Primary Value Proposition</b>", th_style)
        ],
        [
            Paragraph("<b>1. Individuals & Consumers</b>", td_persona_style),
            Paragraph("Everyday consumers, tenants, patients, drivers, parents, seniors", td_cell_style),
            Paragraph("15 Endpoints", td_num_style),
            Paragraph("Protection against exploitation, deciphering medical/legal jargon, home time-saving", td_cell_style)
        ],
        [
            Paragraph("<b>2. Non-Profits & NGOs</b>", td_persona_style),
            Paragraph("Charities, grant writers, volunteer coordinators, crisis relief teams", td_cell_style),
            Paragraph("10 Endpoints", td_num_style),
            Paragraph("Automating grant qualification, donor storytelling, multilingual outreach", td_cell_style)
        ],
        [
            Paragraph("<b>3. Creators & Solopreneurs</b>", td_persona_style),
            Paragraph("YouTubers, podcasters, freelancers, indie founders, designers", td_cell_style),
            Paragraph("10 Endpoints", td_num_style),
            Paragraph("Defending contract scope, 1-to-10 content repurposing, brand pitching", td_cell_style)
        ],
        [
            Paragraph("<b>4. Local SMBs & Trades</b>", td_persona_style),
            Paragraph("Cafes, auto repair, salons, plumbers, boutique retail, clinics", td_cell_style),
            Paragraph("10 Endpoints", td_num_style),
            Paragraph("De-escalating public reviews, voice-to-invoice conversion, inventory digitizing", td_cell_style)
        ],
        [
            Paragraph("<b>5. Education & Public Service</b>", td_persona_style),
            Paragraph("Teachers, social workers, municipal citizens, clinic staff", td_cell_style),
            Paragraph("10 Endpoints", td_num_style),
            Paragraph("Differentiated curriculum creation, objective casework records, civic transparency", td_cell_style)
        ],
    ]
    t_cat = Table(cat_summary, colWidths=[140, 200, 90, 290])
    t_cat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_cat)
    story.append(PageBreak())

    # Widths: Col 0 (# & Route): 140 pt, Col 1 (Persona & Trigger): 110 pt, Col 2 (Raw Input): 130 pt, Col 3 (Output & Action): 170 pt, Col 4 (Demand & Problem): 170 pt = 720 pt total
    col_widths = [140, 110, 130, 170, 170]

    def create_category_table(header_title, rows_data):
        elements = []
        elements.append(Paragraph(header_title, h1_style))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceBefore=2, spaceAfter=6))
        
        table_content = [
            [
                Paragraph("<b># & Endpoint Route</b>", th_style),
                Paragraph("<b>User Persona & Trigger</b>", th_style),
                Paragraph("<b>Raw Input Payload</b>", th_style),
                Paragraph("<b>Clean Structured Output / Action</b>", th_style),
                Paragraph("<b>Pain Point & Market Demand</b>", th_style)
            ]
        ]
        
        for r in rows_data:
            c0 = [
                Paragraph(f"<b>#{r['id']} {r['name']}</b>", td_num_style),
                Paragraph(f"<code>{r['route']}</code>", td_route_style)
            ]
            c1 = [
                Paragraph(f"<b>{r['persona']}</b>", td_persona_style),
                Paragraph(f"Trigger: {r['trigger']}", td_sub_style)
            ]
            c2 = Paragraph(r['input'], td_cell_style)
            c3 = Paragraph(r['output'], td_cell_style)
            c4 = Paragraph(r['demand'], td_demand_style)
            
            table_content.append([c0, c1, c2, c3, c4])
            
        t = Table(table_content, colWidths=col_widths, repeatRows=1)
        t_style = [
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
            ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#CBD5E1')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]
        for i in range(1, len(table_content)):
            if i % 2 == 0:
                t_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F8FAFC')))
            else:
                t_style.append(('BACKGROUND', (0, i), (-1, i), colors.white))
                
        t.setStyle(TableStyle(t_style))
        elements.append(t)
        return elements

    # --- CATEGORY 1: INDIVIDUALS & CONSUMERS (15 endpoints) ---
    c1_rows = [
        {
            "id": 1, "name": "Medical Lab Report Explainer", "route": "POST /v1/health/explain-lab",
            "persona": "Patient / Caregiver", "trigger": "WhatsApp / Portal Upload",
            "input": "Photo or PDF of blood work / lab results.",
            "output": "Plain-English summary, abnormal items highlighted in red, potential dietary causes, and list of 3 specific questions for the physician.",
            "demand": "Patients receive complex lab data online days before their doctor reviews it, leading to extreme panic and frantic WebMD searches."
        },
        {
            "id": 2, "name": "Apartment Lease Auditor", "route": "POST /v1/legal/lease-check",
            "persona": "Tenant / Student", "trigger": "Web Form / PDF Upload",
            "input": "Rental lease agreement PDF.",
            "output": "Audit report highlighting illegal clauses by state, unexpected repair liability, hidden termination penalties, and renewal traps.",
            "demand": "Landlords slip aggressive, unenforceable clauses into leases; standard renters cannot afford a $300/hour real estate attorney."
        },
        {
            "id": 3, "name": "Elder Scam & Phishing Defender", "route": "POST /v1/safety/scam-detector",
            "persona": "Senior / Adult Child", "trigger": "Forwarded SMS / Email",
            "input": "Screenshot of suspicious text, fake bank email, or voice note text.",
            "output": "Threat rating (0-100%), scam taxonomy match (IRS impersonation, crypto trap, family distress), and clear instruction on next safe steps.",
            "demand": "Adult children are inundated with frantic messages from elderly parents asking 'Is this bank warning real? Should I click it?'"
        },
        {
            "id": 4, "name": "Mechanic Quote Sanity Checker", "route": "POST /v1/auto/quote-verifier",
            "persona": "Vehicle Owner", "trigger": "Mobile Photo of Invoice",
            "input": "Itemized repair estimate photo + car year/make/model.",
            "output": "Fair market price benchmark, separation of safety-critical fixes vs optional upsells, and OEM part cost reality check.",
            "demand": "Huge consumer anxiety around getting overcharged at repair shops due to opaque mechanical part names and inflated labor."
        },
        {
            "id": 5, "name": "Subscription & Fee Hunter", "route": "POST /v1/finance/fee-audit",
            "persona": "Budgeter / Household", "trigger": "Bank Statement CSV / PDF",
            "input": "Monthly checking or credit card statement.",
            "output": "Itemized recurring subscriptions, quiet price increases over the prior 6 months, and direct cancellation links/opt-out paths.",
            "demand": "Consumers lose $300–$600 annually on forgotten recurring SaaS, streaming, and gym memberships buried in statements."
        },
        {
            "id": 6, "name": "Allergen & Additive Scanner", "route": "POST /v1/diet/ingredient-alert",
            "persona": "Parent / Allergy Sufferer", "trigger": "Camera Snap in Supermarket",
            "input": "Photo of food ingredient panel + user allergen profile.",
            "output": "Immediate Safe/Danger badge, hidden derivatives flagged (e.g. casein/whey for dairy, hydrolyzed soy for gluten), and E-number breakdown.",
            "demand": "Parents of children with severe celiac or nut allergies spend 15 minutes squinting at microscopic food packaging while grocery shopping."
        },
        {
            "id": 7, "name": "Parking Ticket Appeal Drafter", "route": "POST /v1/legal/ticket-appeal",
            "persona": "Urban Driver", "trigger": "Ticket Photo + Street Sign",
            "input": "Ticket photo + street sign/curb photo + city location.",
            "output": "Formal legal appeal letter citing municipal traffic codes, ambiguous signage precedents, and instructions for city submission.",
            "demand": "Cities issue tens of thousands of ambiguous parking fines; 80% are paid without dispute because drafting appeals is intimidating."
        },
        {
            "id": 8, "name": "Insurance Denial Fighter", "route": "POST /v1/insurance/appeal-generator",
            "persona": "Patient / Homeowner", "trigger": "Denial Letter + Policy PDF",
            "input": "Denial letter photo + insurance declaration page.",
            "output": "Targeted appeal letter citing internal policy clauses, peer-reviewed clinical guidelines, and statutory prompt-pay regulations.",
            "demand": "Insurers automate claim denials counting on consumer exhaustion; an automated rebuttal tool levels the playing field."
        },
        {
            "id": 9, "name": "IEP Special-Ed Decoder", "route": "POST /v1/edu/iep-analyzer",
            "persona": "Special-Ed Parent", "trigger": "School Document Upload",
            "input": "School Individualized Education Program (IEP) PDF.",
            "output": "De-jargonized parent summary, list of omitted accommodations, legal rights under IDEA, and a prioritized checklist for the school meeting.",
            "demand": "School IEPs are 40+ pages of dense educational and bureaucratic terminology that leave anxious parents feeling helpless."
        },
        {
            "id": 10, "name": "Zero-Waste Fridge Chef", "route": "POST /v1/food/fridge-inventory",
            "persona": "Busy Parent / Student", "trigger": "Photo of Open Refrigerator",
            "input": "Image of fridge interior + dietary constraints.",
            "output": "3 exact meal recipes utilizing exclusively available ingredients, prioritizing expiring perishables, with step-by-step instructions.",
            "demand": "Guilt over grocery waste and daily decision fatigue surrounding 'what can I cook with whatever is left in the fridge'."
        },
        {
            "id": 11, "name": "Appliance Error Decryptor", "route": "POST /v1/home/appliance-fix",
            "persona": "Tenant / Homeowner", "trigger": "Photo of Flashing Code",
            "input": "Photo of dishwasher/boiler error code + model label.",
            "output": "Exact diagnosis, difficulty rating (5-min DIY fix vs licensed technician required), safety risk, and exact replacement part numbers.",
            "demand": "Panic when appliances beep or leak; users hate hunting down 80-page manufacturer service manuals on Google."
        },
        {
            "id": 12, "name": "Utility Tariff Optimizer", "route": "POST /v1/energy/bill-optimizer",
            "persona": "Household Manager", "trigger": "Electric / Gas PDF Bill",
            "input": "Hourly/daily energy consumption breakdown + rate schedule.",
            "output": "Cost comparison under alternative time-of-use tariffs, projected annual savings, and actionable shift-schedule for heavy appliances.",
            "demand": "Complicated peak and off-peak utility tariffs confuse homeowners trying to manage soaring heating and cooling bills."
        },
        {
            "id": 13, "name": "Career Transition Mapper", "route": "POST /v1/career/transition-map",
            "persona": "Laid-Off Worker", "trigger": "Resume + Target Role",
            "input": "Existing resume text + desired new industry job title.",
            "output": "Transferable skill crosswalk, industry buzzword translator, identified certification gaps, and a tailored resume narrative.",
            "demand": "Displaced workers in declining industries struggle to re-articulate their real-world experience for high-growth tech or green sectors."
        },
        {
            "id": 14, "name": "Child Behavior Situation Guide", "route": "POST /v1/parenting/coaching",
            "persona": "Stressed Parent", "trigger": "Voice Memo / Quick Text",
            "input": "Description of tantrum/conflict + child age/triggers.",
            "output": "De-escalation script, psychological developmental context, and immediate verbal options ('say this, avoid saying that').",
            "demand": "Parents in the middle of a high-stress behavioral incident do not have time to read 300-page psychology books."
        },
        {
            "id": 15, "name": "Warranty Dispute Drafter", "route": "POST /v1/consumer/warranty-claim",
            "persona": "Online Shopper", "trigger": "Receipt + Defect Photo",
            "input": "Product purchase receipt + defect description.",
            "output": "Formal demand letter citing statutory implied warranties (Magnuson-Moss Act / EU Consumer Directive) and credit card chargeback draft.",
            "demand": "Retailers routinely deflect warranty obligations to overseas manufacturers, banking on customer surrender."
        }
    ]
    story.extend(create_category_table("1. Everyday Individuals, Families & Consumers", c1_rows))
    story.append(PageBreak())

    # --- CATEGORY 2: NON-PROFITS, NGOS & CHARITIES (10 endpoints) ---
    c2_rows = [
        {
            "id": 16, "name": "Grant RFP Criteria Matcher", "route": "POST /v1/ngo/grant-match",
            "persona": "NPO Grant Writer", "trigger": "Airtable / Zapier Webhook",
            "input": "Foundation RFP PDF + non-profit historical mission/projects.",
            "output": "Eligibility match percentage (0-100%), disqualification risks, required compliance metrics, and direct alignment matrix.",
            "demand": "Grant staff spend up to 40% of their bandwidth reading 50-page RFPs only to find out they fail an eligibility clause in paragraph 42."
        },
        {
            "id": 17, "name": "Impact-to-Donor Story Engine", "route": "POST /v1/ngo/donor-story",
            "persona": "Fundraiser / Director", "trigger": "Google Sheets / Typeform",
            "input": "Raw field notes: 'Delivered 300 hygiene kits to shelter X, cost $450'.",
            "output": "Emotionally resonant donor newsletter story, tailored thank-you email, and social media celebration post.",
            "demand": "Donors expect continuous proof of impact, but overworked field workers only have time to jot down brief numerical summaries."
        },
        {
            "id": 18, "name": "IRS 990 / Audit Simplifier", "route": "POST /v1/ngo/990-explainer",
            "persona": "Board Trustee / Donor", "trigger": "Form 990 PDF Upload",
            "input": "Annual Form 990 tax return or financial audit.",
            "output": "Executive governance scorecard, program-to-overhead ratio, executive compensation context, and liquidity reserve health.",
            "demand": "Community board members and donors struggle to interpret complex IRS non-profit tax filings during quarterly meetings."
        },
        {
            "id": 19, "name": "Volunteer Skill Dispatcher", "route": "POST /v1/ngo/volunteer-dispatch",
            "persona": "Volunteer Coordinator", "trigger": "Form Intake Webhook",
            "input": "New volunteer intake questionnaire + list of urgent tasks.",
            "output": "Ranked task allocation matching volunteer credentials (e.g. legal, bookkeeping, physical labor) + personalized onboarding SMS.",
            "demand": "Non-profits collect hundreds of volunteer signups but leave them uncalled because manual coordination is overwhelming."
        },
        {
            "id": 20, "name": "Community Flyer Localizer", "route": "POST /v1/ngo/localize-notice",
            "persona": "Community Organizer", "trigger": "Flyer Text Upload",
            "input": "English clinic or food drive announcement + target immigrant culture.",
            "output": "Culturally adapted copy preserving reading levels, idioms, and local community context in Spanish, Vietnamese, Arabic, etc.",
            "demand": "Literal Google Translations produce confusing, robotic notices that alienate immigrant and refugee populations."
        },
        {
            "id": 21, "name": "Disaster SOS Triage Engine", "route": "POST /v1/crisis/sos-triage",
            "persona": "Disaster Response Lead", "trigger": "SMS / WhatsApp Gateway",
            "input": "Citizen distress texts ('Rising water, 4 trapped, 1 infant needs formula').",
            "output": "Urgency score (1-5), required rescue gear (boat, medical, baby supplies), GPS/address extraction, and structured dispatch JSON.",
            "demand": "During hurricanes, floods, or earthquakes, crisis lines are overwhelmed by unstructured citizen text messages."
        },
        {
            "id": 22, "name": "Major Donor Stewardship Drafter", "route": "POST /v1/ngo/donor-letter",
            "persona": "Development Officer", "trigger": "CRM Gift Webhook",
            "input": "Donor lifetime giving history + current campaign milestone reached.",
            "output": "Deeply customized stewardship letter referencing past personal gifts, family history, and specific project outcomes achieved.",
            "demand": "High-net-worth philanthropists stop giving when they receive generic, templated auto-responder receipts."
        },
        {
            "id": 23, "name": "Pantry Surplus Recipe Creator", "route": "POST /v1/ngo/foodbank-recipes",
            "persona": "Food Bank Lead", "trigger": "Weekly Surplus List",
            "input": "List of current surplus items (e.g. canned kidney beans, squash, oats).",
            "output": "Simple, no-oven/microwave-friendly recipe cards in 3 languages to print and slip into food distribution boxes.",
            "demand": "Pantries receive pallet donations of strange or bulk ingredients that clients end up discarding because they don't know how to prepare them."
        },
        {
            "id": 24, "name": "Legislative Policy Impact Digest", "route": "POST /v1/ngo/policy-impact",
            "persona": "Advocacy Director", "trigger": "Bill PDF Upload",
            "input": "State or municipal legislative bill PDF + NGO focus area.",
            "output": "Section-by-section threat/opportunity breakdown, affected client populations, and 3 talking points for testimony hearings.",
            "demand": "Grassroots community organizations cannot afford corporate lobbying firms to digest 200-page state omnibus bills."
        },
        {
            "id": 25, "name": "Grant Budget Narrative Writer", "route": "POST /v1/ngo/budget-narrative",
            "persona": "Program Manager", "trigger": "Excel Budget Upload",
            "input": "Itemized spreadsheet rows ($15k travel, $8k equipment, $40k personnel).",
            "output": "Comprehensive, audit-ready narrative justification for every line item, strictly aligned with federal or foundation criteria.",
            "demand": "Foundations reject otherwise stellar applications because the mathematical spreadsheet lacks narrative justification."
        }
    ]
    story.extend(create_category_table("2. Non-Profits (NPOs), NGOs & Community Charities", c2_rows))
    story.append(PageBreak())

    # --- CATEGORY 3: SOLOPRENEURS, CREATORS & FREELANCERS (10 endpoints) ---
    c3_rows = [
        {
            "id": 26, "name": "Multi-Platform Repurposer", "route": "POST /v1/creator/repurpose",
            "persona": "YouTuber / Podcaster", "trigger": "Video URL / Audio Upload",
            "input": "Long-form video/podcast transcript.",
            "output": "1 cohesive X/Twitter thread, 3 high-engagement LinkedIn posts, 5 short-form TikTok/Reels hooks, and an email newsletter summary.",
            "demand": "Creators spend 10+ hours producing high-value video, then burn out trying to manually reformat it across 5 social networks."
        },
        {
            "id": 27, "name": "Scope Creep Defense Assistant", "route": "POST /v1/freelance/scope-defense",
            "persona": "Freelance Designer / Dev", "trigger": "Email Forward / Slack Hook",
            "input": "Client message ('Can we also add a live chat?') + original contract text.",
            "output": "Scope analysis confirming contract breach, diplomatic response preserving the client relationship, and an attached change-order quote.",
            "demand": "Freelancers lose thousands doing unpaid 'quick favors' out of fear of sounding rude or aggressive to paying clients."
        },
        {
            "id": 28, "name": "Podcast Show Notes & Timestamps", "route": "POST /v1/audio/shownotes",
            "persona": "Podcast Host / Producer", "trigger": "Audio File / VTT Transcript",
            "input": "Episode audio file or raw transcript.",
            "output": "Polished episode overview, guest biographical context, chapter timestamps (00:04:12), core takeaways, and quote cards.",
            "demand": "Manual listening, timestamp logging, and markdown formatting consumes 1.5 to 2 hours of editing time per audio episode."
        },
        {
            "id": 29, "name": "Sponsorship Pitch & Rate Matrix", "route": "POST /v1/creator/pitch-brand",
            "persona": "Micro-Creator", "trigger": "Web Intake Form",
            "input": "Channel analytics (impressions, audience niche) + target sponsor brand.",
            "output": "Personalized brand pitch deck email, calculated recommended pricing range based on CPM benchmarks, and campaign concept ideas.",
            "demand": "Creators with 10k–100k followers have no idea what their attention is worth and constantly accept lowball $50 sponsorship deals."
        },
        {
            "id": 30, "name": "Portfolio First-Impression Audit", "route": "POST /v1/design/audit-portfolio",
            "persona": "Junior Creative / Dev", "trigger": "Portfolio URL Submission",
            "input": "Personal portfolio website URL or case study screenshots.",
            "output": "5-second recruiter visual clarity score, UX navigation friction points, project storytelling critique, and clear action items.",
            "demand": "Junior creatives submit 100+ job applications wondering why they get zero callbacks, unaware their hero header is confusing."
        },
        {
            "id": 31, "name": "Landing Page Objection Buster", "route": "POST /v1/marketing/objection-handler",
            "persona": "Indie Founder / Creator", "trigger": "Landing Page Copy Text",
            "input": "Draft product sales copy + target buyer persona.",
            "output": "Top 10 hidden buyer hesitation questions (price justification, implementation effort, trust) + punchy FAQ copy answers.",
            "demand": "Digital product creators lose conversions because their sales pages describe features while ignoring unspoken customer anxieties."
        },
        {
            "id": 32, "name": "YouTube Thumbnail & Title Angle", "route": "POST /v1/youtube/thumbnail-concepts",
            "persona": "Video Creator", "trigger": "Video Premise / Script",
            "input": "Draft video topic, audience, and main takeaway.",
            "output": "3 distinct psychological packaging angles (curiosity gap, high-stakes contrarian, urgent mistake), thumbnail visual drafts, and 5 titles.",
            "demand": "The #1 complaint on r/NewTubers is filming a 20-minute masterpiece that gets zero views due to flat packaging."
        },
        {
            "id": 33, "name": "Cold Inbound Lead Qualifier", "route": "POST /v1/freelance/lead-qualifier",
            "persona": "Consultant / Agency Lead", "trigger": "Contact Form Webhook",
            "input": "Inbound inquiry message from prospect.",
            "output": "Budget viability rating (Low/Medium/High), project clarity score, red-flag client warnings, and drafted discovery questionnaire.",
            "demand": "Solopreneurs waste 45-minute unpaid introductory discovery calls on prospects with unrealistic expectations and a $100 budget."
        },
        {
            "id": 34, "name": "Audio Filler & Glitch Cleaner", "route": "POST /v1/audio/clean-transcript",
            "persona": "Audio / Video Editor", "trigger": "SRT / VTT File Upload",
            "input": "Raw transcript with millisecond timestamps.",
            "output": "Automated EDL (Edit Decision List) of precise timecodes for 'um', 'ah', mouth clicks, repeated words, and awkward pauses.",
            "demand": "Audio editors spend hours scrubbing waveforms back and forth to manually slice out vocal hesitations and filler words."
        },
        {
            "id": 35, "name": "Nuanced Subtitle Slang Adapter", "route": "POST /v1/video/tone-subtitles",
            "persona": "Global Video Creator", "trigger": "SRT Subtitle File",
            "input": "English subtitle file + target foreign language.",
            "output": "Culturally accurate subtitles that adapt sarcasm, memes, internet vernacular, and comedic timing rather than dry literal translation.",
            "demand": "Standard machine translation destroys humor and conversational charm, alienating international audiences."
        }
    ]
    story.extend(create_category_table("3. Solopreneurs, Creators & Freelancers", c3_rows))
    story.append(PageBreak())

    # --- CATEGORY 4: LOCAL SMBs & TRADES (10 endpoints) ---
    c4_rows = [
        {
            "id": 36, "name": "Public Review De-escalator", "route": "POST /v1/smb/review-reply",
            "persona": "Bistro / Clinic Owner", "trigger": "Google Maps Webhook",
            "input": "1-star or 5-star customer review + business policy notes.",
            "output": "Empathetic, brand-protective response that validates customer frustration without admitting liability, directing conversation offline.",
            "demand": "Small business owners respond angrily to unfair negative reviews online, permanently damaging their local reputation."
        },
        {
            "id": 37, "name": "Menu Allergen & Digitize Engine", "route": "POST /v1/restaurant/menu-digitizer",
            "persona": "Cafe / Restaurant Owner", "trigger": "Photo of Paper / Board Menu",
            "input": "Smartphone photo of printed or chalkboard menu.",
            "output": "Structured digital JSON menu with item names, prices, dietary badges (GF, Vegan, Halal), potential allergens, and 3 translations.",
            "demand": "Independent restaurants rely on greasy paper menus or unreadable PDFs, exposing themselves to allergen lawsuits."
        },
        {
            "id": 38, "name": "Cancellation Slot Filler", "route": "POST /v1/salon/fill-slot",
            "persona": "Salon / Dental Clinic", "trigger": "Cancellation Webhook",
            "input": "Cancelled appointment timestamp + VIP waitlist database.",
            "output": "Top 3 best-fit waitlisted clients based on past booking history + personalized SMS offer with a one-click confirmation link.",
            "demand": "Empty chair hours and late patient cancellations cost appointment-based service businesses thousands in lost weekly revenue."
        },
        {
            "id": 39, "name": "Voice-to-Trades Job Estimate", "route": "POST /v1/trades/quote-builder",
            "persona": "Plumber / Electrician", "trigger": "Voice Memo from Truck",
            "input": "Audio memo: 'Installed 30ft PVC, replaced P-trap, 2 hours labor at Johnson job'.",
            "output": "Professional itemized PDF/JSON estimate including parts markup, standard labor hours, payment terms, and warranty disclaimer.",
            "demand": "Tradespeople finish demanding physical jobs at 5 PM and dread sitting at a computer at night typing up customer quotes."
        },
        {
            "id": 40, "name": "Local Search SEO Optimizer", "route": "POST /v1/smb/local-seo",
            "persona": "Landscaper / Mechanic", "trigger": "Business Details Form",
            "input": "Business name, service radius, and core offerings.",
            "output": "Optimized Google Business Profile overview, 5 localized geo-targeted posts ('emergency pipe repair in North Austin'), and voice search FAQ.",
            "demand": "Small local contractors lose valuable neighborhood clients to large franchises because their Google profile lacks local search tags."
        },
        {
            "id": 41, "name": "Supplier Slip to POS Normalizer", "route": "POST /v1/retail/vendor-slip",
            "persona": "Boutique Grocer / Shop", "trigger": "Photo of Packing Slip",
            "input": "Photo of wrinkled paper packing slip from wholesaler.",
            "output": "Clean inventory import JSON with SKU, cost per unit, standard retail markup recommendation, and reorder threshold levels.",
            "demand": "Small retail clerks spend hours typing paper supplier delivery slips into Square, Shopify, or Lightspeed inventory systems."
        },
        {
            "id": 42, "name": "Employee Shift Swap Arbiter", "route": "POST /v1/retail/shift-swap",
            "persona": "Store / Restaurant Manager", "trigger": "Staff Chat Message",
            "input": "Staff request: 'Can Alex cover Maria's shift?' + weekly shift schedule.",
            "output": "Swap feasibility check verifying overtime hour thresholds, job certification requirements, and fair-labor compliance.",
            "demand": "Retail managers juggle chaotic text messages trying to approve swaps without accidentally triggering overtime labor penalties."
        },
        {
            "id": 43, "name": "Repair Status Customer Bot", "route": "POST /v1/repair/status-update",
            "persona": "Electronics Repair Shop", "trigger": "Ticket Internal Update",
            "input": "Technician diagnostic note: 'Cleaned liquid damage, soldering chip, delayed 1 day'.",
            "output": "Reassuring, jargon-free customer text update with realistic expected completion time and transparent billing status.",
            "demand": "Customers repeatedly call the workshop asking 'is my phone fixed yet?', interrupting technicians during delicate repairs."
        },
        {
            "id": 44, "name": "Commercial Lease CAM Auditor", "route": "POST /v1/smb/lease-cam-check",
            "persona": "Retail Tenant", "trigger": "Annual CAM Statement PDF",
            "input": "Annual Common Area Maintenance (CAM) reconciliation statement.",
            "output": "Detected non-allowable landlord expenses (capital improvements passed as maintenance), percentage calculation errors, and dispute notice.",
            "demand": "Commercial property managers frequently overcharge small storefront tenants thousands in unauthorized maintenance fees."
        },
        {
            "id": 45, "name": "Equipment Maintenance Voice Log", "route": "POST /v1/trades/maintenance-log",
            "persona": "Bakery / Brewery Manager", "trigger": "Quick Voice Note",
            "input": "Voice memo: 'Oven 2 heating element buzzing, temp offset by 15 degrees'.",
            "output": "Structured machinery log entry, predicted failure probability, recommended service steps, and next scheduled inspection alert.",
            "demand": "Expensive industrial kitchen and brewery equipment fails unexpectedly because staff neglects writing in paper logbooks."
        }
    ]
    story.extend(create_category_table("4. Local Small Businesses & Trades", c4_rows))
    story.append(PageBreak())

    # --- CATEGORY 5: EDUCATION, HEALTHCARE & PUBLIC SERVICE (10 endpoints) ---
    c5_rows = [
        {
            "id": 46, "name": "Differentiated Homework Creator", "route": "POST /v1/edu/differentiate",
            "persona": "Primary / Secondary Teacher", "trigger": "Curriculum Lesson Text",
            "input": "Base lesson text / math concept + target grade.",
            "output": "3 tiered assignments: Tier 1 (remedial/ESL scaffolding), Tier 2 (on grade level), Tier 3 (advanced critical-thinking challenge).",
            "demand": "Teachers spend entire Sunday afternoons creating multiple versions of one lesson to handle wide classroom reading disparities."
        },
        {
            "id": 47, "name": "Student Rubric Feedback Drafter", "route": "POST /v1/edu/rubric-feedback",
            "persona": "High School / College Teacher", "trigger": "LMS Essay Upload",
            "input": "Student essay text + assignment grading rubric.",
            "output": "Growth-oriented, encouraging feedback paragraph highlighting 2 specific strengths and 2 actionable revision targets tied to the rubric.",
            "demand": "Grading 120 student essays with meaningful, personalized critique requires 30+ hours of exhausting repetitive feedback."
        },
        {
            "id": 48, "name": "Objective Social Work Case Note", "route": "POST /v1/social/casenotes",
            "persona": "Caseworker / Child Welfare", "trigger": "Voice Dictation in Car",
            "input": "Raw verbal thoughts following a home welfare visit.",
            "output": "Strictly objective, court-compliant case documentation stripping subjective emotion, formatted according to state compliance rules.",
            "demand": "Caseworkers face immense burnout from paperwork; poorly phrased subjective notes cause severe legal liability in court hearings."
        },
        {
            "id": 49, "name": "City Council & Zoning Digest", "route": "POST /v1/civic/council-digest",
            "persona": "Civic Organizer / Citizen", "trigger": "Meeting Audio / Transcript",
            "input": "3-hour municipal city council meeting recording or transcript.",
            "output": "5-bullet civic summary highlighting property tax votes, zoning reclassifications, road infrastructure spending, and public comment highlights.",
            "demand": "Citizens are unaware of local decisions affecting their neighborhood because nobody has time to watch 4 hours of council broadcasts."
        },
        {
            "id": 50, "name": "Clinical SOAP Note from Audio", "route": "POST /v1/med/soap-note",
            "persona": "Physician / Therapist", "trigger": "Ambient Session Audio",
            "input": "Ambient audio or transcript of doctor-patient encounter.",
            "output": "Standardized medical SOAP note (Subjective, Objective, Assessment, Plan) with ICD-10 diagnostic codes ready for EHR pasting.",
            "demand": "Healthcare professionals spend 2 hours performing EHR computer documentation for every 1 hour they spend face-to-face with patients."
        },
        {
            "id": 51, "name": "Homeschool Interdisciplinary Plan", "route": "POST /v1/edu/homeschool-plan",
            "persona": "Homeschooling Parent", "trigger": "Child Profile Form",
            "input": "Child age/grade, state educational standards, and personal passions (e.g. marine biology).",
            "output": "Comprehensive 5-day lesson plan integrating marine biology into daily math problems, reading comprehension, history, and art.",
            "demand": "Parents struggle to design engaging, interdisciplinary curricula while fulfilling state academic compliance standards."
        },
        {
            "id": 52, "name": "Bilingual Parent-Teacher Bridge", "route": "POST /v1/edu/parent-comms",
            "persona": "School Administrator / Teacher", "trigger": "Staff Communication Form",
            "input": "Teacher update ('Lucas is improving in math but disrupts reading time') + parent native language.",
            "output": "Warm, culturally respectful update in Spanish/Arabic/Vietnamese that frames feedback constructively without alarming the parents.",
            "demand": "Immigrant families frequently misinterpret blunt automated school messages as severe disciplinary reprimands."
        },
        {
            "id": 53, "name": "Social Safety-Net Benefit Matcher", "route": "POST /v1/social/benefits-finder",
            "persona": "Low-Income Family / Advocate", "trigger": "Household Intake Form",
            "input": "Household income, zip code, dependents, and disability status.",
            "output": "Comprehensive list of eligible federal/state programs (SNAP, Medicaid, WIC, LIHEAP energy subsidies) + step-by-step application links.",
            "demand": "Low-income households leave billions of uncollected assistance on the table due to fragmented municipal and federal bureaucracy."
        },
        {
            "id": 54, "name": "Youth Crisis Text De-escalator", "route": "POST /v1/mentalhealth/crisis-aid",
            "persona": "School Counselor / Peer Guide", "trigger": "Incoming Student Text",
            "input": "Distressed youth message ('I can't take this anymore, everyone hates me').",
            "output": "Active listening response options, non-confrontational empathy validation, and safety triage assessment protocol.",
            "demand": "Counselors and hotlines need immediate guidance on high-stakes phrasing when responding to late-night distress messages."
        },
        {
            "id": 55, "name": "Pro-Se Court Hearing Companion", "route": "POST /v1/legal/court-prep",
            "persona": "Self-Represented Litigant", "trigger": "Summons / Petition PDF",
            "input": "Small claims petition or civil summons PDF.",
            "output": "Plain-language summary of allegations, evidentiary document checklist to bring to trial, procedural timeline, and court conduct rules.",
            "demand": "Millions of citizens navigate small claims court without an attorney and lose purely due to lack of procedural understanding."
        }
    ]
    story.extend(create_category_table("5. Education, Healthcare, Social Work & Civic Life", c5_rows))
    story.append(PageBreak())

    # --- FINAL SECTION: TECHNICAL BLUEPRINT & GO-TO-MARKET ---
    story.append(Paragraph("Technical Implementation & Go-To-Market Blueprint", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceBefore=2, spaceAfter=8))
    
    tech_overview = (
        "Building an Endpoint as a Service (EaaS) requires a lean, resilient stack focused on <b>deterministic data validation</b> "
        "and <b>zero-maintenance delivery interfaces</b>. Below is the battle-tested engineering blueprint:"
    )
    story.append(Paragraph(tech_overview, body_style))
    story.append(Spacer(1, 8))

    stack_data = [
        [
            Paragraph("<b>Component Layer</b>", th_style),
            Paragraph("<b>Recommended Technology</b>", th_style),
            Paragraph("<b>Operational Purpose & Best Practice</b>", th_style)
        ],
        [
            Paragraph("<b>API Framework</b>", td_persona_style),
            Paragraph("FastAPI (Python) or Hono / Elysia (TypeScript)", td_cell_style),
            Paragraph("Asynchronous handling, automatic OpenAPI/Swagger generation, native JSON type safety, and micro-second routing.", td_cell_style)
        ],
        [
            Paragraph("<b>Schema Enforcement</b>", td_persona_style),
            Paragraph("Instructor / Pydantic (Python) or Zod (TS)", td_cell_style),
            Paragraph("Guarantees 100% strict JSON schema compliance. Automatically retries with error logs if an LLM drops a required field.", td_cell_style)
        ],
        [
            Paragraph("<b>Model Gateway</b>", td_persona_style),
            Paragraph("LiteLLM / OpenRouter / Portkey", td_cell_style),
            Paragraph("Multi-provider fallbacks. If OpenAI has an outage or rate-limits, requests seamlessly failover to Gemini Flash or Anthropic.", td_cell_style)
        ],
        [
            Paragraph("<b>Compute Tiering</b>", td_persona_style),
            Paragraph("Groq (Llama 3) / Gemini 1.5 Flash / Claude 3.5 Haiku", td_cell_style),
            Paragraph("Sub-second latency (<600ms) and rock-bottom compute costs ($0.05 – $0.15 per million tokens) to maintain 90%+ gross margins.", td_cell_style)
        ],
        [
            Paragraph("<b>Billing & Metering</b>", td_persona_style),
            Paragraph("Stripe Metered Billing / Autumn / Lago", td_cell_style),
            Paragraph("Per-request API key authentication with credit balance decrements, monthly invoicing, and automated top-up alerts.", td_cell_style)
        ],
        [
            Paragraph("<b>Zero-Code Delivery</b>", td_persona_style),
            Paragraph("Zapier CLI / Make Partner / WhatsApp Cloud API", td_cell_style),
            Paragraph("Pre-built integrations allow non-developers to trigger endpoints directly from WhatsApp messages, Google Sheets, or webhooks.", td_cell_style)
        ]
    ]
    t_stack = Table(stack_data, colWidths=[130, 190, 400])
    t_stack.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_stack)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Actionable 3-Day Launch Framework", h2_style))
    launch_text = (
        "<b>Day 1: Prototype the Core Route.</b> Pick 1 specific endpoint from this guide (e.g. <i>#1 Medical Lab Explainer</i> or <i>#36 Review De-escalator</i>). "
        "Define the strict Pydantic output model and write the system prompt in FastAPI.<br/>"
        "<b>Day 2: Build the No-Code Ingestion.</b> Connect the route to a Make.com or Zapier webhook, or hook it to a WhatsApp Business sandbox number via Twilio. "
        "Test with 10 real-world messy inputs.<br/>"
        "<b>Day 3: Seed in Communities.</b> Post the live tool or free Google Sheet template on relevant Reddit communities (r/smallbusiness, r/nonprofit, r/freelance) "
        "offering 100 free requests in exchange for user feedback. Gather traction and convert power users to a $19/month plan."
    )
    story.append(Paragraph(launch_text, body_style))
    
    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF generated successfully: {filename}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "AI_Endpoint_As_A_Service_Playbook.pdf"
    build_pdf(out_file)
