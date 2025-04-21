from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


# Convert American odds to decimal (for future use)
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
    # options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(options=options)


# Scroll to load all matches on the current page
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(0.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    time.sleep(2)


# Extract all match data from the current page
def parse_page_matches(driver, season):
    scroll_to_bottom(driver)

    match_blocks = driver.find_elements(By.CSS_SELECTOR, "div.border-black-borders.border-b.border-l.border-r")
    print(f"🔍 Found {len(match_blocks)} match blocks")

    data = []
    current_date = "Unknown"

    for block in match_blocks:
        try:
            # Get team names
            team_tags = block.find_elements(By.CSS_SELECTOR, "p.participant-name")
            if len(team_tags) != 2:
                continue
            home_team = team_tags[0].text.strip()
            away_team = team_tags[1].text.strip()

            # Get result
            result_el = block.find_element(By.CSS_SELECTOR, "div.text-gray-dark.relative.flex")
            result = result_el.text.strip().replace('\n', '').replace('–', '-')

            # Get odds
            odds_els = block.find_elements(By.CSS_SELECTOR, "p.height-content")
            if len(odds_els) < 3:
                continue
            h_odd = float(odds_els[0].text.strip())
            d_odd = float(odds_els[1].text.strip())
            a_odd = float(odds_els[2].text.strip())

            print(f"Parsed: {home_team} vs {away_team} | {result} | Odds: {h_odd}, {d_odd}, {a_odd}")

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
            print(f"Error parsing match: {e}")
            continue

    return data


# Scrape all result pages for a given season
def scrape_all_pages(season):
    # Handle current season with special URL
    if season == "2024-2025":
        url = "https://www.oddsportal.com/football/england/premier-league/results/"
    else:
        url = f"https://www.oddsportal.com/football/england/premier-league-{season}/results/"

    driver = init_driver()
    driver.get(url)

    print("✅ Please accept cookies if prompted...")
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.border-black-borders.border-b.border-l.border-r"))
        )
    except:
        print(f"❌ No match blocks found for {season}. Skipping.")
        driver.quit()
        return pd.DataFrame()

    time.sleep(4)
    all_data = []
    page = 1

    while True:
        print(f"\n📄 Scraping Page {page}...")
        all_data += parse_page_matches(driver, season)

        try:
            # Scroll near pagination
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)

            next_button = None
            all_links = driver.find_elements(By.CSS_SELECTOR, "a.pagination-link")

            for link in all_links:
                if link.text.strip().lower() == "next":
                    next_button = link
                    break

            if next_button:
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(0.5)
                print("➡️ Clicking 'Next' with JavaScript...")
                driver.execute_script("arguments[0].click();", next_button)
                page += 1
                time.sleep(4)
            else:
                print("❌ No more pages found.")
                break

        except Exception as e:
            print(f"❌ Error clicking next: {e}")
            break

    driver.quit()
    return pd.DataFrame(all_data)

# Run the full scrape
if __name__ == "__main__":
    season = "2020-2021"
    df = scrape_all_pages(season)
    df.to_csv(f"data/{season}_full.csv", index=False)
