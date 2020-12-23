# -*- coding: utf-8 -*-
import traceback
from flask import Blueprint, json, current_app, request
from service.data_service import DataService
data_api = Blueprint("data_api", __name__)

@data_api.teardown_app_request
def _db_close(exc):
    app_context = current_app.config["app_context"]
    if not app_context.mysql_client.is_closed():
        app_context.mysql_client.close()

@data_api.route('/tasks', methods=["GET"])
def list_tasks():

    service = DataService(current_app.config["app_context"])
    try:
        result = service.find_data()
        return json.jsonify(result=result), 200
    except Exception as e:
        print(e)
        return "server error", 500

@data_api.route('/task', methods=["POST"])
def new_task():

    service = DataService(current_app.config["app_context"])
    reqest_data = request.get_json()
    name = reqest_data.get("name", None)
    if not name:
        return None, 400
    try:
        result = service.create_task(name)
        return json.jsonify(result=result), 201
    except Exception as e:
        print(e)
        return "server error", 500


@data_api.route('/task/<string:id>', methods=["PUT", "DELETE"])
def update_task(id):

    service = DataService(current_app.config["app_context"])
    reqest_data = request.get_json()
    try:

        if request.method == "PUT":
            result = service.update_task(id)
            # 判斷拿不到id 要報錯 但不是回傳500
            return json.jsonify(result=result), 200
        if request.method == "DELETE":
            result = service.delete_task(id)
            # 判斷拿不到id 要報錯 但不是回傳500
            return "success" ,200
        return 405
    except Exception as e:
        print(e)
        return "server error", 500
