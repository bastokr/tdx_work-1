from Databases import Databases

class CRUD(Databases):
    def insertDB(self, schema, table, colum, data):
        sql = "INSERT INTO {}.{} ({}) VALUES (%s);".format(schema, table, colum)
        try:
            self.cursor.execute(sql, (data,))
            self.db.commit()
        except Exception as e:
            print("Insert DB error:", e)
    
    def readDB(self,  table, colum):
        sql = "SELECT {} FROM  {}".format(colum,   table)
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

    def deleteDB(self, schema, table, condition):
        sql = "DELETE FROM {}.{} WHERE {};".format(schema, table, condition)
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