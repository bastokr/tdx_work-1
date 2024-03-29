import psycopg2

class Databases:
    def __init__(self):
        self.db = psycopg2.connect(host='211.232.75.41', dbname='logis_db', user='logis_user', password='logis_pwd', port=5433)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def execute(self, query, args={}):
        self.cursor.execute(query, args)
        rows = self.cursor.fetchall()
        return rows

    def commit(self):
        self.db.commit()