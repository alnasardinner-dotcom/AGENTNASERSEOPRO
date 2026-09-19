class LocalGMBSEOPromptTemplate:
    @staticmethod
    def get_local_gmb_seo_prompt(business_name_or_keyword: str, location: str = "Dhaka, Bangladesh", notes: str = "") -> str:
        prompt = f"""
You are an Elite Local SEO & Google Business Profile (GMB / Google My Business) Optimization Specialist.

Generate a complete, high-ranking Local SEO & Google Business Profile (GMB) Setup Suite for:
Business Name / Service: "{business_name_or_keyword}"
Target Location / City: "{location}"

CRITICAL DIRECTIVES:
1. **ENGLISH ONLY**: Generate all GMB profiles, descriptions, citation plans, and schemas strictly in ENGLISH language.
2. **AHREFS BOARD UI**: Format all local SEO metrics, GMB categories, and keyword strategies in clean Ahrefs-style dashboard boards.

---

### REQUIRED LOCAL SEO & GMB SUITE OUTPUT:

# 📍 GOOGLE MY BUSINESS (GMB) & LOCAL SEO SUITE

## SECTION 1: GOOGLE BUSINESS PROFILE (GMB) OPTIMIZER
- **Optimized GMB Business Name**: (Includes primary category + location hook)
- **Primary GMB Category**: (Most accurate Google Business category)
- **Secondary Categories**: (3 supporting sub-categories)
- **GMB Business Description (750 Chars Max)**: (High converting description with NAP consistency, local keywords, and CTA to call/visit)
- **GMB Services / Products Listing**: List 5 core services with BDT/USD price tags & descriptions.

---

## SECTION 2: GOOGLE MAPS 3-PACK RANKING STRATEGY
1. **Geo-Targeted Keywords**: (5 local search terms e.g. "{business_name_or_keyword} in {location}", "best {business_name_or_keyword} near me")
2. **Geo-Tagged Image Strategy**: Recommended ALT tags and geo-location EXIF metadata tags for photos.
3. **Review Request Strategy & Response Prompts**: High-converting template to ask customers for 5-star Google Reviews.

---

## SECTION 3: LOCAL CITATIONS & DIRECTORY LISTING PLAN
List 5 top local directories and citation sources for {location} (e.g. Google Maps, Facebook Local Page, BD Trade Index, Local Yellow Pages).

---

## SECTION 4: LOCALBUSINESS JSON-LD SCHEMA MARKUP
```json
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "{business_name_or_keyword}",
  "image": "https://example.com/logo.jpg",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "Main Street",
    "addressLocality": "{location.split(',')[0] if ',' in location else location}",
    "addressCountry": "BD"
  }},
  "geo": {{
    "@type": "GeoCoordinates",
    "latitude": "23.8103",
    "longitude": "90.4125"
  }},
  "url": "https://example.com",
  "telephone": "+8801700000000",
  "openingHoursSpecification": [
    {{
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
      "opens": "09:00",
      "closes": "20:00"
    }}
  ]
}}
```
"""
        return prompt
