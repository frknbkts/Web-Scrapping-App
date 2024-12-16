from elasticsearch import Elasticsearch
import json

def read_json_file(file_path):
    with open(file_path, 'r',encoding='utf-8') as file:
        data = json.load(file)
    return data

def upload_to_elasticsearch(json_data, index_name, host='localhost', port=9200):
    es = Elasticsearch([{'host': host, 'port': port,'scheme':'http'}])

    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)

    for document in json_data:
        es.index(index=index_name, body=document)

    print(f"Data uploaded to the '{index_name}' index successfully.")


json_file_path = 'output.json' 
es_index_name = 'makaleler2'  

json_data = read_json_file(json_file_path)
upload_to_elasticsearch(json_data, es_index_name)    


