import pandas as pd

df = pd.read_csv('../All_Data\Processed\Constituency_Stats.csv')

if 'State' not in df.columns or 'Party' not in df.columns:
    raise ValueError("The CSV file must contain 'State' and 'Party' columns.")

seats_won = df.groupby(['State', 'Party']).size().reset_index(name='Seats_Won')
leading_parties = seats_won.loc[seats_won.groupby('State')['Seats_Won'].idxmax()]
leading_parties.rename(columns={'Party': 'Leading Party'}, inplace=True)

leading_parties.to_csv('../All_Data/Processed/leading_parties.csv', index=False)

print("Processed data saved to '../All_Data/Processed/leading_parties.csv'.")
