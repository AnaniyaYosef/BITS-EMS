import mysql.connector

class DBService:
    def __init__(self):
        self.db_config = {
            "host": "127.0.0.1",
            "user": "root",
            "password": "@Mendelivium",
            "database": "bits_ems_project"
        }

    def get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def search_employees(self, query):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT full_name FROM employees WHERE full_name LIKE %s LIMIT 5", (f"%{query}%",))
        results = cursor.fetchall()
        conn.close()
        return results

    def get_employee_details(self, name):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT employee_id, department FROM employees WHERE full_name = %s", (name,))
        data = cursor.fetchone()
        conn.close()
        return data

    def create_contract(self, emp_id, start_date, end_date, status):
        conn = self.get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO contracts (employee_id, start_date, end_date, status) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (emp_id, start_date, end_date, status))
        conn.commit()
        conn.close()
