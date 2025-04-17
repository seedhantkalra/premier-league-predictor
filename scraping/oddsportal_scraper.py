# scraping/oddsportal_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up Selenium WebDriver
def init_driver():
    options = Options()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    return driver

# Scrape one season (first page only for now)
def scrape_season(season):
    url = f"https://www.oddsportal.com/soccer/england/premier-league-{season}/results/"
    driver = init_driver()
    driver.get(url)
    time.sleep(5)  # Let page load

    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()

    # Extract match rows
    rows = soup.select('table > tbody > tr')
    
    data = []
    current_date = None

    for row in rows:
        cols = row.find_all('td')
        if not cols:
            continue

        if 'center' in row.get('class', []):
            # New date row
            current_date = row.get_text(strip=True)
            continue

        try:
            match_name = cols[0].get_text(strip=True)
            result = cols[1].get_text(strip=True)
            h_odd = float(cols[2].text)
            d_odd = float(cols[3].text)
            a_odd = float(cols[4].text)

            data.append({
                'season': season.replace('-', '/'),
                'date': current_date,
                'match_name': match_name,
                'result': result,
                'h_odd': h_odd,
                'd_odd': d_odd,
                'a_odd': a_odd
            })
        except:
            continue

    return pd.DataFrame(data)

# Test it
if __name__ == "__main__":
    df = scrape_season("2020-2021")
    print(df.head())
    df.to_csv("data/2020-2021.csv", index=False)
 