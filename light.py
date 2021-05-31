#!/usr/bin/python3

import cgi
import json

form = cgi.FieldStorage()

goalLux = int(form.getvalue('goalLux'))
chlorophyll = str(form.getvalue('chlorophyll'))
allowingOfAUser = form.getvalue('allowingOfAUser') == 'true'


file_path = '/var/www/html/lightSetting.json'
json_data = {}


with open(file_path, 'r') as json_file:
    json_data = json.load(json_file)
    json_data["goalLux"] = goalLux
    json_data["chlorophyll"] = chlorophyll
    json_data["allowingOfAUser"] = allowingOfAUser
 
with open(file_path, 'w') as outfile:
    json.dump(json_data, outfile, indent='\t')

print('Content-type: text/plain')
print()
print(f'goalLux:{goalLux}')
print(f'chlorophyll:{chlorophyll}')
print(f'allowingOfAUser:{allowingOfAUser}')
print(json_data)
