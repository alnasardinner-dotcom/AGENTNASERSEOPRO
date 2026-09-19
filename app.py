import sys
import os
from config import Config
from competitor_tracker import CompetitorTracker
from seo_writer_agent import SEOWriterAgent
from bd_trend_analyzer import BDTrendAnalyzer
from social_media_analyzer import SocialMediaAnalyzer
from indexing_checker import IndexingChecker
from master_agent import Master360Agent
from daily_scheduler import run_daily_job

def print_banner():
    print("=" * 76)
    print("                      AGENT NASER SEO PRO SYSTEM                        ")
    print(" [ Keywords | Competitors | Social Media | BD Trends | Indexing Audit ]")
    print("=" * 76)

def menu():
    print("\nPlease select an option:")
    print("1. 🚀 ALL-IN-ONE 360° REPORT (Keyword/URL + Competitor + Social + Article)")
    print("2. 🔴🟢 AUDIT COMPANY PRODUCT INDEXING STATUS (Check Indexed vs Non-Indexed)")
    print("3. 🔍 Track Competitor SEO & Rankings for a Keyword or URL")
    print("4. 📱 Analyze Social Media Viral Trends (Facebook, TikTok, YouTube BD)")
    print("5. 🇧🇩 Analyze Trending Products in Bangladesh Market")
    print("6. 📝 Generate AEO / GEO / SEO Article Only")
    print("7. ⏰ Run Daily Automated Scan")
    print("8. Exit")

