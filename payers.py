'''
IMPORTING NECESSARY LIBRARIES
'''

from flask import Blueprint, render_template, redirect, request
import json

payers = Blueprint("payers", __name__, static_folder="static", template_folder="templates")


'''
CODE FOR WHEN LOADING THE EXPENSES PAGE
'''
@payers.route('/')
def list1():
    with open('payers.json', 'r+') as p:
        data = p.read()

    records = json.loads(data)
    datalist =[]
    for i in records['names']:
        name = i['name']
        dependent = i['Dependents']
        Expenses = i['Total Expenses']
        datalist.append([name,dependent,Expenses])

    headings = ("Name","Number of dependents","Amount paid")



    return render_template('payers.html', headings=headings, data=datalist)


@payers.route('/', methods=['POST'])
def my_form_post():

    payername = request.form.get('Payer')
    dependentsnew = request.form.get('Dependent')

    with open('payers.json', 'r+') as p:
        data = p.read()

    records = json.loads(data)

    records['names'].append({"name": payername, "Dependents": dependentsnew, "Total Expenses": 0})

    with open('payers.json', 'w') as p:
        data = json.dump(records, p)



    return list1()
