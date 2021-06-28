#%%
from selenium import webdriver
from selenium.webdriver.support.select import Select
import math
import time
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC



driver = webdriver.Chrome()
   
        
        
        
        
driver.get('https://www.tcgplayer.com/search/magic/product?productLineName=magic')

search = driver.find_element_by_xpath('.//*[@id="autocomplete-input"]')
search.click()
search.send_keys('Exquisite Archangel')
time.sleep(1)
#search button
                #search_button = driver.find_element_by_xpath('//*[@id="app"]/div/header/div/div[2]/div/div[2]/div[2]/a/div/div')
                #search_button.click()
                #time.sleep(1)
#search in magic the gathering
search_button = driver.find_element_by_xpath('.//*[@id="app"]/div/header/div/div[2]/div/div[2]/div[2]/a')
time.sleep(1)
search_button.click()


url = driver.current_url

#WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "element_css"))).get_attribute("value")        
        

card_table = driver.find_element_by_xpath('.//*[@id="app"]/div/section[2]/section/section/span/section')

card_price_size = card_table.find_elements_by_xpath('.//*[contains(@class, "market-price--value")]')

#card_price = card_price_list.text



for x in range(1, len(card_price_size), 1):
    card_price = []
    for price in card_price_size:
        
        time.sleep(1)
        card_price_list = driver.find_element_by_xpath('.//*[@id="app"]/div/section[2]/section/section/span/section/div[%s]/div/a[1]/section[3]/span[2]'%str(x))
        card_price.append(card_price_list.text)
    else:
        continue
#driver.find_element_by_xpath('.//*[@id="app"]/div/section[2]/section/section/span/section/div[%s]/div/a[1]/section[3]/span[2]'%str(x))
#         xpath = ".//*[@id='app']/div/section[2]/section/section/span/section/div["
#         xpath += str(x)
#         xpath += "]/div/a[1]/section[3]/span[2]"
#         card_price_list = driver.find_element_by_xpath(xpath)
        
print(['Exquisite Archangel', card_price])
time.sleep(1)

        

driver.quit()

# %%
