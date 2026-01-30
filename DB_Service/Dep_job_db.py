import mysql.connector
from datetime import datetime

class DBService:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "sql2707",
            "database": "bits-ems"
        }

    def get_connection(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            return None

    def search_employees(self, query):
        conn = self.get_connection()
        if not conn: return []
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM employee WHERE name LIKE %s AND active = 1 LIMIT 5", (f"%{query}%",))
        results = cursor.fetchall()
        conn.close()
        return results

    def get_employee_details(self, name):
        conn = self.get_connection()
        if not conn: return None
        cursor = conn.cursor()
        cursor.execute("SELECT EmpID, DepID FROM employee WHERE name = %s", (name,))
        data = cursor.fetchone()
        conn.close()
        return data

    def create_contract(self, emp_id, start_date, end_date, contract_type):
        conn = self.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        
        # Check if Contract table exists
        cursor.execute("SHOW TABLES LIKE 'Contract'")
        if not cursor.fetchone():
            # Create Contract table if it doesn't exist
            create_query = """
            CREATE TABLE IF NOT EXISTS Contract (
                ContractID INT AUTO_INCREMENT PRIMARY KEY,
                EmpID INT NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                contract_type VARCHAR(50) NOT NULL,
                Active BOOLEAN NOT NULL DEFAULT 1,
                FOREIGN KEY (EmpID) REFERENCES employee(EmpID)
            )
            """
            cursor.execute(create_query)
        
        query = """
            INSERT INTO Contract (EmpID, start_date, end_date, contract_type, Active) 
            VALUES (%s, %s, %s, %s, 1)
        """
        cursor.execute(query, (emp_id, start_date, end_date, contract_type))
        conn.commit()
        conn.close()
        return True

    def get_active_contracts(self, search_term=None):
        """Get all active contracts with optional search filter"""
        conn = self.get_connection()
        if not conn: return []
        cursor = conn.cursor()
        
        if search_term:
            query = """
                SELECT c.ContractID, c.EmpID, e.name, d.DepName as department, 
                       c.start_date, c.end_date, c.contract_type
                FROM Contract c
                JOIN employee e ON c.EmpID = e.EmpID
                LEFT JOIN Department d ON e.DepID = d.DepID
                WHERE c.Active = 1 
                AND (e.name LIKE %s OR c.EmpID LIKE %s OR c.ContractID LIKE %s)
                ORDER BY c.end_date ASC
            """
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
        else:
            query = """
                SELECT c.ContractID, c.EmpID, e.name, d.DepName as department, 
                       c.start_date, c.end_date, c.contract_type
                FROM Contract c
                JOIN employee e ON c.EmpID = e.EmpID
                LEFT JOIN Department d ON e.DepID = d.DepID
                WHERE c.Active = 1 
                ORDER BY c.end_date ASC
            """
            cursor.execute(query)
        
        results = cursor.fetchall()
        conn.close()
        return results

    def get_contract_history(self, search_term=None):
        """Get contract history (inactive/ended contracts)"""
        conn = self.get_connection()
        if not conn: return []
        cursor = conn.cursor()
        
        if search_term:
            query = """
                SELECT c.ContractID, c.EmpID, e.name, c.start_date, c.end_date, c.contract_type
                FROM Contract c
                JOIN employee e ON c.EmpID = e.EmpID
                WHERE c.Active = 0 
                AND (e.name LIKE %s OR c.EmpID LIKE %s OR c.ContractID LIKE %s)
                ORDER BY c.end_date DESC
            """
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
        else:
            query = """
                SELECT c.ContractID, c.EmpID, e.name, c.start_date, c.end_date, c.contract_type
                FROM Contract c
                JOIN employee e ON c.EmpID = e.EmpID
                WHERE c.Active = 0 
                ORDER BY c.end_date DESC
            """
            cursor.execute(query)
        
        results = cursor.fetchall()
        conn.close()
        return results

    def end_contract(self, contract_id):
        """Mark a contract as inactive (ended)"""
        conn = self.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        
        query = "UPDATE Contract SET Active = 0 WHERE ContractID = %s"
        cursor.execute(query, (contract_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    def get_contract_stats(self):
        """Get contract statistics"""
        conn = self.get_connection()
        if not conn: return {}
        cursor = conn.cursor()
        
        stats = {}
        
        # Count active contracts
        cursor.execute("SELECT COUNT(*) FROM Contract WHERE Active = 1")
        stats['active'] = cursor.fetchone()[0]
        
        # Count expired contracts (end date < today)
        cursor.execute("SELECT COUNT(*) FROM Contract WHERE Active = 1 AND end_date < CURDATE()")
        stats['expired'] = cursor.fetchone()[0]
        
        # Count expiring soon (within 30 days)
        cursor.execute("SELECT COUNT(*) FROM Contract WHERE Active = 1 AND end_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)")
        stats['expiring_soon'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def create_job_title_table(self):
        """Creates the JobTitle table if it doesn't already exist."""
        conn = self.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        
        query = """
        CREATE TABLE IF NOT EXISTS JobTitle (
            job_title_id INT AUTO_INCREMENT PRIMARY KEY,
            title_name VARCHAR(255) NOT NULL,
            description TEXT,
            Active BOOLEAN NOT NULL DEFAULT 1
        );
        """
        
        try:
            cursor.execute(query)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error creating JobTitle table: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def create_department_table(self):
        """Creates the Department table if it doesn't exist."""
        conn = self.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        
        query = """
        CREATE TABLE IF NOT EXISTS Department (
            DepID INT AUTO_INCREMENT PRIMARY KEY,
            DepName VARCHAR(255) NOT NULL,
            manager_id INT NULL,
            Active BOOLEAN NOT NULL DEFAULT 1,
            FOREIGN KEY (manager_id) REFERENCES employee(EmpID)
        );
        """
        
        try:
            cursor.execute(query)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error creating Department table: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def insert_department(self, name, manager_id, active):
        """Adds a new department record."""
        conn = self.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        
        query = "INSERT INTO Department (DepName, manager_id, Active) VALUES (%s, %s, %s)"
        
        try:
            cursor.execute(query, (name, manager_id, 1 if active else 0))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error inserting department: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def insert_job_title(self, title, description, active=True):
        """Adds a new job title record."""
        conn = self.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        
        query = "INSERT INTO JobTitle (title_name, description, Active) VALUES (%s, %s, %s)"
        
        try:
            cursor.execute(query, (title, description, 1 if active else 0))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error inserting job title: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def search_managers(self, name_query):
        """Search for managers (employees with manager = TRUE)."""
        conn = self.get_connection()
        if not conn: return []
        cursor = conn.cursor()
        
        query = """
        SELECT EmpID, name 
        FROM employee 
        WHERE name LIKE %s AND manager = TRUE AND active = 1 
        LIMIT 5
        """
        
        try:
            cursor.execute(query, (f"%{name_query}%",))
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error searching managers: {err}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_manager_id(self, name):
        """Get employee ID by name."""
        conn = self.get_connection()
        if not conn: return None
        cursor = conn.cursor()
        
        query = "SELECT EmpID FROM employee WHERE name = %s"
        
        try:
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print(f"Error getting manager ID: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_all_job_titles(self, search_term=None):
        """Get all job titles with optional search filter."""
        conn = self.get_connection()
        if not conn: return []
        cursor = conn.cursor()
        
        try:
            if search_term:
                query = """
                SELECT j.job_title_id, j.title_name, j.description, j.Active,
                    COUNT(e.EmpID) as employee_count
                FROM JobTitle j
                LEFT JOIN employee e ON j.job_title_id = e.job_title_id AND e.active = 1
                WHERE j.title_name LIKE %s
                GROUP BY j.job_title_id, j.title_name, j.description, j.Active
                ORDER BY j.title_name
                """
                cursor.execute(query, (f"%{search_term}%",))
            else:
                query = """
                SELECT j.job_title_id, j.title_name, j.description, j.Active,
                    COUNT(e.EmpID) as employee_count
                FROM JobTitle j
                LEFT JOIN employee e ON j.job_title_id = e.job_title_id AND e.active = 1
                GROUP BY j.job_title_id, j.title_name, j.description, j.Active
                ORDER BY j.title_name
                """
                cursor.execute(query)
            
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error getting job titles: {err}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_all_departments(self, search_term=None):
        """Get all departments with optional search filter."""
        conn = self.get_connection()
        if not conn: return []
        cursor = conn.cursor()
        
        try:
            if search_term:
                query = """
                SELECT d.DepID, d.DepName, d.manager_id, d.Active,
                    e.name as manager_name,
                    COUNT(emp.EmpID) as employee_count
                FROM Department d
                LEFT JOIN employee e ON d.manager_id = e.EmpID
                LEFT JOIN employee emp ON d.DepID = emp.DepID AND emp.active = 1
                WHERE d.DepName LIKE %s
                GROUP BY d.DepID, d.DepName, d.manager_id, d.Active, e.name
                ORDER BY d.DepName
                """
                cursor.execute(query, (f"%{search_term}%",))
            else:
                query = """
                SELECT d.DepID, d.DepName, d.manager_id, d.Active,
                    e.name as manager_name,
                    COUNT(emp.EmpID) as employee_count
                FROM Department d
                LEFT JOIN employee e ON d.manager_id = e.EmpID
                LEFT JOIN employee emp ON d.DepID = emp.DepID AND emp.active = 1
                GROUP BY d.DepID, d.DepName, d.manager_id, d.Active, e.name
                ORDER BY d.DepName
                """
                cursor.execute(query)
            
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error getting departments: {err}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_job_title_details(self, job_title_id):
        """Get details of a specific job title."""
        conn = self.get_connection()
        if not conn: return None
        cursor = conn.cursor()
        
        query = "SELECT job_title_id, title_name, description, Active FROM JobTitle WHERE job_title_id = %s"
        
        try:
            cursor.execute(query, (job_title_id,))
            result = cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            print(f"Error getting job title details: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def update_job_title_description(self, job_title_id, description):
        """Update job title description."""
        conn = self.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        
        query = "UPDATE JobTitle SET description = %s WHERE job_title_id = %s"
        
        try:
            cursor.execute(query, (description, job_title_id))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error updating job title description: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def toggle_job_title_status(self, job_title_id):
        """Toggle job title active/inactive status."""
        conn = self.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        
        # First get current status
        cursor.execute("SELECT Active FROM JobTitle WHERE job_title_id = %s", (job_title_id,))
        result = cursor.fetchone()
        
        if not result:
            return False
        
        current_status = result[0]
        new_status = 0 if current_status == 1 else 1
        
        query = "UPDATE JobTitle SET Active = %s WHERE job_title_id = %s"
        
        try:
            cursor.execute(query, (new_status, job_title_id))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error toggling job title status: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def toggle_department_status(self, department_id):
        """Toggle department active/inactive status."""
        conn = self.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        
        # First get current status
        cursor.execute("SELECT Active FROM Department WHERE DepID = %s", (department_id,))
        result = cursor.fetchone()
        
        if not result:
            return False
        
        current_status = result[0]
        new_status = 0 if current_status == 1 else 1
        
        query = "UPDATE Department SET Active = %s WHERE DepID = %s"
        
        try:
            cursor.execute(query, (new_status, department_id))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error toggling department status: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def insert_employee(self, dep_id, job_id, name, email, contact, emergency, 
                    dob, gender, hire_date, status, manager=False):
        """Insert a new employee into the database."""
        conn = self.get_connection()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        # Format dates properly
        dob_date = dob if isinstance(dob, str) else dob.strftime('%Y-%m-%d')
        hire_date_formatted = hire_date if isinstance(hire_date, str) else hire_date.strftime('%Y-%m-%d')
        
        query = """
        INSERT INTO employee 
        (DepID, job_title_id, name, email, contact_number, emergency_contact, 
        date_of_birth, gender, hire_date, employment_status, manager, active) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
        """
        
        try:
            cursor.execute(query, (
                dep_id, job_id, name, email, contact, emergency,
                dob_date, gender, hire_date_formatted, status, manager
            ))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error inserting employee: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def get_latest_emp_id(self):
        """Get the ID of the most recently inserted employee."""
        conn = self.get_connection()
        if not conn:
            return None
        
        cursor = conn.cursor()
        
        query = "SELECT LAST_INSERT_ID()"
        
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print(f"Error getting latest EmpID: {err}")
            return None
        finally:
            cursor.close()
            conn.close()            