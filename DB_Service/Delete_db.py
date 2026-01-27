"""
Service layer for deleting employees from the database.

All actual database access should be implemented here so that the UI code in
`Page/Delete_Page.py` never talks directly to the database.

The database is not available on this machine, so all methods are written in a
way that they can be easily configured by whoever has access to the real DB.
"""

from typing import Any, Dict, Optional


class DeleteDB:
    """
    Entry-point for delete operations used by the Delete page.

    The person who has access to the database should:
    - Initialize the real DB connection inside __init__
    - Implement get_employee_by_id so it returns a small info dict (or None)
    - Implement delete_employee so it actually deletes the employee and any
      related data (or marks them inactive), and returns True/False.
    """

    def __init__(self, connection_params: Optional[Dict[str, Any]] = None) -> None:
        """
        Configure your database connection here.

        Examples (to be implemented by the DB owner, not here):
            import mysql.connector
            self._conn = mysql.connector.connect(
                host=connection_params["host"],
                user=connection_params["user"],
                password=connection_params["password"],
                database="BITS_EMS",
            )
        """
        self._connection_params = connection_params or {}
        # NOTE: No real connection is created here on purpose.

    def get_employee_by_id(self, emp_id: int) -> Optional[Dict[str, Any]]:
        """
        Check whether an employee exists before deletion.

        EXPECTED RETURN VALUE
        ---------------------
        Either:
            None  -> when the employee does not exist
        or:
            A small dictionary with some identifying information for display
            in the UI, for example:

            {
                "emp_id": int,          # Employee.EmpID
                "full_name": str,      # Employee.name
                "department": str,     # Department.DepName
                "job_title": str,      # JobTitle.title_name
            }

        SUGGESTED SQL (for the DB owner)
        --------------------------------
        SELECT
            e.EmpID,
            e.name,
            d.DepName,
            jt.title_name
        FROM Employee e
        LEFT JOIN Department d ON e.DepID = d.DepID
        LEFT JOIN JobTitle jt ON e.job_title_id = jt.job_title_id
        WHERE e.EmpID = %s;
        """

        # Placeholder implementation so the UI can run without a DB.
        # Return None so the page shows "employee doesn't exist" instead of crashing.
        return None

    def delete_employee(self, emp_id: int) -> bool:
        """
        Permanently delete (or deactivate) an employee and related data.

        RETURN VALUE
        ------------
        - True  -> deletion succeeded
        - False -> deletion failed (invalid ID, DB error, foreign key constraint, etc.)

        SUGGESTED APPROACH (for the DB owner)
        -------------------------------------
        - Start a transaction
        - Either:
            a) Hard delete from child tables (Document, Address, Contract,
               LeaveRecord, employee_History, UserAccount, etc.) then delete
               from Employee
           OR
            b) Preferably set the `Active` flags to FALSE on related rows and
               Employee, instead of hard-deleting
        - Commit on success, or roll back and return False on error
        """

        # Placeholder implementation so the UI can run without a DB.
        # The DB owner should replace this with real deletion logic and
        # return True/False based on whether the operation succeeded.
        return False

