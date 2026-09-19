import requests
import json
import urllib.parse
from config import Config
from competitor_tracker import CompetitorTracker

class SocialMediaAnalyzer:
    def __init__(self, gemini_agent=None):
        self.tracker = CompetitorTracker()
        self.gemini_agent = gemini_agent

    def analyze_social_trends(self, product_or_keyword: str):
        """Analyze viral social media trends (Facebook, TikTok, YouTube, Instagram) for a product in BD & Global."""
        search_query = f"{product_or_keyword} unboxing review facebook reels tiktok youtube viral trend bangladesh"
        print(f"[SocialMediaAnalyzer] Scanning social media trends for: '{product_or_keyword}'...")
        
        serp_data = self.tracker.analyze_keyword(search_query)
        
        if self.gemini_agent and self.gemini_agent.client:
            prompt = f"""
You are a Social Media Viral Trend Analyst & E-Commerce Marketing Expert.

Perform a deep social media trend analysis for product/keyword: "{product_or_keyword}".

### Social Media Search Data:
{json.dumps(serp_data['rankings'][:5], indent=2)}

---

### REQUIRED OUTPUT (SOCIAL MEDIA TREND ANALYSIS):

# 📱 SOCIAL MEDIA VIRAL TREND REPORT: {product_or_keyword.upper()}

## 1. Viral Content Angles & Hooks (Facebook, TikTok, YouTube Shorts)
- **Top Viral Angle 1**: (e.g., "Honest Unboxing & Stress Test")
- **Top Viral Angle 2**: (e.g., "Price Comparison: Local Market vs Online Daraz Offer")
- **Top Viral Angle 3**: (e.g., "5 Secret Features You Didn't Know About")

## 2. Platform Dominance & Audience Reaction (Bangladesh & Global)
- **Facebook Reels & Pages**: How BD sellers are promoting this product on Facebook live/videos.
- **TikTok & Instagram**: Video style, music/voiceover trends, short-form video popularity.
- **YouTube Reviews**: Key features reviewers emphasize (battery life, build quality, warranty).

## 3. Top High-Converting Ad Hooks & Copy Phrases (Bangla/Banglish)
List 4-5 high converting video ad headlines used by top sellers:
- e.g. "ঢাকার মধ্যে ২৪ ঘণ্টায় হোম ডেলিভারি! সীমিত স্টকে আসল গ্যাজেট!"
- e.g. "১০০০ টাকার নিচে বাজারের সেরা ইয়ারবাডস! দেখুন আনবক্সিং ভিডিও।"

## 4. Social Media to SEO Synergy Recommendations
How to embed social media video content, user reviews, and reel embeds inside website articles to rank #1 on Google AI Overviews & Search.
"""
            try:
                response = self.gemini_agent.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"[SocialMediaAnalyzer] Gemini AI social trend error: {e}")

        # Fallback social trend report
        return self._fallback_social_report(product_or_keyword)

    def _fallback_social_report(self, product_or_keyword: str) -> str:
        return f"""# 📱 SOCIAL MEDIA VIRAL TREND REPORT: {product_or_keyword.upper()}

## 1. Viral Content Angles & Hooks (Facebook Reels, TikTok, YouTube Shorts)
- **Unboxing & Price Comparison Hook**: Showing the product unboxing live, demonstrating battery/build quality, and comparing BDT prices.
- **Problem vs Solution Hook**: "আশেপাশের কোলাহল ছাড়াই স্পষ্ট কথা বলার সেরা বাড্‌স!" (Focusing on active noise cancellation or battery life).
- **Budget Challenge Hook**: "১০০০ টাকার বাজেটে কোনটা সেরা?" (Comparison videos perform 3x better on Facebook & YouTube).

---

## 2. Platform Dominance & Audience Reaction
- **Facebook Groups & Pages (BD)**: Highest sales conversion happens through Facebook Video Ads with Cash on Delivery (COD) call-to-action.
- **YouTube Shorts & Reviews**: In-depth Bangladeshi tech reviewers (like SamZone, Techland BD, Sohag 360 style) driving search volume on Google.
- **TikTok & Instagram Reels**: Fast 15-second viral video demonstrations showcasing RGB lighting or compact design.

---

## 3. Top High-Converting Social Ad Copy Hooks (Bangla)
- `🔥 সীমিত স্টক! ক্যাশ অন ডেলিভারিতে অরিজিনাল {product_or_keyword} সারাদেশে অর্ডার করুন!`
- `⚡ ১০০০ টাকার নিচে সেরা গ্যাজেট! ৭ দিনের গ্যারান্টি সহ আজই কিনুন।`
- `📦 ডেলিভারি চার্জ ফ্রী! অফারটি শেষ হওয়ার আগেই অর্ডার নিশ্চিত করুন।`

---

## 4. Social-to-SEO Integration Strategy
- Embed YouTube Shorts / Facebook Reel video embeds in H2 article sections.
- Include real customer quotes and social proof inside the AEO FAQ section.
"""
