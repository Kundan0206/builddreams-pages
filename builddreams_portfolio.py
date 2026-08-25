from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether, Image
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.graphics import renderPDF
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas as pdfcanvas
import os

# ─── BRAND PALETTE ────────────────────────────────────────────────────────────
NAVY       = colors.HexColor('#021346')
TEAL       = colors.HexColor('#009599')
TEAL_LIGHT = colors.HexColor('#00B8BD')
TEAL_PALE  = colors.HexColor('#E6F7F7')
NAVY_MID   = colors.HexColor('#0A2460')
GOLD       = colors.HexColor('#F5A623')
LIGHT_GRAY = colors.HexColor('#F4F6FA')
MID_GRAY   = colors.HexColor('#8892A4')
DARK_GRAY  = colors.HexColor('#2D3748')
WHITE      = colors.white
BLACK      = colors.black
DIVIDER    = colors.HexColor('#D0D8E8')

W, H = A4

OUTPUT = os.path.join(os.path.dirname(__file__), 'BuildDreams_Professional_Portfolio.pdf')
PARTNER_RAW_DIR = os.path.join(os.path.dirname(__file__), 'untitled folder')

# ─── CUSTOM FLOWABLES ─────────────────────────────────────────────────────────

class ColorRect(Flowable):
    def __init__(self, width, height, fill_color, radius=0):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.fill_color = fill_color
        self.radius = radius
    def draw(self):
        self.canv.setFillColor(self.fill_color)
        self.canv.roundRect(0, 0, self.width, self.height, self.radius, fill=1, stroke=0)

class HeroBlock(Flowable):
    """Full-width hero banner for cover page"""
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height
    def draw(self):
        c = self.canv
        # Background
        c.setFillColor(NAVY)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        # Decorative teal wave / bar at bottom
        c.setFillColor(TEAL)
        c.rect(0, 0, self.width, 8*mm, fill=1, stroke=0)
        # Diagonal accent shape
        c.setFillColor(NAVY_MID)
        p = c.beginPath()
        p.moveTo(self.width * 0.55, self.height)
        p.lineTo(self.width, self.height)
        p.lineTo(self.width, 0)
        p.lineTo(self.width * 0.75, 0)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        # Subtle circles
        c.setFillColor(TEAL)
        c.setFillAlpha(0.08)
        c.circle(self.width * 0.88, self.height * 0.7, 60*mm, fill=1, stroke=0)
        c.circle(self.width * 0.95, self.height * 0.2, 30*mm, fill=1, stroke=0)
        c.setFillAlpha(1)
        # Company name
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 36)
        c.drawString(18*mm, self.height - 52*mm, 'BuildDreams')
        c.setFillColor(TEAL)
        c.setFont('Helvetica-Bold', 36)
        c.drawString(18*mm, self.height - 68*mm, 'Technologies')
        # Tagline
        c.setFillColor(WHITE)
        c.setFont('Helvetica', 13)
        c.drawString(18*mm, self.height - 82*mm, 'Custom SaaS · Product Licensing · Tech Consultancy')
        # Horizontal rule
        c.setStrokeColor(TEAL)
        c.setLineWidth(2)
        c.line(18*mm, self.height - 88*mm, 120*mm, self.height - 88*mm)
        # Sub-detail
        # Sub-detail intentionally omitted on cover to keep the cover clean
        # Contact details are provided in the closing pages of the portfolio.

