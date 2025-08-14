import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# ------------------------------
# API Config
# ------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# ------------------------------
# Helper Functions
# ------------------------------
def fetch_article_text(url):
    """Fetch and extract article text from a URL."""
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "Untitled Article"
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
        return title, "\n".join(paragraphs)
    except Exception as e:
        st.error(f"Error fetching article: {e}")
        return None, None

def call_groq_api(prompt):
    """Send a prompt to Groq API and return the response text."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1024
    }
    try:
        resp = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

# ------------------------------
# Analysis Functions
# ------------------------------
def extract_claims(title, content):
    """First pass: Extract structured claims."""
    prompt = f"""
Extract all factual claims from the following news article.
Return them in a numbered list without any additional commentary.

Title: {title}
Content: {content}
"""
    return call_groq_api(prompt)

def skeptical_analysis(title, claims):
    """Second pass: Perform skeptical analysis."""
    prompt = f"""
You are a skeptical fact-checking assistant.
Analyze each claim below for credibility, possible bias, and verification steps.

Title: {title}

Claims:
{claims}

Output in **Markdown** with these sections:
- Core Claims Analysis
- Language & Tone Analysis
- Potential Red Flags
- Verification Questions
- Bias Detection
- Source Suggestions (3+ reputable links)
"""
    return call_groq_api(prompt)

def cross_reference_search(title):
    """Return a Google News search link for the same story."""
    search_url = f"https://news.google.com/rss/search?q={title.replace(' ', '+')}"
    return f"[Click here to search on Google News]({search_url})"

# ------------------------------
# Backward Compatibility Wrapper
# ------------------------------
def analyze_with_groq(title, content):
    """
    Wrapper for backward compatibility with app.py calls.
    Runs two-pass analysis: extract claims -> skeptical analysis.
    """
    claims = extract_claims(title, content)
    if not claims:
        return "No claims could be extracted."
    analysis = skeptical_analysis(title, claims)
    return analysis or "Analysis could not be completed."







