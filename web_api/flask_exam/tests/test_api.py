# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
from start import app
from service.data_service import DataService

# From Python unittest document:
# Note The order in which the various tests will be run is determined by 
# sorting the test method names with respect to the built-in ordering 
# for strings.

class APITestCase(unittest.TestCase):
    task_data = None
    def setUp(self):
        app.testing = True  # select app in test mode
        self.client = app.test_client()

    def test_0100_list_tasks_success(self):
        """
        Test case:
        return data need same as result
        """
        response = self.client.get("/tasks")
        resp_data = response.json
        error_code = response.status_code
        self.assertEqual(resp_data, {"result": [{"id": 1,
                                                 "name": "name",
                                                 "status": 0}]})
        self.assertEqual(error_code, 200)

    def test_0101_list_tasks_fail(self):
        """
        Test case:
        return {"error":"server error"} and 500 code
        """
        find_all_data_patch = patch.object(DataService, 'find_all_data',
                                   side_effect=self.mock_raise_fail)
        find_all_data_patch.start()

        response = self.client.get("/tasks")
        resp_data = response.json
        error_code = response.status_code
        self.assertEqual(resp_data, {"error":"server error"})
        self.assertEqual(error_code, 500)
        
        find_all_data_patch.stop()

    def test_0200_new_task(self):
        """
        Test case:
        new task success in db and 201 code
        """
        init_data = {"name":"買晚餐"}
        response = self.client.post("/task", json=init_data)
        resp_data = response.json
        error_code = response.status_code

        assert "name" in list(resp_data["result"])
        assert "status" in list(resp_data["result"])
        assert "id" in list(resp_data["result"])
        self.assertEqual(error_code, 201)

        # target task_data result be global
        self.__class__.task_data = resp_data["result"]

    def test_0201_new_task_fail(self):
        """
        Test case:
        new task request key don't have name and 400 code
        """
        response = self.client.post("/task", json={})
        resp_data = response.json
        error_code = response.status_code
        self.assertEqual(resp_data, {"error":"key error: name"})
        self.assertEqual(error_code, 400)        

    def test_0202_new_task_fail(self):
        """
        Test case:
        return {"error":"server error"} and 500 code
        """
        create_task_patch = patch.object(DataService, 'create_task',
                                   side_effect=self.mock_raise_fail)
        create_task_patch.start()

        init_data = {"name":"買晚餐"}
        response = self.client.post("/task", json=init_data)
        resp_data = response.json
        error_code = response.status_code
        self.assertEqual(resp_data, {"error":"server error"})
        self.assertEqual(error_code, 500) 

        create_task_patch.stop()

    def test_0300_update_task_success(self):
        """
        Test case:
        return update task's data and 200 code
        """
        self.task_data.update({"status":1})
        response = self.client.put("/task/{}".format(self.task_data["id"]), json=self.task_data)
        resp_data = response.json
        error_code = response.status_code
        self.assertEqual(resp_data, self.task_data)
        self.assertEqual(error_code, 200) 

    def test_0301_update_task_fail(self):
        """
        Test case:
        request id and path request id is not match
        """ 
        # change status to 1
        self.task_data.update({"status":1})

        response = self.client.put("/task/{}".format("1"), json=self.task_data)
        resp_data = response.json
        error_code = response.status_code
        self.assertEqual(resp_data, {"error":"id is not match."})
        self.assertEqual(error_code, 400) 

    def test_0302_update_task_fail(self):
        """
        Test case:
        request status or name is None
        """ 
        # name is not in task_data None
        task_data = {"id":int(self.task_data["id"]), "status":1}
        response = self.client.put("/task/{}".format(int(self.task_data["id"])), json=task_data)
        resp_data = response.json
        error_code = response.status_code
        self.assertDictEqual(resp_data, {"error":"missing request"})
        self.assertEqual(error_code, 400) 
        
        # status value is None
        task_data.update({"id":int(self.task_data["id"]), "name":"1", "status":None})
        response = self.client.put("/task/{}".format(int(self.task_data["id"])), json=task_data)
        resp_data = response.json
        error_code = response.status_code
        self.assertDictEqual(resp_data, {"error":"missing request"})
        self.assertEqual(error_code, 400) 

    def test_0303_update_task_fail(self):
        """
        Test case:
        raise RuntimeError && raise Exception fail
        """ 
        update_task_patch = patch.object(DataService, 'update_task',
                                   side_effect=self.mock_raise_runtime_error)
        update_task_patch.start()
        response = self.client.put("/task/{}".format(int(self.task_data["id"])), json=self.task_data)
        resp_data = response.json
        error_code = response.status_code
        self.assertDictEqual(resp_data, {"error":"raise RuntimeError"})
        self.assertEqual(error_code, 400) 
        update_task_patch.stop()

        update_task_patch2 = patch.object(DataService, 'update_task',
                                   side_effect=self.mock_raise_fail)
        update_task_patch2.start()
        response = self.client.put("/task/{}".format(int(self.task_data["id"])), json=self.task_data)
        resp_data = response.json
        error_code = response.status_code
        self.assertDictEqual(resp_data, {"error":"server error"})
        self.assertEqual(error_code, 500)     
        update_task_patch2.stop()

    def test_0401_delete_task_success(self):
        """
        Test case:
        delete task success
        """
        response = self.client.delete("/task/{}".format(self.task_data["id"]))
        resp_data = response.json
        error_code = response.status_code
        self.assertEqual(resp_data, {"success":"delete success"})
        self.assertEqual(error_code, 200) 
    
    def test_0400_delete_task_fail(self):
        """
        Test case:
        raise RuntimeError && raise Exception fail
        """ 
        delete_task_patch = patch.object(DataService, 'delete_task',
                                   side_effect=self.mock_raise_runtime_error)
        delete_task_patch.start()
        response = self.client.delete("/task/{}".format(self.task_data["id"]))
        resp_data = response.json
        error_code = response.status_code
        self.assertDictEqual(resp_data, {"error":"raise RuntimeError"})
        self.assertEqual(error_code, 400) 
        delete_task_patch.stop()

        delete_task_patch2 = patch.object(DataService, 'delete_task',
                                   side_effect=self.mock_raise_fail)
        delete_task_patch2.start()
        response = self.client.delete("/task/{}".format(int(self.task_data["id"])))
        resp_data = response.json
        error_code = response.status_code
        self.assertDictEqual(resp_data, {"error":"server error"})
        self.assertEqual(error_code, 500)     
        delete_task_patch2.stop()

    def test_0402_delete_task_fail(self):
        """
        Test case:
        id is not found in db
        """ 
        response = self.client.delete("/task/{}".format(int(self.task_data["id"])))
        resp_data = response.json
        error_code = response.status_code
        self.assertDictEqual(resp_data, {"error":"id is not found in database"})
        self.assertEqual(error_code, 400)     


    def mock_raise_fail(self, *args, **kwargs):
        raise Exception("raise Error")
    def mock_raise_runtime_error(self, *args, **kwargs):
        raise RuntimeError("raise RuntimeError")

if __name__ == '__main__':
    unittest.main()
