#%%
from selenium import webdriver
from selenium.webdriver.support.select import Select
import math
import time
import pandas as pd

driver = webdriver.Chrome()

#website to be scraped
driver.get('https://gatherer.wizards.com/Pages/Default.aspx')

time.sleep(1)

#find all the sets of cards
'''
No more than 79 characters per line
'''
mtg_sets = driver.find_elements_by_xpath(
    './/*[contains(@id, "setAddText")]/option')
card_sets =[]
for sets in mtg_sets:
        card_sets.append(sets.text)

#currently brings only a few sets, for all, [1:]    
final_card_sets = card_sets[1:11]
print(final_card_sets)


time.sleep(1)

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
    
    #find how many cards are in each page
    mtg_table = driver.find_elements_by_xpath(
        './/*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_searchResultsContainer"]/div/table/tbody/tr/td/table')
    #print(len(mtg_table))

    # divide total no. of cards by no. of cards in page, round up to get the no. of pages 
    '''
    get_no_of_cards sounds more like a function
    variables should have names indicating nouns
    '''
    no_of_cards = driver.find_element_by_xpath(
        './/*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentHeader_searchTermDisplay"]').text
    
    #This find one looks good for targeting text
    '''
    Try making the name of variables more concise
    n_cards
    n_pages
    '''
    n_cards = no_of_cards[no_of_cards.find('(') + 1: no_of_cards.find(')')]
    n_pages = math.ceil(int(n_cards)/len(mtg_table))
    #print(no_of_pages)
    
    time.sleep(1)

 # loop through the no. of pages
    '''
    This range function looks redundant. It's the same as
    writing range(no_of_pages)
    '''
    for page in range(0, n_pages, 1):
        driver.get(url+'&page='+str(page))
# table of contents (cards on the page)
        mtg_table = driver.find_elements_by_xpath(
            './/*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_searchResultsContainer"]/div/table/tbody/tr/td/table')
        #print(len(mtg_table))

    
        # info for every card
   
            
        for card in mtg_table:
            '''
            We can see what this loop is doing, but you need to go 
            through the whole loop to understand it
            Encapsulate it into a function would improve readability
            something such as get_cards_info(mtg_table)
            '''
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
            #gets all attributes for mana cost 
            # (it is a list, so make a list and iterate through the list)
            mana_cost_list = card.find_elements_by_xpath(
                './/*[contains(@class, "manaCost")]/img')
            if len(mana_cost_list) != 0:
                card_mana_cost = []
                for x in mana_cost_list:
                    card_mana_cost.append(x.get_attribute('alt'))
            else:
                continue
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
            card_edition_rarity, card_mana_cost, 
            card_conv_mana_cost, card_type, card_abilities])
     
        
        
    back_to_start = driver.find_element_by_xpath(
        './/*[contains(@id, "Simple")]')
    back_to_start.click()

    #prints all data in a dataframe
df_abilities = pd.DataFrame(cards)
df_abilities.columns = ['card name', 'img url', 'edition - rarity', 
                        'mana cost', 'converted mana cost', 'type', 'abilities']
df_abilities.to_csv('scraper_final.csv')
    #print(df)


#get the names to look for more info (prices so far)
'''
Give more descriptive names
'''
list_of_card_names = df_abilities.loc[:, "card name"]
print(list_of_card_names)


driver.quit()

#use the names from list_of_card_names to find the prices
driver = webdriver.Chrome()

        
driver.get('https://www.mtgstocks.com/prints')

driver.fullscreen_window()
#I need the fullscreen as the search bar does not appear else
time.sleep(1)

search = driver.find_element_by_xpath(
    './/*[@id="navbarSupportedContent"]/form/input')
time.sleep(1)
search.submit()

prices = []


for card in list_of_card_names:

#look for the price of the card

    init_url = driver.current_url

    search.send_keys(card)
    
    time.sleep(1)
    
    search.send_keys(u'\ue007')
    search.click()
    new_url = driver.current_url
    '''
    Give error type to except such as TypeError. That way you will be able
    to detect more bugs 
    Give value None to avg_price if not found, this will make things easier when
    cleaning the data (df.isna(), df.dropna())
    '''
    try:
        avg_price = driver.find_element_by_xpath(
            './/*[contains(@text, "Average")]').text

    except:
        avg_price = 'null'
    
    try:
        market_price = driver.find_element_by_xpath(
            './/*[contains(@text, "Market")]').text
    except:
        market_price = 'null'

    try:    
        foil_price = driver.find_element_by_xpath(
            './/*[contains(@text, "Foil")]').text
    except:
        foil_price = 'null'


#for double cards (2 names with //) search does not work (
# it does not move to the naxt page) 
# so I need to remove // for it to work

    if new_url == init_url:
        search.submit()
        search.clear()
        search.send_keys(card.replace("//", " "))
        time.sleep(1)
        search.send_keys(u'\ue007')
        search.click()

    try:
        avg_price = driver.find_element_by_xpath(
            './/*[contains(@text, "Average")]').text
    except:
        avg_price = 'null'
    
    try:
        market_price = driver.find_element_by_xpath(
            './/*[contains(@text, "Market")]').text
    except:
        market_price = 'null'

    try:    
        foil_price = driver.find_element_by_xpath(
            './/*[contains(@text, "Foil")]').text
    except:
        foil_price = 'null'

    time.sleep(1)


    prices.append([avg_price, market_price, foil_price]) 
    
#create a dataframe with the prices
df_prices = pd.DataFrame(prices, index=[list_of_card_names])
df_prices.columns = ['average price', 'market price', 'foil price']


df_prices.to_csv('prices.csv')
        
#print([cards, prices])

# use card name as a key column to merge the 2 dataframes
complete_df = pd.merge(left=df_abilities, right=df_prices, 
                        how='outer', left_on='card name', right_on='card name')        

complete_df.to_csv('final_set.csv')


driver.quit()




# %%