import customtkinter as ctk
from tkinter import filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import datetime
from utils import EmployeeFile
from DB_Service import Add_DB

ctk.set_appearance_mode("Light")
app = ctk.CTk()
app.title("Add New Employee")
app.geometry("1000x600")

#-----Functions-----
def upload_file(label):
    file_path = filedialog.askopenfilename()
    if file_path:
        label.configure(text=file_path.split("/")[-1])

def ClearFiled():
    full_name_entry.delete(0, "end")
    contact_entry.delete(0, "end")
    email_entry.delete(0, "end")
    emergency_contact_entry.delete(0, "end")


    dob_entry.set_date(datetime.date.today())
    hire_date_entry.set_date(datetime.date.today())


    department_option.set("IT")
    gender_option.set("Male")


def submit():
    EmpId = ""
    full_name = full_name_entry.get()
    dob = dob_entry.get()
    contact = contact_entry.get()
    email = email_entry.get()
    department = department_option.get()


    gender = gender_option.get()
    emergency_contact = emergency_contact_entry.get()
    hire_date = hire_date_entry.get()
    
    file = {
        "image": getattr(image_label, "file_path", None),
        "cv": getattr(cv_label, "file_path", None),
        "certificate": getattr(cert_label, "file_path", None),
        "id": getattr(id_label, "file_path", None),
        "contract": getattr(contract_label, "file_path", None),
    }
    save_file = EmployeeFile.SaveEmpFile(EmployeeId=EmpId,files=file)



    ClearFiled()

#-----Frames-------
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

ctk.CTkLabel(main_frame, text="New Employee From").pack(anchor="n", padx=20)

top_frame = ctk.CTkFrame(main_frame)
top_frame.pack(fill="both", expand=True)

left_frame = ctk.CTkScrollableFrame(top_frame)
left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

right_frame = ctk.CTkScrollableFrame(top_frame)
right_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

bottom_frame = ctk.CTkFrame(main_frame, height=80)
bottom_frame.pack(fill="x", pady=5)

#----left Frame Content------

# Full Name
ctk.CTkLabel(left_frame, text="Full Name").pack(anchor="w", padx=20)
full_name_entry = ctk.CTkEntry(left_frame)
full_name_entry.pack(fill="x", padx=20, pady=5)

# Date of Birth
ctk.CTkLabel(left_frame, text="Date of Birth",font=("Arial", 14, "bold")).pack(pady=(15, 5))
dob_entry = DateEntry(left_frame,width=22,font=("Arial", 12),background="darkblue",foreground="white",borderwidth=2,
date_pattern="yyyy-mm-dd")
dob_entry.pack(padx=20, pady=5)

# Contact Number
ctk.CTkLabel(left_frame, text="Contact Number").pack(anchor="w", padx=20)
contact_entry = ctk.CTkEntry(left_frame)
contact_entry.pack(fill="x", padx=20, pady=5)


# Email
ctk.CTkLabel(left_frame, text="Email").pack(anchor="w", padx=20)
email_entry = ctk.CTkEntry(left_frame)
email_entry.pack(fill="x", padx=20, pady=5)


# Department Dropdown
ctk.CTkLabel(left_frame, text="Department").pack(anchor="w", padx=20)
department_option = ctk.CTkOptionMenu(
left_frame,
values=["IT", "HR", "Finance", "Marketing", "Operations"])
department_option.pack(fill="x", padx=20, pady=5)

#----Right Frame Content------

# Gender
ctk.CTkLabel(right_frame, text="Gender").pack(anchor="w", padx=20)
gender_option = ctk.CTkOptionMenu(right_frame,values=["Male", "Female"])
gender_option.pack(fill="x", padx=20, pady=5)


# Emergency Contact Phone
ctk.CTkLabel(right_frame, text="Emergency Contact Number").pack(anchor="w", padx=20)
emergency_contact_entry = ctk.CTkEntry(right_frame)
emergency_contact_entry.pack(fill="x", padx=20, pady=5)


# Hiring Date
ctk.CTkLabel(right_frame,text="Hiring Date",font=("Arial", 14, "bold")).pack(pady=(15, 5))

hire_date_entry = DateEntry(right_frame,width=22,font=("Arial", 12),background="darkblue",foreground="white",borderwidth=2,
date_pattern="yyyy-mm-dd"
)
hire_date_entry.pack(pady=5)
hire_date_entry.set_date(datetime.date.today())

#----Bottom Frame Content------
bottom_left_frame = ctk.CTkScrollableFrame(bottom_frame)
bottom_left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

bottom_right_frame = ctk.CTkScrollableFrame(bottom_frame)
bottom_right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

#---Left Bottom Side----
ctk.CTkLabel(
    bottom_left_frame,
    text="Employee Documents",
    font=("Arial", 15, "bold")
).pack(anchor="w", pady=(5, 10))

def upload_file(label):
    file_path = filedialog.askopenfilename()
    if file_path:
        label.configure(text=file_path.split("/")[-1])

# Certificate
cert_label = ctk.CTkLabel(bottom_left_frame, text="No file selected")
ctk.CTkButton(
    bottom_left_frame,
    text="Upload Certificate",
    command=lambda: upload_file(cert_label)
).pack(anchor="w", pady=(5, 2))
cert_label.pack(anchor="w", padx=20)

# ID Document
id_label = ctk.CTkLabel(bottom_left_frame, text="No file selected")
ctk.CTkButton(
    bottom_left_frame,
    text="Upload ID Document",
    command=lambda: upload_file(id_label)
).pack(anchor="w", pady=(8, 2))
id_label.pack(anchor="w", padx=20)

# CV / Resume
cv_label = ctk.CTkLabel(bottom_left_frame, text="No file selected")
ctk.CTkButton(
    bottom_left_frame,
    text="Upload CV / Resume",
    command=lambda: upload_file(cv_label)
).pack(anchor="w", pady=(8, 2))
cv_label.pack(anchor="w", padx=20)

# Contract
contract_label = ctk.CTkLabel(bottom_left_frame, text="No file selected")
ctk.CTkButton(
    bottom_left_frame,
    text="Upload Contract",
    command=lambda: upload_file(contract_label)
).pack(anchor="w", pady=(8, 2))
contract_label.pack(anchor="w", padx=20)

# --- Right Bottom Side ----
ctk.CTkLabel(
    bottom_right_frame,
    text="Employee Photo",
    font=("Arial", 15, "bold")
).pack(pady=(5, 10))

IMAGE_BOX_SIZE = 160 

def upload_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )
    if not file_path:
        return

    img = Image.open(file_path)

    img.thumbnail((IMAGE_BOX_SIZE, IMAGE_BOX_SIZE))

    photo = ImageTk.PhotoImage(img)
    image_label.configure(image=photo, text="")
    image_label.image = photo 
    image_label.file_path = file_path 

ctk.CTkButton(
    bottom_right_frame,
    text="Upload Image",
    command=upload_image,
    width=150
).pack(pady=5)

image_label = ctk.CTkLabel(
    bottom_right_frame,
    text="No Image",
    width=IMAGE_BOX_SIZE,
    height=IMAGE_BOX_SIZE
)
image_label.pack(pady=10)

ctk.CTkButton(
    main_frame,
    text="Submit Employee",
    font=("Arial", 14, "bold"),
    height=40,
    command=submit
).pack(pady=15)

app.mainloop()