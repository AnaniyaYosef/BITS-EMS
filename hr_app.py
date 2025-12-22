import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import re

class HREmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HR Employee Management System")
        self.root.geometry("1400x800")
        self.root.configure(bg="#f4f6f8")
        self.root.resizable(True, True)
        
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
        main_container = tk.Frame(self.root, bg="#f9fafb", bd=0, relief=tk.FLAT)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.setup_sidebar(main_container)
        
        # Content area
        content_frame = tk.Frame(main_container, bg="#f9fafb", bd=0, relief=tk.FLAT)
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Header
        self.setup_header(content_frame)
        
        # Search bar
        self.setup_search_bar(content_frame)
        
        # Filters
        self.setup_filters(content_frame)
        
        # Table
        self.setup_table(content_frame)
    
    def setup_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg="#7BC043", width=200, bd=0, relief=tk.FLAT)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Title with icon
        title_frame = tk.Frame(sidebar, bg="#7BC043")
        title_frame.pack(fill=tk.X, pady=20)
        
        title = tk.Label(title_frame, text="HR", font=("Segoe UI", 24, "bold"),
                        bg="#7BC043", fg="white")
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Management", font=("Segoe UI", 10),
                           bg="#7BC043", fg="#e8f5e9")
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
            btn = tk.Button(sidebar, text=item_text, bg="#7BC043", fg="white",
                           font=("Segoe UI", 10), cursor="hand2",
                           command=command, relief=tk.FLAT,
                           padx=15, pady=12, anchor="w", bd=0, highlightthickness=0)
            btn.pack(fill=tk.X, padx=10, pady=2)
            btn.bind("<Enter>", lambda e: e.widget.config(bg="#6BA835"))
            btn.bind("<Leave>", lambda e: e.widget.config(bg="#7BC043"))
    
    def setup_header(self, parent):
        header = tk.Frame(parent, bg="#ffffff", bd=0, relief=tk.FLAT)
        header.pack(fill=tk.X, padx=20, pady=15)
        
        # Header with shadow effect
        header_container = tk.Frame(header, bg="#ffffff", relief=tk.RAISED, bd=1)
        header_container.pack(fill=tk.X, padx=0, pady=0)
        
        title_frame = tk.Frame(header_container, bg="#ffffff")
        title_frame.pack(fill=tk.X, padx=20, pady=15)
        
        title = tk.Label(title_frame, text="Employee Management", font=("Segoe UI", 24, "bold"),
                        bg="#ffffff", fg="#2c3e50")
        title.pack(anchor="w")
        
        subtitle = tk.Label(title_frame, text="Manage your team efficiently", font=("Segoe UI", 10),
                           bg="#ffffff", fg="#7f8c8d")
        subtitle.pack(anchor="w", pady=2)
    
    def setup_search_bar(self, parent):
        search_frame = tk.Frame(parent, bg="#ffffff", bd=0, relief=tk.FLAT)
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(search_frame, text="Search:", bg="#ffffff",
                font=("Segoe UI", 10), fg="#2c3e50").pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               font=("Segoe UI", 11), width=50, highlightthickness=0)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.insert(0, "John Doe")
        
        search_btn = tk.Button(search_frame, text="🔍", font=("Segoe UI", 12),
                              command=self.perform_search, relief=tk.FLAT,
                              bg="#3498db", fg="white", cursor="hand2", padx=15,
                              highlightthickness=0)
        search_btn.pack(side=tk.LEFT, padx=5)
        search_btn.bind("<Enter>", lambda e: e.widget.config(bg="#2980b9"))
        search_btn.bind("<Leave>", lambda e: e.widget.config(bg="#3498db"))
        
        search_entry.bind("<Return>", lambda e: self.perform_search())
    
    def setup_filters(self, parent):
        filter_frame = tk.Frame(parent, bg="#ffffff", bd=0, relief=tk.FLAT)
        filter_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(filter_frame, text="Filters:", bg="#ffffff",
                font=("Segoe UI", 10, "bold"), fg="#2c3e50").pack(side=tk.LEFT, padx=5)
        
        # Name filter
        tk.Label(filter_frame, text="Name ▼", bg="#ffffff",
                font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        self.name_filter = ttk.Combobox(filter_frame, width=15, state="readonly",
                                       style="Custom.TCombobox")
        self.name_filter.pack(side=tk.LEFT, padx=5)
        self.name_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # Employee ID filter
        tk.Label(filter_frame, text="Employee ID ▼", bg="#ffffff",
                font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        self.id_filter = ttk.Combobox(filter_frame, width=15, state="readonly",
                                     style="Custom.TCombobox")
        self.id_filter.pack(side=tk.LEFT, padx=5)
        self.id_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # Department filter
        tk.Label(filter_frame, text="Department ▼", bg="#ffffff",
                font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        self.dept_filter = ttk.Combobox(filter_frame, width=15, state="readonly",
                                      style="Custom.TCombobox")
        self.dept_filter.pack(side=tk.LEFT, padx=5)
        self.dept_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
    
    def setup_table(self, parent):
        table_frame = tk.Frame(parent, bg="#ffffff", bd=0, relief=tk.FLAT)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create treeview with modern styling
        columns = ("Profile", "Full name", "Department", "Gender", "Email",
                   "Contact number", "Employment Status", "Employee ID")
        
        self.tree = ttk.Treeview(table_frame, columns=columns, height=20, show="headings",
                                selectmode="browse", style="Custom.Treeview")
        self.tree.column("Profile", width=80, anchor=tk.CENTER)
        self.tree.column("Full name", width=200)
        self.tree.column("Department", width=150)
        self.tree.column("Gender", width=100)
        self.tree.column("Email", width=220)
        self.tree.column("Contact number", width=140)
        self.tree.column("Employment Status", width=140)
        self.tree.column("Employee ID", width=120)
        
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.W)
        
        # Modern styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                       font=("Segoe UI", 10),
                       rowheight=30,
                       background="#ffffff",
                       foreground="#2c3e50",
                       fieldbackground="#ffffff",
                       borderwidth=0,
                       relief="flat")
        style.configure("Treeview.Heading",
                       font=("Segoe UI", 10, "bold"),
                       background="#7BC043",
                       foreground="#ffffff",
                       borderwidth=0,
                       relief="flat")
        style.map("Treeview", background=[('selected', '#3498db')])
        style.configure("Custom.Treeview", highlightthickness=0, bd=0, relief="flat")
        style.configure("Custom.TCombobox", highlightthickness=0, bd=0, relief="flat")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Remove focus outline from treeview
        self.tree.configure(takefocus=False)
        
        self.tree.bind("<Double-1>", lambda e: self.edit_selected_employee())
    
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
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if employees_to_show is None:
            employees_to_show = self.employees
        
        # Add rows
        for emp in employees_to_show:
            initials = ''.join([name[0].upper() for name in emp['full_name'].split()])
            self.tree.insert("", tk.END, values=(
                f"  {initials}  ",
                emp['full_name'],
                emp['department_name'],
                emp['gender'],
                emp['email'],
                emp['contact_number'] or "",
                "Active",
                f"EMP{emp['employee_id']:03d}"
            ))
    
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
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Employee")
        add_window.geometry("500x450")
        add_window.configure(bg="#ffffff", bd=0, relief=tk.FLAT)
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
            tk.Label(add_window, text=label, bg="#ffffff", font=("Segoe UI", 10), fg="#2c3e50").pack(anchor="w", padx=20, pady=2)
            
            if key == "gender":
                var = tk.StringVar()
                var.set("Male")
                gender_menu = ttk.Combobox(add_window, textvariable=var,
                                          values=["Male", "Female", "Other"], state="readonly",
                                          style="Custom.TCombobox")
                gender_menu.pack(fill=tk.X, padx=20, pady=8)
                fields[key] = var
            else:
                entry = tk.Entry(add_window, font=("Segoe UI", 10), highlightthickness=0)
                entry.pack(fill=tk.X, padx=20, pady=8)
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
                    messagebox.showwarning("Incomplete", "Please fill all required fields")
                    return
                
                # Validate email
                if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
                    messagebox.showerror("Invalid Email", "Please enter a valid email")
                    return
                
                # Validate date
                datetime.strptime(emp_date, "%Y-%m-%d")
                
                insert_query = """
                INSERT INTO employees (full_name, department_name, gender, email, contact_number, employment_date)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                
                self.cursor.execute(insert_query, (full_name, department, gender, email, contact or None, emp_date))
                self.conn.commit()
                
                messagebox.showinfo("Success", "Employee added successfully!")
                add_window.destroy()
                self.load_employees()
                
            except Error as e:
                messagebox.showerror("Error", f"Error adding employee: {e}")
            except ValueError:
                messagebox.showerror("Invalid Date", "Please use YYYY-MM-DD format for date")
        
        save_btn = tk.Button(add_window, text="Save Employee", command=save_employee,
                            bg="#27ae60", fg="white", font=("Segoe UI", 11, "bold"), cursor="hand2",
                            padx=20, pady=10, highlightthickness=0)
        save_btn.pack(pady=20)
        save_btn.bind("<Enter>", lambda e: e.widget.config(bg="#2ecc71"))
        save_btn.bind("<Leave>", lambda e: e.widget.config(bg="#27ae60"))
    
    def edit_employee(self):
        messagebox.showinfo("Edit", "Select an employee from the table and double-click to edit")
    
    def edit_selected_employee(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an employee to edit")
            return
        
        item = selection[0]
        values = self.tree.item(item)['values']
        
        # Find employee by email or name
        emp = None
        for e in self.employees:
            if f"EMP{e['employee_id']:03d}" == values[7]:
                emp = e
                break
        
        if not emp:
            return
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Employee")
        edit_window.geometry("500x450")
        edit_window.configure(bg="#ffffff", bd=0, relief=tk.FLAT)
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
            tk.Label(edit_window, text=label, bg="#ffffff", font=("Segoe UI", 10), fg="#2c3e50").pack(anchor="w", padx=20, pady=2)
            
            if key == "gender":
                var = tk.StringVar()
                var.set(value)
                gender_menu = ttk.Combobox(edit_window, textvariable=var,
                                          values=["Male", "Female", "Other"], state="readonly",
                                          style="Custom.TCombobox")
                gender_menu.pack(fill=tk.X, padx=20, pady=8)
                fields[key] = var
            else:
                entry = tk.Entry(edit_window, font=("Segoe UI", 10), highlightthickness=0)
                entry.insert(0, value)
                entry.pack(fill=tk.X, padx=20, pady=8)
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
                
                messagebox.showinfo("Success", "Employee updated successfully!")
                edit_window.destroy()
                self.load_employees()
                
            except Error as e:
                messagebox.showerror("Error", f"Error updating employee: {e}")
        
        update_btn = tk.Button(edit_window, text="Update Employee", command=update_employee,
                              bg="#27ae60", fg="white", font=("Segoe UI", 11, "bold"), cursor="hand2",
                              padx=20, pady=10, highlightthickness=0)
        update_btn.pack(pady=20)
        update_btn.bind("<Enter>", lambda e: e.widget.config(bg="#2ecc71"))
        update_btn.bind("<Leave>", lambda e: e.widget.config(bg="#27ae60"))
    
    def delete_employee(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an employee to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this employee?"):
            item = selection[0]
            values = self.tree.item(item)['values']
            emp_id = int(values[7].replace("EMP", ""))
            
            try:
                self.cursor.execute("DELETE FROM employees WHERE employee_id=%s", (emp_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Employee deleted successfully!")
                self.load_employees()
            except Error as e:
                messagebox.showerror("Error", f"Error deleting employee: {e}")
    
    def search_employee(self):
        messagebox.showinfo("Search", "Use the search bar above to find employees by name or email")
    
    def view_employee(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an employee to view")
            return
        
        item = selection[0]
        values = self.tree.item(item)['values']
        
        emp = None
        for e in self.employees:
            if f"EMP{e['employee_id']:03d}" == values[7]:
                emp = e
                break
        
        if emp:
            info = f"""
Employee ID: EMP{emp['employee_id']:03d}
Full Name: {emp['full_name']}
Department: {emp['department_name']}
Gender: {emp['gender']}
Email: {emp['email']}
Contact: {emp['contact_number'] or 'N/A'}
Employment Date: {emp['employment_date']}
            """
            messagebox.showinfo("Employee Details", info)
    
    def leave_request(self):
        messagebox.showinfo("Leave Request", "Feature coming soon!")
    
    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = HREmployeeApp(root)
    root.mainloop()
