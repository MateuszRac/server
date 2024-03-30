import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, select, func
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Create SQLAlchemy engine
engine = create_engine('mysql+pymysql://pi:raspberry@localhost:3306/db')

# Reflect the necessary table
metadata = MetaData()
meteo_table = Table('meteo', metadata, autoload=True, autoload_with=engine)

# Calculate the date 7 days ago
seven_days_ago = datetime.now() - timedelta(days=7)



#T1
# Build the select query with the conditions
query = select([meteo_table.c.timestamp, meteo_table.c.value]).where(
    (meteo_table.c.timestamp >= seven_days_ago) &
    (meteo_table.c.variable == '28-3c6204572bfc')
)

# Execute the query and fetch the results
result_proxy = engine.execute(query)
result_set = result_proxy.fetchall()

# Convert the result set into a Pandas DataFrame
df1 = pd.DataFrame(result_set, columns=['timestamp', 'value'])




#T2
# Build the select query with the conditions
query = select([meteo_table.c.timestamp, meteo_table.c.value]).where(
    (meteo_table.c.timestamp >= seven_days_ago) &
    (meteo_table.c.variable == '28-3ce104570b5f')
)

# Execute the query and fetch the results
result_proxy = engine.execute(query)
result_set = result_proxy.fetchall()

# Convert the result set into a Pandas DataFrame
df2 = pd.DataFrame(result_set, columns=['timestamp', 'value'])




# Create a plot with custom styling
plt.figure(figsize=(10, 6))
plt.plot(df1['timestamp'], df1['value'], color='red', linestyle='-', markersize=5, label='Temperatura 2m')
plt.plot(df2['timestamp'], df2['value'], color='blue', linestyle='-', markersize=5, label='Temperatura grunt')
plt.title('Temperatura', fontsize=16)
plt.xlabel('Data', fontsize=12)
plt.ylabel('stopnie C', fontsize=12)
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)

# Add legend
plt.legend(loc='upper right', fontsize=12)

# Save the plot as an image
plt.savefig('/var/www/html/img.png', bbox_inches='tight')

# Close the plot
plt.close()

# Close the result proxy and dispose of the engine
result_proxy.close()
engine.dispose()
