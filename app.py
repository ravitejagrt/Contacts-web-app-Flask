import json
from flask import Flask, jsonify, render_template, request, Response
from flask_restful import Resource, Api
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app) ## To allow direct AJAX calls

# with open('Empires.JSON') as json_data:
#     d = json.load(json_data)
#     list_of_empires = []
#     for data in d['empires']:
#     	list_of_empires.append(data)
#
# with open('Army.JSON') as army_data:
# 	a = json.load(army_data)
# 	list_of_armies = []
# 	for army in a['armies']:
# 		list_of_armies.append(army)
# 	print("list_of_armies: ", list_of_armies)

@app.route('/', methods =['GET'])
def home():
	return render_template("index.html")

@app.route('/contacts', methods=['GET'])
def allContacts():
    r = requests.get('http://127.0.0.1:8081/api/identification')
    print("response from r is ", r.json())
    employees = [emp for emp in r.json()]
    return render_template("index.html", list_data=employees)

if __name__ == '__main__':
	 app.run(host='0.0.0.0', port=5000)