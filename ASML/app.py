#!/usr/bin/env python
from flask import Flask, render_template, request
from flask import jsonify
from flask_restful import Api, Resource, reqparse
import json
from json import dumps
from datetime import datetime
import importlib
from dbconn import *
import requests

app = Flask(__name__)
api = Api(app)

global id
global createServiceMachineId
global radioselection
global response_content
global params

@app.route("/", methods=['GET'])
def healthcheck():
    return render_template("index.html")

@app.route("/", methods=['POST'])
def get_serviceinputs():
    id = request.form['idForAction']
    radioselection = request.form['ActionRadio']
    

    createServiceName = request.form['nameForCreateService']
    createServiceMachineId = request.form['machineIdForCreateService']
    createServiceStartTime = request.form['startTimeForCreateService']
    createServiceEndTime = request.form['startTimeForCreateService']

    payload = { 'id':id, 'startTime':createServiceStartTime,'endTime':createServiceEndTime,'name':createServiceName, 'machineId':createServiceMachineId}
    #print json.dumps(payload)

    createActionName = request.form['nameForCreateAction']
    createActionStartTime = request.form['startTimeForCreateAction']
    createActionEndTime = request.form['endTimeForCreateAction']
    
    payload2 = { 'id':id, 'startTime':createActionStartTime,'endTime':createActionEndTime,'name':createActionName}
    print json.dumps(payload2)

    updateServiceName = request.form['nameForUpdateService']
    updateServiceMachineId = request.form['machineIdForUpdateService']
    updateServiceStartTime = request.form['startTimeForUpdateService']
    updateServiceEndTime = request.form['endTimeForUpdateService']

    payload3 = { 'id':id, 'startTime':updateServiceName,'endTime':updateServiceMachineId,'name':updateServiceStartTime, 'machineId':updateServiceEndTime}
    print json.dumps(payload3)

    updateActionName = request.form['nameForUpdateAction']
    updateActionStartTime = request.form['startTimeForUpdateAction']
    updateActionEndTime = request.form['endTimeForUpdateAction']

    payload4 = { 'id':id, 'startTime':updateActionStartTime,'endTime':updateActionEndTime,'name':updateActionName}
    print json.dumps(payload3)

    if radioselection == 'readServiceAction':
        #test_service_url(id)
        r = requests.get('http://localhost:5000/GetServiceAction_ActionPlans/id?id='+id)
        return render_template("output.html", check = r.text)

    elif radioselection == 'readAction':
        r = requests.get('http://localhost:5000/GetActionPlan/id?id='+id)
        return render_template("output.html", check = r.text)

    elif radioselection == 'readService':
        r = requests.get('http://localhost:5000/GetServiceAction/id?id='+id)
        return render_template("output.html", check = r.text)

    elif radioselection == 'createService':
        r = requests.put('http://localhost:5000/CreateServiceAction',params=payload , timeout=30, verify=False)
        #print r.text
        return render_template("output.html", check = r.text)      

    elif radioselection == 'createAction':
        r = requests.put('http://localhost:5000/CreateActionPlan',params=payload2 , timeout=30, verify=False)
        return render_template("output.html", check = r.text)    

    elif radioselection == 'updateService':
        r = requests.post('http://localhost:5000/UpdateServiceAction', params= payload3 , timeout=30, verify=False)
        return render_template("output.html", check = r.text)  

    elif radioselection == 'updateAction':
        r = requests.post('http://localhost:5000/UpdateActionPlan', params= payload4 , timeout=30, verify=False)
        return render_template("output.html", check = r.text)   

    elif radioselection == 'deleteService':
        r = requests.delete('http://localhost:5000/DeleteServiceAction/id?id='+id)
        return render_template("output.html", check = r.text)

    elif radioselection == 'deleteAction':
        r = requests.delete('http://localhost:5000/DeleteActionPlan/id?id='+id)
        return render_template("output.html", check = r.text)    

