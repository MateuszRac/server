import os
import re
from datetime import datetime
import adafruit_ahtx0
import board
import requests
from dotenv import load_dotenv
import statistics
import time
import pandas as pd
from sqlalchemy import create_engine
from smbus2 import SMBus

load_dotenv()




def calculate_dewpoint(temp_celsius, relative_humidity):
    """
    Calculate dew point in Celsius from temperature in Celsius and relative humidity.

    Args:
        temp_celsius (float): Temperature in Celsius.
        relative_humidity (float): Relative humidity (in percentage).

    Returns:
        float: Dew point temperature in Celsius.
    """
    # Magnus-Tetens formula constants
    
    a = 6.1121
    b = 18.678
    c = 257.14
    d = 234.5
    
    
    l_t_rh = np.log((relative_humidity/100)*np.exp((b-temp_celsius/d)*(temp_celsius/(c+temp_celsius))))
    
    dew_point = (c*l_t_rh)/(b-l_t_rh)

    return dew_point





onewiredir = '/sys/bus/w1/devices/'
onewire_devices = os.listdir(onewiredir)


data_array = []

df = pd.DataFrame(columns=['variable','timestamp','value'])


#get 1Wire devices

for device_adress in onewire_devices:
    try:
        if device_adress[:2]!='00' and device_adress[:2]!='w1':
            device_file = onewiredir+device_adress+'/w1_slave'

            with open(device_file, 'r') as file:
                file_content = file.read()

            pattern = r't=((-?)\d+)'
            match = re.search(pattern, file_content)

            if match:

                T = float(match.group(1))/1000
                #print(device_adress+'\t'+str(T))

                current_time = datetime.utcnow()
                timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")

                if T<=100:
                    data_array.append({"variable": device_adress, "points":[[timestamp,T]]})
                    df.loc[len(df)] = [device_adress,current_time,T]
            else:
                print("No match found")
    except:
        next
            
            
try:
    sensor = adafruit_ahtx0.AHTx0(board.I2C())
    current_time = datetime.utcnow()
    timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    data_array.append({"variable": "AHT20_T", "points":[[timestamp,round(sensor.temperature,2)]]})
    data_array.append({"variable": "AHT20_RH", "points":[[timestamp,round(sensor.relative_humidity,2)]]})
    
    df.loc[len(df)] = ['AHT20_T',current_time,round(sensor.temperature,2)]
    df.loc[len(df)] = ["AHT20_RH",current_time,round(sensor.relative_humidity,2)]
except:
    print('AHT20 error')

    

    
import board
import adafruit_bmp280

# Initialise the BMP280
try:
    
    i2c = board.I2C()
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
    bmp280.sea_level_pressure = 1013.25
    
    current_time = datetime.utcnow()
    timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    data_array.append({"variable": "BMP280_T", "points":[[timestamp,round(bmp280.temperature,2)]]})
    data_array.append({"variable": "BMP280_P", "points":[[timestamp,round(bmp280.pressure,2)]]})
    
    df.loc[len(df)] = ["BMP280_T",current_time,round(bmp280.temperature,2)]
    df.loc[len(df)] = ["BMP280_P",current_time,round(bmp280.pressure,2)]
    
except:
    print('BMP280 error')
    
    
    
    
    
    
    
#IR

from mlx90614 import MLX90614

t_obj_list = []
for i in range(0,10):
    try:
        bus = SMBus(1)
        sensor = MLX90614(bus, address=0x5A)
        
        t_obj = sensor.get_obj_temp()
        t_obj_list.append(t_obj)
        
        bus.close()
        time.sleep(1)
    except:
        print('IR error')
        break
    
if len(t_obj_list) >= 4:
    data_array.append({"variable": "IR_OBJ", "points":[[timestamp,round(statistics.median(t_obj_list),2)]]})
    df.loc[len(df)] = ["IR_OBJ",current_time,round(statistics.median(t_obj_list),2)]

    
    
try:
    print(df)
    engine = create_engine('mysql+pymysql://pi:raspberry@localhost:3306/db')
    df.to_sql('meteo', con=engine, if_exists='append', index=False)
    
except Exception as e:
    print(e)
    
    
url = "http://popruntheworld.pl/raspberry/rpi_python.php"  # Replace with the actual URL
    
    
# Set the headers to specify that you are sending JSON data
headers = {
    "Content-Type": "application/json"
}

# Make the POST request
response = requests.post(url, data=str(data_array), headers=headers)

# Check the response
if response.status_code == 200:
    print("POST request was successful!")
    print("Response content:", response.text)
else:
    print("POST request failed with status code:", response.status_code)
    print("Response content:", response.text)
    
    
print(data_array)




#wunderground
from urllib import parse
import numpy as np

def mslp(P,T,H):
    return P*np.exp(2.30259*H/(18400.0*(1+0.003667*(T+0.0025*H))))

def c_to_f(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit



wurl = 'http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?'


current_time = datetime.utcnow()
timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

params = {'ID': os.getenv('WU_ID'), 'PASSWORD': os.getenv('WU_PASS'), 'dateutc':timestamp}



t_pressure = 2.0

b_height = os.getenv('B_HEIGHT')

AHT20_T, AHT20_RH = None, None

for var in data_array:
        
    if var['variable']== '28-3ce104570b5f':
        params['soiltempf'] = c_to_f(var['points'][0][1])
        t_pressure = var['points'][0][1]
        
    if var['variable']== '28-3c6204572bfc':
        params['tempf'] = c_to_f(var['points'][0][1])
        t_pressure = var['points'][0][1]
        
    if var['variable'] == 'BMP280_P':
        params['baromin'] = mslp(var['points'][0][1],t_pressure,float(b_height))/33.86389
        
    if var['variable']== 'AHT20_T':
        AHT20_T = var['points'][0][1]
        
    if var['variable']== 'AHT20_RH':
        AHT20_RH = var['points'][0][1]

        
if AHT20_T is not None and AHT20_RH is not None:
    dewpoint_f = c_to_f(calculate_dewpoint(AHT20_T, AHT20_RH))
    params['dewptf'] = dewpoint_f
        
print(wurl + parse.urlencode(params))

x = requests.get(wurl + parse.urlencode(params))
print(x.status_code)

















