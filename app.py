
import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="NSE RSI DATA CENTER",
    page_icon="📈",
    layout="wide"
)

FOLDER = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(FOLDER, "RSI_DASHBOARD.csv")

st.title("📈 NSE RSI DATA CENTER")
st.caption("All NSE Stocks | Daily | Weekly | Monthly RSI Scanner")

if not os.path.exists(FILE):
    st.error("NSE_RSI_OUTPUT.xlsx file পাওয়া যায়নি।")
    st.stop()

@st.cache_data(ttl=300)
def load_data():
    return pd.read_csv(FILE)

df = load_data()

if df.empty:
    st.warning("Dashboard-এ কোনো ডেটা পাওয়া যায়নি।")
    st.stop()

st.success(f"মোট ডাউনলোড হওয়া স্টক: {len(df)}")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Stocks", len(df))

with col2:
    if "BUY CROSS" in df.columns:
        buys = (df["BUY CROSS"] == "BUY CROSS").sum()
        st.metric("BUY CROSS Stocks", int(buys))

st.divider()

search = st.text_input("🔍 Search NSE Stock")

if search:
    df = df[df["SYMBOL"].astype(str).str.contains(
        search, case=False, na=False
    )]

if "BUY CROSS" in df.columns:
    choice = st.selectbox(
        "Scanner Filter",
        ["ALL STOCKS", "BUY CROSS", "NO CROSS"]
    )

    if choice != "ALL STOCKS":
        df = df[df["BUY CROSS"] == choice]

st.subheader("NSE RSI Scanner")

if "TRADINGVIEW" in df.columns:
    df["TRADINGVIEW"] = df["TRADINGVIEW"].astype(str)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "Download Scanner Excel",
    data=df.to_csv(index=False).encode("utf-8-sig"),
    file_name="NSE_RSI_SCANNER.csv",
    mime="text/csv"
)

st.caption("Data source: Your local NSE_RSI_OUTPUT.xlsx file")
st.caption("ডেটা আপডেট করতে nse_rsi.py চালাতে হবে।")
