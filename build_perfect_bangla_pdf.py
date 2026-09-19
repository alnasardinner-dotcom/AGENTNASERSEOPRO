import os
import subprocess
import time
import shutil

def generate_perfect_bangla_pdf():
    proj_dir = os.path.dirname(__file__)
    reports_dir = os.path.join(proj_dir, "reports")
    pdf_reports_dir = r"C:\Users\DFIT\.gemini\antigravity\scratch\PDF_REPORTS"
    
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(pdf_reports_dir, exist_ok=True)

    html_path = os.path.join(reports_dir, "bangla_manual.html")
    pdf_proj_path = os.path.join(reports_dir, "2_AGENT_NASER_SEO_PRO_BANGLA_MANUAL.pdf")
    pdf_scratch_path = os.path.join(pdf_reports_dir, "2_AGENT_NASER_SEO_PRO_BANGLA_MANUAL.pdf")

    html_content = """<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <title>AGENT NASER SEO PRO - বাংলা ম্যানুয়াল ও গাইডলাইন (আপডেটেড ১৪টি মডিউল)</title>
    <link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        @page {
            size: A4;
            margin: 15mm;
        }
        body {
            font-family: 'Hind Siliguri', 'Segoe UI', Arial, sans-serif;
            color: #0F172A;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #FFFFFF;
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #1E3A8A;
            padding-bottom: 12px;
            margin-bottom: 20px;
        }
        .title {
            color: #1E3A8A;
            font-size: 24px;
            font-weight: 700;
            margin: 0 0 6px 0;
        }
        .subtitle {
            color: #475569;
            font-size: 13.5px;
            font-weight: 600;
            margin: 0;
        }
        .summary-box {
            background-color: #F8FAFC;
            border-left: 4px solid #1E3A8A;
            padding: 12px 16px;
            border-radius: 6px;
            margin-bottom: 24px;
            font-size: 13.5px;
        }
        .tool-card {
            background-color: #FFFFFF;
            border: 1px solid #CBD5E1;
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 14px;
            page-break-inside: avoid;
        }
        .tool-title {
            color: #1E3A8A;
            font-size: 16px;
            font-weight: 700;
            margin: 0 0 6px 0;
            border-bottom: 1px solid #F1F5F9;
            padding-bottom: 4px;
        }
        .tool-work {
            color: #1E293B;
            font-size: 13px;
            margin-bottom: 8px;
        }
        .tool-benefit {
            color: #166534;
            font-size: 13px;
            background-color: #F0FDF4;
            border: 1px solid #BBF7D0;
            border-radius: 6px;
            padding: 8px 12px;
            font-weight: 600;
        }
        .footer {
            margin-top: 24px;
            text-align: center;
            font-size: 13px;
            color: #64748B;
            border-top: 1px solid #CBD5E1;
            padding-top: 12px;
        }
    </style>
</head>
<body>

    <div class="header">
        <h1 class="title">🚀 AGENT NASER SEO PRO - বাংলা ম্যানুয়াল ও গাইডলাইন (১৪টি মডিউল)</h1>
        <p class="subtitle">Autonomous AI Search & Competitor Intelligence SaaS Engine | নির্মাতা: আব্দুল্লাহ আল নাছের (+8801678684141)</p>
    </div>

    <div class="summary-box">
        <strong>📌 প্ল্যাটফর্মের প্রধান উদ্দেশ্য (Executive Summary):</strong><br>
        AGENT NASER SEO PRO হলো একটি অত্যাধুনিক অটোনোমাস এআই সার্চ ইঞ্জিন ইন্টেলিজেন্স ও ওয়েব অটোমেশন প্ল্যাটফর্ম। এর মূল উদ্দেশ্য হলো—গুগল এবং এআই সার্চ ইঞ্জিনে (Google AI Overviews, Perplexity, ChatGPT) আপনার সাইটকে ১ নম্বরে র‍্যাংক করানো, প্রতিদ্বন্দী সাইটের সিক্রেট রিভার্স-ইঞ্জিনিয়ারিং করা, যেকোনো সাইট স্ক্র্যাপ/ক্লোন করা এবং ১ ক্লিকে অটো-ফিক্স তৈরি করা।
    </div>

    <!-- MODULE 1 NEW -->
    <div class="tool-card">
        <div class="tool-title">1. ⚡ 1-Click AI SEO Auto-Fixer & Rank Healer (এআই এসইও অটো-ফিক্সার)</div>
        <div class="tool-work"><strong>কী কাজ করে:</strong> গুগলের ১ নম্বর প্রতিদ্বন্দী সাইটের সাথে আপনার পেজের গ্যাপ অডিট করে এবং সরাসরি কপি-পেস্ট করার উপযোগী কোড ও কনটেন্ট ফিক্স জেনারেট করে (Meta Title, Description, AEO Answer Block, LSI Paragraph & JSON-LD Schema)।</div>
        <div class="tool-benefit">💡 <strong>উপকারিতা:</strong> সমস্যা খুঁজে নিয়ে সমাধান তৈরি করে দেয়। সাইটে কোড কপি-পেস্ট করলেই দ্রুত পজিশন টপ ৩-তে উন্নীত হয়।</div>
    </div>

    <!-- MODULE 2 NEW -->
    <div class="tool-card">
        <div class="tool-title">2. 🌐 Master Web Scraper, WHOIS & Site Clone Extractor (ওয়েব স্ক্র্যাপার ও ক্লোনার)</div>
        <div class="tool-work"><strong>কী কাজ করে:</strong> যেকোনো ওয়েবসাইটের ফোন নম্বর, হোয়াটসঅ্যাপ, অফিশিয়াল ইমেইল, অফিসের ঠিকানা, ডোমেইন মালিকের তথ্য (WHOIS), লাইভ প্রোডাক্ট দাম, সোশাল লিংক, টেকনোলজি স্ট্যাক এবং ক্লিন HTML সাইট ক্লোন কোড এক্সট্র্যাক্ট করে।</div>
        <div class="tool-benefit">💡 <strong>উপকারিতা:</strong> যেকোনো ওয়েবসাইটের ডাটা এক্সট্র্যাক্ট ও টেমপ্লেট ক্লোন ১ ক্লিকে সম্পাদন করা যায়।</div>
    </div>

    <!-- MODULE 3 -->
    <div class="tool-card">
        <div class="tool-title">3. 🚀 360° Master Hub (All-in-One Intelligence Generator)</div>
        <div class="tool-work"><strong>কী কাজ করে:</strong> ১ ক্লিক অডিটে যেকোনো প্রোডাক্ট বা কিওয়ার্ডের জন্য গুগলের লাইভ SERP ডাটা, প্রতিদ্বন্দীর তথ্য, সোশাল মিডিয়া হুক এবং পূর্ণাঙ্গ SEO/AEO/GEO আর্টিকেল একসাথে জেনারেট করে।</div>
        <div class="tool-benefit">💡 <strong>উপকারিতা:</strong> ১০ ঘণ্টার ম্যানুয়াল রিসার্চের কাজ ১ মিনিটে শেষ হয়। ১ ক্লিকে ১০০০+ ওয়ার্ডের আর্টিকেলের সাথে অন-পেজ ও অফ-পেজ প্ল্যান পাওয়া যায়।</div>
    </div>

    <!-- MODULE 4 -->
    <div class="tool-card">
        <div class="tool-title">4. 🕵️ Competitor Spy & Reverse-Engineering (প্রতিদ্বন্দীর গুপ্তচর)</div>
        <div class="tool-work"><strong>কী কাজ করে:</strong> প্রতিদ্বন্দীদের গোপন কিওয়ার্ড, ব্যাকলিংক সোর্স ম্যাট্রিক্স, কনটেন্ট গ্যাপিং এবং র‍্যাঙ্কিং স্ট্র্যাটেজি লাইভ রিভার্স-ইঞ্জিনিয়ারিং করে।</div>
        <div class="tool-benefit">💡 <strong>উপকারিতা:</strong> প্রতিদ্বন্দীরা কীভাবে ১ নম্বরে আছে তা জানা যায় এবং তাদের দুর্বল বিষয়গুলো কাজে লাগিয়ে সহজেই তাদের ওভারটেক করা যায়।</div>
    </div>

    <!-- MODULE 5 -->
    <div class="tool-card">
        <div class="tool-title">5. 🎯 Keyword Rank Position Tracker (গুগল র‍্যাংক ট্র্যাকার)</div>
        <div class="tool-work"><strong>কী কাজ করে:</strong> গুগল সার্চ রেজাল্ট থেকে আপনার বা ক্লায়েন্টের ডোমেইনের রিয়েল-টাইম পজিশন (Rank #1-25, Page 1, Page 2+, Unranked 30+) অডিট করে এবং Visibility Score হিসাব করে।</div>
        <div class="tool-benefit">💡 <strong>উপকারিতা:</strong> কিওয়ার্ডের সঠিক পজিশন জানা যায় এবং Rank #4-10 পজিশনে থাকা লিংকগুলোকে সহজেই Top 3-তে পুশ করার অ্যাকশন প্ল্যান দেয়।</div>
    </div>

    <!-- MODULE 6 -->
    <div class="tool-card">
        <div class="tool-title">6. 📍 Local SEO & GMB Setup Suite (লোকাল বিজনেস ও গুগল ম্যাপস)</div>
        <div class="tool-work"><strong>কী কাজ করে:</strong> Google Maps 3-Pack র‍্যাঙ্কিং বুস্টার, GMB ক্যাটাগরি, ৭৫০ অক্ষরের অপটিমাইজড ডেসক্রিপশন, লোকাল সাইটেশন ও LocalBusiness Schema জেনারেট করে।</div>
        <div class="tool-benefit">💡 <strong>উপকারিতা:</strong> স্থানীয় কাস্টমারদের সরাসরি ফোন কল, ম্যাপ ডিরেকশন ও লোকাল দোকান/সার্ভিসের সেল বহুগুণ বৃদ্ধি পায়।</div>
    </div>

    <!-- MODULE 7 -->
    <div class="tool-card">
        <div class="tool-title">7. 📦 Amazon FBA & Affiliate SEO Suite (আমাজন সেলার ও অ্যাফিলিয়েট)</div>
        <div class="tool-work"><strong>কী কাজ করে:</strong> আমাজন প্রোডাক্ট টাইটেল, ৫টি হাই-কনভার্টিং বুলেট পয়েন্ট, ব্যাকএন্ড সার্চ টার্মস এবং আমাজন অ্যাফিলিয়েট রিভিউ ব্লগ তৈরি করে।</div>
        <div class="tool-benefit">💡 <strong>উপকারিতা:</strong> আমাজন সেলারদের কনভার্সন রেট (CVR) বাড়ে এবং অ্যাফিলিয়েট মার্কেটরদের সেলস কমিশন কয়েক গুণ বৃদ্ধি পায়।</div>
    </div>

    <!-- MODULE 8 -->
    <div class="tool-card">
        <div class="tool-title">8. 🛍️ Shopify & Dropshipping SEO Suite (ই-কমার্স শপ)</div>
        <div class="tool-work"><strong>কী কাজ করে:</strong> শপিফাই ই-কমার্স স্টোরের প্রোডাক্ট ও কালেকশন মেটা ডাটা, ডেসক্রিপশন এবং Product JSON-LD Schema তৈরি করে।</div>
        <div class="tool-benefit">💡 <strong>উপকারিতা:</strong> অ্যাড ছাড়াই গুগলে ফ্রিতে ই-কমার্স প্রোডাক্ট র‍্যাংক করে অর্গানিক সেলস বহুগুণ বাড়ানো যায়।</div>
    </div>

    <!-- MODULE 9 -->
    <div class="tool-card">
        <div class="tool-title">9. ✍️ Blogger & Niche Content SEO Suite (ব্লগিং ও অ্যাডসেন্স)</div>
        <div class="tool-work"><strong>কী কাজ করে:</strong> নিচ ব্লগের জন্য গুগল E-E-A-T নিয়ম মেনে পোস্ট, মেটা ডাটা এবং Perplexity ও Google AI Overviews-এর উপযোগী FAQPage Schema জেনারেট করে।</div>
        <div class="tool-benefit">💡 <strong>উপকারিতা:</strong> গুগল এআই সার্চে সরাসরি উত্তর হিসেবে সাইট ফিচার্ড হয় এবং গুগল অ্যাডসেন্স ও অ্যাফিলিয়েট ইনকাম বাড়ে।</div>
    </div>

    <!-- MODULE 10 -->
    <div class="tool-card">
        <div class="tool-title">10. 🔴🟢 Google Index Audit (ইনডেক্সিং অডিট)</div>
        <div class="tool-work"><strong>কী কাজ করে:</strong> সাইটম্যাপ অটো-স্ক্রোল করে গুগলে কোন কোন পেজ ইনডেক্স হয়েছে এবং কোনটা হয়নি (Non-indexed) তা অডিট করে।</div>
        <div class="tool-benefit">💡 <strong>উপকারিতা:</strong> ইনডেক্স না হওয়া পেজগুলো দ্রুত গুগলে ইনডেক্স করানোর ৫ ধাপের টেকনিক্যাল অ্যাকশন প্ল্যান পাওয়া যায়।</div>
    </div>

    <!-- MODULE 11 -->
    <div class="tool-card">
        <div class="tool-title">11. 📱 Social Media Viral Content Analyzer (সোশাল মিডিয়া অ্যাডস)</div>
        <div class="tool-work"><strong>কী কাজ করে:</strong> ফেসবুক রিলস, টিকটক ও ইউটিউব শর্টসের জন্য ভাইরাল ভিডিও হুক, প্রমোশনাল স্ক্রিপ্ট এবং হাই-কনভার্টিং অ্যাড কপি জেনারেট করে।</div>
        <div class="tool-benefit">💡 <strong>উপকারিতা:</strong> সোশাল মিডিয়ায় কম খরচে ভাইরাল রিচ ও হাই-কনভার্টিং সেলস অ্যাডস চালানো সম্ভব হয়।</div>
    </div>

    <!-- MODULE 12 -->
    <div class="tool-card">
        <div class="tool-title">12. 🌐 Global & Industrial Market Trends (গ্লোবাল মার্কেট রিসার্চ)</div>
        <div class="tool-work"><strong>কী কাজ করে:</strong> IT, Computer, Networking, Printing, SOHO, Industrial Machinery ইত্যাদির বিশ্বব্যাপী ও স্থানীয় চাহিদা ট্রেন্ড দেখা যায়।</div>
        <div class="tool-benefit">💡 <strong>উপকারিতা:</strong> নতুন কোনো প্রোডাক্ট বাজারে আনার আগেই তার লাভজনকতা ও চাহিদা নিশ্চিত হওয়া যায়।</div>
    </div>

    <!-- MODULE 13 -->
    <div class="tool-card">
        <div class="tool-title">13. 📡 24/7 Agent Activity Stream (লাইভ অ্যাক্টিভিটি লগার)</div>
        <div class="tool-work"><strong>কী কাজ করে:</strong> সিস্টেমে কখন কোন অডিট চালানো হয়েছে তার টাইমস্ট্যাম্প সহ রিয়েল-টাইম লগ ট্র্যাক করে।</div>
        <div class="tool-benefit">💡 <strong>উপকারিতা:</strong> সম্পূর্ণ টিমের কাজের স্বচ্ছতা নিশ্চিত হয়।</div>
    </div>

    <!-- MODULE 14 -->
    <div class="tool-card">
        <div class="tool-title">14. 💳 Multi-Tenant SaaS Subscriptions (বিজনেস মোনেটাইজেশন)</div>
        <div class="tool-work"><strong>কী কাজ করে:</strong> মাস্টার অ্যাডমিন, পেড ইউজার ও ডেমো রোল সেটআপ সহ কমপ্লিট SaaS সিকিউরিটি সিস্টেম।</div>
        <div class="tool-benefit">💡 <strong>উপকারিতা:</strong> আপনি এই সফটওয়্যারটি অন্যদের কাছে মাসিক সাবস্ক্রিপশন ফি দিয়ে বিক্রি করে বিজনেস হিসেবে পরিচালনা করতে পারবেন।</div>
    </div>

    <div class="footer">
        <strong>আব্দুল্লাহ আল নাছের</strong> (Founder & AI Systems Architect) | মোবাইল / হোয়াটসঅ্যাপ: <strong>+8801678684141</strong>
    </div>

</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_proj_path}",
        html_path
    ]

    subprocess.run(cmd, check=True)
    time.sleep(1)

    shutil.copy(pdf_proj_path, pdf_scratch_path)
    print(f"✅ Updated 14-Module Bangla PDF generated at: {pdf_proj_path}")

if __name__ == "__main__":
    generate_perfect_bangla_pdf()
