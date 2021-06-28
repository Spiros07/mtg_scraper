#%%
from selenium import webdriver
import math
import time


driver = webdriver.Chrome()

list_of_sets = ["Unlimited Edition", "Aether Revolt"]
print(list_of_sets[0])

driver.get('https://gatherer.wizards.com/Pages/Search/Default.aspx?action=advanced&set=+["Unlimited+Edition"]&page=0')


no_of_cards = driver.find_element_by_xpath('.//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentHeader_searchTermDisplay"]').text[-4:-1]
no_of_pages = math.ceil(int(no_of_cards)/100)

#print(no_of_pages)

time.sleep(1)

for page in range(0, no_of_pages, 1):
    url = 'https://gatherer.wizards.com/Pages/Search/Default.aspx?action=advanced&set=+["Unlimited+Edition"]&page='+str(page)
    driver.get(url)
    #table of contents
    mtg_table = driver.find_elements_by_xpath('.//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_searchResultsContainer"]/div/table/tbody/tr/td/table')
        #print(len(mtg_table))

    cards = []
    #info for every card
    for card in mtg_table:
        card_name = card.find_element_by_xpath('.//*[contains(@id, "cardTitle")]').text
        print(card_name)


driver.quit()



#mana_cost_list = card.find_elements_by_xpath('.//*[contains(@class, "manaCost")]/img')
#    if len(mana_cost_list) != 0:
#        card_mana_cost =[]
#        for x in mana_cost_list:
#            card_mana_cost.append(x.get_attribute('alt'))
#    else:
#        continue
#    print(card_mana_cost)

#//*[@id="ctl00_ctl00_MainContent_Content_SearchControls_setAddText"]





# %%
