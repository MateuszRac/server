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

# Build the select query with the conditions
query = select([meteo_table.c.timestamp, meteo_table.c.value]).where(
    (meteo_table.c.timestamp >= seven_days_ago) &
    (meteo_table.c.variable == 'BMP280_P')
)

# Execute the query and fetch the results
result_proxy = engine.execute(query)
result_set = result_proxy.fetchall()

# Convert the result set into a Pandas DataFrame
df = pd.DataFrame(result_set, columns=['timestamp', 'value'])

# Create a plot with custom styling
plt.figure(figsize=(10, 6))
plt.plot(df['timestamp'], df['value'], color='blue', linestyle='-', marker='o', markersize=5, label='Value')
plt.title('Plot of Value vs Timestamp', fontsize=16)
plt.xlabel('Timestamp', fontsize=12)
plt.ylabel('Value', fontsize=12)
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
