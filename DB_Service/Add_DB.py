import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sql2707",
    database="bits-ems"
)
cursor = db.cursor()



def CreateEmpTable():
    try:
        cursor.execute("""
        CREATE TABLE employee(
        EmpID INT AUTO_INCREMENT PRIMARY KEY,
        DepID INT,
        name VARCHAR(100) NOT NULL,
        date_of_birth DATE,
        hire_date DATE,
        gender ENUM('Male','Female'),
        employment_status TINYINT(1) DEFAULT 1,
        Manager TINYINT(1) DEFAULT 0,
        active TINYINT(1) DEFAULT 1,

        FOREIGN KEY (DepID) REFERENCES department(DepID) ON DELETE SET NULL)""")
        print("Emp DB Created")
    except Exception as e:
        print("Error Emp DB Failed!,",e)




CreateEmpTable()
