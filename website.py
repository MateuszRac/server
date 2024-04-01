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
        df = dataframe.iloc[filtered_indices]
    return df.reset_index(drop=True)




def plot_with_gaps(df, color, label):
    breaks = []
    prev_time = None
    for index, row in df.iterrows():
        if prev_time is not None:
            time_diff = (row['timestamp'] - prev_time).total_seconds()
            if time_diff > 600:  # 10 minute gap
                breaks.append(index)
        prev_time = row['timestamp']

    for i, break_index in enumerate(breaks):
        if i == 0:
            plt.plot(df.iloc[:break_index]['timestamp'], df.iloc[:break_index]['value'], color=color, linestyle='-', markersize=5, label=label)
        else:
            plt.plot(df.iloc[breaks[i-1]+1:break_index]['timestamp'], df.iloc[breaks[i-1]+1:break_index]['value'], color=color, linestyle='-', markersize=5)

    if len(breaks) > 0:
        plt.plot(df.iloc[breaks[-1]+1:]['timestamp'], df.iloc[breaks[-1]+1:]['value'], color=color, linestyle='-', markersize=5)
    else:
        plt.plot(df['timestamp'], df['value'], color=color, linestyle='-', markersize=5, label=label)













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
df1 = remove_outliers_with_window(df1,'value',window_size=10, threshold=1.5)



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
df2 = remove_outliers_with_window(df2,'value',window_size=10, threshold=1.5)
df2['value'] = df2['value'].astype(float)




#ATH20
# Build the select query with the conditions
query = select([meteo_table.c.timestamp, meteo_table.c.value]).where(
    (meteo_table.c.timestamp >= seven_days_ago) &
    (meteo_table.c.variable == 'AHT20_T')
)

# Execute the query and fetch the results
result_proxy = engine.execute(query)
result_set = result_proxy.fetchall()

# Convert the result set into a Pandas DataFrame
df_aht20_t = pd.DataFrame(result_set, columns=['timestamp', 'value'])
df_aht20_t = remove_outliers_with_window(df_aht20_t,'value',window_size=10, threshold=1.5)
df_aht20_t['value'] = df_aht20_t['value'].astype(float)





# Create a plot with custom styling
plt.figure(figsize=(10, 6))


plot_with_gaps(df1, color='red', label='TP krotki')
plot_with_gaps(df2, color='blue', label='TP dlugi')
plot_with_gaps(df_aht20_t, color='black', label='TP AHT20')


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
#df3 = remove_outliers_with_window(df3,'value',window_size=10, threshold=3.5)



# Create a plot with custom styling
plt.figure(figsize=(10, 6))

plot_with_gaps(df3, color='red', label='Temperatura na piecu')

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
df4 = remove_outliers_with_window(df4,'value',window_size=10, threshold=1.5)



# Create a plot with custom styling
plt.figure(figsize=(10, 6))
#plt.plot(df4['timestamp'], df4['value'], color='green', linestyle='-', label='Cisnienie bezwzgledne')
plot_with_gaps(df4, color='red', label='Cisnienie bezwzgledne')

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




#html table




file_path = '/var/www/html/template.html'
with open(file_path, 'r') as file:
    file_content = file.read()


df1_row = df1.loc[df1['timestamp'].idxmax()]
file_content = file_content.replace('_T1_DATE_', df1_row.timestamp.strftime('%Y-%m-%d %H:%M'))
file_content = file_content.replace('_T1_', str(df1_row.value))


df2_row = df2.loc[df2['timestamp'].idxmax()]
file_content = file_content.replace('_T2_DATE_', df2_row.timestamp.strftime('%Y-%m-%d %H:%M'))
file_content = file_content.replace('_T2_', str(df2_row.value))


df3_row = df3.loc[df3['timestamp'].idxmax()]
file_content = file_content.replace('_TPIEC_DATE_', df3_row.timestamp.strftime('%Y-%m-%d %H:%M'))
file_content = file_content.replace('_TPIEC_', str(df3_row.value))


df4_row = df4.loc[df4['timestamp'].idxmax()]
file_content = file_content.replace('_PABS_DATE_', df4_row.timestamp.strftime('%Y-%m-%d %H:%M'))
file_content = file_content.replace('_PABS_', str(df4_row.value))






# Write the modified content back to the file
with open('/var/www/html/index.html', 'w') as file:
    file.write(file_content)



