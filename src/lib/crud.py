from lib.databases import Databases
import psycopg2
import psycopg2.extras  # psycopg2.extras 모듈을 임포트


class Crud(Databases):
    def insertDB(self, table, column, data):
        if not self.cursor:
            print("Database not connected")
            return
        sql = "INSERT INTO {} ({}) VALUES %s;".format(table, column)
        try:
            self.cursor.execute(sql, (data,))
            self.db.commit()
        except Exception as e:
            print("Insert DB error:", e)

    def readDB(self, table, column, return_column_names=False):
        if not self.cursor:
            print("Database not connected")
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
        if not self.cursor:
            print("Database not connected")
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
        if not self.cursor:
            print("Database not connected")
            return
        sql = "UPDATE {}.{} SET {}=%s WHERE {}=%s".format(schema, table, column, column)
        try:
            self.cursor.execute(sql, (value, condition))
            self.db.commit()
        except Exception as e:
            print("Update DB error:", e)

    def deleteDB(self, table, condition):
        if not self.cursor:
            print("Database not connected")
            return
        sql = "DELETE FROM {} WHERE {};".format(table, condition)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("Delete DB error:", e)

    def execute_param_query(self, query, params):
        if not self.cursor:
            print("Database not connected")
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


# if __name__ == "__main__":
#     db = Crud()
#     print(db.readDB(table='public.my_table', column='*'))
#     db.updateDB(schema='public', table='my_table', column='name', value='new_value', condition="id = 1")
