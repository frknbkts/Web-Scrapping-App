import json

def reformat_ids(json_data):
    for document in json_data:
        if 'id' in document and isinstance(document['id'], dict) and '$oid' in document['id']:
            document['id'] = document['id']['$oid']
    return json_data

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def write_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

json_file_path = 'yazlab.deneme2.json'  

json_data = read_json_file(json_file_path)
updated_data = reformat_ids(json_data)
write_json_file(json_file_path, updated_data)


