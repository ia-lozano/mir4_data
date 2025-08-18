# pip install selenium
# pip install webdriver_manager
# pip install 'urllib3<2.0'
# pip install pandas

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
import time

# website = 'https://www.xdraco.com/nft/'

def nft_list_extractor(website: str) -> pd.DataFrame:
    '''
        Takes the current url that redirects to the XDraco market place and generates
        a pandas DataFrame.

        Params:
        - website: string containing the current XDraco market place url.

        Output:
        - Pandas DataFrame containing the scraped data.
    '''
    start_time = time.time()
    print('Extracting data, this process may take several minutes.')

    # Setting up chrome driver
    chrome_options = Options()
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(website)
    time.sleep(5)

    # Rendering all the elements to scrape by clicking "view more" button
    while True:
        try:
            view_more = WebDriverWait(driver,30).until(
                EC.presence_of_element_located((By.XPATH, '//button[@class="btn-viewmore"]'))
            )
            view_more.click()
        except:
            print('View more button not found or you scrolled till the bottom')
            break

    # Getting the full container of the characters list and a list with all the characters
    try:
        full_list = driver.find_element(By.XPATH, '//ul[@class="list-item wrap-card"][2]')
        print("list found")
        characters = full_list.find_elements(By.XPATH, './li')
        print("characters found")
    except:
        print('List of character not found, perhaps the site is under maintenance or was updated')

    # List for csv later
    name = []
    char_class = []
    level = []
    power_score = []
    rate = []
    date = []

    # Extracting data for each nft character and creating the DataFrame
    for character in characters:
        try:
            # Getting characters name
            name_string = character.find_element(
                By.XPATH, './a/div/div/div[1]/div[2]/dl[1]/dd[1]').text
            
            name.append(name_string)

            # Getting characters class
            class_string = character.find_element(
                By.XPATH, './a/div/div/div/span').text

            char_class.append(class_string)

            # Getting characters level
            level.append(character.find_element(
                By.XPATH, './a/div/div/div/dl/dd').text)
            
            # Getting characters power score
            power_score.append(int(character.find_element(
                By.XPATH, './a/div/div/div/div[2]/div/dd').text.replace(',', '')))
            
            # Getting rate (wemix)
            rate.append(int(character.find_element(
                By.XPATH, './div/button/em/strong').text.replace(',', '')))

            print(f'Character scraped: {name_string} - {class_string}')

            # Getting date
            current_date = datetime.now()
            date.append(current_date.strftime("%Y-%m-%d"))

        except:
            print('character attribute not found')
            pass

    df = pd.DataFrame({'name':name,'class':char_class, 'level':level, 'power':power_score, 'price':rate, 'date':date})

    end_time = time.time()
    # Give us time to watch the scraped window
    time.sleep(20)
    print(f'Scraping finished in {end_time - start_time}:.4f')

    return df

def generate_nft_csv(data: pd.DataFrame):
    '''
        Creates a csv file from scraped data

        Params:
        - data: Pandas DataFRame containing the data

        Output:
        - No output, the function creates the csv file only
    '''
    data.to_csv(f'nft_list_{datetime.now().strftime("%Y-%m-%d")}.csv', index=False)
    print(f'csv file created:\n {data.head()}')

def main():
    df = nft_list_extractor('https://xdraco.com/nft')
    generate_nft_csv(df)

if __name__ == '__main__':
    main()
    print('process ended.')