import os
import re
from datetime import datetime
import adafruit_ahtx0
import board
import requests


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
    next

    
    
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


























