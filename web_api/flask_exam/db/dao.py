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

    def insert_data(self, **kwargs):
    	result = self.table.insert(**kwargs).execute()

    	return result

    def update_status(self, id):
    	result = self.table.update(status=1).where(self.table.id==id).execute()

    	return result

    def delete_data(self, id):
    	result = self.table.delete().where(self.table.id==id).execute()

    	return result