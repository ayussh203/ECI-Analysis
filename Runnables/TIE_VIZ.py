import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

shapefile_path = '../India_Shapefile/India_State_Boundary.shp'
gdf = gpd.read_file(shapefile_path) #Indian States map shapefile
leading_parties = pd.read_csv('../All_Data/Processed/Top2_Analysis.csv')

expected_columns = ['State', 'Leading Party 1', 'Leading Party 2']
if not all(column in leading_parties.columns for column in expected_columns):
    raise ValueError(f"CSV file must contain the columns: {expected_columns}")

def check_tie(row):
    leading_parties = [row['Leading Party 1'], row['Leading Party 2']]
    return 'Bharatiya Janata Party - BJP' in leading_parties and 'Indian National Congress - INC' in leading_parties

leading_parties['Tie'] = leading_parties.apply(check_tie, axis=1)

tie_states = leading_parties[leading_parties['Tie'] == True]['State']
gdf['Tie'] = gdf['State_Name'].apply(lambda x: x in tie_states.values)

fig, ax = plt.subplots(1, 1, figsize=(15, 15))
gdf.boundary.plot(ax=ax, linewidth=1)
gdf[gdf['Tie'] == True].plot(ax=ax, color='red', legend=True)



ax.set_title('States with Tie between BJP and INC', fontsize=15)
ax.set_axis_off()
import matplotlib.patches as mpatches
tie_patch = mpatches.Patch(color='orange', label='Tie between BJP and INC')
plt.legend(handles=[tie_patch])
plt.savefig('../BJP_INC_TIE.png')
#plt.show()
