import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import messagebox, ttk
import sys
import os
from datetime import datetime

# Fix for the ModuleNotFoundError
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB_Service.Contracts_db import DBService

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ContractPage(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        
        # Make it a proper child window
        if master:
            self.transient(master)  # Make it stay on top of parent
            self.grab_set()  # Make it modal
        
        self.db = DBService()
        self.title("Employee Contract Management")
        
        # Center Window - Increased height to accommodate new sections
        width, height = 900, 700
        x = (self.winfo_screenwidth() / 2) - (width / 2)
        y = (self.winfo_screenheight() / 2) - (height / 2)
        self.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
        
        # Handle window close properly
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.setup_ui()

    def on_close(self):
        """Clean up before closing"""
        self.destroy()

    def setup_ui(self):
        # Create notebook for tabs
        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.notebook.add("New Contract")
        self.notebook.add("Active Contracts")
        self.notebook.add("Contract History")
        
        # Setup each tab
        self.setup_new_contract_tab()
        self.setup_active_contracts_tab()
        self.setup_contract_history_tab()
        
        # Create suggestion frame for autocomplete
        self.suggestion_frame = ctk.CTkScrollableFrame(self, width=300, height=0)

    def setup_new_contract_tab(self):
        tab = self.notebook.tab("New Contract")
        
        # Title
        self.title_lbl = ctk.CTkLabel(tab, text="New Contract Entry", font=("Arial", 24, "bold"))
        self.title_lbl.pack(pady=20)

        # Search Section
        self.search_frame = ctk.CTkFrame(tab, fg_color="transparent")
        self.search_frame.pack(pady=10, padx=40, fill="x")

        self.lbl_name = ctk.CTkLabel(self.search_frame, text="Search Employee Name:")
        self.lbl_name.pack(anchor="w")

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.on_search_change)
        
        self.entry_search = ctk.CTkEntry(self.search_frame, textvariable=self.search_var, placeholder_text="Type name...")
        self.entry_search.pack(fill="x", pady=5)

        # Autofill Fields (Locked)
        self.details_frame = ctk.CTkFrame(tab)
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
        self.date_frame = ctk.CTkFrame(tab, fg_color="transparent")
        self.date_frame.pack(pady=10, padx=40, fill="x")

        self.lbl_start = ctk.CTkLabel(self.date_frame, text="Start Date:")
        self.lbl_start.grid(row=0, column=0, padx=5)
        self.start_cal = DateEntry(self.date_frame, width=18, background='darkblue', font=("Arial", 12))
        self.start_cal.grid(row=0, column=1, padx=5)

        self.lbl_end = ctk.CTkLabel(self.date_frame, text="End Date:")
        self.lbl_end.grid(row=0, column=2, padx=5)
        self.end_cal = DateEntry(self.date_frame, width=18, background='darkblue', font=("Arial", 12))
        self.end_cal.grid(row=0, column=3, padx=5)

        # Status
        self.status_var = ctk.StringVar(value="Active")
        self.lbl_status = ctk.CTkLabel(tab, text="Contract Status:")
        self.lbl_status.pack(pady=(15, 0))
        
        self.radio_frame = ctk.CTkFrame(tab, fg_color="transparent")
        self.radio_frame.pack(pady=5)
        ctk.CTkRadioButton(self.radio_frame, text="Active", variable=self.status_var, value="Active").pack(side="left", padx=20)
        ctk.CTkRadioButton(self.radio_frame, text="Inactive", variable=self.status_var, value="Inactive").pack(side="left", padx=20)

        # Button
        self.btn_save = ctk.CTkButton(tab, text="Create Contract", command=self.save_contract, height=40)
        self.btn_save.pack(pady=30)

    def setup_active_contracts_tab(self):
        tab = self.notebook.tab("Active Contracts")
        
        # Title
        title_lbl = ctk.CTkLabel(tab, text="Active Contracts", font=("Arial", 24, "bold"))
        title_lbl.pack(pady=20)
        
        # Search and filter frame
        filter_frame = ctk.CTkFrame(tab, fg_color="transparent")
        filter_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(filter_frame, text="Search:").pack(side="left", padx=5)
        self.active_search_var = ctk.StringVar()
        self.active_search_var.trace_add("write", self.load_active_contracts)
        self.active_search_entry = ctk.CTkEntry(filter_frame, textvariable=self.active_search_var, width=200, placeholder_text="Search by employee name or ID...")
        self.active_search_entry.pack(side="left", padx=10)
        
        refresh_btn = ctk.CTkButton(filter_frame, text="Refresh", command=self.load_active_contracts, width=100)
        refresh_btn.pack(side="left", padx=10)
        
        # Treeview for active contracts
        self.active_tree_frame = ctk.CTkFrame(tab)
        self.active_tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create Treeview with customtkinter styling
        style = ttk.Style()
        style.theme_use("clam")
        
        # Create a frame for the tree and scrollbars
        tree_container = ctk.CTkFrame(self.active_tree_frame)
        tree_container.pack(fill="both", expand=True)
        
        # Create vertical scrollbar
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical")
        v_scrollbar.pack(side="right", fill="y")
        
        # Create horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Create Treeview
        self.active_tree = ttk.Treeview(
            tree_container,
            columns=("ContractID", "EmployeeID", "EmployeeName", "Department", "StartDate", "EndDate", "Status", "DaysRemaining"),
            show="headings",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        # Configure scrollbars
        v_scrollbar.config(command=self.active_tree.yview)
        h_scrollbar.config(command=self.active_tree.xview)
        
        # Define headings
        columns = [
            ("ContractID", "Contract ID", 80),
            ("EmployeeID", "Emp ID", 70),
            ("EmployeeName", "Employee Name", 150),
            ("Department", "Department", 120),
            ("StartDate", "Start Date", 100),
            ("EndDate", "End Date", 100),
            ("Status", "Status", 80),
            ("DaysRemaining", "Days Remaining", 100)
        ]
        
        for col_id, heading, width in columns:
            self.active_tree.heading(col_id, text=heading)
            self.active_tree.column(col_id, width=width, minwidth=50)
        
        self.active_tree.pack(fill="both", expand=True)
        
        # Action buttons frame
        action_frame = ctk.CTkFrame(tab, fg_color="transparent")
        action_frame.pack(pady=10)
        
        end_btn = ctk.CTkButton(action_frame, text="End Selected Contract", command=self.end_selected_contract, 
                               fg_color="#e53935", hover_color="#c62828")
        end_btn.pack(side="left", padx=10)
        
        # Load active contracts initially
        self.load_active_contracts()

    def setup_contract_history_tab(self):
        tab = self.notebook.tab("Contract History")
        
        # Title
        title_lbl = ctk.CTkLabel(tab, text="Contract History", font=("Arial", 24, "bold"))
        title_lbl.pack(pady=20)
        
        # Filter frame
        filter_frame = ctk.CTkFrame(tab, fg_color="transparent")
        filter_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(filter_frame, text="Search:").pack(side="left", padx=5)
        self.history_search_var = ctk.StringVar()
        self.history_search_var.trace_add("write", self.load_contract_history)
        self.history_search_entry = ctk.CTkEntry(filter_frame, textvariable=self.history_search_var, width=200, placeholder_text="Search by employee name or ID...")
        self.history_search_entry.pack(side="left", padx=10)
        
        refresh_btn = ctk.CTkButton(filter_frame, text="Refresh", command=self.load_contract_history, width=100)
        refresh_btn.pack(side="left", padx=10)
        
        # Treeview for contract history
        self.history_tree_frame = ctk.CTkFrame(tab)
        self.history_tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create a frame for the tree and scrollbars
        tree_container = ctk.CTkFrame(self.history_tree_frame)
        tree_container.pack(fill="both", expand=True)
        
        # Create vertical scrollbar
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical")
        v_scrollbar.pack(side="right", fill="y")
        
        # Create horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Create Treeview
        self.history_tree = ttk.Treeview(
            tree_container,
            columns=("ContractID", "EmployeeID", "EmployeeName", "StartDate", "EndDate", "Status", "Duration", "EndedOn"),
            show="headings",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        # Configure scrollbars
        v_scrollbar.config(command=self.history_tree.yview)
        h_scrollbar.config(command=self.history_tree.xview)
        
        # Define headings
        columns = [
            ("ContractID", "Contract ID", 80),
            ("EmployeeID", "Emp ID", 70),
            ("EmployeeName", "Employee Name", 150),
            ("StartDate", "Start Date", 100),
            ("EndDate", "End Date", 100),
            ("Status", "Status", 80),
            ("Duration", "Duration", 80),
            ("EndedOn", "Ended On", 100)
        ]
        
        for col_id, heading, width in columns:
            self.history_tree.heading(col_id, text=heading)
            self.history_tree.column(col_id, width=width, minwidth=50)
        
        self.history_tree.pack(fill="both", expand=True)
        
        # Load contract history initially
        self.load_contract_history()

    def on_search_change(self, *args):
        query = self.search_var.get()
        
        # Clear previous suggestions
        for widget in self.suggestion_frame.winfo_children():
            widget.destroy()

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
            self.entry_id.configure(state="normal")
            self.entry_dept.configure(state="normal")
            self.id_var.set(data[0])
            self.dept_var.set(data[1])
            self.entry_id.configure(state="disabled")
            self.entry_dept.configure(state="disabled")

    def save_contract(self):
        emp_id = self.id_var.get()
        if not emp_id:
            messagebox.showwarning("Incomplete", "Please select an employee.")
            return
        try:
            self.db.create_contract(emp_id, self.start_cal.get_date(), self.end_cal.get_date(), self.status_var.get())
            messagebox.showinfo("Success", "Contract saved successfully!")
            # Clear form after successful save
            self.search_var.set("")
            self.id_var.set("")
            self.dept_var.set("")
            # Refresh active contracts
            self.load_active_contracts()
        except Exception as e: 
            messagebox.showerror("Error", str(e))

    def load_active_contracts(self, *args):
        # Clear existing items
        for item in self.active_tree.get_children():
            self.active_tree.delete(item)
        
        # Get search term
        search_term = self.active_search_var.get()
        
        try:
            contracts = self.db.get_active_contracts(search_term)
            today = datetime.now().date()
            
            for contract in contracts:
                contract_id, emp_id, emp_name, dept, start_date, end_date, status = contract
                
                # Calculate days remaining
                try:
                    end_date_obj = end_date if isinstance(end_date, datetime) else datetime.strptime(str(end_date), "%Y-%m-%d")
                    days_remaining = (end_date_obj.date() - today).days
                    days_text = f"{days_remaining} days" if days_remaining > 0 else "Expired" if days_remaining < 0 else "Today"
                except:
                    days_text = "N/A"
                
                # Color code based on days remaining
                tags = ()
                if days_remaining < 7 and days_remaining >= 0:
                    tags = ("warning",)
                elif days_remaining < 0:
                    tags = ("expired",)
                
                self.active_tree.insert("", "end", values=(
                    contract_id, emp_id, emp_name, dept, 
                    start_date.strftime("%Y-%m-%d") if hasattr(start_date, 'strftime') else start_date,
                    end_date.strftime("%Y-%m-%d") if hasattr(end_date, 'strftime') else end_date,
                    status, days_text
                ), tags=tags)
            
            # Configure tag colors
            self.active_tree.tag_configure("warning", background="#fff3cd")
            self.active_tree.tag_configure("expired", background="#f8d7da")
            
        except Exception as e:
            print(f"Error loading active contracts: {e}")
            messagebox.showerror("Error", f"Failed to load active contracts: {str(e)}")

    def load_contract_history(self, *args):
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Get search term
        search_term = self.history_search_var.get()
        
        try:
            history = self.db.get_contract_history(search_term)
            
            for contract in history:
                contract_id, emp_id, emp_name, start_date, end_date, status = contract
                
                # Calculate duration
                try:
                    start_date_obj = start_date if isinstance(start_date, datetime) else datetime.strptime(str(start_date), "%Y-%m-%d")
                    end_date_obj = end_date if isinstance(end_date, datetime) else datetime.strptime(str(end_date), "%Y-%m-%d")
                    duration_days = (end_date_obj - start_date_obj).days
                    duration_text = f"{duration_days} days"
                except:
                    duration_text = "N/A"
                
                # Format dates
                start_fmt = start_date.strftime("%Y-%m-%d") if hasattr(start_date, 'strftime') else start_date
                end_fmt = end_date.strftime("%Y-%m-%d") if hasattr(end_date, 'strftime') else end_date
                
                self.history_tree.insert("", "end", values=(
                    contract_id, emp_id, emp_name, start_fmt, end_fmt, status, duration_text, end_fmt
                ))
            
        except Exception as e:
            print(f"Error loading contract history: {e}")
            messagebox.showerror("Error", f"Failed to load contract history: {str(e)}")

    def end_selected_contract(self):
        selection = self.active_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a contract to end.")
            return
        
        item = self.active_tree.item(selection[0])
        contract_id = item['values'][0]
        emp_name = item['values'][2]
        
        if messagebox.askyesno("Confirm", f"End contract for {emp_name}?"):
            try:
                if self.db.end_contract(contract_id):
                    messagebox.showinfo("Success", "Contract ended successfully.")
                    self.load_active_contracts()
                    self.load_contract_history()
                else:
                    messagebox.showerror("Error", "Failed to end contract.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to end contract: {str(e)}")

if __name__ == "__main__":
    app = ContractPage()
    app.mainloop()