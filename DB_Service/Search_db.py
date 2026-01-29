import mysql.connector

class SearchDB:
    def __init__(self):
        self.db_config = {
            'host': "localhost",
            'user': "root",
            'password': "sql2707",
            'database': "bits-ems"
        }

    def get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def search_all_employees(self, search_query=""):
        """Fetches employees based on name or ID for the search list."""
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT e.EmpID, e.name, d.DepName, e.employment_status 
                FROM employee e
                LEFT JOIN department d ON e.DepID = d.DepID
                WHERE e.active = 1 AND (e.name LIKE %s OR e.EmpID LIKE %s)
            """
            like_query = f"%{search_query}%"
            cursor.execute(query, (like_query, like_query))
            return cursor.fetchall()
        finally:
            conn.close()

    def get_full_profile(self, emp_id):
        """Fetches every detail about an employee, including their profile image."""
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT e.*, d.DepName, doc.file_path as profile_image
                FROM employee e
                LEFT JOIN department d ON e.DepID = d.DepID
                LEFT JOIN Document doc ON e.EmpID = doc.EmpID AND doc.document_type = 'image'
                WHERE e.EmpID = %s
            """
            cursor.execute(query, (emp_id,))
            return cursor.fetchone()
        finally:
            conn.close()