
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from DB_Service.Login_db import LoginDB

class LoginPage(ctk.CTkFrame):
 
    def __init__(self, master):
        super().__init__(master)
        
        self.master = master
        self.login_db = LoginDB()
        
        # Set theme and appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_container = ctk.CTkFrame(
            self, 
            corner_radius=0,
            fg_color=("white", "#1a1a1a")
        )
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Two-panel layout
        self.two_panel_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.two_panel_frame.grid(row=0, column=0, sticky="nsew")
        self.two_panel_frame.grid_columnconfigure(0, weight=1)
        self.two_panel_frame.grid_columnconfigure(1, weight=1)
        self.two_panel_frame.grid_rowconfigure(0, weight=1)
        
        # Left Panel - Branding/Image
        self.left_panel = ctk.CTkFrame(
            self.two_panel_frame, 
            fg_color="#7DC243",
            corner_radius=0
        )
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        
        # Branding content in left panel
        self.brand_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.brand_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        try:
            logo_path = os.path.join("assets", "logo.png")
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                # Resize logo for better display
                logo_img = logo_img.resize((200, 200), Image.Resampling.LANCZOS)
                logo_image = ctk.CTkImage(logo_img, size=(200, 200))
                logo_label = ctk.CTkLabel(self.brand_frame, image=logo_image, text="")
                logo_label.pack(pady=(0, 20))
        except Exception as e:
            print(f"Logo loading error: {e}")
        
        # Brand name with styling
        brand_label = ctk.CTkLabel(
            self.brand_frame,
            text="BITS-EMS",
            font=ctk.CTkFont(family="Segoe UI", size=36, weight="bold"),
            text_color="white"
        )
        brand_label.pack(pady=(0, 10))
        
        # Tagline
        tagline_label = ctk.CTkLabel(
            self.brand_frame,
            text="Employee Management System",
            font=ctk.CTkFont(family="Segoe UI", size=16),
            text_color="#f3f3f3"
        )
        tagline_label.pack()
        
        # Right Panel - Login Form
        self.right_panel = ctk.CTkFrame(
            self.two_panel_frame,
            fg_color="transparent"
        )
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=80)

        self.form_container = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.form_container.place(relx=0.5, rely=0.5, anchor="center")

        welcome_header = ctk.CTkLabel(
            self.form_container,
            text="Welcome Back",
            font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"),
            text_color=("black", "white")
        )
        welcome_header.pack(pady=(0, 10))
        
        welcome_subtitle = ctk.CTkLabel(
            self.form_container,
            text="Sign in to your account",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color="#7f8c8d"
        )
        welcome_subtitle.pack(pady=(0, 40))
        
        # Username field with icon
        self.username_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.username_frame.pack(fill="x", pady=(0, 20))
        
        self.username_label = ctk.CTkLabel(
            self.username_frame,
            text="Username",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=("black", "white")
        )
        self.username_label.pack(anchor="w", pady=(0, 8))
        
        self.username_entry = ctk.CTkEntry(
            self.username_frame,
            placeholder_text="Enter your username",
            width=350,
            height=48,
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=14),
            border_color="#2c3e50"
        )
        self.username_entry.pack(fill="x")
        
        # Password field with icon
        self.password_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.password_frame.pack(fill="x", pady=(0, 30))
        
        self.password_label = ctk.CTkLabel(
            self.password_frame,
            text="Password",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=("black", "white")
        )
        self.password_label.pack(anchor="w", pady=(0, 8))
        
        self.password_entry = ctk.CTkEntry(
            self.password_frame,
            placeholder_text="Enter your password",
            width=350,
            height=48,
            corner_radius=8,
            show="•",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            border_color="#2c3e50"
        )
        self.password_entry.pack(fill="x")
        
        # Remember me and Forgot password
        self.remember_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.remember_frame.pack(fill="x", pady=(0, 30))
        
        self.remember_var = ctk.BooleanVar(value=False)
        self.remember_checkbox = ctk.CTkCheckBox(
            self.remember_frame,
            text="Remember me",
            variable=self.remember_var,
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.remember_checkbox.pack(side="left")
        
        self.forgot_button = ctk.CTkButton(
            self.remember_frame,
            text="Forgot password?",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color="transparent",
            hover_color="#ecf0f1",
            text_color="#2c3e50",
            command=self.forgot_password,
            width=0
        )
        self.forgot_button.pack(side="right")

        self.login_button = ctk.CTkButton(
            self.form_container,
            text="Sign In",
            command=self.validate_login,
            width=350,
            height=50,
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            fg_color="#7DC243",
            hover_color="#81C946",
            text_color="white",
            border_width=0
        )
        self.login_button.pack(pady=(0, 20))
        
        # Status message with icon
        self.status_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.status_frame.pack()
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="red"
        )
        self.status_label.pack()
        
        # Footer
        footer_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        footer_frame.pack(side="bottom", pady=20)
        
        footer_label = ctk.CTkLabel(
            footer_frame,
            text="© 2024 BITS-EMS | Employee Management System",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color="#95a5a6"
        )
        footer_label.pack()
        
        # Bind Enter key to login
        self.username_entry.bind("<Return>", lambda event: self.validate_login())
        self.password_entry.bind("<Return>", lambda event: self.validate_login())
        
        # Set focus to username field
        self.after(100, self.username_entry.focus)
    
    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Clear previous status
        self.status_label.configure(text="")
        
        # Basic validation
        if not username:
            self.show_error("Username is required")
            self.username_entry.focus()
            return
        
        if not password:
            self.show_error("Password is required")
            self.password_entry.focus()
            return
        
        # Show loading state
        original_text = self.login_button.cget("text")
        self.login_button.configure(text="Authenticating...", state="disabled")
        self.update()
        
        try:
            # Authenticate with database
            user = self.login_db.authenticate_user(username, password)
            
            if user:
                self.show_success(f"Welcome, {user.get('full_name', user['username'])}!")
                print(f"Login successful: {user['username']}")
                
                # ================================================
                # REDIRECT BUTTON FOR DEVELOPERS AFTER SUCCESSFUL LOGIN
                # ================================================
                # This section provides a clear redirect mechanism
                # to implement the actual navigation to the main application or dashboard
                self.create_redirect_button(user)
                
            else:
                self.show_error("Invalid username or password")
                self.password_entry.delete(0, 'end')
                self.password_entry.focus()
                
        except Exception as e:
            self.show_error(f"Connection error: {str(e)}")
        finally:
            # Restore button state
            self.login_button.configure(text=original_text, state="normal")
    
    def create_redirect_button(self, user):
        if hasattr(self, 'redirect_button') and self.redirect_button.winfo_exists():
            return
        self.redirect_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.redirect_frame.pack(pady=(20, 0))

        self.redirect_button = ctk.CTkButton(
            self.redirect_frame,
            text="Go to Dashboard",
            command=lambda: self.navigate_to_dashboard(user),
            width=350,
            height=50,
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            fg_color="#2c3e50",
            hover_color="#34495e",
            text_color="white"
        )
        self.redirect_button.pack()

        self.redirect_label = ctk.CTkLabel(
            self.redirect_frame,
            text="(Developers: Implement actual dashboard navigation here)",
            font=ctk.CTkFont(family="Segoe UI", size=10, slant="italic"),
            text_color="#95a5a6"
        )
        self.redirect_label.pack(pady=(10, 0))
        
        print("Redirect button created. Implement navigate_to_dashboard() function for actual navigation.")
    
    def navigate_to_dashboard(self, user):
        """
        Placeholder function for dashboard navigation
        
        This function should be implemented by other developers to handle the actual
        transition from the login page to the main application or dashboard.
        
        Suggestions for implementation:
            1. Hide or remove the login page
            2. Create and display the dashboard frame/window
            3. Pass user information to the dashboard
            4. Initialize dashboard components
            
        Args:
            user: Dictionary containing user information (username, full_name, role, etc.)
        """
        
        # ================================================
        # DEVELOPER TODO: Implement actual navigation logic
        # ================================================
        
        # Current placeholder behavior (will be replaced by actual implementation)
        print(f"Navigating to dashboard for user: {user['username']}")
        print("ROLE:", user.get('role', 'user'))
        print("USER DATA:", user)
        
        # Example implementation (uncomment and customize):
        #
        # from Page.Home_page import HomePage
        # 
        # # Hide login page
        # self.pack_forget()
        # 
        # # Create and show dashboard
        # self.dashboard = HomePage(self.master, user)
        # self.dashboard.pack(expand=True, fill="both")
        # 
        # # Optional: Update window title
        # self.master.title(f"BITS-EMS - Dashboard ({user['username']})")
        
        # Show temporary alert for demonstration
        self.status_label.configure(
            text="✓ Redirect button clicked! Implement actual navigation in navigate_to_dashboard()",
            text_color="#3498db"
        )
    
    def show_error(self, message):
        """Display error message with red styling"""
        self.status_label.configure(
            text=f"✗ {message}",
            text_color="#e74c3c"
        )
    
    def show_success(self, message):
        """Display success message with green styling"""
        self.status_label.configure(
            text=f"✓ {message}",
            text_color="#27ae60"
        )
    
    def forgot_password(self):
        """Handle forgot password functionality"""

        print("Forgot password clicked")

    
    def on_closing(self):
        """Clean up resources when closing"""
        if self.login_db:
            self.login_db.close()
    
    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "dark" if current_mode == "light" else "light"
        ctk.set_appearance_mode(new_mode)