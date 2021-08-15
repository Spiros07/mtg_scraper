#%%

from numpy import NaN, average, expand_dims
import pandas as pd
import numpy as np

mtg_df = pd.read_csv('final_set_final_1_5.csv')

# remove string 'rarity' from column 'rarity'
mtg_df['rarity'] = mtg_df['rarity'].str.split(pat=':', expand=True)[1] 

# split mana cost to coloured and colourless
mtg_df['mana cost'] = mtg_df['mana cost'].str.replace(r'(\[)', '', regex=True)
mtg_df['mana cost'] = mtg_df['mana cost'].str.replace(r'(\])', '', regex=True)

mtg_df['colourless mana'] = mtg_df['mana cost'].str.extract(r'([^a-zA-Z]\d)', expand=True)
mtg_df['colourless mana'] = mtg_df['colourless mana'].str.replace(r'(\')', '', regex=True)
mtg_df['colourless mana'] = mtg_df['colourless mana'].fillna(0) 
mtg_df['colourless mana'] = mtg_df['colourless mana'].astype(int)

mtg_df['coloured mana'] = mtg_df['mana cost'].str.extract(r'([a-zA-Z]\D+)', expand=True)
mtg_df['coloured mana'] = mtg_df['coloured mana'].str.replace(r'(\')', '', regex=True)


# split type of cards to creatures and the rest and show power and toughness
mtg_df['main type'] = mtg_df['type'].str.split(n=1, pat='—', expand=True)[0]

mtg_df['sub type'] = mtg_df['type'].str.split(n=1, pat='—', expand=True)[1]

#drop duplicate flavour text without droping the row
mtg_df.loc[mtg_df.duplicated(subset='flavour text-1', keep='first',), 'flavour text-1'] = np.nan
mtg_df.loc[mtg_df.duplicated(subset='flavour text-2', keep='first',), 'flavour text-2'] = np.nan

#split power and toughness
mtg_df['power'] = mtg_df['power/toughness'].str.split(n=1, pat='/', expand=True)[0]

mtg_df['toughness'] = mtg_df['power/toughness'].str.split(n=1, pat='/', expand=True)[1]

#re-arrange everything to give the final form to the dataset
mtg_df = mtg_df[['card name', 'expansion', 'rarity', 
                 'converted mana cost', 'colourless mana', 'coloured mana', 
                 'main type', 'sub type', 'power', 'toughness', 'abilities-1',
                 'abilities-2', 'flavour text-1', 'flavour text-2',
                 'card no', 'artist', 'avg price ($)', 'market price ($)',
                 'foil avg ($)','foil price ($)', 'img url'
                 ]]

print(mtg_df.dtypes)

mtg_df.to_csv('cleaned_test_final_1_5.csv')

# #print(mtg_df)

# mtg_df.to_csv('mtg_final.csv')
# mtg_df.to_json('mtg_final.json')


# mtg_df.isnull().sum()
# #in the categories they appear, nulls are acceptable (they can/shoul exist) 

# x = len(pd.concat(g for _, g in mtg_df.groupby("card name") if len(g) > 1))
# print (x)

# mtg_df.sort_values('card name', inplace=True)

mtg_df.drop_duplicates(subset='card name', keep=False, inplace=True)

mtg_df.to_csv('mtg_final_cleaned_no_dupl_1_5.csv')

print(mtg_df.dtypes)

# %%
