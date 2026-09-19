import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Global & Industrial Market Product Categories
MARKET_TREND_CATEGORIES = [
    "💻 Computer & Components (Laptops, Desktops, GPUs, Storage)",
    "📡 Networking & Wireless Gadgets (Routers, Switches, Access Points, Fiber)",
    "🖨️ Printing, Scanners & Office Electronics (SOHO Equipment, 3D Printers)",
    "🏭 Industrial Machinery & Automation (Robotics, PLC, Sensors, Power)",
    "⚙️ CNC Industry & Precision Tools (CNC Routers, Milling, Laser Cutters, Lathes)",
    "🏠 SOHO & Smart Office Automation",
    "📱 Smart Electronics & Mobile Accessories (TWS, Smartwatches, Power Banks)",
    "🛍️ General E-Commerce & Retail Products",
    "✍️ Custom Category (User Defined)"
]

BD_TRENDING_CATEGORIES = MARKET_TREND_CATEGORIES  # Backward compatibility alias

TARGET_COUNTRIES = [
    "🌐 Worldwide / Global (USD $)",
    "🇧🇩 Bangladesh (BDT ৳)",
    "🇺🇸 United States (USD $)",
    "🇪🇺 Europe & UK (EUR € / GBP £)",
    "🇸🇬 Asia-Pacific & Middle East",
    "🌍 All Countries (Global Analysis)"
]

class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
    SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

    # Default Target Competitors (Global & Bangladesh Local)
    COMPETITOR_DOMAINS = [
        # Major Bangladesh E-commerce & Tech Competitors
        "daraz.com.bd",
        "startech.com.bd",
        "ryans.com",
        "pickaboo.com",
        "bdshop.com",
        "gadgetandgear.com",
        "customercare.com.bd"
    ]

    # Target Product Keywords (Global & Bangladesh Market Focus)
    TARGET_KEYWORDS = [
        "best smartwatch price in bd",
        "wireless earbuds price in bd",
        "trending gadgets in bangladesh",
        "best budget laptop in bangladesh"
    ]

    # Global & Industrial Market Product Categories (Class Level)
    MARKET_TREND_CATEGORIES = MARKET_TREND_CATEGORIES
    BD_TRENDING_CATEGORIES = BD_TRENDING_CATEGORIES
    TARGET_COUNTRIES = TARGET_COUNTRIES

    # Output Directory for generated reports
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./reports")
