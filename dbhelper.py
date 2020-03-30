import pymysql
import datetime

class DBHelper:

    def __init__(self, dbhost, dbname, dbuser, dbpassword):
        self.dbpassword = dbpassword
        self.dbuser = dbuser
        self.dbname = dbname
        self.dbhost = dbhost


    def connect(self):
        return pymysql.connect(host=self.dbhost,
                               user=self.dbuser,
                               password=self.dbpassword,
                               db=self.dbname)

    def get_all_inputs(self):
        connection = self.connect()
        try:
            query = "SELECT latitude, longitude, date, category, description FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                crimes = []
                for rowdb in cursor:
                    data = {'latitude': rowdb[0],
                            'longitude': rowdb[1],
                            'date': datetime.datetime.strftime(rowdb[2], '%Y-%m-%d'),
                            'category': rowdb[3],
                            'description': rowdb[4]}
                    crimes.append(data)
                return crimes
        finally:
            cursor.close()

    def add_input(self, data):
        connection = self.connect()
        try:
            query = "INSERT INTO crimes (category, date, latitude, longitude, description) VALUES (%s, %s, %s, %s, %s);"
            with connection.cursor() as cursor:
                cursor.execute(query, (data["category"], data["date"],
                               data["latitude"], data["longitude"], data["description"]))
                connection.commit()
        finally:
            connection.close()


    def clear_all(self):
        connection = self.connect()
        try:
            query = 'DELETE FROM crimes;'
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        finally:
            connection.close()
