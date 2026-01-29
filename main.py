import customtkinter as ctk

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("BITS EMPLOYEE MANAGEMENT SYSTEM")
app.geometry("1000x600")


#-----MainFrame
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True)

#---Button/Left Frame
left_frame = ctk.CTkFrame(
    main_frame,
    width=220,
    corner_radius=0
)
left_frame.pack(side="left", fill="y")
left_frame.pack_propagate(False)  # keep fixed width

#---Page/Right Frame
right_frame = ctk.CTkFrame(main_frame)
right_frame.pack(side="left", fill="both", expand=True)

# --- Button Container
button_container = ctk.CTkFrame(left_frame, fg_color="transparent")
button_container.place(relx=0.5, rely=0.5, anchor="center")

# ---- BUTTON STYLE 
def sidebar_button(text):
    return ctk.CTkButton(
        button_container,
        text=text,
        width=180,
        height=40,
        font=("Arial", 13)
    )
# -------- BUTTONS 
sidebar_button("Home").pack(pady=6)
sidebar_button("New Employee").pack(pady=6)
sidebar_button("Search").pack(pady=6)
sidebar_button("Edit Employee").pack(pady=6)
sidebar_button("Remove Employee").pack(pady=6)
sidebar_button("Contract").pack(pady=6)
sidebar_button("Department / Job").pack(pady=6)

app.mainloop()