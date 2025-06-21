import streamlit as st
import pandas as pd
import numpy as np
from model.regression import RegressionPricingModel
from scraper.competitor_scraper import CompetitorPriceScraper

st.set_page_config(page_title="Dynamic Pricing Engine", layout="wide")
st.title("💸 Dynamic Pricing Engine")
st.markdown("""
This app suggests the best price for a product based on demand, time, and competitors.\
Upload your data or use the sample below to get started.
""")

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Run Pricing Engine", "About"])

if page == "About":
    st.header("About")
    st.write("""
    - **Business Value:** Maximizes revenue and competitiveness.
    - **Model Type:** Regression (Linear Regression).\
    - **Add-on:** Scrapes real competitor prices (demo only).
    """)
    st.stop()

# Sample data
sample_data = pd.DataFrame({
    'demand': [100, 150, 200, 250, 300],
    'time': [1, 2, 3, 4, 5],
    'competitor_price': [10, 12, 11, 13, 12],
    'actual_price': [11, 13, 12, 14, 13]
})

st.subheader("1. Upload Your Data or Use Sample")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Data uploaded successfully!")
else:
    df = sample_data
    st.info("Using sample data. Upload your own for real use.")

st.dataframe(df)

st.subheader("2. (Optional) Scrape Competitor Prices")
urls = st.text_area("Enter competitor product URLs (one per line)")
if st.button("Scrape Competitor Prices"):
    url_list = [u.strip() for u in urls.splitlines() if u.strip()]
    if url_list:
        scraper = CompetitorPriceScraper(url_list)
        prices = scraper.scrape_prices()
        st.write(prices)
    else:
        st.warning("Please enter at least one URL.")

st.subheader("3. Run Pricing Model")
if st.button("Suggest Prices"):
    if {'demand', 'time', 'competitor_price', 'actual_price'}.issubset(df.columns):
        X = df[['demand', 'time', 'competitor_price']]
        y = df['actual_price']
        model = RegressionPricingModel()
        model.train(X, y)
        suggested = model.predict(X)
        df['suggested_price'] = np.round(suggested, 2)
        st.success("Suggested prices calculated!")
        st.dataframe(df)
        st.download_button("Download Results as CSV", df.to_csv(index=False), "suggested_prices.csv")
    else:
        st.error("Data must include columns: demand, time, competitor_price, actual_price.")

st.markdown("---")
st.caption("© 2025 Dynamic Pricing Engine. Built with Streamlit.")
