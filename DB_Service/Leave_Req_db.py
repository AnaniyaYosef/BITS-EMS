import mysql.connector
from datetime import date, datetime, timedelta

class LeaveRequestDB:
    def __init__(self):
        self.db_config = {
            'host': "localhost",
            'user': "root",
            'password': "sql2707",
            'database': "bits-ems"
        }
        #self.create_table_if_not_exists()

    def get_connection(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            return None

    def create_table_if_not_exists(self):
        """Create LeaveRecord table if it doesn't exist"""
        conn = self.get_connection()
        if not conn: return
        
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS LeaveRecord (
                    LeaveID INT AUTO_INCREMENT PRIMARY KEY,
                    EmpID INT NOT NULL,
                    leave_type VARCHAR(50) NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    reason TEXT,
                    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
                    submitted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    Active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (EmpID) REFERENCES employee(EmpID)
                )
            """)
            conn.commit()
            print("LeaveRecord table checked/created successfully")
        except mysql.connector.Error as err:
            print(f"Error creating table: {err}")
        finally:
            cursor.close()
            conn.close()

    def fetch_active_employees(self):
        """Fetches list of active employees with ID and Name for dropdown menu."""
        conn = self.get_connection()
        if not conn: return []
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT EmpID, name 
                FROM employee 
                WHERE active = 1 
                ORDER BY name ASC
            """)
            employees = cursor.fetchall()
            # Return list of tuples: (EmpID, name, "") - empty string for code since it doesn't exist
            return [(emp[0], emp[1], "") for emp in employees]
        except mysql.connector.Error as err:
            print(f"Error fetching employees: {err}")
            return []
        finally:
            cursor.close()
            conn.close()

    def submit_leave_request(self, emp_id, leave_type, start_date, end_date, reason):
        """Inserts a new leave record into the database."""
        conn = self.get_connection()
        if not conn: return False, "Database connection failed."
        
        cursor = conn.cursor()
        try:
            # Check if employee exists and is active
            cursor.execute("SELECT name FROM employee WHERE EmpID = %s AND active = 1", (emp_id,))
            employee = cursor.fetchone()
            if not employee:
                return False, "Employee not found or inactive."
            
            # Check for overlapping leave requests
            cursor.execute("""
                SELECT COUNT(*) FROM LeaveRecord 
                WHERE EmpID = %s 
                AND status = 'Approved'
                AND Active = 1
                AND (
                    (start_date BETWEEN %s AND %s)
                    OR (end_date BETWEEN %s AND %s)
                    OR (%s BETWEEN start_date AND end_date)
                    OR (%s BETWEEN start_date AND end_date)
                )
            """, (emp_id, start_date, end_date, start_date, end_date, start_date, end_date))
            
            overlapping_count = cursor.fetchone()[0]
            if overlapping_count > 0:
                return False, "This employee already has approved leave during this period."
            
            # Insert new leave request
            query = """
                INSERT INTO LeaveRecord (EmpID, leave_type, start_date, end_date, reason, status)
                VALUES (%s, %s, %s, %s, %s, 'Pending')
            """
            cursor.execute(query, (emp_id, leave_type, start_date, end_date, reason))
            conn.commit()
            return True, "Leave request submitted successfully."
        except mysql.connector.Error as err:
            print(f"Error submitting leave: {err}")
            return False, str(err)
        finally:
            cursor.close()
            conn.close()

    def get_current_leave_employees(self):
        """Get employees currently on leave (between start and end dates)"""
        conn = self.get_connection()
        if not conn: return []
        
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                    e.name,
                    lr.leave_type,
                    lr.start_date,
                    lr.end_date,
                    DATEDIFF(lr.end_date, CURDATE()) as days_remaining,
                    lr.status
                FROM LeaveRecord lr
                JOIN employee e ON lr.EmpID = e.EmpID
                WHERE lr.status = 'Approved'
                AND CURDATE() BETWEEN lr.start_date AND lr.end_date
                AND lr.Active = 1
                AND e.active = 1
                ORDER BY lr.end_date ASC
            """)
            
            results = cursor.fetchall()
            # Return with empty string for employee code since it doesn't exist
            return [
                (
                    r[0],  # name
                    "",    # empty for code (no Employee_Code column)
                    r[1],  # leave_type
                    r[2],  # start_date
                    r[3],  # end_date
                    r[4],  # days_remaining
                    r[5]   # status
                )
                for r in results
            ]
        except mysql.connector.Error as err:
            print(f"Error fetching current leave: {err}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_leave_history(self, search_term=""):
        """Get leave history with optional search"""
        conn = self.get_connection()
        if not conn: return []
        
        cursor = conn.cursor()
        try:
            query = """
                SELECT 
                    e.name,
                    lr.leave_type,
                    lr.start_date,
                    lr.end_date,
                    DATEDIFF(lr.end_date, lr.start_date) + 1 as duration,
                    lr.status,
                    lr.submitted_date
                FROM LeaveRecord lr
                JOIN employee e ON lr.EmpID = e.EmpID
                WHERE lr.Active = 1
            """
            
            params = []
            if search_term:
                query += " AND e.name LIKE %s"
                params.append(f"%{search_term}%")
            
            query += " ORDER BY lr.submitted_date DESC"
            
            cursor.execute(query, tuple(params))
            results = cursor.fetchall()
            
            return [
                (
                    r[0],  # name
                    r[1],  # leave_type
                    r[2],  # start_date
                    r[3],  # end_date
                    r[4],  # duration
                    r[5],  # status
                    r[6]   # submitted_date
                )
                for r in results
            ]
        except mysql.connector.Error as err:
            print(f"Error fetching leave history: {err}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_pending_requests_count(self):
        """Get count of pending leave requests"""
        conn = self.get_connection()
        if not conn: return 0
        
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM LeaveRecord 
                WHERE status = 'Pending' 
                AND Active = 1
            """)
            result = cursor.fetchone()
            return result[0] if result else 0
        except mysql.connector.Error as err:
            print(f"Error counting pending requests: {err}")
            return 0
        finally:
            cursor.close()
            conn.close()

    def get_employee_leave_summary(self, emp_id):
        """Get leave summary for a specific employee"""
        conn = self.get_connection()
        if not conn: return {}
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_requests,
                    SUM(CASE WHEN status = 'Approved' THEN 1 ELSE 0 END) as approved,
                    SUM(CASE WHEN status = 'Rejected' THEN 1 ELSE 0 END) as rejected,
                    SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) as pending,
                    SUM(CASE WHEN status = 'Approved' THEN DATEDIFF(end_date, start_date) + 1 ELSE 0 END) as total_days
                FROM LeaveRecord 
                WHERE EmpID = %s 
                AND Active = 1
                AND YEAR(start_date) = YEAR(CURDATE())
            """, (emp_id,))
            
            result = cursor.fetchone()
            return result if result else {}
        except mysql.connector.Error as err:
            print(f"Error fetching leave summary: {err}")
            return {}
        finally:
            cursor.close()
            conn.close()

    def update_leave_status(self, leave_id, status):
        """Update leave request status"""
        conn = self.get_connection()
        if not conn: return False
        
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE LeaveRecord 
                SET status = %s 
                WHERE LeaveID = %s
            """, (status, leave_id))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error updating leave status: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def get_employee_by_name(self, name):
        """Get employee ID by name"""
        conn = self.get_connection()
        if not conn: return None
        
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT EmpID FROM employee WHERE name = %s AND active = 1", (name,))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print(f"Error getting employee by name: {err}")
            return None
        finally:
            cursor.close()
            conn.close()