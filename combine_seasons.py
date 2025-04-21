# combine_seasons.py

import pandas as pd
import os
from glob import glob

# Step 1: Point to the folder with all your CSVs
data_folder = "data"
csv_files = sorted(glob(os.path.join(data_folder, "*_full.csv")))

# Step 2: Combine all CSVs
all_data = []
for file in csv_files:
    df = pd.read_csv(file)
    df['source_file'] = os.path.basename(file)  # optional: track file of origin
    all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)

# Step 3: Save the combined file
combined_df.to_csv("data/all_seasons_combined.csv", index=False)

# Step 4: Show basic info
print(f"✅ Combined {len(csv_files)} files")
print(f"📊 Total matches: {len(combined_df)}")
print("📄 Saved as: data/all_seasons_combined.csv")
