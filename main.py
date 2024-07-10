import tkinter as tk
from tkinter import ttk, messagebox
from src.mie_trak import MieTrak


class DocGroupAccess(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Document Group User Access")
        self.geometry("600x400")
        self.database_conn = MieTrak()

        self.user_data_dict = self.database_conn.get_user_data()
        self.user_names = list(self.user_data_dict.values())
        self.user_data_list = [(v, k) for k, v in self.user_data_dict.items()]
        self.user_display_list = [
            f"{name} (UserPK: {pk})" for name, pk in self.user_data_list
        ]
        self.current_user_display_list = (
            self.user_display_list.copy()
        )  # Store current display list

        self.document_group_dict = self.database_conn.get_document_groups()
        self.document_groups = list(self.document_group_dict.values())
        self.make_combobox()

    def make_combobox(self):
        tk.Label(self, text="Select User: ").grid(row=0, column=0)
        self.user_combobox = ttk.Combobox(
            self, values=self.user_display_list, state="normal"
        )
        self.user_combobox.grid(row=0, column=1)
        self.user_combobox.bind("<KeyRelease>", self.filter_combobox)

        self.enabled_user_var = tk.BooleanVar()
        self.enabled_user_checkbox = tk.Checkbutton(
            self,
            text="Enabled Users",
            variable=self.enabled_user_var,
            command=self.filter_by_enabled_user,
        )
        self.enabled_user_checkbox.grid(row=0, column=2)

        tk.Label(self, text="Select Document Group(s):").grid(row=1, column=0)
        self.document_group_listbox = tk.Listbox(
            self, height=10, width=50, exportselection=False, selectmode=tk.MULTIPLE
        )
        for group in self.document_groups:
            self.document_group_listbox.insert(tk.END, group)
        self.document_group_listbox.grid(row=1, column=1)

        tk.Label(self, text="Accessed Document Groups:").grid(row=2, column=0)
        self.selected_user_info = tk.Listbox(
            self, height=10, width=50, exportselection=False, selectmode=tk.MULTIPLE
        )
        self.selected_user_info.grid(row=2, column=1)
        self.user_combobox.bind("<<ComboboxSelected>>", self.update_selected_user_info)

        give_access_button = tk.Button(
            self, text="GIVE ACCESS", command=self.give_access
        )
        give_access_button.grid(row=3, column=0)
        remove_access_button = tk.Button(
            self, text="REMOVE ACCESS", command=self.confirm_delete_access
        )
        remove_access_button.grid(row=3, column=1)
        remove_all_access_button = tk.Button(
            self, text="REMOVE ALL ACCESS", command=self.confirm_remove_all_access
        )
        remove_all_access_button.grid(row=3, column=2)

    def filter_by_enabled_user(self):
        if self.enabled_user_var.get():
            user_data_dict = self.database_conn.get_user_data(enabled=True)
        else:
            user_data_dict = self.database_conn.get_user_data()

        user_data_list = [(v, k) for k, v in user_data_dict.items()]
        self.user_display_list = [
            f"{name} (UserPK: {pk})" for name, pk in user_data_list
        ]
        self.current_user_display_list = self.user_display_list.copy()

        self.user_combobox["values"] = self.user_display_list
        self.user_combobox.set("")  # Clear the current selection

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
        self.user_pk = selected_user_display.split(" (UserPK: ")[1][:-1]
        self.doc_user_group_dict = self.database_conn.get_accesed_document_group(
            self.user_pk, self.document_group_dict
        )

        self.selected_user_info.delete(0, tk.END)

        if self.doc_user_group_dict:
            for pk, group in self.doc_user_group_dict.items():
                self.selected_user_info.insert(tk.END, f"{pk}: {group}")

    def give_access(self):
        selected_indices = self.document_group_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning(
                "No Selection", "Please select at least one document group."
            )
            return

        for index in selected_indices:
            selected_doc_group = self.document_group_listbox.get(index)
            selected_doc_group_pk = None
            for key, value in self.document_group_dict.items():
                if value == selected_doc_group:
                    selected_doc_group_pk = key
                    break
            if selected_doc_group_pk and self.user_pk:
                self.database_conn.add_document_group_user(
                    selected_doc_group_pk, self.user_pk
                )

        self.update_selected_user_info(None)
        self.document_group_listbox.selection_clear(0, tk.END)

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


if __name__ == "__main__":
    app = DocGroupAccess()
    app.mainloop()
