import sqlite3 as sql

class TransactionObject():
    database = "clientes.db"
    conexion = None
    cursor = None
    connected = False

    def connect(self):
        TransactionObject.conexion = sql.connect(TransactionObject.database)
        TransactionObject.cursor = TransactionObject.conexion.cursor()
        TransactionObject.connected = True

    def disconnect(self):
        TransactionObject.conexion.close()
        TransactionObject.connected = False

    def execute(self, sql, parms = None):
        if TransactionObject.connected:
            if parms == None:
                TransactionObject.cursor.execute(sql) 
            else:
                TransactionObject.cursor.execute(sql, parms)
            return True
        else:
            return False
    
    def fetchall(self):
        return TransactionObject.cursor.fetchall()
    
    def persist(self):
        if TransactionObject.connected:
            TransactionObject.conexion.commit()
            return True
        else:
            return False
        
    def initDB(self):
        trans = TransactionObject()
        trans.connect()
        trans.execute("CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY, nome TEXT, sobrenome TEXT, email TEXT, cpf TEXT)")
        trans.persist()
        trans.disconnect()

def insert(nome, sobrenome, email, cpf):
        trans = TransactionObject()
        trans.connect()
        trans.execute(("INSERT INTO clientes VALUES (NULL, ?, ?, ?, ?)"), (nome, sobrenome, email, cpf))
        trans.persist()
        trans.disconnect()

    
def view():
    trans = TransactionObject()
    trans.connect()
    trans.execute("SELECT * FROM clientes")
    rows = trans.fetchall()
    trans.disconnect()
    return rows

def search(nome="", sobrenome="", email="", cpf=""):
    trans = TransactionObject()
    trans.connect()
    trans.execute("SELECT * FROM clientes WHERE nome=? or sobrenome=? or email=? or cpf=?", (nome, sobrenome, email, cpf))
    rows = trans.fetchall()
    trans.disconnect()
    return rows

def delete(id):
    trans = TransactionObject()
    trans.connect()
    trans.execute("DELETE FROM clientes WHERE id=?", (id,)) 
    trans.persist()
    trans.disconnect()

def update(id, nome, sobrenome, email, cpf):
    trans = TransactionObject()
    trans.connect()
    trans.execute(("UPDATE clientes SET nome = ?,  sobrenome = ?, email = ?, cpf = ? WHERE id = ?"), (nome, sobrenome, email, cpf, id))
    trans.persist()
    trans.disconnect()

x = TransactionObject()
x.initDB()