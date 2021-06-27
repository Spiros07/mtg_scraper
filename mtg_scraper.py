
#%%
from selenium import webdriver
from selenium.webdriver.support.select import Select
import math
import time
import pandas as pd





options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=options)

#website to be scraped
driver.get('https://gatherer.wizards.com/Pages/Default.aspx')

time.sleep(1)

#find all the sets of cards
mtg_sets = driver.find_elements_by_xpath(
            './/*[contains(@id, "setAddText")]/option')
card_sets =[]
for sets in mtg_sets:
        card_sets.append(sets.text)
#currently brings only a few sets, for all, [1:]    
final_card_sets = card_sets[130:131]
print(final_card_sets)


#scrape the cards of every set in final_card_sets
cards = []

for set in final_card_sets:
    
    card_search = driver.find_element_by_xpath(
            './/*[contains(@id, "setAddText")]')
    choose_set = Select(card_search)
    choose_set.select_by_visible_text(set)
    
    search = driver.find_element_by_xpath(
            './/*[contains(@id, "searchSubmitButton")]')
    search.click()
    url = driver.current_url
    #print(url)
    time.sleep(1)
  
  
    # find how many cards are in each page
    mtg_table = driver.find_elements_by_xpath(
        './/*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_searchResultsContainer"]/div/table/tbody/tr/td/table')
    #print(len(mtg_table))

    # divide total no. of cards by no. of cards in page, round up to get the no. of pages 

    get_no_of_cards = driver.find_element_by_xpath(
        './/*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentHeader_searchTermDisplay"]').text
    
    #This find one looks good for targeting text
    no_of_cards = get_no_of_cards[
        get_no_of_cards.find('(') + 1: get_no_of_cards.find(')')]
    no_of_pages = math.ceil(int(no_of_cards)/len(mtg_table))
    #print(no_of_pages)
    

    # loop through the no. of pages      
    for page in range(0, no_of_pages, 1):
        driver.get(url+'&page='+str(page))
        # table of contents (cards on the page)
        mtg_table = driver.find_elements_by_xpath(
            './/*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_searchResultsContainer"]/div/table/tbody/tr/td/table')
        print(len(mtg_table))

    
        # info for every card
   
            
        for card in mtg_table:
                              
            # card name    
            cards_title = card.find_element_by_xpath(
                './/*[contains(@id, "cardTitle")]').text
            #print(cards_title)
            # card url    
            card_img_url = card.find_element_by_xpath(
                './/img').get_attribute('src')
            #print(card_img_url)
            # card edition and rarity
            card_edition_rarity = card.find_element_by_xpath(
                './/*[contains(@id, "cardSetCurrent")]/a/img').get_attribute('title')
            #print(card_edition_rarity)

            #gets all attributes for mana cost (it is a list, so make a list and iterate through the list)
            mana_cost_list = card.find_elements_by_xpath(
                './/*[contains(@class, "manaCost")]/img')
            if len(mana_cost_list) != 0:
                card_mana_cost = []
                for x in mana_cost_list:
                    card_mana_cost.append(x.get_attribute('alt'))
            else:
                print('0')
            #print(card_mana_cost)

            # card converted mana cost
            card_conv_mana_cost = card.find_element_by_xpath(
                './/*[contains(@class, "convertedManaCost")]').text
            #print(card_conv_mana_cost)
    
            # card type    
            card_type = card.find_element_by_xpath(
                './/*[contains(@class, "typeLine")]').text
            #print(card_type)
            # card abilities            
            card_abilities = card.find_element_by_xpath(
                './/*[contains(@class, "rulesText")]').text
            #print(card_abilities)


            time.sleep(1)

            cards.append([cards_title, card_img_url, 
            card_edition_rarity, card_mana_cost, card_conv_mana_cost, 
            card_type, card_abilities])
            
    
       
     
        
        
    back_to_start = driver.find_element_by_xpath(
        './/*[contains(@id, "Simple")]')
    back_to_start.click()

#prints all data in a dataframe
df_abilities = pd.DataFrame(cards)
df_abilities.columns = ['card name', 'img url', 
            'edition - rarity', 'mana cost', 'converted mana cost', 
            'type', 'abilities']
df_abilities.to_csv('scraper_final_130_131.csv')
    #print(df)



driver.quit()
