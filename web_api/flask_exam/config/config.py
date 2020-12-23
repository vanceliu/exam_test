# -*- coding: utf-8 -*-
from db.mysql_base import MySqlConnectionProvider, MySqlConfig

class init_config():
    def __init__(self):
        self.mysql_client = self.init_mysql_client()
    def init_mysql_client(self):
        try:
            mysql_config =  MySqlConfig(dbname="Test",
                                        host="mysql",
                                        username="root",
                                        port=3306,
                                        password="abcd123"
                                        )
            provider = MySqlConnectionProvider(mysql_config)
            # print("init mysql client success")
            return provider.create_client()
        except Exception as e:
            print("init mysql client has error")
            raise

app_context = init_config()