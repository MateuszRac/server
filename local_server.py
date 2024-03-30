import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# Replace 'username', 'password', 'host', 'port', and 'database_name' with your MySQL credentials
engine = create_engine('mysql+pymysql://pi:raspberry@localhost:3306/db')

df = pd.DataFrame(columns=['variable','timestamp','value'])
df.loc[len(df)] = ['TEST',datetime(2024,3,30,12,0),69]
df.loc[len(df)] = ['TEST',datetime(2024,3,30,12,0),666]

# Replace 'meteo' with your table name
df.to_sql('meteo', con=engine, if_exists='append', index=False)
