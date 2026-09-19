class ShopifySEOPromptTemplate:
    @staticmethod
    def get_shopify_seo_prompt(product_or_keyword: str, competitor_insights: dict = None, notes: str = "") -> str:
        prompt = f"""
You are an Expert Shopify E-Commerce SEO Specialist & Conversion Rate Optimizer (CRO).

Generate a complete, high-ranking, publication-ready Shopify Product & Collection Page SEO Suite for:
"{product_or_keyword}"

CRITICAL DIRECTIVES:
1. **ENGLISH ONLY**: Generate all Shopify descriptions, metadata, FAQs, and schemas strictly in ENGLISH language.
2. **AHREFS BOARD UI**: Present key product features, competitor comparisons, and metadata in Ahrefs-style structured dashboard boards.

---

### REQUIRED SHOPIFY SEO OUTPUT:

# 🛍️ SHOPIFY E-COMMERCE SEO & CONVERSION SUITE

## SECTION 1: SHOPIFY METADATA (COPY-PASTE READY FOR SHOPIFY ADMIN)
- **Shopify Page Title**: (Under 60 chars, includes product keyword + value hook)
- **Shopify Meta Description**: (140-155 chars, includes keyword, BDT/USD price hook, and Cash on Delivery / Free Shipping CTA)
- **Shopify URL Handle / Slug**: (clean handle e.g. `products/wireless-gaming-mouse`)
- **Primary Target Keyword**: {product_or_keyword}
- **Secondary LSI Keywords**: (5 e-commerce intent keywords)

---

## SECTION 2: SHOPIFY PRODUCT DESCRIPTION (H1, H2, H3 RICH TEXT FORMAT)
- **H1 Product Title**: (Engaging main product title)
- **Product Hook & Summary**: High-converting introduction addressing customer pain points.
- **H2 Key Features & Specifications**: Highlight 4-5 major technical specs & benefits.
  - **H3 Highlights**: Bullet points with bold features.
- **H2 Why Buy From Us**: (Highlight warranty, fast delivery inside BD/Global, authentic guarantee).

---

## SECTION 3: AEO FAQ & SHOPIFY JSON-LD SCHEMA MARKUP
Provide 4 high-intent customer Q&As (Price, Warranty, Delivery time, Returns).
Provide ready-to-paste **JSON-LD Schema Markup** for Shopify `theme.liquid` / `product.liquid`:
```json
{{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "{product_or_keyword}",
  "description": "High quality {product_or_keyword} with fast delivery and official warranty.",
  "offers": {{
    "@type": "Offer",
    "priceCurrency": "BDT",
    "availability": "https://schema.org/InStock"
  }}
}}
```

---

## SECTION 4: SHOPIFY ON-PAGE & INTERNAL LINKING STRATEGY
1. **Shopify Collection Link Strategy**: Link to parent collection `/collections/all` with exact anchor text.
2. **Shopify Image Alt Text**: `best-{product_or_keyword.lower().replace(' ', '-')}-main-view.jpg`
3. **Shopify Speed & Core Web Vitals Tip**: Compress WebP images & defer non-essential Shopify Apps.
"""
        return prompt
