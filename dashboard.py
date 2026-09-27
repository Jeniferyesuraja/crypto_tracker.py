import streamlit as st
from crypto_tracker import scrape_top_coins, save_with_timestamp, filter_coins
import pandas as pd

st.title("💰 Cryptocurrency Price Tracker")
st.write("Top 10 crypto coins oda live data")

if st.button("Fetch Latest Prices"):
    with st.spinner("Fetching data..."):
        data = scrape_top_coins(headless=True)

    if data:
        save_with_timestamp(data)
        df = pd.DataFrame(data, columns=["Name", "Price", "24h Change", "Market Cap"])

        st.success(f"{len(data)} coins fetched successfully!")
        st.table(df)

        st.subheader("Filter Coins")
        min_price = st.number_input("Minimum Price ($)", value=1.0)
        min_gain = st.number_input("Minimum 24h Gain (%)", value=0.0)

        filtered = filter_coins(data, min_price=min_price, min_gain=min_gain)
        filtered_df = pd.DataFrame(filtered, columns=["Name", "Price", "24h Change", "Market Cap"])
        st.write(f"Filtered Coins ({len(filtered)} matched)")
        st.table(filtered_df)
    else:
        st.error("No data fetched. Try again.")

st.subheader("📜 Historical Data")
try:
    history_df = pd.read_csv("crypto_history.csv")
    st.dataframe(history_df)
except FileNotFoundError:
    st.info("No history yet. Click 'Fetch Latest Prices' first.")