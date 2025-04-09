# scraper/website_scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_website_and_linkedin(website_url, linkedin_url=None):
    text = ""

    def extract_text(url):
        try:
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            for script in soup(["script", "style", "noscript"]):
                script.decompose()
            return soup.get_text(separator=" ", strip=True)
        except:
            return ""

    text += extract_text(website_url)

    if linkedin_url:
        text += "\n\n" + extract_text(linkedin_url)

    return text.strip()
