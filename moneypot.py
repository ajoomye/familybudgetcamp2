'''
IMPORTING NECESSARY LIBRARIES
'''

from flask import Blueprint, render_template, redirect, request, Flask
import json


moneypot = Blueprint("moneypot", __name__, static_folder="static", template_folder="templates")


'''
GETTING DETAILS FOR SET SCHEDULE LIST TABLE
'''
@moneypot.route('/')
def list1():
    totalspent = 0
    with open('expenses.json', 'r+') as p:
        data = p.read()

    records = json.loads(data)

    for i in records['expenses']:
        totalspent += float(i['Total amount'])


    with open('payers.json', 'r+') as p:
        data = p.read()

    recordspayer = json.loads(data)

    totaldependents = 0

    for i in recordspayer['names']:
        name = i['name']
        dependent = i['Dependents']
        Expenses = i['Total Expenses']

        totaldependents += int(dependent)

    costperperson = round((totalspent / totaldependents),2)

    costperpayers = []

    headings = ("Name",  "Share of cost", "Money Spent",  "Money owed")
    toreceive = []
    tosend = []
    for i in recordspayer['names']:
        name = i['name']
        dependent = int(i['Dependents'])
        payercost = round((costperperson * dependent),2)
        Expenses = i['Total Expenses']
        moneyowed = payercost - Expenses
        moneyowed = round(moneyowed, 2)
        if moneyowed < 0:
            toreceive.append([name, (0 - moneyowed)])
        if moneyowed >= 0:
            tosend.append([name, moneyowed])
        costsummary = [name, payercost,  Expenses, moneyowed]
        costperpayers.append(costsummary)

    messages = []
    for i in range(len(toreceive)):
        for j in range(len(tosend)):
            if tosend[j][1] <= toreceive[i][1]:
                toreceive[i][1] -= tosend[j][1]
                if tosend[j][1] != 0:
                    message = f'{tosend[j][0]} to send {round(tosend[j][1],2)} to {toreceive[i][0]}'
                    messages.append(message)
                tosend[j][1] = 0
            elif tosend[j][1] > toreceive[i][1]:
                tosend[j][1] -= toreceive[i][1]
                if toreceive[i][1] != 0:
                    message = f'{tosend[j][0]} to send {round(toreceive[i][1],2)} to {toreceive[i][0]}'
                    messages.append(message)
                toreceive[i][1] = 0



    return render_template('moneypot.html', headings=headings, data=costperpayers, messages = messages, costperperson = costperperson,
                           totalspent=totalspent)