#Read Action Plans with substring as <>
@app.route('/GetServiceAction_ActionPlans/<string:name>',methods=['GET'])
def get_serviceActionsActionPlans(name):
    try:
        #print id    
        name = request.args.get('id')
        print('name:%s' %name)
        cursor.execute("SELECT * FROM testdata.actionplans WHERE id LIKE %s",('%%%s%%' % name))

        data = cursor.fetchone()
        if data == None:
            res="Id not found. Please try again with different Id Status Code:404"
            return res
        columnNames = cursor.description
        dicta = {}
        for(name, value) in zip(columnNames, data):
            dicta[name[0]] = value
            res=json.dumps(dicta)
        return res

    except Exception:
        ex= "Exception Occured"
        return ex

#Read Service Action with <id>
@app.route('/GetServiceAction/<string:name>',methods=['GET'])
def get_serviceActions(name):
    try:
        name = request.args.get('id')
        print('name:%s' %name)
        cursor.execute("SELECT * FROM testdata.serviceactions WHERE id=%s",name)
        data = cursor.fetchone()
        if data == None:
            return "Id not found. Please try again with different Id Status Code:404", 404
        columnNames = cursor.description
        dict = {}
        for(name, value) in zip(columnNames, data):
            dict[name[0]] = value
        return jsonify(dict)

    except Exception:
        return {'Exception Occured'}

#Read Action Plan
@app.route('/GetActionPlan/<string:name>',methods=['GET'])
def get_actionPlans(name):
    try:
        name = request.args.get('id')
        print('name:%s' %name)
        cursor.execute("SELECT * FROM testdata.actionplans WHERE id=%s",name)
        data = cursor.fetchone()
        if data == None:
            return "Id not found. Please try again with different Id Status Code:404", 404
        
        columnNames = cursor.description
        dict = {}
        for(name, value) in zip(columnNames, data):
            dict[name[0]] = value
        return jsonify(dict)

    except Exception:
        return {'Exception Occured'}

#Update Service Action
@app.route('/UpdateServiceAction',methods=['POST'])
def update_serviceAction():
    try:
        name = request.args.get('id')
        print('name:%s' %name)
        m = request.args.get('machineId')
        print ('m:%s' %m)
        na = request.args.get('name')
        print ('na:%s' %na)
        sa = request.args.get('startTime')
        print ('sa:%s' %sa)
        ea = request.args.get('endTime')
        print ('ea:%s' %ea)

        cursor.execute("SELECT * FROM testdata.serviceactions WHERE id=%s",name)
        data = cursor.fetchone()
        print data
        if data == None:
            return "id {} is not in Database".format(name), 404
            # res="id is not in Database Status Code: 404"
            # return render_template("output.html", check = res)            
        else:
            query_two = ("""UPDATE testdata.serviceactions SET machineId = '%s', name='%s', startTime='%s', endTime ='%s' WHERE id = %s"""%(m,na,sa,ea,name))
            cursor.execute(query_two)
            conn.commit()
            return "id {} is updated successfully".format(name), 200
            
    except Exception:
        return "Exception occured. Please check if Id: {} already exists".format(name), 422
       
#UPDATE Action Plan
@app.route('/UpdateActionPlan',methods=['POST'])
def update_actionPlan():
    try:
        name = request.args.get('id')
        print('name:%s' %name)
        m = request.args.get('machineId')
        print ('m:%s' %m)
        na = request.args.get('name')
        print ('na:%s' %na)
        sa = request.args.get('startTime')
        print ('sa:%s' %sa)
        ea = request.args.get('endTime')
        print ('ea:%s' %ea)

        cursor.execute("SELECT * FROM testdata.actionplans WHERE id=%s",name)
        data = cursor.fetchone()
        if data == None:
            return "id {} is not in Database".format(name), 404
            # res="id is not in Database Status Code: 404"
            # return render_template("output.html", check = res)
        else:
            query_two = ("""UPDATE testdata.actionplans SET name='%s', startTime='%s', endTime ='%s' WHERE id = %s"""%(na, sa, ea, name))
            cursor.execute(query_two)
            conn.commit()
            return "id {} is updated successfully".format(name), 200

        
    except Exception:
        return "Exception occured. Please check if Id: {} already exists".format(name), 422
     

