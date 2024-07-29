from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

#Per state csv file created
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
options = webdriver.FirefoxOptions()
options.add_argument(f"user-agent={user_agent}")

driver = webdriver.Firefox(options=options)

url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"
driver.get(url)

wait = WebDriverWait(driver, 10)
dropdown = wait.until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_Result1_ddlState')))
select = Select(dropdown)
options = select.options

output_directory = "../All_Data/Scraped/state_results"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for i in range(1, len(options)):  # Skip placeholder
    dropdown = wait.until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_Result1_ddlState')))
    select = Select(dropdown)
    option = select.options[i]
    state_value = option.get_attribute('value')
    state_name = option.text.strip()

    select.select_by_value(state_value)
    print(f"Scraping data for {state_name}")

    time.sleep(5)  

    table = wait.until(EC.presence_of_element_located((By.XPATH, '//table[@class="table"]')))
    print("Table found!!")

    headers = [th.text.strip() for th in table.find_elements(By.XPATH, './/thead/tr/th')]

    all_rows = []
    for tr in table.find_elements(By.XPATH, './/tbody/tr'):
        columns = tr.find_elements(By.TAG_NAME, 'td')
        if len(columns) > 0:  # To avoid footer
            row = [col.text.strip() for col in columns]
            all_rows.append(row)
            print("Table making ....")

    df = pd.DataFrame(all_rows, columns=headers)

    csv_filename = os.path.join(output_directory, f'{state_name}_election_results.csv')
    df.to_csv(csv_filename, index=False)
    print(f"Data has been successfully scraped and saved to '{csv_filename}'.")

    driver.back()
    dropdown = wait.until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_Result1_ddlState')))


driver.quit()

print("All state election results have been successfully scraped and saved.")
