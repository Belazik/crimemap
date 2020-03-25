import pymysql


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
            query = "SELECT description FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            cursor.close()

    def add_input(self, data):
        connection = self.connect()
        try:
            query = "INSERT INTO crimes (description) VALUES ('{}');".format(data)
            with connection.cursor() as cursor:
                cursor.execute(query)
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