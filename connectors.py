#coding:utf-8
from sqlite3 import connect as sl_connect
from pymysql import connect as sql_connect

class SqliteConnector():

    def __init__(self,db_name="db.sqlite"):
        self.db_name=db_name
        self.connection=None
        self.connect()
    
    def connect(self):
        self.connection=sl_connect(self.db_name)
        

    def get_connection(self):
        curs=self.connection.cursor()
        return curs,self.connection

class MySQLConnector():

    def __init__(self,host="",port=3306,db_name="db",username="root",password="",charset="utf-8"):
        self.host=host
        self.port=port
        self.db_name=db_name
        self.username=username
        self.password=password
        self.charset=charset
        self.connection=None
    
    def connect(self):
        self.connection=sql_connect(
            host=self.host,
            port=self.port,
            database=self.db_name,
            user=self.username,
            password=self.password,
        )

    def get_connnection(self):
        curs=self.connection.cursor()
        return curs,self.connection