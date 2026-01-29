import mysql.connector

class DepJobDB:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "sql2707", 
            "database": "bits-ems"
        }

    def execute_query(self, query, params=None, is_select=False):
        """Helper to ensure we always have a valid connection/cursor."""
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            if is_select:
                result = cursor.fetchall()
                return result
            else:
                conn.commit()
                return True
        finally:
            cursor.close()
            conn.close()

    def create_job_title_table(self):
        """Creates the JobTitle table if it doesn't already exist."""
        query = """
        CREATE TABLE IF NOT EXISTS JobTitle (
            job_title_id INT AUTO_INCREMENT PRIMARY KEY,
            title_name VARCHAR(255) NOT NULL,
            description LONGTEXT,
            Active BOOLEAN NOT NULL DEFAULT 1
        );
        """
        return self.execute_query(query)

    def create_department_table(self):
        """Creates the Department table based on your exact SQL."""
        query = """
        CREATE TABLE IF NOT EXISTS Department (
            DepID INT AUTO_INCREMENT PRIMARY KEY,
            DepName VARCHAR(255) NOT NULL,
            manager_id VARCHAR(20) NULL,
            Active BOOLEAN NOT NULL DEFAULT 1
        );
        """
        return self.execute_query(query)

    def insert_department(self, name, manager_id, active):
        """Adds a new department record using a VARCHAR(20) manager_id."""
        query = "INSERT INTO departments (DepName,manager_id, Active) VALUES (%s, %s, %s)"
        return self.execute_query(query, (name,manager_id, active))
    
    def insert_job_title(self, title, description, active=True):
        query = "INSERT INTO JobTitle (title_name, description, Active) VALUES (%s, %s, %s)"
        return self.execute_query(query, (title, description, active))

    def get_all_departments(self, only_active=True):
        """Fetches departments for dropdowns or lists."""
        if only_active:
            query = "SELECT DepID, DepName FROM Department WHERE Active = 1"
        else:
            query = "SELECT * FROM Department"
        return self.execute_query(query, is_select=True)
    
    def search_managers(self, name_query):
        """Find names that match the user's typing for the Smart Search."""
        # Note: Ensure your 'employees' table actually has 'full_name'
        query = "SELECT full_name FROM employee WHERE full_name LIKE %s LIMIT 5"
        return self.execute_query(query, (f'%{name_query}%',), is_select=True)

    def get_manager_id(self, full_name):
        """Get the VARCHAR(20) ID for the selected name."""
        query = "SELECT employee_id FROM employees WHERE full_name = %s"
        result = self.execute_query(query, (full_name,), is_select=True)
        return result[0][0] if result else None
    
    def get_all_job_titles(self, only_active=True):
        query = "SELECT job_title_id, title_name FROM jobtitle"
        if only_active: query += " WHERE Active = 1"
        return self.execute_query(query, is_select=True)

    def insert_employee(self, dep_id, job_id, name, email, contact, emergency, dob, gender, hire_date, status, is_manager=False):
        """Adds a new employee with all captured fields."""
        query = """
        INSERT INTO employee (
            DepID, job_title_id, name, email, contact_number, 
            emergency_contact, date_of_birth, gender, hire_date, 
            employment_status, manager, active
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
        """
        params = (dep_id, job_id, name, email, contact, emergency, dob, gender, hire_date, status, is_manager)
        return self.execute_query(query, params)

    def get_latest_emp_id(self):
            query = "SELECT LAST_INSERT_ID()"
            result = self.execute_query(query, is_select=True)
            return result[0][0] if result else None