import customtkinter as ctk
from PIL import Image
import os
import sys

# Ensure project root is on sys.path so imports like `DB_Service` resolve
# when running this file directly (e.g., `python Page/main_page.py`).
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the Dashboard class and Database
try:
    # Preferred when running as a package (python -m Page.main_page)
    from .Dashboard import Dashboard
except Exception:
    # Fallback when running the file directly (python Page/main_page.py)
    from Dashboard import Dashboard

from DB_Service.dashboard_DB import DashboardDB


class EmployeeDashboard(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="#FFFFFF")

        # 1. Window Setup
        self.title("Employee Information Desk")
        self.geometry("1200x850")

        # Configure Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 2. Define Colors
        self.sidebar_color = "#8CC63F"
        self.text_color_primary = "#1D3557"
        self.white_bg = "#FFFFFF"
        self.card_bg_color = "#F8FAFC"
        self.alert_bg_color = "#FEF2F2"
        self.border_color = "#E2E8F0"

        # 3. Initialize Database Helper
        self.db = DashboardDB()

        # Variable to track the notification popup widget
        self.notification_popup = None

        # 4. Create Sections
        self.setup_sidebar()
        self.setup_main_frame_structure()

        # 5. Load Default View (Dashboard)
        self.show_dashboard()

        # 6. Trigger initial notification check
        self.update_header_status()

    def get_asset(self, file_path, size=(20, 20), fallback_color="gray"):
        candidates = []
        candidates.append(file_path)
        try:
            this_dir = os.path.dirname(__file__)
            rel_assets = os.path.abspath(os.path.join(this_dir, '..', 'assets'))
            candidates.append(os.path.join(rel_assets, os.path.basename(file_path)))
        except Exception:
            pass
        try:
            workspace_assets = os.path.abspath(os.path.join(this_dir, '..', '..', 'assets'))
            candidates.append(os.path.join(workspace_assets, os.path.basename(file_path)))
        except Exception:
            pass
        candidates.append(
            os.path.join("C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets", os.path.basename(file_path)))

        for p in candidates:
            if p and os.path.exists(p):
                try:
                    img = Image.open(p)
                    return ctk.CTkImage(light_image=img, dark_image=img, size=size)
                except Exception as e:
                    print(f"Error loading {p}: {e}")

        dummy_img = Image.new("RGB", size, fallback_color)
        return ctk.CTkImage(light_image=dummy_img, size=size)

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0,
                                    fg_color=self.sidebar_color, border_width=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar.grid_rowconfigure(7, weight=1)

        hr_label = ctk.CTkLabel(self.sidebar, text="HR", text_color="white",
                                font=("Arial", 20, "bold"), anchor="w")
        hr_label.grid(row=0, column=0, padx=20, pady=(30, 20), sticky="w")

        menu_items = [
            ("Add Employee", "Add_user.png", self.open_add_employee_window), 
            ("Edit Employee", "Edit_user.png", None),
            ("Delete Employee", "Remove_user.png", None),
            ("Search Employee", "View_employee.png", None),
            ("View Employee", "Search_employe.png", None),
            ("Leave Request Form", "Leave_request.png", None)
        ]

        for i, (text, path, cmd) in enumerate(menu_items):
            img = self.get_asset(path, size=(20, 20), fallback_color="#FFFFFF")
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                image=img,
                fg_color="transparent",
                text_color="white",
                hover_color="#C8D7E2",
                anchor="w",
                font=("Arial", 14),
                height=45,
                command=cmd  
            )
            btn.grid(row=i + 1, column=0, padx=10, pady=2, sticky="ew")

        logout_btn = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            fg_color="#D32F2F",
            text_color="white",
            hover_color="#B71C1C",
            anchor="center",
            font=("Arial", 14, "bold"),
            height=40
        )
        logout_btn.grid(row=8, column=0, padx=20, pady=30, sticky="ew")

    # --- FIXED: RENAMED TO MATCH SIDEBAR AND CHANGED TO POPUP LOGIC ---
    def open_add_employee_window(self):
        try:
            from Page.Add_page import AddEmployeeApp
            # Creates a new independent window
            add_window = AddEmployeeApp()
            add_window.attributes("-topmost", True)
            add_window.focus()
        except Exception as e:
            print(f"Error opening Add Page Window: {e}")

    def setup_main_frame_structure(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=self.white_bg, corner_radius=0, border_width=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)

        # --- CONSTANT HEADER (ROW 0) ---
        header_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_container.grid(row=0, column=0, sticky="ew", padx=50, pady=(30, 10))

        logo_img = self.get_asset("Bits_College_Logo.png", size=(220, 60), fallback_color="#E0E0E0")
        self.logo_label = ctk.CTkLabel(header_container, text="", image=logo_img, cursor="hand2")
        self.logo_label.pack(side="left", anchor="w")
        self.logo_label.bind("<Button-1>", lambda event: self.show_dashboard())

        # Notification Area
        notif_frame = ctk.CTkFrame(header_container, fg_color="transparent")
        notif_frame.pack(side="right", anchor="e")

        # Bell Button
        self.bell_btn = ctk.CTkButton(notif_frame, text="", width=40, height=40,
                                      corner_radius=20, fg_color="#E8F5E9",
                                      image=self.get_asset("Notification_Bell.png", (20, 20), "green"),
                                      hover_color="#C8E6C9",
                                      command=self.toggle_notifications)  
        self.bell_btn.pack(side="right", padx=(10, 0))

        # Notification Label
        self.notif_label = ctk.CTkLabel(notif_frame,
                                        compound="left",
                                        padx=8,
                                        image=self.get_asset("Warning.png", (14, 14), "gray"),
                                        text="Checking System...",  
                                        anchor="e",
                                        text_color="gray",
                                        font=("Arial", 12, "bold"))
        self.notif_label.pack(side="right")

    def update_header_status(self):
        alerts = self.db.fetch_contract_alerts()
        pending_leaves = self.db.fetch_pending_leave_count()

        if alerts:
            count = len(alerts)
            text = f"System Alert: {count} Contracts Expiring Soon"
            color = "#D32F2F"  
        elif pending_leaves > 0:
            text = f"Action Needed: {pending_leaves} Leave Requests Pending"
            color = "#F57C00"  
        else:
            text = "System Status: Normal"
            color = "#2E7D32"  

        self.notif_label.configure(text=text, text_color=color)

    def toggle_notifications(self):
        if self.notification_popup is not None and self.notification_popup.winfo_exists():
            self.notification_popup.destroy()
            self.notification_popup = None
            return

        alerts = self.db.fetch_contract_alerts()
        pending_leaves = self.db.fetch_pending_leave_count()

        if not alerts and pending_leaves == 0:
            self.notification_popup = ctk.CTkFrame(self.main_frame, fg_color="#F1F8E9", corner_radius=10,
                                                    border_width=1, border_color="green")
            self.notification_popup.place(relx=0.96, rely=0.12, anchor="ne")
            ctk.CTkLabel(self.notification_popup, text="No new notifications", padx=20, pady=10).pack()
            return

        self.notification_popup = ctk.CTkFrame(self.main_frame, fg_color="white",
                                                corner_radius=10, border_width=1, border_color="#E0E0E0", width=300)
        self.notification_popup.place(relx=0.96, rely=0.12, anchor="ne")

        ctk.CTkLabel(self.notification_popup, text="Notifications", font=("Arial", 14, "bold"), text_color="#333").pack(
            anchor="w", padx=15, pady=(15, 5))

        if alerts:
            ctk.CTkLabel(self.notification_popup, text="⚠ Contracts Expiring", font=("Arial", 12, "bold"),
                         text_color="#D32F2F").pack(anchor="w", padx=15, pady=(5, 0))
            for name_dept, time_msg in alerts:
                row = ctk.CTkFrame(self.notification_popup, fg_color="#FEF2F2", corner_radius=5)
                row.pack(fill="x", padx=10, pady=2)
                ctk.CTkLabel(row, text=f"{name_dept}\n{time_msg}", font=("Arial", 11), text_color="#333",
                             justify="left").pack(anchor="w", padx=5, pady=5)

        if pending_leaves > 0:
            ctk.CTkLabel(self.notification_popup, text="✎ Leave Requests", font=("Arial", 12, "bold"),
                         text_color="#F57C00").pack(anchor="w", padx=15, pady=(10, 0))
            row = ctk.CTkFrame(self.notification_popup, fg_color="#FFF3E0", corner_radius=5)
            row.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(row, text=f"{pending_leaves} requests waiting for approval.", font=("Arial", 11),
                         text_color="#333").pack(anchor="w", padx=5, pady=5)

        ctk.CTkButton(self.notification_popup, text="Close", fg_color="#EEE", text_color="#333", hover_color="#DDD",
                      height=25, command=self.toggle_notifications).pack(pady=10)

    def clear_content(self):
        for widget in self.main_frame.winfo_children():
            grid_info = widget.grid_info()
            if 'row' in grid_info and int(grid_info['row']) > 0:
                widget.destroy()
        if self.notification_popup and self.notification_popup.winfo_exists():
            self.notification_popup.destroy()

    def show_dashboard(self):
        self.clear_content()
        self.update_header_status()
        Dashboard(self, self.main_frame)


if __name__ == "__main__":
    app = EmployeeDashboard()
    icon_path = "assets\\Bar_Bits_College_Logo.ico"
    if os.path.exists(icon_path):
        try:
            app.iconbitmap(icon_path)
        except Exception:
            pass
    app.mainloop()