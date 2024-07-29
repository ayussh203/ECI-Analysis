import os
import pandas as pd

df = pd.read_csv('../All_Data/Processed/Constituency_Stats.csv')
if 'State' not in df.columns or 'Party' not in df.columns:
    raise ValueError("The CSV file must contain 'State' and 'Party' columns.")
seats_won = df.groupby(['State', 'Party']).size().reset_index(name='Seats_Won')

results = []

for state, group in seats_won.groupby('State'):
    sorted_group = group.sort_values(by='Seats_Won', ascending=False)
    max_seats = sorted_group['Seats_Won'].max()
    
    leading_parties = sorted_group[sorted_group['Seats_Won'] == max_seats]
    
    second_max_seats = sorted_group[sorted_group['Seats_Won'] < max_seats]['Seats_Won'].max()
    second_leading_parties = sorted_group[sorted_group['Seats_Won'] == second_max_seats]
    
    result = {
        'State': state,
        'Leading Party 1': leading_parties.iloc[0]['Party'],
        'Leading Seats Won 1': max_seats
    }
    
    for idx, party in enumerate(leading_parties['Party'][1:], start=2):
        result[f'Leading Party {idx}'] = party
        result[f'Leading Seats Won {idx}'] = max_seats
    
    result['Second Leading Party 1'] = second_leading_parties.iloc[0]['Party'] if not second_leading_parties.empty else ''
    result['Second Leading Seats Won 1'] = second_max_seats if not second_leading_parties.empty else ''
    
    for idx, party in enumerate(second_leading_parties['Party'][1:], start=2):
        result[f'Second Leading Party {idx}'] = party
        result[f'Second Leading Seats Won {idx}'] = second_max_seats
    
    results.append(result)

results_df = pd.DataFrame(results)

#Fill NaN values with empty strings
results_df = results_df.fillna('')
results_df.to_csv('../All_Data/Processed/Top2_Analysis.csv', index=False)
print("Processed data saved to '../All_Data/Processed/Top2_Analysis.csv'.")
