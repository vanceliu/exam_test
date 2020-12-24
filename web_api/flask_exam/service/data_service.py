# -*- coding: utf-8 -*-
from db.dao import TestDao

class DataService(object):
    def __init__(self, app_context):
        self.__test_dao = TestDao(app_context.mysql_client)

    def find_all_data(self):
        result = self.__test_dao.find_all()
        return_data = list()
        for i in result:
            return_data.append(i)
        return return_data

    def check_exist_by_id(self, id):
        boolean = self.__test_dao.check_exist_by_id(id)
        if boolean == True:
            pass
        else:
            raise RuntimeError("id is not found in database")

    def create_task(self, name):
        with self.__test_dao.db.atomic():
            return_id = self.__test_dao.insert_data(name=name)
            return_data = self.__test_dao.get_by_id(return_id)
        return return_data

    def update_task(self, id, **kwargs):
        with self.__test_dao.db.atomic():
            return_data = self.__test_dao.update_data(id, **kwargs)
            return_data = self.__test_dao.get_by_id(id)
        return return_data

    def delete_task(self, id):
        with self.__test_dao.db.atomic():
            return_data = self.__test_dao.delete_data(id)
        if return_data == True:
            return "success"
        else:
            raise RuntimeError("id is not found in database")