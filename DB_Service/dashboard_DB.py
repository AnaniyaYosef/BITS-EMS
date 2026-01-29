import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class DashboardDB:
    def __init__(self):
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

    def fetch_total_employees(self):
        conn = self.get_connection()
        if not conn: return 0
        cursor = conn.cursor()
        try:
            # Updated to lowercase table 'employee' and 'active'
            cursor.execute("SELECT COUNT(*) FROM employee WHERE active = 1")
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            cursor.close()
            conn.close()

    def fetch_top_stats(self):
        conn = self.get_connection()
        if not conn: return []
        cursor = conn.cursor()
        stats = {"Full Time": 0, "Contract": 0, "Interns": 0, "On Leave": 0}

        try:
            # Updated to lowercase 'contract'
            query_contracts = "SELECT contract_type, COUNT(*) FROM contract WHERE active = 1 GROUP BY contract_type"
            cursor.execute(query_contracts)
            for c_type, count in cursor.fetchall():
                key = c_type.strip().title()
                if key in stats: stats[key] = count
                elif "Full" in key: stats["Full Time"] += count
                elif "Intern" in key: stats["Interns"] += count

            # Updated to lowercase 'leaverecord'
            query_leave = """
                SELECT COUNT(*) FROM leaverecord 
                WHERE status = 'Approved' AND CURDATE() BETWEEN start_date AND end_date AND active = 1
            """
            cursor.execute(query_leave)
            stats["On Leave"] = cursor.fetchone()[0]

        except mysql.connector.Error as err:
            print(f"Error fetching stats: {err}")
        finally:
            cursor.close()
            conn.close()

        return [
            ("Full Time", str(stats["Full Time"]), "#2E7D32"),
            ("Contract", str(stats["Contract"]), "#F9A825"),
            ("Interns", str(stats["Interns"]), "#0277BD"),
            ("On Leave", str(stats["On Leave"]), "#C62828")
        ]

    def fetch_dept_distribution(self):
        conn = self.get_connection()
        if not conn: return []
        cursor = conn.cursor()
        data = []
        try:
            # Updated to lowercase 'department' and 'employee'
            query = """
                SELECT d.DepName, COUNT(e.EmpID) as count
                FROM department d
                LEFT JOIN employee e ON d.DepID = e.DepID AND e.active = 1
                WHERE d.Active = 1
                GROUP BY d.DepID, d.DepName
            """
            cursor.execute(query)
            for name, count in cursor.fetchall():
                data.append((name, str(count)))
        finally:
            cursor.close()
            conn.close()
        return data

    def fetch_contract_alerts(self):
        conn = self.get_connection()
        if not conn: return []
        cursor = conn.cursor()
        alerts = []
        try:
            # Updated to lowercase 'contract', 'employee', 'department'
            query = """
                SELECT e.name, d.DepName, DATEDIFF(c.end_date, CURDATE()) as days_left
                FROM contract c
                JOIN employee e ON c.EmpID = e.EmpID
                JOIN department d ON e.DepID = d.DepID
                WHERE c.active = 1
                  AND c.end_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
                ORDER BY days_left ASC LIMIT 5
            """
            cursor.execute(query)
            for name, dept, days in cursor.fetchall():
                name_display = f"{name} ({dept})"
                time_msg = "Expires Today" if days == 0 else f"Expires in: {days} Days"
                alerts.append((name_display, time_msg))
        finally:
            cursor.close()
            conn.close()
        return alerts

    def fetch_pending_leave_count(self):
        conn = self.get_connection()
        if not conn: return 0
        cursor = conn.cursor()
        try:
            # Updated to lowercase 'leaverecord'
            cursor.execute("SELECT COUNT(*) FROM leaverecord WHERE status = 'Pending' AND active = 1")
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            cursor.close()
            conn.close()