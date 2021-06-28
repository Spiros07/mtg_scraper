#%%
from selenium import webdriver
from selenium.webdriver.support.select import Select
import math
import time
import pandas as pd



driver = webdriver.Chrome()

driver.get('https://gatherer.wizards.com/Pages/Default.aspx')

time.sleep(1)


mtg_sets = driver.find_elements_by_xpath('.//*[contains(@id, "setAddText")]/option')
card_sets =[]
for sets in mtg_sets:
    card_sets.append(sets.text)
#currently brings only a few sets, for all, [1:]    
    final_card_sets = card_sets[1:3]
    print(final_card_sets)

time.sleep(2)
card_search = driver.find_element_by_xpath('.//*[contains(@id, "setAddText")]')
card_search.click()


for set in final_card_sets:

    card_search = driver.find_element_by_xpath('.//*[contains(@id, "setAddText")]')
    choose_set = Select(card_search)
    choose_set.select_by_visible_text(set)

    search = driver.find_element_by_xpath('.//*[contains(@id, "searchSubmitButton")]')
    search.click()
    url = driver.current_url
#print(url)
time.sleep(1)

driver.get(url)

mtg_table = driver.find_elements_by_xpath('.//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_searchResultsContainer"]/div/table/tbody/tr/td/table')
#print(len(mtg_table))



no_of_cards = driver.find_element_by_xpath('.//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentHeader_searchTermDisplay"]').text[-4:-1]
no_of_pages = math.ceil(int(no_of_cards)/len(mtg_table))



time.sleep(1)
#print(no_of_pages)
for page in range(0, no_of_pages, 1):
        driver.get(url+'&page='+str(page))
#table of contents
        mtg_table = driver.find_elements_by_xpath('.//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_searchResultsContainer"]/div/table/tbody/tr/td/table')
    #print(len(mtg_table))


#info for every card

cards = []
    #cards = {}
for card in mtg_table:
#card name    
        cards_title = card.find_element_by_xpath('.//*[contains(@id, "cardTitle")]').text

#print(cards_title)
#card url    
        card_img_url = card.find_element_by_xpath('.//img').get_attribute('src')
        #print(card_img_url)

print(cards)


back_to_start = driver.find_element_by_xpath('.//*[contains(@id, "Simple")]')
back_to_start.click()


driver.quit()
# %%
