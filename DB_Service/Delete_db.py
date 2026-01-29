"""
Service layer for deleting employees from the database.
Works with the existing BITS-EMS MySQL schema.
"""

import mysql.connector
from typing import Any, Dict, Optional


class DeleteDB:
    def __init__(self, connection_params: Optional[Dict[str, Any]] = None) -> None:
        self._conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sql2707",
            database="bits-ems",
        )
        self._cursor = self._conn.cursor(dictionary=True)

    # --------------------------------------------------
    # Get employee info (used before delete confirmation)
    # --------------------------------------------------
    def get_employee_by_id(self, emp_id: int) -> Optional[Dict[str, Any]]:
        query = """
        SELECT
            e.EmpID       AS emp_id,
            e.name        AS full_name,
            d.DepName     AS department,
            jt.title_name AS job_title
        FROM employee e
        LEFT JOIN department d ON e.DepID = d.DepID
        LEFT JOIN jobtitle jt ON e.job_title_id = jt.job_title_id
        WHERE e.EmpID = %s AND e.active = 1
        """
        self._cursor.execute(query, (emp_id,))
        result = self._cursor.fetchone()
        return result  # None if not found

    # --------------------------------------------------
    # Soft delete (recommended)
    # --------------------------------------------------
    def delete_employee(self, emp_id: int) -> bool:
        try:
            query = """
            UPDATE employee
            SET active = 0
            WHERE EmpID = %s AND active = 1
            """
            self._cursor.execute(query, (emp_id,))
            self._conn.commit()
            return self._cursor.rowcount > 0
        except Exception as e:
            print("Delete employee error:", e)
            self._conn.rollback()
            return False