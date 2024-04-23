from lib.Databases import Databases
import psycopg2
import psycopg2.extras  # psycopg2.extras 모듈을 임포트
class CRUD(Databases):
    def insertDB(self,  table, colum, data):
        sql = "INSERT INTO {} ({}) VALUES %s;".format( table, colum)
        try:
            self.cursor.execute(sql, (data,))
            self.db.commit()
        except Exception as e:
            print("Insert DB error:", e)
    
    def insertDBSeq(self, table, colum, data,seq):
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

    def whereDB(self,  table, colum ,where):
        sql = "SELECT {} FROM  {} WHERE {} ".format(colum,   table , where)
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

if __name__ == "__main__":
    db = CRUD()
    db.insertDB(schema='myschema', table='table', colum='ID', data='유동적변경')
    print(db.readDB(schema='myschema', table='table', colum='ID'))
    db.updateDB(schema='myschema', table='table', colum='ID', value='와우', condition='유동적변경')
    db.deleteDB(schema='myschema', table='table', condition="id != 'd'")