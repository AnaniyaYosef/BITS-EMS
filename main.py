"""
Main application entry point for BITS-EMS
"""
import customtkinter as ctk
from Page.Login_page import LoginPage

class App(ctk.CTk):
    """Main application window"""
    def __init__(self):
        super().__init__()
        
        self.title("BITS-EMS - Employee Management System")
        self.geometry("1200x800")
        self.resizable(True, True)
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode("system")  # Modes: system, light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue, dark-blue, green
        
        # Create login page
        self.login_page = LoginPage(self)
        self.login_page.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = App()
    app.mainloop()
