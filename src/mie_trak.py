from src.general_class import TableManger


class MieTrak:
    def __init__(self):
        self.user_table = TableManger("[User]")
        self.document_group_table = TableManger("DocumentGroup")
        self.document_group_users_table = TableManger("DocumentGroupUsers")

    def get_user_data(self, enabled=False):
        """Returns all the user data in the form of a dict with UserPK as Key and FirstName as Value

        Returns:
            dict = {"UserPK": "FirstName"}
        """
        user_dict = {}
        if enabled:
            user = self.user_table.get("UserPK", "FirstName", Enabled=1)
        else:
            user = self.user_table.get("UserPK", "FirstName")

        if user:
            for x in user:
                if x:
                    user_dict[x[0]] = x[1]
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
        info_dict = {"DocumentGroupFK": doc_group_pk, "UserFK": user_fk}
        pk = self.document_group_users_table.insert(info_dict)
        return pk
