import customtkinter
from customtkinter import CTkFrame, CTkScrollableFrame
from customtkinter.windows.widgets.font import customtkinter_directory


class Edit(CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width=600, height=500)
        self.grid_columnconfigure(0, weight=1)

        self._top_frame()
        self._middle_frame()
        self._address_frame()
        self._file_upload_frame()
        self._bottom_frame()

        self.save_btn = customtkinter.CTkButton(self, text="Save changes")
        self.save_btn.grid(row=5, column=0)

        self.grid(sticky="nsew")

    def _top_frame(self):
        self._top_frame_container = customtkinter.CTkFrame(self, fg_color="transparent")
        self._top_frame_container.grid_columnconfigure(0, weight=1)

        self._title = customtkinter.CTkLabel(
            self._top_frame_container,
            text="Edit Employee Information",
            font=("Arial", 30),
        )

        self._search_bar = customtkinter.CTkEntry(
            self._top_frame_container,
            placeholder_text="Search by employee ID",
            width=250,
            height=40,
            corner_radius=10,
        )
        self._search_btn = customtkinter.CTkButton(
            self._top_frame_container, text="Search", command=self.search_emp, height=35
        )

        self._title.grid(row=0, column=0, padx=20, pady=20, columnspan=5, sticky="ew")
        self._search_bar.grid(row=1, column=0, padx=10, sticky="ew")
        self._search_btn.grid(row=1, column=1)

        self._top_frame_container.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

    def _middle_frame(self):
        self._container = customtkinter.CTkFrame(self, fg_color="transparent")

        self._full_name_label = customtkinter.CTkLabel(
            self._container, text="Full name"
        )
        self._full_name_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._emp_ID_label = customtkinter.CTkLabel(self._container, text="Employee ID")
        self._emp_ID_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._date_of_birth_label = customtkinter.CTkLabel(
            self._container, text="Date of birth"
        )
        self._date_of_birth_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._gender_label = customtkinter.CTkLabel(self._container, text="Gender")
        self._gender_entry = customtkinter.CTkOptionMenu(
            self._container, values=["Male", "Female"]
        )

        self._contact_num_label = customtkinter.CTkLabel(
            self._container, text="Contact number"
        )
        self._contact_num_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._emergency_contact_label = customtkinter.CTkLabel(
            self._container, text="Emergency Contact"
        )
        self._emergency_contact_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._email_label = customtkinter.CTkLabel(self._container, text="Email")
        self._email_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._hiring_date_label = customtkinter.CTkLabel(
            self._container, text="Hiring date"
        )
        self._hirirg_date_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._address_label = customtkinter.CTkLabel(self._container, text="Address")
        self._address_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._job_category_label = customtkinter.CTkLabel(
            self._container, text="Job Category"
        )
        self._job_category_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._department_label = customtkinter.CTkLabel(
            self._container, text="Department"
        )
        self._department_entry = customtkinter.CTkEntry(
            self._container, width=250, height=40
        )

        self._full_name_label.grid(row=0, column=0)
        self._full_name_entry.grid(row=1, column=0, padx=20)

        self._emp_ID_label.grid(row=0, column=1)
        self._emp_ID_entry.grid(row=1, column=1)

        self._date_of_birth_label.grid(row=2, column=0)
        self._date_of_birth_entry.grid(row=3, column=0)

        self._gender_label.grid(row=2, column=1)
        self._gender_entry.grid(row=3, column=1)

        self._contact_num_label.grid(row=4, column=0)
        self._contact_num_entry.grid(row=5, column=0)

        self._emergency_contact_label.grid(row=4, column=1)
        self._emergency_contact_entry.grid(row=5, column=1)

        self._email_label.grid(row=6, column=0)
        self._email_entry.grid(row=7, column=0)

        self._hiring_date_label.grid(row=6, column=1)
        self._hirirg_date_entry.grid(row=7, column=1)

        self._address_label.grid(row=8, column=0)
        self._address_entry.grid(row=9, column=0)

        self._job_category_label.grid(row=8, column=1)
        self._job_category_entry.grid(row=9, column=1)

        self._department_label.grid(row=10, column=1)
        self._department_entry.grid(row=11, column=1)

        self._container.grid(row=1, column=0)

    def _bottom_frame(self):
        self._bottom_frame_container = customtkinter.CTkFrame(
            self, fg_color="transparent"
        )

        self._employee_status_label = customtkinter.CTkLabel(
            self._bottom_frame_container, text="Employement status"
        )
        self._employee_status_entry = customtkinter.CTkOptionMenu(
            self._bottom_frame_container, values=["Full time", "Part time", "Intern"]
        )

        self._employee_status_label.grid(row=0, column=0, padx=20)
        self._employee_status_entry.grid(row=0, column=1, padx=20)

        self._bottom_frame_container.grid(row=4, column=0, pady=20)

    def _address_frame(self):
        self._address_container = customtkinter.CTkFrame(self, fg_color="transparent")

        self._citizenship_label = customtkinter.CTkLabel(
            self._address_container, text="Citizenship"
        )
        self._citizenship_entry = customtkinter.CTkEntry(self._address_container)

        self._citizenship_label.grid(row=0, column=0)
        self._citizenship_entry.grid(row=1, column=0)

        self._city_label = customtkinter.CTkLabel(self._address_container, text="City")
        self._city_entry = customtkinter.CTkEntry(self._address_container)

        self._city_label.grid(row=0, column=1)
        self._city_entry.grid(row=1, column=1)

        self._subcity_label = customtkinter.CTkLabel(
            self._address_container, text="Subcity"
        )
        self._subcity_entry = customtkinter.CTkEntry(self._address_container)

        self._subcity_label.grid(row=2, column=0)
        self._subcity_entry.grid(row=3, column=0)

        self._woreda_label = customtkinter.CTkLabel(
            self._address_container, text="Woreda"
        )
        self._woreda_entry = customtkinter.CTkEntry(self._address_container)

        self._woreda_label.grid(row=2, column=1)
        self._woreda_entry.grid(row=3, column=1)

        self._kebele_label = customtkinter.CTkLabel(
            self._address_container, text="Kebele"
        )
        self._kebele_entry = customtkinter.CTkEntry(self._address_container)

        self._kebele_label.grid(row=4, column=0)
        self._kebele_entry.grid(row=5, column=0)

        self._houseNo_label = customtkinter.CTkLabel(
            self._address_container, text="House No."
        )
        self._houseNO_entry = customtkinter.CTkEntry(self._address_container)

        self._houseNo_label.grid(row=4, column=1)
        self._houseNO_entry.grid(row=5, column=1)

        self._address_container.grid(row=2, column=0)

    def _file_upload_frame(self):
        self.file_upload_container = customtkinter.CTkFrame(self)

        self._certificate_button = customtkinter.CTkButton(
            self.file_upload_container, text="Upload Certificate"
        )
        self._certificate_button.grid(row=0, column=0)

        self._resume_button = customtkinter.CTkButton(
            self.file_upload_container, text="Upload CV / Resume"
        )
        self._resume_button.grid(row=0, column=1)

        self._contract_button = customtkinter.CTkButton(
            self.file_upload_container, text="Upload Contract"
        )
        self._contract_button.grid(row=1, column=0)

        self._id_document_button = customtkinter.CTkButton(
            self.file_upload_container, text="Upload ID Document"
        )
        self._id_document_button.grid(row=1, column=1)

        self.file_upload_container.grid(row=3, column=0)

    def search_emp(self):
        print("Button clicked")

        empId: str = self._search_bar.get().strip()

        if empId == "":
            return
        else:
            # result = self.editDB.search_emp(empId)

            # if result is None:
            #     self.emp_not_found()

            self.emp_not_found()

    def emp_not_found(self):
        new_window = customtkinter.CTkToplevel(self)
        new_window.title("Error")
        new_window.geometry("400x200")
        new_window.resizable(False, False)
        new_window.wm_attributes("-topmost", True)
        new_window.grab_set()

        label = customtkinter.CTkLabel(new_window, text="Invalid employee id")
        label.pack()

        new_btn = customtkinter.CTkButton(
            new_window, text="Close", command=new_window.destroy
        )
        new_btn.pack(pady=40)


# for testing

if __name__ == "__main__":
    customtkinter.set_appearance_mode("Light")
    customtkinter.set_default_color_theme("green")

    root = customtkinter.CTk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.title("Edit page")
    Edit(root)
    root.mainloop()
