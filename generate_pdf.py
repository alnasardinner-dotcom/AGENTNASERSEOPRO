import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_both_pdfs():
    folder_proj = os.path.join(os.path.dirname(__file__), "PDF_REPORTS")
    folder_scratch = r"C:\Users\DFIT\.gemini\antigravity\scratch\PDF_REPORTS"

    os.makedirs(folder_proj, exist_ok=True)
    os.makedirs(folder_scratch, exist_ok=True)

    pdf1_path = os.path.join(folder_proj, "1_AGENT_NASER_SEO_PRO_ENGLISH_MANUAL.pdf")
    build_english_pdf(pdf1_path)

    shutil.copy(pdf1_path, os.path.join(folder_scratch, "1_AGENT_NASER_SEO_PRO_ENGLISH_MANUAL.pdf"))
    print(f"✅ Updated 14-Module English PDF generated at: {pdf1_path}")

def build_english_pdf(pdf_path):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle1',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1E3A8A'),
        fontName='Helvetica-Bold',
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle1',
        parent=styles['Normal'],
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#475569'),
        fontName='Helvetica',
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        'SectionH2_1',
        parent=styles['Heading2'],
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1E3A8A'),
        fontName='Helvetica-Bold',
        spaceBefore=12,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body1',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1E293B'),
        fontName='Helvetica',
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet1',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        fontName='Helvetica',
        leftIndent=10,
        spaceAfter=3
    )

    elements = []

    # Title & Header
    elements.append(Paragraph("AGENT NASER SEO PRO - OFFICIAL ENGLISH MANUAL (14 MODULES)", title_style))
    elements.append(Paragraph("Autonomous AI Search & Competitor Intelligence SaaS Engine | Creator: Abdullah Al Naser (+8801678684141)", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceAfter=10))

    elements.append(Paragraph("<b>EXECUTIVE PLATFORM SUMMARY:</b><br/>AGENT NASER SEO PRO is an enterprise-grade autonomous AI search engine intelligence & web scraping automation platform designed to reverse-engineer competitor ranking strategies, generate 1-click ready-to-paste SEO code fixes, scrape contact details & WHOIS data, automate AEO/GEO content, track exact Google SERP positions, and audit site indexing.", body_style))
    elements.append(Spacer(1, 8))

    modules_eng = [
        ("1. ⚡ 1-Click AI SEO Auto-Fixer & Rank Healer", "Automated SEO Code & Content Generator", "Diagnoses page gaps vs top Google SERP competitors and generates copy-paste ready fix code (Meta tags, AEO AI Answer blocks, LSI paragraphs & JSON-LD schema).", "Eliminates guess work by producing exact HTML/Markdown fix code to boost rankings into Top 3."),
        ("2. 🌐 Master Web Scraper, WHOIS & Site Clone", "Deep Contact, WHOIS & HTML Extractor", "Scrapes business phone numbers, email addresses, physical locations, Facebook/WhatsApp links, WHOIS domain owner details, live prices, tech stack scripts, and clean HTML clone templates.", "Enables instant lead generation, site auditing, tech stack inspection, and layout template cloning."),
        ("3. 🚀 360° Master Hub", "All-in-One Intelligence Generator", "Executes full 360-degree audit for any keyword/product. Combines live SERP rankings, competitor strategies, social media hooks, and 1000+ word AEO/GEO article generation.", "Saves 10+ hours of manual audit work. Gives immediate actionable strategy to rank #1 on Google & AI Overviews."),
        ("4. 🕵️ Competitor Spy Agent", "Competitor Secret Reverse-Engineering", "Extracts competitor secret keywords, product focus, content hierarchy, and backlink source matrix.", "Reveals competitor weaknesses and secret sources, enabling you to outrank them with ease."),
        ("5. 🎯 Keyword Rank Tracker", "Exact Google SERP Position Auditor", "Audits live rank positions (#1-25, Page 1, Page 2+, Unranked 30+) for target keywords across Google SERPs.", "Provides exact visibility score and action plan to push #4-10 keywords into Top 3 positions."),
        ("6. 📍 Local SEO & GMB Suite", "Google Maps 3-Pack Optimization", "Generates GMB categories, 750-char description, local citations, LocalBusiness JSON-LD schema, and review strategies.", "Drives high-converting local phone calls, store visits, and Google Maps 3-Pack domination."),
        ("7. 📦 Amazon FBA & Affiliate", "Amazon Listing & Review Optimizer", "Generates Amazon product titles, 5 benefit bullet points, backend search terms, affiliate reviews, and Product JSON-LD schema.", "Increases Amazon FBA seller conversion rates (CVR) and boosts affiliate commissions."),
        ("8. 🛍️ Shopify & Dropshipping", "Shopify Product & Collection Suite", "Creates copy-paste Shopify metadata, high-converting product descriptions, collection linking strategy, and Product schema.", "Maximizes e-commerce organic sales and elevates Shopify product page search rankings."),
        ("9. ✍️ Blogger & Niche Content", "Google E-E-A-T Content Suite", "Produces CTR-optimized blog titles, search descriptions, E-E-A-T articles, and FAQPage schema for Perplexity & AI Overviews.", "Ensures placement in Google AI Overviews and dramatically increases AdSense & Affiliate revenue."),
        ("10. 🔴🟢 Google Index Audit", "Full Site Sitemap & Indexing Checker", "Auto-crawls sitemaps, verifies Google index status (`site:` audit), identifies non-indexed URLs, and gives 5-step GSC fix plan.", "Fixes indexation issues so all website pages get indexed and discovered by Google bots."),
        ("11. 📱 Social Media Viral Extractor", "Reels, TikTok & Shorts Hook Generator", "Extracts viral video hooks, promotional scripts, and high-converting ad copies for Facebook, TikTok, and YouTube.", "Reduces social media ad costs while driving viral organic reach and store conversions."),
        ("12. 🌐 Global Market Trends", "Industrial & Category Trend Scanner", "Scans worldwide & local product trends across IT, Computer, Networking, Printing, SOHO, Industrial Machinery, and CNC.", "Identifies high-margin trending products before competitors to dominate new markets."),
        ("13. 📡 24/7 Activity Stream", "Real-time Operations Log Stream", "Logs every single live scan, audit, timestamp, and status across the platform.", "Ensures total operational transparency and system logging for agency teams."),
        ("14. 💳 Multi-Tenant SaaS Engine", "Monetization & Role Access Suite", "Built-in Master Admin, Paid User, and Public Demo role permissions with ready subscription tiers.", "Enables you to sell monthly SaaS subscriptions or client services to generate recurring income.")
    ]

    for title, subtitle, desc, benefit in modules_eng:
        mod_content = []
        mod_content.append(Paragraph(f"<b>{title}</b> - <i>{subtitle}</i>", h2_style))
        mod_content.append(Paragraph(f"<b>Core Functionality:</b> {desc}", body_style))
        mod_content.append(Paragraph(f"<b>Key Business Benefit:</b> {benefit}", bullet_style))
        mod_content.append(Spacer(1, 3))
        elements.append(KeepTogether(mod_content))

    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))
    elements.append(Paragraph("<b>System Creator & Support:</b> Abdullah Al Naser (+8801678684141 | WhatsApp Direct Available)", body_style))

    doc.build(elements)

if __name__ == "__main__":
    generate_both_pdfs()
