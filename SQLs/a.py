import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import base64
import os

st.set_page_config(page_title="📊 Data Profiler", layout="wide")
st.title("🧠 CSV Data Profiler App")

# --- Helper to load and parse the CSV with smart date detection ---
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)

    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                sample = df[col].dropna().iloc[0]
                parsed = pd.to_datetime(sample, utc=True)
                if 1900 < parsed.year < 2100:
                    df[col] = pd.to_datetime(df[col], utc=True)
            except Exception as e:
                print(f"🕒 Failed to parse column '{col}' as datetime: {e}")
    return df

# --- Upload CSV ---
uploaded_file = st.file_uploader("📤 Upload your CSV file", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    st.subheader("📋 Generating Profile Report...")
    profile = ProfileReport(df, title="Profiling Report", explorative=True)

    # Show inside Streamlit
    st_profile_report(profile)

    # Export to HTML
    html_path = "profile_report.html"
    profile.to_file(html_path)

    # Make download button
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        b64 = base64.b64encode(html_content.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="profile_report.html">📥 Download HTML Report</a>'
        st.markdown(href, unsafe_allow_html=True)

    # Optional: clean up saved file
    os.remove(html_path)

else:
    st.info("👆 Upload a CSV file to get started.")
