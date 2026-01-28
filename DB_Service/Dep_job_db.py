import mysql.connector

class DepJobDB:
    def __init__(self):
        self.db_config = {
            "host": "127.0.0.1",
            "user": "root",
            "password": "@Mendelivium", 
            "database": "bits_ems_project"
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

    def insert_department(self, name, faculty, manager_id, status):
        """Adds a new department record using a VARCHAR(20) manager_id."""
        query = "INSERT INTO departments (dept_name, faculty, manager_id, status) VALUES (%s, %s, %s, %s)"
        return self.execute_query(query, (name, faculty, manager_id, status))

    def search_managers(self, name_query):
        """Find names that match the user's typing for the Smart Search."""
        # Use execute_query to keep it consistent and safe
        query = "SELECT full_name FROM employees WHERE full_name LIKE %s LIMIT 5"
        return self.execute_query(query, (f'%{name_query}%',), is_select=True)

    def get_manager_id(self, full_name):
        """Get the VARCHAR(20) ID for the selected name."""
        query = "SELECT employee_id FROM employees WHERE full_name = %s"
        result = self.execute_query(query, (full_name,), is_select=True)
        return result[0][0] if result else None
