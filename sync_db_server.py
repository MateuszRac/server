import pandas as pd
from sqlalchemy import create_engine
import requests


df_server = pd.read_csv("https://popruntheworld.pl/raspberry/db_timestamps.php")
df_server['timestamp'] = pd.to_datetime(df_server['timestamp'])
df_server['valid'] = 1


engine = create_engine('mysql+pymysql://pi:raspberry@localhost:3306/db')
query = "SELECT * FROM meteo where timestamp >= DATE(NOW() - INTERVAL 7 DAY) group by 1,2;"
df_db = pd.read_sql(query, engine)
df_db['timestamp'] = pd.to_datetime(df_db['timestamp'])


df_upload = pd.merge(df_db, df_server, how="left", on=["timestamp", "variable"])

df_upload = df_upload[~df_upload['valid'].notnull()]
df_upload = df_upload[['variable','timestamp','value']]









# Convert DataFrame to CSV
csv_data = df_upload.to_csv(index=False)
url = 'https://popruntheworld.pl/raspberry/rpi_batch_upload.php'

response = requests.post(url, files={'csvfile': ('data.csv', csv_data)})
print(response.text)