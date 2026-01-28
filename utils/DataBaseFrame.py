from DB_Service import Add_DB
import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sql2707",
    database="bits-ems"
)
cursor = db.cursor()


def CreateDB():
    Add_DB.CreateEmpTable()
