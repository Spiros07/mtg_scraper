#%%
import pandas as pd



df1 = pd.read_csv('prices_new_ult_test_1_290.csv')
df2 = pd.read_csv('scraper_final_test_1_5.csv')
complete_df = pd.merge(left=df2, right=df1, 
                    how='left', left_on='card name', right_on='card name') 

complete_df.to_csv('final_set_final_1_5.csv')


# %%
