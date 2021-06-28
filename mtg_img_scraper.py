#%%
from selenium import webdriver
import urllib.request
from aws_upload import download_file
from aws_upload import upload_file
import tempfile
from tqdm import tqdm
import pandas as pd


# Define the driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=options)

init_src_list = pd.read_csv('final_set_11_21.csv')
src_list_med = init_src_list.loc[:, 'card name': 'img url']
src_list = pd.DataFrame(src_list_med)

#print(src_list)

with tempfile.TemporaryDirectory() as temp_dir:

    for card in tqdm(src_list.itertuples(index=True, name='Pandas')):

        try:
            urllib.request.urlretrieve(card[2], f'{temp_dir}/{card[1]}.png')
            upload_file(f'{temp_dir}/{card[1]}.png', 'mtg-project-bucket', f'mtg/{card[1]}')

        except:
           urllib.request.urlretrieve(card[2], f'{temp_dir}/{card[1][0]}.png')
           upload_file(f'{temp_dir}/{card[1][0]}.png', 'mtg-project-bucket', f'mtg/{card[1][0]}') 

driver.quit()
# Get the list of cat images
# src_list = ['https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=423808&type=card',
#             'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=423668&type=card'
#             ]

#          # Create a temporary directory, so you don't store images in your local machine
# with tempfile.TemporaryDirectory() as temp_dir:
# for card_name, scr in (tqdm(src_list)):
#                 urllib.request.urlretrieve(scr, f'{temp_dir}/card_{i}.png')
#                 upload_file(f'{temp_dir}/card_{i}.png', 'morfonios07.2', f'mtg/img_{i}')
# driver.quit()


# %%
