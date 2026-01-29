import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry
from PIL import Image
import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import EmployeeFile
from DB_Service.Dep_job_db import DepJobDB

ctk.set_appearance_mode("Light")

class AddEmployeeApp(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Add New Employee")
        self.geometry("1100x850")
        self.attributes('-topmost', True)
        
        self.db_service = DepJobDB()
        
        # Load DB Data for dropdowns
        self.dept_data = self.db_service.get_all_departments()
        self.job_data = self.db_service.get_all_job_titles()

        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self.main_frame, text="New Employee Registration", font=("Arial", 26, "bold")).pack(pady=20)
        top_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_container.pack(fill="both", expand=True, padx=10)

        # --- LEFT COLUMN ---
        left_col = ctk.CTkFrame(top_container)
        left_col.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.add_field(left_col, "Full Name", "full_name_entry")
        self.add_field(left_col, "Email Address", "email_entry")
        self.add_field(left_col, "Personal Contact", "contact_entry")

        ctk.CTkLabel(left_col, text="Department", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(10,0))
        dept_names = [d[1] for d in self.dept_data] if self.dept_data else ["None"]
        self.dept_option = ctk.CTkOptionMenu(left_col, values=dept_names)
        self.dept_option.pack(fill="x", padx=20, pady=5)

        # --- RIGHT COLUMN ---
        right_col = ctk.CTkFrame(top_container)
        right_col.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # NEW: Job Title Dropdown
        ctk.CTkLabel(right_col, text="Job Title", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(10,0))
        job_names = [j[1] for j in self.job_data] if self.job_data else ["None"]
        self.job_option = ctk.CTkOptionMenu(right_col, values=job_names)
        self.job_option.pack(fill="x", padx=20, pady=5)

        self.add_dropdown(right_col, "Gender", ["Male", "Female"], "gender_option")
        self.add_dropdown(right_col, "Employment Status", ["Full-Time", "Part-Time"], "status_option")
        self.add_field(right_col, "Emergency Contact", "emergency_entry")

        # Dates
        df = ctk.CTkFrame(right_col, fg_color="transparent")
        df.pack(fill="x", padx=20, pady=10)
        self.dob_entry = self.add_date(df, "DOB", 0)
        self.hire_entry = self.add_date(df, "Hiring Date", 1)

        # --- BOTTOM (DOCS) ---
        self.setup_docs()

        ctk.CTkButton(self.main_frame, text="SAVE EMPLOYEE", font=("Arial", 18, "bold"), 
                      height=50, fg_color="#2ECC71", command=self.submit_action).pack(pady=40)

    # UI Helpers
    def add_field(self, p, txt, attr):
        ctk.CTkLabel(p, text=txt, font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(10,0))
        ent = ctk.CTkEntry(p)
        ent.pack(fill="x", padx=20, pady=5)
        setattr(self, attr, ent)

    def add_dropdown(self, p, txt, vals, attr):
        ctk.CTkLabel(p, text=txt, font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(10,0))
        opt = ctk.CTkOptionMenu(p, values=vals)
        opt.pack(fill="x", padx=20, pady=5)
        setattr(self, attr, opt)

    def add_date(self, p, txt, col):
        ctk.CTkLabel(p, text=txt).grid(row=0, column=col, sticky="w")
        de = DateEntry(p, width=12, date_pattern="yyyy-mm-dd")
        de.grid(row=1, column=col, padx=5)
        return de

    def setup_docs(self):
        f = ctk.CTkFrame(self.main_frame)
        f.pack(fill="x", padx=20, pady=10)
        self.cert_lbl = self.add_doc_row(f, "Certificate")
        self.cv_lbl = self.add_doc_row(f, "CV")
        self.img_lbl = ctk.CTkLabel(f, text="No Image", width=100, height=100, fg_color="gray")
        self.img_lbl.pack(side="right", padx=20)
        ctk.CTkButton(f, text="Photo", command=self.upload_img).pack(side="right")

    def add_doc_row(self, p, txt):
        lbl = ctk.CTkLabel(p, text="No file")
        ctk.CTkButton(p, text=f"Upload {txt}", command=lambda: self.up_file(lbl)).pack(anchor="w")
        lbl.pack(anchor="w", padx=10)
        return lbl

    def up_file(self, lbl):
        path = filedialog.askopenfilename()
        if path:
            lbl.configure(text=os.path.basename(path))
            lbl.full_path = path

    def upload_img(self):
        path = filedialog.askopenfilename()
        if path:
            img = Image.open(path)
            ctk_img = ctk.CTkImage(img, size=(100, 100))
            self.img_lbl.configure(image=ctk_img, text="")
            self.img_lbl.full_path = path

    def submit_action(self):
        try:
            # Map Names to IDs
            d_id = next(i[0] for i in self.dept_data if i[1] == self.dept_option.get())
            j_id = next(i[0] for i in self.job_data if i[1] == self.job_option.get())

            success = self.db_service.insert_employee(
                dep_id=d_id, job_id=j_id,
                name=self.full_name_entry.get(),
                email=self.email_entry.get(),
                contact=self.contact_entry.get(),
                emergency=self.emergency_entry.get(),
                dob=self.dob_entry.get_date().strftime('%Y-%m-%d'),
                gender=self.gender_option.get(),
                hire_date=self.hire_entry.get_date().strftime('%Y-%m-%d'),
                status=self.status_option.get()
            )

            if success:
                emp_id = self.db_service.get_latest_emp_id()
                files = {"image": getattr(self.img_lbl, 'full_path', None)} # Add others similarly
                EmployeeFile.SaveEmpFile(emp_id, files)
                messagebox.showinfo("Success", f"Saved! ID: {emp_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))



if __name__ == "__main__":
    app = AddEmployeeApp()
    app.mainloop()