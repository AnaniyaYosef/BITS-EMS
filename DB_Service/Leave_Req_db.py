import mysql.connector
from datetime import date

class LeaveRequestDB:
    def __init__(self):
        # Using the same credentials as your main project
        self.db_config = {
            'host': "localhost",
            'user': "root",
            'password': "sql2707",
            'database': "bits-ems"
        }

    def get_connection(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            return None

    def fetch_active_employees(self):
        """Fetches list of employees for the dropdown menu."""
        conn = self.get_connection()
        if not conn: return []
        cursor = conn.cursor()
        try:
            # Returns a list of names for the UI dropdown
            cursor.execute("SELECT name FROM Employee WHERE Active = 1 ORDER BY name ASC")
            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def get_employee_id(self, name):
        """Helper to get EmpID from a name string."""
        conn = self.get_connection()
        if not conn: return None
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT EmpID FROM Employee WHERE name = %s", (name,))
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            cursor.close()
            conn.close()

    def submit_leave_request(self, emp_name, leave_type, start_date, end_date, reason):
        """Inserts a new leave record into the database."""
        emp_id = self.get_employee_id(emp_name)
        if not emp_id:
            return False, "Employee not found."

        conn = self.get_connection()
        if not conn: return False, "Database connection failed."
        
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO LeaveRecord (EmpID, start_date, end_date, status, Active)
                VALUES (%s, %s, %s, 'Pending', 1)
            """
            # Note: If you add a 'leave_type' or 'reason' column to your table, 
            # update the query above to include them.
            cursor.execute(query, (emp_id, start_date, end_date))
            conn.commit()
            return True, "Request submitted successfully."
        except mysql.connector.Error as err:
            print(f"Error submitting leave: {err}")
            return False, str(err)
        finally:
            cursor.close()
            conn.close()