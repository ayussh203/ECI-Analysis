from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

# The most difficult thing I have ever worked on!
#Government makes weird sites...

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
options = webdriver.FirefoxOptions()
options.add_argument(f"user-agent={user_agent}")

driver = webdriver.Firefox(options=options)
url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"
driver.get(url)
wait = WebDriverWait(driver, 10)

#Get dropdown for length
dropdown = wait.until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_Result1_ddlState')))
select = Select(dropdown)
options = select.options

for i in range(1, len(options)):
    #Repeated fetching of dropdown to avoid staleElement exception
    dropdown = wait.until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_Result1_ddlState')))
    select = Select(dropdown)
    option = select.options[i]
    state_value = option.get_attribute('value')
    state_name = option.text.strip()
    print("Checkpoint 0/3")
    #Skip the placeholder: doesnt have state_value
    if state_value == "":
        continue

    state_dir = os.path.join('../All_Data/Scraped/State-Wise Results', state_name)
    if not os.path.exists(state_dir):
        os.makedirs(state_dir)
        print(f"Directory created for {state_name}")

    #Re-fetch the dropdown and re-create the Select object to avoid stale element exception
    dropdown = wait.until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_Result1_ddlState')))
    select = Select(dropdown)
    select.select_by_value(state_value)
    print(f"Scraping data for {state_name}")

    time.sleep(4)

    table = wait.until(EC.presence_of_element_located((By.XPATH, '//table[@class="table"]')))
    print("State Table found!!")
    headers = [th.text.strip() for th in table.find_elements(By.XPATH, './/thead/tr/th')]
    all_rows = []
    buttons = []

    for tr in table.find_elements(By.XPATH, './/tbody/tr'):
        columns = tr.find_elements(By.TAG_NAME, 'td')
        if len(columns) > 0 and 'Total' not in columns[0].text:  #To avoid footer
            row = [col.text.strip() for col in columns]
            all_rows.append(row)
            buttons.append(tr.find_element(By.TAG_NAME, 'a'))
    '''
No need to make state summary csv. If required: uncomment
    '''
    df = pd.DataFrame(all_rows, columns=headers)
    #state_csv_path = os.path.join(state_dir, f'{state_name}_results.csv')
    #df.to_csv(state_csv_path, index=False)
    #print(f"Data for {state_name} has been saved to '{state_csv_path}'.")

    for i in range(len(buttons)):                
        try:
            table = wait.until(EC.presence_of_element_located((By.XPATH, '//table[@class="table"]')))
            print("State table found inside Loop")

            buttons.clear()
            for tr in table.find_elements(By.XPATH, './/tbody/tr'):
                columns = tr.find_elements(By.TAG_NAME, 'td')
                if len(columns) > 0 and 'Total' not in columns[0].text:
                    row = [col.text.strip() for col in columns]
                    buttons.append(tr.find_element(By.TAG_NAME, 'a'))

            button = buttons[i]
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)
            button.click()
            time.sleep(3)  

            new_table = wait.until(EC.presence_of_element_located((By.XPATH, '//table[@class="table table-striped table-bordered"]')))
            print("Inner table found!!")

            new_headers = [th.text.strip() for th in new_table.find_elements(By.XPATH, './/thead/tr/th')]

            new_rows = []

            for tr in new_table.find_elements(By.XPATH, './/tbody/tr'):
                columns = tr.find_elements(By.TAG_NAME, 'td')
                if len(columns) > 0 and 'Total' not in columns[0].text:  # To avoid footer
                    row = [col.text.strip() for col in columns]
                    new_rows.append(row)

            party_name = df.iloc[i, df.columns.get_loc('Party')]  
            party_csv_path = os.path.join(state_dir, f'{party_name}_details.csv')
            new_df = pd.DataFrame(new_rows, columns=new_headers)
            new_df.to_csv(party_csv_path, index=False)
            print(f"Data for {party_name} in {state_name} has been saved to '{party_csv_path}'.")

            driver.back()
            time.sleep(8)

        except Exception as e:
            print(f"Failed to scrape data for {state_name} - {party_name}. Error: {e}") #Hope I never get this

    driver.back()
    time.sleep(5)
    print("Checkpost 1...")
    dropdown = wait.until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_Result1_ddlState')))
    print("Checkpoint 2...")
    select = Select(dropdown)
    options = select.options

driver.quit()
print("All data has been successfully scraped.")
