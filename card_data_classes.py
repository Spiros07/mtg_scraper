#%%
from selenium import webdriver
import time
import pandas as pd
from scraper_classes import mtg_card_sets
from scraper_classes import cards_init_info
from scraper_classes import cards
import multiprocessing
from functools import partial



options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=options)

start = time.time()

#website to be scraped
driver.get('https://gatherer.wizards.com/Pages/Default.aspx')

time.sleep(1)

#find all the sets of cards
mtg_sets = driver.find_elements_by_xpath(
            './/*[contains(@id, "setAddText")]/option')

mtg_card_sets(mtg_sets)
final_card_sets = mtg_card_sets(mtg_sets)

cards_init_info(final_card_sets)
cards_urls = cards_init_info(final_card_sets)
cards_urls[0].to_csv('cards urls_1_2_v3.csv')



img_urls =[]
for img in cards_urls[1]:
    img_urls.append(img)

cards(cards_urls)
cards_info = cards(cards_urls)

df_img_urls = pd.DataFrame(img_urls)
df_card_info = pd.DataFrame(cards_info)
df_abilities = pd.concat([df_card_info, df_img_urls], axis=1)
df_abilities.columns = ['card name', 'mana cost', 
                'converted mana cost','type', 'abilities-1', 
                'abilities-2', 'flavour text-1', 'flavour text-2', 
                'power/toughness', 'rarity', 'expansion', 'card no', 'artist',
                 'img url']
df_abilities.to_csv('scraper_final_131_141_final.csv')


driver.quit()

end = time.time()
print((end - start)/60, " minutes")




# %%
