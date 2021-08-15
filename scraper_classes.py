#%%
from selenium import webdriver
from selenium.webdriver.support.select import Select
import math
import time
import pandas as pd
#import numpy as np


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

#function that scrapes all the MtG sets
def mtg_card_sets(mtg_sets):
    card_sets = []
    for sets in mtg_sets:
        card_sets.append(sets.text)
#currently brings only a few sets, for all, [1:]    
    final_card_sets = card_sets[1:5]
    return(final_card_sets)

final_card_sets = mtg_card_sets(mtg_sets)


#function that scrapes card and img url to be used for more info
def cards_init_info(final_card_sets):
    cards_initial_info = []
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

        n_cards = driver.find_element_by_xpath(
        './/*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentHeader_searchTermDisplay"]').text
    
    #This find one looks good for targeting text
        no_of_cards = n_cards[
            n_cards.find('(') + 1: n_cards.find(')')]
        no_of_pages = math.ceil(int(no_of_cards)/len(mtg_table))
    #print(no_of_pages)
    

    # loop through the no. of pages      
        for page in range(no_of_pages):
            driver.get(url+'&page='+str(page))
        # table of contents (cards on the page)
            mtg_table = driver.find_elements_by_xpath(
            './/*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_searchResultsContainer"]/div/table/tbody/tr/td/table')
        #print(mtg_table)

    
        # info for every card
   
            
            for card in mtg_table:
                              
            # card name    
                cards_title = card.find_element_by_xpath(
                './/*[contains(@id, "cardTitle")]').text
            #print(cards_title)
            # card url    
                card_url = card.find_element_by_xpath(
                './/*[contains(@id, "cardTitle")]').get_attribute('href')
            #print(card_url)
            #card image url
                card_img_url = card.find_element_by_xpath(
                './/img').get_attribute('src')

                cards_initial_info.append([cards_title, card_url, card_img_url])


        back_to_start = driver.find_element_by_xpath(
            './/*[contains(@id, "Simple")]')
        back_to_start.click()    

    cards_init_info_list = pd.DataFrame(cards_initial_info)
    cards_init_info_list.columns =['card title', 'card url', 'card img url']

    cards_urls = cards_init_info_list.loc[:, "card url"]
    card_img_url = cards_init_info_list.loc[:, "card img url"]
#print(cards_urls)
    #cards_urls.to_csv('cards urls.csv')
    return[cards_urls, card_img_url]


#function that scrapes all info of a card

def cards(cards_urls):
    cards = []
    for card in cards_urls[0]:
        current_url = driver.get(card)
    #card name
        c_name = driver.find_element_by_xpath(
        './/*[contains(@id, "nameRow")]')
        cards_name = c_name.find_element_by_xpath(
        './/*[contains(@class, "value")]').text
    #print(cards_name)
    #mana cost
        mana_cost_list = driver.find_elements_by_xpath(
            './/*[contains(@id, "manaRow")]/div/img')
        try:
            card_mana_cost = []
            for mana in mana_cost_list:
                card_mana_cost.append(mana.get_attribute('alt'))
        except:
            print("0") 
    #print(card_mana_cost) 
    #converted mana cost
        try:
            total_mana_cost = driver.find_element_by_xpath(
                './/*[contains(@id, "cmcRow")]')
            converted_mana_cost = total_mana_cost.find_element_by_xpath(
                './/*[contains(@class, "value")]').text
        #print(converted_mana_cost)
        except:
            pass    
    #card type
        initial_card_type = driver.find_element_by_xpath(
            './/*[contains(@id, "typeRow")]')
        card_type = initial_card_type.find_element_by_xpath(
            './/*[contains(@class, "value")]').text
    #print(card_type)
    #card abilities
        try:
            card_ability = driver.find_element_by_xpath(
                './/*[contains(@class, "cardtextbox")]').text
        #print(card_ability)
        except:
            pass

        card_ability_2 = " "

    #flavour text
        try:
            flavour_text = driver.find_element_by_xpath(
                 './/*[contains(@class, "flavortextbox")]').text
         #print(flavour_text)
        except:
            flavour_text = " "

        flavour_text_2 = " "
    #power/toughness
        try:
            pt_text = driver.find_element_by_xpath(
            './/*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow"]')
            card_power_tough = pt_text.find_element_by_xpath(
             './/*[contains(@class, "value")]').text
         #print(card_power_tough)
        except:
            card_power_tough = " "
    #expansion
        expansion = driver.find_element_by_xpath(
                './/*[contains(@id, "currentSetSymbol")]').text
    #print(expansion)
    #rarity
        rarity = driver.find_element_by_xpath(
                './/*[contains(@id, "rarityRow")]').text
    #print(rarity)
    #card number
        try:
            card_number = driver.find_element_by_xpath(
                    './/*[contains(@id, "CardNumberValue")]').text
        except:
            pass
    #print(card_number)
    #artist
        card_artist = driver.find_element_by_xpath(
                './/*[contains(@id, "ArtistCredit")]').text
    #print(card_artist)
    
        cards.append([cards_name, card_mana_cost, 
            converted_mana_cost, card_type, card_ability, 
            card_ability_2, flavour_text, flavour_text_2,
            card_power_tough, rarity, expansion, card_number, card_artist])
    
    return cards    



# %%