class SectionHeader(Flowable):
    def __init__(self, title, subtitle='', width=170*mm):
        Flowable.__init__(self)
        self.title = title
        self.subtitle = subtitle
        self.width = width
        self.height = 18*mm
    def draw(self):
        c = self.canv
        # Teal left bar
        c.setFillColor(TEAL)
        c.rect(0, 2*mm, 4*mm, 12*mm, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont('Helvetica-Bold', 18)
        c.drawString(8*mm, 9*mm, self.title)
        if self.subtitle:
            c.setFillColor(MID_GRAY)
            c.setFont('Helvetica', 9)
            c.drawString(8*mm, 4*mm, self.subtitle)

class StatBox(Flowable):
    def __init__(self, number, label, width=38*mm, height=22*mm):
        Flowable.__init__(self)
        self.number = number
        self.label = label
        self.width = width
        self.height = height
    def draw(self):
        c = self.canv
        c.setFillColor(TEAL_PALE)
        c.roundRect(0, 0, self.width, self.height, 4*mm, fill=1, stroke=0)
        c.setFillColor(TEAL)
        c.rect(0, self.height - 3*mm, self.width, 3*mm, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont('Helvetica-Bold', 16)
        c.drawCentredString(self.width/2, 10*mm, self.number)
        c.setFillColor(DARK_GRAY)
        c.setFont('Helvetica', 7)
        c.drawCentredString(self.width/2, 5*mm, self.label)

class ProductCard(Flowable):
    def __init__(self, name, tag, description, width=80*mm, height=40*mm):
        Flowable.__init__(self)
        self.name = name
        self.tag = tag
        self.description = description
        self.width = width
        self.height = height
    def draw(self):
        c = self.canv
        c.setFillColor(WHITE)
        c.setStrokeColor(DIVIDER)
        c.setLineWidth(0.5)
        c.roundRect(0, 0, self.width, self.height, 3*mm, fill=1, stroke=1)
        # Top teal strip
        c.setFillColor(NAVY)
        c.roundRect(0, self.height - 10*mm, self.width, 10*mm, 3*mm, fill=1, stroke=0)
        c.rect(0, self.height - 10*mm, self.width, 5*mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 9.5)
        c.drawString(4*mm, self.height - 7*mm, self.name)
        # Tag pill
        tag_w = len(self.tag) * 4.5 + 4
        c.setFillColor(TEAL)
        c.roundRect(self.width - tag_w - 3*mm, self.height - 8*mm, tag_w, 5*mm, 1.5*mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 6)
        c.drawCentredString(self.width - 3*mm - tag_w/2, self.height - 5.5*mm, self.tag)
        # Description
        from reportlab.platypus import Paragraph
        c.setFillColor(DARK_GRAY)
        c.setFont('Helvetica', 7.5)
        lines = self._wrap(self.description, 7.5, self.width - 8*mm)
        y = self.height - 16*mm
        for line in lines[:4]:
            if y < 4*mm: break
            c.drawString(4*mm, y, line)
            y -= 4*mm

    def _wrap(self, text, font_size, max_width):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        words = text.split()
        lines = []
        current = ''
        for word in words:
            test = (current + ' ' + word).strip()
            if stringWidth(test, 'Helvetica', font_size) <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

class ServicePill(Flowable):
    def __init__(self, icon_char, title, desc, width=170*mm, height=20*mm):
        Flowable.__init__(self)
        self.icon_char = icon_char
        self.title = title
        self.desc = desc
        self.width = width
        self.height = height
    def draw(self):
        c = self.canv
        c.setFillColor(LIGHT_GRAY)
        c.roundRect(0, 0, self.width, self.height, 3*mm, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.circle(10*mm, self.height/2, 5.5*mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(10*mm, self.height/2 - 3, self.icon_char)
        c.setFillColor(NAVY)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(19*mm, self.height/2 + 2*mm, self.title)
        c.setFillColor(MID_GRAY)
        c.setFont('Helvetica', 8.5)
        c.drawString(19*mm, self.height/2 - 4*mm, self.desc)

class FooterCanvas(pdfcanvas.Canvas):
    def __init__(self, *args, **kwargs):
        pdfcanvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_footer(num_pages)
            pdfcanvas.Canvas.showPage(self)
        pdfcanvas.Canvas.save(self)

    def _draw_footer(self, page_count):
        page = self._pageNumber
        if page == 1:
            return  # No footer on cover
        self.setFillColor(NAVY)
        self.rect(0, 0, W, 10*mm, fill=1, stroke=0)
        self.setFillColor(TEAL)
        self.rect(0, 9.5*mm, W, 1*mm, fill=1, stroke=0)
        self.setFillColor(WHITE)
        self.setFont('Helvetica', 8)
        self.drawString(20*mm, 3.5*mm, 'BuildDreams Technologies  ·  builddreams.co.in  ·  Nagpur, MH, India')
        self.setFont('Helvetica-Bold', 8)
        self.drawRightString(W - 20*mm, 3.5*mm, f'Page {page} of {page_count}')


# ─── STYLES ───────────────────────────────────────────────────────────────────
def styles():
    return {
        'h1': ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=22, textColor=NAVY, spaceAfter=4),
        'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=14, textColor=NAVY, spaceAfter=3),
        'h3': ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=11, textColor=TEAL, spaceAfter=2),
        'body': ParagraphStyle('body', fontName='Helvetica', fontSize=9.5, textColor=DARK_GRAY, leading=15, spaceAfter=4, alignment=TA_JUSTIFY),
        'small': ParagraphStyle('small', fontName='Helvetica', fontSize=8, textColor=MID_GRAY, leading=12, spaceAfter=2),
        'tag': ParagraphStyle('tag', fontName='Helvetica-Bold', fontSize=8, textColor=TEAL),
        'center': ParagraphStyle('center', fontName='Helvetica', fontSize=9.5, alignment=TA_CENTER, textColor=DARK_GRAY),
        'white': ParagraphStyle('white', fontName='Helvetica', fontSize=10, textColor=WHITE),
        'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=9, textColor=DARK_GRAY, leading=14, spaceAfter=2, leftIndent=10, firstLineIndent=-10),
    }

S = styles()


def prepare_partner_logos():
    if not os.path.isdir(PARTNER_RAW_DIR):
        return []

    files = sorted(
        f for f in os.listdir(PARTNER_RAW_DIR)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
        and not f.lower().startswith('screenshot')
    )
    if not files:
        return []

    return [(f'Partner {idx:02d}', os.path.join(PARTNER_RAW_DIR, filename)) for idx, filename in enumerate(files, start=1)]


# ─── BUILD ────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=14*mm,
        bottomMargin=16*mm,
        title='BuildDreams Technologies – Company Portfolio',
        author='BuildDreams Technologies',
    )
    story = []
    partners = prepare_partner_logos()

    # ══ PAGE 1: COVER ══════════════════════════════════════════════════════════
    story.append(HeroBlock(W - 40*mm, 90*mm))
    story.append(Spacer(1, 8*mm))

    # Tagline box
    tag_data = [['   BuildDreams Technologies builds future-ready SaaS products, delivers\n   custom software solutions, and provides strategic technology consultancy\n   to help businesses scale smarter — faster.']]
    tag_table = Table(tag_data, colWidths=[170*mm])
    tag_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), TEAL_PALE),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9.5),
        ('TEXTCOLOR', (0,0), (-1,-1), DARK_GRAY),
        ('ROUNDEDCORNERS', [3]),
    ]))
    story.append(tag_table)
    story.append(Spacer(1, 8*mm))

    # Stats row
    stats = [
        ('13+', 'SaaS Products Built'),
        ('50+', 'Institutions Served'),
        ('50K+', 'Students Impacted'),
        ('200+', 'Companies Onboarded'),
        ('MSME', 'Registered Enterprise'),
    ]
    stat_row = []
    for num, lbl in stats:
        stat_row.append(StatBox(num, lbl, width=30*mm, height=22*mm))

    st = Table([[s] for s in stat_row], colWidths=[30*mm]*5)
    # Actually do it as a row
    st = Table([stat_row], colWidths=[32*mm]*5)
    st.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(st)
    story.append(Spacer(1, 8*mm))

    # Three pillars
    pillars = [
        ['CUSTOM SAAS\nDEVELOPMENT', 'End-to-end custom software built for your workflows, sector, and scale. From MVP to production.'],
        ['PREBUILT PRODUCT\nLICENSING', 'Deploy proven, white-label SaaS products immediately. 13+ ready products across sectors.'],
        ['TECH\nCONSULTANCY', 'Architecture reviews, AI integration strategy, product roadmaps, and digital transformation guidance.'],
    ]
    pillar_cells = []
    for title, desc in pillars:
        cell = [
            [Paragraph(f'<b>{title}</b>', ParagraphStyle('pt', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE))],
            [Paragraph(desc, ParagraphStyle('pd', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#B0C4DE'), leading=12))],
        ]
        t = Table(cell, colWidths=[50*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), NAVY),
            ('BACKGROUND', (0,1), (-1,-1), NAVY_MID),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        pillar_cells.append(t)

    pillar_table = Table([pillar_cells], colWidths=[54*mm, 54*mm, 56*mm], rowHeights=[None])
    pillar_table.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(pillar_table)
    story.append(Spacer(1, 7*mm))

    # ══ EXECUTIVE SUMMARY (NEW) ═══════════════════════════════════════════════
    story.append(SectionHeader('Executive Summary', 'Key highlights and value proposition'))
    story.append(Spacer(1, 4*mm))
    es = (
        'BuildDreams Technologies combines pragmatic engineering discipline with product-minded design to deliver production-grade SaaS platforms, rapid white-label licensing, and strategic technical consultancy. '
        'We prioritise durability, observability, and integration readiness so clients receive solutions that scale and endure. Below are the core claims we consistently deliver:'
    )
    story.append(Paragraph(es, S['body']))
    story.append(Spacer(1, 3*mm))

    # Executive bullets
    bullets = [
        'Production-first delivery: staging + load testing + post-launch support.',
        'Flexible engagement: license, customized build, or retained support.',
        'Multi-sector experience: healthcare, finance, government, manufacturing, education.',
        'Modern stack with pragmatic integration: API-first, secure, and maintainable.',
    ]
    for b in bullets:
        story.append(Paragraph(f'•  {b}', S['bullet']))

    # ══ ASSOCIATION PARTNERS ═════════════════════════════════════════════════
    story.append(SectionHeader('Association Partners', 'Trusted organizations we collaborate with'))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        'BuildDreams collaborates with multiple partner organizations across sectors. '
        'The following logos are shown exactly from the original assets shared by our partners.',
        S['body']
    ))
    story.append(Spacer(1, 4*mm))

    if partners:
        cards = []
        logo_w = 50 * mm
        logo_h = 22 * mm
        for name, path in partners:
            try:
                logo = Image(path, width=logo_w, height=logo_h, kind='proportional')
            except Exception:
                logo = Paragraph(name, S['center'])
            cell = Table(
                [[logo], [Paragraph(name, ParagraphStyle('pn', fontName='Helvetica', fontSize=7.5, textColor=MID_GRAY, alignment=TA_CENTER))]],
                colWidths=[54*mm]
            )
            cell.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), WHITE),
                ('BOX', (0, 0), (-1, -1), 0.4, DIVIDER),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            cards.append(cell)

        rows = []
        for i in range(0, len(cards), 3):
            row = cards[i:i + 3]
            while len(row) < 3:
                row.append(Spacer(54*mm, 30*mm))
            rows.append(row)

        partner_grid = Table(rows, colWidths=[56*mm, 56*mm, 56*mm])
        partner_grid.setStyle(TableStyle([
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(partner_grid)
    else:
        story.append(Paragraph('Partner logos folder is empty or unavailable.', S['small']))

    # ══ LEADERSHIP & TEAM (NEW) ═══════════════════════════════════════════════
    story.append(SectionHeader('Leadership & Team', 'Experienced delivery and product leadership'))
    story.append(Spacer(1, 4*mm))
    team_table_data = [
        [Paragraph('<b>Suhomatech (Founder & CTO)</b>', S['h3']), Paragraph('15+ years building large-scale enterprise systems, leads architecture and AI initiatives.', S['body'])],
        [Paragraph('<b>Operations Lead</b>', S['h3']), Paragraph('Delivery manager focusing on SLAs, client onboarding and support.', S['body'])],
        [Paragraph('<b>Product & Design Lead</b>', S['h3']), Paragraph('Product-first thinking for UX, product-market fit and roadmap prioritisation.', S['body'])],
    ]
    tt = Table(team_table_data, colWidths=[50*mm, 120*mm])
    tt.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4)]))
    story.append(tt)
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('We supplement our core team with trusted contractors and partner firms for specialised areas such as vision AI, voice AI, and advanced analytics.', S['small']))
    # ══ CASE STUDIES (NEW) ═══════════════════════════════════════════════════
    story.append(SectionHeader('Selected Case Studies', 'Problem → Approach → Outcome'))
    story.append(Spacer(1, 4*mm))

    case_studies = [
        (
            'Defence Operations Platform — Asset & Field Operations platform',
            'Manual asset movement records, delayed field updates, and limited visibility across distributed operational units.',
            'Built a secure field operations platform with asset tracking, approval workflows, issue reporting, role-based dashboards, and central reporting for supervisors.',
            'Improved asset visibility, reduced manual reporting dependency, and enabled faster coordination between field teams and command-level reviewers.'
        ),
        (
            'Sutra — Complete Sales Funnel & Business Automation platform',
            'Leads were coming from multiple channels, but follow-ups, stage tracking, quotation movement, and closure reporting were scattered across calls, sheets, and WhatsApp.',
            'Built a complete sales funnel platform covering lead capture, pipeline stages, automated follow-up reminders, team assignment, quotation tracking, and conversion reports.',
            'Created a single source of truth for the sales team, improved follow-up discipline, and gave management clear visibility into active deals and revenue movement.'
        ),
        (
            'Real Estate CRM — Property sales and broker management platform',
            'Real estate teams were losing enquiries, repeating property explanations, and struggling to track broker activity, site visits, buyer preferences, and deal status.',
            'Designed a CRM with property inventory, enquiry capture, broker allocation, visit scheduling, buyer requirement matching, payment milestones, and sales dashboards.',
            'Reduced lead leakage, improved buyer follow-ups, and helped the sales team track every deal from first enquiry to booking confirmation.'
        ),
        (
            'Aspira — Hiring, internship, and talent matching platform',
            'Institutions and companies needed a structured way to connect students with internships, jobs, mentors, and hiring opportunities without manual coordination overload.',
            'Built a hiring platform with student profiles, company onboarding, job and internship listings, mentor matching, application tracking, and placement reporting.',
            'Improved hiring visibility for colleges and employers, simplified candidate shortlisting, and created a scalable placement ecosystem for students and companies.'
        ),
        (
            'JewelSight AI — Jewellery image recognition software',
            'Jewellery shops needed faster identification of ornaments, design references, and similar product matches from photos, but manual catalog search was slow and inconsistent.',
            'Developed an image recognition workflow that analyzes jewellery photos, detects visual patterns, maps them to catalog items, and supports staff in finding similar designs quickly.',
            'Reduced product search time, improved customer handling during showroom visits, and helped staff recommend matching jewellery designs with more confidence.'
        ),
        (
            'CymaticX Design — Retail design and automation process platform',
            'Repetitive site issues, delays, missing maintenance history, and execution gaps were affecting retail design and on-site delivery.',
            'Built an automated operations platform with site progress tracking, design approvals, ticketing, field forms, and central reporting for project stakeholders.',
            'Improved site execution time, reduced reporting gaps, resolved delays faster, and improved overall execution efficiency.'
        ),
    ]

    for title, problem, approach, outcome in case_studies:
        story.append(Paragraph(
            f'<b>{title}</b><br/>'
            f'<b>Problem:</b> {problem}<br/>'
            f'<b>Approach:</b> {approach}<br/>'
            f'<b>Outcome:</b> {outcome}',
            S['body']
        ))
        story.append(Spacer(1, 3*mm))
    # ══ SYSTEM & ARCHITECTURE (NEW) ═══════════════════════════════════════════
    story.append(SectionHeader('System & Architecture', 'Practical architecture choices for reliability'))
    story.append(Spacer(1, 4*mm))
    arch_text = (
        'We design systems with clear separation of concerns: frontends are stateless and CDN-delivered, APIs are auth-first with role-based access, and data stores are chosen per workload (Postgres for relational, Redis for caching, object stores for blobs). We bake observability and security into every design.'
    )
    story.append(Paragraph(arch_text, S['body']))
    arch_points = [
        'API-first design with OpenAPI contracts and versioning.',
        'Event-driven integrations for decoupling and reliability.',
        'RAG pipelines and guarded model access for AI features.',
        'Staging, canary releases, and automated rollback procedures.',
    ]
    for p in arch_points:
        story.append(Paragraph(f'•  {p}', S['bullet']))

    story.append(Spacer(1, 4*mm))

    # ══ PAGE 2: ABOUT US ═══════════════════════════════════════════════════════
    story.append(SectionHeader('About Us', 'Who We Are & What We Stand For'))
    story.append(Spacer(1, 4*mm))

    about_text = (
        'BuildDreams Technologies is a Nagpur-based software company registered as an MSME enterprise '
        '(UDYAM-MH-20-0340233). We design, build, and deploy production-grade SaaS tools, workflow automation '
        'systems, and enterprise software platforms for businesses across India and beyond.\n\n'
        'We operate at the intersection of three capabilities: <b>building custom software</b> from scratch for '
        'complex enterprise needs, <b>licensing prebuilt products</b> that can be deployed and branded immediately, '
        'and <b>advising businesses</b> on technology strategy, AI integration, and digital transformation.\n\n'
        'Our team has delivered platforms across healthcare, NBFC, government, real estate, manufacturing, logistics, '
        'and education — each built with production discipline, not prototype shortcuts.'
    )
    story.append(Paragraph(about_text, S['body']))
    story.append(Spacer(1, 5*mm))

    # Mission / Vision / Values row
    mvv = [
        ['MISSION', 'Build software that solves real operational problems — not impressive demos — and deploy it in production environments that withstand real-world load.'],
        ['VISION', 'Become the most trusted B2B software partner for mid-market Indian enterprises, known for delivery discipline and product longevity.'],
        ['VALUES', 'Practicality over polish. Reliability over features. Transparency over sales pitch. Long-term partnerships over one-time projects.'],
    ]
    mvv_cells = []
    for label, text in mvv:
        cell_content = [
            [Paragraph(f'<b>{label}</b>', ParagraphStyle('mvvl', fontName='Helvetica-Bold', fontSize=9, textColor=TEAL))],
            [Paragraph(text, ParagraphStyle('mvvt', fontName='Helvetica', fontSize=8.5, textColor=DARK_GRAY, leading=13))],
        ]
        t = Table(cell_content, colWidths=[50*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), LIGHT_GRAY),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        mvv_cells.append(t)

    mvv_table = Table([mvv_cells], colWidths=[54*mm, 54*mm, 56*mm])
    mvv_table.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(mvv_table)
    story.append(Spacer(1, 6*mm))

    # Why BuildDreams
    story.append(Paragraph('<b>Why Companies Choose BuildDreams</b>', S['h2']))
    story.append(Spacer(1, 3*mm))

    why_points = [
        ('Production-first mindset', 'We build for real deployment — offline-first where needed, multi-tenant, load-tested. Not demos.'),
        ('Sector-specific depth', 'Healthcare, NBFC, government kiosks, manufacturing, real estate — we understand operational context before writing code.'),
        ('Prebuilt + Custom hybrid', 'Need speed? License a prebuilt product. Need fit? Customize it. Need something new? We build from scratch.'),
        ('Honest delivery estimates', 'We don\'t oversell timelines. If a project takes 3 months, we tell you 3 months — and deliver in 3 months.'),
        ('Long-term support', 'Post-deployment AMC, feature iterations, and dedicated support — not hand-offs to a helpdesk queue.'),
    ]
    for title, desc in why_points:
        row = Table(
            [[Paragraph(f'<b>→  {title}</b>', ParagraphStyle('wt', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY)),
              Paragraph(desc, ParagraphStyle('wd', fontName='Helvetica', fontSize=8.5, textColor=DARK_GRAY, leading=13))]],
            colWidths=[55*mm, 112*mm]
        )
        row.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('LINEBELOW', (0,0), (-1,-1), 0.3, DIVIDER),
        ]))
        story.append(row)

    story.append(PageBreak())

    # ══ PAGE 3: SERVICES ═══════════════════════════════════════════════════════
    story.append(SectionHeader('Our Services', 'Three Core Capabilities. One Reliable Partner.'))
    story.append(Spacer(1, 4*mm))

    # Service 1
    story.append(Paragraph('01  Custom SaaS & Software Development', S['h2']))
    story.append(HRFlowable(width=170*mm, thickness=0.4, color=TEAL, spaceAfter=3))
    svc1 = (
        'We design and build production-grade SaaS platforms, enterprise workflow systems, and web applications '
        'from the ground up. Every project begins with a requirements audit — we map your actual operational workflows '
        'before a single line of code is written. Deliverables include architecture documentation, staging environments, '
        'and a post-launch support plan.'
    )
    story.append(Paragraph(svc1, S['body']))
    story.append(Spacer(1, 2*mm))

    svc1_items = [
        'Multi-tenant SaaS platforms with role-based access control',
        'Workflow automation (approval chains, ticket routing, escalation logic)',
        'AI-powered features: RAG pipelines, vision AI, voice AI, chatbots',
        'WhatsApp Business API integrations and communication automation',
        'Custom ERP modules, reporting dashboards, and admin portals',
        'Offline-first architectures for low-connectivity environments',
    ]
    for item in svc1_items:
        story.append(Paragraph(f'&#x2022;  {item}', S['bullet']))
    story.append(Spacer(1, 5*mm))

    # Service 2
    story.append(Paragraph('02  Prebuilt Product Licensing', S['h2']))
    story.append(HRFlowable(width=170*mm, thickness=0.4, color=TEAL, spaceAfter=3))
    svc2 = (
        'We maintain a portfolio of 13+ production-ready SaaS products across verticals. These can be licensed as-is, '
        'white-labeled under your brand, or customized to your specific workflows. Deployment timelines of 2–4 weeks '
        'vs. 3–6 months for custom builds — ideal when speed to market is critical.'
    )
    story.append(Paragraph(svc2, S['body']))
    story.append(Spacer(1, 2*mm))

    svc2_items = [
        'White-label licensing with your branding and domain',
        'Configuration-based customization (no re-engineering required)',
        'API access for integration with your existing systems',
        'Dedicated onboarding and training support',
        'SLA-backed hosting or on-premise deployment options',
    ]
    for item in svc2_items:
        story.append(Paragraph(f'&#x2022;  {item}', S['bullet']))
    story.append(Spacer(1, 5*mm))

    # Service 3
    story.append(Paragraph('03  Technology Consultancy', S['h2']))
    story.append(HRFlowable(width=170*mm, thickness=0.4, color=TEAL, spaceAfter=3))
    svc3 = (
        'For businesses that need a technology partner rather than just a vendor, we offer strategic consultancy '
        'engagements. We assess your current stack, identify technical debt, recommend architectures, and build '
        'product roadmaps. We also guide AI adoption — separating genuine use cases from hype.'
    )
    story.append(Paragraph(svc3, S['body']))
    story.append(Spacer(1, 2*mm))

    svc3_items = [
        'Technology stack audit and modernisation roadmaps',
        'AI readiness assessments and integration strategy',
        'Product architecture design and documentation',
        'Vendor evaluation and procurement advisory',
        'CTO-as-a-Service for early-stage startups and growing SMEs',
    ]
    for item in svc3_items:
        story.append(Paragraph(f'&#x2022;  {item}', S['bullet']))

    story.append(Spacer(1, 5*mm))

    # Engagement models
    story.append(Paragraph('<b>Engagement Models</b>', S['h3']))
    story.append(Spacer(1, 2*mm))
    eng_data = [
        ['Fixed-Price Projects', 'Retainer / AMC', 'License + Support', 'Consulting Sprint'],
        [
            'Defined scope, timeline,\nand milestone payments.',
            'Monthly retainer for\nongoing development\nand maintenance.',
            'One-time product license\nfee + annual support\ncontract.',
            'Short-term (2–8 week)\nfocused advisory\nengagements.',
        ]
    ]
    eng_table = Table(eng_data, colWidths=[41*mm, 41*mm, 41*mm, 41*mm])
    eng_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BACKGROUND', (0,1), (-1,-1), LIGHT_GRAY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('TEXTCOLOR', (0,1), (-1,-1), DARK_GRAY),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.3, WHITE),
    ]))
    story.append(eng_table)

    story.append(PageBreak())

    # ══ PAGE 4: SOLUTIONS & LICENSING ═════════════════════════════════════════
    story.append(SectionHeader('Solutions & Licensing', 'Enterprise-grade platforms, licensing, and bespoke builds'))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph(
        'We offer production-ready platforms that can be licensed and configured for rapid deployment, as well as fully bespoke builds when organisations need tailored workflows and integrations. Our approach balances time-to-market with maintainability and integration flexibility so customers receive a supported, long-term solution, not a brittle prototype.',
        S['body']
    ))
    story.append(Spacer(1, 3*mm))

    licensing_info = [
        ('License (Fast Deploy)', 'Configuration, white-labeling, and integration for rapid time-to-value — ideal when speed and proven reliability matter.'),
        ('Custom Build (Fit & Scale)', 'Discovery-led bespoke development with architecture, iterative sprints, and staging environments to match complex operational needs.'),
        ('Support & Hosting', 'SLA-backed support, annual maintenance contracts, and flexible hosting (cloud, VPS, or on-premise) to ensure long-term stability.'),
    ]

    lic_cells = []
    for title, desc in licensing_info:
        t = Table([[Paragraph(f'<b>{title}</b>', S['h3'])], [Paragraph(desc, S['body'])]], colWidths=[170*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), LIGHT_GRAY),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        lic_cells.append(t)

    # Stack them vertically for a clean, corporate layout
    for cell in lic_cells:
        story.append(cell)
        story.append(Spacer(1, 4*mm))

    story.append(PageBreak())

    # ══ PAGE 5: SECTORS + TECH + PROCESS ══════════════════════════════════════
    story.append(SectionHeader('Sectors & Technology', 'Proven Across Industries. Built on Modern Stack.'))
    story.append(Spacer(1, 4*mm))

    # Sectors
    story.append(Paragraph('<b>Sectors We Serve</b>', S['h2']))
    story.append(Spacer(1, 2*mm))

    sectors = [
        ('Banking & NBFC', 'Compliance dashboards, agent monitoring, KYC workflow, audit log systems.'),
        ('Healthcare', 'Front-desk locking, patient flow management, diagnostic chain operations.'),
        ('Government & PSU', 'CSC kiosk management, citizen service portals, multi-location monitoring.'),
        ('Manufacturing & MRO', 'Visual parts recognition, inventory automation, maintenance ticketing.'),
        ('Real Estate', 'Property marketplaces, buyer verification portals, project progress tracking.'),
        ('Education & EdTech', 'Career platforms, student management, mentor-company matching ecosystems.'),
        ('Logistics & Fleet', 'Fleet tracking, route management, driver compliance and reporting.'),
        ('Hospitality & Retail', 'QR-based loyalty, reward disbursement, multi-outlet management.'),
    ]
    sec_rows = []
    for i in range(0, len(sectors), 2):
        row = []
        for j in [i, i+1]:
            if j < len(sectors):
                name, desc = sectors[j]
                cell = Table(
                    [[Paragraph(f'<b>{name}</b>', ParagraphStyle('sn', fontName='Helvetica-Bold', fontSize=8.5, textColor=NAVY))],
                     [Paragraph(desc, ParagraphStyle('sd', fontName='Helvetica', fontSize=8, textColor=DARK_GRAY, leading=12))]],
                    colWidths=[81*mm]
                )
                cell.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), LIGHT_GRAY),
                    ('TOPPADDING', (0,0), (-1,-1), 4),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                    ('LEFTPADDING', (0,0), (-1,-1), 5),
                    ('RIGHTPADDING', (0,0), (-1,-1), 5),
                    ('LINERIGHT', (0,0), (0,-1), 2.5, TEAL),
                ]))
                row.append(cell)
            else:
                row.append(Spacer(81*mm, 1))
        sec_rows.append(row)

    sec_table = Table(sec_rows, colWidths=[84*mm, 84*mm])
    sec_table.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(sec_table)
    story.append(Spacer(1, 6*mm))

    # Tech stack
    story.append(Paragraph('<b>Technology Stack</b>', S['h2']))
    story.append(Spacer(1, 2*mm))

    tech_categories = [
        ('Frontend', 'React, Next.js, Tailwind CSS, HTML5/CSS3, GSAP, Lenis'),
        ('Backend', 'Node.js, Python (FastAPI/Django), REST APIs, WebSockets'),
        ('AI / ML', 'OpenAI GPT, Claude API, RAG pipelines, Vision AI, Whisper'),
        ('Databases', 'PostgreSQL, MongoDB, MySQL, Redis, SQLite (offline-first)'),
        ('Infrastructure', 'Vercel, AWS, Docker, Nginx, Linux VPS, On-Premise'),
        ('Integrations', 'WhatsApp Business API, Razorpay, Stripe, Twilio, Slack, Email SMTP'),
    ]
    tech_rows = []
    for i in range(0, len(tech_categories), 2):
        row = []
        for j in [i, i+1]:
            if j < len(tech_categories):
                cat, items = tech_categories[j]
                content = f'<b><font color="#009599">{cat}:</font></b>  {items}'
                row.append(Paragraph(content, ParagraphStyle('tech', fontName='Helvetica', fontSize=8.5, textColor=DARK_GRAY, leading=13)))
            else:
                row.append(Spacer(1,1))
        tech_rows.append(row)

    tech_table = Table(tech_rows, colWidths=[84*mm, 84*mm])
    tech_table.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, DIVIDER),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 6*mm))

    # Delivery Process
    story.append(Paragraph('<b>Our Delivery Process</b>', S['h2']))
    story.append(Spacer(1, 2*mm))

    steps = [
        ('01', 'Discovery', 'Requirements workshop, operational workflow mapping, constraint identification.'),
        ('02', 'Architecture', 'System design, database schema, API contracts, tech stack finalisation.'),
        ('03', 'Build', 'Iterative sprints with staging deployments. Client reviews at each milestone.'),
        ('04', 'QA & Testing', 'Load testing, edge case coverage, security review, UAT with client team.'),
        ('05', 'Deploy', 'Production deployment, documentation handover, team training.'),
        ('06', 'Support', 'Post-launch monitoring, bug fixes, AMC, and iteration planning.'),
    ]
    step_cells = []
    for num, title, desc in steps:
        cell = Table(
            [[Paragraph(f'<b>{num}</b>', ParagraphStyle('sn', fontName='Helvetica-Bold', fontSize=14, textColor=TEAL))],
             [Paragraph(f'<b>{title}</b>', ParagraphStyle('st', fontName='Helvetica-Bold', fontSize=8.5, textColor=NAVY))],
             [Paragraph(desc, ParagraphStyle('sd', fontName='Helvetica', fontSize=7.5, textColor=DARK_GRAY, leading=11))]],
            colWidths=[26*mm]
        )
        cell.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), LIGHT_GRAY),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('LINEABOVE', (0,0), (-1,0), 2.5, NAVY),
        ]))
        step_cells.append(cell)

    step_table = Table([step_cells[:3], step_cells[3:]], colWidths=[28*mm, 28*mm, 28*mm, 28*mm, 28*mm, 28*mm][:3])
    step_table = Table([step_cells[:3], step_cells[3:]], colWidths=[56*mm, 56*mm, 56*mm])
    step_table.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(step_table)

    story.append(PageBreak())

    # ══ PAGE 6: TESTIMONIALS + ACHIEVEMENTS + CONTACT ══════════════════════════
    story.append(SectionHeader('Client Testimonials', 'Real Results from Real Deployments'))
    story.append(Spacer(1, 4*mm))

    testimonials = [
        ('Priya Sharma', 'Private NBFC · Mumbai',
         'We had 22 KYC desks across 4 branches and zero visibility into what agents were doing. FlowGuard gave us a live compliance dashboard in 2 weeks. Our team saved 6 hours a week on manual log verification.'),
        ('Ramesh Patil', 'Government Services Integrator · Nashik',
         'We deployed FlowGuard across 40 government CSC kiosks in three districts. The offline-first architecture was the deciding factor — our locations have unreliable connectivity. No missed filings since go-live.'),
        ('Dr. Anand Mehta', 'Diagnostic Chain · Pune',
         'Front-desk PCs were being used for personal browsing during patient check-in. After FlowGuard, every interaction is logged and browser-locked. Works perfectly even when our hospital\'s internet drops.'),
        ('Rohan Iyer', 'Operations Lead · Bangalore',
         'Our team stopped missing follow-ups. The workflow system gives us a clear daily run-of-show. We went from chaos to clarity in about three weeks of deployment.'),
    ]

    test_rows = []
    for name, company, quote in testimonials:
        cell = Table(
            [[Paragraph(f'"  {quote}  "', ParagraphStyle('tq', fontName='Helvetica', fontSize=8.5, textColor=DARK_GRAY, leading=13, fontStyle='italic'))],
             [Paragraph(f'<b>{name}</b>  <font color="#8892A4">·  {company}</font>', ParagraphStyle('tn', fontName='Helvetica', fontSize=8, textColor=NAVY))]],
            colWidths=[80*mm]
        )
        cell.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL_PALE),
            ('BACKGROUND', (0,1), (-1,-1), LIGHT_GRAY),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('LINERIGHT', (0,0), (0,-1), 3, TEAL),
        ]))
        test_rows.append(cell)

    for i in range(0, len(test_rows), 2):
        row = [test_rows[i]]
        if i+1 < len(test_rows):
            row.append(test_rows[i+1])
        t = Table([row], colWidths=[84*mm, 84*mm])
        t.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), 2),
            ('RIGHTPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(t)

    story.append(Spacer(1, 6*mm))

    # Achievements + Certifications
    story.append(SectionHeader('Recognition & Credentials'))
    story.append(Spacer(1, 3*mm))

    ach_data = [
        ['MSME Registered\nUDYAM-MH-20-0340233', '50+ Institutions\nServed Across India', '50,000+ Students\nImpacted', '200+ Companies\nOnboarded'],
        ['Registered Office\nNagpur, Maharashtra', '13+ Production\nSaaS Products', 'Offline-First\nArchitecture Expertise', 'AI Integration\nAcross 5+ Products'],
    ]
    ach_table = Table(ach_data, colWidths=[42*mm, 42*mm, 42*mm, 42*mm])
    ach_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('TEXTCOLOR', (0,0), (-1,-1), WHITE),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#0A2460')),
        ('LINEABOVE', (0,0), (-1,0), 3, TEAL),
    ]))
    story.append(ach_table)

    story.append(Spacer(1, 6*mm))

    # Contact
    story.append(SectionHeader('Get In Touch', 'Let\'s Build Something That Actually Works'))
    story.append(Spacer(1, 3*mm))

    contact_body = (
        'Whether you\'re evaluating a product license, scoping a custom build, or need a technology strategy session — '
        'reach out. We respond within 1 business day and offer a free 30-minute discovery call for all new enquiries.'
    )
    story.append(Paragraph(contact_body, S['body']))
    story.append(Spacer(1, 4*mm))

    contact_info = [
        ['Website', 'builddreams.co.in'],
        ['Email', 'suhomatech@gmail.com'],
        ['Phone', '+91 93568 73562'],
        ['Address', 'Plot No. 11, Maa Padmavati Nagar, Bokde Layout, Nagpur 440034, Maharashtra, India'],
        ['Registration', 'UDYAM-MH-20-0340233 · MSME Registered Enterprise'],
    ]

    ci_rows = []
    for label, value in contact_info:
        ci_rows.append([
            Paragraph(f'<b>{label}</b>', ParagraphStyle('cl', fontName='Helvetica-Bold', fontSize=9, textColor=TEAL)),
            Paragraph(value, ParagraphStyle('cv', fontName='Helvetica', fontSize=9, textColor=DARK_GRAY)),
        ])
    ci_table = Table(ci_rows, colWidths=[28*mm, 140*mm])
    ci_table.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, DIVIDER),
    ]))
    story.append(ci_table)

    story.append(Spacer(1, 6*mm))

    # Final CTA banner
    cta_data = [['  Ready to build? Request an intro call — builddreams.co.in  ']]
    cta = Table(cta_data, colWidths=[170*mm])
    cta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), TEAL),
        ('TEXTCOLOR', (0,0), (-1,-1), WHITE),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(cta)

    # Build
    doc.build(story, canvasmaker=FooterCanvas)
    print('Done:', OUTPUT)

if __name__ == '__main__':
    build()
