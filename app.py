import re
import streamlit as st
from analyzer import fetch_article_text, extract_claims, skeptical_analysis

# ------------------ Page Config ------------------
st.set_page_config(page_title="Skeptical News Analyzer 📰", layout="wide")

# ------------------ Custom CSS -------------------
st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .stButton button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        font-weight: bold;
    }
    .stButton button:hover { background-color: #ff1a1a; }
    .title-text { font-size: 2.5rem; text-align: center; font-weight: bold; color: #222; }
    .subtitle-text { font-size: 1.2rem; text-align: center; color: #555; margin-bottom: 1rem; }
    .card {
        padding: 20px;
        border-radius: 15px;
        color: white;
        font-weight: bold;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    .bias-card { background-color: #ff4b4b; }
    .tone-card { background-color: #4b7fff; }
    .claims-card { background-color: #2ecc71; }
    </style>
""", unsafe_allow_html=True)

# ------------------ Sidebar ------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2965/2965879.png", width=100)
    st.markdown("## About")
    st.write("Analyze online news for tone, claims, and bias using AI.")
    st.write("Powered by **Groq AI** and NLP magic.")
    st.markdown("---")
    st.write("💡 *Tip:* Use credible sources for best results.")

# ------------------ Session State for Saved Articles ------------------
if "saved_urls" not in st.session_state:
    st.session_state.saved_urls = []

# ------------------ Main Title ------------------
st.markdown('<div class="title-text">📰 Skeptical News Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Paste a news article URL below and let AI find biases & tone</div>', unsafe_allow_html=True)

# ------------------ Input ------------------
url = st.text_input("🔗 Enter Article URL", placeholder="https://example.com/article")
analyze_button = st.button("🚀 Analyze Article")

# ------------------ Processing ------------------
if analyze_button and url:
    with st.spinner("⏳ Fetching and analyzing article..."):
        title, content = fetch_article_text(url)

        if not content:
            st.error("❌ Could not fetch the article content. Try another URL.")
        else:
            # Save URL to session state
            if url not in st.session_state.saved_urls:
                st.session_state.saved_urls.append(url)

            # Extract claims
            claims = extract_claims(title, content)

            # Run skeptical analysis
            report_md = skeptical_analysis(title, claims)

            # -------- Extract Bias, Tone, and Claims Dynamically --------
            bias_match = re.search(r"(?i)Bias\s*:\s*(.+)", report_md)
            tone_match = re.search(r"(?i)Tone\s*:\s*(.+)", report_md)
            claims_count = len(claims)

            bias_value = bias_match.group(1).strip() if bias_match else "Not Found"
            tone_value = tone_match.group(1).strip() if tone_match else "Not Found"

            # ------------------ Dashboard ------------------
            st.success("✅ Analysis Complete!")
            st.markdown(f"### 📌 Title: {title}")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f'<div class="card bias-card">🧐 Bias Level<br><span style="font-size:1.5rem;">{bias_value}</span></div>', unsafe_allow_html=True)

            with col2:
                st.markdown(f'<div class="card tone-card">🎭 Tone<br><span style="font-size:1.5rem;">{tone_value}</span></div>', unsafe_allow_html=True)

            with col3:
                st.markdown(f'<div class="card claims-card">📢 Claims Found<br><span style="font-size:1.5rem;">{claims_count}</span></div>', unsafe_allow_html=True)

            # ------------------ Detailed Report ------------------
            st.markdown("### 📊 AI Report")
            with st.expander("📄 Full Analysis", expanded=True):
                st.markdown(report_md)

            with st.expander("🧠 Summary & Insights"):
                st.markdown("""
                - Key claims identified
                - Possible bias sources
                - Tone & sentiment detected
                """)




