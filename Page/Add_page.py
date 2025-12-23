import customtkinter as ctk
from tkinter import filedialog
from tkcalendar import DateEntry
from PIL import Image
import datetime


app = ctk.CTk()
app.title("Add New Employee")
app.geometry("1000x600")

EmpFrame = ctk.CTkFrame(app)
EmpFrame.pack(Expand=True)





app.mainloop()