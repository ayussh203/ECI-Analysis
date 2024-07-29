import os
import pandas as pd

base_dir = '../All_Data\Scraped\State-Wise Results'
data_list = []

for state in os.listdir(base_dir):
    state_dir = os.path.join(base_dir, state)
    if os.path.isdir(state_dir):
        for file in os.listdir(state_dir):
            if file.endswith('_details.csv'):
                file_path = os.path.join(state_dir, file)
                df = pd.read_csv(file_path)
                if 'S.No' in df.columns:
                    df.drop(columns=['S.No'], inplace=True)
                party_name = file.replace('_details.csv', '')
                df['State'] = state
                df['Party'] = party_name
                data_list.append(df)

combined_df = pd.concat(data_list, ignore_index=True)

combined_df.insert(0, 'S.No.', range(1, len(combined_df) + 1))
output_file = '../All_Data/Processed/Constituency_Stats.csv'
combined_df.to_csv(output_file, index=False)

print(f"Combined data with party names has been saved to '{output_file}'")
