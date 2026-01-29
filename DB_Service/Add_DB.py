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
            email VARCHAR(255) NOT NULL,
            contact_number VARCHAR(20),
            emergency_contact VARCHAR(20),
            date_of_birth DATE NOT NULL,
            gender ENUM('Male','Female'),
            hire_date DATE,
            employment_status VARCHAR(50) NOT NULL,
            manager BOOLEAN DEFAULT FALSE,  
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

    def insert_employee(self, dep_id, job_id, name, dob, gender, hire_date, status, is_manager=False):
        """Adds a new employee to the database."""
        query = """
        INSERT INTO employee (
            DepID, job_title_id, name, date_of_birth, 
            gender, hire_date, employment_status, manager, active
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1)
        """
        params = (dep_id, job_id, name, dob, gender, hire_date, status, is_manager)
        return self.execute_query(query, params)

    def get_latest_emp_id(self):
        """Returns the ID of the last employee added (useful for folder naming)."""
        query = "SELECT LAST_INSERT_ID()"
        result = self.execute_query(query, is_select=True)
        return result[0][0] if result else None

    def get_employee_by_name(self, name):
        """Search for a specific employee by name."""
        query = "SELECT * FROM employee WHERE name = %s"
        result = self.execute_query(query, (name,), is_select=True)
        return result[0] if result else None

