import customtkinter as ctk
from PIL import Image
import os

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

        # 3. Create Sections
        self.setup_sidebar()
        self.setup_main_content()

    def get_asset(self, file_path, size=(20, 20), fallback_color="gray"):
        clean_path = os.path.normpath(file_path)

        if os.path.exists(clean_path) and clean_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                img = Image.open(clean_path)
                return ctk.CTkImage(light_image=img, dark_image=img, size=size)
            except Exception as e:
                print(f"Error loading {clean_path}: {e}")

        dummy_img = Image.new("RGB", size, fallback_color)
        return ctk.CTkImage(light_image=dummy_img, size=size)

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0,
                                    fg_color=self.sidebar_color, border_width=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # sidebar grid to push Logout to bottom
        self.sidebar.grid_rowconfigure(7, weight=1)

        # 'HR' Header
        hr_label = ctk.CTkLabel(self.sidebar, text="HR", text_color="white",
                                font=("Arial", 20, "bold"), anchor="w")
        hr_label.grid(row=0, column=0, padx=20, pady=(30, 20), sticky="w")

        # Sidebar Buttons Data - KEEPING YOUR EXACT PATHS
        menu_items = [
            ("Add Employee", "C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets\\Add_user.png"),
            ("Edit Employee", "C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets\\Edit_user.png"),
            ("Delete Employee", "C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets\\Remove_user.png"),
            ("Search Employee", "C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets\\View_employee.png"),
            ("View Employee", "C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets\\Search_employe.png"),
            ("Leave Request Form", "C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets\\Leave_request.png")
        ]

        for i, (text, path) in enumerate(menu_items):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                image=self.get_asset(path),
                fg_color="transparent",
                text_color="white",
                hover_color="#C8D7E2",
                anchor="w",
                font=("Arial", 14),
                height=45
            )
            btn.grid(row=i + 1, column=0, padx=10, pady=2, sticky="ew")

        # --- LOGOUT BUTTON ---
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

    def setup_main_content(self):

        self.main_frame = ctk.CTkFrame(self, fg_color=self.white_bg, corner_radius=0, border_width=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

        # grid for main content structure
        self.main_frame.grid_columnconfigure(0, weight=1)
        # Row 0: Header Container (Logo + Alerts)
        # Row 1: Main Title
        # Row 2: Top Stats
        # Row 3: Middle Section
        self.main_frame.grid_rowconfigure(3, weight=1)


        header_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_container.grid(row=0, column=0, sticky="ew", padx=50, pady=(30, 10))

        # Company Logo

        logo_img = self.get_asset(
            "C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets\\Bits_College_Logo.png",
            size=(220, 60),  # Adjusted size for header look
            fallback_color="#E0E0E0"
        )
        logo_label = ctk.CTkLabel(header_container, text="", image=logo_img)
        logo_label.pack(side="left", anchor="w")

        # Notification Area
        notif_frame = ctk.CTkFrame(header_container, fg_color="transparent")
        notif_frame.pack(side="right", anchor="e")

        bell_btn = ctk.CTkButton(notif_frame, text="", width=40, height=40,
                                 corner_radius=20, fg_color="#E8F5E9",
                                 image=self.get_asset(
                                     "C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets\\Notification_Bell.png",
                                     (20, 20), "green"),
                                 hover_color="#C8E6C9")
        bell_btn.pack(side="right", padx=(10, 0))

        notif_text = ctk.CTkLabel(notif_frame,
                                  compound="left",
                                  padx=8,
                                  image=self.get_asset(
                                      "C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets\\Warning.png", (14, 14),
                                      "gray"),
                                  text="System Alert: 2 Contracts Expiring Soon",
                                  anchor="e",
                                  text_color="#D32F2F",
                                  font=("Arial", 12, "bold"))
        notif_text.pack(side="right")


        # Main Title
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="EMPLOYEE INFORMATION DESK",
            font=("Arial", 32, "bold"),
            text_color=self.text_color_primary,
            justify="left"
        )
        title_label.grid(row=1, column=0, padx=50, pady=(10, 25), sticky="w")

        # Top Statistics Row
        self.setup_top_stats(row=2)

        # Middle Section (Department & Alerts)
        middle_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        middle_container.grid(row=3, column=0, padx=50, pady=10, sticky="nsew")
        middle_container.grid_columnconfigure(0, weight=2)
        middle_container.grid_columnconfigure(1, weight=1)

        self.setup_dept_distribution(middle_container, col=0)
        self.setup_contract_alerts(middle_container, col=1)

    def setup_top_stats(self, row):
        stats_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        stats_container.grid(row=row, column=0, padx=50, pady=10, sticky="ew")
        stats_container.grid_columnconfigure((0, 1, 2, 3), weight=1)

        stats_data = [
            ("Full Time", "124", "#2E7D32"),
            ("Contract", "12", "#F9A825"),
            ("Interns", "4", "#0277BD"),
            ("On Leave", "8", "#C62828")
        ]

        for i, (label, value, color) in enumerate(stats_data):
            self.create_stat_card(stats_container, i, label, value, color)

    def create_stat_card(self, parent, col_idx, title, value, border_color):
        card = ctk.CTkFrame(parent, fg_color=self.card_bg_color, corner_radius=8, border_width=1,
                            border_color=self.border_color)
        card.grid(row=0, column=col_idx, padx=8, pady=0, sticky="ew")

        strip = ctk.CTkFrame(card, width=5, fg_color=border_color, corner_radius=0)
        strip.pack(side="left", fill="y", padx=(0, 10))

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(side="left", padx=5, pady=12)

        val_label = ctk.CTkLabel(content, text=value, font=("Arial", 24, "bold"), text_color=self.text_color_primary)
        val_label.pack(anchor="w")

        title_label = ctk.CTkLabel(content, text=title, font=("Arial", 12), text_color="gray")
        title_label.pack(anchor="w")

    def setup_dept_distribution(self, parent, col):
        frame = ctk.CTkFrame(parent, fg_color=self.card_bg_color, corner_radius=10, border_width=1,
                             border_color=self.border_color)
        frame.grid(row=0, column=col, padx=(0, 15), sticky="nsew")

        header = ctk.CTkLabel(frame, text="Department Distribution", font=("Arial", 14, "bold"),
                              text_color=self.text_color_primary)
        header.pack(anchor="w", padx=15, pady=(15, 10))

        depts = [
            ("IT Department", "45"),
            ("HR Department", "12"),
            ("Finance", "18"),
            ("Marketing", "22")
        ]

        for name, count in depts:
            row = ctk.CTkFrame(frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=6)

            lbl_frame = ctk.CTkFrame(row, fg_color="transparent")
            lbl_frame.pack(fill="x")
            ctk.CTkLabel(lbl_frame, text=name, font=("Arial", 12), text_color="#333").pack(side="left")
            ctk.CTkLabel(lbl_frame, text=count, font=("Arial", 12, "bold"), text_color=self.text_color_primary).pack(
                side="right")



    def setup_contract_alerts(self, parent, col):
        frame = ctk.CTkFrame(parent, fg_color=self.alert_bg_color, corner_radius=10, border_width=1,
                             border_color="#FECACA")
        frame.grid(row=0, column=col, padx=0, sticky="nsew")

        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))

        ctk.CTkLabel(header_frame, text="⚠ Contract Expiry Alerts", font=("Arial", 14, "bold"),
                     text_color="#B91C1C").pack(side="left")

        alerts = [
            ("John Doe (IT)", "Expires in: 2 Days"),
            ("Jane Smith (HR)", "Expires in: 1 Week")
        ]

        for name, time in alerts:
            item = ctk.CTkFrame(frame, fg_color="white", corner_radius=6)
            item.pack(fill="x", padx=15, pady=5)

            ctk.CTkLabel(item, text=name, font=("Arial", 12, "bold"), text_color="#333").pack(anchor="w", padx=10,
                                                                                              pady=(8, 0))
            ctk.CTkLabel(item, text=time, font=("Arial", 11), text_color="#DC2626").pack(anchor="w", padx=10,
                                                                                         pady=(0, 8))

        ctk.CTkButton(frame, text="View All", fg_color="transparent", text_color="#B91C1C",
                      hover_color="#FEE2E2", font=("Arial", 11, "bold"), height=25).pack(pady=10)


if __name__ == "__main__":
    app = EmployeeDashboard()
    icon_path = "C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets\\Bar_Bits_College_Logo.ico"
    if os.path.exists(icon_path):
        try:
            app.iconbitmap(icon_path)
            pass
        except Exception:
            pass

    app.mainloop()