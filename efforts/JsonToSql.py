from sqlalchemy import create_engine 
import pandas as pd

# setting up the db
user = 'postgres' 
password = 'postgres' 
host = 'localhost' 
port = '5432' 
db_name = 'postgres' 
db_string = f"postgresql://{user}:{password}@{host}:{port}/{db_name}" 

# create engine
db = create_engine(db_string) 

# open json file
with open('vets.json') as f:
    df = pd.read_json(f, orient='records')

# insert data to db
df.to_sql('vets', db)