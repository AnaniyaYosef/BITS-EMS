"""
Service layer for employee-related database operations used by the Edit page.

All actual database access should be implemented here so that the UI code in
`Page/Edit_Page.py` never talks directly to the database.

The database is not available on this machine, so all methods are written in a
way that they can be easily configured by whoever has access to the real DB.
"""

from typing import Any, Dict, Optional


class EditDB:
    """
    Entry-point for fetching employee data for the Edit page.

    The person who has access to the database should:
    - Initialize the real DB connection inside __init__
    - Implement get_employee_by_id so it returns the expected dictionary
      (or None if no employee is found).
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
        Look up an employee and all related data needed for the Edit page.

        EXPECTED RETURN VALUE
        ---------------------
        Either:
            None  -> when the employee does not exist
        or:
            A dictionary with (at least) the following keys so that the UI
            can populate all fields:

            {
                "emp_id": int,                  # Employee.EmpID
                "full_name": str,              # Employee.name
                "date_of_birth": str,          # Employee.date_of_birth  (YYYY-MM-DD)
                "gender": str,                 # Employee.gender
                "hire_date": str,              # Employee.hire_date      (YYYY-MM-DD)
                "employment_status": str,      # Employee.employment_status
                "department": str,             # Department.DepName
                "job_title": str,              # JobTitle.title_name
                "citizenship": str,            # Address.Citizenship
                "city": str,                   # Address.city
                "sub_city": str,               # Address.sub_city
                "woreda": str,                 # Address.woreda
                "kebele": str,                 # Address.kebele
                "house_number": str,           # Address.house_number
                "phone_number": str,           # Address.phone_number
                "emergency_contact": str,      # Address.emergency_contact
                "email": str,                  # Address.email
            }

        SUGGESTED SQL (for the DB owner)
        --------------------------------
        SELECT
            e.EmpID,
            e.name,
            e.date_of_birth,
            e.gender,
            e.hire_date,
            e.employment_status,
            d.DepName,
            jt.title_name,
            a.Citizenship,
            a.city,
            a.sub_city,
            a.woreda,
            a.kebele,
            a.house_number,
            a.phone_number,
            a.emergency_contact,
            a.email
        FROM Employee e
        LEFT JOIN Department d ON e.DepID = d.DepID
        LEFT JOIN JobTitle jt ON e.job_title_id = jt.job_title_id
        LEFT JOIN Address a ON e.EmpID = a.EmpID
        WHERE e.EmpID = %s;
        """

        # Placeholder implementation so the UI can run without a DB.
        # Return None so the page shows "employee not found" instead of crashing.
        #
        # The DB owner should replace everything below with real DB logic:
        #   - run the SQL
        #   - fetch one row
        #   - map the row into the dictionary structure described above
        return None

    def update_employee(self, emp_id: int, data: Dict[str, Any]) -> bool:
        """
        Persist changes to an existing employee.

        EXPECTED INPUT
        --------------
        emp_id:
            The numeric employee ID (Employee.EmpID) to update.

        data:
            Dictionary with the same keys produced/consumed by get_employee_by_id:

            {
                "full_name": str,
                "date_of_birth": str,      # YYYY-MM-DD
                "gender": str,
                "hire_date": str,          # YYYY-MM-DD
                "employment_status": str,
                "department": str,         # Department name (DepName)
                "job_title": str,          # Job title name (JobTitle.title_name)
                "citizenship": str,
                "city": str,
                "sub_city": str,
                "woreda": str,
                "kebele": str,
                "house_number": str,
                "phone_number": str,
                "emergency_contact": str,
                "email": str,
            }

        RETURN VALUE
        ------------
        - True  -> update succeeded
        - False -> update failed (invalid data, DB error, etc.)

        SUGGESTED APPROACH (for the DB owner)
        -------------------------------------
        - Start a transaction
        - Update Employee (name, date_of_birth, gender, hire_date, employment_status)
        - Resolve department name -> DepID, and job title name -> job_title_id
        - Update Department / JobTitle references if needed
        - Update Address row for the given EmpID
        - Commit on success, or roll back and return False on error
        """

        # Placeholder implementation so the UI can run without a DB.
        # The DB owner should replace this with real update logic and
        # return True/False based on whether the UPDATEs succeeded.
        return False
