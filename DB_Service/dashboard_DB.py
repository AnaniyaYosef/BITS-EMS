import mysql.connector

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
            print("DB Connection Error:", err)
            return None

    # =========================
    # TOTAL EMPLOYEES
    # =========================
    def fetch_total_employees(self):
        conn = self.get_connection()
        if not conn: return 0
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM employee WHERE active = 1")
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()

    # =========================
    # TOP DASHBOARD STATS
    # =========================
    def fetch_top_stats(self):
        conn = self.get_connection()
        if not conn: return []
        cursor = conn.cursor()

        stats = {
            "Full-Time": 0,
            "Part-Time": 0,
            "Interns": 0,
            "On Leave": 0
        }

        try:
            # Full-Time / Part-Time
            cursor.execute("""
                SELECT employment_status, COUNT(*) 
                FROM employee 
                WHERE active = 1 
                GROUP BY employment_status
            """)
            for status, count in cursor.fetchall():
                if status in stats:
                    stats[status] = count

            # Interns (job title based)
            cursor.execute("""
                SELECT COUNT(*) 
                FROM employee e
                JOIN jobtitle j ON e.job_title_id = j.job_title_id
                WHERE e.active = 1
                  AND j.Active = 1
                  AND LOWER(j.title_name) LIKE '%intern%'
            """)
            stats["Interns"] = cursor.fetchone()[0]

            # On Leave (approved & active today)
            cursor.execute("""
                SELECT COUNT(*) 
                FROM leaverecord
                WHERE status = 'Approved'
                  AND Active = 1
                  AND CURDATE() BETWEEN start_date AND end_date
            """)
            stats["On Leave"] = cursor.fetchone()[0]

        except mysql.connector.Error as err:
            print("Dashboard stat error:", err)

        finally:
            cursor.close()
            conn.close()

        return [
            ("Full Time", str(stats["Full-Time"]), "#2E7D32"),
            ("Part Time", str(stats["Part-Time"]), "#1565C0"),
            ("Interns", str(stats["Interns"]), "#0277BD"),
            ("On Leave", str(stats["On Leave"]), "#C62828")
        ]

    # =========================
    # DEPARTMENT DISTRIBUTION
    # =========================
    def fetch_dept_distribution(self):
        conn = self.get_connection()
        if not conn: return []
        cursor = conn.cursor()
        data = []

        try:
            cursor.execute("""
                SELECT d.DepName, COUNT(e.EmpID)
                FROM department d
                LEFT JOIN employee e 
                    ON d.DepID = e.DepID AND e.active = 1
                WHERE d.Active = 1
                GROUP BY d.DepID, d.DepName
            """)
            for name, count in cursor.fetchall():
                data.append((name, str(count)))
        finally:
            cursor.close()
            conn.close()

        return data

    # =========================
    # CONTRACT EXPIRY ALERTS
    # =========================
    def fetch_contract_alerts(self):
        conn = self.get_connection()
        if not conn: return []
        cursor = conn.cursor()
        alerts = []

        try:
            cursor.execute("""
                SELECT e.name, d.DepName,
                       DATEDIFF(c.end_date, CURDATE()) AS days_left
                FROM contract c
                JOIN employee e ON c.EmpID = e.EmpID
                JOIN department d ON e.DepID = d.DepID
                WHERE c.Active = 1
                  AND c.end_date BETWEEN CURDATE()
                  AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
                ORDER BY days_left ASC
                LIMIT 5
            """)

            for name, dept, days in cursor.fetchall():
                msg = "Expires Today" if days == 0 else f"Expires in {days} days"
                alerts.append((f"{name} ({dept})", msg))

        finally:
            cursor.close()
            conn.close()

        return alerts

    # =========================
    # PENDING LEAVE COUNT
    # =========================
    def fetch_pending_leave_count(self):
        conn = self.get_connection()
        if not conn: return 0
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM leaverecord
                WHERE status = 'Pending' AND Active = 1
            """)
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()