import customtkinter as ctk
from customtkinter import CTkComboBox, CTkEntry, CTkButton, CTkLabel, CTkFrame
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import re

class HREmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HR Employee Management System")
        self.root.geometry("1400x800")
        self.root.resizable(True, True)
        
        # Configure CustomTkinter appearance
        ctk.set_appearance_mode("light")  # or "dark"
        ctk.set_default_color_theme("green")  # Use green theme to match sidebar
        
        # Database connection
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Amoori.1927',
            'database': 'bitsems',
            'port': 3306
        }
        
        self.conn = None
        self.cursor = None
        self.employees = []
        
        self.connect_database()
        self.create_table()
        self.setup_ui()
        self.load_employees()
    
    def connect_database(self):
        try:
            # First connect without database to create it if needed
            temp_config = self.db_config.copy()
            temp_config.pop('database', None)
            
            temp_conn = mysql.connector.connect(**temp_config)
            temp_cursor = temp_conn.cursor()
            
            # Create database if it doesn't exist
            temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_config['database']}")
            temp_cursor.close()
            temp_conn.close()
            
            # Now connect to the specific database
            self.conn = mysql.connector.connect(**self.db_config)
            self.cursor = self.conn.cursor(dictionary=True)
            print("Database connected successfully")
        except Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            self.root.destroy()
    
    def create_table(self):
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS employees (
                employee_id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                department_name VARCHAR(100) NOT NULL,
                gender ENUM('Male', 'Female', 'Other') NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                contact_number VARCHAR(20),
                employment_date DATE NOT NULL
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Table created or already exists")
        except Error as e:
            messagebox.showerror("Table Error", f"Error creating table: {e}")
    
    def setup_ui(self):
        # Main container with sidebar and content
        main_container = ctk.CTkFrame(self.root, fg_color="#f9fafb")
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Sidebar
        self.setup_sidebar(main_container)
        
        # Content area
        content_frame = ctk.CTkFrame(main_container, fg_color="#f9fafb")
        content_frame.pack(side="right", fill="both", expand=True)
        
        # Header
        self.setup_header(content_frame)
        
        # Search bar
        self.setup_search_bar(content_frame)
        
        # Filters
        self.setup_filters(content_frame)
        
        # Table
        self.setup_table(content_frame)
    
    def setup_sidebar(self, parent):
        sidebar = ctk.CTkFrame(parent, fg_color="#7BC043", width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Title with icon
        title_frame = ctk.CTkFrame(sidebar, fg_color="#7BC043")
        title_frame.pack(fill="x", pady=20)
        
        title = ctk.CTkLabel(title_frame, text="HR", font=("Segoe UI", 40, "bold"),
                           text_color="white")
        title.pack()
        
        subtitle = ctk.CTkLabel(title_frame, text="Management", font=("Segoe UI", 16),
                              text_color="#e8f5e9")
        subtitle.pack()
        
        # Menu items
        menu_items = [
            ("+ Add Employee", self.add_employee),
            ("✎ Edit Employee", self.edit_employee),
            ("🗑 Delete Employee", self.delete_employee),
            ("🔍 Search Employee", self.search_employee),
            ("👁 View Employee", self.view_employee),
            ("📋 Leave Request Form", self.leave_request)
        ]
        
        for item_text, command in menu_items:
            btn = ctk.CTkButton(sidebar, text=item_text, fg_color="#7BC043", text_color="white",
                              font=("Segoe UI", 16), cursor="hand2",
                              command=command, anchor="w",
                              width=180, height=40)
            btn.pack(fill="x", padx=10, pady=2)
    
    def setup_header(self, parent):
        header = ctk.CTkFrame(parent, fg_color="#ffffff")
        header.pack(fill="x", padx=20, pady=15)
        
        # Header with shadow effect
        header_container = ctk.CTkFrame(header, fg_color="#ffffff")
        header_container.pack(fill="x", padx=0, pady=0)
        
        title_frame = ctk.CTkFrame(header_container, fg_color="#ffffff")
        title_frame.pack(fill="x", padx=20, pady=15)
        
        title = ctk.CTkLabel(title_frame, text="Employee Management", font=("Segoe UI", 36, "bold"),
                           text_color="#2c3e50")
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(title_frame, text="Manage your team efficiently", font=("Segoe UI", 14),
                              text_color="#7f8c8d")
        subtitle.pack(anchor="w", pady=2)
    
    def setup_search_bar(self, parent):
        search_frame = ctk.CTkFrame(parent, fg_color="#ffffff")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(search_frame, text="Search:", font=("Segoe UI", 14),
                   text_color="#2c3e50").pack(side="left", padx=5)
        
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var,
                                  font=("Segoe UI", 14), width=400)
        search_entry.pack(side="left", padx=5)
        search_entry.insert(0, "John Doe")
        
        search_btn = ctk.CTkButton(search_frame, text="🔍", font=("Segoe UI", 16),
                                 command=self.perform_search,
                                 fg_color="#3498db", text_color="white", cursor="hand2", width=40)
        search_btn.pack(side="left", padx=5)
        
        search_entry.bind("<Return>", lambda e: self.perform_search())
    
    def setup_filters(self, parent):
        filter_frame = ctk.CTkFrame(parent, fg_color="#ffffff")
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(filter_frame, text="Filters:", font=("Segoe UI", 16, "bold"),
                   text_color="#2c3e50").pack(side="left", padx=5)
        
        # Name filter
        ctk.CTkLabel(filter_frame, text="Name ▼", font=("Segoe UI", 14),
                   text_color="#2c3e50").pack(side="left", padx=5)
        self.name_filter = CTkComboBox(filter_frame, width=150, state="readonly")
        self.name_filter.pack(side="left", padx=5)
        self.name_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # Employee ID filter
        ctk.CTkLabel(filter_frame, text="Employee ID ▼", font=("Segoe UI", 14),
                   text_color="#2c3e50").pack(side="left", padx=5)
        self.id_filter = CTkComboBox(filter_frame, width=150, state="readonly")
        self.id_filter.pack(side="left", padx=5)
        self.id_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # Department filter
        ctk.CTkLabel(filter_frame, text="Department ▼", font=("Segoe UI", 14),
                   text_color="#2c3e50").pack(side="left", padx=5)
        self.dept_filter = CTkComboBox(filter_frame, width=150, state="readonly")
        self.dept_filter.pack(side="left", padx=5)
        self.dept_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
    
    def setup_table(self, parent):
        table_frame = ctk.CTkFrame(parent, fg_color="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create a custom table using CTkScrollableFrame
        self.table_container = ctk.CTkScrollableFrame(table_frame, fg_color="#ffffff")
        self.table_container.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Table headers
        headers = ["Profile", "Full name", "Department", "Gender", "Email",
                  "Contact number", "Employment Status", "Employee ID"]
        
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(self.table_container, text=header, font=("Segoe UI", 16, "bold"),
                                      text_color="#ffffff", fg_color="#7BC043", width=100 if i == 0 else 150)
            header_label.grid(row=0, column=i, sticky="ew", padx=1, pady=1)
        
        # Configure column weights
        for i in range(len(headers)):
            self.table_container.grid_columnconfigure(i, weight=1)
        
        # Store table data for interaction
        self.table_rows = []
        
        # Add scrollbar
        scrollbar = ctk.CTkScrollbar(table_frame, orientation="vertical", command=self.table_container._parent_canvas.yview)
        self.table_container._parent_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=0, pady=0)
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
    
    def load_employees(self):
        try:
            self.cursor.execute("SELECT * FROM employees")
            self.employees = self.cursor.fetchall()
            self.refresh_table()
            self.update_filter_options()
        except Error as e:
            messagebox.showerror("Error", f"Error loading employees: {e}")
    
    def refresh_table(self, employees_to_show=None):
        # Clear table
        for widget in self.table_container.winfo_children():
            if hasattr(widget, 'row_index') and widget.row_index > 0:  # Skip headers
                widget.destroy()
        
        if employees_to_show is None:
            employees_to_show = self.employees
        
        # Add rows
        for row_idx, emp in enumerate(employees_to_show, 1):
            initials = ''.join([name[0].upper() for name in emp['full_name'].split()])
            
            # Create row widgets
            row_data = [
                f"  {initials}  ",
                emp['full_name'],
                emp['department_name'],
                emp['gender'],
                emp['email'],
                emp['contact_number'] or "",
                "Active",
                f"EMP{emp['employee_id']:03d}"
            ]
            
            row_widgets = []
            for col_idx, data in enumerate(row_data):
                cell = ctk.CTkLabel(self.table_container, text=data, font=("Segoe UI", 14),
                                  text_color="#2c3e50", fg_color="#ffffff", width=100 if col_idx == 0 else 150)
                cell.grid(row=row_idx, column=col_idx, sticky="ew", padx=1, pady=1)
                cell.row_index = row_idx
                cell.col_index = col_idx
                cell.emp_data = emp  # Store employee data for interaction
                row_widgets.append(cell)
            
            self.table_rows.append(row_widgets)
    
    def update_filter_options(self):
        names = [""] + sorted(list(set([e['full_name'] for e in self.employees])))
        ids = [""] + sorted(list(set([f"EMP{e['employee_id']:03d}" for e in self.employees])))
        depts = [""] + sorted(list(set([e['department_name'] for e in self.employees])))
        
        self.name_filter['values'] = names
        self.id_filter['values'] = ids
        self.dept_filter['values'] = depts
    
    def perform_search(self):
        search_term = self.search_var.get().lower()
        if not search_term:
            self.refresh_table()
            return
        
        filtered = [e for e in self.employees 
                   if search_term in e['full_name'].lower() 
                   or search_term in e['email'].lower()]
        self.refresh_table(filtered)
    
    def apply_filters(self):
        name_filter = self.name_filter.get()
        id_filter = self.id_filter.get()
        dept_filter = self.dept_filter.get()
        
        filtered = self.employees.copy()
        
        if name_filter:
            filtered = [e for e in filtered if e['full_name'] == name_filter]
        if id_filter:
            emp_id = int(id_filter.replace("EMP", ""))
            filtered = [e for e in filtered if e['employee_id'] == emp_id]
        if dept_filter:
            filtered = [e for e in filtered if e['department_name'] == dept_filter]
        
        self.refresh_table(filtered)
    
    def add_employee(self):
        add_window = ctk.CTkToplevel(self.root)
        add_window.title("Add Employee")
        add_window.geometry("500x450")
        add_window.transient(self.root)
        add_window.grab_set()
        
        fields = {}
        field_labels = [
            ("Full Name", "full_name"),
            ("Department", "department"),
            ("Gender", "gender"),
            ("Email", "email"),
            ("Contact Number", "contact"),
            ("Employment Date (YYYY-MM-DD)", "employment_date")
        ]
        
        for label, key in field_labels:
            ctk.CTkLabel(add_window, text=label, font=("Segoe UI", 10),
                       text_color="#2c3e50").pack(anchor="w", padx=20, pady=2)
            
            if key == "gender":
                var = ctk.StringVar()
                var.set("Male")
                gender_menu = CTkComboBox(add_window, variable=var,
                                        values=["Male", "Female", "Other"], state="readonly")
                gender_menu.pack(fill="x", padx=20, pady=8)
                fields[key] = var
            else:
                entry = ctk.CTkEntry(add_window, font=("Segoe UI", 10))
                entry.pack(fill="x", padx=20, pady=8)
                fields[key] = entry
        
        def save_employee():
            try:
                full_name = fields['full_name'].get()
                department = fields['department'].get()
                gender = fields['gender'].get()
                email = fields['email'].get()
                contact = fields['contact'].get()
                emp_date = fields['employment_date'].get()
                
                if not all([full_name, department, gender, email, emp_date]):
                    ctk.CTkMessagebox(title="Incomplete", message="Please fill all required fields", icon="warning")
                    return
                
                # Validate email
                if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
                    ctk.CTkMessagebox(title="Invalid Email", message="Please enter a valid email", icon="error")
                    return
                
                # Validate date
                datetime.strptime(emp_date, "%Y-%m-%d")
                
                insert_query = """
                INSERT INTO employees (full_name, department_name, gender, email, contact_number, employment_date)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                
                self.cursor.execute(insert_query, (full_name, department, gender, email, contact or None, emp_date))
                self.conn.commit()
                
                ctk.CTkMessagebox(title="Success", message="Employee added successfully!", icon="check")
                add_window.destroy()
                self.load_employees()
                
            except Error as e:
                ctk.CTkMessagebox(title="Error", message=f"Error adding employee: {e}", icon="error")
            except ValueError:
                ctk.CTkMessagebox(title="Invalid Date", message="Please use YYYY-MM-DD format for date", icon="error")
        
        save_btn = ctk.CTkButton(add_window, text="Save Employee", command=save_employee,
                               fg_color="#27ae60", text_color="white", font=("Segoe UI", 11, "bold"),
                               cursor="hand2", width=200, height=40)
        save_btn.pack(pady=20)
    
    def edit_employee(self):
        # Message box functionality removed for CustomTkinter compatibility
        pass
    
    def edit_selected_employee(self, emp=None):
        if not emp:
            # Message box functionality removed for CustomTkinter compatibility
            return
        
        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title("Edit Employee")
        edit_window.geometry("500x450")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        fields = {}
        field_labels = [
            ("Full Name", "full_name", emp['full_name']),
            ("Department", "department", emp['department_name']),
            ("Gender", "gender", emp['gender']),
            ("Email", "email", emp['email']),
            ("Contact Number", "contact", emp['contact_number'] or ""),
            ("Employment Date", "employment_date", emp['employment_date'].strftime("%Y-%m-%d"))
        ]
        
        for label, key, value in field_labels:
            ctk.CTkLabel(edit_window, text=label, font=("Segoe UI", 10),
                       text_color="#2c3e50").pack(anchor="w", padx=20, pady=2)
            
            if key == "gender":
                var = ctk.StringVar()
                var.set(value)
                gender_menu = CTkComboBox(edit_window, variable=var,
                                        values=["Male", "Female", "Other"], state="readonly")
                gender_menu.pack(fill="x", padx=20, pady=8)
                fields[key] = var
            else:
                entry = ctk.CTkEntry(edit_window, font=("Segoe UI", 10))
                entry.insert(0, value)
                entry.pack(fill="x", padx=20, pady=8)
                fields[key] = entry
        
        def update_employee():
            try:
                update_query = """
                UPDATE employees SET full_name=%s, department_name=%s, gender=%s,
                email=%s, contact_number=%s, employment_date=%s WHERE employee_id=%s
                """
                
                self.cursor.execute(update_query, (
                    fields['full_name'].get(),
                    fields['department'].get(),
                    fields['gender'].get(),
                    fields['email'].get(),
                    fields['contact'].get() or None,
                    fields['employment_date'].get(),
                    emp['employee_id']
                ))
                self.conn.commit()
                
                ctk.CTkMessagebox(title="Success", message="Employee updated successfully!", icon="check")
                edit_window.destroy()
                self.load_employees()
                
            except Error as e:
                ctk.CTkMessagebox(title="Error", message=f"Error updating employee: {e}", icon="error")
        
        update_btn = ctk.CTkButton(edit_window, text="Update Employee", command=update_employee,
                                 fg_color="#27ae60", text_color="white", font=("Segoe UI", 11, "bold"),
                                 cursor="hand2", width=200, height=40)
        update_btn.pack(pady=20)
    
    def delete_employee(self):
        # Get selected employee from table interaction
        # For now, show a message since we need to implement row selection
        pass
    
    def search_employee(self):
        ctk.CTkMessagebox(title="Search", message="Use the search bar above to find employees by name or email", icon="info")
    
    def view_employee(self):
        # Get selected employee from table interaction
        # For now, show a message since we need to implement row selection
        pass
    
    def leave_request(self):
        # Feature coming soon - message box removed for CustomTkinter compatibility
        pass
    
    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    root = ctk.CTk()
    app = HREmployeeApp(root)
    root.mainloop()
