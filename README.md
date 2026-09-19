# SEO & Competitor Intelligence AI Agent

A powerful, automated AI Agent system built with Python and Gemini LLM to track competitor rankings on Google and automatically generate high-ranking, AEO (Answer Engine Optimization) & GEO (Generative Engine Optimization) friendly content.

## 🌟 Key Features

1. **Competitor SERP Intelligence**: Tracks top-ranking competitor products, URLs, domains, and keywords on Google.
2. **AEO & GEO Content Generator**: Produces complete articles with:
   - **SEO Metadata**: Optimized Title, Meta Description, Primary & LSI Keywords, URL Slug.
   - **AI Search Direct Answers**: Concise summary blocks tuned for Google AI Overviews, Perplexity, and ChatGPT.
   - **H1, H2, H3 Heading Hierarchy**: Full structured long-form content.
   - **AEO FAQ & JSON-LD Schema**: Ready-to-use Schema markup for direct Google rich snippet indexing.
3. **360° SEO Strategy Output**:
   - **On-Page SEO**: Keyword density advice, internal link strategy, ALT text suggestions.
   - **Technical SEO**: Schema recommendations, Core Web Vitals targets.
   - **Off-Page SEO**: Backlink outreach angles & link-building opportunities.
4. **Daily Automation & Scheduler**: Run background scans daily at 08:00 AM to generate updated reports automatically.

---

## 🚀 Quick Start Guide

### 1. Installation & Setup

Navigate to the project directory and install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configuration (`.env` or `config.py`)

Create a `.env` file or update `config.py` with your API keys:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
TAVILY_API_KEY=your_tavily_search_api_key_here
```

### 3. Usage Modes

#### A. Interactive CLI Menu
Run the interactive CLI:
```bash
python app.py
```

#### B. Quick Single Keyword Command
Generate a report directly for any keyword or product:
```bash
python app.py "best wireless mechanical keyboard"
```

#### C. Run Daily Background Automation
Start the daily automated competitor tracker and report generator:
```bash
python daily_scheduler.py
```

---

## 📁 Output Directory

All generated articles and daily summaries are automatically saved inside `./reports/` in markdown format (`.md`).