#CREATE a new service plan
@app.route('/CreateServiceAction',methods=['PUT'])
def create_servicePlan():
    try:
        name = request.args.get('id')
        print('name:%s' %name)
        m = request.args.get('machineId')
        print ('m:%s' %m)
        na = request.args.get('name')
        print ('na:%s' %na)
        sa = request.args.get('startTime')
        print ('sa:%s' %sa)
        ea = request.args.get('endTime')
        print ('ea:%s' %ea)
        
        cursor.execute("SELECT * FROM testdata.serviceactions WHERE id=%s",name)
        result = cursor.fetchone()
        print result
        if result == None:
            query=("""INSERT INTO testdata.serviceactions (id, machineId, name, startTime, endTime) VALUES (%s,%s,%s,%s,%s)""")
            vals=(name, m,sa,ea,na)
            cursor.execute(query, vals)
            print json.dumps(vals)
            conn.commit()
            conn.close()
            return "Service Action with Id: {} is created successfully".format(name), 200
           
        else:
            return "Id: {} already exists".format(name),422
           
    except Exception:
        return "Exception occured. Please check if Id: {} already exists".format(name), 422
       
#CREATE a new one
@app.route('/CreateActionPlan',methods=['PUT'])
def create_actionPlan():
    try:
        name = request.args.get('id')
        print('name:%s' %name)
        na = request.args.get('name')
        print ('na:%s' %na)
        sa = request.args.get('startTime')
        print ('sa:%s' %sa)
        ea = request.args.get('endTime')
        print ('ea:%s' %ea)

        cursor.execute("SELECT * FROM testdata.actionplans WHERE id=%s",name)
        result = cursor.fetchone()
        if result == None:            
            query=("""INSERT INTO testdata.actionplans (id, name, startTime, endTime) VALUES (%s,%s,%s,%s)""")
            #vals=([name],args["name"],args["startTime"],args["endTime"])
            vals=(name, na, sa, ea,)
            print vals
            cursor.execute(query,vals)
            conn.commit()
            conn.close()
            return "Action Plan with Id: {} is created successfully".format(name), 200
           
        else:
            return "Id: {} already exists".format(name),422
            # res="Id already exists Status Code: 422"
            # return render_template("output.html", check = res)
            
    except Exception:
        return "Exception occured. Please check if Id: {} already exists".format(name), 422 
       
#DELETE Service Action
@app.route('/DeleteServiceAction/<string:name>',methods=['DELETE'])
def delete_serviceAction(name):
    try:
        name = request.args.get('id')
        print('name:%s' %name)
        cursor.execute("SELECT * FROM testdata.serviceactions WHERE id=%s",name)
        data = cursor.fetchone()
        if data == None:
            return "Id is not found in Database", 404
           
        else:
            query = ("DELETE FROM testdata.serviceactions WHERE id = %s")
            values = (name)
            cursor.execute(query,values)
            conn.commit()
            return "1 row deleted successfully"
            # res="1 row(s) deleted successfully Status Code: 200"
            # return render_template("output.html", check = res)
    except Exception:
        return {'Exception Occured'}
        # res="Exception Occured"
        # return render_template("output.html", check = res)

#DELETE Action Plan
@app.route('/DeleteActionPlan/<string:name>',methods=['DELETE'])
def delete_actionPlan(name):
    try:
        name = request.args.get('id')
        print('name:%s' %name)
        cursor.execute("SELECT * FROM testdata.actionplans WHERE id=%s",name)
        data = cursor.fetchone()
        if data == None:
            return "Id is not found in Database", 404
            
        else:
            query = ("DELETE FROM testdata.actionplans WHERE id = %s")
            values = (name)
            cursor.execute(query,values)
            conn.commit()
            return "1 row deleted successfully"
           
    except Exception:
        return {'Exception Occured'}
       

if __name__ == '__main__':
    app.run(debug=True)