def main():
    print_banner()
    tracker = CompetitorTracker()
    writer = SEOWriterAgent()
    bd_analyzer = BDTrendAnalyzer(gemini_agent=writer)
    social_analyzer = SocialMediaAnalyzer(gemini_agent=writer)
    indexing_checker = IndexingChecker()
    master_agent = Master360Agent()

    # CLI Direct argument mode
    if len(sys.argv) > 1:
        raw_input = " ".join(sys.argv[1:])
        filepath, report = master_agent.run_full_360_analysis(raw_input)
        print(f"\n==================================================================")
        print(report[:1200])
        print(f"\n[... Full Report Saved at: {filepath} ...]")
        return

    # Interactive Loop
    while True:
        menu()
        choice = input("\nEnter choice (1-8): ").strip()
        
        if choice == "1":
            inp = input("\nEnter Target Product Name or Page URL: ").strip()
            if not inp:
                print("Input cannot be empty.")
                continue
            cat = input("Enter Category (press Enter for Smart Electronics & Gadgets): ").strip()
            if not cat:
                cat = "Smart Electronics & Gadgets"
            
            filepath, report = master_agent.run_full_360_analysis(inp, cat)
            print(f"\n==================================================================")
            print(f"🎉 360° MASTER REPORT GENERATION COMPLETE (AGENT NASER SEO PRO)")
            print(f"==================================================================")
            print(report[:1500])
            print(f"\n📄 Full Report Saved to: {filepath}\n")

        elif choice == "2":
            domain = input("\nEnter your Company Domain: ").strip()
            if not domain:
                print("Domain cannot be empty.")
                continue
            print("Enter Product Names or Page URLs to audit (comma separated):")
            products_str = input("Products/URLs: ").strip()
            if not products_str:
                print("Product list cannot be empty.")
                continue
            
            product_list = [p.strip() for p in products_str.split(",") if p.strip()]
            report = indexing_checker.check_product_indexing(domain, product_list)
            
            output_dir = Config.OUTPUT_DIR
            os.makedirs(output_dir, exist_ok=True)
            domain_clean = domain.replace("http://", "").replace("https://", "").replace("/", "").replace(".", "_")
            filepath = os.path.join(output_dir, f"indexing_audit_{domain_clean}.md")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(report)
            
            print(f"\n==================================================================")
            print(f"✅ COMPANY PRODUCT INDEXING AUDIT REPORT")
            print(f"==================================================================")
            print(report)
            print(f"\n📄 Saved to: {filepath}\n")

        elif choice == "3":
            inp = input("\nEnter Keyword or Product URL to analyze: ").strip()
            if not inp:
                print("Input cannot be empty.")
                continue
            print(f"\nScanning SERP for '{inp}'...")
            res = tracker.analyze_keyword(inp)
            
            print(f"\n==================================================================")
            print(f"🔍 SERP RANKING & COMPETITOR AUDIT FOR: '{res['keyword']}'")
            print(f"==================================================================")
            print(f"Total Search Results Found: {res['total_results']}")
            print(f"Competitor Matches Found: {len(res['competitor_matches'])}\n")
            for r in res['rankings']:
                comp_tag = " ⚠️ [COMPETITOR MATCH]" if r['is_competitor'] else ""
                print(f"Rank #{r['rank']}: {r['title']}{comp_tag}")
                print(f"  URL: {r['url']}")
                print(f"  Domain: {r['domain']}")
                print(f"  Snippet: {r['snippet']}\n")

        elif choice == "4":
            inp = input("\nEnter Product or Keyword for Social Media Trend Analysis: ").strip()
            if not inp:
                print("Input cannot be empty.")
                continue
            report = social_analyzer.analyze_social_trends(inp)
            output_dir = Config.OUTPUT_DIR
            os.makedirs(output_dir, exist_ok=True)
            filepath = os.path.join(output_dir, f"social_trend_{inp.lower().replace(' ', '_').replace('/', '_')}.md")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(report)
            
            print(f"\n==================================================================")
            print(f"📱 SOCIAL MEDIA VIRAL TREND REPORT")
            print(f"==================================================================")
            print(report)
            print(f"\n📄 Saved to: {filepath}\n")

        elif choice == "5":
            print("\nSelect Category for Bangladesh Market Trend Analysis:")
            for idx, c in enumerate(Config.BD_TRENDING_CATEGORIES, 1):
                print(f"{idx}. {c}")
            cat_choice = input("Select category (1-5, or press Enter for Smart Electronics): ").strip()
            selected_cat = Config.BD_TRENDING_CATEGORIES[0]
            if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(Config.BD_TRENDING_CATEGORIES):
                selected_cat = Config.BD_TRENDING_CATEGORIES[int(cat_choice) - 1]
            
            report = bd_analyzer.analyze_trending_products(selected_cat)
            output_dir = Config.OUTPUT_DIR
            os.makedirs(output_dir, exist_ok=True)
            filepath = os.path.join(output_dir, f"bd_trend_{selected_cat.lower().replace(' ', '_')}.md")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(report)
            
            print(f"\n==================================================================")
            print(f"🇧🇩 BANGLADESH MARKET TREND REPORT")
            print(f"==================================================================")
            print(report)
            print(f"\n📄 Saved to: {filepath}\n")

        elif choice == "6":
            inp = input("\nEnter Keyword or Product Name to write article for: ").strip()
            if not inp:
                print("Input cannot be empty.")
                continue
            analysis = tracker.analyze_keyword(inp)
            content = writer.generate_content(inp, analysis)
            output_dir = Config.OUTPUT_DIR
            os.makedirs(output_dir, exist_ok=True)
            filepath = os.path.join(output_dir, f"article_{inp.lower().replace(' ', '_').replace('/', '_')}.md")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"\n==================================================================")
            print(f"📝 SEO / AEO / GEO ARTICLE GENERATED")
            print(f"==================================================================")
            print(content[:1200])
            print(f"\n📄 Full Article Saved to: {filepath}\n")

        elif choice == "7":
            run_daily_job()

        elif choice == "8":
            print("Exiting AGENT NASER SEO PRO. Goodbye!")
            break
        else:
            print("Invalid selection. Please enter 1-8.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ An error occurred while running AGENT NASER SEO PRO: {e}")
        input("\nPress Enter to exit...")
