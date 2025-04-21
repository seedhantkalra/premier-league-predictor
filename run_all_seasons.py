# run_all_seasons.py

import os
from scraping.oddsportal_scraper import scrape_all_pages

# Ensure the output folder exists
os.makedirs("data", exist_ok=True)

# Generate season strings like "2004-2005", "2005-2006", ..., "2023-2024", "2024-2025"
def generate_seasons(start=2004, end=2024):
    seasons = []
    for year in range(start, end):
        seasons.append(f"{year}-{year+1}")
    seasons.append("2024-2025")
    return seasons

if __name__ == "__main__":
    all_seasons = generate_seasons()

    for season in all_seasons:
        print(f"\nStarting scrape for season {season}...")
        try:
            df = scrape_all_pages(season)
            filename = f"data/{season}_full.csv"
            df.to_csv(filename, index=False)
            print(f"Completed and saved: {filename} with {len(df)} matches")
        except Exception as e:
            print(f"Failed to scrape {season}: {e}")
