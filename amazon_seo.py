class AmazonSEOPromptTemplate:
    @staticmethod
    def get_amazon_seo_prompt(product_or_keyword: str, competitor_insights: dict = None, notes: str = "") -> str:
        prompt = f"""
You are an Elite Amazon FBA & Affiliate SEO Copywriter & Listing Specialist.

Generate a complete, high-converting Amazon FBA & Affiliate SEO Suite for:
"{product_or_keyword}"

CRITICAL DIRECTIVES:
1. **ENGLISH ONLY**: Generate all titles, bullet points, reviews, tables, and schemas strictly in ENGLISH language.
2. **AHREFS BOARD UI**: Present key metrics, pros/cons, and comparison tables in Ahrefs-style structured dashboard boards.

---

### REQUIRED AMAZON SEO & AFFILIATE OUTPUT:

# 📦 AMAZON FBA & AFFILIATE SEO SUITE

## SECTION 1: AMAZON LISTING OPTIMIZER (FOR AMAZON FBA SELLERS)
- **Amazon Product Title**: (200 chars max, includes brand placeholder, primary keywords, size/color/specs, high search volume terms)
- **5 High-Converting Bullet Points**: (Capitalized benefit hooks e.g. **ULTIMATE ERGONOMIC DESIGN**, **24-HOUR BATTERY LIFE**)
- **Backend Search Terms**: (249 bytes max, space-separated high intent keywords, no duplicates)

---

## SECTION 2: AMAZON AFFILIATE REVIEW BLOG (FOR AFFILIATE MARKETERS)
- **Affiliate Article Title**: (e.g. "Honest Review: Is {product_or_keyword.title()} Worth Buying in 2026?")
- **Product Overview & Pros & Cons Table**: Factual comparison breakdown.
- **Why It Ranks**: Addressing key buying intent and target audience questions.

---

## SECTION 3: AMAZON PRODUCT & REVIEW JSON-LD SCHEMA
```json
{{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "{product_or_keyword}",
  "review": {{
    "@type": "Review",
    "reviewRating": {{
      "@type": "Rating",
      "ratingValue": "4.8",
      "bestRating": "5"
    }},
    "author": {{
      "@type": "Person",
      "name": "Expert Product Reviewer"
    }}
  }}
}}
```
"""
        return prompt
