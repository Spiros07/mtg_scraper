
#%%
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException
import json

driver = webdriver.Chrome()

driver = webdriver.Chrome()

driver.get('https://gatherer.wizards.com/Pages/Search/Default.aspx?action=advanced&set=+%5B%22Unlimited%20Edition%22%5D')

mtg_cards = []
#mtg_cards = driver.find_element_by_xpath('//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_listRepeater_ctl00_cardTitle"]').text
#mtg_card_name = driver.find_element_by_xpath('//*[contains(@id, "cardTitle")]').text

#mtg_cards_img = driver.find_elements_by_xpath('//*[contains(@id, "cardImageLink")]')
#print(len(mtg_cards_img))
#print([mtg_card_name])

mtg_table = driver.find_elements_by_xpath('//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_searchResultsContainer"]/div/table/tbody/tr/td/table')
print(len(mtg_table))



for card in mtg_table:
    card_name = card.find_element_by_xpath('.//*[contains(@id, "cardTitle")]').text
    print(card_name)
#     card_img_url = card.find_element_by_xpath('//img')
#     print(card_img_url)

driver.quit()

# %%
#//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_searchResultsContainer"]/div/table/tbody/tr/td
#//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_listRepeater_ctl00_cardTitle"]