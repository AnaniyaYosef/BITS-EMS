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



def PermantDelete_DB_Table():
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    for (table_name,) in tables:
        cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.commit()
    print("All tables deleted successfully.")

