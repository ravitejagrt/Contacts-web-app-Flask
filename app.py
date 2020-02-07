import json
import flask
from flask import Flask, jsonify, render_template, request, Response, flash
from flask_restful import Resource, Api
from flask_cors import CORS
import requests
import configparser

config = configparser.RawConfigParser()
config.read('ms3-properties.properties')

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
	return render_template("employees.html")

# @app.route('/employees', methods=['GET'])
# def allContacts():
#     r = requests.get('http://127.0.0.1:8081/api/identification')
#     print("response from r is ", r.json())
#     employees = [emp for emp in r.json()]
#     return render_template("employees.html", list_data=employees)

@app.route('/employee', methods=['GET', 'POST'])
def employee():
    if flask.request.method == 'POST':
        print("request form : ", request.form)
        identificationData = {}
        identificationData["firstName"] = str(request.form['firstName'])
        identificationData["lastName"] = str(request.form['lastName'])
        identificationData["title"] = str(request.form['title'])
        identificationData["gender"] = str(request.form['gender'])
        identificationData["dob"] = str(request.form['dob'])

        addressData = {}
        addressData["type"] = str(request.form['addresstype'])
        addressData["number"] = str(request.form['housenumber'])
        print("housenumber : ", addressData["number"])
        print("type : ", type(addressData["number"]))
        addressData["number"] = int(addressData["number"])
        addressData["street"] = str(request.form['street'])

        addressData["unit"] = str(request.form['unit'])
        addressData["city"] = str(request.form['city'])
        addressData["state"] = str(request.form['state'])
        addressData["zipcode"] = str(request.form['zipcode'])

        emailData = {}
        emailData["type"] = str("email")
        emailData["value"] = str(request.form['email'])
        if (str(request.form['preferred']) == "Email"):
            emailData["preferred"] = True
        else:
            emailData["preferred"] = False
        phoneData = {}
        phoneData["type"] = str("phone")
        phoneData["value"] = str(request.form['phone'])
        if (str(request.form['preferred']) == "Email"):
            phoneData["preferred"] = False
        else:
            phoneData["preferred"] = True

        empData = {}
        empData["identification"] = identificationData
        empData["addresses"] = [addressData]
        empData["communications"] = [emailData, phoneData]
        print("employee data : ", empData)
        #json_data = json.dumps(data)
        response = requests.post((config['ms3.contacts.web.api']['url'] + config['resource']['employee']), json=empData)
        # print("response::: ", response)
        # print("json response :: ", response.json())
        empId = response.json()["empId"]
        return flask.redirect("/employee/" + str(empId))
    if flask.request.method == 'GET':
        response = requests.get((config['ms3.contacts.web.api']['url'] + config['resource']['identification']))
        print("response::: ", response)
        employees = [emp for emp in response.json()]
        return render_template("employees.html", list_data=employees)

@app.route('/newEmployee', methods=['GET'])
def newEmployee():
    return render_template("create-employee.html")

@app.route('/employee/<string:empId>', methods=['GET'])
def getEmployee(empId):
    empData = requests.get((config['ms3.contacts.web.api']['url'] + config['resource']['identification'] + "/" + empId))
    print("empdata response : ", empData)
    print("empdata : ", empData.json())

    addressData = requests.get((config['ms3.contacts.web.api']['url'] + config['resource']['identification'] + "/" + empId + config['resource']['address']))
    print("addressData response : ", addressData)
    print("addressData : ", addressData.json())

    communicationData = requests.get((config['ms3.contacts.web.api']['url'] + config['resource']['identification'] + "/" + empId + config['resource']['communication']))
    print("communicationData response : ", communicationData)
    print("communicationData : ", communicationData.json())

    return render_template("view-employee.html", emp_data=empData.json(), address_data=addressData.json(), comm_data=communicationData.json())

@app.route('/employee/<string:empId>/modify', methods=['GET'])
def modifyEmployee(empId):
    empData = requests.get((config['ms3.contacts.web.api']['url'] + config['resource']['identification'] + "/" + empId))
    return render_template("modify-employee.html", emp_data=empData.json())

@app.route('/employee/<string:empId>/addAddress', methods=['GET'])
def newAddress(empId):
    return render_template("add-address.html", empId=empId)

