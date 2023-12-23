import os
import re
from datetime import datetime
import adafruit_ahtx0
import board
import requests
from dotenv import load_dotenv

load_dotenv()



onewiredir = '/sys/bus/w1/devices/'
onewire_devices = os.listdir(onewiredir)


data_array = []


#get 1Wire devices

for device_adress in onewire_devices:
    try:
        if device_adress[:2]!='00' and device_adress[:2]!='w1':
            device_file = onewiredir+device_adress+'/w1_slave'

            with open(device_file, 'r') as file:
                file_content = file.read()

            pattern = r't=(\d+)'
            match = re.search(pattern, file_content)

            if match:

                T = float(match.group(1))/1000
                #print(device_adress+'\t'+str(T))

                current_time = datetime.utcnow()
                timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")

                if T > -50 and T<100:
                    data_array.append({"variable": device_adress, "points":[[timestamp,T]]})
                    upload_to_db(db_config,device_adress,timestamp,T)
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
except:
    print('AHT20 error')

    

    
    
    
    
#BMP280 data

from bmp280 import BMP280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


# Initialise the BMP280
try:
    bus = SMBus(1)
    bmp280 = BMP280(i2c_dev=bus)

    current_time = datetime.utcnow()
    timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    data_array.append({"variable": "BMP280_T", "points":[[timestamp,round(bmp280.get_temperature(),2)]]})
    data_array.append({"variable": "BMP280_P", "points":[[timestamp,round(bmp280.get_pressure(),2)]]})
except:
    print('BMP280 error')
    
    
    
    
    
    
    
#IR

from mlx90614 import MLX90614

try:
    bus = SMBus(1)
    sensor = MLX90614(bus, address=0x5A)
    
    data_array.append({"variable": "IR_AMB", "points":[[timestamp,round(sensor.get_amb_temp(),2)]]})
    data_array.append({"variable": "IR_OBJ", "points":[[timestamp,round(sensor.get_obj_temp(),2)]]})
    
    bus.close()
except:
    print('IR error')


    
    
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





wurl = 'http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?'


current_time = datetime.utcnow()
timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

params = {'ID': os.getenv('WU_ID'), 'PASSWORD': os.getenv('WU_PASS'), 'dateutc':timestamp}



t_pressure = 2.0
b_height = os.getenv('B_HEIGHT')

for var in data_array:
    if var['variable'] == 'BMP280_P':
        params['baromin'] = mslp(var['points'][0][1],t_pressure,b_height)/33.86389

print(wurl + parse.urlencode(params))

x = requests.get(wurl + parse.urlencode(params))
print(x.status_code)

















