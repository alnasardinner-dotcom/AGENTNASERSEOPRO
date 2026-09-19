import json
import os
from datetime import datetime
from config import Config
from competitor_tracker import CompetitorTracker

POSITION_LOG_FILE = os.path.join(Config.OUTPUT_DIR, "keyword_positions.json")

class KeywordRankTracker:
    def __init__(self):
        self.tracker = CompetitorTracker()

    def track_keyword_positions(self, domain: str, keywords: list):
        """Track exact Google rank positions for a list of keywords for a target domain."""
        domain_clean = domain.strip().replace("http://", "").replace("https://", "").strip("/")
        print(f"[KeywordRankTracker] Tracking keyword positions for domain: '{domain_clean}'...")

        tracked_results = []
        top_3_count = 0
        page_1_count = 0
        page_2_3_count = 0
        unranked_count = 0

        for kw in keywords:
            kw_clean = kw.strip()
            if not kw_clean:
                continue

            print(f"--> Checking Google rank position for keyword: '{kw_clean}'...")
            serp_data = self.tracker.analyze_keyword(kw_clean, competitors=[domain_clean])
            
            rank_found = -1
            found_url = ""
            found_title = ""

            base_target = domain_clean.lower().replace("www.", "").replace("https://", "").replace("http://", "").split(".com")[0].split(".bd")[0].strip()

            for item in serp_data['rankings']:
                item_domain = item.get("domain", "").lower().replace("www.", "")
                item_url = item.get("url", "").lower()
                if (base_target and base_target in item_domain) or (base_target and base_target in item_url) or domain_clean.lower() in item_domain or domain_clean.lower() in item_url:
                    rank_found = item['rank']
                    found_url = item['url']
                    found_title = item['title']
                    break

            if rank_found == -1:
                status = "🔴 Unranked (Outside Top 10)"
                unranked_count += 1
            elif rank_found <= 3:
                status = f"🏆 Top 3 (Rank #{rank_found})"
                top_3_count += 1
                page_1_count += 1
            elif rank_found <= 10:
                status = f"🟢 Page 1 (Rank #{rank_found})"
                page_1_count += 1
            else:
                status = f"🟡 Page 2+ (Rank #{rank_found})"
                page_2_3_count += 1

            tracked_item = {
                "keyword": kw_clean,
                "rank": rank_found if rank_found != -1 else "30+",
                "status": status,
                "title": found_title if found_title else "N/A",
                "url": found_url if found_url else "N/A"
            }
            tracked_results.append(tracked_item)

        # Log history with timestamp
        self._save_position_history(domain_clean, tracked_results)

        return self._build_position_report(domain_clean, tracked_results, top_3_count, page_1_count, unranked_count)

    def _save_position_history(self, domain: str, results: list):
        history = []
        if os.path.exists(POSITION_LOG_FILE):
            try:
                with open(POSITION_LOG_FILE, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception as e:
                print(f"[KeywordRankTracker] History read error: {e}")

        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "domain": domain,
            "results": results
        }
        history.insert(0, record)
        history = history[:50]  # Keep last 50 audit logs

        try:
            output_dir = Config.OUTPUT_DIR
            os.makedirs(output_dir, exist_ok=True)
            with open(POSITION_LOG_FILE, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[KeywordRankTracker] History save error: {e}")

    def _build_position_report(self, domain: str, results: list, top3: int, page1: int, unranked: int) -> str:
        total = len(results)
        visibility_pct = (page1 / total * 100) if total > 0 else 0

        report = f"""# 🎯 KEYWORD RANK POSITION REPORT: {domain.upper()}

<div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px;">
  <div style="font-size: 13px; font-weight: 800; color: #1E3A8A; text-transform: uppercase; margin-bottom: 8px;">📊 AHREFS RANK POSITION BOARD: {domain.upper()}</div>
  <div style="display: flex; gap: 10px; flex-wrap: wrap;">
    <div style="flex: 1; min-width: 110px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; text-align: center;">
      <div style="font-size: 20px; font-weight: 800; color: #1E3A8A;">{total}</div>
      <div style="font-size: 10.5px; font-weight: 700; color: #64748B;">KEYWORDS</div>
    </div>
    <div style="flex: 1; min-width: 110px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; text-align: center;">
      <div style="font-size: 20px; font-weight: 800; color: #166534;">{top3}</div>
      <div style="font-size: 10.5px; font-weight: 700; color: #64748B;">TOP 3 RANKS</div>
    </div>
    <div style="flex: 1; min-width: 110px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; text-align: center;">
      <div style="font-size: 20px; font-weight: 800; color: #2563EB;">{page1}</div>
      <div style="font-size: 10.5px; font-weight: 700; color: #64748B;">PAGE 1 RANKS</div>
    </div>
    <div style="flex: 1; min-width: 110px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; text-align: center;">
      <div style="font-size: 20px; font-weight: 800; color: #DC2626;">{unranked}</div>
      <div style="font-size: 10.5px; font-weight: 700; color: #64748B;">UNRANKED</div>
    </div>
    <div style="flex: 1; min-width: 110px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; text-align: center;">
      <div style="font-size: 20px; font-weight: 800; color: #1E3A8A;">{visibility_pct:.1f}%</div>
      <div style="font-size: 10.5px; font-weight: 700; color: #64748B;">VISIBILITY</div>
    </div>
  </div>
</div>

**Target Domain**: `{domain}` | **Date**: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`

---

## 📊 LIVE KEYWORD POSITION TABLE

| Target Keyword | Exact Rank Position | Status | Live Ranking URL |
| :--- | :---: | :---: | :--- |
"""
        for r in results:
            url_display = f"[{r['url'][:40]}...]({r['url']})" if r['url'] != "N/A" else "N/A"
            report += f"| `{r['keyword']}` | **#{r['rank']}** | {r['status']} | {url_display} |\n"

        report += f"""\n---

#### 🛠️ Rank Boost Action Plan (How to Increase Positions)

1. **Keywords in Rank #4 to #10 (Quick Win Opportunity)**:
   - Update internal links from homepage pointing to these pages with exact keyword anchor text to push them into Top 3!
2. **Unranked Keywords**:
   - Check if page has thin content. Add 400+ words of structured text with AEO/GEO FAQ sections.
3. **Core Web Vitals & CTR Optimization**:
   - Add numbers (e.g. `2026`, `BDT ৳`) and brackets to Meta Titles to increase CTR from SERP.
"""
        return report
