import json

# a json File I/O test

car_group = dict()

K5 = dict()
K5["price"] = "5000"
K5["year"] = "2015"

car_group["K5"]  = K5

Avante = dict()
Avante["price"] = "3000"
Avante["year"] = "2014"

car_group["Avante"] = Avante

with open('/root/Desktop/Capstone Design/banana-storage/ServerFiles/a.json', 'w', encoding='utf-8') as file:
    json.dump(car_group, file, indent="\t")


# Print the saved file

with open('/root/Desktop/Capstone Design/banana-storage/ServerFiles/a.json', 'r', encoding='utf-8') as read_file:
    json_data = json.load(read_file)

print(json.dumps(json_data, indent="\t"))
    
          
