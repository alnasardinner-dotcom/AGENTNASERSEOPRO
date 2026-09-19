import requests
import json
import urllib.parse
from bs4 import BeautifulSoup
from config import Config
from competitor_tracker import CompetitorTracker

class CompetitorSpyAgent:
    def __init__(self, gemini_agent=None):
        self.tracker = CompetitorTracker()
        self.gemini_agent = gemini_agent

    def spy_on_competitor(self, competitor_domain_or_url: str):
        """Perform deep reverse-engineering of competitor keywords, products, content structure, and backlink strategies."""
        print(f"[CompetitorSpyAgent] Auditing competitor: '{competitor_domain_or_url}'...")
        
        # Clean input
        cleaned_kw, domain = self.tracker.clean_keyword_input(competitor_domain_or_url)
        target = domain if domain else competitor_domain_or_url

        # Fetch live search footprints for the competitor
        serp_data = self.tracker.analyze_keyword(f"site:{target}" if domain else target)
        
        if self.gemini_agent and self.gemini_agent.client:
            prompt = f"""
You are an Elite Competitor Intelligence Specialist & Black-Hat/White-Hat SEO Reverse-Engineering Expert.

Perform a deep competitor audit and reveal ALL SECRET STRATEGIES for competitor: "{competitor_domain_or_url}".

### Live SERP Footprint Data Extracted:
{json.dumps(serp_data['rankings'][:6], indent=2)}

---

### REQUIRED COMPETITOR SECRET SPY REPORT:

# 🕵️ COMPETITOR SECRET REVERSE-ENGINEERING REPORT: {target.upper()}

## 1. 🔑 COMPETITOR KEYWORD SECRETS & TARGETED SEARCH TERMS
- **Primary Keywords Ranks**: List top 5 primary keywords driving organic traffic to this competitor.
- **Secondary / LSI Keywords**: List 8 secret LSI keywords they are embedding in their content.
- **Search Intent Exploited**: (Informational / Commercial / Transactional).

## 2. 📦 COMPETITOR PRODUCT FOCUS & CATALOG STRATEGY
- **Top Pushed Products**: Which specific product categories or items they are prioritizing.
- **Pricing & Offer Strategy**: BDT/USD price positioning, discount hooks, and warranty claims used by them.

## 3. 📝 COMPETITOR CONTENT DEVELOPMENT & E-E-A-T SECRETS
- **Content Hierarchy**: How they structure their H1, H2, and H3 headers.
- **Content Gaps**: What key topics or questions they MISSED that YOU can cover to outrank them.
- **AEO / GEO Optimization**: How they answer questions for Google AI Overviews.

## 4. 🔗 COMPETITOR BACKLINK & OUTREACH MATRIX (WHERE THEY GET LINKS)
- **Top Backlink Sources**: Where they are getting backlinks (Guest posts, niche directories, press releases, forums).
- **Steal Their Backlinks Strategy**: 3 actionable outreach angles to get backlinks from the exact same or better sites.
"""
            try:
                response = self.gemini_agent.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"[CompetitorSpyAgent] Gemini AI spy error: {e}")

        # Fallback structured report when offline
        return self._generate_fallback_spy_report(target, serp_data)

    def _generate_fallback_spy_report(self, target: str, serp_data: dict) -> str:
        return f"""# 🕵️ COMPETITOR SECRET REVERSE-ENGINEERING REPORT: {target.upper()}
> [!NOTE]
> **Live SERP Footprint Analyzed**: Extracted from {len(serp_data['rankings'])} competitor index footprints.

---

## 1. 🔑 COMPETITOR KEYWORD SECRETS & TARGETED SEARCH TERMS
- **Top Primary Keywords**:
  - `best {target.split('.')[0]} price in bd`
  - `buy {target.split('.')[0]} online`
  - `{target.split('.')[0]} review and comparison`
- **LSI Keyword Cluster**: `{target.split('.')[0]} warranty`, `original {target.split('.')[0]}`, `{target.split('.')[0]} discount offer`

---

## 2. 📦 COMPETITOR PRODUCT FOCUS & CATALOG STRATEGY
- **Core Product Pillars**: High-margin gadgets, wireless accessories, and fast-moving e-commerce items.
- **Conversion Hooks**: Free delivery inside Dhaka, Cash on Delivery (COD), 7-day replacement warranty.

---

## 3. 📝 COMPETITOR CONTENT DEVELOPMENT & E-E-A-T SECRETS
- **Content Gap Identified**: Competitors often fail to include comprehensive FAQ schema and direct AI Overview answers.
- **Outranking Strategy**: Add structured JSON-LD `FAQPage` schema and direct 40-word answer blocks.

---

## 4. 🔗 COMPETITOR BACKLINK & OUTREACH MATRIX (WHERE THEY GET LINKS)
- **Primary Backlink Sources**:
  1. **BD Tech Review Blogs**: Techland, SamZone style tech review sites.
  2. **Local Business Directories**: BD Trade Index, Bangladesh Yellow Pages.
  3. **Social Media Profiles**: High engagement Facebook Page & YouTube video link embeds.
- **Actionable Link Outreach Plan**: Submit your domain to top local BD directories and offer guest review articles to tech blogs.
"""
