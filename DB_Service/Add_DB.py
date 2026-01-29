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
            job_title_id INT,
            name VARCHAR(255) NOT NULL,
            date_of_birth DATE NOT NULL,
            gender ENUM('Male','Female'),
            hire_date DATE,
            employment_status VARCHAR(50) NOT NULL,
            manager BOOLEAN NOT NULL DEFAULT FALSE,  -- Added manager column
            active BOOLEAN NOT NULL DEFAULT 1,
            CONSTRAINT employee_depid_fk 
                FOREIGN KEY (DepID) REFERENCES department(DepID),
            CONSTRAINT employee_jobtitle_fk 
                FOREIGN KEY (job_title_id) REFERENCES jobtitle(job_title_id)
        )""")
        print("Employee table created successfully!")
    except Exception as e:
        print("Error creating employee table:", e)

def DropEmployeeTable():
    """Drop the employee table if it exists"""
    try:
        cursor.execute("DROP TABLE IF EXISTS employee")
        print("Employee table dropped successfully!")
    except Exception as e:
        print("Error dropping employee table:", e)

CreateEmpTable()
