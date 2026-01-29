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
        cursor.execute("SELECT name FROM Employee WHERE name LIKE %s AND Active = 1 LIMIT 5", (f"%{query}%",))
        results = cursor.fetchall()
        conn.close()
        return results

    def get_employee_details(self, name):
        conn = self.get_connection()
        if not conn: return None
        cursor = conn.cursor()
        cursor.execute("SELECT EmpID, DepID FROM Employee WHERE name = %s", (name,))
        data = cursor.fetchone()
        conn.close()
        return data

    def create_contract(self, emp_id, start_date, end_date, contract_type):
        conn = self.get_connection()
        if not conn: return False
        cursor = conn.cursor()
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
                JOIN Employee e ON c.EmpID = e.EmpID
                LEFT JOIN department d ON e.DepID = d.DepID
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
                JOIN Employee e ON c.EmpID = e.EmpID
                LEFT JOIN department d ON e.DepID = d.DepID
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
                JOIN Employee e ON c.EmpID = e.EmpID
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
                JOIN Employee e ON c.EmpID = e.EmpID
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