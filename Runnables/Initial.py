import requests
from bs4 import BeautifulSoup
import pandas as pd

#First page table of national seats per party
url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('table', class_='table')

headers = []
for th in table.find('thead').find_all('th'):
    headers.append(th.text.strip())

rows = []
for tr in table.find('tbody').find_all('tr'):
    columns = tr.find_all('td')
    if len(columns) > 0: #to avoid footer
        row = [col.text.strip() for col in columns]
        rows.append(row)

df = pd.DataFrame(rows, columns=headers)
df.to_csv('../All_Data/Scraped/election_results.csv', index=False)
print("Data has been successfully scraped and saved to '../All_Data/Scraped/election_results.csv'.")
