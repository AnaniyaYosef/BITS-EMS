import customtkinter as ctk
from PIL import Image
import os
from DB_Service.Search_db import SearchDB

class SearchPage(ctk.CTkToplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.db = SearchDB()
        
        # --- Window Configuration ---
        self.title("Employee Directory")
        self.geometry("1000x750")
        self.after(200, self.lift) 
        self.attributes('-topmost', True)
        self.configure(fg_color="#FFFFFF")
        
        # --- UI Header ---
        self.header = ctk.CTkLabel(self, text="Employee Directory", font=("Arial", 28, "bold"), text_color="#1D3557")
        self.header.pack(pady=(30, 10))

        # --- Search Bar ---
        self.search_container = ctk.CTkFrame(self, fg_color="transparent")
        self.search_container.pack(fill="x", padx=50, pady=10)

        self.search_var = ctk.StringVar()
        # Trace 'write' to update results as you type
        self.search_var.trace_add("write", lambda *args: self.load_results())
        
        self.search_entry = ctk.CTkEntry(
            self.search_container, 
            placeholder_text="Search by Name or Employee ID (e.g. 101)...", 
            textvariable=self.search_var, 
            height=45,
            font=("Arial", 14)
        )
        self.search_entry.pack(fill="x", side="left", expand=True)
        
        # --- Results Area ---
        self.results_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color="#F8FAFC", 
            border_width=1, 
            border_color="#E2E8F0"
        )
        self.results_frame.pack(pady=20, padx=50, fill="both", expand=True)
        
        # Initial call to show all employees on startup
        self.load_results()
        self.search_entry.focus()

    def load_results(self):
        # Clear frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        search_query = self.search_var.get()
        employees = self.db.search_all_employees(search_query)
        
        if not employees:
            no_data = ctk.CTkLabel(self.results_frame, text="No matching employees found.", font=("Arial", 13), text_color="gray")
            no_data.pack(pady=40)
            return

        for emp in employees:
            # Main Card
            card = ctk.CTkFrame(self.results_frame, height=75, fg_color="#FFFFFF", border_width=1, border_color="#E2E8F0")
            card.pack(fill="x", pady=6, padx=10)
            card.pack_propagate(False) 
            
            # Left Side: ID and Name
            # Formatting ID to look like EMP001
            display_id = f"EMP{int(emp['employee_id']):03d}" if emp.get('employee_id') else "EMP???"
            
            info_label = ctk.CTkLabel(card, text=f"{display_id}  |  {emp['full_name']}", 
                                     font=("Arial", 15, "bold"), text_color="#1D3557")
            info_label.pack(side="left", padx=20)
            
            # Middle: Department
            dept_text = f"📍 {emp['department_name']}" if emp.get('department_name') else "No Department"
            dept_label = ctk.CTkLabel(card, text=dept_text, font=("Arial", 13), text_color="#64748B")
            dept_label.pack(side="left", padx=40)

            # Right Side: View Button
            view_btn = ctk.CTkButton(
                card, text="View Profile", 
                width=120, 
                height=35,
                fg_color="#8CC63F", 
                hover_color="#7BB035",
                font=("Arial", 12, "bold"),
                command=lambda e=emp: self.show_profile(e['employee_id'])
            )
            view_btn.pack(side="right", padx=20)

    def show_profile(self, emp_id):
        data = self.db.get_full_profile(emp_id)
        if not data: 
            return

        profile_win = ctk.CTkToplevel(self)
        profile_win.title(f"Profile: {data['full_name']}")
        profile_win.geometry("480x680")
        profile_win.attributes('-topmost', True) 
        profile_win.configure(fg_color="#FFFFFF")

        # --- Profile Image ---
        img_path = self.db.get_employee_image(emp_id)

        img_container = ctk.CTkFrame(profile_win, width=140, height=140, fg_color="transparent")
        img_container.pack(pady=25)

        if img_path and os.path.exists(img_path):
            img = Image.open(img_path).resize((120, 120))
            profile_img = ctk.CTkImage(img, size=(120, 120))

            img_label = ctk.CTkLabel(img_container, image=profile_img, text="")
            img_label.image = profile_img  # 🚨 keep a reference
            img_label.pack()
        else:
            # Fallback avatar
            placeholder = ctk.CTkFrame(
                img_container,
                width=120,
                height=120,
                fg_color="#F1F5F9",
                corner_radius=60
            )
            placeholder.pack()
            ctk.CTkLabel(
                placeholder,
                text="👤",
                font=("Arial", 50)
            ).place(relx=0.5, rely=0.5, anchor="center")

        # --- DETAILS FRAME: always create, outside image logic ---
        details_frame = ctk.CTkFrame(profile_win, fg_color="transparent")
        details_frame.pack(fill="both", expand=True, padx=45)

        # Mapping your Database columns to the UI rows
        fields = [
            ("Full Name", data['full_name']),
            ("Employee ID", f"EMP{int(data['employee_id']):03d}"),
            ("Department", data['department_name']),
            ("Gender", data['gender']),
            ("Email", data['email']),
            ("Contact", data['contact_number'] if data['contact_number'] else "N/A"),
            ("Joined Date", data['employment_date'])
        ]

        for label, value in fields:
            row = ctk.CTkFrame(details_frame, fg_color="transparent")
            row.pack(fill="x", pady=8)
            ctk.CTkLabel(row, text=f"{label}:", font=("Arial", 12, "bold"), text_color="#64748B", width=120, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=f"{value}", font=("Arial", 13), text_color="#1D3557", wraplength=220, justify="left").pack(side="left")

        ctk.CTkButton(profile_win, text="Close Window", fg_color="#1D3557", height=40, command=profile_win.destroy).pack(pady=30)
        