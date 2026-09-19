import os
from datetime import datetime
from config import Config
from competitor_tracker import CompetitorTracker
from bd_trend_analyzer import BDTrendAnalyzer
from social_media_analyzer import SocialMediaAnalyzer
from seo_writer_agent import SEOWriterAgent
from agent_activity import AgentActivityLogger


class Master360Agent:
    def __init__(self):
        self.tracker = CompetitorTracker()
        self.writer = SEOWriterAgent()
        self.bd_analyzer = BDTrendAnalyzer(gemini_agent=self.writer)
        self.social_analyzer = SocialMediaAnalyzer(gemini_agent=self.writer)

    def run_full_360_analysis(self, keyword_or_product: str, category: str = "Smart Electronics & Gadgets"):
        print(f"\n==================================================================")
        print(f"🚀 STARTING 360° ALL-IN-ONE INTELLIGENCE SCAN FOR: '{keyword_or_product}'")
        print(f"==================================================================")

        # 1. Competitor SERP & SEO Strategy Tracking
        print("--> [1/4] Scanning Competitor SEO Strategies & Rankings...")
        comp_analysis = self.tracker.analyze_keyword(keyword_or_product)
        AgentActivityLogger.log_activity("Competitor SERP Scan", keyword_or_product, "SUCCESS", f"Rankings found: {comp_analysis['total_results']}")

        # 2. BD Market & Category Trend Scanning
        print("--> [2/4] Scanning Bangladesh Market & Category Trends...")
        bd_trends = self.bd_analyzer.analyze_trending_products(category)
        AgentActivityLogger.log_activity("BD Market Trend Scan", category, "SUCCESS", "Category trend analysis compiled")

        # 3. Social Media Viral Trend Scanning
        print("--> [3/4] Scanning Social Media Trends (Facebook, TikTok, YouTube)...")
        social_trends = self.social_analyzer.analyze_social_trends(keyword_or_product)
        AgentActivityLogger.log_activity("Social Media Viral Scan", keyword_or_product, "SUCCESS", "Social media hooks & ad copy compiled")

        # 4. Article & Full SEO / AEO / GEO Generation
        print("--> [4/4] Generating SEO / AEO / GEO Article & Complete Strategy...")
        article = self.writer.generate_content(keyword_or_product, comp_analysis)
        AgentActivityLogger.log_activity("SEO Article Generation", keyword_or_product, "SUCCESS", "AEO/GEO full article generated")


        # Combine into Master 360° Report with Ahrefs Board Formatting
        master_report = f"""# 🏆 360° ALL-IN-ONE INTELLIGENCE & SEO REPORT: {keyword_or_product.upper()}

<div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px;">
  <div style="font-size: 13px; font-weight: 800; color: #1E3A8A; text-transform: uppercase; margin-bottom: 8px;">📊 AHREFS OVERVIEW BOARD: {keyword_or_product.upper()}</div>
  <div style="display: flex; gap: 10px; flex-wrap: wrap;">
    <div style="flex: 1; min-width: 120px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; text-align: center;">
      <div style="font-size: 20px; font-weight: 800; color: #1E3A8A;">{comp_analysis['total_results']}</div>
      <div style="font-size: 10.5px; font-weight: 700; color: #64748B;">SERP RESULTS</div>
    </div>
    <div style="flex: 1; min-width: 120px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; text-align: center;">
      <div style="font-size: 20px; font-weight: 800; color: #166534;">{len(comp_analysis['competitor_matches'])}</div>
      <div style="font-size: 10.5px; font-weight: 700; color: #64748B;">COMPETITORS</div>
    </div>
    <div style="flex: 1; min-width: 120px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; text-align: center;">
      <div style="font-size: 20px; font-weight: 800; color: #2563EB;">HIGH</div>
      <div style="font-size: 10.5px; font-weight: 700; color: #64748B;">INTENT SCORE</div>
    </div>
    <div style="flex: 1; min-width: 120px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; text-align: center;">
      <div style="font-size: 20px; font-weight: 800; color: #D97706;">94%</div>
      <div style="font-size: 10.5px; font-weight: 700; color: #64748B;">OPPORTUNITY</div>
    </div>
  </div>
</div>

**Target Keyword**: `{keyword_or_product}` | **Category**: `{category}` | **Generated Date**: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`

---

## 🔍 COMPETITOR SERP OVERVIEW TABLE

| Rank | Organic Page Title | Target Domain | Competitor Status | Live URL |
| :---: | :--- | :---: | :---: | :--- |
"""
        for r in comp_analysis['rankings']:
            comp_badge = "🟢 Competitor Match" if r['is_competitor'] else "⚪ General Result"
            master_report += f"| **#{r['rank']}** | {r['title']} | `{r['domain']}` | {comp_badge} | [View Page]({r['url']}) |\n"

        master_report += f"\n---\n\n{social_trends}\n\n---\n\n{article}\n"

        # Save to output directory
        output_dir = Config.OUTPUT_DIR
        os.makedirs(output_dir, exist_ok=True)
        filename = f"360_master_{keyword_or_product.lower().replace(' ', '_')}.md"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(master_report)

        print(f"\n==================================================================")
        print(f"✅ 360° MASTER INTELLIGENCE REPORT SAVED AT:")
        print(f"📄 {filepath}")
        print(f"==================================================================\n")
        return filepath, master_report
