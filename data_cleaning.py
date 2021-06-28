#%%

from numpy import average
import pandas as pd
import re

mtg_df = pd.read_csv('final_set.csv', delimiter=',')


mtg_df['average price'] = mtg_df['average price'].replace(
    {'null':'None'}
    )

mtg_df['market price'] = mtg_df['market price'].replace(
    {'null':'None'}
    )

mtg_df['foil price'] = mtg_df['foil price'].replace(
    {'null':'None'}
    )



# split edition-rarity to edition and rarity
ed_rar_df = mtg_df['edition - rarity'].str.rsplit(n=1, pat='(', expand=True)
edition_df = ed_rar_df[0]
rarity_df = ed_rar_df[1]

# print(ed_rar_df)
# print(edition_df)
# print(rarity_df)

edition_rarity_df = pd.DataFrame({'edition':[], 'rarity':[]})
edition_rarity_df['edition'] = edition_df
edition_rarity_df['rarity'] = rarity_df


mtg_df = pd.concat([mtg_df, edition_rarity_df], axis=1, ignore_index=False) 



# split mana cost to coloured and colourless
mana_df = mtg_df['mana cost'].str.split(n=1, pat=',', expand=True)
colourless_df = mana_df[0]
coloured_df = mana_df[1]

mana_cost_df = pd.DataFrame({'colourless mana':[], 'coloured mana':[]})
mana_cost_df['colourless mana'] = colourless_df
mana_cost_df['coloured mana'] = coloured_df

mtg_df = pd.concat([mtg_df, mana_cost_df], axis=1, ignore_index=False) 


# split type of cards to creatures and the rest and show power and toughness
type_df = mtg_df['type'].str.split(n=1, pat='—', expand=True)
main_type_df = type_df[0]
sub_type_df = type_df[1]

card_type_df = pd.DataFrame({'main type':[], 'sub_type':[]})
card_type_df['main type'] = main_type_df
card_type_df['sub_type'] = sub_type_df

mtg_df = pd.concat([mtg_df, card_type_df], axis=1, ignore_index=False) 


subtype_df = mtg_df['sub_type'].str.split(n=1, pat='(', expand=True)
main_subtype_df = subtype_df[0]
sub_subtype_df = type_df[1]

subtype_df = pd.DataFrame({'sub type':[], 'power/toughness':[]})
subtype_df['sub type'] = main_subtype_df
subtype_df['power/toughness'] = sub_subtype_df

mtg_df = pd.concat([mtg_df, subtype_df], axis=1, ignore_index=False) 


power_toughness_df = mtg_df['power/toughness'].str.split(n=1, pat='/', expand=True)
power_df = power_toughness_df[0]
toughness_df = power_toughness_df[1]

power_toughness_df = pd.DataFrame({'power':[], 'toughness':[]})
power_toughness_df['power'] = power_df
power_toughness_df['toughness'] = toughness_df

mtg_df = pd.concat([mtg_df, power_toughness_df], axis=1, ignore_index=False) 


# show the average price as a float
avg_price_df = mtg_df['average price'].str.split(n=1, pat='$', expand=True)
average_price_df = avg_price_df[1]

avg_price_df = pd.DataFrame({'average price in $':[]})
avg_price_df['average price in $'] = average_price_df


mtg_df = pd.concat([mtg_df, avg_price_df], axis=1, ignore_index=False) 


# show the market price as a float
mark_price_df = mtg_df['market price'].str.split(n=1, pat='$', expand=True)
market_price_df = mark_price_df[1]

mark_price_df = pd.DataFrame({'market price in $':[]})
mark_price_df['market price in $'] = market_price_df


mtg_df = pd.concat([mtg_df, mark_price_df], axis=1, ignore_index=False) 


#show the price of a foil card (if printed in foil) as a float
f_price_df = mtg_df['foil price'].str.split(n=1, pat='$', expand=True)
foil_price_df = f_price_df[1]

f_price_df = pd.DataFrame({'foil price in $':[]})
f_price_df['foil price in $'] = foil_price_df


mtg_df = pd.concat([mtg_df, f_price_df], axis=1, ignore_index=False) 


# delete all unwanted columns
del mtg_df['Unnamed: 11']
del mtg_df['edition - rarity']
del mtg_df['mana cost']
del mtg_df['type']
del mtg_df['sub_type']
del mtg_df['power/toughness']
del mtg_df['average price']
del mtg_df['market price']
del mtg_df['foil price']
del mtg_df['Unnamed: 0']



mtg_df = mtg_df[['card name', 'edition', 'rarity', 
                 'converted mana cost', 'colourless mana', 'coloured mana', 
                 'main type', 'sub type', 'power', 'toughness', 
                 'abilities', 'average price in $', 'market price in $',
                 'foil price in $', 'img url'
                 ]]


#print(mtg_df)

mtg_df.to_csv('mtg_final.csv')
mtg_df.to_json('mtg_final.json')


mtg_df.isnull().sum()
#in the categories they appear, nulls are acceptable (they can/shoul exist) 

x = len(pd.concat(g for _, g in mtg_df.groupby("card name") if len(g) > 1))
print (x)

mtg_df.sort_values('card name', inplace=True)

mtg_df.drop_duplicates(subset='card name', keep=False, inplace=True)

mtg_df.to_csv('mtg_final_cleaned.csv')



# %%
