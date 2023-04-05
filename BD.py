import sqlite3
import uuid


class DBForAll():
  def Connect(self):
    self.con = sqlite3.connect('UltimateBD.db')
    self.cur = self.con.cursor()

  def create_table(self):
    self.Connect()
    self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
        UUID TEXT NOT NULL UNIQUE,
        Tg_id INTEGER NULL,
        Ds_id INTEGER NULL,
        Tg_name TEXT NULL,
        Ds_name TEXT NULL,
        Password TEXT NOT NULL);""")
    self.Close()


  def CreateUser(self,Password, Tg_name=None, Tg_id=None,  Ds_id=None, Ds_name=None):
    self.Connect()  
    self.cur.execute("SELECT * FROM users")
    self.id = str(uuid.uuid4())
    rest = (self.id, Tg_id, Ds_id, Tg_name, Ds_name, Password) # добавить парольЫ
    self.cur.execute("INSERT INTO users VALUES(?,?,?,?,?,?);", rest)
    self.con.commit()
    self.cur.execute("SELECT * FROM users")
    results = self.cur.fetchall()
    print(results)
    self.Close()
  
  def getValues(self, column, value):
    self.Connect()
    self.cur.execute(f"SELECT * FROM users WHERE {column} = {value}")
    self.con.commit()
    return self.cur.fetchall()

  def UpdateUser(self, uuid, id, name):
    self.Connect()      
    self.cur.execute("SELECT * FROM users WHERE UUID=?",(uuid,))
    rest=(id,name,uuid)
    results = self.cur.fetchall()
    if results[0][1]==None:
        print('tg пуст')
        self.cur.execute(f"UPDATE users set Ts_id=?, Ts_name=? where UUID=?;", rest)
    elif results[0][2]==None:
        print('ds пуст')
        self.cur.execute(f"UPDATE users set Ds_id=?, Ds_name=? where UUID=?;", rest)
    else:
        print('Все поля заполнены, перезаписи не будет!')    
    self.Close()    

  def delete_tabl(self):
    self.Connect()  
    self.cur.execute("DELETE FROM users")
    self.Close

  def ConCommit(self):  
    self.con.commit()

  def Close(self):
    #self.con.commit()
    self.con.close()