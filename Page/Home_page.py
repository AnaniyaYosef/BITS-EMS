import customtkinter as ctk
from PIL import Image
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import io


class EmployeeDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Window Setup
        self.title("Employee Information Desk - SVG Version")
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

    def load_svg(self, file_path, size=(20, 20)):
        """Converts SVG to a PIL Image so CustomTkinter can use it."""
        try:
            drawing = svg2rlg(file_path)
            # Scaling the drawing to fit the requested size
            scaling_factor = size[0] / drawing.width
            drawing.width *= scaling_factor
            drawing.height *= scaling_factor
            drawing.scale(scaling_factor, scaling_factor)

            # Render SVG to PNG in memory
            png_data = renderPM.drawToString(drawing, fmt="PNG")
            img = Image.open(io.BytesIO(png_data))
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except Exception as e:
            print(f"Error processing SVG {file_path}: {e}")
            return self.get_fallback_image(size)

    def get_fallback_image(self, size):
        """Creates a simple square if the SVG fails to load."""
        dummy_img = Image.new("RGBA", size, (255, 255, 255, 0))  # Transparent
        return ctk.CTkImage(light_image=dummy_img, size=size)

    def get_asset(self, file_path, size=(20, 20)):
        """Checks if file is SVG or PNG and routes to the correct loader."""
        if not os.path.exists(file_path):
            return self.get_fallback_image(size)

        if file_path.lower().endswith(".svg"):
            return self.load_svg(file_path, size)
        else:
            img = Image.open(file_path)
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=self.sidebar_color)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        hr_label = ctk.CTkLabel(self.sidebar, text="HR", text_color="white",
                                font=("Arial", 18, "bold"), anchor="w")
        hr_label.grid(row=0, column=0, padx=20, pady=(30, 20), sticky="w")

        # Note: You can now use .svg paths here!
        menu_items = [
            ("Add Employee", "assets/add-employe.svg"),
            ("Edit Employee", "assets/edit.svg"),
            ("Delete Employee", "assets/delete.svg"),
            ("Search Employee", "assets/search.svg"),
            ("View Employee", "assets/view.svg"),
            ("Leave Request Form", "assets/leave.svg")
        ]

        for i, (text, path) in enumerate(menu_items):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                image=self.get_asset(path),
                fg_color="transparent",
                text_color="white",
                hover_color="#76A835",
                anchor="w",
                font=("Arial", 13),
                height=45
            )
            btn.grid(row=i + 1, column=0, padx=10, pady=2, sticky="ew")

    def setup_main_content(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=self.white_bg, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # -- Notification Area --
        notif_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        notif_frame.grid(row=0, column=0, padx=30, pady=20, sticky="e")

        notif_text = ctk.CTkLabel(notif_frame, text="▲ Your leave balance is finished.",
                                  text_color="gray", font=("Arial", 11))
        notif_text.pack(side="left", padx=10)

        # Notification Bell (SVG)
        bell_btn = ctk.CTkButton(notif_frame, text="", width=35, height=35,
                                 corner_radius=17, fg_color="#C8E6C9",
                                 image=self.get_asset("assets/bell.svg", (18, 18)),
                                 hover=False)
        bell_btn.pack(side="left")

        # -- Main Title --
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="EMPLOYEE INFORMATION\nDESK",
            font=("Arial", 42, "bold"),
            text_color=self.text_color_primary,
            justify="left"
        )
        title_label.grid(row=1, column=0, padx=60, pady=(60, 0), sticky="nw")

        # -- Bottom Hero Image (Usually PNG/JPG as it's a photo) --
        hero_img = self.get_asset("assets/team.png", size=(700, 300))
        image_label = ctk.CTkLabel(self.main_frame, text="", image=hero_img)
        image_label.grid(row=2, column=0, padx=40, pady=40, sticky="s")


if __name__ == "__main__":
    if not os.path.exists("assets"):
        os.makedirs("assets")

    app = EmployeeDashboard()
    app.mainloop()