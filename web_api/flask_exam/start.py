# -*- coding: utf-8 -*-
from flask import Flask
from api.data_api import data_api
from config.config import app_context

def main():

    app = Flask(__name__)
    app.config["app_context"] = app_context
    app.register_blueprint(data_api)
    return app

app = main()

if __name__ == "__main__":
    app = main()
    arg_debug = False 
    app.run(host="0.0.0.0", port=8080, debug=arg_debug, threaded=True)