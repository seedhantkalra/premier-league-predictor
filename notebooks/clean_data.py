# clean_data.py

import pandas as pd
import os

# Load the full dataset
df = pd.read_csv("data/all_seasons_combined.csv")

# ✅ 1. Drop 'date' and 'source_file'
df.drop(columns=["date", "source_file"], inplace=True, errors='ignore')

# ✅ 2. Convert odds to float
for col in ["h_odd", "d_odd", "a_odd"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ✅ 3. Extract starting year of season
df['season'] = df['season'].str[:4]

# ✅ 4. Split match_name
df[['home_team', 'away_team']] = df['match_name'].str.split(" vs ", expand=True)

# ✅ 5. Split result into home/away score
df[['home_score', 'away_score']] = df['result'].str.split("-", expand=True).astype("Int64")

# ✅ 6. Determine winner
def get_winner(row):
    if pd.isnull(row['home_score']) or pd.isnull(row['away_score']):
        return "UNKNOWN"
    elif row['home_score'] > row['away_score']:
        return "HOME_TEAM"
    elif row['home_score'] < row['away_score']:
        return "AWAY_TEAM"
    else:
        return "DRAW"

df['winner'] = df.apply(get_winner, axis=1)

# ✅ 7. Save cleaned version
df.to_csv("data/all_seasons_cleaned.csv", index=False)
print("✅ Cleaned dataset saved as: data/all_seasons_cleaned.csv")
