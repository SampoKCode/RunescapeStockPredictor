# For manually updating item catalogue

import json

with open("mapping.json", "r") as file:
    data = json.load(file)

id_name = {}

for item in data:
    id_name[item.get("id")] = (item.get("name"),item.get("limit"))

with open("name_limit_list.json","w") as output_file:
    json.dump(id_name,output_file,indent=4)
    print("succesfully updated name_limit_list.json")