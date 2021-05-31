#!/usr/bin/python3

import cgi
import json

form = cgi.FieldStorage()
humThreshold = int(form.getvalue('humThreshold'))
allowingOfAUser = form.getvalue('allowingOfAUser') == 'true'


file_path = '/var/www/html/waterSetting.json'
json_data = {}


with open(file_path, 'r') as json_file:
    json_data = json.load(json_file)
    json_data["humThreshold"] = humThreshold
    json_data["allowingOfAUser"] = allowingOfAUser
    
with open(file_path, 'w') as outfile:
    json.dump(json_data, outfile, indent='\t')

print('Content-type: text/plain')
print()
print(f'humThreshold:{humThreshold}')
print(f'allowingOfAUser:{allowingOfAUser}')
print(json_data)
