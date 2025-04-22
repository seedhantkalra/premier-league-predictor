import pandas as pd

# Load cleaned data from previous step
df = pd.read_csv("data/all_seasons_cleaned.csv")

# ✅ Drop the 'result' column (no longer needed)
df.drop(columns=['result'], inplace=True, errors='ignore')

# ✅ Convert American odds to Decimal odds
def american_to_decimal(odd):
    if pd.isnull(odd):
        return None
    try:
        odd = float(odd)
        if odd > 0:
            return round(1 + odd / 100, 2)
        else:
            return round(1 + 100 / abs(odd), 2)
    except:
        return None

for col in ['h_odd', 'd_odd', 'a_odd']:
    df[col] = df[col].apply(american_to_decimal)

# ✅ Save updated DataFrame
df.to_csv("data/all_seasons_ready.csv", index=False)

print("✅ Cleaned odds and removed result column.")
print("📄 Saved as: data/all_seasons_ready.csv")
