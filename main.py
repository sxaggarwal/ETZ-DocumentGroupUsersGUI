import tkinter as tk
from tkinter import ttk, messagebox
from src.mie_trak import MieTrak


class DocGroupAccess(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Document Group User Access")
        self.geometry("920x600")
        self.database_conn = MieTrak()
        self.user_pk = None

        self.user_data_dict = self.database_conn.get_user_data()
        # self.user_names = list(" ".join(self.user_data_dict.values()[0], self.user_data_dict.values()[1]))
        self.user_data_list = [(value[0], value[1]) for value in self.user_data_dict.values()]
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
        self.make_combobox()

    def make_combobox(self):
        tk.Label(self, text="Select User: ").grid(row=1, column=1)
        self.user_combobox = ttk.Combobox(
            self, values=self.user_display_list, state="normal"
        )
        self.user_combobox.grid(row=2, column=1)
        self.user_combobox.bind("<KeyRelease>", self.filter_combobox)

        self.enabled_user_var = tk.BooleanVar()
        self.enabled_user_checkbox = tk.Checkbutton(
            self,
            text="Active Users Only",
            variable=self.enabled_user_var,
            command=self.filter_by_enabled_user,
        )
        self.enabled_user_checkbox.grid(row=0, column=1)

        tk.Label(self, text="Select Document Group(s):").grid(row=6, column=0)
        self.document_group_listbox = tk.Listbox(
            self, height=10, width=50, exportselection=False, selectmode=tk.EXTENDED
        )
        for group in self.document_groups:
            self.document_group_listbox.insert(tk.END, group)
        self.document_group_listbox.grid(row=7, column=0)

        tk.Label(self, text="Accessed Document Groups:").grid(row=3, column=1)
        self.selected_user_info = tk.Listbox(
            self, height=10, width=50, exportselection=False, selectmode=tk.EXTENDED
        )
        self.selected_user_info.grid(row=4, column=1)
        self.user_combobox.bind("<<ComboboxSelected>>", self.update_selected_user_info)

        give_access_button = tk.Button(
            self, text="GIVE ACCESS", command=self.give_access
        )
        give_access_button.grid(row=8, column=1)
        remove_access_button = tk.Button(
            self, text="REMOVE ACCESS", command=self.confirm_delete_access
        )
        remove_access_button.grid(row=5, column=0)
        remove_all_access_button = tk.Button(
            self, text="REMOVE ALL ACCESS", command=self.confirm_remove_all_access
        )
        remove_all_access_button.grid(row=5, column=2)

        tk.Label(self, text="Select Users to Give Access: ").grid(row=6, column=2)
        self.multi_user_listbox = tk.Listbox(
            self, height=10, width=50, exportselection=False, selectmode=tk.EXTENDED
        )
        for user in self.user_display_list:
            self.multi_user_listbox.insert(tk.END, user)
        self.multi_user_listbox.grid(row=7, column=2)

        remove_non_active_users_access_button = tk.Button(self, text="Remove Non Active Access", command=self.database_conn.remove_access_non_active_user)
        remove_non_active_users_access_button.grid(row=9, column=1)

        tk.Label(self, text="Select Department: ").grid(row=10,column=0)
        self.department_combobox = ttk.Combobox(self, values=self.department_display_list, state="normal")
        self.department_combobox.grid(row=10, column=1)

        give_dept_access_button = tk.Button(self, text="Give Dept Access", command= lambda: self.give_or_remove_department_access("give"))
        give_dept_access_button.grid(row=11, column=0)

        remove_dept_access_button = tk.Button(self, text="Remove Dept Access", command=lambda: self.give_or_remove_department_access("remove"))
        remove_dept_access_button.grid(row=11, column=1)

        maintain_dept_access_button = tk.Button(self, text="Maintain Dept Access", command=self.database_conn.maintain_department_access)
        maintain_dept_access_button.grid(row=11, column=2)

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
        user_last_name = selected_user_display.split(" ")[1]
        # for first_name in self.user_data_dict.values():
        #     if first_name[0] == user_first_name:
        #         self.selected_user_pk = self.user_data_dict[first_name]
        for key, value in self.user_data_dict.items():
            if value[0] == user_first_name and value[1] == user_last_name:
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
        if self.user_pk:
            self.update_selected_user_info(None)
        self.document_group_listbox.selection_clear(0, tk.END)
        self.multi_user_listbox.selection_clear(0, tk.END)

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
                self.database_conn.department_access("Give", selected_department_pk, selected_doc_group_pk)
            elif access == "remove":
                self.database_conn.department_access("Remove", selected_department_pk, selected_doc_group_pk)
        
        if self.user_pk:
            self.update_selected_user_info(None)
        self.document_group_listbox.selection_clear(0, tk.END)
        self.multi_user_listbox.selection_clear(0, tk.END)

    
    def maintain_all_department_access(self):
        pass


if __name__ == "__main__":
    app = DocGroupAccess()
    app.mainloop()
