import customtkinter as ctk
import sys
import os
from tkinter import messagebox, ttk

# Adds the BITS-EMS folder to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the service
from DB_Service.Dep_job_db import DBService 

# In JobTitle_Page.py
class JobTitlePage(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Job Title Management")
        self.geometry("1000x700")
        self.configure(fg_color="#FFFFFF")
        self.resizable(True, True)

        self.transient(master)
        self.grab_set()
        self.db_service = DBService()

        self.primary_green = "#8CC63F"
        self.dark_green = "#6BA336"
        self.light_green = "#E8F5E9"
        self.white = "#FFFFFF"
        self.dark_text = "#1A3752"
        self.light_text = "#666666"
        
        # Main container
        main_container = ctk.CTkFrame(self, fg_color=self.white)
        main_container.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Title
        ctk.CTkLabel(main_container, text="Job Title Management", 
                     text_color=self.dark_text, font=("Arial", 28, "bold")).pack(pady=(0, 30))
        
        # Create two columns
        columns_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        columns_frame.pack(fill="both", expand=True)
        
        # Left column - Add Job Title
        left_frame = ctk.CTkFrame(columns_frame, fg_color=self.white, corner_radius=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        ctk.CTkLabel(left_frame, text="Add New Job Title", 
                     font=("Arial", 20, "bold"), text_color=self.dark_text).pack(pady=(20, 20))
        
        # Job Title
        ctk.CTkLabel(left_frame, text="Job Title:", anchor="w", text_color=self.dark_text).pack(fill="x", padx=20, pady=(5, 0))
        self.job_title_entry = ctk.CTkEntry(left_frame, fg_color=self.white, border_color=self.primary_green)
        self.job_title_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Description
        ctk.CTkLabel(left_frame, text="Description:", anchor="w", text_color=self.dark_text).pack(fill="x", padx=20, pady=(5, 0))
        self.job_desc_text = ctk.CTkTextbox(left_frame, height=100, fg_color=self.white, border_color=self.primary_green)
        self.job_desc_text.pack(fill="x", padx=20, pady=(0, 15))
        
        # Status
        ctk.CTkLabel(left_frame, text="Status:", anchor="w", text_color=self.dark_text).pack(fill="x", padx=20, pady=(5, 0))
        status_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        status_frame.pack(fill="x", padx=20, pady=5)
        self.status_var = ctk.StringVar(value="Active")
        ctk.CTkRadioButton(status_frame, text="Active", variable=self.status_var, 
                          value="Active", text_color=self.dark_text,
                          fg_color=self.primary_green, hover_color=self.dark_green).pack(side="left", padx=15)
        ctk.CTkRadioButton(status_frame, text="Inactive", variable=self.status_var, 
                          value="Inactive", text_color=self.dark_text,
                          fg_color=self.primary_green, hover_color=self.dark_green).pack(side="left", padx=15)
        
        # Add Button
        ctk.CTkButton(left_frame, text="Add Job Title", command=self.save_job_title,
                     fg_color=self.primary_green, hover_color=self.dark_green,
                     text_color=self.white, font=("Arial", 14, "bold"), 
                     height=40).pack(pady=20, padx=20)
        
        # Right column - View/Manage Job Titles
        right_frame = ctk.CTkFrame(columns_frame, fg_color=self.white, corner_radius=10)
        right_frame.pack(side="right", fill="both", expand=True)
        
        ctk.CTkLabel(right_frame, text="Existing Job Titles", 
                     font=("Arial", 20, "bold"), text_color=self.dark_text).pack(pady=(20, 20))
        
        # Search frame
        search_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(search_frame, text="Search:", text_color=self.dark_text).pack(side="left", padx=5)
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.load_job_titles)
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, 
                                        width=200, placeholder_text="Search job titles...",
                                        fg_color=self.white, border_color=self.primary_green)
        self.search_entry.pack(side="left", padx=10)
        
        refresh_btn = ctk.CTkButton(search_frame, text="Refresh", command=self.load_job_titles, 
                                   width=100, fg_color=self.primary_green, hover_color=self.dark_green)
        refresh_btn.pack(side="left", padx=10)
        
        # Treeview for job titles
        self.tree_frame = ctk.CTkFrame(right_frame, fg_color=self.white)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create a frame for the tree and scrollbars
        tree_container = ctk.CTkFrame(self.tree_frame, fg_color=self.white)
        tree_container.pack(fill="both", expand=True)
        
        # Create vertical scrollbar
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical")
        v_scrollbar.pack(side="right", fill="y")
        
        # Style the treeview
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure treeview colors
        style.configure("Treeview",
                        background=self.white,
                        foreground=self.dark_text,
                        fieldbackground=self.white,
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        background=self.primary_green,
                        foreground=self.white,
                        relief="flat",
                        font=("Arial", 10, "bold"))
        style.map("Treeview.Heading",
                  background=[('active', self.dark_green)])
        
        # Create Treeview
        self.job_tree = ttk.Treeview(
            tree_container,
            columns=("ID", "Title", "Description", "Status", "EmployeeCount"),
            show="headings",
            yscrollcommand=v_scrollbar.set,
            height=15,
            style="Custom.Treeview"
        )
        
        # Configure scrollbars
        v_scrollbar.config(command=self.job_tree.yview)
        
        # Define headings
        columns = [
            ("ID", "ID", 50),
            ("Title", "Job Title", 150),
            ("Description", "Description", 250),
            ("Status", "Status", 80),
            ("EmployeeCount", "Employees", 80)
        ]
        
        for col_id, heading, width in columns:
            self.job_tree.heading(col_id, text=heading)
            self.job_tree.column(col_id, width=width, minwidth=50)
        
        self.job_tree.pack(fill="both", expand=True)
        
        # Action buttons frame
        action_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        action_frame.pack(pady=10, padx=20)
        
        toggle_btn = ctk.CTkButton(action_frame, text="Toggle Status", 
                                  command=self.toggle_job_status,
                                  fg_color=self.primary_green, hover_color=self.dark_green)
        toggle_btn.pack(side="left", padx=10)
        
        edit_btn = ctk.CTkButton(action_frame, text="Edit Description", 
                                command=self.edit_job_description,
                                fg_color=self.primary_green, hover_color=self.dark_green)
        edit_btn.pack(side="left", padx=10)
        
        # Load job titles initially
        self.load_job_titles()

    def load_job_titles(self, *args):
        # Clear existing items
        for item in self.job_tree.get_children():
            self.job_tree.delete(item)
        
        search_term = self.search_var.get()
        
        try:
            # Use the new method from DBService
            job_titles = self.db_service.get_all_job_titles(search_term)
            
            for job in job_titles:
                job_id, title_name, description, active, employee_count = job
                
                status = "Active" if active == 1 else "Inactive"
                desc_short = description[:50] + "..." if description and len(description) > 50 else description or ""
                
                # Add tag for status color
                tags = ("active",) if active == 1 else ("inactive",)
                
                self.job_tree.insert("", "end", values=(
                    job_id, title_name, desc_short, status, employee_count
                ), tags=tags)
            
            # Configure tag colors
            self.job_tree.tag_configure("active", foreground="#2E7D32")  # Green for active
            self.job_tree.tag_configure("inactive", foreground="#D32F2F")  # Red for inactive
                
        except Exception as e:
            print(f"Error loading job titles: {e}")
            messagebox.showerror("Error", f"Failed to load job titles: {str(e)}")

    def save_job_title(self):
        title = self.job_title_entry.get()
        description = self.job_desc_text.get("1.0", "end-1c").strip()
        is_active = True if self.status_var.get() == "Active" else False

        if not title:
            messagebox.showwarning("Incomplete Form", "Please enter a job title.")
            return

        try:
            success = self.db_service.insert_job_title(
                title=title, 
                description=description, 
                active=is_active
            )
            
            if success:
                messagebox.showinfo("Success", f"Job Title '{title}' added successfully!")
                # Clear form
                self.job_title_entry.delete(0, 'end')
                self.job_desc_text.delete("1.0", "end")
                # Refresh list
                self.load_job_titles()
        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {e}")

    def toggle_job_status(self):
        selection = self.job_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a job title.")
            return
        
        item = self.job_tree.item(selection[0])
        job_id = item['values'][0]
        job_title = item['values'][1]
        current_status = item['values'][3]
        
        new_status = "Inactive" if current_status == "Active" else "Active"
        
        if messagebox.askyesno("Confirm", f"Change status of '{job_title}' to {new_status}?"):
            try:
                success = self.db_service.toggle_job_title_status(job_id)
                
                if success:
                    messagebox.showinfo("Success", f"Job title status updated to {new_status}.")
                    self.load_job_titles()
                else:
                    messagebox.showerror("Error", "Failed to update status.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update status: {str(e)}")

    def edit_job_description(self):
        selection = self.job_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a job title.")
            return
        
        item = self.job_tree.item(selection[0])
        job_id = item['values'][0]
        job_title = item['values'][1]
        
        # Get current description
        try:
            job_details = self.db_service.get_job_title_details(job_id)
            if job_details:
                job_id, title_name, description, active = job_details
                current_desc = description or ""
                
                # Create edit popup with white/green theme
                popup = ctk.CTkToplevel(self)
                popup.title(f"Edit Description: {job_title}")
                popup.geometry("500x400")
                popup.configure(fg_color=self.white)
                popup.grab_set()
                
                ctk.CTkLabel(popup, text=f"Edit Description for '{job_title}'", 
                           font=("Arial", 16, "bold"), text_color=self.dark_text).pack(pady=20)
                
                desc_text = ctk.CTkTextbox(popup, width=450, height=200,
                                         fg_color=self.white, border_color=self.primary_green)
                desc_text.pack(pady=10, padx=20)
                desc_text.insert("1.0", current_desc)
                
                def save_description():
                    new_desc = desc_text.get("1.0", "end-1c").strip()
                    try:
                        success = self.db_service.update_job_title_description(job_id, new_desc)
                        
                        if success:
                            messagebox.showinfo("Success", "Description updated.")
                            popup.destroy()
                            self.load_job_titles()
                        else:
                            messagebox.showerror("Error", "Failed to update description.")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to update: {str(e)}")
                
                save_btn = ctk.CTkButton(popup, text="Save", command=save_description,
                                       fg_color=self.primary_green, hover_color=self.dark_green)
                save_btn.pack(pady=20)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load description: {str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1000x700")
    page = JobTitlePage(root)
    page.pack(expand=True, fill="both")
    root.mainloop()