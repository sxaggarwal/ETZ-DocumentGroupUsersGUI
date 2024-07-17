from src.general_class import TableManger


class MieTrak:
    def __init__(self):
        self.user_table = TableManger("[User]")
        self.document_group_table = TableManger("DocumentGroup")
        self.document_group_users_table = TableManger("DocumentGroupUsers")
        self.department_table = TableManger("Department")

    def get_user_data(self, enabled=False, not_active=False, departmentfk=None):
        """Returns all the user data in the form of a dict with UserPK as Key and FirstName as Value

        Returns:
            dict = {"UserPK": "FirstName"}
        """
        user_dict = {}
        if enabled:
            user = self.user_table.get("UserPK", "FirstName", "LastName", Enabled=1)
        elif not_active:
            user = self.user_table.get("UserPK", "FirstName", "LastName",Enabled=0)
        elif departmentfk:
            user = self.user_table.get("UserPK", "FirstName", "LastName",DepartmentFK=departmentfk, Enabled=1)
        else:
            user = self.user_table.get("UserPK", "FirstName", "LastName")

        if user:
            for x in user:
                if x:
                    user_dict[x[0]] = [x[1],x[2]]
        return user_dict

    def get_document_groups(self):
        """Returns all the DocumentGroups data in the form of a dict with DocumentGroupPK as Key and Name as Value

        Returns:
            dict = {"DocumentGroupPK" : "DocumentGroupName"}
        """
        document_group_dict = {}
        document_groups = self.document_group_table.get("DocumentGroupPK", "Name")
        if document_groups:
            for x in document_groups:
                if x:
                    document_group_dict[x[0]] = x[1]
        return document_group_dict

    def get_accesed_document_group(self, user_pk, document_group_dict):
        """Returns all the document Group that the user has access to in the form of a dict"""
        doc_user_group_dict = {}
        document_group_pk = self.document_group_users_table.get(
            "DocumentGroupUsersPK", "DocumentGroupFK", UserFK=user_pk
        )
        if document_group_pk:
            for pk in document_group_pk:
                if pk:
                    doc_user_group_dict[pk[0]] = document_group_dict[pk[1]]
            return doc_user_group_dict

    def delete_document_group_user(self, document_group_users_pk):
        """Deletes the entry for a selected PK from DocumentGroupUsers Table"""
        self.document_group_users_table.delete(document_group_users_pk)

    def add_document_group_user(self, doc_group_pk, user_fk):
        """Adds a new entry to the DocumentGroupUsers table"""
        pk = self.document_group_users_table.get("DocumentGroupUsersPK", UserFK=user_fk, DocumentGroupFK=doc_group_pk)
        if not pk:
            info_dict = {"DocumentGroupFK": doc_group_pk, "UserFK": user_fk}
            pk = self.document_group_users_table.insert(info_dict)
        return pk
    
    def remove_access_non_active_user(self):
        """Removes access to all non active users"""
        non_active_user_dict = self.get_user_data(not_active=True)
        doc_group_dict = self.get_document_groups()
        for user_pk in non_active_user_dict.keys():
            doc_user_group_dict = self.get_accesed_document_group(user_pk, doc_group_dict)
            if doc_user_group_dict:
                for doc_group_pk in doc_user_group_dict.keys():
                    self.delete_document_group_user(doc_group_pk) 

    def get_department(self):
        """Returns all the Department data in the form of a dict with DepartmentPK as Key and Name as value"""
        department_dict = {}
        departments = self.department_table.get("DepartmentPK", "Name")
        if departments:
            for x in departments:
                if x:
                    department_dict[x[0]] = x[1]
        return department_dict
    
    def department_access(self, access, departmentfk, document_group_fk):
        user = self.get_user_data(departmentfk=departmentfk)
        print(user)
        if access=="Give":
            for user_pk in user.keys():
                self.add_document_group_user(document_group_fk, user_pk)
        elif access=="Remove":
            for user_pk1 in user.keys():
                document_group_users_pk = self.document_group_users_table.get("DocumentGroupUsersPK", DocumentGroupFK=document_group_fk, UserFK=user_pk1)
                if document_group_users_pk:
                    for pk in document_group_users_pk:
                        self.delete_document_group_user(pk[0])

    def maintain_department_access(self):
        """Maintains the access of the users to the documents based on the department they belong to"""
        department_doc_groups = {

        }
        document_group_dict = self.get_document_groups()
        department_dict = self.get_department()
        for departmentfk in department_dict.keys():

            user = self.get_user_data(departmentfk=departmentfk)
            for user_pk in user.keys():
                doc_user_group_dict = self.get_accesed_document_group(user_pk, document_group_dict) 
                if doc_user_group_dict:
                    for doc_group_pk in doc_user_group_dict.keys():
                        if doc_group_pk not in department_doc_groups[departmentfk].values():
                            self.add_document_group_user(doc_group_pk, user_pk)
                else:
                    for pk in department_doc_groups[departmentfk].values():
                        self.add_document_group_user(pk, user_pk)


