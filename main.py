import tkinter as tk
from tkinter import ttk, messagebox, font
from mie_trak import MieTrak
import json


class LoginScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login Screen")
        self.geometry("300x200")
        self.database_conn = MieTrak()
        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Username label and entry
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack(pady=5)

        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        # Password label and entry
        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)
        self.password_entry.bind("<Return>", self.login_check)

        # Login button
        self.login_button = tk.Button(self, text="Login", command=self.login_check)
        self.login_button.pack(pady=10)

    def login_check(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()

        login_succes_or_not = self.database_conn.login_check(username, password)

        # TODO: DELETE THIS
        login_succes_or_not = True
        # TODO: DELETE THIS

        if login_succes_or_not is True:
            # messagebox.showinfo("Login", "Login successful!")
            self.destroy()
            doc_app = DocGroupAccess()
            doc_app.mainloop()
        else:
            messagebox.showerror("Login", "Invalid credentials")


class DocGroupAccess(tk.Tk):
    def __init__(self):
        super().__init__()
        self.heading_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")

        self.title("Document Group User Access")
        self.geometry("700x500")
        self.database_conn = MieTrak()
        self.user_pk = None

        self.user_data_dict = self.database_conn.get_user_data(enabled=True)
        # self.user_names = list(" ".join(self.user_data_dict.values()[0], self.user_data_dict.values()[1]))
        self.user_data_list = [
            (value[0], value[1]) for value in self.user_data_dict.values()
        ]
        # [(v, k) for k, v in self.user_data_dict.items()]
        self.user_display_list = [
            f"{firstname} {lastname}" for firstname, lastname in self.user_data_list
        ]
        self.current_user_display_list = (
            self.user_display_list.copy()
        )  # Store current display list

        self.department_dict = self.database_conn.get_department()
        self.department_names = list(self.department_dict.values())
        self.department_data_list = [(v, k) for k, v in self.department_dict.items()]
        self.department_display_list = [
            f"{name}" for name, pk in self.department_data_list
        ]
        self.document_group_dict = self.database_conn.get_document_groups()
        self.document_groups = list(self.document_group_dict.values())
        self.make_combobox1()

    def make_combobox1(self):
        tk.Label(self, text="Add/Delete Users", font=self.heading_font).grid(
            row=0, column=0, columnspan=2, sticky="WE"
        )

        button1 = tk.Button(
            self,
            text="Remove User Access GUI",
            font=self.button_font,
            command=self.open_single_user,
        )
        button1.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="WENS")

        button2 = tk.Button(
            self,
            text="Multiple User GUI",
            font=self.button_font,
            command=self.open_multiple_user,
        )
        button2.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="WSNE")

        tk.Label(self, text="Department Mapping", font=self.heading_font).grid(
            row=0, column=2, columnspan=2, sticky="WE"
        )

        button3 = tk.Button(
            self,
            text="Configure GUI",
            font=self.button_font,
            command=self.open_department,
        )
        button3.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="NSWE")

        maintain_dept_access_button = tk.Button(
            self,
            text="EXE-Maintain Dept Access",
            font=self.button_font,
            command=self.maintain_all_department_access,
        )
        maintain_dept_access_button.grid(
            row=2, column=2, padx=5, pady=5, columnspan=2, sticky="WENS"
        )

        remove_non_active_users_access_button = tk.Button(
            self,
            text="EXE-Remove all access from non-active users",
            font=self.button_font,
            command=self.database_conn.remove_access_non_active_user,
        )
        remove_non_active_users_access_button.grid(
            row=3, column=0, padx=5, pady=5, columnspan=4, sticky="WENS"
        )

        col, row = self.grid_size()
        for c in range(col):
            self.grid_columnconfigure(c, weight=1)
        for r in range(row):
            self.grid_rowconfigure(r, weight=1)

    def open_single_user(self):
        self.open_new_window("Single User")

    def open_multiple_user(self):
        self.open_new_window("Multiple User")

    def open_department(self):
        self.open_new_window("Department")

    def open_new_window(self, title):
        new_window = tk.Toplevel(self)
        new_window.title(title)
        # new_window.geometry("950x500")
        new_window.grab_set()

        # # Create a label or any other widgets here
        # label = tk.Label(new_window, text=f"This is {title}")
        # label.pack(pady=20)

        # # Create a back button
        # back_button = tk.Button(new_window, text="Back", command=new_window.destroy)
        # back_button.pack(pady=10)
        if title == "Single User":
            new_window.geometry("600x500")

            tk.Label(new_window, text="Select User: ", font=self.heading_font).grid(
                row=0, column=0, columnspan=4, sticky="NSEW", padx=5, pady=5
            )
            self.user_combobox = ttk.Combobox(
                new_window,
                values=self.user_display_list,
                state="normal",
                font=self.button_font,
            )
            self.user_combobox.grid(
                row=1, column=0, columnspan=4, sticky="NS", padx=5, pady=5
            )
            self.user_combobox.bind("<KeyRelease>", self.filter_combobox)

            # self.enabled_user_var = tk.BooleanVar()
            # self.enabled_user_checkbox = tk.Checkbutton(
            #     new_window,
            #     text="Active Users Only",
            #     variable=self.enabled_user_var,
            #     command=self.filter_by_enabled_user,
            # )
            # self.enabled_user_checkbox.grid(row=0, column=1)
            remove_access_button = tk.Button(
                new_window,
                text="REMOVE ACCESS",
                command=self.confirm_delete_access,
                font=self.button_font,
            )
            remove_access_button.grid(
                row=9, column=0, columnspan=2, padx=5, pady=5, sticky="NSEW"
            )
            remove_all_access_button = tk.Button(
                new_window,
                text="REMOVE ALL ACCESS",
                command=self.confirm_remove_all_access,
                font=self.button_font,
            )
            remove_all_access_button.grid(
                row=9, column=2, columnspan=2, padx=5, pady=5, sticky="NSEW"
            )
            tk.Label(new_window, text="Accessed Document Groups:", font=self.heading_font).grid(
                row=2, column=0, columnspan=4, sticky="NSEW"
            )
            self.selected_user_info = tk.Listbox(
                new_window,
                height=10,
                width=50,
                exportselection=False,
                selectmode=tk.EXTENDED,
            )
            self.selected_user_info.grid(
                row=4, column=0, columnspan=4, rowspan=4, sticky="NSEW", padx=5, pady=5
            )
            self.user_combobox.bind(
                "<<ComboboxSelected>>", self.update_selected_user_info
            )

            col, row = new_window.grid_size()
            for c in range(col):
                new_window.grid_columnconfigure(c, weight=1)
            for r in range(3):
                new_window.grid_rowconfigure(r, weight=1)

            for c in range(4, 9):
                new_window.grid_rowconfigure(c, weight=2)

        elif title == "Multiple User":
            tk.Label(
                new_window, text="Select Document Group(s):", font=self.heading_font
            ).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
            self.document_group_listbox = tk.Listbox(
                new_window,
                height=10,
                width=50,
                exportselection=False,
                selectmode=tk.EXTENDED,
            )
            for group in self.document_groups:
                self.document_group_listbox.insert(tk.END, group)
            self.document_group_listbox.grid(
                row=1, column=0, rowspan=3, columnspan=2, sticky="NSEW", padx=5, pady=5
            )
            tk.Label(
                new_window, text="Select Users to Give Access: ", font=self.heading_font
            ).grid(row=0, column=2, columnspan=2, padx=5, pady=5)
            self.multi_user_listbox = tk.Listbox(
                new_window,
                height=10,
                width=50,
                exportselection=False,
                selectmode=tk.EXTENDED,
            )
            for user in self.user_display_list:
                self.multi_user_listbox.insert(tk.END, user)
            self.multi_user_listbox.grid(
                row=1, column=2, rowspan=3, columnspan=2, sticky="NSEW", padx=5, pady=5
            )
            give_access_button = tk.Button(
                new_window,
                text="EXE-GIVE ACCESS",
                command=self.give_access,
                font=self.button_font,
            )
            give_access_button.grid(
                row=4, column=0, columnspan=4, sticky="NSEW", padx=5, pady=5
            )

            col, row = new_window.grid_size()
            for c in range(col):
                new_window.grid_columnconfigure(c, weight=1)
            for r in range(row):
                new_window.grid_rowconfigure(r, weight=1)

        elif title == "Department":
            tk.Label(
                new_window, text="Select Department: ", font=self.heading_font
            ).grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky="NSEW")
            self.department_combobox = ttk.Combobox(
                new_window, values=self.department_display_list, state="normal"
            )
            self.department_combobox.grid(
                row=1, column=0, columnspan=6, padx=5, pady=5, sticky="SN"
            )

            self.department_combobox.bind(
                "<<ComboboxSelected>>", self.display_accessable_document_groups
            )

            # give_dept_access_button = tk.Button(new_window, text="Give Dept Access", command= lambda: self.give_or_remove_department_access("give"))
            # give_dept_access_button.grid(row=4, column=0)

            # remove_dept_access_button = tk.Button(new_window, text="Remove Dept Access", command=lambda: self.give_or_remove_department_access("remove"))
            # remove_dept_access_button.grid(row=4, column=1)

            tk.Label(
                new_window, text="Add/Remove Doc Groups", font=self.heading_font
            ).grid(row=2, column=2, columnspan=2, padx=5, pady=5)
            self.document_group_listbox = tk.Listbox(
                new_window,
                height=10,
                width=50,
                exportselection=False,
                selectmode=tk.EXTENDED,
            )
            for group in self.document_groups:
                self.document_group_listbox.insert(tk.END, group)
            self.document_group_listbox.grid(
                row=3, column=2, columnspan=2, rowspan=3, padx=5, pady=5, sticky="NSEW"
            )

            tk.Label(
                new_window, text="Users in Department: ", font=self.heading_font
            ).grid(row=2, column=4, columnspan=2, padx=5, pady=5, sticky="NSEW")
            self.department_user_listbox = tk.Listbox(
                new_window,
                height=10,
                width=50,
                exportselection=False,
                selectmode="browse",
            )
            self.department_user_listbox.grid(
                row=3, column=4, columnspan=2, rowspan=3, padx=5, pady=5, sticky="NSEW"
            )

            tk.Label(
                new_window, text="Document groups mapped", font=self.heading_font
            ).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="NSEW")
            self.department_doc_group_listbox = tk.Listbox(
                new_window,
                height=10,
                width=50,
                exportselection=False,
                selectmode=tk.EXTENDED,
            )
            self.department_doc_group_listbox.grid(
                row=3, column=0, columnspan=2, rowspan=3, padx=5, pady=5, sticky="NSEW"
            )

            add_to_dept_button = tk.Button(
                new_window,
                text="Add to Dept map",
                command=lambda: self.add_or_remove_from_department("add"),
                font=self.button_font,
            )
            add_to_dept_button.grid(
                row=6, column=2, columnspan=2, padx=5, pady=5, sticky="NSEW"
            )

            remove_from_dept = tk.Button(
                new_window,
                text="Remove from Dept",
                command=lambda: self.add_or_remove_from_department("remove"),
                font=self.button_font,
            )
            remove_from_dept.grid(
                row=6, column=0, columnspan=2, padx=5, pady=5, sticky="NSEW"
            )

            maintain_dept_access_button = tk.Button(
                new_window,
                text="EXE-Maintain Dept Access",
                command=self.maintain_all_department_access,
                font=self.button_font,
            )
            maintain_dept_access_button.grid(
                row=6, column=4, columnspan=2, padx=5, pady=5, sticky="NSEW"
            )

            col, row = new_window.grid_size()
            print(col, row)
            for c in range(col):
                new_window.grid_columnconfigure(c, weight=1)
            for r in range(row):
                new_window.grid_rowconfigure(r, weight=1)

    def filter_by_enabled_user(self):
        if self.enabled_user_var.get():
            user_data_dict = self.database_conn.get_user_data(enabled=True)
        else:
            user_data_dict = self.database_conn.get_user_data()

        user_data_list = [(value[0], value[1]) for value in user_data_dict.values()]
        # [(v, k) for k, v in user_data_dict.items()]
        self.user_display_list = [
            f"{name} {lastname}" for name, lastname in user_data_list
        ]
        self.current_user_display_list = self.user_display_list.copy()

        self.user_combobox["values"] = self.user_display_list
        self.user_combobox.set("")  # Clear the current selection
        self.multi_user_listbox.delete(0, tk.END)
        for user in self.user_display_list:
            self.multi_user_listbox.insert(tk.END, user)

    def filter_combobox(self, event):
        """Filter for selecting customers, type and search"""
        current_text = self.user_combobox.get().lower()
        filtered_values = [
            name
            for name in self.current_user_display_list
            if name.lower().startswith(current_text)
        ]
        self.user_combobox["values"] = filtered_values

    def update_selected_user_info(self, event):
        selected_user_display = self.user_combobox.get()
        user_first_name = selected_user_display.split(" ")[0]
        user_last_name = selected_user_display.split(" ")[-1]
        # for first_name in self.user_data_dict.values():
        #     if first_name[0] == user_first_name:
        #         self.selected_user_pk = self.user_data_dict[first_name]
        for key, value in self.user_data_dict.items():
            if user_first_name in value[0] and user_last_name in value[1]:
                self.user_pk = key
        # self.user_pk = selected_user_display.split(" (UserPK: ")[1][:-1]
        self.doc_user_group_dict = self.database_conn.get_accesed_document_group(
            self.user_pk, self.document_group_dict
        )

        self.selected_user_info.delete(0, tk.END)

        if self.doc_user_group_dict:
            for pk, group in self.doc_user_group_dict.items():
                self.selected_user_info.insert(tk.END, f"{pk}: {group}")

    def give_access(self):
        selected_indices = self.document_group_listbox.curselection()
        selected_user_indices = self.multi_user_listbox.curselection()
        if not selected_indices and selected_user_indices:
            messagebox.showwarning(
                "No Selection", "Please select at least one document group and User."
            )
            return

        for index in selected_indices:
            selected_doc_group = self.document_group_listbox.get(index)
            selected_doc_group_pk = None
            for key, value in self.document_group_dict.items():
                if value == selected_doc_group:
                    selected_doc_group_pk = key
                    break
            for ind in selected_user_indices:
                selected_user = self.multi_user_listbox.get(ind)
                # selected_user_pk = None
                user_first_name = selected_user.split(" ")[0]
                user_last_name = selected_user.split(" ")[1]
                # for first_name in self.user_data_dict.values():
                #     if first_name[0] == user_first_name:
                #         self.selected_user_pk = self.user_data_dict[first_name]
                for key, value in self.user_data_dict.items():
                    if value[0] == user_first_name and value[1] == user_last_name:
                        selected_user_pk = key
                # selected_user_pk = selected_user.split(" (UserPK: ")[1][:-1]

                if selected_doc_group_pk and selected_user_pk:
                    self.database_conn.add_document_group_user(
                        selected_doc_group_pk, selected_user_pk
                    )
        # if self.user_pk:
        #     self.update_selected_user_info(None)
        self.document_group_listbox.selection_clear(0, tk.END)
        self.multi_user_listbox.selection_clear(0, tk.END)
        messagebox.showinfo("Done", "Access Given")

    def confirm_delete_access(self):
        selected_indices = self.selected_user_info.curselection()
        if not selected_indices:
            return

        confirmation = messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete selected access?"
        )
        if confirmation:
            self.delete_access()

    def delete_access(self):
        selected_indices = self.selected_user_info.curselection()
        for index in selected_indices:
            selected_doc_group = self.selected_user_info.get(index)
            selected_doc_group_pk = selected_doc_group.split(":")[0]
            self.database_conn.delete_document_group_user(selected_doc_group_pk)
        self.update_selected_user_info(None)
        messagebox.showinfo("Done", "Access Removed")

    def confirm_remove_all_access(self):
        if not self.doc_user_group_dict:
            return

        confirmation = messagebox.askyesno(
            "Confirm Remove All", "Are you sure you want to remove all access?"
        )
        if confirmation:
            self.remove_all_access()

    def remove_all_access(self):
        for pk, group in self.doc_user_group_dict.items():
            self.database_conn.delete_document_group_user(pk)
        self.update_selected_user_info(None)
        messagebox.showinfo("Done", "All Access Removed")

    def give_or_remove_department_access(self, access):
        selected_indices = self.document_group_listbox.curselection()
        for index in selected_indices:
            selected_doc_group = self.document_group_listbox.get(index)
            selected_doc_group_pk = None
            for key, value in self.document_group_dict.items():
                if value == selected_doc_group:
                    selected_doc_group_pk = key
                    break
            selected_department = self.department_combobox.get()
            for key, value in self.department_dict.items():
                if value == selected_department:
                    selected_department_pk = key
            # selected_dpartment_pk = selected_department.split(" (DepartmentPK: ")[1][:-1]
            if access == "give":
                self.database_conn.department_access(
                    "Give", selected_department_pk, selected_doc_group_pk
                )
            elif access == "remove":
                self.database_conn.department_access(
                    "Remove", selected_department_pk, selected_doc_group_pk
                )

        # if self.user_pk:
        #     self.update_selected_user_info(None)
        self.document_group_listbox.selection_clear(0, tk.END)
        # self.multi_user_listbox.selection_clear(0, tk.END)

    def maintain_all_department_access(self):
        department_doc_group = self.load_dict()
        self.database_conn.maintain_department_access(department_doc_group)
        messagebox.showinfo(
            "Done", "Access given to all the Users according to their Department"
        )

    def display_accessable_document_groups(self, event=None):
        self.department_user_listbox.delete(0, tk.END)
        self.department_doc_group_listbox.delete(0, tk.END)
        department_doc_group_dict = self.load_dict()
        selected_department = self.department_combobox.get()
        for key, value in self.department_dict.items():
            if value == selected_department:
                selected_department_pk = key
        department_user = self.database_conn.get_department_user(selected_department_pk)
        for key2, value2 in department_user.items():
            self.department_user_listbox.insert(tk.END, value2[0] + " " + value2[1])
        for k, v in department_doc_group_dict.items():
            if int(k) == selected_department_pk:
                for doc_group_pk in v:
                    for key1, value1 in self.document_group_dict.items():
                        if key1 == doc_group_pk:
                            self.department_doc_group_listbox.insert(tk.END, value1)
        # selected_indices = self.document_group_listbox.curselection()
        # for index in selected_indices:
        #     selected_doc_group = self.document_group_listbox.get(index)
        #     selected_doc_group_pk = None
        #     for key, value in self.document_group_dict.items():
        #         if value == selected_doc_group:
        #             selected_doc_group_pk = key
        #             break

    def add_or_remove_from_department(self, access):
        selected_department = self.department_combobox.get()
        for key1, value1 in self.department_dict.items():
            if value1 == selected_department:
                selected_department_pk = key1
        selected_indices = self.document_group_listbox.curselection()
        for index in selected_indices:
            selected_doc_group = self.document_group_listbox.get(index)
            selected_doc_group_pk = None
            for key, value in self.document_group_dict.items():
                if value == selected_doc_group:
                    selected_doc_group_pk = key
                    if access == "add":
                        self.add_value(
                            str(selected_department_pk), selected_doc_group_pk
                        )
                    elif access == "remove":
                        self.remove_value(
                            str(selected_department_pk), selected_doc_group_pk
                        )

        if access == "add":
            messagebox.showinfo("Done", "Doc Groups added")
        elif access == "remove":
            messagebox.showinfo("Done", "Doc Groups removed")

    def load_dict(self):
        try:
            with open("data.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    # Save dictionary to JSON file
    def save_dict(self, data):
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

    # Add value to list
    def add_value(self, key, new_value):
        # new_value = simpledialog.askstring("Input", f"Enter new value for {key}:")
        dictionary = self.load_dict()
        if new_value and dictionary:
            if new_value not in dictionary[key]:
                dictionary[key].append(new_value)
            self.save_dict(dictionary)
            self.refresh_listbox(dictionary, key)

    # Remove value from list
    def remove_value(self, key, value):
        # value = simpledialog.askstring("Input", f"Enter value to remove from {key}:")
        dictionary = self.load_dict()
        if dictionary and value in dictionary[key]:
            dictionary[key].remove(value)
            self.save_dict(dictionary)
            self.refresh_listbox(dictionary, key)
        # else:
        #     messagebox.showerror("Error", f"Value '{value}' not found in {key}")

    # Refresh the listbox with updated dictionary values
    def refresh_listbox(self, dictionary, selected_department_pk):
        self.department_doc_group_listbox.delete(0, tk.END)
        for key, values in dictionary.items():
            if key == selected_department_pk:
                for doc_group_pk in values:
                    for key1, value1 in self.document_group_dict.items():
                        if key1 == doc_group_pk:
                            self.department_doc_group_listbox.insert(tk.END, value1)


if __name__ == "__main__":
    app = LoginScreen()
    # app = DocGroupAccess()
    app.mainloop()
