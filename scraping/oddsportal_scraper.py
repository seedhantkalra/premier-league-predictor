# scraping/oddsportal_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Convert American odds to decimal (if needed in future)
def american_to_decimal(odd_str):
    try:
        odd_str = odd_str.strip()
        if not odd_str or odd_str in ['-', '']:
            return None
        if odd_str.startswith('+'):
            return round(1 + int(odd_str[1:]) / 100, 2)
        else:
            return round(1 + 100 / abs(int(odd_str)), 2)
    except:
        return None

# Set up Chrome driver
def init_driver():
    options = Options()
    # Uncomment if you want headless scraping
    # options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(options=options)

def scrape_first_page(season):
    url = f"https://www.oddsportal.com/soccer/england/premier-league-{season}/results/"
    driver = init_driver()
    driver.get(url)

    print("✅ Please accept cookies if prompted...")

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.border-black-borders.border-b.border-l.border-r"))
        )
    except:
        print("❌ Match containers not found.")
        driver.quit()
        return pd.DataFrame()

    time.sleep(5)

    match_blocks = driver.find_elements(By.CSS_SELECTOR, "div.border-black-borders.border-b.border-l.border-r")
    print(f"🔍 Found {len(match_blocks)} match blocks")

    data = []
    current_date = "Unknown"

    for block in match_blocks:
        try:
            # Get team names
            team_tags = block.find_elements(By.CSS_SELECTOR, "p.participant-name")
            if len(team_tags) != 2:
                print("❌ Skipping: Could not find both team names")
                continue
            home_team = team_tags[0].text.strip()
            away_team = team_tags[1].text.strip()

            # Get result
            result_el = block.find_element(By.CSS_SELECTOR, "div.text-gray-dark.relative.flex")
            result = result_el.text.strip().replace('\n', '').replace('–', '-')

            # Get odds (first 3 p tags with .height-content)
            odds_els = block.find_elements(By.CSS_SELECTOR, "p.height-content")
            if len(odds_els) < 3:
                print(f"❌ Skipping {home_team} vs {away_team}: Not enough odds")
                continue
            h_odd = float(odds_els[0].text.strip())
            d_odd = float(odds_els[1].text.strip())
            a_odd = float(odds_els[2].text.strip())

            print(f"✅ Parsed: {home_team} vs {away_team} | {result} | Odds: {h_odd}, {d_odd}, {a_odd}")

            data.append({
                "season": season.replace("-", "/"),
                "date": current_date,
                "match_name": f"{home_team} vs {away_team}",
                "result": result,
                "h_odd": h_odd,
                "d_odd": d_odd,
                "a_odd": a_odd
            })

        except Exception as e:
            print(f"❌ Error parsing match: {e}")
            continue

    driver.quit()
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = scrape_first_page("2020-2021")
    print("\n📄 Final DataFrame Preview:")
    print(df.head())
    df.to_csv("data/2020-2021_page1.csv", index=False)
