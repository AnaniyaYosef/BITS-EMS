import mysql.connector
import os

BASE_DOC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Document")


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
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            if search_query.strip() == "":
                query = """
                    SELECT 
                        e.EmpID AS employee_id,
                        e.name AS full_name,
                        d.DepName AS department_name,
                        e.email
                    FROM employee e
                    LEFT JOIN Department d
                        ON e.DepID = d.DepID
                    WHERE e.active = 1
                    ORDER BY e.EmpID
                """
                cursor.execute(query)
            else:
                query = """
                    SELECT 
                        e.EmpID AS employee_id,
                        e.name AS full_name,
                        d.DepName AS department_name,
                        e.email
                    FROM employee e
                    LEFT JOIN Department d
                        ON e.DepID = d.DepID
                    WHERE e.active = 1
                      AND (
                          e.name LIKE %s
                          OR CAST(e.EmpID AS CHAR) LIKE %s
                      )
                """
                like = f"%{search_query}%"
                cursor.execute(query, (like, like))

            return cursor.fetchall()

        except Exception as e:
            print("❌ Search Error:", e)
            return []

        finally:
            cursor.close()
            conn.close()
    
    
    def get_employee_image(self, emp_id):
        """Return the image path for a given employee ID."""
        query = "SELECT file_path FROM document WHERE EmpID = %s AND document_type = 'image' LIMIT 1"

        conn = self.get_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(query, (emp_id,))
            result = cursor.fetchone()
            if result:
                file_path = result[0]
                if not os.path.isabs(file_path):
                    employee_folder = os.path.join(BASE_DOC_DIR, f"{emp_id}_File")
                    file_path = os.path.join(employee_folder,file_path)
                if os.path.exists(file_path):
                    return file_path
            return None
        finally:
            cursor.close()
            conn.close()

    def get_full_profile(self, emp_id):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            query = """
                SELECT 
                    e.EmpID AS employee_id,
                    e.name AS full_name,
                    e.email,
                    e.contact_number,
                    e.gender,
                    e.hire_date AS employment_date,
                    e.employment_status,
                    d.DepName AS department_name
                FROM employee e
                LEFT JOIN Department d
                    ON e.DepID = d.DepID
                WHERE e.EmpID = %s
            """
            cursor.execute(query, (emp_id,))
            return cursor.fetchone()

        finally:
            cursor.close()
            conn.close()