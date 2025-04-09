import streamlit as st
import json
from scraper.website_scraper import scrape_website_and_linkedin
from llm.enrich import enrich_company_features, extract_revenue_estimate
import pandas as pd
import io

st.set_page_config(page_title="Caprae Capital Partners — Lead Enricher", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;600;800&display=swap');

        .stApp {
            background-color: #0a0a0a;
            font-family: 'Work Sans', sans-serif;
            color: #f7c948;
        }

        h1, h2, h3 {
            color: #f7c948;
        }

        .main-title {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
            text-align: center;
        }

        .subtitle {
            font-size: 1rem;
            color: #ccc;
            text-align: center;
            margin-bottom: 2rem;
        }

        .json-container {
            border: 1px solid #333;
            border-radius: 12px;
            padding: 1rem;
            background-color: #1a1a1a;
            margin-top: 1rem;
        }

        button[kind="primary"] {
            background-color: #f7c948 !important;
            color: #000 !important;
            border: none !important;
            transition: all 0.3s ease;
            border-radius: 8px;
        }

        button[kind="primary"]:hover {
            background-color: #f9d75e !important;
            transform: scale(1.02);
        }

        .download-button {
            background-color: #1a1a1a;
            border: 1px solid #f7c948;
            color: #f7c948;
            padding: 0.5rem 1rem;
            margin-top: 1rem;
            border-radius: 8px;
            text-align: center;
            display: inline-block;
            text-decoration: none;
        }

        .download-button:hover {
            background-color: #f7c948;
            color: #000;
        }
    </style>
""", unsafe_allow_html=True)

# Title + Logo
st.markdown('<div class="main-title">Caprae Capital Partners — Lead Enricher</div>', unsafe_allow_html=True)
st.image("assets/caprae_logo.png", width=100)
st.markdown('<div class="subtitle">Great founders working with great founders. Enrich company data aligned with Caprae\'s investment lens.</div>', unsafe_allow_html=True)
st.markdown("---")

# Inputs
website_url = st.text_input("🌐 Company Website", placeholder="https://www.example.com")
linkedin_url = st.text_input("🔗 LinkedIn URL (optional)", placeholder="https://www.linkedin.com/company/example")

# Enrichment Logic
if st.button("✨ Enrich Company Info"):
    if not website_url:
        st.error("❗ Company website is required.")
    else:
        with st.spinner("🔎 Scraping content..."):
            full_text = scrape_website_and_linkedin(website_url, linkedin_url)

        if not full_text.strip():
            st.error("⚠️ Failed to retrieve content from the provided URLs.")
        else:
            with st.spinner("🤖 Enriching company info..."):
                enrichment = enrich_company_features(full_text)

            with st.spinner("📈 Estimating revenue..."):
                revenue_info = extract_revenue_estimate(full_text)

            enrichment["revenue_growth"] = revenue_info

            st.success("✅ Enrichment Complete")
            st.subheader("📊 Enriched Company Summary")
            st.markdown('<div class="json-container">', unsafe_allow_html=True)
            st.json(enrichment)
            st.markdown('</div>', unsafe_allow_html=True)

            # JSON Download
            json_str = json.dumps(enrichment, indent=2)
            st.download_button(
                label="⬇️ Download Enriched JSON",
                data=json_str,
                file_name="enriched_company.json",
                mime="application/json"
            )

            # CSV logic (inside the button block)
            def flatten_enrichment_to_csv(enrichment):
                flat = {
                    "Fit with Caprae Thesis": enrichment.get("fit_with_caprae_thesis", False),
                    "Founder Name": enrichment.get("founder_exec", {}).get("name", ""),
                    "Founder Title": enrichment.get("founder_exec", {}).get("title", ""),
                    "Executive Email": enrichment.get("executive_email", ""),
                    "Business Model / Industry": enrichment.get("business_model_industry", {}).get("value", ""),
                    "Business Model Confidence": enrichment.get("business_model_industry", {}).get("confidence", ""),
                    "Funding Stage": enrichment.get("funding_stage", {}).get("value", ""),
                    "Funding Confidence": enrichment.get("funding_stage", {}).get("confidence", ""),
                    "Revenue Estimate": enrichment.get("revenue_growth", {}).get("value", ""),
                    "Revenue Confidence": enrichment.get("revenue_growth", {}).get("confidence", "")
                }

                for i, insight in enumerate(enrichment.get("additional_insights", [])):
                    flat[f"Insight {i+1}"] = insight.get("value", "")
                    flat[f"Insight {i+1} Confidence"] = insight.get("confidence", "")

                competitors = enrichment.get("competitors", [])
                for i, comp in enumerate(competitors):
                    flat[f"Competitor {i+1}"] = comp

                return flat

            csv_data = flatten_enrichment_to_csv(enrichment)
            df = pd.DataFrame([csv_data])
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_bytes = csv_buffer.getvalue().encode('utf-8')

            st.download_button(
                label="📥 Export as CSV",
                data=csv_bytes,
                file_name="enriched_company.csv",
                mime="text/csv"
            )
