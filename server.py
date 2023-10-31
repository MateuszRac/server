import os
import re
    
onewiredir = '/sys/bus/w1/devices/'
onewire_devices = os.listdir(onewiredir)

print(onewire_devices)

for device_adress in onewire_devices:
    if device_adress[:2]!='00' and device_adress[:2]!='w1':
        device_file = onewiredir+device_adress+'/w1_slave'

        with open(device_file, 'r') as file:
            file_content = file.read()

        pattern = r't=(\d+)'
        matches = re.findall(pattern, file_content)
        T = [float(match) for match in matches]/1000
        print(device_adress+'\t'+str(T))