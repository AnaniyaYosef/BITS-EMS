import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import messagebox, ttk
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB_Service.Leave_Req_db import LeaveRequestDB

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class LeaveRequestPage(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Leave Management System")
        self.geometry("900x800")
        self.resizable(True, True)
        self.configure(fg_color="#FFFFFF")
        self.minsize(800, 700)
        
        if master:
            self.transient(master)
            self.grab_set()
        
        self.db = LeaveRequestDB()
        self.primary_green = "#8CC63F"
        self.dark_green = "#6BA336"
        self.white = "#FFFFFF"
        self.dark_text = "#1A3752"
        self.light_gray = "#F5F5F5"
        
        # Create notebook for tabs
        self.notebook = ctk.CTkTabview(self, fg_color=self.white)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.request_tab = self.notebook.add("Request Leave")
        self.current_tab = self.notebook.add("Current on Leave")
        self.history_tab = self.notebook.add("Leave History")
        
        # Setup each tab
        self.setup_request_tab()
        self.setup_current_tab()
        self.setup_history_tab()
        
        self.center_window()

    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def setup_request_tab(self):
        """Setup the leave request tab with scrollable frame"""
        # Create main scrollable frame
        main_container = ctk.CTkFrame(self.request_tab, fg_color=self.white)
        main_container.pack(fill="both", expand=True)
        
        # Create canvas and scrollbar
        canvas = ctk.CTkCanvas(main_container, highlightthickness=0, bg=self.white)
        scrollbar = ctk.CTkScrollbar(main_container, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color=self.white)
        
        # Configure canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Create window in canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=800)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack everything
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Content
        title_label = ctk.CTkLabel(
            scrollable_frame, 
            text="Leave Request Form",
            text_color=self.dark_text,
            font=("Arial", 28, "bold")
        )
        title_label.pack(pady=(0, 30))
        
        # Employee selection with better display
        employee_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.light_gray, corner_radius=8)
        employee_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            employee_frame,
            text="Select Employee:",
            text_color=self.dark_text,
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        # Fetch employees - YOUR DATABASE DOESN'T HAVE Employee_Code
        employees_data = self.db.fetch_active_employees()
        employee_display = []
        self.employee_id_map = {}  # Store mapping for lookup
        
        # Display employees with ID since there's no Employee_Code
        for emp_id, emp_name, _ in employees_data:  # Third element is empty
            display_text = f"{emp_name} (ID: {emp_id})"
            employee_display.append(display_text)
            self.employee_id_map[display_text] = emp_id
        
        self.employee_var = ctk.StringVar(value="Select Employee")
        
        self.employee_dropdown = ctk.CTkOptionMenu(
            employee_frame,
            values=employee_display,
            variable=self.employee_var,
            fg_color=self.white,
            button_color=self.primary_green,
            button_hover_color=self.dark_green,
            dropdown_fg_color=self.white,
            dropdown_text_color=self.dark_text,
            width=400
        )
        self.employee_dropdown.pack(padx=20, pady=(0, 15))
        
        # Leave details
        details_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.light_gray, corner_radius=8)
        details_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            details_frame,
            text="Leave Details:",
            text_color=self.dark_text,
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        # Leave type
        ctk.CTkLabel(
            details_frame,
            text="Leave Type:",
            text_color=self.dark_text
        ).pack(anchor="w", padx=20, pady=(5, 0))
        
        leave_types = ["Sick Leave", "Annual Leave", "Maternity Leave", "Paternity Leave", 
                      "Emergency Leave", "Unpaid Leave", "Other"]
        self.leave_type_var = ctk.StringVar(value="Sick Leave")
        
        self.leave_type_dropdown = ctk.CTkOptionMenu(
            details_frame,
            values=leave_types,
            variable=self.leave_type_var,
            fg_color=self.white,
            button_color=self.primary_green,
            button_hover_color=self.dark_green,
            dropdown_fg_color=self.white,
            dropdown_text_color=self.dark_text,
            width=400
        )
        self.leave_type_dropdown.pack(padx=20, pady=(0, 15))
        
        # Date selection
        date_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        date_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(
            date_frame,
            text="Start Date:",
            text_color=self.dark_text
        ).pack(side="left", padx=(0, 10))
        
        self.start_date_entry = DateEntry(
            date_frame,
            width=15,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            font=("Arial", 11),
            date_pattern='yyyy-mm-dd'
        )
        self.start_date_entry.pack(side="left", padx=(0, 30))
        
        ctk.CTkLabel(
            date_frame,
            text="End Date:",
            text_color=self.dark_text
        ).pack(side="left", padx=(0, 10))
        
        self.end_date_entry = DateEntry(
            date_frame,
            width=15,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            font=("Arial", 11),
            date_pattern='yyyy-mm-dd'
        )
        self.end_date_entry.pack(side="left")
        
        # Calculate duration
        duration_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        duration_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.duration_label = ctk.CTkLabel(
            duration_frame,
            text="Duration: 0 day(s)",
            text_color=self.dark_text,
            font=("Arial", 12)
        )
        self.duration_label.pack(side="left")
        
        # Bind date changes to update duration
        self.start_date_entry.bind("<<DateEntrySelected>>", self.update_duration)
        self.end_date_entry.bind("<<DateEntrySelected>>", self.update_duration)
        
        # Reason
        reason_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.light_gray, corner_radius=8)
        reason_frame.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(
            reason_frame,
            text="Reason for Leave:",
            text_color=self.dark_text,
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.reason_text = ctk.CTkTextbox(
            reason_frame,
            height=120,
            fg_color=self.white,
            border_color=self.primary_green,
            border_width=1,
            text_color=self.dark_text,
            font=("Arial", 12)
        )
        self.reason_text.pack(padx=20, pady=(0, 15), fill="x")
        
        # Buttons
        button_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        button_frame.pack(pady=(10, 0))
        
        submit_btn = ctk.CTkButton(
            button_frame,
            text="Submit Leave Request",
            command=self.submit_leave_request,
            fg_color=self.primary_green,
            hover_color=self.dark_green,
            text_color=self.white,
            font=("Arial", 14, "bold"),
            height=45,
            width=200
        )
        submit_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            fg_color="#E0E0E0",
            hover_color="#D0D0D0",
            text_color=self.dark_text,
            font=("Arial", 14),
            height=45,
            width=120
        )
        cancel_btn.pack(side="left", padx=10)
        
        self.status_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            text_color=self.dark_text,
            font=("Arial", 12)
        )
        self.status_label.pack(pady=(20, 0))

    def update_duration(self, event=None):
        """Update duration label when dates change"""
        try:
            start_date = self.start_date_entry.get_date()
            end_date = self.end_date_entry.get_date()
            
            if start_date and end_date:
                days = (end_date - start_date).days + 1
                if days > 0:
                    self.duration_label.configure(
                        text=f"Duration: {days} day(s)",
                        text_color="#2E7D32" if days <= 30 else "#F57C00"
                    )
                else:
                    self.duration_label.configure(
                        text="Invalid date range",
                        text_color="#D32F2F"
                    )
        except:
            pass

    def setup_current_tab(self):
        """Setup tab showing current employees on leave"""
        main_frame = ctk.CTkFrame(self.current_tab, fg_color=self.white)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Employees Currently on Leave",
            text_color=self.dark_text,
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Create treeview frame
        tree_frame = ctk.CTkFrame(main_frame, fg_color=self.white)
        tree_frame.pack(fill="both", expand=True)
        
        # Create treeview - REMOVED "Employee Code" column
        columns = ("Employee", "Leave Type", "Start Date", "End Date", "Days Remaining", "Status")
        self.current_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        # Configure columns
        col_widths = [200, 150, 120, 120, 120, 100]  # Adjusted widths
        for col, width in zip(columns, col_widths):
            self.current_tree.heading(col, text=col)
            self.current_tree.column(col, width=width, minwidth=80)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.current_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.current_tree.xview)
        self.current_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.current_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=(20, 0))
        
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="Refresh",
            command=self.load_current_leave,
            fg_color=self.primary_green,
            hover_color=self.dark_green,
            width=120
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Load data
        self.load_current_leave()

    def setup_history_tab(self):
        """Setup tab showing leave history"""
        main_frame = ctk.CTkFrame(self.history_tab, fg_color=self.white)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Leave History",
            text_color=self.dark_text,
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Search frame
        search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(search_frame, text="Search:", text_color=self.dark_text).pack(side="left", padx=5)
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Search by employee name...",
            width=300
        )
        self.search_entry.pack(side="left", padx=10)
        
        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.load_leave_history,
            fg_color=self.primary_green,
            hover_color=self.dark_green,
            width=100
        )
        search_btn.pack(side="left", padx=5)
        
        clear_btn = ctk.CTkButton(
            search_frame,
            text="Clear",
            command=self.clear_search,
            fg_color="#E0E0E0",
            hover_color="#D0D0D0",
            text_color=self.dark_text,
            width=80
        )
        clear_btn.pack(side="left", padx=5)
        
        # Create treeview frame
        tree_frame = ctk.CTkFrame(main_frame, fg_color=self.white)
        tree_frame.pack(fill="both", expand=True)
        
        # Create treeview
        columns = ("Employee", "Leave Type", "Start Date", "End Date", "Duration", "Status", "Submitted Date")
        self.history_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        # Configure columns
        col_widths = [200, 150, 120, 120, 80, 100, 120]  # Adjusted widths
        for col, width in zip(columns, col_widths):
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=width, minwidth=80)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.history_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.history_tree.xview)
        self.history_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.history_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Load data
        self.load_leave_history()

    def load_current_leave(self):
        """Load employees currently on leave"""
        # Clear existing items
        for item in self.current_tree.get_children():
            self.current_tree.delete(item)
        
        try:
            current_leaves = self.db.get_current_leave_employees()
            
            for leave in current_leaves:
                # leave structure: (name, "", leave_type, start_date, end_date, days_remaining, status)
                emp_name, _, leave_type, start_date, end_date, days_remaining, status = leave
                
                # Add to treeview without employee code
                self.current_tree.insert("", "end", values=(
                    emp_name,
                    leave_type,
                    start_date.strftime('%Y-%m-%d') if start_date else "",
                    end_date.strftime('%Y-%m-%d') if end_date else "",
                    days_remaining,
                    status
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load current leave data: {str(e)}")
            print(f"Error details: {e}")

    def load_leave_history(self):
        """Load leave history with search"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        search_term = self.search_var.get()
        
        try:
            history = self.db.get_leave_history(search_term)
            
            for record in history:
                # record structure: (name, leave_type, start_date, end_date, duration, status, submitted_date)
                emp_name, leave_type, start_date, end_date, duration, status, submitted_date = record
                
                # Add to treeview
                self.history_tree.insert("", "end", values=(
                    emp_name,
                    leave_type,
                    start_date.strftime('%Y-%m-%d') if start_date else "",
                    end_date.strftime('%Y-%m-%d') if end_date else "",
                    f"{duration} days" if duration else "0 days",
                    status,
                    submitted_date.strftime('%Y-%m-%d %H:%M') if submitted_date else ""
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load leave history: {str(e)}")
            print(f"Error details: {e}")

    def clear_search(self):
        """Clear search field and reload all history"""
        self.search_var.set("")
        self.load_leave_history()

    def submit_leave_request(self):
        """Submit the leave request to database"""
        emp_display = self.employee_var.get()
        leave_type = self.leave_type_var.get()
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        reason = self.reason_text.get("1.0", "end-1c").strip()
        
        if emp_display == "Select Employee" or not emp_display:
            messagebox.showwarning("Input Error", "Please select an employee.")
            return
            
        if not reason:
            messagebox.showwarning("Input Error", "Please provide a reason for leave.")
            return
            
        if end_date < start_date:
            messagebox.showwarning("Input Error", "End date cannot be before start date.")
            return
            
        days_requested = (end_date - start_date).days + 1
        if days_requested <= 0:
            messagebox.showwarning("Input Error", "Invalid date range.")
            return
        
        # Get employee ID from mapping
        emp_id = self.employee_id_map.get(emp_display)
        if not emp_id:
            messagebox.showwarning("Error", "Could not find employee ID.")
            return
        
        confirm_msg = f"""
        Please confirm leave request details:
        
        Employee: {emp_display}
        Leave Type: {leave_type}
        Start Date: {start_date.strftime('%Y-%m-%d')}
        End Date: {end_date.strftime('%Y-%m-%d')}
        Duration: {days_requested} day(s)
        
        Reason: {reason[:100]}{'...' if len(reason) > 100 else ''}
        
        Submit this request?
        """
        
        if not messagebox.askyesno("Confirm Leave Request", confirm_msg):
            return
        
        try:
            success, message = self.db.submit_leave_request(
                emp_id=emp_id,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                reason=reason
            )
            
            if success:
                messagebox.showinfo("Success", message)
                self.status_label.configure(
                    text=f"✓ Leave request submitted successfully!",
                    text_color="#2E7D32"
                )
                self.clear_form()
                # Refresh current leave tab
                self.load_current_leave()
                # Refresh history tab
                self.load_leave_history()
                # Switch to current tab
                self.notebook.set("Current on Leave")
            else:
                messagebox.showerror("Error", message)
                self.status_label.configure(
                    text=f"✗ Error: {message}",
                    text_color="#D32F2F"
                )
                
        except Exception as e:
            messagebox.showerror("System Error", f"An unexpected error occurred: {str(e)}")
            self.status_label.configure(
                text="✗ System error occurred",
                text_color="#D32F2F"
            )

    def clear_form(self):
        """Clear the form after successful submission"""
        self.employee_var.set("Select Employee")
        self.leave_type_var.set("Sick Leave")
        
        tomorrow = datetime.now().date()
        day_after = datetime.now().date()
        
        self.start_date_entry.set_date(tomorrow)
        self.end_date_entry.set_date(day_after)
        self.update_duration()
        
        self.reason_text.delete("1.0", "end")
        self.after(5000, lambda: self.status_label.configure(text=""))


if __name__ == "__main__":
    root = ctk.CTk()
    leave_window = LeaveRequestPage(root)
    root.mainloop()