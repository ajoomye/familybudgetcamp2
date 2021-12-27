'''
IMPORTING NECESSARY LIBRARIES
'''

from flask import Blueprint, render_template, redirect, request
import json
from datetime import date as datemodule

expenses = Blueprint("expenses", __name__, static_folder="static", template_folder="templates")


'''
CODE FOR WHEN LOADING THE EXPENSES PAGE
'''
@expenses.route('/')
def list1():
    with open('expenses.json', 'r+') as p:
        data = p.read()

    records = json.loads(data)
    datalist=[]
    for i in records['expenses']:
        date = i['date']
        Expense = i['Expense']
        amount = i['Total amount']
        payer = i['Payer']
        datalist.append([date,Expense,amount,payer])

    headings = ("Date","Expense", "Amount", "Payer")

    with open('payers.json', 'r+') as p:
        data = p.read()

    records = json.loads(data)
    payers = []
    for i in range(len(records['names'])):
        namelist = records['names'][i]
        payers.append(namelist['name'])


    return render_template('expenses.html', headings=headings, data=datalist, payers=payers)


@expenses.route('/', methods=['POST'])
def my_form_post():
    datetoday = str(datemodule.today())
    expensenew = request.form.get('expense')
    amountnew = request.form.get('amount')
    payernew = request.form.get('payer')
    print(payernew)

    amountnew=int(amountnew)

    with open('expenses.json', 'r+') as p:
        data = p.read()

    records = json.loads(data)

    records['expenses'].append({"date": datetoday, "Expense": expensenew, "Total amount": amountnew, "Payer": payernew})

    with open('expenses.json', 'w') as p:
        data = json.dump(records, p)

    with open('payers.json', 'r+') as p:
        data = p.read()

    records = json.loads(data)

    for i in records['names']:
        if i['name'] == payernew:
            i['Total Expenses'] += amountnew

    with open('payers.json', 'w') as p:
        data = json.dump(records, p)

    return list1()
