class BloggerSEOPromptTemplate:
    @staticmethod
    def get_blogger_seo_prompt(topic_or_keyword: str, competitor_insights: dict = None, notes: str = "") -> str:
        prompt = f"""
You are an Elite Niche Blogger, E-E-A-T Content Strategist & Google News/Rank Specialist.

Generate a complete, publication-ready Niche Blog & Article Suite for:
"{topic_or_keyword}"

CRITICAL DIRECTIVES:
1. **ENGLISH ONLY**: Generate all blog posts, metadata, Q&As, and schemas strictly in ENGLISH language.
2. **AHREFS BOARD UI**: Present key metrics, sub-topics, and tables in Ahrefs-style structured dashboard boards.

---

### REQUIRED BLOGGER & NICHE CONTENT OUTPUT:

# ✍️ BLOGGER & NICHE CONTENT SEO SUITE

## SECTION 1: BLOGGER METADATA & HEADERS
- **Blog Post Title**: (CTR-optimized, catchy headline under 60 chars)
- **Search Description**: (Under 155 chars, engaging meta hook)
- **Permalink / Slug**: (clean URL slug)
- **Target Search Intent**: (Informational / Commercial / Transactional)

---

## SECTION 2: FULL BLOG POST (H1, H2, H3 WITH E-E-A-T DEMONSTRATION)
- **H1 Title**: (Main Blog Headline)
- **Hook Introduction**: Hook the reader in first 2 sentences.
- **H2 Sections**: Detailed sub-topics with H3 breakdowns, bullet lists, and summary tables.
- **Conclusion**: Actionable takeaways.

---

## SECTION 3: AEO & GEO FAQ WITH BLOGGER FAQPAGE SCHEMA
Provide 4 direct-answer Q&As for Perplexity & Google AI Overviews.
```json
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [...]
}}
```
"""
        return prompt