@app.route('/employee/<string:empId>/address', methods=['POST'])
def addAddress(empId):
    if flask.request.method == 'POST':
        data = {}
        data["type"] = str(request.form['type'])
        data["number"] = str(request.form['number'])
        data["street"] = str(request.form['street'])
        data["unit"] = str(request.form['unit'])
        data["city"] = str(request.form['city'])
        data["state"] = str(request.form['state'])
        data["zipcode"] = str(request.form['zipcode'])
        json_data = data
        #json_data = json.dumps(data)
        response = requests.post((config['ms3.contacts.web.api']['url'] + config['resource']['identification'] + "/" + empId + config['resource']['address']), json=json_data)
        print("response::: ", response)
        return flask.redirect("/employee/" + empId)

@app.route('/modifyAddress/<empId>/<addressId>', methods=['GET'])
def modifyAddress(empId, addressId):
    addressData = requests.get((config['ms3.contacts.web.api']['url'] + config['resource']['identification'] + "/" + empId + config['resource']['address']) + "/" + addressId)
    # print("addressData response : ", addressData)
    # print("addressData : ", addressData.json())
    return render_template("modify-address.html", empId=empId, address_data=addressData.json())

@app.route('/updateAddress/<empId>/<addressId>', methods=['POST'])
def updateAddress(empId, addressId):
    if flask.request.method == 'POST':
        data = {}
        data["empId"] = int(empId)
        data["addressId"] = int(addressId)
        data["type"] = str(request.form['addresstype'])
        data["number"] = int(request.form['housenumber'])
        data["street"] = str(request.form['street'])
        data["unit"] = str(request.form['unit'])
        data["city"] = str(request.form['city'])
        data["state"] = str(request.form['state'])
        data["zipcode"] = str(request.form['zipcode'])
        json_data = data
        #json_data = json.dumps(data)
        response = requests.put((config['ms3.contacts.web.api']['url'] + config['resource']['identification'] + "/"
                                  + empId + config['resource']['address'] + "/" + addressId), json=json_data)
        print("response::: ", response)
        return flask.redirect("/employee/" + empId)

@app.route('/deleteAddress/<empId>/<addressId>', methods=['GET'])
def deleteAddress(empId, addressId):
    response = requests.delete((config['ms3.contacts.web.api']['url'] + config['resource']['identification'] + "/" + empId + config['resource']['address'] + "/" + addressId))
    return flask.redirect("/employee/" + empId)

@app.route('/employee/<string:empId>/addCommunication', methods=['GET'])
def newCommunication(empId):
    return render_template("add-address.html", empId=empId)

@app.route('/employee/<string:empId>/communication', methods=['POST'])
def addCommunication(empId):
    if flask.request.method == 'POST':
        data = {}
        data["type"] = str(request.form['type'])
        data["value"] = str(request.form['value'])
        data["preferred"] = str(request.form['preferred'])
        json_data = data
        #json_data = json.dumps(data)
        response = requests.post((config['ms3.contacts.web.api']['url'] + config['resource']['identification'] + "/" + empId + config['resource']['address']), json=json_data)
        print("response::: ", response)
        return flask.redirect("/employee/" + empId)

@app.route('/modifyCommunication/<empId>/<communicationId>', methods=['GET'])
def modifyCommunication(empId, communicationId):
    communicationData = requests.get((config['ms3.contacts.web.api']['url'] + config['resource']['identification'] + "/" + empId + config['resource']['communication']) + "/" + communicationId)
    # print("addressData response : ", addressData)
    # print("addressData : ", addressData.json())
    return render_template("modify-communication.html", empId=empId, communication_data=communicationData.json())

@app.route('/updateCommunication/<empId>/<communicationId>', methods=['POST'])
def updateCommunication(empId, communicationId):
    if flask.request.method == 'POST':
        data = {}
        # data["empId"] = int(empId)
        # data["communicationId"] = int(communicationId)
        data["type"] = str(request.form['communicationtype'])
        data["value"] = str(request.form['value'])
        print("request.form['preferred'] : ", str(request.form['preferred']))
        if (str(request.form['preferred']) == "true"):
            data["preferred"] = True
        else:
            data["preferred"] = False

        json_data = data
        #json_data = json.dumps(data)
        response = requests.put((config['ms3.contacts.web.api']['url'] + config['resource']['identification'] + "/" + empId + config['resource']['communication'] + "/" + communicationId), json=json_data)
        print("response::: ", response)
        return flask.redirect("/employee/" + empId)

@app.route('/deleteCommunication/<empId>/<communicationId>', methods=['GET'])
def deleteCommunication(empId, communicationId):
    response = requests.delete((config['ms3.contacts.web.api']['url'] + config['resource']['identification'] + "/" + empId + config['resource']['communication'] + "/" + communicationId))
    return flask.redirect("/employee/" + empId)

if __name__ == '__main__':
	 app.run(host='0.0.0.0', port=5000)