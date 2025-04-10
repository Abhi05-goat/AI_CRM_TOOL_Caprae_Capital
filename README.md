# Caprae Capital Partners — Lead Enricher

🦌 **Great founders working with great founders.**

This internal tool enables Caprae Capital Partners to rapidly enrich and qualify startup leads using AI. It scrapes websites and LinkedIn pages, applies an investment-focused LLM analysis, and outputs structured insight — aligned to Caprae's SaaS thesis.

---

## ✨ Features

- 🕸️ Website + LinkedIn content scraping  
- 🤖 AI enrichment via OpenRouter LLMs  
- 🔍 Key data extracted:  
  - Founder / Executive info  
  - Business model & funding stage (with confidence ratings)  
  - Fit with Caprae's investment lens  
  - Revenue estimate  
  - Additional insights & competitors  
- 📤 Export to JSON or CSV  
- 🎨 Custom UI with Caprae brand styling

---

## 🧠 Powered By

- OpenRouter API (`tokyotech-llm/llama-3.1-swallow-70b-instruct-v0.3`)
- Streamlit frontend  
- BeautifulSoup scraping  
- Custom prompt engineering

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/caprae-lead-enricher.git
cd caprae-lead-enricher
```

### 2. Install dependencies

```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 3. Set your API key

Create a `.env` file:

```
OPENAI_API_KEY=your_openai_key_here
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## 🎥 Demo Video

Check out the full walkthrough here:  
👉 [https://youtu.be/Ya0G8pMd1GM](https://youtu.be/Ya0G8pMd1GM)

---

## 📁 Directory Structure

```
.
├── app.py
├── utils/
│   └── llm_client.py
├── llm/
│   └── enrich.py
├── scraper/
│   └── website_scraper.py
├── assets/
│   └── caprae_logo.png
├── .env
├── requirements.txt
└── README.md
```

---

## 📝 License

Internal use only – Caprae Capital Partners.
