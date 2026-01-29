import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import messagebox
import sys
import os

# Fix for the ModuleNotFoundError
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB_Service.Contracts_db import DBService

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ContractPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = DBService()
        self.title("Employee Contract Management")
        
        # Center Window
        width, height = 600, 560
        x = (self.winfo_screenwidth() / 2) - (width / 2)
        y = (self.winfo_screenheight() / 2) - (height / 2)
        self.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

        self.setup_ui()

    def setup_ui(self):
        # Title
        self.title_lbl = ctk.CTkLabel(self, text="New Contract Entry", font=("Arial", 24, "bold"))
        self.title_lbl.pack(pady=20)

        # Search Section
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(pady=10, padx=40, fill="x")

        self.lbl_name = ctk.CTkLabel(self.search_frame, text="Search Employee Name:")
        self.lbl_name.pack(anchor="w")

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.on_search_change)
        
        self.entry_search = ctk.CTkEntry(self.search_frame, textvariable=self.search_var, placeholder_text="Type name...")
        self.entry_search.pack(fill="x", pady=5)

        # Autofill Fields (Locked)
        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.pack(pady=20, padx=40, fill="x")

        self.lbl_id = ctk.CTkLabel(self.details_frame, text="Employee ID (Locked):")
        self.lbl_id.grid(row=0, column=0, padx=20, pady=10, sticky="e")
        self.id_var = ctk.StringVar()
        self.entry_id = ctk.CTkEntry(self.details_frame, textvariable=self.id_var, state="disabled", width=200)
        self.entry_id.grid(row=0, column=1, padx=20, pady=10)

        self.lbl_dept = ctk.CTkLabel(self.details_frame, text="Department (Locked):")
        self.lbl_dept.grid(row=1, column=0, padx=20, pady=10, sticky="e")
        self.dept_var = ctk.StringVar()
        self.entry_dept = ctk.CTkEntry(self.details_frame, textvariable=self.dept_var, state="disabled", width=200)
        self.entry_dept.grid(row=1, column=1, padx=20, pady=10)

        # Date Pickers (Bigger Font/Width)
        self.date_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.date_frame.pack(pady=10, padx=40, fill="x")

        self.lbl_start = ctk.CTkLabel(self.date_frame, text="Start Date:")
        self.lbl_start.grid(row=0, column=0, padx=5)
        # font=("Arial", 12) makes the internal text and box bigger
        self.start_cal = DateEntry(self.date_frame, width=18, background='darkblue', font=("Arial", 12))
        self.start_cal.grid(row=0, column=1, padx=5)

        self.lbl_end = ctk.CTkLabel(self.date_frame, text="End Date:")
        self.lbl_end.grid(row=0, column=2, padx=5)
        self.end_cal = DateEntry(self.date_frame, width=18, background='darkblue', font=("Arial", 12))
        self.end_cal.grid(row=0, column=3, padx=5)

        # Status
        self.status_var = ctk.StringVar(value="Active")
        self.lbl_status = ctk.CTkLabel(self, text="Contract Status:")
        self.lbl_status.pack(pady=(15, 0))
        
        self.radio_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.radio_frame.pack(pady=5)
        ctk.CTkRadioButton(self.radio_frame, text="Active", variable=self.status_var, value="Active").pack(side="left", padx=20)
        ctk.CTkRadioButton(self.radio_frame, text="Inactive", variable=self.status_var, value="Inactive").pack(side="left", padx=20)

        # Button
        self.btn_save = ctk.CTkButton(self, text="Create Contract", command=self.save_contract, height=40)
        self.btn_save.pack(pady=30)

        # Create suggestion frame last to ensure it sits on top (Z-index)
        self.suggestion_frame = ctk.CTkScrollableFrame(self, width=300, height=0)

    def on_search_change(self, *args):
        query = self.search_var.get()
        
        # Clear previous suggestions
        for widget in self.suggestion_frame.winfo_children():
            widget.destroy()

        # Change trigger to 1 character instead of 2
        if len(query) >= 1:
            try:
                results = self.db.search_employees(query)
                if results:
                    
                    self.suggestion_frame.place(x=40, y=150, relwidth=0.8)
                    self.suggestion_frame.lift()
                    self.suggestion_frame.configure(height=180, fg_color="#4A4949")
                    
                    for row in results:
                        name = row[0]
                        btn = ctk.CTkButton(
                            self.suggestion_frame, 
                            text=f"  🔍  {name}", 
                            anchor="w", 
                            height=35,
                            fg_color="transparent", 
                            hover_color="#767575",
                            text_color="#e8eaed",
                            font=("Arial", 14),
                            corner_radius=0,
                            command=lambda n=name: self.autofill_employee(n)
                        )
                        btn.pack(fill="x", pady=1)
                else:
                    self.suggestion_frame.place_forget()
            except Exception as e:
                print(f"Search Error: {e}")
        else:
            self.suggestion_frame.place_forget()

    def autofill_employee(self, name):
        self.search_var.set(name)
        self.suggestion_frame.place_forget()
        data = self.db.get_employee_details(name)
        if data:
            self.entry_id.configure(state="normal"); self.entry_dept.configure(state="normal")
            self.id_var.set(data[0]); self.dept_var.set(data[1])
            self.entry_id.configure(state="disabled"); self.entry_dept.configure(state="disabled")

    def save_contract(self):
        emp_id = self.id_var.get()
        if not emp_id:
            messagebox.showwarning("Incomplete", "Please select an employee.")
            return
        try:
            self.db.create_contract(emp_id, self.start_cal.get_date(), self.end_cal.get_date(), self.status_var.get())
            messagebox.showinfo("Success", "Contract saved!")
        except Exception as e: messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = ContractPage()
    app.mainloop()
