import pandas as pd

df = pd.read_csv('../All_Data/Processed/Constituency_Stats.csv')
df['Margin'] = pd.to_numeric(df['Margin'], errors='coerce')
highest_margin_row = df.loc[df['Margin'].idxmax()]
lowest_margin_row = df.loc[df['Margin'].idxmin()]

#Display
print("Candidate with the Highest Margin:")
print(f"State: {highest_margin_row['State']}")
print(f"Constituency: {highest_margin_row['Parliament Constituency']}")
print(f"Candidate: {highest_margin_row['Winning Candidate']}")
print(f"Party: {highest_margin_row['Party']}")
print(f"Total Votes: {highest_margin_row['Total Votes']}")
print(f"Margin: {highest_margin_row['Margin']}\n")

print("Candidate with the Lowest Margin:")
print(f"State: {lowest_margin_row['State']}")
print(f"Constituency: {lowest_margin_row['Parliament Constituency']}")
print(f"Candidate: {lowest_margin_row['Winning Candidate']}")
print(f"Party: {lowest_margin_row['Party']}")
print(f"Total Votes: {lowest_margin_row['Total Votes']}")
print(f"Margin: {lowest_margin_row['Margin']}")
