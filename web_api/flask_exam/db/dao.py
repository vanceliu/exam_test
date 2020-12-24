# -*- coding: utf-8 -*-
import peewee
from db.models import Test_Table
from db.mysql_base import MySqlRepository

class TestDao(MySqlRepository):
    def __init__(self, mysql_client):
        super().__init__(mysql_client)

    def _get_table(self):
        return Test_Table

    def find_all(self):
        result = self.table.select().dicts()
        return result
    
    def get_by_id(self, id):
        result = self.table.select().where(self.table.id==id).dicts().get()
        return result if result else None

    def check_exist_by_id(self, id):
        result = self.table.select().where(self.table.id==id).exists()
        return True if result else False

    def insert_data(self, **kwargs):
        result = self.table.insert(**kwargs).execute()
        return result

    def update_data(self, id, **kwargs):
        result = self.table.update(**kwargs).where(self.table.id==id).execute()
        return True if result !=0 else False

    def delete_data(self, id):
        result = self.table.delete().where(self.table.id==id).execute()
        print(result)
        return True if result !=0 else False