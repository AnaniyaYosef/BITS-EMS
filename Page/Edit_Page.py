import os
import sys
import customtkinter
from customtkinter import CTkScrollableFrame
from tkinter import filedialog as fd, TclError

# Ensure project root (containing DB_Service) is on sys.path when running this file directly.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from DB_Service.Edit_db import EditDB


class Edit(CTkScrollableFrame):
    def __init__(self, master):
        """Scrollable frame used to edit employee information."""
        super().__init__(master, width=800, height=600)

        # make root column stretch
        self.grid_columnconfigure(0, weight=1)

        # overall background kept clean / white to match theme
        self.configure(fg_color="white")

        # service layer for all database-related operations
        self.edit_db = EditDB()

        self._top_frame()
        self._middle_frame()
        self._address_frame()
        self._file_upload_frame()
        self._bottom_frame()

        # primary action button
        self.save_btn = customtkinter.CTkButton(
            self,
            text="Save changes",
            height=40,
            corner_radius=10,
            fg_color="#1faa5b",  # soft green accent
            hover_color="#17914b",
            command=self._save_employee,
        )
        self.save_btn.grid(row=5, column=0, pady=(10, 20), padx=20, sticky="e")

        self.grid(sticky="nsew", padx=10, pady=10)

    def _top_frame(self):
        """Header section with page title and search."""
        self._top_frame_container = customtkinter.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12,
        )
        self._top_frame_container.grid_columnconfigure(0, weight=1)
        self._top_frame_container.grid_columnconfigure(1, weight=0)

        self._title = customtkinter.CTkLabel(
            self._top_frame_container,
            text="Edit Employee Information",
            font=("Arial", 28, "bold"),
        )

        self._search_bar = customtkinter.CTkEntry(
            self._top_frame_container,
            placeholder_text="Search by employee ID",
            width=260,
            height=40,
            corner_radius=10,
        )
        self._search_btn = customtkinter.CTkButton(
            self._top_frame_container,
            text="Search",
            command=self.search_emp,
            height=36,
            corner_radius=10,
            fg_color="#1faa5b",
            hover_color="#17914b",
        )

        self._title.grid(
            row=0,
            column=0,
            padx=20,
            pady=(16, 8),
            columnspan=2,
            sticky="ew",
        )
        self._search_bar.grid(row=1, column=0, padx=(20, 10), pady=(0, 16), sticky="ew")
        self._search_btn.grid(row=1, column=1, padx=(0, 20), pady=(0, 16), sticky="e")

        self._top_frame_container.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(10, 5),
        )

    def _middle_frame(self):
        """Core employee details section."""
        self._container = customtkinter.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12,
        )
        self._container.grid_columnconfigure((0, 1), weight=1)

        self._full_name_label = customtkinter.CTkLabel(
            self._container, text="Full name"
        )
        self._full_name_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._emp_ID_label = customtkinter.CTkLabel(self._container, text="Employee ID")
        self._emp_ID_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._date_of_birth_label = customtkinter.CTkLabel(
            self._container, text="Date of birth"
        )
        self._date_of_birth_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._gender_label = customtkinter.CTkLabel(self._container, text="Gender")
        self._gender_entry = customtkinter.CTkOptionMenu(
            self._container, values=["Male", "Female"]
        )

        self._contact_num_label = customtkinter.CTkLabel(
            self._container, text="Contact number"
        )
        self._contact_num_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._emergency_contact_label = customtkinter.CTkLabel(
            self._container, text="Emergency Contact"
        )
        self._emergency_contact_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._email_label = customtkinter.CTkLabel(self._container, text="Email")
        self._email_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._hiring_date_label = customtkinter.CTkLabel(
            self._container, text="Hiring date"
        )
        self._hirirg_date_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._job_category_label = customtkinter.CTkLabel(
            self._container, text="Job Category"
        )
        self._job_category_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._department_label = customtkinter.CTkLabel(
            self._container, text="Department"
        )
        self._department_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        # layout
        label_padx = 20
        entry_padx = 20
        pady_small = (4, 0)
        pady_entry = (0, 10)

        self._full_name_label.grid(row=0, column=0, padx=label_padx, pady=pady_small, sticky="w")
        self._full_name_entry.grid(row=1, column=0, padx=entry_padx, pady=pady_entry, sticky="ew")

        self._emp_ID_label.grid(row=0, column=1, padx=label_padx, pady=pady_small, sticky="w")
        self._emp_ID_entry.grid(row=1, column=1, padx=entry_padx, pady=pady_entry, sticky="ew")

        self._date_of_birth_label.grid(row=2, column=0, padx=label_padx, pady=pady_small, sticky="w")
        self._date_of_birth_entry.grid(row=3, column=0, padx=entry_padx, pady=pady_entry, sticky="ew")

        self._gender_label.grid(row=2, column=1, padx=label_padx, pady=pady_small, sticky="w")
        self._gender_entry.grid(row=3, column=1, padx=entry_padx, pady=pady_entry, sticky="ew")

        self._contact_num_label.grid(row=4, column=0, padx=label_padx, pady=pady_small, sticky="w")
        self._contact_num_entry.grid(row=5, column=0, padx=entry_padx, pady=pady_entry, sticky="ew")

        self._emergency_contact_label.grid(row=4, column=1, padx=label_padx, pady=pady_small, sticky="w")
        self._emergency_contact_entry.grid(row=5, column=1, padx=entry_padx, pady=pady_entry, sticky="ew")

        self._email_label.grid(row=6, column=0, padx=label_padx, pady=pady_small, sticky="w")
        self._email_entry.grid(row=7, column=0, padx=entry_padx, pady=pady_entry, sticky="ew")

        self._hiring_date_label.grid(row=6, column=1, padx=label_padx, pady=pady_small, sticky="w")
        self._hirirg_date_entry.grid(row=7, column=1, padx=entry_padx, pady=pady_entry, sticky="ew")

        self._job_category_label.grid(row=8, column=1, padx=label_padx, pady=pady_small, sticky="w")
        self._job_category_entry.grid(row=9, column=1, padx=entry_padx, pady=pady_entry, sticky="ew")

        self._department_label.grid(row=10, column=1, padx=label_padx, pady=pady_small, sticky="w")
        self._department_entry.grid(row=11, column=1, padx=entry_padx, pady=(0, 20), sticky="ew")

        self._container.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="ew")

    def _bottom_frame(self):
        """Footer section with employment status."""
        self._bottom_frame_container = customtkinter.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12,
        )
        self._bottom_frame_container.grid_columnconfigure((0, 1), weight=1)

        self._employee_status_label = customtkinter.CTkLabel(
            self._bottom_frame_container,
            text="Employment status",
        )
        self._employee_status_entry = customtkinter.CTkOptionMenu(
            self._bottom_frame_container,
            values=["Full time", "Part time", "Intern"],
        )

        self._employee_status_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=(10, 10),
            sticky="e",
        )
        self._employee_status_entry.grid(
            row=0,
            column=1,
            padx=20,
            pady=(10, 10),
            sticky="w",
        )

        self._bottom_frame_container.grid(
            row=4,
            column=0,
            pady=(10, 5),
            padx=20,
            sticky="ew",
        )

    def _address_frame(self):
        """Address details section."""
        self._address_container = customtkinter.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12,
        )
        self._address_container.grid_columnconfigure((0, 1), weight=1)

        self._citizenship_label = customtkinter.CTkLabel(
            self._address_container, text="Citizenship"
        )
        self._citizenship_entry = customtkinter.CTkEntry(self._address_container)

        self._citizenship_label.grid(row=0, column=0)
        self._citizenship_entry.grid(row=1, column=0)

        self._city_label = customtkinter.CTkLabel(self._address_container, text="City")
        self._city_entry = customtkinter.CTkEntry(self._address_container)

        self._city_label.grid(row=0, column=1)
        self._city_entry.grid(row=1, column=1)

        self._subcity_label = customtkinter.CTkLabel(
            self._address_container, text="Subcity"
        )
        self._subcity_entry = customtkinter.CTkEntry(self._address_container)

        self._subcity_label.grid(row=2, column=0)
        self._subcity_entry.grid(row=3, column=0)

        self._woreda_label = customtkinter.CTkLabel(
            self._address_container, text="Woreda"
        )
        self._woreda_entry = customtkinter.CTkEntry(self._address_container)

        self._woreda_label.grid(row=2, column=1)
        self._woreda_entry.grid(row=3, column=1)

        self._kebele_label = customtkinter.CTkLabel(
            self._address_container, text="Kebele"
        )
        self._kebele_entry = customtkinter.CTkEntry(self._address_container)

        self._kebele_label.grid(row=4, column=0)
        self._kebele_entry.grid(row=5, column=0)

        self._houseNo_label = customtkinter.CTkLabel(
            self._address_container, text="House No."
        )
        self._houseNO_entry = customtkinter.CTkEntry(self._address_container)

        label_padx = 20
        entry_padx = 20
        pady_small = (4, 0)
        pady_entry = (0, 10)

        self._citizenship_label.grid(row=0, column=0, padx=label_padx, pady=pady_small, sticky="w")
        self._citizenship_entry.grid(row=1, column=0, padx=entry_padx, pady=pady_entry, sticky="ew")

        self._city_label.grid(row=0, column=1, padx=label_padx, pady=pady_small, sticky="w")
        self._city_entry.grid(row=1, column=1, padx=entry_padx, pady=pady_entry, sticky="ew")

        self._subcity_label.grid(row=2, column=0, padx=label_padx, pady=pady_small, sticky="w")
        self._subcity_entry.grid(row=3, column=0, padx=entry_padx, pady=pady_entry, sticky="ew")

        self._woreda_label.grid(row=2, column=1, padx=label_padx, pady=pady_small, sticky="w")
        self._woreda_entry.grid(row=3, column=1, padx=entry_padx, pady=pady_entry, sticky="ew")

        self._kebele_label.grid(row=4, column=0, padx=label_padx, pady=pady_small, sticky="w")
        self._kebele_entry.grid(row=5, column=0, padx=entry_padx, pady=pady_entry, sticky="ew")

        self._houseNo_label.grid(row=4, column=1, padx=label_padx, pady=pady_small, sticky="w")
        self._houseNO_entry.grid(row=5, column=1, padx=entry_padx, pady=pady_entry, sticky="ew")

        self._address_container.grid(row=2, column=0, padx=20, pady=(5, 5), sticky="ew")

    def _file_upload_frame(self):
        """Section with document upload shortcuts."""
        self.file_upload_container = customtkinter.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12,
        )
        self.file_upload_container.grid_columnconfigure((0, 1), weight=1)

        button_kwargs = {
            "height": 36,
            "corner_radius": 10,
            "fg_color": "#1faa5b",
            "hover_color": "#17914b",
        }

        self._certificate_button = customtkinter.CTkButton(
            self.file_upload_container,
            text="Upload Certificate",
            command=lambda: self._handle_file_upload("certificate"),
            **button_kwargs,
        )
        self._certificate_button.grid(row=0, column=0, padx=20, pady=(12, 6), sticky="ew")

        self._resume_button = customtkinter.CTkButton(
            self.file_upload_container,
            text="Upload CV / Resume",
            command=lambda: self._handle_file_upload("resume"),
            **button_kwargs,
        )
        self._resume_button.grid(row=0, column=1, padx=20, pady=(12, 6), sticky="ew")

        self._contract_button = customtkinter.CTkButton(
            self.file_upload_container,
            text="Upload Contract",
            command=lambda: self._handle_file_upload("contract"),
            **button_kwargs,
        )
        self._contract_button.grid(row=1, column=0, padx=20, pady=(6, 12), sticky="ew")

        self._id_document_button = customtkinter.CTkButton(
            self.file_upload_container,
            text="Upload ID Document",
            command=lambda: self._handle_file_upload("id_document"),
            **button_kwargs,
        )
        self._id_document_button.grid(row=1, column=1, padx=20, pady=(6, 12), sticky="ew")

        self.file_upload_container.grid(
            row=3,
            column=0,
            padx=20,
            pady=(5, 5),
            sticky="ew",
        )

    def search_emp(self):
        """Search employee by ID and populate the form."""
        emp_id_str: str = self._search_bar.get().strip()

        if not emp_id_str:
            self._show_error_popup("Error", "Please enter an employee ID.")
            return

        if not emp_id_str.isdigit():
            self._show_error_popup("Error", "Employee ID must be a number.")
            return

        emp_id = int(emp_id_str)

        # All DB interaction is delegated to EditDB
        employee_data = self.edit_db.get_employee_by_id(emp_id)

        if employee_data is None:
            self._show_error_popup("Employee not found", "No employee found with that ID.")
            return

        self._populate_employee_fields(employee_data)

    def _handle_file_upload(self, doc_kind: str) -> None:
        """Open file dialog and validate selected document."""
        # allowed readable document extensions
        allowed_exts = {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"}

        file_path = fd.askopenfilename(
            title="Select document",
            filetypes=[
                ("Documents", "*.pdf *.doc *.docx *.txt *.rtf *.odt"),
                ("All files", "*.*"),
            ],
        )

        # user cancelled
        if not file_path:
            return

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext not in allowed_exts:
            self._show_error_popup(
                "Invalid file",
                "Please select a document file (PDF, Word, text, etc.).\n"
                "Music and video files are not allowed.",
            )
            return

        # store the last selected path for potential later use
        setattr(self, f"{doc_kind}_file_path", file_path)

    def _show_error_popup(self, title: str, message: str) -> None:
        """Generic error popup used across the page."""
        new_window = customtkinter.CTkToplevel(self)
        new_window.title(title)
        new_window.geometry("400x200")
        new_window.resizable(False, False)
        new_window.wm_attributes("-topmost", True)

        # Make sure the window is visible before trying to grab focus
        new_window.update_idletasks()
        try:
            new_window.grab_set()
        except TclError:
            # If grab fails (e.g. window not viewable yet), ignore so it doesn't crash
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

    def _populate_employee_fields(self, data: dict) -> None:
        """Fill all widgets on the page from the employee data dictionary."""
        # Core info
        self._emp_ID_entry.delete(0, "end")
        self._emp_ID_entry.insert(0, str(data.get("emp_id", "")))

        self._full_name_entry.delete(0, "end")
        self._full_name_entry.insert(0, data.get("full_name", ""))

        self._date_of_birth_entry.delete(0, "end")
        self._date_of_birth_entry.insert(0, data.get("date_of_birth", ""))

        self._gender_entry.set(data.get("gender", ""))

        self._hirirg_date_entry.delete(0, "end")
        self._hirirg_date_entry.insert(0, data.get("hire_date", ""))

        # Contact and address-related info
        self._contact_num_entry.delete(0, "end")
        self._contact_num_entry.insert(0, data.get("phone_number", ""))

        self._emergency_contact_entry.delete(0, "end")
        self._emergency_contact_entry.insert(0, data.get("emergency_contact", ""))

        self._email_entry.delete(0, "end")
        self._email_entry.insert(0, data.get("email", ""))

        # Job / department
        self._job_category_entry.delete(0, "end")
        self._job_category_entry.insert(0, data.get("job_title", ""))

        self._department_entry.delete(0, "end")
        self._department_entry.insert(0, data.get("department", ""))

        # Employment status (option menu)
        employment_status = data.get("employment_status", "")
        if employment_status:
            self._employee_status_entry.set(employment_status)

        # Detailed address
        self._citizenship_entry.delete(0, "end")
        self._citizenship_entry.insert(0, data.get("citizenship", ""))

        self._city_entry.delete(0, "end")
        self._city_entry.insert(0, data.get("city", ""))

        self._subcity_entry.delete(0, "end")
        self._subcity_entry.insert(0, data.get("sub_city", ""))

        self._woreda_entry.delete(0, "end")
        self._woreda_entry.insert(0, data.get("woreda", ""))

        self._kebele_entry.delete(0, "end")
        self._kebele_entry.insert(0, data.get("kebele", ""))

        self._houseNO_entry.delete(0, "end")
        self._houseNO_entry.insert(0, str(data.get("house_number", "")))

    def _collect_employee_form_data(self) -> Optional[dict]:
        """
        Collect and lightly validate form values before saving.

        Returns a dict matching the structure expected by EditDB.update_employee,
        or None if validation fails (and a popup is shown).
        """
        emp_id_str = self._emp_ID_entry.get().strip()
        if not emp_id_str or not emp_id_str.isdigit():
            self._show_error_popup("Error", "Employee ID must be a non-empty number.")
            return None

        full_name = self._full_name_entry.get().strip()
        if not full_name:
            self._show_error_popup("Error", "Full name cannot be empty.")
            return None

        date_of_birth = self._date_of_birth_entry.get().strip()
        hire_date = self._hirirg_date_entry.get().strip()

        email = self._email_entry.get().strip()
        if not email:
            self._show_error_popup("Error", "Email cannot be empty.")
            return None

        data = {
            "full_name": full_name,
            "date_of_birth": date_of_birth,
            "gender": self._gender_entry.get().strip(),
            "hire_date": hire_date,
            "employment_status": self._employee_status_entry.get().strip(),
            "department": self._department_entry.get().strip(),
            "job_title": self._job_category_entry.get().strip(),
            "citizenship": self._citizenship_entry.get().strip(),
            "city": self._city_entry.get().strip(),
            "sub_city": self._subcity_entry.get().strip(),
            "woreda": self._woreda_entry.get().strip(),
            "kebele": self._kebele_entry.get().strip(),
            "house_number": self._houseNO_entry.get().strip(),
            "phone_number": self._contact_num_entry.get().strip(),
            "emergency_contact": self._emergency_contact_entry.get().strip(),
            "email": email,
        }

        return data

    def _save_employee(self) -> None:
        """Validate and save edited employee data via EditDB."""
        form_data = self._collect_employee_form_data()
        if form_data is None:
            return

        emp_id = int(self._emp_ID_entry.get().strip())

        try:
            success = self.edit_db.update_employee(emp_id, form_data)
        except Exception:
            success = False

        if success:
            self._show_error_popup("Success", "Employee information updated successfully.")
        else:
            self._show_error_popup(
                "Update failed",
                "Could not update employee information.\n"
                "Please check your input or try again later.",
            )

# for testing

if __name__ == "__main__":
    customtkinter.set_appearance_mode("Light")
    customtkinter.set_default_color_theme("green")

    root = customtkinter.CTk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.title("Edit page")
    Edit(root)
    root.mainloop()
