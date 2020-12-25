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
        result = service.find_all_data()
        return json.jsonify(result=result), 200
    except Exception as e:
        return json.jsonify({"error":"server error"}), 500

@data_api.route('/task', methods=["POST"])
def new_task():

    service = DataService(current_app.config["app_context"])
    request_data = request.get_json()
    name = request_data.get("name", None)
    if not name:
        return json.jsonify({"error":"key error: name"}), 400
    try:
        result = service.create_task(name)
        return json.jsonify(result=result), 201
    except Exception as e:
        return json.jsonify({"error":"server error"}), 500


@data_api.route('/task/<int:id>', methods=["PUT", "DELETE"])
def update_or_delete_task(id):

    service = DataService(current_app.config["app_context"])
    request_data = request.get_json()
    try:
        data_exist = service.check_exist_by_id(id)
        
        if request.method == "PUT":
            status = request_data.get("status")
            name = request_data.get("name")
            _id = request_data.get("id")
            if int(_id) != id:
                return json.jsonify({"error":"id is not match."}), 400
            if status == None or name == None:          
                return json.jsonify({"error":"missing request"}), 400
            if not isinstance(status, int) or not isinstance(name, str):
                return json.jsonify({"error":"request type wrong"}), 400
            result = service.update_task(id=_id, status=status, name=name)
            return json.jsonify(result), 200
        
        if request.method == "DELETE":
            result = service.delete_task(id)
            return json.jsonify({"success":"delete success"}), 200
    except RuntimeError as exp:
        return json.jsonify({"error": str(exp)}), 400
    except Exception as e:
        return json.jsonify({"error":"server error"}), 500
