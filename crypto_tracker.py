from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import time


def scrape_top_coins(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get("https://coinmarketcap.com/")
    time.sleep(10)

    coins = []
    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")[:10]

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        try:
            name = cols[2].text.split("\n")[0]
            price = cols[3].text
            change_24h = cols[4].text
            market_cap = cols[7].text
            coins.append([name, price, change_24h, market_cap])
        except Exception:
            continue

    driver.quit()
    return coins


def save_with_timestamp(coins, filename="crypto_history.csv"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame(coins, columns=["Name", "Price", "24h Change", "Market Cap"])
    df["Timestamp"] = timestamp

    try:
        old_df = pd.read_csv(filename)
        df = pd.concat([old_df, df], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_csv(filename, index=False)
    print(f"Saved {len(coins)} coins with timestamp to {filename}")


def filter_coins(coins, min_price=None, min_gain=None):
    filtered = []
    for name, price, change, mcap in coins:
        p = float(price.replace("$", "").replace(",", ""))
        c = float(change.replace("%", "").replace("+", ""))

        if min_price is not None and p < min_price:
            continue
        if min_gain is not None and c < min_gain:
            continue
        filtered.append([name, price, change, mcap])
    return filtered


if __name__ == "__main__":
    print("Fetching top 10 crypto coins...")
    data = scrape_top_coins(headless=False)

    if data:
        save_with_timestamp(data)
        print("Done! Check crypto_history.csv file.")

        filtered = filter_coins(data, min_price=1, min_gain=0)
        print(f"\nFiltered coins ({len(filtered)} matched):")
        for coin in filtered:
            print(coin)
    else:
        print("No data fetched. Website structure maari irukalam.")