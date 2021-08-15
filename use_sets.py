#%%
from selenium import webdriver
import time
import pandas as pd


start = time.time()


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

start = time.time()


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
final_card_sets = card_sets[1:5]

# final_card_sets =['Aether Revolt', 'Tenth Edition', 'Eighth Edition', 'Alara Reborn']
# #, 'Tenth Edition', 'Eighth Edition'

print(final_card_sets)

driver.quit()



options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)


# final_sets = ['Aether Revolt', 'Alara Reborn', 'Alliances', 
#               'Amonkhet', 'Antiquities']
 
#, '10th Edition', '8th Edition', 
#              'Alara Reborn', 'Alliances', 'Amonhket', 'Exodus'

driver.get('https://www.mtgstocks.com/sets')



time.sleep(1)

all_sets = driver.find_elements_by_xpath('.//*[@id="wrapper"]/div/div/div/div[1]/ng-component/div[3]/div/ul/li')
print(len(all_sets))



search_sets = []
for set in all_sets:
    search = set.find_element_by_xpath('.//*[contains(@href, "sets")]')
    search_sets.append(search.text) 

#print(final_sets)
#print(search_sets)

card_prices = []
  

for set_of_cards in final_card_sets:
    if set_of_cards in search_sets:
        try:
            current_set = driver.find_element_by_xpath(f'.//*[contains(text(), "{set_of_cards}")]')
            current_set.click()
        except:
            pass

#//*[@id="wrapper"]/div/div/div/div[1]/ng-component/div[3]/div/ul/li[18]/a
#//*[@id="wrapper"]/div/div/div/div[1]/ng-component/div[3]/div/ul/li[15]/a
#//*[@id="wrapper"]/div/div/div/div[1]/ng-component/div[3]/div/ul/li[1]/a

        time.sleep(1)
           
        pagination = driver.find_elements_by_xpath('.//*[contains(@class, "pagination")]')
        #print(len(pagination))

        for x in range(len(pagination)+5):
            try:
                cards_values = driver.find_element_by_xpath(
                './/*[@id="wrapper"]/div/div/div/div[1]/ng-component/div[2]/div/tabset/div/tab[1]/mtg-sets-overview/data-table/div[2]/div/table/tbody').text
        
                card_prices.append(cards_values)
            
                next_page = driver.find_element_by_xpath('.//*[contains(@class, "next page")]')
            except:
                pass
            
            try:
                next_page.click()
                #time.sleep(1)
            except:
                pass
      
        #print(card_prices)

    go_back = driver.find_element_by_xpath('.//*[contains(@class, "nav-link")]')
    go_back.click()
  

#cleaning process

card_prices = [prices.split('\n') for prices in card_prices]

df_card_values = pd.DataFrame(card_prices)    
df_card_values_trans = df_card_values.transpose()
df_card_values_trans

df_card_values_trans = df_card_values_trans.stack().reset_index()
df_card_values_trans
df_card_values_trans.columns = ['level_0', 'level_1', 'card values']

df_card_values_trans = df_card_values_trans.drop(['level_0', 'level_1'], axis=1)
df_card_values_trans

df_card_values_trans = df_card_values_trans.drop_duplicates()
df_card_values_trans


df_split = df_card_values_trans.replace(regex=['N/A'], value=' $0.00 ')
# df_split = df_card_values_trans.replace(r'(\{/})', '', regex=True)
# df_split = df_card_values_trans.replace(r'(\{A})', '', regex=True)

#regex=['N/A'], value=' $ ')

#str.replace(r'(\[)', '', regex=True)

df_split_values = df_split.loc[:, 'card values'].str.split(pat='$', expand=True)


df_split_values.columns = ['card', 'avg price ($)', 
                            'market price ($)', 'foil avg ($)', 'foil price ($)']
df_split_values                            

df_split = df_split_values.loc[:, 'card'].str.rsplit(n=1, expand=True)
df_split

final_df = df_split_values.join(df_split, lsuffix='_caller', rsuffix='_other')
final_df.columns = ['col_1', 'avg price ($)', 'market price ($)', 'foil avg ($)', 
                    'foil price ($)', 'card name', 'rarity']

final_df = final_df.drop(['col_1', 'rarity'], axis=1)

final_df = final_df[['card name', 'avg price ($)', 'market price ($)', 
            'foil avg ($)', 'foil price ($)' ]]



#print(final_df)
#final_df.to_csv('prices_new_1_20_final.csv')
print(final_df.head())
print(final_df.dtypes)


driver.quit()

end = time.time()
print(end - start)

# %%

df_1 = pd.read_csv('prices_new_1_140_final.csv')

print(df_1.dtypes)



# %%
