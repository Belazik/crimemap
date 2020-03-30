import json
import dateparser
import datetime
import string
from flask import Flask
from flask import render_template
from flask import request
from dbhelper import DBHelper

app = Flask(__name__)
DBDATA = {"dbhost": "localhost", "dbname": "crimemap", "dbuser": "dbcruser", "dbpassword": "crimepass"}
DB = DBHelper(DBDATA["dbhost"], DBDATA["dbname"], DBDATA["dbuser"], DBDATA["dbpassword"])
categories = ['mugging', 'break-in']
GOOGLE_API = "YOUR API-KEY IT`S HERE"


@app.route('/')
def home(error_message=None):
    try:
        crimes = DB.get_all_inputs()
        crimes = json.dumps(crimes)
    except Exception as e:
        print(e)
        crimes = None
    return render_template("home.html", crimes=crimes, categories=categories, error_message=error_message, api=GOOGLE_API)


# @app.route('/add', methods=['POST'])
# def add():
#     try:
#         data = request.form.get("userinput")
#         DB.add_input(data)
#     except Exception as e:
#         print(e)
#     return home()


@app.route('/submitcrime', methods=["POST"])
def submitcrime():
    category = request.form.get("category")
    if category not in categories:
        return home()
    date = format_date(request.form.get("date"))
    if not date:
        return home("Invalid date. Please use yyyy-mm-dd format")
    try:
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
    except ValueError:
        return home()
    description = sanitize_desc((request.form.get("description")))
    data = {"category": category,
            "date": date,
            "latitude": latitude,
            "longitude": longitude,
            "description": description
            }
    DB.add_input(data)
    return home()


@app.route('/clear')
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
    return home()


def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None

def sanitize_desc(userinput):
    whitelist = string.ascii_letters + string.digits + " !?$.,;:-'()&"
    check = list(filter(lambda x: x in whitelist, userinput))
    return ''.join(check)

if __name__ == '__main__':
    app.run(debug=True)

