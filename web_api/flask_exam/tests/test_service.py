# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
from service.data_service import DataService
from db.dao import TestDao

# From Python unittest document:
# Note The order in which the various tests will be run is determined by 
# sorting the test method names with respect to the built-in ordering 
# for strings.

class mock_init_config():
    def __init__(self):
        self.mysql_client = mock_db()
class mock_db():
    class atomic():
        def __enter__(self):
            pass
        def __exit__(self, *args, **kwargs):
            pass
app_context = mock_init_config()

class ServiceTestCase(unittest.TestCase):
    task_data = None
    def setUp(self):
        self.service = DataService(app_context)

    def test_0100_find_all_data_success(self):
        find_all_patch = patch.object(TestDao, 'find_all',
                                      side_effect=self.mock_find_all)
        find_all_patch.start()
        return_data = self.service.find_all_data()
        assert return_data == [{"id": 1,"name": "name","status": 0}, {"id": 2,"name": "name2","status": 1}]
        find_all_patch.stop()
    def test_0200_check_exist_by_id_success(self):
        """
        Test case:
        return_data must be true
        """
        check_exist_by_id_patch = patch.object(TestDao, 'check_exist_by_id',
                                                side_effect=self.mock_check_exist_by_id)
        check_exist_by_id_patch.start()
        id = 1
        return_data = self.service.check_exist_by_id(id)
        assert return_data == True
        check_exist_by_id_patch.stop()
    def test_0201_check_exist_by_id_fail(self):
        """
        Test case:
        function will raise RuntimeError
        """
        self.assertRaisesRegex(RuntimeError, "id is not found in database", self.check_exist_by_id_fail)
    def check_exist_by_id_fail(self):
        check_exist_by_id_patch = patch.object(TestDao, 'check_exist_by_id',
                                                side_effect=self.mock_check_exist_by_id)
        check_exist_by_id_patch.start()
        id = 2
        self.service.check_exist_by_id(id)
        check_exist_by_id_patch.stop()
        
    def test_0300_create_task_success(self):
        """
        Test case:
        create task will return data
        """
        name = "test"
        insert_data_patch = patch.object(TestDao, 'insert_data',
                                        side_effect=self.mock_insert_data)
        get_by_id_patch = patch.object(TestDao, 'get_by_id', 
                                        side_effect=self.mock_get_by_id)
        get_by_id_patch.start()
        insert_data_patch.start()
        return_data = self.service.create_task(name)
        insert_data_patch.stop()
        get_by_id_patch.stop()
        assert return_data == {"id":1, "name":name, "status":0}

    def test_0400_update_task_success(self):
        """
        Test case:
        update task will return data
        """
        _id = 1
        status = 1
        name = "test2"
        update_data_patch = patch.object(TestDao, 'update_data',
                                        side_effect=self.mock_update_data)
        get_by_id_patch = patch.object(TestDao, 'get_by_id', 
                                        side_effect=self.mock_get_by_id)
        get_by_id_patch.start()
        update_data_patch.start()
        return_data = self.service.update_task(_id, status=status, name=name)
        update_data_patch.stop()
        get_by_id_patch.stop()
        assert return_data == {"id":1, "name":"test2", "status":1}

    def test_0500_delete_task_success(self):
        """
        Test case:
        delete task success
        """
        _id = 1
        delete_data_patch = patch.object(TestDao, 'delete_data',
                                        side_effect=self.mock_delete_data)
        delete_data_patch.start()
        return_data = self.service.delete_task(_id)
        delete_data_patch.stop()
        assert return_data == "success"

    def test_0501_delete_task_fail(self):
        """
        Test case:
        delete task fail
        """
        self.assertRaisesRegex(RuntimeError, "id is not found in database", self.delete_task_fail)
    def delete_task_fail(self):
        _id = 2
        delete_data_patch = patch.object(TestDao, 'delete_data',
                                        side_effect=self.mock_delete_data)
        delete_data_patch.start()
        return_data = self.service.delete_task(_id)
        delete_data_patch.stop()      

    def mock_find_all(self, *args, **kwargs):
        return [{"id": 1,"name": "name","status": 0}, {"id": 2,"name": "name2","status": 1}]
    def mock_check_exist_by_id(self, id):
        if id == 1:
            return True
        else:
            return False
    def mock_insert_data(self, name):
        self.__class__.task_data = {"id":1, "name":name, "status":0}
        return 1
    def mock_get_by_id(self, id):
        if id ==1:
            return self.task_data
    def mock_update_data(self, id, **kwargs):
        self.__class__.task_data = {"id":id,"name":kwargs["name"], "status":kwargs["status"]}
    def mock_delete_data(self, id):
        if id == 1:
            return True
        else:
            return False

if __name__ == '__main__':
    unittest.main()