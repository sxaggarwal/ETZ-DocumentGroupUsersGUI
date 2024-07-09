import tkinter as tk
from tkinter import ttk
from src.mie_trak import MieTrak

class DocGroupAccess(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Document Group User Access")
        self.geometry("600x300")
        self.database_conn = MieTrak()
        
        self.user_data_dict = self.database_conn.get_user_data()
        self.user_names = list(self.user_data_dict.values())
        self.user_data_list = [(v, k) for k, v in self.user_data_dict.items()]
        self.user_display_list = [f"{name} (UserPK: {pk})" for name, pk in self.user_data_list]
        self.document_group_dict = self.database_conn.get_document_groups()
        self.document_groups = list(self.document_group_dict.values())
        self.make_combobox()

    def make_combobox(self):
        tk.Label(self, text="Select User: ").grid(row=0, column=0)
        self.user_combobox = ttk.Combobox(self, values=self.user_display_list, state="normal")
        self.user_combobox.grid(row=0, column=1)
        tk.Label(self, text="Select Document Group").grid(row=1, column=0)
        self.document_group_combobox = ttk.Combobox(self, values=self.document_groups, state="normal")
        self.document_group_combobox.grid(row=1, column=1)
        tk.Label(self, text="Accessed Document Groups:").grid(row=2, column=0)
        self.selected_user_info = tk.Listbox(self, height=4, width=50, exportselection=False)
        self.selected_user_info.grid(row=2, column=1)
        self.user_combobox.bind("<<ComboboxSelected>>", self.update_selected_user_info)
        give_access_button = tk.Button(self, text="GIVE ACCESS", command=self.give_access)
        give_access_button.grid(row=3, column=0)
        remove_access_button = tk.Button(self, text="REMOVE ACCESS", command=self.delete_access)
        remove_access_button.grid(row=3, column=1)
        remove_all_access_button = tk.Button(self, text="REMOVE ALL ACCESS", command=self.remove_all_access)
        remove_all_access_button.grid(row=3, column=2)

    
    def update_selected_user_info(self, event):
        selected_user_display = self.user_combobox.get()
        # Extract the PK from the selected display string
        self.user_pk = selected_user_display.split(" (UserPK: ")[1][:-1]
        # user_name = selected_user_display.split(" (PK: ")[0]

        self.doc_user_group_dict = self.database_conn.get_accesed_document_group(self.user_pk, self.document_group_dict)
        self.selected_user_info.delete(0, tk.END)
        # self.selected_user_info.insert(tk.END, f"User PK: {user_pk}\nName: {user_name}\n\nAccessed Document Groups:\n")
        
        for pk, group in self.doc_user_group_dict.items():
            self.selected_user_info.insert(tk.END, f"{pk}:{group}")
    
    def give_access(self):
        selected_doc_group = self.document_group_combobox.get()
        selected_doc_group_pk = None
        for key, value in self.document_group_dict.items():
            if value == selected_doc_group:
                selected_doc_group_pk = key
                break
        if selected_doc_group_pk and self.user_pk:
            pk = self.database_conn.add_document_group_user(selected_doc_group_pk, self.user_pk)
            # Update the listbox
            self.update_selected_user_info(None)

    def delete_access(self):
        try:
            selected_index = self.selected_user_info.curselection()[0]
            selected_doc_group = self.selected_user_info.get(selected_index)
            selected_doc_group_pk = selected_doc_group.split(":")[0]
            self.database_conn.delete_document_group_user(selected_doc_group_pk)
            # Update the listbox
            self.update_selected_user_info(None)
        except IndexError:
            pass  # No selection made in the Listbox
    
    def remove_all_access(self):
        for pk, group in self.doc_user_group_dict.items():
            self.database_conn.delete_document_group_user(pk)
        self.update_selected_user_info(None)

    
if __name__ == "__main__":
    app = DocGroupAccess()
    app.mainloop()
        
