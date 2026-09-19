import os
from config import Config
try:
    from templates.seo_prompt import SEOPromptTemplate
except ModuleNotFoundError:
    from seo_prompt import SEOPromptTemplate

try:
    from templates.shopify_seo import ShopifySEOPromptTemplate
except ModuleNotFoundError:
    from shopify_seo import ShopifySEOPromptTemplate

try:
    from templates.amazon_seo import AmazonSEOPromptTemplate
except ModuleNotFoundError:
    from amazon_seo import AmazonSEOPromptTemplate

try:
    from templates.blogger_seo import BloggerSEOPromptTemplate
except ModuleNotFoundError:
    from blogger_seo import BloggerSEOPromptTemplate

try:
    from templates.local_gmb_seo import LocalGMBSEOPromptTemplate
except ModuleNotFoundError:
    from local_gmb_seo import LocalGMBSEOPromptTemplate

class SEOWriterAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.GEMINI_API_KEY
        self.client = None
        self._init_client()

    def generate_local_gmb_seo(self, business_name: str, location: str = "Dhaka, Bangladesh", user_notes: str = "") -> str:
        prompt = LocalGMBSEOPromptTemplate.get_local_gmb_seo_prompt(business_name, location, user_notes)
        if self.client:
            try:
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"[SEOWriterAgent] Local GMB Gemini API error: {e}")
        return self._generate_offline_gmb_template(business_name, location)

    def _generate_offline_gmb_template(self, business_name: str, location: str) -> str:
        return f"""# 📍 GOOGLE MY BUSINESS (GMB) & LOCAL SEO SUITE: {business_name.upper()}

## SECTION 1: GOOGLE BUSINESS PROFILE (GMB) OPTIMIZER
- **GMB Business Name**: {business_name.title()} - Best Services in {location}
- **Primary GMB Category**: Internet & Marketing Services / Retail Store
- **Secondary Categories**: E-Commerce Store, Tech Shop, Business Consultant
- **GMB Description (750 Chars)**: Welcome to {business_name.title()} located in {location}. We offer high quality products and services with 100% customer satisfaction guarantee, official warranty, and fast home delivery. Contact us today!

---

## SECTION 2: GOOGLE MAPS 3-PACK STRATEGY
- Local Keyword 1: `best {business_name.lower()} in {location}`
- Local Keyword 2: `{business_name.lower()} near me`

---

## SECTION 3: LOCALBUSINESS JSON-LD SCHEMA
```json
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "{business_name}",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "{location}",
    "addressCountry": "BD"
  }}
}}
```
"""


    def generate_amazon_seo(self, keyword: str, competitor_insights: dict = None, user_notes: str = "") -> str:
        prompt = AmazonSEOPromptTemplate.get_amazon_seo_prompt(keyword, competitor_insights, user_notes)
        if self.client:
            try:
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"[SEOWriterAgent] Amazon Gemini API error: {e}")
        return self._generate_offline_amazon_template(keyword)

    def generate_blogger_seo(self, keyword: str, competitor_insights: dict = None, user_notes: str = "") -> str:
        prompt = BloggerSEOPromptTemplate.get_blogger_seo_prompt(keyword, competitor_insights, user_notes)
        if self.client:
            try:
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"[SEOWriterAgent] Blogger Gemini API error: {e}")
        return self._generate_offline_blogger_template(keyword)

    def _generate_offline_amazon_template(self, keyword: str) -> str:
        return f"""# 📦 AMAZON FBA & AFFILIATE SEO SUITE: {keyword.upper()}

## SECTION 1: AMAZON LISTING OPTIMIZER
- **Amazon Title**: Premium {keyword.title()} for Gaming & Work - High Performance Compact Design
- **Bullet 1**: **ULTIMATE ERGONOMIC DESIGN** - Engineered for maximum comfort during long hours.
- **Bullet 2**: **HIGH PRECISION SENSORS** - Fast response time with zero latency.
- **Bullet 3**: **LONG BATTERY LIFE** - Rechargeable battery offering up to 50 hours of continuous use.
- **Bullet 4**: **WIDE COMPATIBILITY** - Plug-and-play support for Windows, macOS, and Linux.
- **Bullet 5**: **OFFICIAL WARRANTY** - 100% authentic quality backed by 1-year replacement warranty.

---

## SECTION 2: AMAZON AFFILIATE REVIEW BLOG
# {keyword.title()} Review: Is It Worth Buying in 2026?
If you are looking for an affordable, high quality **{keyword}**, this comprehensive review breaks down specs, performance, and pros & cons.
"""

    def _generate_offline_blogger_template(self, keyword: str) -> str:
        return f"""# ✍️ BLOGGER & NICHE CONTENT SEO SUITE: {keyword.upper()}

## SECTION 1: BLOGGER METADATA
- **Blog Title**: Master {keyword.title()} in 2026: Complete Niche Guide
- **Search Description**: Looking for expert tips on {keyword}? Read our ultimate guide covering features, reviews, and step-by-step strategies.
- **Permalink**: {keyword.lower().replace(' ', '-')}

---

## SECTION 2: BLOGGER ARTICLE
# The Ultimate Guide to {keyword.title()}

## Introduction
Whether you are a beginner or experienced enthusiast, understanding **{keyword}** is key to getting the best results.

## Key Insights & Takeaways
1. Focus on quality and authentic specifications.
2. Optimize your workflow with proven strategies.
"""


    def generate_shopify_seo(self, keyword: str, competitor_insights: dict = None, user_notes: str = "") -> str:
        prompt = ShopifySEOPromptTemplate.get_shopify_seo_prompt(keyword, competitor_insights, user_notes)
        if self.client:
            try:
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"[SEOWriterAgent] Shopify Gemini API error: {e}")
        return self._generate_offline_shopify_template(keyword)

    def _generate_offline_shopify_template(self, keyword: str) -> str:
        return f"""# 🛍️ SHOPIFY E-COMMERCE SEO SUITE: {keyword.upper()}

## SECTION 1: SHOPIFY METADATA (COPY-PASTE FOR SHOPIFY ADMIN)
- **Shopify Page Title**: Buy Best {keyword.title()} in 2026 | Fast Delivery & Warranty
- **Shopify Meta Description**: Order authentic {keyword} at best price. Cash on delivery inside Dhaka & nationwide 24h delivery. Get your deal today!
- **Shopify URL Handle**: products/best-{keyword.lower().replace(' ', '-')}-bd
- **Primary Keyword**: {keyword}
- **Secondary Keywords**: {keyword} price in bd, buy {keyword} online, best {keyword} shopify

---

## SECTION 2: SHOPIFY PRODUCT DESCRIPTION (H1, H2, H3)

# Authentic {keyword.title()} - Premium Quality

## Product Overview
Upgrade your daily routine with high-performance **{keyword}**. Built with durable materials, ergonomic design, and official warranty.

## Key Features & Specifications
- **High Efficiency Performance**: Designed for maximum speed and longevity.
- **Ergonomic Build Quality**: Sleek lightweight design with premium finish.
- **24/7 Customer Support & Warranty**: 7-day replacement guarantee.

---

## SECTION 3: SHOPIFY FAQ & JSON-LD SCHEMA

```json
{{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "{keyword}",
  "offers": {{
    "@type": "Offer",
    "priceCurrency": "BDT",
    "availability": "https://schema.org/InStock"
  }}
}}
```

---

## SECTION 4: SHOPIFY ON-PAGE STRATEGY
- Internal Link: Link to `/collections/all` with anchor text "{keyword} collection".
- Image Alt Tag: `authentic-{keyword.lower().replace(' ', '-')}-shopify.jpg`
"""


    def _init_client(self):
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[SEOWriterAgent] google-genai SDK init notice: {e}")

    def generate_content(self, keyword: str, competitor_insights: dict = None, user_notes: str = "") -> str:
        prompt = SEOPromptTemplate.get_article_prompt(keyword, competitor_insights, user_notes)
        
        if self.client:
            try:
                # Using Gemini 2.5/2.0 Flash model via google-genai SDK
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"[SEOWriterAgent] Gemini API generation error: {e}")
                # Fallback model attempt
                try:
                    response = self.client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=prompt
                    )
                    if response and response.text:
                        return response.text
                except Exception as e2:
                    print(f"[SEOWriterAgent] Gemini 2.0 API generation error: {e2}")

        # Fallback template output when Gemini API Key is not set or API call fails
        return self._generate_offline_template(keyword, competitor_insights)

    def _generate_offline_template(self, keyword: str, competitor_insights: dict = None) -> str:
        """Returns structured SEO document template when offline or API key missing."""
        comp_info = ""
        if competitor_insights and competitor_insights.get("rankings"):
            comp_info = f"\nCompetitors Analyzed: {len(competitor_insights['rankings'])} top domains.\n"

        return f"""# SEO / AEO / GEO Strategy & Content Report
> [!NOTE]
> **API Key Notice**: Add your `GEMINI_API_KEY` to `.env` or `config.py` for full live AI generation.

## 🎯 Target Keyword: `{keyword}`
{comp_info}

---

# SECTION 1: METADATA & HEADERS (SEO OPTIMIZED)
- **SEO Title**: Master {keyword.title()} in 2026: Complete Strategy & Buyer Guide
- **Meta Description**: Looking for the best insights on {keyword}? Read our expert guide covering top features, comparisons, and implementation strategies.
- **Primary Keyword**: {keyword}
- **Secondary / LSI Keywords**: {keyword} review, best {keyword} 2026, {keyword} guide, top {keyword} features, {keyword} comparison
- **URL Slug**: best-{keyword.lower().replace(' ', '-')}-guide

---

# SECTION 2: AEO & GEO DIRECT ANSWER SUMMARY (FOR AI SEARCH OVERVIEWS)
> **AI Direct Answer**: {keyword.title()} refers to strategic tools and methodologies designed to optimize ranking, user experience, and search visibility on both traditional search engines (Google) and Generative AI engines (Perplexity, AI Overviews). Selecting the right strategy requires analyzing competitor gap data and optimizing for semantic search intent.

---

# SECTION 3: FULL ARTICLE STRUCTURE

# The Ultimate Guide to {keyword.title()} in 2026

## Introduction
In today's evolving digital search landscape, mastering **{keyword}** is essential for staying ahead of competitors. Search engines now evaluate content not just on keywords, but on entity authority and direct answer clarity.

## Key Features & Competitor Analysis
When analyzing top-ranking pages for *{keyword}*, leading competitors focus on three core pillars:
1. **User Experience & Fast Page Loading**
2. **Comprehensive Topic Coverage**
3. **Structured Data & FAQ Integration**

### Detailed Feature Breakdown
- **Pillar 1: Data Accuracy** - Providing up-to-date information.
- **Pillar 2: E-E-A-T Signal Alignment** - Demonstrating firsthand experience.

## Conclusion
By implementing structured content optimized for both traditional SEO and Generative AI engines, you can secure top rankings for **{keyword}**.

---

# SECTION 4: AEO & GEO OPTIMIZED FAQ SECTION

### Frequently Asked Questions

**Q1: What is the primary benefit of {keyword}?**
*A1: It improves search visibility, drives target organic traffic, and ensures your content is cited by AI search engines.*

**Q2: How often should content for {keyword} be updated?**
*A2: We recommend reviewing competitor rankings monthly and updating stats and FAQs quarterly.*

```json
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "What is the primary benefit of {keyword}?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "It improves search visibility, drives target organic traffic, and ensures your content is cited by AI search engines."
      }}
    }},
    {{
      "@type": "Question",
      "name": "How often should content for {keyword} be updated?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "We recommend reviewing competitor rankings monthly and updating stats and FAQs quarterly."
      }}
    }}
  ]
}}
```

---

# SECTION 5: COMPREHENSIVE SEO ACTION STRATEGY

### 1. On-Page SEO Guidelines
- Keep keyword density around 1.5% - 2.0%.
- Image ALT Tags: `best-{keyword.lower().replace(' ', '-')}-diagram.png`
- Internal Links: Link to related product review pages and topic hubs.

### 2. Technical SEO Checklist
- Implement `FAQPage` and `Article` JSON-LD Schemas.
- Ensure Core Web Vitals LCP < 2.5s and CLS < 0.1.

### 3. Off-Page SEO & Backlink Strategy
- Create an infographic summarizing key data for outreach.
- Target niche industry blogs for guest contributions focusing on {keyword}.
"""
