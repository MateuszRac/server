import os
import re
    
onewiredir = '/sys/bus/w1/devices/'
onewire_devices = os.listdir(onewiredir)


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

        else:
            print("No match found")
