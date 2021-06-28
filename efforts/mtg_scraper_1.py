#%%
from selenium import webdriver
from selenium.webdriver.support.select import Select
import math
import time
import pandas as pd






driver = webdriver.Chrome()

# options = webdriver.ChromeOptions()
# options.add_argument('--no-sandbox')
# chrome = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)



driver.get('https://gatherer.wizards.com/Pages/Default.aspx')

time.sleep(1)



mtg_sets = driver.find_elements_by_xpath('.//*[contains(@id, "setAddText")]/option')
card_sets =[]
for sets in mtg_sets:
        card_sets.append(sets.text)
#currently brings only a few sets, for all, [1:]    
final_card_sets = card_sets[1:2]
print(final_card_sets)


time.sleep(2)
card_search = driver.find_element_by_xpath('.//*[contains(@id, "setAddText")]')
card_search.click()

cards = []


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
   
            
        for card in mtg_table:
                 
    #card name    
            cards_title = card.find_element_by_xpath('.//*[contains(@id, "cardTitle")]').text
            #print(cards_title)
    #card url    
            #card_img_url = card.find_element_by_xpath('.//img').get_attribute('src')
            #print(card_img_url)



            cards.append([cards_title])
            
    
       
     
        
        
    back_to_start = driver.find_element_by_xpath('.//*[contains(@id, "Simple")]')
    back_to_start.click()

    #prints all data in a dataframe
df = pd.DataFrame(cards)
df.columns = ['card name']
df.to_csv('scraper.csv')
    #print(df)

card_names_2 = df.loc[:, "card name"]
print(card_names_2)


    

for k in card_names_2:
                driver.get('https://www.tcgplayer.com/search/magic/product?productLineName=magic')

                search = driver.find_element_by_xpath('.//*[@id="autocomplete-input"]')
                search.click()
                search.send_keys(k)
                time.sleep(1)
#search button
                search_button = driver.find_element_by_xpath('//*[@id="app"]/div/header/div/div[2]/div/div[2]/div[2]/a/div/div')
                search_button.click()
                time.sleep(1)
#search in magic the gathering
                # search_button = driver.find_element_by_xpath('.//*[@id="app"]/div/header/div/div[2]/div/div[2]/div[2]/a')
                # time.sleep(1)
                # search_button.click()


                url = driver.current_url

#WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "element_css"))).get_attribute("value")        
        
                
                card_table = driver.find_element_by_xpath('.//*[@id="app"]/div/section[2]/section/section/span/section')


                card_price_size = card_table.find_elements_by_xpath('.//*[contains(@class, "market-price--value")]')
                #print('card-price-size', card_price_size)
                
                time.sleep(1)
#card_price = card_price_list.text

                card_price = []

                #for x in range(1, len(card_price_size)):
                for price in card_price_size:
                    if price in card_price_size:
                        time.sleep(1)
                        card_price_list = price.text
                        #card_table.find_element_by_xpath('.//*[contains(@class, "market-price--value")]')
                    #card_price_list = driver.find_element_by_xpath('.//*[@id="app"]/div/section[2]/section/section/span/section/div[%s]/div/a[1]/section[3]/span[2]'%str(x))
                    
                        card_price.append(card_price_list)
                        
                
                        time.sleep(1)
                    else:
                        continue
                

                print([k, card_price])


#driver.find_element_by_xpath('.//*[@id="app"]/div/section[2]/section/section/span/section/div[%s]/div/a[1]/section[3]/span[2]'%str(x))
#         xpath = ".//*[@id='app']/div/section[2]/section/section/span/section/div["
#         xpath += str(x)
#         xpath += "]/div/a[1]/section[3]/span[2]"
#         card_price_list = driver.find_element_by_xpath(xpath)
time.sleep(1)

                

        

driver.quit()




# %%
'''
fetch the whole list of sets

mtg_sets = driver.find_elements_by_xpath('.//*[contains(@id, "setAddText")]/option')
card_sets =[]
for sets in mtg_sets:
        card_sets.append(sets.text)
    # else:
    #     continue
final_card_sets = card_sets[1:]
print(card_sets)
'''

'''
write something in the search bar and then click search
from selenium import webdriver
import math
import time

driver = webdriver.Chrome()

driver.get('https://gatherer.wizards.com/Pages/Default.aspx')

card_search = driver.find_element_by_xpath('.//*[contains(@class, "textboxinput")]')
card_search.click()
card_search.send_keys('Unlimited Edition')

search = driver.find_element_by_xpath('.//*[contains(@id, "searchSubmitButton")]')
search.click()
'''


