import customtkinter as ctk
from PIL import Image
import os

# Import the Dashboard class
from Dashboard import Dashboard


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
        self.setup_main_frame_structure()

        # 4. Load Default View (Dashboard)
        self.show_dashboard()

    def get_asset(self, file_path, size=(20, 20), fallback_color="gray"):
        # Build a list of candidate paths to try (given path, project assets, workspace assets, old HRA path)
        candidates = []
        candidates.append(file_path)

        # Try relative to this file: ../assets/<file_path>
        try:
            this_dir = os.path.dirname(__file__)
            rel_assets = os.path.abspath(os.path.join(this_dir, '..', 'assets'))
            candidates.append(os.path.join(rel_assets, os.path.basename(file_path)))
        except Exception:
            pass

        # Try workspace-level assets (two levels up if project layout differs)
        try:
            workspace_assets = os.path.abspath(os.path.join(this_dir, '..', '..', 'assets'))
            candidates.append(os.path.join(workspace_assets, os.path.basename(file_path)))
        except Exception:
            pass

        # Legacy absolute HRA path fallback
        candidates.append(os.path.join("C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets", os.path.basename(file_path)))

        # Try each candidate until one loads
        for p in candidates:
            if p and os.path.exists(p):
                try:
                    img = Image.open(p)
                    return ctk.CTkImage(light_image=img, dark_image=img, size=size)
                except Exception as e:
                    print(f"Error loading {p}: {e}")

        # If none found or failed to load, log attempted locations and return dummy image
        print(f"Asset not found, tried: {candidates}")
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

        # Sidebar Buttons Data
        menu_items = [
            ("Add Employee", "C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets\\Add_user.png"),
            ("Edit Employee", "C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets\\Edit_user.png"),
            ("Delete Employee", "C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets\\Remove_user.png"),
            ("Search Employee", "C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets\\View_employee.png"),
            ("View Employee", "C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets\\Search_employe.png"),
            ("Leave Request Form", "C:\\Users\\Debian\\Documents\\HRA\\BITS-EMS\\assets\\Leave_request.png")
        ]

        for i, (text, path) in enumerate(menu_items):
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

    def setup_main_frame_structure(self):
        # This creates the white background frame on the right
        self.main_frame = ctk.CTkFrame(self, fg_color=self.white_bg, corner_radius=0, border_width=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

        # Grid configuration for the content inside
        self.main_frame.grid_columnconfigure(0, weight=1)
        # Row 0: Header
        # Row 1-3: Page Content
        self.main_frame.grid_rowconfigure(3, weight=1)

        # --- CONSTANT HEADER (ROW 0) ---
        header_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_container.grid(row=0, column=0, sticky="ew", padx=50, pady=(30, 10))

        # Company Logo
        logo_img = self.get_asset(
            "Bits_College_Logo.png",
            size=(220, 60),
            fallback_color="#E0E0E0"
        )

        self.logo_label = ctk.CTkLabel(header_container, text="", image=logo_img, cursor="hand2")
        self.logo_label.pack(side="left", anchor="w")

        # BIND CLICK EVENT TO LOGO -> GO TO DASHBOARD
        self.logo_label.bind("<Button-1>", lambda event: self.show_dashboard())

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

    def clear_content(self):
        """
        Clears all widgets from the main_frame EXCEPT the Header (Row 0).
        """
        for widget in self.main_frame.winfo_children():
            # Get grid info to check the row
            grid_info = widget.grid_info()
            # If the widget is in a row greater than 0, destroy it.
            # (Row 0 is the Header, we want to keep that).
            if 'row' in grid_info and int(grid_info['row']) > 0:
                widget.destroy()

    def show_dashboard(self):
        """Displays the Dashboard content."""
        self.clear_content()
        Dashboard(self, self.main_frame)


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