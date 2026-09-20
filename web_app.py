import streamlit as st
import os
import pandas as pd
from datetime import datetime
from config import Config
from master_agent import Master360Agent
from competitor_tracker import CompetitorTracker
from competitor_spy_agent import CompetitorSpyAgent
from indexing_checker import IndexingChecker
from social_media_analyzer import SocialMediaAnalyzer
from bd_trend_analyzer import BDTrendAnalyzer
from seo_writer_agent import SEOWriterAgent
from agent_activity import AgentActivityLogger
from notifier import TelegramNotifier
from keyword_rank_tracker import KeywordRankTracker
from seo_healer_agent import SEOHealerAgent
from site_scraper_clone_agent import SiteScraperCloneAgent
from ahrefs_semrush_deep_agent import AhrefsSemrushDeepAgent
from auth import AuthManager

# Helper function to save API Keys permanently into .env file
def save_env_keys(gemini_key, tavily_key, telegram_token="", telegram_chat=""):
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    existing_keys = {}
    
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    parts = line.split("=", 1)
                    existing_keys[parts[0].strip()] = parts[1].strip()
                    
    if gemini_key:
        existing_keys["GEMINI_API_KEY"] = gemini_key
    if tavily_key:
        existing_keys["TAVILY_API_KEY"] = tavily_key
    if telegram_token:
        existing_keys["TELEGRAM_BOT_TOKEN"] = telegram_token
    if telegram_chat:
        existing_keys["TELEGRAM_CHAT_ID"] = telegram_chat
        
    with open(env_path, "w", encoding="utf-8") as f:
        for k, v in existing_keys.items():
            f.write(f"{k}={v}\n")

    if gemini_key:
        Config.GEMINI_API_KEY = gemini_key
        os.environ["GEMINI_API_KEY"] = gemini_key
    if tavily_key:
        Config.TAVILY_API_KEY = tavily_key
        os.environ["TAVILY_API_KEY"] = tavily_key
    if telegram_token:
        os.environ["TELEGRAM_BOT_TOKEN"] = telegram_token
    if telegram_chat:
        os.environ["TELEGRAM_CHAT_ID"] = telegram_chat

def check_execution_permission() -> bool:
    """Check if current logged in user has execution permissions.
    If Public Demo user, show notification and return False."""
    user = st.session_state.get("user_data") or {}
    role = user.get("role", "Admin")
    if role == "Demo":
        st.warning("🔒 **READ-ONLY DEMO MODE ACTIVE**: You are logged in as Public Demo User (`demo`). You can navigate all 12 operational tabs, view dashboards, system features & sample reports, but live engine execution is restricted to Master Admin (Abdullah Al Naser).")
        return False
    return True

