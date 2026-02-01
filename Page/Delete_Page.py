import os
import sys
import customtkinter
from customtkinter import CTkScrollableFrame
from tkinter import TclError

# Ensure project root (containing DB_Service) is on sys.path when running this file directly.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from DB_Service.Delete_db import DeleteDB


class DeleteEmployeePage(CTkScrollableFrame):
    """Page that allows searching for and deleting an employee by ID."""

    def __init__(self, master):
        super().__init__(master, width=300, height=200)

        self.grid_columnconfigure(0, weight=1)
        self.configure(fg_color="white")

        # DB service
        self.delete_db = DeleteDB()

        self._build_ui()

        self.grid(sticky="nsew", padx=10, pady=10)

    def _build_ui(self) -> None:
        """Create the search and delete controls."""
        self._container = customtkinter.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12,
        )
        self._container.grid_columnconfigure(0, weight=1)
        self._container.grid_columnconfigure(1, weight=0)

        title = customtkinter.CTkLabel(
            self._container,
            text="Delete Employee",
            font=("Arial", 26, "bold"),
        )

        self._search_entry = customtkinter.CTkEntry(
            self._container,
            placeholder_text="Enter employee ID",
            width=220,
            height=40,
            corner_radius=10,
        )
        self._search_button = customtkinter.CTkButton(
            self._container,
            text="Search",
            height=36,
            corner_radius=10,
            fg_color="#1faa5b",
            hover_color="#17914b",
            command=self._on_search_clicked,
        )

        self._delete_button = customtkinter.CTkButton(
            self._container,
            text="Delete employee",
            height=40,
            corner_radius=10,
            fg_color="#e53935",
            hover_color="#c62828",
            state="disabled",
            command=self._on_delete_clicked,
        )

        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(16, 8), sticky="w")
        self._search_entry.grid(row=1, column=0, padx=(20, 10), pady=(0, 16), sticky="ew")
        self._search_button.grid(row=1, column=1, padx=(0, 20), pady=(0, 16), sticky="e")
        self._delete_button.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 16), sticky="e")

        self._container.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 5))

        # Track currently-found employee
        self._current_emp_id = None

    def _on_search_clicked(self) -> None:
        """Search for an employee and show a popup about the result."""
        emp_id_str = self._search_entry.get().strip()

        if not emp_id_str:
            self._show_popup("Error", "Please enter an employee ID.")
            self._current_emp_id = None
            self._delete_button.configure(state="disabled")
            return

        if not emp_id_str.isdigit():
            self._show_popup("Error", "Employee ID must be a number.")
            self._current_emp_id = None
            self._delete_button.configure(state="disabled")
            return

        emp_id = int(emp_id_str)
        employee = self.delete_db.get_employee_by_id(emp_id)

        if employee is None:
            self._show_popup("Employee doesn't exist", "No employee found with that ID.")
            self._current_emp_id = None
            self._delete_button.configure(state="disabled")
        else:
            # Employee exists; enable delete button and inform user
            self._current_emp_id = emp_id
            self._delete_button.configure(state="normal")

            name = employee.get("full_name", f"ID {emp_id}")
            self._show_popup(
                "Employee found",
                f"Employee '{name}' was found.\nYou can now delete this employee.",
            )

    def _on_delete_clicked(self) -> None:
        """Ask for confirmation then perform deletion."""
        if self._current_emp_id is None:
            self._show_popup("Error", "No employee selected to delete.")
            return

        # Confirmation popup
        def _confirm_proceed():
            self._perform_delete()

        self._show_confirmation_popup(
            "Confirm delete",
            "This action cannot be undone.\n\n"
            "Are you sure you want to permanently delete this employee?",
            on_proceed=_confirm_proceed,
        )

    def _perform_delete(self) -> None:
        """Call the DB service to delete the employee and show result."""
        emp_id = self._current_emp_id
        if emp_id is None:
            self._show_popup("Error", "No employee selected to delete.")
            return

        try:
            success = self.delete_db.delete_employee(emp_id)
        except Exception:
            success = False

        if success:
            self._show_popup("Deleted", "Employee deleted successfully.")
            self._delete_button.configure(state="disabled")
            self._current_emp_id = None
        else:
            self._show_popup(
                "Deletion failed",
                "Could not delete the employee.\nPlease try again or contact support.",
            )

    def _show_popup(self, title: str, message: str) -> None:
        """Generic info/error popup with a Close button."""
        new_window = customtkinter.CTkToplevel(self)
        new_window.title(title)
        new_window.geometry("400x200")
        new_window.resizable(False, False)
        new_window.wm_attributes("-topmost", True)

        new_window.update_idletasks()
        try:
            new_window.grab_set()
        except TclError:
            pass

        container = customtkinter.CTkFrame(
            new_window,
            fg_color="white",
            corner_radius=12,
        )
        container.pack(expand=True, fill="both", padx=20, pady=20)

        label = customtkinter.CTkLabel(
            container,
            text=message,
            font=("Arial", 14),
            wraplength=340,
            justify="center",
        )
        label.pack(pady=(10, 10))

        close_btn = customtkinter.CTkButton(
            container,
            text="Close",
            command=new_window.destroy,
            fg_color="#1faa5b",
            hover_color="#17914b",
            corner_radius=10,
            width=120,
        )
        close_btn.pack(pady=(5, 10))

    def _show_confirmation_popup(self, title: str, message: str, on_proceed) -> None:
        """Confirmation popup with Cancel / Proceed buttons."""
        new_window = customtkinter.CTkToplevel(self)
        new_window.title(title)
        new_window.geometry("420x220")
        new_window.resizable(False, False)
        new_window.wm_attributes("-topmost", True)

        new_window.update_idletasks()
        try:
            new_window.grab_set()
        except TclError:
            pass

        container = customtkinter.CTkFrame(
            new_window,
            fg_color="white",
            corner_radius=12,
        )
        container.pack(expand=True, fill="both", padx=20, pady=20)

        label = customtkinter.CTkLabel(
            container,
            text=message,
            font=("Arial", 14),
            wraplength=360,
            justify="center",
        )
        label.pack(pady=(10, 10))

        button_frame = customtkinter.CTkFrame(
            container,
            fg_color="transparent",
        )
        button_frame.pack(pady=(5, 10))

        cancel_btn = customtkinter.CTkButton(
            button_frame,
            text="Cancel",
            command=new_window.destroy,
            corner_radius=10,
            width=120,
        )

        def _on_proceed_clicked():
            new_window.destroy()
            on_proceed()

        proceed_btn = customtkinter.CTkButton(
            button_frame,
            text="Proceed",
            command=_on_proceed_clicked,
            fg_color="#e53935",
            hover_color="#c62828",
            corner_radius=10,
            width=120,
        )

        cancel_btn.grid(row=0, column=0, padx=10)
        proceed_btn.grid(row=0, column=1, padx=10)


if __name__ == "__main__":
    customtkinter.set_appearance_mode("Light")
    customtkinter.set_default_color_theme("green")

    root = customtkinter.CTk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.title("Delete employee")

    DeleteEmployeePage(root)

    root.mainloop()

