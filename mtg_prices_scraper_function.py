#%%
from selenium import webdriver
import time
import pandas as pd

start = time.time()

#prepare the driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

driver.get('https://www.mtgstocks.com/sets')

time.sleep(1)


def no_mtg_sets():
    '''returns the number of all mtg sets'''
    all_sets = driver.find_elements_by_xpath('.//*[@id="wrapper"]/div/div/div/div[1]/ng-component/div[3]/div/ul/li')
    return len(all_sets)


def card_values():
    '''returns a list with the cards and their prices'''
    card_prices = []

    no_of_sets = no_mtg_sets()
    for i in range(no_of_sets):
#    for i in range(1, 10):    
            try:
                current_set = driver.find_element_by_xpath(f'.//*[@id="wrapper"]/div/div/div/div[1]/ng-component/div[3]/div/ul/li[{i}]/a')
                driver.execute_script("arguments[0].click();", current_set)

            except:
                pass

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
  
    return card_prices  


def card_cleaning():
    '''performs data cleaning on the cards scraped, 
    splits the cards and the prices in different columns, 
    drops the $ to turn strings into (potentially) floats,
    replaces the None values with Nan'''

    card_prices = card_values()
    #cleaning process

    card_prices = [prices.split('\n') for prices in card_prices]

    #merge all sublists in one
    card_prices = [item for sublist in card_prices for item in sublist]

    #split the list into correct length
    card_prices = [card_prices[x:x+2] for x in range(0, len(card_prices), 2)]


    df_card_values = pd.DataFrame(card_prices)    

    df_card_values.columns = ['card name', 'card values']

    df_split = df_card_values.replace(regex=['N/A'], value='$')

    df_split_values = df_split.loc[:, 'card values'].str.split(pat=' ', expand=True)

    df_split_values.columns = ['rarity', 'avg price ($)', 
                                'market price ($)', 'foil avg ($)', 'foil price ($)', 'col_6']
    df_split_values     

    final_df = df_split_values.join(df_split, lsuffix='_caller', rsuffix='_other')

    final_df = final_df.drop(['rarity', 'card values'], axis=1)

    final_df = final_df[['card name', 'avg price ($)', 'market price ($)', 
                'foil avg ($)', 'foil price ($)' ]]


    final_df = pd.DataFrame(final_df)
    clean_df =final_df.drop_duplicates(subset='card name')

    #change none values to $
    clean_df['avg price ($)'] = [str(i or '$') for i in clean_df['avg price ($)']]
    clean_df['market price ($)'] = [str(i or '$') for i in clean_df['market price ($)']]
    clean_df['foil avg ($)'] = [str(i or '$') for i in clean_df['foil avg ($)']]
    clean_df['foil price ($)'] = [str(i or '$') for i in clean_df['foil price ($)']]

    #if needed to make complete column a float, uncomment following row to fill NaN with 0.00
    #final_df.fillna('$0.00')

    #remove $ to end up with floats and Nan
    clean_df['avg price ($)'] = clean_df['avg price ($)'].map(lambda x: x.lstrip('$'))
    clean_df['market price ($)'] = clean_df['market price ($)'].map(lambda x: x.lstrip('$'))
    clean_df['foil avg ($)'] = clean_df['foil avg ($)'].map(lambda x: x.lstrip('$'))
    clean_df['foil price ($)'] = clean_df['foil price ($)'].map(lambda x: x.lstrip('$'))

    return clean_df

clean_df = card_cleaning()

print(clean_df)

clean_df.to_csv('prices_new_class_test.csv')

#print(final_df.dtypes)


driver.quit()

end = time.time()

print('time needed in sec: ', end - start)

# %%


