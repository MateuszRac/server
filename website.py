import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, select, func
from datetime import datetime, timedelta
import matplotlib.pyplot as plt



def remove_outliers_with_window(dataframe, column_name, window_size=5, threshold=1.5):
    filtered_indices = []
    
    for i in range(len(dataframe)):
        start_index = max(0, i - window_size // 2)
        end_index = min(len(dataframe), i + window_size // 2 + 1)
        
        window = dataframe.iloc[start_index:end_index][column_name].astype(float)  # Convert to float
        
        Q1 = window.quantile(0.25)
        Q3 = window.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        if dataframe.iloc[i][column_name] >= lower_bound and dataframe.iloc[i][column_name] <= upper_bound:
            filtered_indices.append(i)
    
    return dataframe.iloc[filtered_indices]


















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
plt.plot(df1['timestamp'], df1['value'], color='red', linestyle='-', markersize=5, label='TP 1.5m')
plt.plot(df2['timestamp'], df2['value'], color='blue', linestyle='-', markersize=5, label='TP grunt')
plt.title('Temperatura na zewnatrz', fontsize=16)
plt.xlabel('Data', fontsize=12)
plt.ylabel('stopnie C', fontsize=12)
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)

# Add legend
plt.legend(loc='upper left', fontsize=12)

# Save the plot as an image
plt.savefig('/var/www/html/tp_week.png', bbox_inches='tight')

# Close the plot
plt.close()








#PIEC
# Build the select query with the conditions
query = select([meteo_table.c.timestamp, meteo_table.c.value]).where(
    (meteo_table.c.timestamp >= seven_days_ago) &
    (meteo_table.c.variable == '28-0000092414da')
)

# Execute the query and fetch the results
result_proxy = engine.execute(query)
result_set = result_proxy.fetchall()

# Convert the result set into a Pandas DataFrame
df3 = pd.DataFrame(result_set, columns=['timestamp', 'value'])




# Create a plot with custom styling
plt.figure(figsize=(10, 6))
plt.plot(df3['timestamp'], df3['value'], color='red', linestyle='-', markersize=5, label='Temperatura na piecu')
plt.title('Piec', fontsize=16)
plt.xlabel('Data', fontsize=12)
plt.ylabel('stopnie C', fontsize=12)
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)

# Add legend
plt.legend(loc='upper left', fontsize=12)

# Save the plot as an image
plt.savefig('/var/www/html/piec_week.png', bbox_inches='tight')

# Close the plot
plt.close()







#BMP280
# Build the select query with the conditions
query = select([meteo_table.c.timestamp, meteo_table.c.value]).where(
    (meteo_table.c.timestamp >= seven_days_ago) &
    (meteo_table.c.variable == 'BMP280_P')
)

# Execute the query and fetch the results
result_proxy = engine.execute(query)
result_set = result_proxy.fetchall()

# Convert the result set into a Pandas DataFrame
df4 = pd.DataFrame(result_set, columns=['timestamp', 'value'])
df4_clean = remove_outliers_with_window(df4,'value',window_size=10, threshold=1.5)



# Create a plot with custom styling
plt.figure(figsize=(10, 6))
plt.plot(df4['timestamp'], df4['value'], color='green', linestyle='-', label='Cisnienie bezwzgledne')
plt.plot(df4_clean['timestamp'], df4_clean['value'], color='black', linestyle='-', label='Cisnienie bezwzgledne')
plt.title('Cisnienie atmosferyczne', fontsize=16)
plt.xlabel('Data', fontsize=12)
plt.ylabel('stopnie C', fontsize=12)
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)

# Add legend
plt.legend(loc='upper left', fontsize=12)

# Save the plot as an image
plt.savefig('/var/www/html/p_rel_week.png', bbox_inches='tight')

# Close the plot
plt.close()




# Close the result proxy and dispose of the engine
result_proxy.close()
engine.dispose()
