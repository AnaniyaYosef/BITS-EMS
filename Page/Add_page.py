import customtkinter as ctk
from tkinter import filedialog
from tkcalendar import DateEntry
from PIL import Image
import datetime

ctk.set_appearance_mode("Light")
app = ctk.CTk()
app.title("Add New Employee")
app.geometry("1000x600")

main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

top_frame = ctk.CTkFrame(main_frame)
top_frame.pack(fill="both", expand=True)

left_frame = ctk.CTkFrame(top_frame)
left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

right_frame = ctk.CTkFrame(top_frame)
right_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

bottom_frame = ctk.CTkFrame(main_frame, height=80)
bottom_frame.pack(fill="x", pady=5)


app.mainloop()