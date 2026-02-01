import mysql.connector

class EditDB:
    def __init__(self):
        self.conn_params = {
            "host": "localhost",
            "user": "root",   
            "password": "sql2707",
            "database": "bits-ems"  
        }
        self._connect()

    def _connect(self):
        try:
            self.conn = mysql.connector.connect(**self.conn_params)
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as e:
            print(f"Database connection failed: {e}")
            self.conn = None
            self.cursor = None

    def close(self):
        """Close database connection"""
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def get_employee_by_id(self, emp_id):
        """Return employee info as a dict. Returns None if not found."""
        if not self.cursor:
            return None

        query = """
        SELECT
            EmpID, DepID, job_title_id, name, email, contact_number,
            emergency_contact, date_of_birth, gender, hire_date, employment_status
        FROM employee
        WHERE EmpID = %s
        """
        try:
            self.cursor.execute(query, (emp_id,))
            result = self.cursor.fetchone()
            return result
        except mysql.connector.Error as e:
            print(f"MySQL error: {e}")
            return None

    def search_employee_by_name(self, name_part):
        """Return a list of employees whose names match partially."""
        if not self.cursor:
            return []

        query = """
        SELECT EmpID, name
        FROM employee
        WHERE name LIKE %s
        LIMIT 10
        """
        try:
            self.cursor.execute(query, (f"%{name_part}%",))
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"MySQL error: {e}")
            return []

    def update_employee(self, emp_id, data):
        """Update employee information in database"""
        if not self.cursor:
            return False

        try:
            # First, check if employee exists
            check_query = "SELECT EmpID FROM employee WHERE EmpID = %s"
            self.cursor.execute(check_query, (emp_id,))
            if not self.cursor.fetchone():
                print(f"Employee with ID {emp_id} not found")
                return False

            # Update employee main table
            update_query = """
            UPDATE employee 
            SET name = %s, date_of_birth = %s, gender = %s, hire_date = %s,
                employment_status = %s, DepID = %s, job_title_id = %s,
                contact_number = %s, emergency_contact = %s, email = %s
            WHERE EmpID = %s
            """
            
            update_values = (
                data.get('name', ''),
                data.get('date_of_birth', ''),
                data.get('gender', ''),
                data.get('hire_date', ''),
                data.get('employment_status', ''),
                data.get('DepID', '') if str(data.get('DepID', '')).isdigit() else None,
                data.get('job_title_id', '') if str(data.get('job_title_id', '')).isdigit() else None,
                data.get('contact_number', ''),
                data.get('emergency_contact', ''),
                data.get('email', ''),
                emp_id
            )
            
            self.cursor.execute(update_query, update_values)
            self.conn.commit()
            
            print(f"Employee {emp_id} updated successfully")
            return True
            
        except mysql.connector.Error as e:
            print(f"MySQL error updating employee: {e}")
            if self.conn:
                self.conn.rollback()
            return False
        except Exception as e:
            print(f"Error updating employee: {e}")
            if self.conn:
                self.conn.rollback()
            return False

    def get_employee_address(self, emp_id):
        """Get address information for employee"""
        if not self.cursor:
            return {}
        
        try:
            query = """
            SELECT citizenship, city, sub_city, woreda, kebele, house_number
            FROM address
            WHERE EmpID = %s
            """
            self.cursor.execute(query, (emp_id,))
            result = self.cursor.fetchone()
            return result if result else {}
        except mysql.connector.Error as e:
            print(f"MySQL error getting address: {e}")
            return {}