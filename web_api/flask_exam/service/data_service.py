# -*- coding: utf-8 -*-
from db.dao import TestDao

class DataService(object):
    def __init__(self, app_context):
        self.__test_dao = TestDao(app_context.mysql_client)

    def find_data(self):
        result = self.__test_dao.find_all()
        return_data = list()
        for i in result:
            return_data.append(i)
        return return_data

    def create_task(self, name):
        return_data = self.__test_dao.insert_data(name=name)

        return return_data

    def update_task(self, id):
        return_data = self.__test_dao.update_status(id)

        return return_data

    def delete_task(self, id):
        return_data = self.__test_dao.delete_data(id)

        return return_data