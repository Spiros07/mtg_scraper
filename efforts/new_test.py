#%%

#write something in the search bar and then click search
from selenium import webdriver
import math
import time


driver = webdriver.Chrome()

driver.get('https://prices.tcgplayer.com/price-guide')

search = driver.find_element_by_xpath('.//*[contains(@id, "SearchProductName")]')
search.click()
search.send_keys('Aegis Automaton')

search_button = driver.find_element_by_xpath('.//*[@id="pagecontent"]/header/div[3]/div[2]/button')
search_button.click()

url = driver.current_url

time.sleep(2)

card_table = driver.find_element_by_xpath('.//*[@id="app"]/div/section[2]/section/section/span/section')

card_price_size = card_table.find_elements_by_xpath('.//*[contains(@class, "market-price--value")]')

#card_price = card_price_list.text

card_price = []
for x in range(1, len(card_price_size)+1):
       card_price_list = driver.find_element_by_xpath('.//*[@id="app"]/div/section[2]/section/section/span/section/div[%s]/div/a[1]/section[3]/span[2]'%str(x))
       
#         xpath = ".//*[@id='app']/div/section[2]/section/section/span/section/div["
#         xpath += str(x)
#         xpath += "]/div/a[1]/section[3]/span[2]"
#         card_price_list = driver.find_element_by_xpath(xpath)
       card_price.append(card_price_list.text)
print(card_price)






#//*[@id="app"]/div/section[2]/section/section/span/section/div[1]/div/a[1]/section[3]/span[2]
#//*[@id="app"]/div/section[2]/section/section/span/section/div[2]/div/a[1]/section[3]/span[2]

# driver = webdriver.Chrome()

# driver.get('https://gatherer.wizards.com/Pages/Default.aspx')

# time.sleep(1)




# mtg_sets = driver.find_elements_by_xpath('.//*[contains(@id, "setAddText")]/option')
# card_sets =[]
# for sets in mtg_sets:
#         card_sets.append(sets.text)
#     # else:
#     #     continue
# final_card_sets = card_sets[1:]
# print(final_card_sets)

#driver.quit()
# %%
