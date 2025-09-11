import pandas as pd
import sys

# Read the CSV file
df = pd.read_csv("data/tdm-20250911-geocoded.csv")

# Drop columns where all values are NaN or empty
cleaned_df = df.dropna(axis=1, how='all')
cleaned_df = cleaned_df.loc[:, ~(cleaned_df == '').all()]

# Replace commas in cell values with semicolons
for col in cleaned_df.columns:
	cleaned_df[col] = cleaned_df[col].apply(lambda x: str(x).replace(',', ';') if isinstance(x, str) and ',' in str(x) else x)

# Save the cleaned CSV
cleaned_df.to_csv("data/tdm-20250911-geocoded-cleaned.csv", index=False)
print(f"Saved cleaned CSV to data/tdm-20250911-geocoded-cleaned.csv")