# 1. Configure Page Settings
st.set_page_config(
    page_title="AGENT NASER SEO PRO",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS Theme: Clean White Background, Navy Blue Buttons, Crisp Typography & Aligned Cards
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Remove empty top header bar & adjust container padding */
    header[data-testid="stHeader"], div[data-testid="stHeader"], .stAppHeader {
        display: none !important;
        height: 0 !important;
    }

    /* Hide sidebar collapse/toggle buttons so sidebar never slides left/right */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    button[aria-label="Collapse sidebar"],
    button[aria-label="Expand sidebar"] {
        display: none !important;
        visibility: hidden !important;
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    html, body, .stApp, section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        overflow-x: hidden !important;
    }

    /* Hide all horizontal scrollbars */
    ::-webkit-scrollbar:horizontal {
        display: none !important;
        height: 0 !important;
    }

    /* Force all rendered markdown headings & result text to be small but bold */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        color: #1E3A8A !important;
        letter-spacing: -0.01em !important;
    }

    h1, .stMarkdown h1 { font-size: 18px !important; font-weight: 800 !important; margin-top: 6px !important; margin-bottom: 4px !important; }
    h2, .stMarkdown h2 { font-size: 15px !important; font-weight: 800 !important; margin-top: 6px !important; margin-bottom: 4px !important; }
    h3, .stMarkdown h3 { font-size: 14px !important; font-weight: 700 !important; margin-top: 4px !important; margin-bottom: 2px !important; }
    h4, h5, h6, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 { font-size: 13.5px !important; font-weight: 700 !important; margin-top: 4px !important; margin-bottom: 2px !important; }

    .stMarkdown p, .stMarkdown li, .stMarkdown td {
        font-size: 13.5px !important;
        line-height: 1.5 !important;
    }
    
    .stMarkdown strong, .stMarkdown b {
        font-weight: 700 !important;
        color: #0F172A !important;
    }

    /* Ahrefs-style Table & Dashboard Board Styling */
    .stMarkdown table {
        width: 100% !important;
        border-collapse: collapse !important;
        font-size: 13px !important;
        margin-top: 10px !important;
        margin-bottom: 16px !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }

    .stMarkdown th {
        background-color: #F8FAFC !important;
        color: #1E3A8A !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        font-size: 11.5px !important;
        padding: 10px 12px !important;
        border-bottom: 2px solid #CBD5E1 !important;
        border-right: 1px solid #E2E8F0 !important;
    }

    .stMarkdown td {
        padding: 8px 12px !important;
        border-bottom: 1px solid #F1F5F9 !important;
        border-right: 1px solid #F1F5F9 !important;
        color: #0F172A !important;
    }

    .stMarkdown tr:hover td {
        background-color: #F8FAFC !important;
    }

    .ahrefs-card {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        padding: 14px 18px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
    }

    /* Lock Streamlit sidebar PERMANENTLY OPEN & visible in all viewports/iframes */
    section[data-testid="stSidebar"] {
        display: flex !important;
        visibility: visible !important;
        transform: translate3d(0, 0, 0) !important;
        margin-left: 0 !important;
        left: 0 !important;
        width: 310px !important;
        min-width: 310px !important;
        max-width: 310px !important;
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
        overflow-x: hidden !important;
        overflow-y: auto !important;
    }

    /* Hide sidebar collapse/toggle controls completely */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"],
    button[aria-label="Collapse sidebar"],
    button[aria-label="Expand sidebar"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
    }

    div.stButton > button, 
    div.stDownloadButton > button,
    button[data-testid="baseButton-secondary"] {
        background-color: #1E3A8A !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 0.6rem 0.8rem !important;
        border: none !important;
        box-shadow: 0 2px 4px rgba(30, 58, 138, 0.15) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        text-align: left !important;
        font-size: 13px !important;
        line-height: 1.3 !important;
    }
    
    div.stButton > button *, 
    div.stDownloadButton > button *,
    button[data-testid="baseButton-secondary"] * {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Fix password visibility toggle icon button */
    div[data-baseweb="input"] button,
    div[data-baseweb="input"] button *,
    button[aria-label="Show password"], 
    button[aria-label="Hide password"], 
    button[data-testid="stBaseButton-icon"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #64748B !important;
        padding: 0 !important;
        width: auto !important;
        min-height: auto !important;
    }

    div.stButton > button:hover, 
    div.stDownloadButton > button:hover,
    button[data-testid="baseButton-secondary"]:hover {
        background-color: #1D4ED8 !important;
        box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3) !important;
    }
    
    div.stButton > button:hover *, 
    div.stDownloadButton > button:hover * {
        color: #FFFFFF !important;
    }

    input, textarea, select {
        background-color: #F8FAFC !important;
        border: 1px solid #CBD5E1 !important;
        color: #0F172A !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        box-shadow: 0 2px 4px rgba(30, 58, 138, 0.15) !important;
    }

    .stButton > button:hover {
        background-color: #1E40AF !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 6px rgba(30, 58, 138, 0.25) !important;
        transform: translateY(-1px);
    }

    .price-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 16px;
    }

    .price-card-popular {
        border: 2px solid #1E3A8A;
        background-color: #F8FAFC;
    }

    .price-title {
        font-size: 20px;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 8px;
    }

    .price-amount {
        font-size: 32px;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 16px;
    }

    .price-amount span {
        font-size: 16px;
        font-weight: 500;
        color: #64748B;
    }

    .feature-list {
        list-style-type: none;
        padding-left: 0;
        margin-bottom: 24px;
    }

    .feature-list li {
        font-size: 14px;
        color: #334155;
        padding: 6px 0;
        display: flex;
        align-items: center;
    }

    .feature-list li::before {
        content: "✓";
        color: #1E3A8A;
        font-weight: bold;
        margin-right: 8px;
    }

    .status-badge {
        display: inline-block;
        background-color: #DCFCE7;
        color: #166534;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 13px;
        margin-bottom: 16px;
    }

    .agent-badge-pill {
        display: inline-block;
        background-color: #EFF6FF;
        color: #1E3A8A;
        border: 1px solid #BFDBFE;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 700;
    }

    div[data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }

    .metric-container {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    div[data-testid="stExpander"] {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Initialize Agent Classes
@st.cache_resource
def get_agents():
    master = Master360Agent()
    tracker = CompetitorTracker()
    writer = SEOWriterAgent()
    indexing = IndexingChecker()
    social = SocialMediaAnalyzer(gemini_agent=writer)
    bd_trend = BDTrendAnalyzer(gemini_agent=writer)
    spy = CompetitorSpyAgent(gemini_agent=writer)
    telegram = TelegramNotifier()
    rank_tracker = KeywordRankTracker()
    healer = SEOHealerAgent()
    scraper = SiteScraperCloneAgent()
    deep_audit = AhrefsSemrushDeepAgent(gemini_agent=writer)
    return master, tracker, writer, indexing, social, bd_trend, spy, telegram, rank_tracker, healer, scraper, deep_audit

master_agent, tracker_agent, writer_agent, indexing_agent, social_agent, bd_agent, spy_agent, telegram_notifier, rank_tracker_agent, healer_agent, scraper_agent, deep_audit_agent = get_agents()

# 3.5 AUTHENTICATION & LOGIN GATE
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_data" not in st.session_state:
    st.session_state.user_data = None

if not st.session_state.authenticated:
    st.markdown("""
    <style>
        div[data-testid="stSidebar"] {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Modern Side-by-Side 2-Column Login Layout: Left Agent Picture & Info, Right Login/Register Form (Symmetrically Aligned)
    pad_left, left_agent_col, pad_mid, right_form_col, pad_right = st.columns([0.25, 1.05, 0.1, 1.25, 0.25], vertical_alignment="center")

    with left_agent_col:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 10px;">
                <h1 style="color: #1E3A8A; font-size: 22px; font-weight: 800; margin-top: 0px; margin-bottom: 4px; letter-spacing: -0.01em;">AGENT NASER SEO PRO</h1>
                <span style="font-size: 11px; background: #1E3A8A; color: #FFFFFF; padding: 4px 12px; border-radius: 20px; font-weight: 700;">🕵️ AUTONOMOUS AI AGENT</span>
            </div>
        """, unsafe_allow_html=True)
        
        avatar_candidates = [
            os.path.join(os.path.dirname(__file__), "assets", "agent_avatar.jpg"),
            os.path.join(os.path.dirname(__file__), "agent_avatar.jpg"),
            os.path.join(os.path.dirname(__file__), "netlify_deploy", "agent_avatar.jpg")
        ]
        found_avatar = None
        for cand in avatar_candidates:
            if os.path.exists(cand):
                found_avatar = cand
                break
        if found_avatar:
            st.image(found_avatar, use_container_width=True)

    with right_form_col:
        # Side-by-Side Login & Registration Tabs
        login_tab, register_tab = st.tabs(["🔑 SIGN IN PANEL", "📝 CREATE ACCOUNT"])

        with login_tab:
            # COMPACT PUBLIC DEMO ACCOUNT NOTICE BANNER (ADMIN CREDENTIALS HIDDEN)
            st.markdown("""
            <div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; padding: 6px 10px; margin-top: 6px; margin-bottom: 8px; font-size: 11.5px; text-align: center;">
                <b>👁️ Public Demo Access:</b> Username: <code>demo</code> | Password: <code>demo123</code>
            </div>
            """, unsafe_allow_html=True)

            if st.button("👁️ 1-CLICK DEMO LOGIN (READ-ONLY)", use_container_width=True, key="btn_quick_demo"):
                success, u_data, msg = AuthManager.authenticate("demo", "demo123")
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_data = u_data
                    st.success(msg)
                    st.rerun()

            login_user = st.text_input("Username or Email", placeholder="e.g. admin or demo", key="l_user")
            login_pass = st.text_input("Password", type="password", placeholder="Enter password", key="l_pass")
            
            if st.button("🔑 SIGN IN TO AGENT NASER SEO PRO", use_container_width=True, key="btn_signin"):
                if not login_user or not login_pass:
                    st.error("Please enter both username/email and password.")
                else:
                    success, u_data, msg = AuthManager.authenticate(login_user, login_pass)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_data = u_data
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

        with register_tab:
            st.markdown("<h4 style='color: #1E3A8A; text-align: center; font-weight: 800;'>📝 Register Account</h4>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 13px; color: #64748B; text-align: center; margin-bottom: 16px;'>Create a new user profile to run competitor audits & rank position scans.</p>", unsafe_allow_html=True)
            
            reg_name = st.text_input("Full Name", placeholder="e.g. Abdullah Al Naser", key="r_name")
            reg_email = st.text_input("Email Address", placeholder="e.g. naser@example.com", key="r_email")
            reg_user = st.text_input("Choose Username", placeholder="e.g. naserpro", key="r_user")
            reg_pass = st.text_input("Choose Password", type="password", placeholder="Create a strong password", key="r_pass")
            reg_plan = st.selectbox("Select Subscription Tier", ["🌱 Starter Free", "⚡ Pro Business", "🏢 Enterprise Agency"], key="r_plan")
            
            st.write("")
            if st.button("📝 REGISTER ACCOUNT", use_container_width=True, key="btn_reg"):
                if not reg_name or not reg_email or not reg_user or not reg_pass:
                    st.error("Please fill in all registration fields.")
                else:
                    ok, res_msg = AuthManager.register_user(reg_name, reg_email, reg_user, reg_pass, plan=reg_plan)
                    if ok:
                        st.success(res_msg)
                        st.info("Account created successfully! You can now switch to the '🔑 SIGN IN PANEL' tab.")
                    else:
                        st.error(res_msg)

    st.stop()  # Stop execution until user authenticates!

# 4. LEFT SIDEBAR: OPERATIONAL SEGMENTS
if "current_segment" not in st.session_state:
    st.session_state.current_segment = "🚀 360° Master Hub"

with st.sidebar:
    user_info = st.session_state.get("user_data") or {}
    st.markdown(f"<div style='background-color: #EFF6FF; border: 1px solid #BFDBFE; padding: 10px; border-radius: 8px; margin-bottom: 12px;'><p style='margin:0; font-size:12px; color:#1E3A8A; font-weight:700;'>👤 LOGGED IN AS:</p><p style='margin:0; font-size:14px; font-weight:800; color:#0F172A;'>{user_info.get('full_name', 'Admin')}</p><p style='margin:0; font-size:12px; color:#64748B;'>Role: {user_info.get('role', 'Admin')} | Plan: {user_info.get('plan', 'Enterprise Agency')}</p></div>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: #1E3A8A; font-weight: 800; margin-bottom: 0;'>AGENT NASER SEO PRO</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 13px; color: #64748B;'>AI Search & Competitor Intelligence</p>", unsafe_allow_html=True)
    st.write("")
    
    # PROMINENT TOP NAVY BLUE BUTTON FOR FOUNDER PROFILE
    if st.button("👨‍💼 ABOUT FOUNDER (ABDULLAH AL NASER)", use_container_width=True):
        st.session_state.current_segment = "👨‍💼 About Founder (Abdullah Al Naser)"

    st.divider()

    if st.button("👑 Ahrefs & Semrush Master Deep Audit", use_container_width=True):
        st.session_state.current_segment = "👑 Ahrefs & Semrush Master Deep Audit"

    if st.button("🔑 Master Keyword Research & Intent Matrix", use_container_width=True):
        st.session_state.current_segment = "🔑 Master Keyword Research & Intent Matrix"

    if st.button("🔗 Keyword Competitor Backlink Spy & Link Finder", use_container_width=True):
        st.session_state.current_segment = "🔗 Keyword Competitor Backlink Spy & Link Finder"

    if st.button("🌐 Master Web Scraper & Site Clone Extractor", use_container_width=True):
        st.session_state.current_segment = "🌐 Master Web Scraper & Site Clone Extractor"

    if st.button("⚡ 1-Click AI SEO Auto-Fixer & Rank Healer", use_container_width=True):
        st.session_state.current_segment = "⚡ 1-Click AI SEO Auto-Fixer & Rank Healer"

    if st.button("🚀 360° Master Hub", use_container_width=True):
        st.session_state.current_segment = "🚀 360° Master Hub"

    if st.button("🕵️ Competitor Spy & Reverse-Engineering", use_container_width=True):
        st.session_state.current_segment = "🕵️ Competitor Spy & Reverse-Engineering"

    if st.button("🎯 Keyword Rank Position Tracker", use_container_width=True):
        st.session_state.current_segment = "🎯 Keyword Rank Position Tracker"

    if st.button("📍 Local SEO & GMB Setup Suite", use_container_width=True):
        st.session_state.current_segment = "📍 Local SEO & GMB Setup Suite"

    if st.button("📦 Amazon FBA & Affiliate SEO Suite", use_container_width=True):
        st.session_state.current_segment = "📦 Amazon FBA & Affiliate SEO Suite"

    if st.button("🛍️ Shopify & Dropship SEO Suite", use_container_width=True):
        st.session_state.current_segment = "🛍️ Shopify & Dropship SEO Suite"

    if st.button("✍️ Blogger & Niche Content SEO Suite", use_container_width=True):
        st.session_state.current_segment = "✍️ Blogger & Niche Content SEO Suite"

    if st.button("📡 24/7 Agent Activity Stream", use_container_width=True):
        st.session_state.current_segment = "📡 24/7 Agent Activity Stream"

    if st.button("🔴🟢 Google Index Audit", use_container_width=True):
        st.session_state.current_segment = "🔴🟢 Google Index Audit"

    if st.button("🔍 Competitor SERP Tracker", use_container_width=True):
        st.session_state.current_segment = "🔍 Competitor SERP Tracker"

    if st.button("📱 Social Media Viral Analyzer", use_container_width=True):
        st.session_state.current_segment = "📱 Social Media Viral Analyzer"

    if st.button("🌐 Global & Industrial Market Trends", use_container_width=True):
        st.session_state.current_segment = "🌐 Global & Industrial Market Trends"

    if st.button("💳 SaaS Subscription Plans", use_container_width=True):
        st.session_state.current_segment = "💳 SaaS Subscription Plans"

    st.divider()

    # HIDDEN ADMIN API KEY SETTINGS (PROTECTED BY ADMIN PASSCODE)
    with st.expander("🔒 Admin Settings"):
        admin_pass = st.text_input("Enter Admin Passcode", type="password", help="Default passcode: naser123")
        if admin_pass == "naser123":
            st.success("Admin Access Granted")
            gemini_key = st.text_input("Gemini API Key", value=Config.GEMINI_API_KEY, type="password")
            tavily_key = st.text_input("Tavily API Key", value=Config.TAVILY_API_KEY, type="password")
            
            st.markdown("##### Real-Time Data Push Settings")
            tg_token = st.text_input("Telegram Bot Token", value=os.getenv("TELEGRAM_BOT_TOKEN", ""), type="password")
            tg_chat = st.text_input("Telegram Chat ID", value=os.getenv("TELEGRAM_CHAT_ID", ""))
            
            st.write("")
            if st.button("💾 SAVE API SETTINGS PERMANENTLY", use_container_width=True):
                save_env_keys(gemini_key, tavily_key, tg_token, tg_chat)
                st.success("✅ API Settings Saved Permanently to .env File!")
                
        elif admin_pass:
            st.error("Incorrect Admin Passcode")

    st.write("")
    if st.button("🚪 LOG OUT SESSION", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.rerun()

# 5. MAIN CONTENT AREA
st.markdown("""
<div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-left: 4px solid #1E3A8A; border-radius: 8px; padding: 12px 18px; margin-bottom: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1 style="color: #1E3A8A !important; font-size: 20px !important; font-weight: 800 !important; margin: 0 0 4px 0 !important; letter-spacing: -0.01em;">AGENT NASER SEO PRO</h1>
            <p style="color: #475569; font-size: 12.5px; margin: 0; font-weight: 500;">
                🕵️ Autonomous AI Engine for Competitor SERP Reverse-Engineering, Live Rank Tracking & Sitemap Index Audits.
            </p>
        </div>
        <div style="margin-top: 4px;">
            <span style="background-color: #EFF6FF; color: #1E3A8A; border: 1px solid #BFDBFE; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 20px;">
                🟢 14 AI MODULES ACTIVE
            </span>
        </div>
    </div>
    <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; padding-top: 8px; border-top: 1px solid #F1F5F9;">
        <span style="background-color: #F8FAFC; border: 1px solid #E2E8F0; color: #1E3A8A; font-size: 11.5px; font-weight: 700; padding: 3px 10px; border-radius: 6px;">🚀 360° SERP Spy</span>
        <span style="background-color: #F8FAFC; border: 1px solid #E2E8F0; color: #1E3A8A; font-size: 11.5px; font-weight: 700; padding: 3px 10px; border-radius: 6px;">⚡ AI Rank Healer</span>
        <span style="background-color: #F8FAFC; border: 1px solid #E2E8F0; color: #1E3A8A; font-size: 11.5px; font-weight: 700; padding: 3px 10px; border-radius: 6px;">🌐 Site Scraper & Clone</span>
        <span style="background-color: #F8FAFC; border: 1px solid #E2E8F0; color: #1E3A8A; font-size: 11.5px; font-weight: 700; padding: 3px 10px; border-radius: 6px;">🔴 Index Auditor</span>
        <span style="background-color: #F8FAFC; border: 1px solid #E2E8F0; color: #1E3A8A; font-size: 11.5px; font-weight: 700; padding: 3px 10px; border-radius: 6px;">🛒 E-Com & Local SEO</span>
        <span style="background-color: #F8FAFC; border: 1px solid #E2E8F0; color: #1E3A8A; font-size: 11.5px; font-weight: 700; padding: 3px 10px; border-radius: 6px;">📊 Ahrefs Board</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"### {st.session_state.current_segment}")
st.divider()

# SEGMENT 0: ABOUT FOUNDER (ABDULLAH AL NASER)
if st.session_state.current_segment == "👨‍💼 About Founder (Abdullah Al Naser)":
    st.subheader("👨‍💼 About Abdullah Al Naser - Founder & AI Systems Architect")
    
    # Hero Profile Header Card
    col_photo, col_info = st.columns([1, 2])
    with col_photo:
        photo_path = os.path.join(os.path.dirname(__file__), "assets", "naser_photo.jpg")
        if os.path.exists(photo_path):
            st.image(photo_path, caption="Abdullah Al Naser", use_container_width=True)
        else:
            st.info("Photo loading...")
            
    with col_info:
        st.markdown("""
        ## **ABDULLAH AL NASER**
        **Founder, AI Search Architect & Digital Business Strategist**
        
        📱 **Mobile / Direct Line**: `+8801678684141`  
        💬 **WhatsApp**: [Chat on WhatsApp (+8801678684141)](https://wa.me/8801678684141)  
        📧 **System Creator**: AGENT NASER SEO PRO Engine  
        📍 **Location**: Dhaka, Bangladesh  
        """)
        
        st.markdown("""
        <div style="background-color: #F8FAFC; border-left: 4px solid #1E3A8A; padding: 16px; border-radius: 6px; margin: 12px 0;">
            <p style="margin: 0; font-size: 15px; color: #1E293B; font-weight: 500;">
                "I specialize in building autonomous AI Agents, Search Engine Intelligence platforms, competitor reverse-engineering systems, and high-converting SEO engines for E-Commerce sellers, dropshippers, and global industrial businesses."
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    
    # Section 1: Who I Am & Professional Background
    st.markdown("### 👤 Who I Am & Professional Portfolio")
    st.markdown("""
    I am **Abdullah Al Naser**, an innovative tech creator, Search Engine Optimization specialist, and AI Agent Developer. 
    My work focuses on bridging advanced Artificial Intelligence with real-world digital commerce, SERP competitive intelligence, and automated marketing workflows.
    """)
    
    st.write("")
    
    # Section 2: What I Build & Technical Capabilities ("AMI KI KI BANATE PARCHI")
    st.markdown("### 🛠️ What I Build & Custom Systems Developed")
    st.markdown("Here is a summary of the specialized AI agents, automation platforms, and software engines I create:")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        #### 🤖 1. Autonomous AI Agents & SaaS Dashboards
        - Full-stack AI agents integrated with LLMs (Gemini, OpenAI, Claude).
        - Multi-tenant Streamlit & Python SaaS web applications with Admin controls.
        - Telegram bot integrations for real-time live alert streaming.
        
        #### 🕵️ 2. Competitor Spy & SERP Reverse-Engineering
        - Automated DuckDuckGo / Tavily Google search parsers.
        - Reverse-engineering competitor secret keywords, product focus, and content gaps.
        - Backlink matrix extraction and competitor ranking audit engines.
        
        #### 🎯 3. Keyword Position & Google Index Trackers
        - Real-time Google SERP position auditing (#1-3, Page 1, Page 2+, Unranked).
        - Domain Visibility Score calculations and timestamped position logs.
        - Automated `site:` search indexing verification tools.
        """)
        
    with c2:
        st.markdown("""
        #### 📦 4. E-Commerce SEO Engines (Amazon, Shopify & Local)
        - **Amazon FBA & Affiliate Suite**: ASIN title generation, 5 bullet points, backend search terms, affiliate reviews.
        - **Shopify & Dropshipping Suite**: High-converting product descriptions, meta titles, H1/H2 structures, Product JSON-LD schema.
        - **Local SEO & GMB Suite**: Google Maps 3-Pack rank booster, GMB category optimizer, 750-char description generator.
        
        #### 🏭 5. Global & Industrial Market Intelligence
        - Worldwide & local product trend scanning across 6+ countries/regions.
        - Market research across **Computer & IT**, **Networking**, **Printing**, **SOHO**, **Industrial Machinery**, and **CNC Industry** tools.
        
        #### 📱 6. Viral Social Media Content Extractor
        - Facebook Reels, TikTok & Shorts viral video hook extractor.
        - High-converting social media ad copy and promotional script generator.
        """)
        
    st.divider()
    
    # Section 3: Contact & Collaboration
    st.markdown("### 📞 Get in Touch with Abdullah Al Naser")
    st.markdown("Need a custom AI agent built for your business, an automated e-commerce system, or advanced SEO consulting?")
    
    col_call, col_wa = st.columns(2)
    with col_call:
        st.info("📞 **Direct Phone Call**: +8801678684141")
    with col_wa:
        st.success("💬 **WhatsApp Direct Chat**: [+8801678684141](https://wa.me/8801678684141)")

# SEGMENT 0.1: AHREFS & SEMRUSH MASTER DEEP AUDIT
elif st.session_state.current_segment == "👑 Ahrefs & Semrush Master Deep Audit":
    st.subheader("👑 Ahrefs & Semrush Master Deep Audit Engine")
    st.markdown("Run an enterprise-grade 360° deep audit ($499/mo paid tool equivalent) for any target website or domain. Analyzes Domain Rating (DR), Organic Traffic Value, Backlink Matrix, Core Web Vitals, Keyword Gaps & 5-Phase Master Execution Roadmap.")
    
    col_d1, col_d2 = st.columns([2, 1])
    with col_d1:
        deep_domain = st.text_input("Enter Target Website Address or Domain URL", placeholder="e.g. startech.com.bd, techlandbd.com, or yoursite.com", key="in_deep_dom")
        deep_keyword = st.text_input("Primary Focus Keyword (Optional)", placeholder="e.g. gaming mouse or laptop price in bd", key="in_deep_kw")
    with col_d2:
        st.caption("AI Agent will execute a deep Ahrefs & Semrush multi-tier audit covering backlinks, keyword position tiers, technical bugs & 5-phase growth strategy.")
        
    if st.button("👑 RUN AHREFS & SEMRUSH MASTER DEEP AUDIT"):
        if check_execution_permission():
            if not deep_domain:
                st.error("Please enter a target domain URL.")
            else:
                with st.spinner(f"Executing Enterprise Ahrefs & Semrush Deep Audit for '{deep_domain}'..."):
                    deep_res = deep_audit_agent.run_master_deep_audit(deep_domain, deep_keyword)
                    report = deep_res["report_markdown"]
                    
                    AgentActivityLogger.log_activity("Ahrefs & Semrush Master Audit", deep_domain, "SUCCESS", f"Generated deep enterprise audit report")
                    telegram_notifier.send_message(f"👑 *AHREFS & SEMRUSH DEEP AUDIT ALERT*\nExecuted deep audit for: `{deep_domain}` (DR: {deep_res['dr']})")
                    
                    st.markdown(f"<span class='status-badge'>🟢 REAL-TIME ENTERPRISE DEEP AUDIT GENERATED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                    st.download_button(
                        label="📥 DOWNLOAD AHREFS & SEMRUSH MASTER DEEP REPORT",
                        data=report,
                        file_name=f"ahrefs_semrush_deep_audit_{deep_domain.replace('.', '_')}.md",
                        mime="text/markdown"
                    )
                    st.markdown(report)

# SEGMENT 0.2: MASTER KEYWORD RESEARCH & INTENT MATRIX
elif st.session_state.current_segment == "🔑 Master Keyword Research & Intent Matrix":
    st.subheader("🔑 Master Keyword Research & Intent Matrix")
    st.markdown("Enter your main target keyword to generate **10 Seed Keywords**, **20 LSI Keywords**, **10 High-Intent Hit Keywords**, and **Competition Difficulty (Easy/Medium/Hard)**.")
    
    col_kw1, col_kw2 = st.columns([2, 1])
    with col_kw1:
        main_research_kw = st.text_input("Enter Your Main Target Keyword", placeholder="e.g. gaming mouse, laptop stand, or web hosting", key="in_res_kw")
    with col_kw2:
        st.caption("AI Agent will analyze SERP competition, calculate difficulty (Easy/Medium/Hard) & map 40 seed, LSI & hit keywords.")
        
    if st.button("🔑 RUN MASTER KEYWORD RESEARCH & INTENT MATRIX"):
        if check_execution_permission():
            if not main_research_kw:
                st.error("Please enter a main target keyword.")
            else:
                with st.spinner(f"Analyzing SERP Competition & Generating 40 Seed, LSI & Hit Keywords for '{main_research_kw}'..."):
                    kw_res = tracker_agent.generate_keyword_research_matrix(main_research_kw, gemini_agent=writer_agent)
                    report = kw_res["report_markdown"]
                    
                    AgentActivityLogger.log_activity("Keyword Research Matrix", main_research_kw, "SUCCESS", f"Generated 40 keywords & difficulty matrix")
                    telegram_notifier.send_message(f"🔑 *KEYWORD RESEARCH ALERT*\nGenerated keyword matrix for: `{main_research_kw}` ({kw_res['difficulty_label']})")
                    
                    st.markdown(f"<span class='status-badge'>🟢 REAL-TIME KEYWORD MATRIX GENERATED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                    st.download_button(
                        label="📥 DOWNLOAD MASTER KEYWORD RESEARCH REPORT",
                        data=report,
                        file_name=f"keyword_research_{main_research_kw.lower().replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                    st.markdown(report)

# SEGMENT 0.3: KEYWORD COMPETITOR BACKLINK SPY & LINK FINDER
elif st.session_state.current_segment == "🔗 Keyword Competitor Backlink Spy & Link Finder":
    st.subheader("🔗 Keyword Competitor Backlink Spy & Link Finder")
    st.markdown("Enter your main target keyword to discover the **Top 5 Ranking Google Competitors** and extract their exact live **Backlink Source URLs**, anchor text, domain authority DA, and 1-click backlink replication strategy.")
    
    col_bk1, col_bk2 = st.columns([2, 1])
    with col_bk1:
        target_bk_keyword = st.text_input("Enter Your Main Target Keyword", placeholder="e.g. gaming mouse price in bd or portable laptop stand", key="in_bk_kw")
    with col_bk2:
        st.caption("AI Agent will search Google SERP, extract Top 5 competitors, and map all their live referring backlink source URLs.")
        
    if st.button("🔗 FETCH TOP 5 COMPETITORS & BACKLINK SOURCES"):
        if check_execution_permission():
            if not target_bk_keyword:
                st.error("Please enter a target keyword.")
            else:
                with st.spinner(f"Scraping Top 5 SERP Competitors & Mapping Live Backlink Source URLs for '{target_bk_keyword}'..."):
                    bk_res = tracker_agent.fetch_top5_competitors_backlinks(target_bk_keyword, gemini_agent=writer_agent)
                    report = bk_res["report_markdown"]
                    
                    AgentActivityLogger.log_activity("Competitor Backlink Spy", target_bk_keyword, "SUCCESS", f"Mapped backlinks for top 5 competitors")
                    telegram_notifier.send_message(f"🔗 *BACKLINK SPY ALERT*\nMapped backlinks for keyword: `{target_bk_keyword}`")
                    
                    st.markdown(f"<span class='status-badge'>🟢 REAL-TIME BACKLINK DATA EXTRACTED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                    st.download_button(
                        label="📥 DOWNLOAD COMPETITOR BACKLINK SPY REPORT",
                        data=report,
                        file_name=f"competitor_backlinks_{target_bk_keyword.lower().replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                    st.markdown(report)

# SEGMENT 0.4: MASTER WEB SCRAPER, WHOIS & SITE CLONE EXTRACTOR
elif st.session_state.current_segment == "🌐 Master Web Scraper & Site Clone Extractor":
    st.subheader("🌐 Master Web Scraper, WHOIS & Site Clone Extractor")
    st.markdown("Scrape any target website to extract business phone numbers, email addresses, physical locations, Facebook/WhatsApp links, domain WHOIS owner details, live prices, tech stack scripts, and clean HTML clone templates.")
    
    scrape_target_url = st.text_input("Enter Target Website Address or Page URL", placeholder="e.g. https://targetsite.com or indexpro.app")
    
    if st.button("🌐 RUN MASTER WEB SCRAPE & SITE CLONE"):
        if check_execution_permission():
            if not scrape_target_url:
                st.error("Please enter a target website URL.")
            else:
                with st.spinner("Scraping Contact Details, Domain WHOIS Owner, Tech Stack Scripts, Live Prices & Generating Site Clone..."):
                    res_dict = scraper_agent.scrape_and_clone_website(scrape_target_url)
                    report = res_dict["report"]
                    AgentActivityLogger.log_activity("Master Web Scraper & Clone", scrape_target_url, "SUCCESS", f"Extracted contacts, WHOIS owner & HTML clone")
                    telegram_notifier.send_message(f"🌐 *MASTER WEB SCRAPER ALERT*\nScraped site & WHOIS for: `{scrape_target_url}`")
                    
                    st.markdown(f"<span class='status-badge'>🟢 REAL-TIME SCRAPE & CLONE DATA EXTRACTED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                    st.download_button(
                        label="📥 DOWNLOAD MASTER SCRAPE & SITE CLONE REPORT",
                        data=report,
                        file_name=f"site_scrape_{scrape_target_url.replace('https://', '').replace('http://', '').replace('/', '_')}.md",
                        mime="text/markdown"
                    )
                    st.markdown(report)

# SEGMENT 0.5: 1-CLICK AI SEO AUTO-FIXER & RANK HEALER
elif st.session_state.current_segment == "⚡ 1-Click AI SEO Auto-Fixer & Rank Healer":
    st.subheader("⚡ 1-Click AI SEO Auto-Fixer & Rank Healer")
    st.markdown("Diagnose page gaps vs top Google SERP competitors and generate copy-paste ready fix code (Meta tags, AEO AI Answer blocks, LSI paragraphs & JSON-LD schema).")
    
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        heal_url = st.text_input("Your Page URL", placeholder="e.g. https://mycompany.com/product-page")
        heal_kw = st.text_input("Target Keyword", placeholder="e.g. wireless gaming mouse price in bd")
    with col_h2:
        heal_comp = st.text_input("Top Competitor URL (Optional)", placeholder="e.g. https://competitor.com/best-product (Leave blank to auto-detect)")
        st.caption("AI Agent will scrape Google SERP, diagnose gap matrix & generate instant copy-paste fix code.")

    if st.button("⚡ GENERATE 1-CLICK COPY-PASTE SEO FIXES"):
        if check_execution_permission():
            if not heal_url or not heal_kw:
                st.error("Please enter both Your Page URL and Target Keyword.")
            else:
                with st.spinner("AI Agent Diagnosing Competitor Gaps & Generating Copy-Paste Fix Code..."):
                    report = healer_agent.heal_and_boost_page(heal_url, heal_kw, heal_comp)
                    AgentActivityLogger.log_activity("AI SEO Auto-Fixer", heal_url, "SUCCESS", f"Generated fix code for {heal_kw}")
                    telegram_notifier.send_message(f"⚡ *AI SEO AUTO-FIXER ALERT*\nGenerated fix package for: `{heal_url}` ({heal_kw})")
                    
                    st.markdown(f"<span class='status-badge'>🟢 REAL-TIME LIVE FIX PACKAGE GENERATED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                    st.download_button(
                        label="📥 DOWNLOAD 1-CLICK SEO FIX PACKAGE",
                        data=report,
                        file_name=f"seo_fix_{heal_kw.lower().replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                    st.markdown(report)

# SEGMENT 1: 360° MASTER HUB
elif st.session_state.current_segment == "🚀 360° Master Hub":
    st.subheader("360° All-in-One Intelligence Generator")
    st.markdown("Run a complete 360-degree audit for any target keyword or product page URL in 1 click.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        target_input = st.text_input("Target Keyword or Product Page URL", placeholder="e.g. Wireless Gaming Mouse or https://site.com/product")
    with col2:
        categories_list = getattr(Config, 'MARKET_TREND_CATEGORIES', getattr(Config, 'BD_TRENDING_CATEGORIES', ["Computer & Components", "Smart Electronics"]))
        category_input = st.selectbox("Category", categories_list)
        
    if st.button("RUN 360° MASTER SCAN"):
        if check_execution_permission():
            if not target_input:
                st.error("Please enter a target keyword or product URL.")
            else:
                with st.spinner("Fetching Live Google SERP, Competitors, Social Media Trends & Writing Content..."):
                    filepath, report = master_agent.run_full_360_analysis(target_input, category_input)
                    telegram_notifier.send_message(f"🚀 *AGENT NASER SEO PRO REAL-TIME ALERT*\nFinished 360° Master Scan for: `{target_input}`\nSaved to: `{filepath}`")
                    
                    st.markdown(f"<span class='status-badge'>🟢 REAL-TIME LIVE DATA FETCHED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                    st.success(f"Report Generated & Real-Time Data Transferred! Saved to {filepath}")
                    
                    st.download_button(
                        label="📥 DOWNLOAD 360° MASTER REPORT",
                        data=report,
                        file_name=f"360_master_{target_input.lower().replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                    st.markdown(report)

# SEGMENT 2: COMPETITOR SPY & SECRET REVERSE-ENGINEERING
elif st.session_state.current_segment == "🕵️ Competitor Spy & Reverse-Engineering":
    st.subheader("🕵️ Competitor Secret Reverse-Engineering & Spy Agent")
    st.markdown("Reveal competitor secret keywords, product focus, content structures, and backlink sources.")
    
    spy_target = st.text_input("Enter Competitor Domain or Page URL", placeholder="e.g. competitor.com or https://competitor.com/product")
    
    if st.button("RUN COMPETITOR SPY AUDIT"):
        if check_execution_permission():
            if not spy_target:
                st.error("Please enter a competitor domain or URL.")
            else:
                with st.spinner("Reverse-Engineering Competitor Keywords, Content & Backlink Matrix..."):
                    report = spy_agent.spy_on_competitor(spy_target)
                    AgentActivityLogger.log_activity("Competitor Spy Audit", spy_target, "SUCCESS", "Extracted competitor secret keywords & backlink matrix")
                    telegram_notifier.send_message(f"🕵️ *COMPETITOR SPY REAL-TIME ALERT*\nRevealed secrets for competitor: `{spy_target}`")
                    
                    st.markdown(f"<span class='status-badge'>🟢 REAL-TIME LIVE DATA FETCHED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                    st.download_button(
                        label="📥 DOWNLOAD COMPETITOR SPY REPORT",
                        data=report,
                        file_name=f"competitor_spy_{spy_target.replace('.', '_').replace('/', '_')}.md",
                        mime="text/markdown"
                    )
                    st.markdown(report)

# SEGMENT 2.5: KEYWORD RANK POSITION TRACKER
elif st.session_state.current_segment == "🎯 Keyword Rank Position Tracker":
    st.subheader("🎯 Keyword Rank Position Tracker")
    st.markdown("Track exact Google rank positions (#1-3, Page 1, Page 2+, Unranked) and visibility score for your target domain.")
    
    rank_domain = st.text_input("Your Domain Name", placeholder="e.g. mycompany.com or https://mycompany.com")
    rank_keywords = st.text_area("Target Keywords (one per line or comma separated)", placeholder="wireless gaming mouse\nrgb mechanical keyboard\nm10 tws earbuds price in bd")
    
    if st.button("RUN KEYWORD RANK TRACKING"):
        if check_execution_permission():
            if not rank_domain or not rank_keywords:
                st.error("Please enter both domain name and keywords.")
            else:
                kw_list = [k.strip() for k in rank_keywords.replace(',', '\n').split('\n') if k.strip()]
                with st.spinner("Tracking exact Google rank positions across SERPs..."):
                    report = rank_tracker_agent.track_keyword_positions(rank_domain, kw_list)
                    AgentActivityLogger.log_activity("Keyword Rank Position Audit", rank_domain, "SUCCESS", f"Tracked {len(kw_list)} keywords")
                    telegram_notifier.send_message(f"🎯 *KEYWORD RANK POSITION ALERT*\nTracked `{rank_domain}` for {len(kw_list)} keywords")
                    
                    st.markdown(f"<span class='status-badge'>🟢 REAL-TIME LIVE DATA FETCHED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                    st.download_button(
                        label="📥 DOWNLOAD KEYWORD RANK POSITION REPORT",
                        data=report,
                        file_name=f"keyword_ranks_{rank_domain.replace('.', '_')}.md",
                        mime="text/markdown"
                    )
                    st.markdown(report)

# SEGMENT 3: LOCAL SEO & GMB SETUP SUITE
elif st.session_state.current_segment == "📍 Local SEO & GMB Setup Suite":
    st.subheader("📍 Local SEO & Google My Business (GMB) Optimization Suite")
    st.markdown("Optimize Google Maps 3-Pack Rankings, GMB Categories, 750-char Description, Local Citations, and LocalBusiness Schema.")
    
    local_biz = st.text_input("Business Name or Local Service", placeholder="e.g. Naser Tech Shop or IT Support Agency")
    local_city = st.text_input("Target City / Location", value="Dhaka, Bangladesh", placeholder="e.g. Dhaka, Bangladesh or Chittagong")
    local_notes = st.text_area("Business Details / Phone / Opening Hours", placeholder="e.g. Gulshan Dhaka, Phone: +8801700000000, Open 9am-8pm")
    
    if st.button("GENERATE LOCAL SEO & GMB SUITE"):
        if check_execution_permission():
            if not local_biz:
                st.error("Please enter your business name or local service.")
            else:
                with st.spinner("Analyzing Local Search Intent & Generating GMB Setup Package..."):
                    report = writer_agent.generate_local_gmb_seo(local_biz, local_city, local_notes)
                    AgentActivityLogger.log_activity("Local SEO & GMB Setup", local_biz, "SUCCESS", f"Location: {local_city}")
                    telegram_notifier.send_message(f"📍 *LOCAL SEO & GMB REAL-TIME ALERT*\nGenerated GMB Suite for: `{local_biz}` ({local_city})")
                    
                    st.markdown(f"<span class='status-badge'>🟢 REAL-TIME LIVE DATA FETCHED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                    st.download_button(
                        label="📥 DOWNLOAD LOCAL GMB SUITE REPORT",
                        data=report,
                        file_name=f"local_gmb_{local_biz.lower().replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                    st.markdown(report)

# SEGMENT 4: AMAZON FBA & AFFILIATE SEO SUITE
elif st.session_state.current_segment == "📦 Amazon FBA & Affiliate SEO Suite":
    st.subheader("📦 Amazon FBA Seller & Affiliate Marketing SEO Suite")
    st.markdown("Optimize Amazon ASIN Product Titles, 5 Bullet Point Features, Backend Search Terms, and Affiliate Review Blogs.")
    
    amz_product = st.text_input("Amazon Product Name, ASIN, or Keyword", placeholder="e.g. Ergonomic Gaming Mouse")
    amz_notes = st.text_area("Amazon Listing Directives / Target Audience", placeholder="e.g. Emphasize 50h battery life, 1-year replacement warranty, target PC gamers")
    
    if st.button("GENERATE AMAZON SEO SUITE"):
        if check_execution_permission():
            if not amz_product:
                st.error("Please enter an Amazon product name or keyword.")
            else:
                with st.spinner("Fetching Real-Time Amazon & SERP Market Data..."):
                    analysis = tracker_agent.analyze_keyword(amz_product)
                    report = writer_agent.generate_amazon_seo(amz_product, analysis, amz_notes)
                    AgentActivityLogger.log_activity("Amazon FBA & Affiliate SEO", amz_product, "SUCCESS", "Generated Amazon Listing & Review Schema")
                    telegram_notifier.send_message(f"📦 *AMAZON SEO REAL-TIME ALERT*\nGenerated Amazon SEO Suite for: `{amz_product}`")
                    
                    st.markdown(f"<span class='status-badge'>🟢 REAL-TIME LIVE DATA FETCHED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                    st.download_button(
                        label="📥 DOWNLOAD AMAZON SEO REPORT",
                        data=report,
                        file_name=f"amazon_seo_{amz_product.lower().replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                    st.markdown(report)

# SEGMENT 5: SHOPIFY & DROPSHIP SEO SUITE
elif st.session_state.current_segment == "🛍️ Shopify & Dropship SEO Suite":
    st.subheader("🛍️ Shopify Store & Dropshipping Product Conversion Suite")
    st.markdown("Generate copy-paste ready Shopify Meta Titles, Meta Descriptions, H1/H2 Product Descriptions, and Product JSON-LD Schemas.")
    
    shop_product = st.text_input("Shopify Product Name or URL Handle", placeholder="e.g. RGB Wireless Gaming Mouse")
    shop_notes = st.text_area("Shopify Directives (Price BDT/USD, Free Shipping, Target Audience)", placeholder="e.g. Price 1800 BDT, Free Delivery inside Dhaka, 1-year warranty")
    
    if st.button("GENERATE SHOPIFY DROPSHIP SUITE"):
        if check_execution_permission():
            if not shop_product:
                st.error("Please enter a product name.")
            else:
                with st.spinner("Fetching Real-Time E-Commerce SERP Data..."):
                    analysis = tracker_agent.analyze_keyword(shop_product)
                    report = writer_agent.generate_shopify_seo(shop_product, analysis, shop_notes)
                    AgentActivityLogger.log_activity("Shopify Dropship SEO Suite", shop_product, "SUCCESS", "Generated Shopify Product SEO & Schema")
                    telegram_notifier.send_message(f"🛍️ *SHOPIFY DROPSHIP REAL-TIME ALERT*\nGenerated Shopify Suite for: `{shop_product}`")
                    
                    st.markdown(f"<span class='status-badge'>🟢 REAL-TIME LIVE DATA FETCHED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                    st.download_button(
                        label="📥 DOWNLOAD SHOPIFY SEO SUITE",
                        data=report,
                        file_name=f"shopify_seo_{shop_product.lower().replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                    st.markdown(report)

# SEGMENT 6: BLOGGER & NICHE CONTENT SEO SUITE
elif st.session_state.current_segment == "✍️ Blogger & Niche Content SEO Suite":
    st.subheader("✍️ Blogger & Niche Content SEO Suite")
    st.markdown("Generate Google E-E-A-T articles, AEO AI Overview summaries, Search Descriptions, and FAQPage JSON-LD Schema.")
    
    blog_topic = st.text_input("Blogger Topic or Niche Keyword", placeholder="e.g. How to choose best gaming laptop in 2026")
    blog_notes = st.text_area("Blogger Directives / Target Niche Audience", placeholder="e.g. Focus on budget options, AdSense monetization, and high E-E-A-T guidelines")
    
    if st.button("GENERATE BLOGGER ARTICLE & STRATEGY"):
        if check_execution_permission():
            if not blog_topic:
                st.error("Please enter a blog topic.")
            else:
                with st.spinner("Fetching Real-Time Niche SERP Insights..."):
                    analysis = tracker_agent.analyze_keyword(blog_topic)
                    report = writer_agent.generate_blogger_seo(blog_topic, analysis, blog_notes)
                    AgentActivityLogger.log_activity("Blogger Niche Content SEO", blog_topic, "SUCCESS", "Generated Blogger E-E-A-T article")
                    telegram_notifier.send_message(f"✍️ *BLOGGER SEO REAL-TIME ALERT*\nGenerated Niche Blog Suite for: `{blog_topic}`")
                    
                    st.markdown(f"<span class='status-badge'>🟢 REAL-TIME LIVE DATA FETCHED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                    st.download_button(
                        label="📥 DOWNLOAD BLOGGER ARTICLE MARKDOWN",
                        data=report,
                        file_name=f"blogger_seo_{blog_topic.lower().replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                    st.markdown(report)

# SEGMENT 7: 24/7 AGENT ACTIVITY STREAM
elif st.session_state.current_segment == "📡 24/7 Agent Activity Stream":
    st.subheader("📡 24/7 Real-Time Agent Activity & Data Transfer Stream")
    
    col_status, col_btn = st.columns([3, 1])
    with col_status:
        st.markdown("<span class='status-badge'>🟢 AGENT STATUS: ACTIVE 24/7 & MONITORING</span>", unsafe_allow_html=True)
    with col_btn:
        if st.button("🔄 REFRESH LIVE STREAM"):
            st.rerun()
            
    st.write("")
    st.markdown("Below is the live real-time timestamped log of all background actions performed by **AGENT NASER SEO PRO**:")
    
    activities = AgentActivityLogger.get_activities()
    if activities:
        df = pd.DataFrame(activities)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No background activity logged yet. Run a 360° scan or daily job to populate real-time activity stream.")

# SEGMENT 8: GOOGLE INDEX AUDIT & NON-INDEXED SITE CRAWLER
elif st.session_state.current_segment == "🔴🟢 Google Index Audit":
    st.subheader("🔴 Google Index Audit - Non-Indexed Site Pages & Products Finder")
    st.markdown("Audit your website sitemap/pages to detect **ONLY the non-indexed (un-indexed)** products, category pages, and URLs with exact diagnostic reasons.")
    
    tab_auto, tab_manual = st.tabs(["⚡ Full Site Auto-Sitemap Crawler (Non-Indexed Only)", "📝 Custom Product / URL List Audit"])
    
    with tab_auto:
        st.markdown("#### ⚡ Auto-Crawl Entire Website & Detect Non-Indexed Pages")
        st.markdown("Automatically extracts all products, categories, and page URLs from `sitemap.xml` / navigation and reports **ONLY THE NON-INDEXED URLs**.")
        auto_domain = st.text_input("Enter Website Domain", placeholder="e.g. mycompany.com or https://mycompany.com", key="auto_domain_key")
        
        if st.button("RUN FULL SITE NON-INDEXED AUDIT", key="auto_audit_btn"):
            if check_execution_permission():
                if not auto_domain:
                    st.error("Please enter a valid website domain.")
                else:
                    with st.spinner("Crawling website sitemap & auditing Google Index status for non-indexed pages..."):
                        report = indexing_agent.audit_full_site_non_indexed_only(auto_domain)
                        AgentActivityLogger.log_activity("Full Site Non-Indexed Audit", auto_domain, "SUCCESS", "Audited website sitemap for non-indexed pages")
                        telegram_notifier.send_message(f"🔴 *NON-INDEXED SITE AUDIT ALERT*\nAudited `{auto_domain}` for non-indexed pages")
                        
                        st.markdown(f"<span class='status-badge'>🟢 REAL-TIME LIVE DATA FETCHED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                        st.download_button(
                            label="📥 DOWNLOAD NON-INDEXED PAGES REPORT",
                            data=report,
                            file_name=f"non_indexed_{auto_domain.replace('.', '_').replace('/', '_')}.md",
                            mime="text/markdown"
                        )
                        st.markdown(report)

    with tab_manual:
        st.markdown("#### 📝 Custom Product / Page List Audit")
        domain_input = st.text_input("Your Company Domain", placeholder="e.g. mycompany.com or https://mycompany.com", key="manual_domain_key")
        products_input = st.text_area("Product Names or Page URLs (one per line or comma separated)", placeholder="Wireless Earbuds\nRGB Mouse\nhttps://mycompany.com/product/laptop")
        only_non_indexed = st.checkbox("Show ONLY Non-Indexed Pages in Report", value=True, help="Filter out indexed pages and show only non-indexed results")
        
        if st.button("RUN CUSTOM LIST INDEXING AUDIT", key="manual_audit_btn"):
            if check_execution_permission():
                if not domain_input or not products_input:
                    st.error("Please provide both your domain and product list.")
                else:
                    product_list = [p.strip() for p in products_input.replace(',', '\n').split('\n') if p.strip()]
                    with st.spinner("Auditing Real-Time Google Index Status..."):
                        report = indexing_agent.check_product_indexing(domain_input, product_list, non_indexed_only=only_non_indexed)
                        AgentActivityLogger.log_activity("Google Index Audit", domain_input, "SUCCESS", f"Audited {len(product_list)} products")
                        telegram_notifier.send_message(f"🔴🟢 *INDEXING AUDIT REAL-TIME ALERT*\nAudited `{domain_input}` for {len(product_list)} products")
                        
                        st.markdown(f"<span class='status-badge'>🟢 REAL-TIME LIVE DATA FETCHED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                        st.download_button(
                            label="📥 DOWNLOAD INDEXING AUDIT REPORT",
                            data=report,
                            file_name=f"indexing_audit_{domain_input.replace('.', '_')}.md",
                            mime="text/markdown"
                        )
                        st.markdown(report)

# SEGMENT 9: COMPETITOR SERP TRACKER
elif st.session_state.current_segment == "🔍 Competitor SERP Tracker":
    st.subheader("Competitor SERP & Keyword Position Tracker")
    st.markdown("Audit Google Search Engine Result Pages (SERP) to detect competitor positions, page titles, and search intent.")
    
    kw_input = st.text_input("Enter Keyword or Product URL to Audit", placeholder="e.g. best mechanical keyboard price in bd")
    
    if st.button("SCAN COMPETITOR SERP"):
        if check_execution_permission():
            if not kw_input:
                st.error("Please enter a keyword or URL.")
            else:
                with st.spinner("Fetching Real-Time Live Google Search Rankings..."):
                    res = tracker_agent.analyze_keyword(kw_input)
                    AgentActivityLogger.log_activity("Competitor SERP Audit", kw_input, "SUCCESS", f"Found {res['total_results']} results")
                    telegram_notifier.send_message(f"🔍 *SERP AUDIT REAL-TIME ALERT*\nScanned SERP for: `{kw_input}` ({res['total_results']} results found)")
                    
                    st.markdown(f"<span class='status-badge'>🟢 REAL-TIME LIVE DATA FETCHED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                    st.subheader(f"Results for: '{res['keyword']}'")
                    
                    c1, c2 = st.columns(2)
                    c1.metric("Total Search Results Found", res['total_results'])
                    c2.metric("Competitor Matches Detected", len(res['competitor_matches']))
                    
                    for r in res['rankings']:
                        with st.expander(f"Rank #{r['rank']}: {r['title']} ({r['domain']}) {'⚠️ [COMPETITOR]' if r['is_competitor'] else ''}"):
                            st.write(f"**URL**: {r['url']}")
                            st.write(f"**Snippet**: {r['snippet']}")

# SEGMENT 10: SOCIAL MEDIA VIRAL ANALYZER
elif st.session_state.current_segment == "📱 Social Media Viral Analyzer":
    st.subheader("Social Media Viral Trend Analyzer")
    st.markdown("Extract viral video hooks, ad copies, and promotional strategies used on Facebook Reels, TikTok & YouTube Shorts.")
    
    sm_input = st.text_input("Product Name or Keyword", placeholder="e.g. M10 TWS Earbuds")
    
    if st.button("ANALYZE SOCIAL MEDIA TRENDS"):
        if check_execution_permission():
            if not sm_input:
                st.error("Please enter a product name.")
            else:
                with st.spinner("Fetching Real-Time Facebook, TikTok & YouTube Viral Trends..."):
                    report = social_agent.analyze_social_trends(sm_input)
                    AgentActivityLogger.log_activity("Social Media Trend Scan", sm_input, "SUCCESS", "Social media hooks extracted")
                    telegram_notifier.send_message(f"📱 *SOCIAL MEDIA REAL-TIME ALERT*\nAnalyzed viral trends for: `{sm_input}`")
                    
                    st.markdown(f"<span class='status-badge'>🟢 REAL-TIME LIVE DATA FETCHED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                    st.markdown(report)

# SEGMENT 11: GLOBAL & INDUSTRIAL MARKET TRENDS
elif st.session_state.current_segment in ["🌐 Global & Industrial Market Trends", "🇧🇩 BD Market Product Trends"]:
    st.subheader("🌐 Global, Regional & Industrial Market Product Trend Explorer")
    st.markdown("Discover top-selling trending products, B2B/B2C demand, pricing, and high-converting search terms for any country or industry (Computer, IT, Networking, Printing, SOHO, CNC & Machinery).")
    
    col_country, col_cat = st.columns(2)
    with col_country:
        country_list = getattr(Config, 'TARGET_COUNTRIES', ["🌐 Worldwide / Global (USD $)", "🇧🇩 Bangladesh (BDT ৳)"])
        country_sel = st.selectbox("Select Target Country / Region", country_list)
    with col_cat:
        category_list = getattr(Config, 'MARKET_TREND_CATEGORIES', getattr(Config, 'BD_TRENDING_CATEGORIES', ["Computer & Components", "Smart Electronics"]))
        cat_sel = st.selectbox("Select Product Industry / Category", category_list)
        
    custom_cat_input = ""
    if "Custom" in cat_sel:
        custom_cat_input = st.text_input("Enter Custom Category / Product Focus", placeholder="e.g. CNC Wood Routers, Industrial Automation PLC, Fiber Optic Switches")
        
    final_cat = custom_cat_input.strip() if custom_cat_input.strip() else cat_sel
    
    if st.button("ANALYZE MARKET TRENDS"):
        if check_execution_permission():
            with st.spinner(f"Fetching Real-Time Market Data for '{final_cat}' ({country_sel})..."):
                report = bd_agent.analyze_trending_products(category=final_cat, target_country=country_sel)
                AgentActivityLogger.log_activity("Global Market Trend Scan", f"{final_cat} ({country_sel})", "SUCCESS", "Market trends analyzed")
                telegram_notifier.send_message(f"🌐 *GLOBAL MARKET REAL-TIME ALERT*\nAnalyzed trends for: `{final_cat}` in `{country_sel}`")
                
                st.markdown(f"<span class='status-badge'>🟢 REAL-TIME LIVE DATA FETCHED: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 DOWNLOAD MARKET TREND REPORT",
                    data=report,
                    file_name=f"market_trends_{final_cat.lower().replace(' ', '_').replace('/', '_')}.md",
                    mime="text/markdown"
                )
                st.markdown(report)

# SEGMENT 12: SAAS PLANS & SUBSCRIPTIONS
elif st.session_state.current_segment == "💳 SaaS Subscription Plans":
    st.subheader("💳 AGENT NASER SEO PRO - SaaS Subscription Plans")
    st.markdown("Select your subscription model: **Monthly**, **Yearly (2 Months FREE)**, or **Corporate Enterprise**.")
    st.write("")
    
    plan_tab1, plan_tab2, plan_tab3 = st.tabs([
        "📅 Monthly Package (মাসিক প্যাকেজ)",
        "🎉 Yearly Package (বার্ষিক প্যাকেজ - 2 Months Free)",
        "🏢 Corporate / Enterprise Package (কর্পোরেট প্যাকেজ)"
    ])
    
    with plan_tab1:
        st.markdown("#### 📅 Monthly Subscription Plans (USD / BDT)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="price-card">
                <div>
                    <div class="price-title">👤 Single User Starter</div>
                    <div class="price-amount">USD $20 <span>/ Month</span></div>
                    <p style="color:#64748B; font-weight:600; margin-top:-10px;">(~BDT 2,400 / Month)</p>
                    <ul class="feature-list">
                        <li>1 Single User Account</li>
                        <li>1 Host Domain Full Audit</li>
                        <li>Google Index Sitemap Crawler (Up to 1,000 URLs)</li>
                        <li>Non-Indexed URL & Meta Robots Diagnostic</li>
                        <li>Basic SERP Competitor Spy Engine</li>
                        <li>Standard Markdown & HTML Report Export</li>
                        <li>Standard Email Support</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("SUBSCRIBE SINGLE USER ($20/MO)", key="m_single_btn", use_container_width=True):
                st.success("Selected USD $20 Monthly Single User Plan! Contact Admin to activate.")

        with col2:
            st.markdown("""
            <div class="price-card price-card-popular">
                <div>
                    <div class="price-title">🔥 Pro Single User (Popular)</div>
                    <div class="price-amount">USD $50 <span>/ Month</span></div>
                    <p style="color:#1E3A8A; font-weight:700; margin-top:-10px;">(~BDT 6,000 / Month)</p>
                    <ul class="feature-list">
                        <li>1 Pro Single User Account</li>
                        <li>5 Host Domains Full Audit</li>
                        <li>Google Index Sitemap Crawler (Up to 10,000 URLs)</li>
                        <li>Non-Indexed URL Detector (100% Real HTTP Live Check)</li>
                        <li>360° AI SEO & Competitor Spy Engine</li>
                        <li>Market Trends (CNC, Industrial, IT, Laptops)</li>
                        <li>Amazon & Shopify E-Commerce Product SEO</li>
                        <li>AEO & GEO FAQ Content Generator</li>
                        <li>Priority Chat & Email Support</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("UPGRADE TO PRO ($50/MO)", key="m_pro_btn", use_container_width=True):
                st.success("Selected USD $50 Monthly Pro Single User Plan! Contact Admin to activate.")

        with col3:
            st.markdown("""
            <div class="price-card">
                <div>
                    <div class="price-title">🏢 Corporate User / Agency</div>
                    <div class="price-amount">USD $150 <span>/ Month</span></div>
                    <p style="color:#166534; font-weight:700; margin-top:-10px;">(~BDT 18,000 / Month)</p>
                    <ul class="feature-list">
                        <li>Multi-User Team & Corporate Account (RBAC)</li>
                        <li>Unlimited Host Domains Full Audit</li>
                        <li>Google Index Sitemap Crawler (Unlimited URLs)</li>
                        <li>Real-Time Non-Indexed URL Diagnostic & Webhooks</li>
                        <li>Advanced Competitor Backlink & Content Gap Spy</li>
                        <li>Global Country SERP Filter (BD, USA, EU, Asia)</li>
                        <li>Telegram Bot Instant Indexing Alerts</li>
                        <li>24/7 VIP Dedicated Account Manager</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("SUBSCRIBE CORPORATE ($150/MO)", key="m_corp_btn", use_container_width=True):
                st.success("Selected USD $150 Monthly Corporate User Plan! Contact Admin to activate.")

    with plan_tab2:
        st.markdown("#### 🎉 Yearly Subscription Plans (Save 2 Months FREE)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="price-card">
                <div>
                    <div class="price-title">👤 Single User Yearly</div>
                    <div class="price-amount">USD $200 <span>/ Year</span></div>
                    <p style="color:#166534; font-weight:bold; margin-top:-10px;">🎁 Save $40 (Includes 2 Months FREE)</p>
                    <ul class="feature-list">
                        <li>1 Single User Account</li>
                        <li>1 Host Domain Full Audit</li>
                        <li>Google Index Sitemap Crawler (Up to 2,000 URLs)</li>
                        <li>Non-Indexed URL & Meta Robots Diagnostic</li>
                        <li>Basic SERP Competitor Spy Engine</li>
                        <li>Annual Indexing History Report</li>
                        <li>Priority Email Support</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("SUBSCRIBE SINGLE USER ($200/YR)", key="y_single_btn", use_container_width=True):
                st.success("Selected USD $200 Yearly Single User Plan! Contact Admin to activate.")

        with col2:
            st.markdown("""
            <div class="price-card price-card-popular">
                <div>
                    <div class="price-title">👑 Pro Single User Yearly (Best Value)</div>
                    <div class="price-amount">USD $500 <span>/ Year</span></div>
                    <p style="color:#166534; font-weight:bold; margin-top:-10px;">🎁 Save $100 (Includes 2 Months FREE)</p>
                    <ul class="feature-list">
                        <li>1 Pro Single User Account</li>
                        <li>5 Host Domains Full Audit</li>
                        <li>Google Index Sitemap Crawler (Up to 20,000 URLs)</li>
                        <li>100% Real HTTP Non-Indexed URL Diagnostic</li>
                        <li>360° AI SEO & Competitor Spy Engine</li>
                        <li>Full E-Commerce & Industrial Market Trend Intelligence</li>
                        <li>Automated Scheduled Weekly Sitemap Audits</li>
                        <li>Dedicated Onboarding & Strategy Setup Call</li>
                        <li>Priority Chat & Email Support</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("UPGRADE TO PRO ($500/YR)", key="y_pro_btn", use_container_width=True):
                st.success("Selected USD $500 Yearly Pro Single User Plan! Contact Admin to activate.")

        with col3:
            st.markdown("""
            <div class="price-card">
                <div>
                    <div class="price-title">⚡ Corporate User Yearly</div>
                    <div class="price-amount">USD $1,500 <span>/ Year</span></div>
                    <p style="color:#166534; font-weight:bold; margin-top:-10px;">🎁 Save $300 (Includes 2 Months FREE)</p>
                    <ul class="feature-list">
                        <li>Multi-User Team & Corporate Account (RBAC)</li>
                        <li>Unlimited Host Domains Full Audit</li>
                        <li>Unlimited Google Index Sitemap Crawler</li>
                        <li>Telegram Bot Instant Alerts for Non-Indexed Pages</li>
                        <li>Global Country SERP Filter & Country Trend Intelligence</li>
                        <li>Advanced E-Commerce & Keyword Strategy Engine</li>
                        <li>24/7 VIP Priority Support & SLA</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("SUBSCRIBE CORPORATE ($1,500/YR)", key="y_corp_btn", use_container_width=True):
                st.success("Selected USD $1,500 Yearly Corporate User Plan! Contact Admin to activate.")

    with plan_tab3:
        st.markdown("#### 🏢 Corporate & Enterprise Custom Packages")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="price-card price-card-popular">
                <div>
                    <div class="price-title">🏢 Corporate User / Agency Plan</div>
                    <div class="price-amount">USD $150 <span>/ Month</span></div>
                    <p style="color:#1E3A8A; font-weight:bold; margin-top:-10px;">💼 Full Agency & Multi-Site Solution ($1,500 / Year)</p>
                    <ul class="feature-list">
                        <li>Unlimited Host Domains & Enterprise Web Portals</li>
                        <li>Real-Time Automated Multi-Site Sitemap & Index Monitor</li>
                        <li>Non-Indexed URL Instant Telegram Bot & Custom Webhook Alerts</li>
                        <li>Custom AI Multi-Agent Autonomous Workflows</li>
                        <li>Up to 10 Team Member User Accounts (RBAC)</li>
                        <li>White-Label Custom PDF & HTML Branding Reports</li>
                        <li>Dedicated High-Speed API Access</li>
                        <li>24/7 Dedicated Account Manager & VIP Support</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("SUBSCRIBE CORPORATE USER ($150/MO)", key="tab3_corp_agency_btn", use_container_width=True):
                st.success("Selected Corporate User Plan! Dedicated Manager will reach out.")

        with col2:
            st.markdown("""
            <div class="price-card">
                <div>
                    <div class="price-title">🏛️ Private SaaS Enterprise / Custom</div>
                    <div class="price-amount">Custom Quote <span>/ Year</span></div>
                    <p style="color:#1E3A8A; font-weight:bold; margin-top:-10px;">🛡️ Private Server & Dedicated Infrastructure</p>
                    <ul class="feature-list">
                        <li>Private SaaS Dedicated Server Deployment</li>
                        <li>Unlimited Team Users & Custom Role-Based Access</li>
                        <li>Custom SEO & SERP Pipeline Integration</li>
                        <li>Custom AI Prompt Tuning for Specific Niche Sectors</li>
                        <li>On-Premise Data Security & SLA Guarantee</li>
                        <li>Direct Founder & Core Developer Engineering Support</li>
                        <li>1-on-1 SEO Architecture Strategy Consultations</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("CONTACT CORPORATE SALES", key="tab3_corp_custom_btn", use_container_width=True):
                st.info("Please email founder@agentnaser.com or contact live support for custom quotes.")

    st.write("")
    st.divider()
    st.subheader("💳 Supported Payment Gateways")
    st.markdown("**Global Payments**: Stripe, Visa, Mastercard, Wire Transfer | **Local BD Payments**: bKash, Nagad, Rocket, SSLCommerz, AmarPay")
