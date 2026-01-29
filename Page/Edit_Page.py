import os
import sys
import customtkinter
from customtkinter import CTkScrollableFrame
from tkinter import filedialog as fd, TclError, messagebox
from typing import Optional
from datetime import datetime

# Ensure project root is on sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from DB_Service.Edit_db import EditDB


class Edit(CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width=800, height=600)
        self.grid_columnconfigure(0, weight=1)
        self.configure(fg_color="white")

        self.edit_db = EditDB()  # DB service
        self.current_emp_id = None  # Track current employee being edited

        self._top_frame()
        self._middle_frame()
        self._address_frame()
        self._file_upload_frame()
        self._bottom_frame()

        self.save_btn = customtkinter.CTkButton(
            self,
            text="Save changes",
            height=40,
            corner_radius=10,
            fg_color="#1faa5b",
            hover_color="#17914b",
            command=self._save_employee,
        )
        self.save_btn.grid(row=5, column=0, pady=(10, 20), padx=20, sticky="e")
        self.grid(sticky="nsew", padx=10, pady=10)

    # ---------------- Top Frame ----------------
    def _top_frame(self):
        self._top_frame_container = customtkinter.CTkFrame(
            self, fg_color="white", corner_radius=12
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
            placeholder_text="Search by employee ID or name",
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

        self._title.grid(row=0, column=0, padx=20, pady=(16, 8), columnspan=2, sticky="ew")
        self._search_bar.grid(row=1, column=0, padx=(20, 10), pady=(0, 16), sticky="ew")
        self._search_btn.grid(row=1, column=1, padx=(0, 20), pady=(0, 16), sticky="e")
        self._top_frame_container.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 5))

    # ---------------- Middle Frame ----------------
    def _middle_frame(self):
        self._container = customtkinter.CTkFrame(self, fg_color="white", corner_radius=12)
        self._container.grid_columnconfigure((0, 1), weight=1)

        # Employee fields
        self._full_name_label = customtkinter.CTkLabel(self._container, text="Full name")
        self._full_name_entry = customtkinter.CTkEntry(self._container, width=250, height=40)

        self._emp_ID_label = customtkinter.CTkLabel(self._container, text="Employee ID")
        self._emp_ID_entry = customtkinter.CTkEntry(self._container, width=250, height=40)

        self._date_of_birth_label = customtkinter.CTkLabel(self._container, text="Date of birth")
        self._date_of_birth_entry = customtkinter.CTkEntry(self._container, width=250, height=40)

        self._gender_label = customtkinter.CTkLabel(self._container, text="Gender")
        self._gender_entry = customtkinter.CTkOptionMenu(self._container, values=["Male", "Female"])

        self._contact_num_label = customtkinter.CTkLabel(self._container, text="Contact number")
        self._contact_num_entry = customtkinter.CTkEntry(self._container, width=250, height=40)

        self._emergency_contact_label = customtkinter.CTkLabel(self._container, text="Emergency Contact")
        self._emergency_contact_entry = customtkinter.CTkEntry(self._container, width=250, height=40)

        self._email_label = customtkinter.CTkLabel(self._container, text="Email")
        self._email_entry = customtkinter.CTkEntry(self._container, width=250, height=40)

        self._hiring_date_label = customtkinter.CTkLabel(self._container, text="Hiring date")
        self._hiring_date_entry = customtkinter.CTkEntry(self._container, width=250, height=40)

        self._job_category_label = customtkinter.CTkLabel(self._container, text="Job Category")
        self._job_category_entry = customtkinter.CTkEntry(self._container, width=250, height=40)

        self._department_label = customtkinter.CTkLabel(self._container, text="Department")
        self._department_entry = customtkinter.CTkEntry(self._container, width=250, height=40)

        pad_x = 20
        pady_small = (4, 0)
        pady_entry = (0, 10)

        self._full_name_label.grid(row=0, column=0, padx=pad_x, pady=pady_small, sticky="w")
        self._full_name_entry.grid(row=1, column=0, padx=pad_x, pady=pady_entry, sticky="ew")
        self._emp_ID_label.grid(row=0, column=1, padx=pad_x, pady=pady_small, sticky="w")
        self._emp_ID_entry.grid(row=1, column=1, padx=pad_x, pady=pady_entry, sticky="ew")
        self._date_of_birth_label.grid(row=2, column=0, padx=pad_x, pady=pady_small, sticky="w")
        self._date_of_birth_entry.grid(row=3, column=0, padx=pad_x, pady=pady_entry, sticky="ew")
        self._gender_label.grid(row=2, column=1, padx=pad_x, pady=pady_small, sticky="w")
        self._gender_entry.grid(row=3, column=1, padx=pad_x, pady=pady_entry, sticky="ew")
        self._contact_num_label.grid(row=4, column=0, padx=pad_x, pady=pady_small, sticky="w")
        self._contact_num_entry.grid(row=5, column=0, padx=pad_x, pady=pady_entry, sticky="ew")
        self._emergency_contact_label.grid(row=4, column=1, padx=pad_x, pady=pady_small, sticky="w")
        self._emergency_contact_entry.grid(row=5, column=1, padx=pad_x, pady=pady_entry, sticky="ew")
        self._email_label.grid(row=6, column=0, padx=pad_x, pady=pady_small, sticky="w")
        self._email_entry.grid(row=7, column=0, padx=pad_x, pady=pady_entry, sticky="ew")
        self._hiring_date_label.grid(row=6, column=1, padx=pad_x, pady=pady_small, sticky="w")
        self._hiring_date_entry.grid(row=7, column=1, padx=pad_x, pady=pady_entry, sticky="ew")
        self._job_category_label.grid(row=8, column=1, padx=pad_x, pady=pady_small, sticky="w")
        self._job_category_entry.grid(row=9, column=1, padx=pad_x, pady=pady_entry, sticky="ew")
        self._department_label.grid(row=10, column=1, padx=pad_x, pady=pady_small, sticky="w")
        self._department_entry.grid(row=11, column=1, padx=pad_x, pady=(0, 20), sticky="ew")

        self._container.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="ew")

    # ---------------- Address Frame ----------------
    def _address_frame(self):
        self._address_container = customtkinter.CTkFrame(self, fg_color="white", corner_radius=12)
        self._address_container.grid_columnconfigure((0, 1), weight=1)

        labels_entries = [
            ("Citizenship", "_citizenship_entry"),
            ("City", "_city_entry"),
            ("Subcity", "_subcity_entry"),
            ("Woreda", "_woreda_entry"),
            ("Kebele", "_kebele_entry"),
            ("House No.", "_houseNO_entry"),
        ]
        for i, (label_text, attr_name) in enumerate(labels_entries):
            lbl = customtkinter.CTkLabel(self._address_container, text=label_text)
            ent = customtkinter.CTkEntry(self._address_container)
            setattr(self, f"{attr_name}_label", lbl)
            setattr(self, attr_name, ent)
            row, col = divmod(i, 2)
            lbl.grid(row=row*2, column=col, padx=20, pady=(4, 0), sticky="w")
            ent.grid(row=row*2+1, column=col, padx=20, pady=(0, 10), sticky="ew")

        self._address_container.grid(row=2, column=0, padx=20, pady=(5, 5), sticky="ew")

    # ---------------- File Upload ----------------
    def _file_upload_frame(self):
        self.file_upload_container = customtkinter.CTkFrame(self, fg_color="white", corner_radius=12)
        self.file_upload_container.grid_columnconfigure((0, 1), weight=1)
        button_kwargs = {"height": 36, "corner_radius": 10, "fg_color": "#1faa5b", "hover_color": "#17914b"}

        for i, doc_name in enumerate(["certificate", "resume", "contract", "id_document"]):
            btn = customtkinter.CTkButton(
                self.file_upload_container,
                text=f"Upload {doc_name.replace('_',' ').title()}",
                command=lambda kind=doc_name: self._handle_file_upload(kind),
                **button_kwargs,
            )
            btn.grid(row=i//2, column=i%2, padx=20, pady=(12 if i<2 else 6, 6 if i<2 else 12), sticky="ew")

        self.file_upload_container.grid(row=3, column=0, padx=20, pady=(5, 5), sticky="ew")

    # ---------------- Bottom Frame ----------------
    def _bottom_frame(self):
        self._bottom_frame_container = customtkinter.CTkFrame(self, fg_color="white", corner_radius=12)
        self._bottom_frame_container.grid_columnconfigure((0, 1), weight=1)

        self._employee_status_label = customtkinter.CTkLabel(self._bottom_frame_container, text="Employment status")
        self._employee_status_entry = customtkinter.CTkOptionMenu(
            self._bottom_frame_container, values=["Full time", "Part time", "Intern"]
        )
        self._employee_status_label.grid(row=0, column=0, padx=20, pady=(10,10), sticky="e")
        self._employee_status_entry.grid(row=0, column=1, padx=20, pady=(10,10), sticky="w")
        self._bottom_frame_container.grid(row=4, column=0, pady=(10,5), padx=20, sticky="ew")

    # ---------------- Search ----------------
    def search_emp(self):
        emp_id_str = self._search_bar.get().strip()
        if not emp_id_str:
            self._show_error_popup("Error", "Please enter an employee ID or name.")
            return
        if emp_id_str.isdigit():
            emp_id = int(emp_id_str)
            employee_data = self.edit_db.get_employee_by_id(emp_id)
            if not employee_data:
                self._show_error_popup("Not found", f"No employee with ID {emp_id}")
                return
            self.current_emp_id = emp_id
            self._populate_employee_fields(employee_data)
        else:
            matches = self.edit_db.search_employee_by_name(emp_id_str)
            if not matches:
                self._show_error_popup("Not found", f"No employees match '{emp_id_str}'")
                return
            elif len(matches) == 1:
                employee_data = self.edit_db.get_employee_by_id(matches[0]['EmpID'])
                self.current_emp_id = matches[0]['EmpID']
                self._populate_employee_fields(employee_data)
            else:
                self._show_suggestion_popup(matches)

    def _show_suggestion_popup(self, matches):
        popup = customtkinter.CTkToplevel(self)
        popup.title("Select Employee")
        popup.geometry("400x300")
        popup.grab_set()

        container = customtkinter.CTkFrame(popup, fg_color="white")
        container.pack(expand=True, fill="both", padx=20, pady=20)

        label = customtkinter.CTkLabel(container, text="Multiple employees found. Please select one:")
        label.pack(pady=(0,10))

        for emp in matches:
            btn = customtkinter.CTkButton(
                container,
                text=f"{emp['name']} (ID: {emp['EmpID']})",
                command=lambda emp_id=emp['EmpID']: self._select_employee_from_suggestion(emp_id, popup),
                fg_color="#1faa5b",
                hover_color="#17914b",
                corner_radius=8
            )
            btn.pack(fill="x", pady=5)

    def _select_employee_from_suggestion(self, emp_id, popup):
        popup.destroy()
        employee_data = self.edit_db.get_employee_by_id(emp_id)
        self.current_emp_id = emp_id
        self._populate_employee_fields(employee_data)

    # ---------------- File upload ----------------
    def _handle_file_upload(self, doc_kind: str):
        allowed_exts = {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"}
        file_path = fd.askopenfilename(title="Select document",
                                       filetypes=[("Documents","*.pdf *.doc *.docx *.txt *.rtf *.odt"),
                                                  ("All files","*.*")])
        if not file_path:
            return
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in allowed_exts:
            self._show_error_popup("Invalid file", "Please select a document file (PDF, Word, text, etc.)")
            return
        setattr(self, f"{doc_kind}_file_path", file_path)
        
        # Save the document to database if an employee is selected
        if self.current_emp_id:
            try:
                from DB_Service.DocumentDB import DocumentDB
                doc_db = DocumentDB()
                doc_db.add_document(
                    emp_id=self.current_emp_id,
                    document_type=doc_kind.title(),
                    file_path=file_path
                )
                doc_db.close()
                messagebox.showinfo("Success", f"{doc_kind.title()} uploaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save document: {str(e)}")

    # ---------------- Error popup ----------------
    def _show_error_popup(self, title: str, message: str):
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
        container = customtkinter.CTkFrame(new_window, fg_color="white", corner_radius=12)
        container.pack(expand=True, fill="both", padx=20, pady=20)
        label = customtkinter.CTkLabel(container, text=message, font=("Arial",14), wraplength=340, justify="center")
        label.pack(pady=(10,10))
        close_btn = customtkinter.CTkButton(container, text="Close", command=new_window.destroy,
                                           fg_color="#1faa5b", hover_color="#17914b", corner_radius=10, width=120)
        close_btn.pack(pady=(5,10))

    # ---------------- Populate ----------------
    def _populate_employee_fields(self, data: dict):
        if not data:
            return
        self._emp_ID_entry.delete(0, "end")
        self._emp_ID_entry.insert(0, str(data.get("EmpID","")))
        self._full_name_entry.delete(0, "end")
        self._full_name_entry.insert(0, data.get("name",""))
        self._date_of_birth_entry.delete(0, "end")
        self._date_of_birth_entry.insert(0, str(data.get("date_of_birth","")))
        self._gender_entry.set(data.get("gender",""))
        self._hiring_date_entry.delete(0, "end")
        self._hiring_date_entry.insert(0, str(data.get("hire_date","")))
        self._contact_num_entry.delete(0, "end")
        self._contact_num_entry.insert(0, data.get("contact_number",""))
        self._emergency_contact_entry.delete(0, "end")
        self._emergency_contact_entry.insert(0, data.get("emergency_contact",""))
        self._email_entry.delete(0, "end")
        self._email_entry.insert(0, data.get("email",""))
        self._job_category_entry.delete(0, "end")
        self._job_category_entry.insert(0, str(data.get("job_title_id","")))
        self._department_entry.delete(0, "end")
        self._department_entry.insert(0, str(data.get("DepID","")))
        employment_status = data.get("employment_status","")
        if employment_status:
            self._employee_status_entry.set(employment_status)

        # Address fields
        for field_name, db_key in [
            ("_citizenship_entry", "citizenship"),
            ("_city_entry", "city"),
            ("_subcity_entry", "sub_city"),
            ("_woreda_entry", "woreda"),
            ("_kebele_entry", "kebele"),
            ("_houseNO_entry", "house_number")
        ]:
            widget = getattr(self, field_name, None)
            if widget:
                widget.delete(0,"end")
                widget.insert(0, str(data.get(db_key,"")))

    # ---------------- Collect form ----------------
    def _collect_employee_form_data(self) -> Optional[dict]:
        emp_id_str = self._emp_ID_entry.get().strip()
        if not emp_id_str or not emp_id_str.isdigit():
            self._show_error_popup("Error", "Employee ID must be a non-empty number.")
            return None

        full_name = self._full_name_entry.get().strip()
        if not full_name:
            self._show_error_popup("Error", "Full name cannot be empty.")
            return None

        date_of_birth = self._date_of_birth_entry.get().strip()
        hire_date = self._hiring_date_entry.get().strip()

        # Validate date formats
        try:
            if date_of_birth:
                datetime.strptime(date_of_birth, "%Y-%m-%d")
            if hire_date:
                datetime.strptime(hire_date, "%Y-%m-%d")
        except ValueError:
            self._show_error_popup("Error", "Invalid date format. Use YYYY-MM-DD")
            return None

        email = self._email_entry.get().strip()
        if not email:
            self._show_error_popup("Error", "Email cannot be empty.")
            return None

        # Collect all data
        data = {
            "EmpID": int(emp_id_str),
            "name": full_name,
            "date_of_birth": date_of_birth,
            "gender": self._gender_entry.get(),
            "hire_date": hire_date,
            "employment_status": self._employee_status_entry.get(),
            "DepID": self._department_entry.get().strip(),
            "job_title_id": self._job_category_entry.get().strip(),
            "contact_number": self._contact_num_entry.get().strip(),
            "emergency_contact": self._emergency_contact_entry.get().strip(),
            "email": email,
            "citizenship": self._citizenship_entry.get().strip(),
            "city": self._city_entry.get().strip(),
            "sub_city": self._subcity_entry.get().strip(),
            "woreda": self._woreda_entry.get().strip(),
            "kebele": self._kebele_entry.get().strip(),
            "house_number": self._houseNO_entry.get().strip(),
        }

        return data

    # ---------------- Save employee ----------------
    def _save_employee(self):
        """Save the edited employee data to database"""
        form_data = self._collect_employee_form_data()
        if form_data is None:
            return

        # Convert DepID and job_title_id to integers if they're digits
        try:
            if form_data["DepID"].isdigit():
                form_data["DepID"] = int(form_data["DepID"])
            if form_data["job_title_id"].isdigit():
                form_data["job_title_id"] = int(form_data["job_title_id"])
        except (ValueError, AttributeError):
            pass

        emp_id = form_data["EmpID"]
        
        try:
            success = self.edit_db.update_employee(emp_id, form_data)
            if success:
                self._show_error_popup("Success", "Employee information updated successfully!")
                # Clear the form after successful save
                self._clear_form()
            else:
                self._show_error_popup("Error", "Failed to update employee information.")
        except Exception as e:
            self._show_error_popup("Error", f"An error occurred: {str(e)}")

    # ---------------- Clear form ----------------
    def _clear_form(self):
        """Clear all form fields"""
        self.current_emp_id = None
        self._emp_ID_entry.delete(0, "end")
        self._full_name_entry.delete(0, "end")
        self._date_of_birth_entry.delete(0, "end")
        self._gender_entry.set("")
        self._hiring_date_entry.delete(0, "end")
        self._contact_num_entry.delete(0, "end")
        self._emergency_contact_entry.delete(0, "end")
        self._email_entry.delete(0, "end")
        self._job_category_entry.delete(0, "end")
        self._department_entry.delete(0, "end")
        self._employee_status_entry.set("")
        
        # Clear address fields
        for field in [
            "_citizenship_entry", "_city_entry", "_subcity_entry",
            "_woreda_entry", "_kebele_entry", "_houseNO_entry"
        ]:
            widget = getattr(self, field, None)
            if widget:
                widget.delete(0, "end")

    # ---------------- Cleanup ----------------
    def cleanup(self):
        """Clean up resources when frame is destroyed"""
        if hasattr(self, 'edit_db'):
            self.edit_db.close()


# Testing
if __name__ == "__main__":
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("green")
    
    root = customtkinter.CTk()
    root.geometry("900x700")
    root.title("Edit Employee")
    
    # Make root expandable
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    edit_frame = Edit(root)
    
    def on_closing():
        edit_frame.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()