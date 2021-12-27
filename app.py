'''
IMPORTING NECESSARY LIBRARIES
'''

from flask import Flask, render_template
from payers import payers
from expenses import expenses
from moneypot import moneypot

'''
CREATING INSTANCE AND REGISTER FLASK BLUEPRINTS
'''

app = Flask(__name__, template_folder='./')
app.register_blueprint(payers, url_prefix="/Payers")
app.register_blueprint(expenses, url_prefix="/Expenses")
app.register_blueprint(moneypot, url_prefix="/Moneypot")


'''
FOR INDEX PAGE
'''
@app.route('/')
def index():
    return render_template('index.html')

#####
# FOR THE DEVICES ON TABLE SHOWING ONLY TURNED ON DEVICES
#####

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)




