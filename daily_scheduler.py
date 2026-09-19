import time
import os
from datetime import datetime
try:
    import schedule
except ImportError:
    schedule = None

from config import Config
from competitor_tracker import CompetitorTracker
from seo_writer_agent import SEOWriterAgent

def run_daily_job():
    print(f"\n==================================================")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Daily SEO & Competitor Scan...")
    print(f"==================================================")

    output_dir = Config.OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    tracker = CompetitorTracker()
    writer = SEOWriterAgent()

    daily_report = f"# Daily Competitor & SEO Intelligence Report\n"
    daily_report += f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    for keyword in Config.TARGET_KEYWORDS:
        print(f"--> Scanning SERP for Keyword: '{keyword}'...")
        analysis = tracker.analyze_keyword(keyword)
        
        daily_report += f"## Topic / Keyword: `{keyword}`\n"
        daily_report += f"- Total SERP URLs Checked: {analysis['total_results']}\n"
        
        if analysis['competitor_matches']:
            daily_report += f"- ⚠️ **Competitor Matches Found ({len(analysis['competitor_matches'])}):**\n"
            for match in analysis['competitor_matches']:
                daily_report += f"  - Rank #{match['rank']}: [{match['title']}]({match['url']}) (Domain: `{match['domain']}`)\n"
        else:
            daily_report += f"- ✅ No target competitors detected in top SERP results for this keyword.\n"

        # Generate fresh SEO article report for the keyword
        print(f"--> Generating SEO/AEO/GEO Article for '{keyword}'...")
        content = writer.generate_content(keyword, analysis)
        
        # Save individual keyword article report
        filename = f"{datetime.now().strftime('%Y%m%d')}_{keyword.lower().replace(' ', '_')}.md"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        daily_report += f"- 📄 Generated Article Report: `{filepath}`\n\n"

    # Save master daily report
    summary_filename = f"daily_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    summary_filepath = os.path.join(output_dir, summary_filename)
    with open(summary_filepath, "w", encoding="utf-8") as f:
        f.write(daily_report)

    print(f"--> Daily Job Completed Successfully!")
    print(f"--> Master Summary saved at: {summary_filepath}\n")

def start_scheduler():
    print("SEO Competitor AI Agent Scheduler Started.")
    print("Running initial scan now...")
    run_daily_job()
    
    # Schedule to run every day at 08:00 AM
    schedule.every().day.at("08:00").do(run_daily_job)
    
    print("Scheduler running in loop. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    start_scheduler()
