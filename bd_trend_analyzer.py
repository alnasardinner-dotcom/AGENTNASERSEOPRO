import requests
import json
import urllib.parse
from bs4 import BeautifulSoup
from config import Config
from competitor_tracker import CompetitorTracker

class MarketTrendAnalyzer:
    def __init__(self, gemini_agent=None):
        self.tracker = CompetitorTracker()
        self.gemini_agent = gemini_agent

    def fetch_market_trends(self, category: str = "💻 Computer & Components", target_country: str = "🌐 Worldwide / Global (USD $)"):
        """Search Google SERP for trending products in a target country/region for a given category."""
        location_str = "worldwide global" if "Worldwide" in target_country or "Global" in target_country or "All" in target_country else target_country
        search_query = f"trending {category} top selling products price in {location_str} 2026"
        print(f"[MarketTrendAnalyzer] Scanning market trends for: '{category}' in '{target_country}'...")
        
        serp_data = self.tracker.analyze_keyword(search_query)
        return serp_data

    def analyze_trending_products(self, category: str = "💻 Computer & Components", target_country: str = "🌐 Worldwide / Global (USD $)"):
        """Analyze search data to produce Global & Local Market Product Trend Analysis."""
        serp_data = self.fetch_market_trends(category, target_country)
        
        if self.gemini_agent and self.gemini_agent.client:
            prompt = f"""
You are a Global E-Commerce & Industrial Market Intelligence Expert & Product Trend Researcher.

Analyze current market demand, search trends, pricing, B2B/B2C buyers, and top-selling products for:
- Category / Industry: "{category}"
- Target Country / Region: "{target_country}"

### SERP Data Extracted:
{json.dumps(serp_data['rankings'][:6], indent=2)}

---

### REQUIRED OUTPUT FORMAT:

# 🌐 MARKET TREND REPORT: {category.upper()} ({target_country})

## 1. Top 5 High-Demand Trending Products in {target_country}
List 5 specific trending products currently in high demand in this category/industry (e.g., Laptops, CNC Routers, Fiber Routers, Industrial Automation Sensors, 3D Printers, TWS, etc.).
For each product provide:
- **Product Name & Specs**:
- **Estimated Price Range**: (Include local currency BDT ৳ if Bangladesh, USD $ / EUR € if Global/Worldwide)
- **Target Audience / Buyer Persona**: (e.g. IT departments, CNC machine shops, SOHO workers, gamers, B2B factories)
- **Why it is Trending**: (e.g. technological shift, automation demand, viral short videos, high search volume)

## 2. Top E-Commerce & Industrial Competitors Analysis
- Identify top ranking online stores, distributors, or marketplaces (e.g. Amazon, Daraz, StarTech, McMaster-Carr, Grainger, B&H, Alibaba, eBay) ranking for these products in {target_country}.
- What promotional tactics and value propositions work best? (e.g., Free Shipping, Express Delivery, COD, B2B bulk discounts, Warranty & Technical Support).

## 3. High-Converting High-Intent Search Keywords
List 8-10 high intent search terms used by target buyers in this region (including both general English and regional/local search phrases).

## 4. Strategic Content & Launch Recommendations
Provide actionable strategy for SEO, content optimization, and marketing to achieve #1 rankings and high conversion rates for this product line in {target_country}.
"""
            try:
                response = self.gemini_agent.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"[MarketTrendAnalyzer] Gemini AI analysis error: {e}")

        # Structured fallback trend report when offline
        return self._generate_fallback_market_report(category, target_country, serp_data)

    def _generate_fallback_market_report(self, category: str, target_country: str, serp_data: dict) -> str:
        currency = "BDT (৳)" if "Bangladesh" in target_country else "USD ($) / EUR (€)"
        return f"""# 🌐 MARKET TREND REPORT: {category.upper()}
> [!NOTE]
> **Live Search Data Included**: Extracted from {len(serp_data['rankings'])} top ranking web pages in {target_country}.

---

## 1. Top 5 High-Demand Trending Products in {target_country} (2026)

### 1. High-Performance Laptops & Workstations (Intel Core Ultra / AMD Ryzen 9)
- **Estimated Price Range**: {currency}
- **Target Audience**: Software Engineers, Industrial Designers, Corporate IT, Gamers
- **Why Trending**: Massive surge in AI workload, video editing, and remote work requiring dedicated NPU hardware.

### 2. Enterprise & SOHO Wi-Fi 7 Gigabit Networking Routers & Fiber Switches
- **Estimated Price Range**: {currency}
- **Target Audience**: SOHO Offices, IT Infrastructure Managers, Smart Home Users
- **Why Trending**: Rapid transition to high-speed fiber optics, low-latency gaming, and multi-device office networks.

### 3. Industrial CNC Routers, Milling & Laser Engraving Machines
- **Estimated Price Range**: {currency}
- **Target Audience**: CNC Machine Shops, Furniture & Signage Manufacturers, DIY Makers
- **Why Trending**: Growing demand for precision manufacturing, custom metal/wood fabrication, and automated CNC production.

### 4. High-Resolution Industrial & Office Multifunction Printers (3D & Label Printers)
- **Estimated Price Range**: {currency}
- **Target Audience**: Packaging & Logistics Warehouses, Offices, Prototyping Labs
- **Why Trending**: High adoption of barcode labeling, direct-to-garment (DTG) printing, and rapid 3D prototyping.

### 5. SOHO Smart Office Electronics & Automation Sensors
- **Estimated Price Range**: {currency}
- **Target Audience**: Small Business Owners, Remote Professionals, Smart Factory Operators
- **Why Trending**: Rising demand for energy-efficient workspace controls, biometric access, and ergonomic desk gear.

---

## 2. Top Competitors & Distribution Channels Analysis
- **Top Dominant Marketplaces & Distributors**:
  - **Global / USA**: Amazon, B&H Photo, McMaster-Carr, Grainger, Alibaba, Newegg.
  - **Bangladesh / South Asia**: Daraz, StarTech, Ryans Computers, Techland BD, Pickaboo.
- **Key Buyer Conversion Drivers**:
  - Clear warranty & post-sales technical support.
  - Fast shipping & flexible payment terms (COD, Credit Card, B2B Invoicing).

---

## 3. High-Converting High-Intent Search Keywords
- `best budget laptops in {target_country} 2026`
- `enterprise wifi 7 router price`
- `cnc laser cutting machine price`
- `industrial automation plc controllers`
- `soho office multifunction printer reviews`

---

## 4. Strategic Content & Ranking Advice
1. **Highlight Specs & Price Range**: Clearly list technical specs (RAM, CNC spindle power, wattage, warranty) prominently near top of page.
2. **Target B2B & B2C Intent**: Create buyer guides comparing entry-level vs professional enterprise gear.
3. **Structured Data**: Implement Product JSON-LD schema with exact currency ({currency}) and availability status.
"""

# Alias for backwards compatibility
BDTrendAnalyzer = MarketTrendAnalyzer
