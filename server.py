import os
import re
from datetime import datetime
import adafruit_ahtx0
import board


onewiredir = '/sys/bus/w1/devices/'
onewire_devices = os.listdir(onewiredir)


data_array = []


#get 1Wire devices

for device_adress in onewire_devices:
    if device_adress[:2]!='00' and device_adress[:2]!='w1':
        device_file = onewiredir+device_adress+'/w1_slave'

        with open(device_file, 'r') as file:
            file_content = file.read()

        pattern = r't=(\d+)'
        match = re.search(pattern, file_content)
        
        if match:
            
            T = float(match.group(1))/1000
            print(device_adress+'\t'+str(T))

            current_time = datetime.utcnow()
            timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            
            if T > -50 and T<100:
                data_array.append({"variable": device_adress, "points":[[timestamp,T]]})
        else:
            print("No match found")

            
            
try:
    sensor = adafruit_ahtx0.AHTx0(board.I2C())
    current_time = datetime.utcnow()
    timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    data_array.append({"variable": 'AHT20_T', "points":[[timestamp,sensor.temperature]]})
    data_array.append({"variable": 'AHT20_RH', "points":[[timestamp,sensor.relative_humidity]]})
except:
    next

print(data_array)