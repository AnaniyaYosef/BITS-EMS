import customtkinter as ctk
from Page.Login_page import LoginPage
from Page.main_page import EmployeeDashboard


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BITS-EMS - Login")
        self.geometry("1200x800")
        self.minsize(1000, 650)

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        # Login page only
        self.login_page = LoginPage(
            master=self,
            on_login_success=self.on_login_success
        )
        self.login_page.pack(expand=True, fill="both")

    def on_login_success(self):
        """
        Called when login is confirmed.
        No user data, no transfer.
        """
        # Close login window safely
        self.after(0, self._open_main_page)

    def _open_main_page(self):
        # Destroy login window completely
        self.destroy()

        # Open main page as its own window
        main_page = EmployeeDashboard()
        main_page.mainloop()


if __name__ == "__main__":
    app = App()
    app.mainloop()
