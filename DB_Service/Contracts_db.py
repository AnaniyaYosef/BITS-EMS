import mysql.connector

class DBService:
    def __init__(self):
        # UPDATED: Matched to your working credentials
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "sql2707",   # Updated password
            "database": "bits-ems"    # Updated database name
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
        # FIXED: Table name changed from 'employees' to 'Employee' and column to 'name'
        cursor.execute("SELECT name FROM Employee WHERE name LIKE %s AND Active = 1 LIMIT 5", (f"%{query}%",))
        results = cursor.fetchall()
        conn.close()
        return results

    def get_employee_details(self, name):
        conn = self.get_connection()
        if not conn: return None
        cursor = conn.cursor()
        # FIXED: Table name changed to 'Employee' and 'DepID' (based on your dashboard schema)
        cursor.execute("SELECT EmpID, DepID FROM Employee WHERE name = %s", (name,))
        data = cursor.fetchone()
        conn.close()
        return data

    def create_contract(self, emp_id, start_date, end_date, contract_type):
        conn = self.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        # FIXED: Table name changed to 'Contract' and columns matched to Dashboard logic
        query = """
            INSERT INTO Contract (EmpID, start_date, end_date, contract_type, Active) 
            VALUES (%s, %s, %s, %s, 1)
        """
        cursor.execute(query, (emp_id, start_date, end_date, contract_type))
        conn.commit()
        conn.close()
        return True