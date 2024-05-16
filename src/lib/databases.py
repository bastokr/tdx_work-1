import psycopg2

class Databases:
    def __init__(self):
        self.db = psycopg2.connect(host='211.232.75.41', dbname='tdx_db', user='tdx_user', password='tdx_password', port=5433)
        self.cursor = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def execute(self, query, args={}):
        self.cursor.execute(query, args)
        rows = self.cursor.fetchall()
        return rows

    def commit(self):
        self.db.commit()