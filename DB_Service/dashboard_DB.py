import mysql.connector
import os
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()


class DashboardDB:
    def __init__(self):
        # Update these credentials to match your local MySQL setup
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME', 'BITS_EMS')
        }

    def get_connection(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            return None

    def fetch_top_stats(self):
        """
        Fetches counts for: Full Time, Contract, Interns, and On Leave.
        Assumes 'contract_type' in Contract table holds values like 'Full Time', 'Intern', etc.
        """
        conn = self.get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        stats = {
            "Full Time": 0,
            "Contract": 0,
            "Interns": 0,
            "On Leave": 0
        }

        try:
            # 1. Get counts based on Contract Type (Active contracts only)
            # We assume contract_type contains strings like 'Full Time', 'Intern', 'Contract'
            query_contracts = """
                              SELECT contract_type, COUNT(*)
                              FROM Contract
                              WHERE Active = 1
                              GROUP BY contract_type \
                              """
            cursor.execute(query_contracts)
            for c_type, count in cursor.fetchall():
                # Normalize string to title case to match keys
                key = c_type.strip().title()
                if key in stats:
                    stats[key] = count
                elif "Full" in key:  # Handle variations like "Full-Time"
                    stats["Full Time"] += count
                elif "Intern" in key:
                    stats["Interns"] += count

            # 2. Get count of people currently On Leave
            # Checks if today is between start and end date of a leave record
            query_leave = """
                          SELECT COUNT(*)
                          FROM LeaveRecord
                          WHERE status = 'Approved'
                            AND curdate() BETWEEN start_date AND end_date
                            AND Active = 1 \
                          """
            cursor.execute(query_leave)
            stats["On Leave"] = cursor.fetchone()[0]

        except mysql.connector.Error as err:
            print(f"Error fetching stats: {err}")
        finally:
            cursor.close()
            conn.close()

        # Format for the Dashboard UI: (Label, Value, Color)
        return [
            ("Full Time", str(stats["Full Time"]), "#2E7D32"),
            ("Contract", str(stats["Contract"]), "#F9A825"),
            ("Interns", str(stats["Interns"]), "#0277BD"),
            ("On Leave", str(stats["On Leave"]), "#C62828")
        ]

    def fetch_dept_distribution(self):
        """
        Fetches Department Name and the count of Active employees in that department.
        """
        conn = self.get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        data = []

        try:
            query = """
                    SELECT d.DepName, COUNT(e.EmpID) as count
                    FROM Department d
                        LEFT JOIN Employee e \
                    ON d.DepID = e.DepID AND e.Active = 1
                    WHERE d.Active = 1
                    GROUP BY d.DepID, d.DepName \
                    """
            cursor.execute(query)
            results = cursor.fetchall()

            # Convert to list of tuples (Name, Count_String)
            for name, count in results:
                data.append((name, str(count)))

        except mysql.connector.Error as err:
            print(f"Error fetching departments: {err}")
        finally:
            cursor.close()
            conn.close()

        return data

    def fetch_contract_alerts(self):
        """
        Fetches contracts expiring in the next 30 days.
        Returns: List of tuples (Name + Dept, Expiry Message)
        """
        conn = self.get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        alerts = []

        try:
            # DATEDIFF returns (end_date - current_date) in days
            query = """
                    SELECT e.name, d.DepName, DATEDIFF(c.end_date, CURDATE()) as days_left
                    FROM Contract c
                             JOIN Employee e ON c.EmpID = e.EmpID
                             JOIN Department d ON e.DepID = d.DepID
                    WHERE c.Active = 1
                      AND c.end_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
                    ORDER BY days_left ASC LIMIT 5 \
                    """
            cursor.execute(query)
            results = cursor.fetchall()

            for name, dept, days in results:
                # Format the display string
                name_display = f"{name} ({dept})"
                if days == 0:
                    time_msg = "Expires Today"
                elif days == 1:
                    time_msg = "Expires in: 1 Day"
                else:
                    time_msg = f"Expires in: {days} Days"

                alerts.append((name_display, time_msg))

        except mysql.connector.Error as err:
            print(f"Error fetching alerts: {err}")
        finally:
            cursor.close()
            conn.close()

        return alerts

    def fetch_pending_leave_count(self):
        """
        Returns the number of LeaveRecord entries with status 'Pending'.
        """
        conn = self.get_connection()
        if not conn:
            return 0

        cursor = conn.cursor()
        count = 0
        try:
            query = "SELECT COUNT(*) FROM LeaveRecord WHERE status = 'Pending' AND Active = 1"
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                count = result[0]
        except mysql.connector.Error as err:
            print(f"Error fetching pending leaves: {err}")
        except Exception as e:
            print(f"Unexpected error fetching pending leaves: {e}")
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass

        return count