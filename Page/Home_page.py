import customtkinter as ctk
from PIL import Image
import os


class EmployeeDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Window Setup
        self.title("Employee Information Desk")
        self.geometry("1000x700")

        # Configure Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 2. Define Colors
        self.sidebar_color = "#8CC63F"
        self.text_color_primary = "#1D3557"
        self.white_bg = "#FFFFFF"

        # 3. Create Sections
        self.setup_sidebar()
        self.setup_main_content()

    def get_asset(self, file_path, size=(20, 20), fallback_color="white"):
        if os.path.exists(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                img = Image.open(file_path)
                return ctk.CTkImage(light_image=img, dark_image=img, size=size)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")

        dummy_img = Image.new("RGB", size, fallback_color)
        return ctk.CTkImage(light_image=dummy_img, size=size)

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=self.sidebar_color)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # 'HR' Header
        hr_label = ctk.CTkLabel(self.sidebar, text="HR", text_color="white",
                                font=("Arial", 18, "bold"), anchor="w")
        hr_label.grid(row=0, column=0, padx=20, pady=(30, 20), sticky="w")

        # Sidebar Buttons Data (Update these paths to your actual PNG files)
        menu_items = [
            ("Add Employee", "C:\\Users\Debian\Documents\HRA\BITS-EMS\\assets\Add_user.png"),
            ("Edit Employee", "C:\\Users\Debian\Documents\HRA\BITS-EMS\\assets\Edit_user.png"),
            ("Delete Employee", "C:\\Users\Debian\Documents\HRA\BITS-EMS\\assets\Remove_user.png"),
            ("Search Employee", "C:\\Users\Debian\Documents\HRA\BITS-EMS\\assets\View_employee.png"),
            ("View Employee", "C:\\Users\Debian\Documents\HRA\BITS-EMS\\assets\Search_employe.png"),
            ("Leave Request Form", "C:\\Users\Debian\Documents\HRA\BITS-EMS\\assets\Leave_request.png")
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
                font=("Arial", 13),
                height=45
            )
            # row i+1 because HR label is at row 0
            btn.grid(row=i + 1, column=0, padx=10, pady=2, sticky="ew")

    def setup_main_content(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=self.white_bg, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # -- Notification Area --
        notif_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        notif_frame.grid(row=0, column=0, padx=30, pady=20, sticky="e")

        notif_text = ctk.CTkLabel(notif_frame,
            compound="left",
            padx=8,
            image=self.get_asset("C:\\Users\Debian\Documents\HRA\BITS-EMS\\assets\Warning.png", (11, 11), "gray"),
            text="Your leave balance is finished.",
            anchor="w",
            text_color="gray",
            font=("Arial", 11))

        notif_text.pack(side="left", padx=10)

        bell_btn = ctk.CTkButton(notif_frame, text="", width=35, height=35,
                                 corner_radius=17, fg_color="#C8E6C9",
                                 image=self.get_asset("C:\\Users\Debian\Documents\HRA\BITS-EMS\\assets\\Notification_Bell.png", (18, 18), "green"),
                                 hover=False)
        bell_btn.pack(side="left")

        # -- Main Title --
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="EMPLOYEE INFORMATION DESK",
            font=("Arial", 42, "bold"),
            text_color=self.text_color_primary,
            justify="left"
        )
        title_label.grid(row=1, column=0, padx=60, pady=(60, 0), sticky="nw")

        # -- Bottom Hero Image --
        hero_img = self.get_asset("C:\\Users\Debian\Documents\HRA\BITS-EMS\\assets\Bits_College_Logo.png", size=(500, 200), fallback_color="#E0E0E0")
        image_label = ctk.CTkLabel(self.main_frame, text="", image=hero_img)
        image_label.grid(row=2, column=0, padx=40, pady=100, sticky="s")


if __name__ == "__main__":
    if not os.path.exists("assets"):
        os.makedirs("assets")

    app = EmployeeDashboard()
    app.mainloop()