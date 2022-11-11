from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

s = Service('C:\Program Files (x86)\chromedriver.exe')
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(service=s, options=options)

df = pd.DataFrame(columns=['Price','Address','Metro', 'Summary', 'General Information', 'Building Information'])

PAGES = 50

#URL = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1' #regular
#URL = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&house_material%5B0%5D=1&offer_type=flat&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1' #Kirpich
#URL = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&house_material%5B0%5D=2&offer_type=flat&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1' #Monolitny
#URL = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&house_material%5B0%5D=3&offer_type=flat&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1' #Panel
URL = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&house_material%5B0%5D=8&offer_type=flat&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1' # Kirpich monolitny
driver.get(URL)

# Cookie acceptance
cookie = driver.find_element(By.CSS_SELECTOR, "[data-name='CookiesNotification']")
cookie_button = cookie.find_element(By.TAG_NAME, 'button')
cookie_button.click()


def ParseArticles():
     # Take the search page
    SearchResults = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-name='SearchEngineResultsPage']"))
    )
    articles = SearchResults.find_elements(By.CLASS_NAME, "_93444fe79c--avatar--WC_Vu")

    # Go through every article on the page
    for article in articles:
        article_data = {}
        # Click on the article   
        article.click()

        time.sleep(5)
        # Swith to the second tab
        try:
            window_after = driver.window_handles[1]
            driver.switch_to.window(window_after)
        except Exception:
            print("НЕ ОТКРЫЛОСЬ")
            continue

        # Take the price
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[itemprop='price']"))
                )
            article_data['Price'] = element.text
        except Exception:
            pass

        # Take the price per meter
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[class = 'a10a3f92e9--color_gray60_100--MlpSF a10a3f92e9--lineHeight_5u--cJ35s a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_14px--TCfeJ a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG a10a3f92e9--text_letterSpacing__0--mdnqq a10a3f92e9--text_whiteSpace__nowrap--Akbtc']"))
                )
            article_data['Price per meter'] = element.text
        except Exception:
           pass

        # Take the address
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "a10a3f92e9--address--F06X3"))
                )
            article_data['Address'] = element.text.replace("На карте", "")
        except Exception:
            pass

        # Take the metro station (Doesn't appear in every article)
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "a10a3f92e9--underground_link--Sxo7K"))
                )
            article_data['Metro'] = element.text
        except Exception:
            pass

        # Take the summary
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "a10a3f92e9--info-block--kXrDj"))
                )
            article_data['Summary'] = element.text.replace("\n",";")
        except Exception:
            pass

        # Take the general information (Doesn't appear in every article)
        try:
            expend_button = driver.find_element(By.CSS_SELECTOR, "[class='a10a3f92e9--button--OUjNH a10a3f92e9--offer_card_page-bti--spgEZ a10a3f92e9--collapsed-block-header--YjVTc a10a3f92e9--offer_card_block--no-margin--Qa9YL a10a3f92e9--offer_card_block--no-borderradius--xJTgJ']")
            expend_button.click()
            element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "a10a3f92e9--list--jHl8z"))
            )
            article_data['General Information'] = element.text.replace("\n",";")
        except Exception:
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "a10a3f92e9--list--jHl8z"))
                )
                article_data['General Information'] = element.text.replace("\n",";")
            except Exception:
                pass

        # Take the information about the building (Doesn't appear in every article)
        try:
            expend_button = driver.find_element(By.CSS_SELECTOR, "[class='a10a3f92e9--offer_card_page-bti--spgEZ a10a3f92e9--offer_card_content--no-margin--vjk7F a10a3f92e9--offer_card_block--no-borderradius--xJTgJ']")
            expend_button.click()
            element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "a10a3f92e9--container--z1RwI"))
        )
            article_data['Building Information'] = element.text.replace("\n",";")
        except Exception:
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "a10a3f92e9--column--XINlk"))
                )
                article_data['Building Information'] = element.text.replace("\n",";")
            except Exception:
                pass
        print(article_data)

        global df
        df = pd.concat([df, pd.DataFrame(article_data, index=[0])], ignore_index=True)

        # Close the second tab
        driver.close()

        # Switch to the first tab
        window_default = driver.window_handles[0]
        driver.switch_to.window(window_default)

try:
    for i in range(PAGES):
        print(str('='*20)+'Page ' + str(i+1) + str('='*20))
        ParseArticles()
        driver.get(URL + '&p=' + str(i+2))

finally:
    df.to_csv('Output.csv', index=False)
    driver.quit()