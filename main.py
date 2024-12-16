from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


index_name = 'yayin'
documents = []

mongo_client = MongoClient('mongodb://localhost:27017/')
collection = mongo_client.yazlab.deneme

@app.route('/yayin', methods=['GET'])
def get_yayin():
    try:
        result = list(collection.find())
        for doc in result:
            doc['_id'] = str(doc['_id'])

        return jsonify(result)
    except Exception as e:
        return f"Error: {e}"

@app.route('/yayin/<param>/<order>', methods=['GET'])
def get_tarih(param,order):
    data = list(collection.find({'Başlık': {'$regex': param, '$options': 'i'}}))
    
    for entry in data:
        entry['Çıkış Tarihi'] = int(entry['Çıkış Tarihi'])
        entry['_id'] = str(entry['_id'])
    if order == 'asc':
        ordered_data = sorted(data, key=lambda x: x['Çıkış Tarihi'])
    else:
        ordered_data = sorted(data, key=lambda x: x['Çıkış Tarihi'],reverse=True)    



    return jsonify(ordered_data)
@app.route('/yayinas/<param>/<order>', methods=['GET'])
def get_alinti(param,order):
    data = list(collection.find({'Başlık': {'$regex': param, '$options': 'i'}}))
    
    for entry in data:
        entry['Alıntılar'] = int(entry['Alıntılar'])
        entry['_id'] = str(entry['_id'])

    
    if order == 'asc':
        ordered_data = sorted(data, key=lambda x: x['Alıntılar'])
    else:
        ordered_data = sorted(data, key=lambda x: x['Alıntılar'],reverse=True)    
        
    return jsonify(ordered_data)    


if __name__ == '__main__':
    app.run(port=3005)
