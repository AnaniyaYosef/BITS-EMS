"""
Login page for BITS-EMS application
"""
import customtkinter as ctk
from PIL import Image
from DB_Service.Login_db import LoginDB
import os

class LoginPage(ctk.CTkFrame):
    """Login page with username and password fields"""
    
    def __init__(self, master):
        super().__init__(master)
        
        self.master = master
        self.login_db = LoginDB()
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Create login container
        self.login_container = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.login_container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.login_container.grid_columnconfigure(0, weight=1)
        self.login_container.grid_rowconfigure(0, weight=1)
        
        # Create content frame
        self.content_frame = ctk.CTkFrame(self.login_container)
        self.content_frame.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Add logo/image at the top
        try:
            logo_path = os.path.join("assets", "logo.png")
            if os.path.exists(logo_path):
                logo_image = ctk.CTkImage(Image.open(logo_path), size=(150, 150))
                logo_label = ctk.CTkLabel(self.content_frame, image=logo_image, text="")
                logo_label.grid(row=0, column=0, pady=(0, 20))
            else:
                title_label = ctk.CTkLabel(self.content_frame, text="BITS-EMS", 
                                         font=ctk.CTkFont(size=32, weight="bold"))
                title_label.grid(row=0, column=0, pady=(0, 20))
        except Exception as e:
            print(f"Error loading logo: {e}")
            title_label = ctk.CTkLabel(self.content_frame, text="BITS-EMS", 
                                     font=ctk.CTkFont(size=32, weight="bold"))
            title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Add welcome message
        welcome_label = ctk.CTkLabel(self.content_frame, text="Welcome to Employee Management System",
                                     font=ctk.CTkFont(size=16))
        welcome_label.grid(row=1, column=0, pady=(0, 30))
        
        # Username field
        self.username_label = ctk.CTkLabel(self.content_frame, text="Username:",
                                          font=ctk.CTkFont(weight="bold"))
        self.username_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Enter your username",
                                          width=300, height=40)
        self.username_entry.grid(row=3, column=0, pady=(0, 20))
        
        # Password field
        self.password_label = ctk.CTkLabel(self.content_frame, text="Password:",
                                          font=ctk.CTkFont(weight="bold"))
        self.password_label.grid(row=4, column=0, sticky="w", pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Enter your password",
                                          width=300, height=40, show="*")
        self.password_entry.grid(row=5, column=0, pady=(0, 30))
        
        # Login button
        self.login_button = ctk.CTkButton(self.content_frame, text="Login",
                                         command=self.validate_login, width=300, height=45,
                                         font=ctk.CTkFont(weight="bold"))
        self.login_button.grid(row=6, column=0, pady=(0, 15))
        
        # Status message
        self.status_label = ctk.CTkLabel(self.content_frame, text="", text_color="red")
        self.status_label.grid(row=7, column=0)
        
        # Add footer
        footer_label = ctk.CTkLabel(self.content_frame, text="© 2024 BITS-EMS | Employee Management System",
                                    font=ctk.CTkFont(size=10))
        footer_label.grid(row=8, column=0, pady=(20, 0))
    
    def validate_login(self):
        """Validate login credentials"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Clear previous status
        self.status_label.configure(text="", text_color="red")
        
        # Basic validation
        if not username:
            self.status_label.configure(text="Username is required", text_color="red")
            return
        
        if not password:
            self.status_label.configure(text="Password is required", text_color="red")
            return
        
        # Authenticate with database
        user = self.login_db.authenticate_user(username, password)
        
        if user:
            self.status_label.configure(text="Login successful!", text_color="green")
            print(f"Login successful for user: {user['username']}")
            # Here you would typically navigate to the main dashboard
            # For now, we'll just show a success message
        else:
            self.status_label.configure(text="Invalid username or password", text_color="red")
    
    def on_closing(self):
        """Clean up resources when closing"""
        self.login_db.close()
