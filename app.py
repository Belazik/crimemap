from flask import Flask
from flask import render_template
from flask import request
from dbhelper import DBHelper

app = Flask(__name__)
DBDATA = {"dbhost": "localhost", "dbname": "crimemap", "dbuser": "dbcruser", "dbpassword": "crimepass"}
DB = DBHelper(DBDATA["dbhost"], DBDATA["dbname"], DBDATA["dbuser"], DBDATA["dbpassword"])

@app.route('/')
def home():
    try:
        data = DB.get_all_inputs()
    except Exception as e:
        print(e)
        data = None
    return render_template("home.html", data=data)


@app.route('/add', methods=['POST'])
def add():
    try:
        data = request.form.get("userinput")
        DB.add_input(data)
    except Exception as e:
        print(e)
    return home()

@app.route('/clear')
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
    return home()


if __name__ == '__main__':
    app.run(debug=True)

