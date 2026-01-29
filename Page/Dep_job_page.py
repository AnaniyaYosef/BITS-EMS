import customtkinter as ctk
import sys
import os
from tkinter import messagebox, Listbox

# Adds the BITS-EMS folder to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the service we fixed earlier
from DB_Service.Dep_job_db import DBService 

class DepartmentPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="white", corner_radius=0)
        
        # Initialize the database service
        self.db_service = DBService() 
        self.selected_manager_id = None 

        # --- UI LAYOUT ---
        ctk.CTkLabel(self, text="Department Management", 
                     text_color="#1A3752", font=("Arial", 28, "bold")).pack(pady=(40, 20))

        self.add_btn = ctk.CTkButton(self, text="+ Add Department", 
                                     fg_color="#82C941", hover_color="#6BA336",
                                     text_color="white", font=("Arial", 14, "bold"), 
                                     height=45, width=250,
                                     command=self.open_add_modal)
        self.add_btn.pack(pady=20)

    def open_add_modal(self):
        self.modal = ctk.CTkToplevel(self)
        self.modal.title("Add New Department")
        self.modal.geometry("450x450")
        self.modal.configure(fg_color="white")
        
        self.modal.transient(self.master) 
        self.modal.grab_set()

        ctk.CTkLabel(self.modal, text="Create Department", 
                     font=("Arial", 20, "bold"), text_color="#1A3752").pack(pady=20)

        # 1. Department Name
        self.create_modal_label("Department Name")
        self.dept_name_entry = ctk.CTkEntry(self.modal, width=320)
        self.dept_name_entry.pack(pady=(0, 15))

        # 2. Manager Name (Smart Search)
        self.create_modal_label("Manager Name")
        
        self.manager_search = ctk.CTkEntry(self.modal, width=320, placeholder_text="🔍 Type to search manager...")
        self.manager_search.pack(pady=(0, 5))
        self.manager_search.bind("<KeyRelease>", self.update_manager_list)

        # Suggestions Listbox (Float over UI)
        self.mgr_list = Listbox(self.modal, height=4, width=45, font=("Arial", 10),
                                relief="flat", borderwidth=1, highlightthickness=1)

        # Feedback label for ID confirmation
        self.mgr_id_label = ctk.CTkLabel(self.modal, text="No manager selected", text_color="gray", font=("Arial", 10))
        self.mgr_id_label.pack(pady=(0, 10))

        # 3. Status
        self.create_modal_label("Status")
        status_frame = ctk.CTkFrame(self.modal, fg_color="transparent")
        status_frame.pack(pady=5)
        self.status_var = ctk.StringVar(value="Active")
        ctk.CTkRadioButton(status_frame, text="Active", variable=self.status_var, value="Active", text_color="black").pack(side="left", padx=15)
        ctk.CTkRadioButton(status_frame, text="Inactive", variable=self.status_var, value="Inactive", text_color="black").pack(side="left", padx=15)

        # Buttons
        btn_frame = ctk.CTkFrame(self.modal, fg_color="transparent")
        btn_frame.pack(pady=30)
        ctk.CTkButton(btn_frame, text="Cancel", fg_color="#E0E0E0", text_color="black", width=100, command=self.modal.destroy).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Save", fg_color="#1E88E5", width=150, command=self.save_department).pack(side="left", padx=10)

    def update_manager_list(self, event):
        val = self.manager_search.get()
        if not val:
            self.mgr_list.place_forget()
            return
        
        try:
            results = self.db_service.search_managers(val)
            if results:
                self.mgr_list.delete(0, 'end')
                for r in results:
                    # Assuming search_managers returns (id, full_name)
                    self.mgr_list.insert('end', r[1]) 
                
                self.mgr_list.place(x=65, y=230) # Adjusted Y for removed faculty field
                self.mgr_list.lift() 
                self.mgr_list.bind("<<ListboxSelect>>", self.on_manager_select)
            else:
                self.mgr_list.place_forget()
        except Exception as e:
            print(f"Search Error: {e}")

    def on_manager_select(self, event):
        if not self.mgr_list.curselection(): return
        selection = self.mgr_list.get(self.mgr_list.curselection())
        
        mgr_id = self.db_service.get_manager_id(selection)
        if mgr_id:
            self.selected_manager_id = mgr_id
            self.manager_search.delete(0, 'end')
            self.manager_search.insert(0, selection) 
            self.mgr_id_label.configure(text=f"Linked ID: {mgr_id}", text_color="green")
        
        self.mgr_list.place_forget()

    def create_modal_label(self, txt):
        lbl = ctk.CTkLabel(self.modal, text=txt, text_color="black", font=("Arial", 12, "bold"))
        lbl.pack(anchor="w", padx=65, pady=(5, 2))

    def save_department(self):
        name = self.dept_name_entry.get()
        # Convert "Active" string to Boolean for the DB
        is_active = True if self.status_var.get() == "Active" else False

        if not name:
            messagebox.showwarning("Incomplete Form", "Please enter a department name.", parent=self.modal)
            return

        try:
            # Use the method we created in the service class
            success = self.db_service.insert_department(
                name=name, 
                manager_id=self.selected_manager_id, 
                active=is_active
            )
            
            if success:
                messagebox.showinfo("Success", f"Department '{name}' added successfully!", parent=self.modal)
                self.modal.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {e}", parent=self.modal)

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("600x450")
    page = DepartmentPage(root)
    page.pack(expand=True, fill="both")
    root.mainloop()