import json
import os
config="app.conf.json"

def parse_folder_with_json_files():
    f = open(config)
    json_files_list=[]
    data = json.load(f)
    folder_name= data["input_folder"]
    for filename in os.listdir(folder_name):
        f = os.path.join(folder_name, filename)
        # checking if it is a file
        if os.path.isfile(f):
            if ".json" in f:
                json_files_list.append(f)
    
    return json_files_list




