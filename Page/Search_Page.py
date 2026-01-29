import customtkinter as ctk
from PIL import Image
import os
from DB_Service.Search_db import SearchDB

class SearchPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.db = SearchDB()
        
        # --- UI Header ---
        header = ctk.CTkLabel(self, text="Employee Directory", font=("Arial", 24, "bold"))
        header.pack(pady=(20, 10))

        # --- Search Bar ---
        search_container = ctk.CTkFrame(self, fg_color="transparent")
        search_container.pack(fill="x", padx=50, pady=10)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.load_results())
        
        self.search_entry = ctk.CTkEntry(search_container, placeholder_text="Type name or ID to search...", 
                                        textvariable=self.search_var, height=40)
        self.search_entry.pack(fill="x", side="left", expand=True)
        
        # --- Results Area ---
        self.results_frame = ctk.CTkScrollableFrame(self, fg_color="#2B2B2B")
        self.results_frame.pack(pady=20, padx=50, fill="both", expand=True)
        
        self.load_results()

    def load_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        employees = self.db.search_all_employees(self.search_var.get())
        
        for emp in employees:
            # Create a card-like row for each employee
            card = ctk.CTkFrame(self.results_frame, height=50, fg_color="#333333")
            card.pack(fill="x", pady=5, padx=5)
            
            info_label = ctk.CTkLabel(card, text=f" {emp['EmpID']} | {emp['name']}", font=("Arial", 13))
            info_label.pack(side="left", padx=15)
            
            dept_label = ctk.CTkLabel(card, text=emp['DepName'], text_color="gray")
            dept_label.pack(side="left", padx=20)

            view_btn = ctk.CTkButton(card, text="View Profile", width=100, height=28,
                                    command=lambda e=emp: self.show_profile(e['EmpID']))
            view_btn.pack(side="right", padx=10)

    def show_profile(self, emp_id):
        data = self.db.get_full_profile(emp_id)
        
        # Popup Window for Profile
        profile_win = ctk.CTkToplevel(self)
        profile_win.title(f"Profile: {data['name']}")
        profile_win.geometry("450x650")
        profile_win.attributes('-topmost', True) # Keep on top

        # Profile Image Section
        img_path = data.get('profile_image')
        if img_path and os.path.exists(img_path):
            pil_img = Image.open(img_path)
            ctk_img = ctk.CTkImage(light_image=pil_img, size=(160, 180))
            img_display = ctk.CTkLabel(profile_win, image=ctk_img, text="")
            img_display.pack(pady=20)
        else:
            placeholder = ctk.CTkFrame(profile_win, width=160, height=180, fg_color="gray20")
            placeholder.pack(pady=20)
            ctk.CTkLabel(placeholder, text="No Image").place(relx=0.5, rely=0.5, anchor="center")

        # Detailed Information
        details_frame = ctk.CTkFrame(profile_win, fg_color="transparent")
        details_frame.pack(fill="both", expand=True, padx=30)

        # Labels for details
        fields = [
            ("Full Name", data['name']),
            ("Employee ID", data['EmpID']),
            ("Department", data['DepName']),
            ("Position", data['employment_status']),
            ("Hire Date", data['hire_date']),
            ("Gender", data['gender']),
            ("Email", data.get('email', 'Not provided'))
        ]

        for label, value in fields:
            f = ctk.CTkFrame(details_frame, fg_color="transparent")
            f.pack(fill="x", pady=5)
            ctk.CTkLabel(f, text=f"{label}:", font=("Arial", 12, "bold"), text_color="gray").pack(side="left")
            ctk.CTkLabel(f, text=f" {value}", font=("Arial", 13)).pack(side="left")

        close_btn = ctk.CTkButton(profile_win, text="Close", command=profile_win.destroy)
        close_btn.pack(pady=20)