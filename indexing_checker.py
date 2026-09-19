import requests
import urllib.parse
import re
from datetime import datetime
from bs4 import BeautifulSoup
from config import Config
from competitor_tracker import CompetitorTracker

class IndexingChecker:
    def __init__(self, company_domain: str = ""):
        self.company_domain = company_domain.strip().replace("http://", "").replace("https://", "").strip("/")
        self.tracker = CompetitorTracker()

    def fetch_site_sitemap_urls(self, company_domain: str) -> dict:
        """Crawl website sitemaps or homepage links to automatically discover product, category & page URLs."""
        domain_clean = company_domain.strip().replace("http://", "").replace("https://", "").replace("www.", "").strip("/")
        base_url = f"https://{domain_clean}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        sitemap_candidates = [
            f"{base_url}/sitemap.xml",
            f"{base_url}/sitemap_index.xml",
            f"{base_url}/product-sitemap.xml",
            f"{base_url}/category-sitemap.xml",
            f"{base_url}/page-sitemap.xml"
        ]

        found_urls = set()

        for sitemap_url in sitemap_candidates:
            try:
                res = requests.get(sitemap_url, headers=headers, timeout=6)
                if res.status_code == 200 and ("xml" in res.headers.get("content-type", "") or "<loc>" in res.text):
                    soup = BeautifulSoup(res.text, "xml")
                    locs = soup.find_all("loc")
                    for loc in locs:
                        url_str = loc.text.strip()
                        if domain_clean in url_str:
                            found_urls.add(url_str)
                    if len(found_urls) > 10:
                        break
            except Exception as e:
                print(f"[IndexingChecker] Sitemap fetch notice for {sitemap_url}: {e}")

        # Fallback: Scrape homepage navigation & internal links if sitemap returned few links
        if len(found_urls) < 3:
            try:
                res = requests.get(base_url, headers=headers, timeout=8)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, "html.parser")
                    for a_tag in soup.find_all("a", href=True):
                        href = a_tag["href"].strip()
                        full_url = urllib.parse.urljoin(base_url, href)
                        parsed = urllib.parse.urlparse(full_url)
                        if domain_clean in parsed.netloc and not full_url.endswith(("#", ".png", ".jpg", ".css", ".js", ".pdf")):
                            found_urls.add(full_url)
            except Exception as e:
                print(f"[IndexingChecker] Homepage crawler notice: {e}")

        # Categorize discovered URLs
        products = []
        categories = []
        pages = []

        for url in sorted(found_urls):
            url_lower = url.lower()
            if any(k in url_lower for k in ["/product/", "/p/", "/item/", "/pd/", "/product-page/", "/buy/"]):
                products.append(url)
            elif any(k in url_lower for k in ["/category/", "/c/", "/collection/", "/collections/", "/cat/"]):
                categories.append(url)
            else:
                pages.append(url)

        return {
            "all_urls": list(found_urls),
            "products": products,
            "categories": categories,
            "pages": pages
        }

    def check_product_indexing(self, company_domain: str, product_urls_or_names: list, non_indexed_only: bool = False):
        """Check which products/URLs of the user's company domain are indexed on Google. Option to report ONLY non-indexed items."""
        domain_raw = company_domain or self.company_domain
        domain_clean = domain_raw.strip().replace("http://", "").replace("https://", "").replace("www.", "").strip("/")

        print(f"\n[IndexingChecker] Auditing Google Index Status for Domain: '{domain_clean}'...")

        indexed_products = []
        non_indexed_products = []

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        for item in product_urls_or_names:
            item_clean = item.strip()
            if not item_clean:
                continue

            is_url = item_clean.startswith("http://") or item_clean.startswith("https://") or ("." in item_clean and "/" in item_clean)
            http_status = None
            has_noindex_tag = False
            page_title = ""

            # 1. Direct Page HTTP & Meta Tag Audit if item is a URL
            if is_url:
                target_url = item_clean if item_clean.startswith("http") else f"https://{item_clean}"
                try:
                    res = requests.get(target_url, headers=headers, timeout=6, allow_redirects=True)
                    http_status = res.status_code
                    if res.status_code == 200:
                        soup = BeautifulSoup(res.text, "html.parser")
                        meta_robots = soup.find("meta", attrs={"name": re.compile(r"robots", re.I)})
                        if meta_robots and meta_robots.get("content"):
                            content_val = meta_robots.get("content", "").lower()
                            if "noindex" in content_val or "none" in content_val:
                                has_noindex_tag = True
                        title_tag = soup.find("title")
                        if title_tag:
                            page_title = title_tag.text.strip()
                except Exception as e:
                    print(f"[IndexingChecker] HTTP check notice for {target_url}: {e}")

            # 2. Search Engine Index Status Check
            if is_url:
                query = f"site:{item_clean}"
            else:
                query = f"site:{domain_clean} \"{item_clean}\""

            print(f"--> Auditing index status for: '{item_clean}'...")
            
            # Use Tavily API first if available, else HTML scraper with NO fake fallback data
            serp_results = self.tracker.search_keyword_tavily(query)
            if not serp_results:
                serp_results = self.tracker.search_keyword_html(query, allow_fallback=False)

            is_indexed = False
            matched_url = ""
            matched_title = ""

            if serp_results:
                for r in serp_results:
                    raw_res_url = r.get("url", "")
                    parsed_res = urllib.parse.urlparse(raw_res_url)
                    res_netloc = parsed_res.netloc.lower().replace("www.", "")

                    # Strict domain match on host name only
                    if domain_clean.lower() in res_netloc or res_netloc in domain_clean.lower():
                        is_indexed = True
                        matched_url = raw_res_url
                        matched_title = r.get("title", "")
                        break

            # 3. Categorize status based on empirical audit
            if is_indexed and not has_noindex_tag:
                indexed_products.append({
                    "product": item_clean,
                    "status": "Indexed",
                    "indexed_url": matched_url,
                    "title": matched_title or page_title or "Indexed Page"
                })
            else:
                reason = "Not Found in Google Index"
                if http_status and http_status >= 400:
                    reason = f"HTTP Error {http_status} (Page Not Found / Dead Link)"
                elif has_noindex_tag:
                    reason = "Blocked by HTML <meta name='robots' content='noindex'>"

                non_indexed_products.append({
                    "product": item_clean,
                    "status": "Not Indexed",
                    "reason": reason,
                    "query_used": query
                })

        return self._build_indexing_report(domain_clean, indexed_products, non_indexed_products, non_indexed_only=non_indexed_only)

    def audit_full_site_non_indexed_only(self, company_domain: str):
        """Auto-crawl website sitemap/links and produce a report showing ONLY non-indexed pages & products."""
        discovered = self.fetch_site_sitemap_urls(company_domain)
        all_urls = discovered["all_urls"]

        if not all_urls:
            # Fallback if domain had no crawlable URLs
            all_urls = [f"https://{company_domain}", f"https://{company_domain}/products", f"https://{company_domain}/categories"]

        return self.check_product_indexing(company_domain, all_urls[:30], non_indexed_only=True)

    def _build_indexing_report(self, domain: str, indexed: list, non_indexed: list, non_indexed_only: bool = False) -> str:
        total = len(indexed) + len(non_indexed)
        indexed_count = len(indexed)
        non_indexed_count = len(non_indexed)
        ratio = (indexed_count / total * 100) if total > 0 else 0

        report = f"""# 🚨 GOOGLE INDEX AUDIT REPORT: {domain.upper()}

<div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px;">
  <div style="font-size: 13px; font-weight: 800; color: #1E3A8A; text-transform: uppercase; margin-bottom: 8px;">📊 AHREFS INDEX AUDIT BOARD: {domain.upper()}</div>
  <div style="display: flex; gap: 10px; flex-wrap: wrap;">
    <div style="flex: 1; min-width: 110px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; text-align: center;">
      <div style="font-size: 20px; font-weight: 800; color: #1E3A8A;">{total}</div>
      <div style="font-size: 10.5px; font-weight: 700; color: #64748B;">AUDITED URLS</div>
    </div>
    <div style="flex: 1; min-width: 110px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; text-align: center;">
      <div style="font-size: 20px; font-weight: 800; color: #166534;">{indexed_count}</div>
      <div style="font-size: 10.5px; font-weight: 700; color: #64748B;">INDEXED</div>
    </div>
    <div style="flex: 1; min-width: 110px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; text-align: center;">
      <div style="font-size: 20px; font-weight: 800; color: #DC2626;">{non_indexed_count}</div>
      <div style="font-size: 10.5px; font-weight: 700; color: #64748B;">NON-INDEXED</div>
    </div>
    <div style="flex: 1; min-width: 110px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; text-align: center;">
      <div style="font-size: 20px; font-weight: 800; color: #2563EB;">{ratio:.1f}%</div>
      <div style="font-size: 10.5px; font-weight: 700; color: #64748B;">INDEX RATIO</div>
    </div>
  </div>
</div>

**Audited Domain**: `{domain}` | **Date**: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`

---

"""
        if non_indexed_only or non_indexed:
            report += "## ❌ 1. NON-INDEXED PAGES & PRODUCTS LIST\n\n"
            if non_indexed:
                report += "| # | Page / Product URL | Diagnostic Reason | Action Required |\n"
                report += "| :---: | :--- | :--- | :--- |\n"
                for idx, item in enumerate(non_indexed, 1):
                    report += f"| **#{idx}** | `{item['product']}` | `{item['reason']}` | Request GSC Indexing |\n"
                report += "\n"
            else:
                report += "🎉 **All checked site URLs are currently 100% indexed on Google!** No non-indexed pages detected.\n\n"

        if not non_indexed_only:
            report += f"""---

## 🟢 2. INDEXED PAGES SUMMARY
"""
            if indexed:
                report += "| Page / Product URL | Page Title | Status |\n"
                report += "| :--- | :--- | :---: |\n"
                for item in indexed:
                    report += f"| `{item['product']}` | {item['title']} | 🟢 Indexed |\n"
                report += "\n"
            else:
                report += "- *No indexed pages detected in this audit batch.*\n"

        report += f"""---

## 🛠️ 3. ACTION PLAN TO FIX NON-INDEXED PAGES ON GOOGLE

Follow this 5-step checklist to get all your non-indexed URLs indexed immediately:

1. **Google Search Console (GSC) Inspection**:
   - Open [Google Search Console](https://search.google.com/search-console) -> Paste the non-indexed URL -> Click **Request Indexing**.
2. **XML Sitemap Verification**:
   - Ensure all non-indexed product and category URLs are present in `https://{domain}/sitemap.xml`.
3. **Internal Link Boosting**:
   - Add internal links to non-indexed pages from high-traffic indexed pages (e.g., Homepage, Main Category pages).
4. **Fix Technical Blockers**:
   - Verify `robots.txt` does not have `Disallow:` rules for product/category paths.
   - Ensure the HTML `<head>` tag does not contain `<meta name="robots" content="noindex">`.
5. **Content Quality & Canonical Tags**:
   - Ensure product description text is unique (>300 words) and `rel="canonical"` tag points to itself.
"""
        return report
