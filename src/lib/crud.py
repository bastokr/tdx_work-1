import ctypes
from lib.databases import Databases
import psycopg2
import psycopg2.extras  # psycopg2.extras 모듈을 임포트

class Crud(Databases):
    _instance = None

    def __new__(cls, settings=None):
        if cls._instance is None:
            cls._instance = super(Crud, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, settings=None):
        if self.__initialized:
            return
        super().__init__(settings)
        self.__initialized = True

    def insertDB(self, table, column, data):
        self.check_connection()
        if not self.cursor:
            print("Database not connected insertDB")
            return
        sql = "INSERT INTO {} ({}) VALUES %s;".format(table, column)
        try:
            self.cursor.execute(sql, (data,))
            self.db.commit()
        except Exception as e:
            print("Insert DB error:", e)

    def readDB(self, table, column, return_column_names=False):
        self.check_connection()
        if not self.cursor:
            print("Database not connected readDB")
            return []
        sql = f"SELECT {column} FROM {table}"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if return_column_names:
                colnames = [desc[0] for desc in self.cursor.description]
                return result, colnames
            else:
                return result
        except Exception as e:
            print(f"Read DB error: {e}")
            raise e

    def whereDB(self, table, column, where, return_column_names=False):
        self.check_connection()
        if not self.cursor:
            print("self.cursor" + self.cursor)
            print("Database not connected whereDB")
            return []
        sql = "SELECT {} FROM {} WHERE {}".format(column, table, where)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if return_column_names:
                colnames = [desc[0] for desc in self.cursor.description]
                return result, colnames
            else:
                return result
        except Exception as e:
            print("Read DB error:", e)

    def updateDB(self, schema, table, column, value, condition):
        self.check_connection()
        if not self.cursor:
            print("Database not connected updateDB")
            return
        sql = "UPDATE {}.{} SET {}=%s WHERE {}=%s".format(schema, table, column, column)
        try:
            self.cursor.execute(sql, (value, condition))
            self.db.commit()
        except Exception as e:
            print("Update DB error:", e)

    def deleteDB(self, table, condition):
        self.check_connection()
        if not self.cursor:
            print("Database not connected deleteDB")
            return
        sql = "DELETE FROM {} WHERE {};".format(table, condition)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("Delete DB error:", e)

    def execute_param_query(self, query, params):
        self.check_connection()
        if not self.cursor:
            print("Database not connected execute_param_query")
            return []
        try:
            formatted_params = {key.lstrip(':'): value for key, value in params.items()}
            for key, value in formatted_params.items():
                query = query.replace(f":{key}", f"{{{key}}}")
            query = query.format(**formatted_params)
            print("Executing Query:", query)
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print("Query execution with parameters error:", e)
            return []

    def test_connection(self, settings):
        try:
            print("test_connection")
            settings['connect_timeout'] = 3  # 3초 타임아웃 설정
            conn = psycopg2.connect(**settings)
            conn.close()
            return True
        except psycopg2.OperationalError as e:
            if 'timeout expired' in str(e):
                message = "데이터베이스 연결 시간 초과. 데이터베이스에 연결할 수 없습니다."
            else:
                message = f"Connection test failed: {e}"
            print(message)
            ctypes.windll.user32.MessageBoxW(0, message, "Database Connection Error", 0x10)
            return False
        except Exception as e:
            message = f"Connection test failed: {e}"
            print(message)
            return False
