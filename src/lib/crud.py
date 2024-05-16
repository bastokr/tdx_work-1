from lib.databases import Databases
import psycopg2
import psycopg2.extras  # psycopg2.extras 모듈을 임포트

class Crud(Databases):
    def insertDB(self, table, colum, data):
        sql = "INSERT INTO {} ({}) VALUES %s;".format(table, colum)
        try:
            self.cursor.execute(sql, (data,))
            self.db.commit()
        except Exception as e:
            print("Insert DB error:", e)

    def insertDBSeq(self, table, colum, data, seq):
        sql = "INSERT INTO {} ({}) VALUES %s;".format(table, colum)
        try:
            self.cursor.execute(sql, (data,))
            self.db.commit()
        except Exception as e:
            print("Insert DB error:", e)

    def readDB(self, table, colum):
        try:
            sql = f"SELECT {colum} FROM {table}"
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Read DB error: {e}")
            raise e

    def whereDB(self, table, colum, where):
        sql = "SELECT {} FROM  {} WHERE {}".format(colum, table, where)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print("Read DB error:", e)

    def updateDB(self, schema, table, colum, value, condition):
        sql = "UPDATE {}.{} SET {}=%s WHERE {}=%s".format(schema, table, colum, colum)
        try:
            self.cursor.execute(sql, (value, condition))
            self.db.commit()
        except Exception as e:
            print("Update DB error:", e)

    def deleteDB(self, table, condition):
        sql = "DELETE FROM {} WHERE {};".format(table, condition)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("Delete DB error:", e)

    def execute_param_query(self, query, params):
        """
        파라미터화된 쿼리를 실행하고 결과를 반환하는 메서드
        :param query: 실행할 쿼리 문자열
        :param params: 파라미터로 대체할 값들이 담긴 딕셔너리
        :return: 쿼리 결과
        """
        try:
            # ':' 파라미터를 실제 값으로 대체
            formatted_params = {key.lstrip(':'): value for key, value in params.items()}
            for key, value in formatted_params.items():
                query = query.replace(f":{key}", f"{{{key}}}")

            # `params` 딕셔너리의 키를 `{}`로 둘러싸인 플레이스홀더에 맵핑하여 대체
            query = query.format(**formatted_params)

            print("Executing Query:", query)  # 쿼리 확인용 로그

            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print("Query execution with parameters error:", e)
            return []

if __name__ == "__main__":
    db = Crud()
    print(db.readDB(table='public.my_table', colum='*'))
    db.updateDB(schema='public', table='my_table', colum='name', value='new_value', condition="id = 1")
