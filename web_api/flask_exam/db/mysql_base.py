# -*- coding: utf-8 -*-
import abc
from peewee import MySQLDatabase

class MySqlConfig(object):
    __charset = "utf8mb4"

    def __init__(self, host, username, password, port=None, dbname=None):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.username = username
        self.password = password

    @property
    def charset(self):
        return self.__charset

    @charset.setter
    def charset(self, value):
        self.__charset = value

class MySqlConnectionProvider(object):
    def __init__(self, config):
        self.mysql_config = config

    def create_client(self,  **kwargs):
        client =  MySQLDatabase(self.mysql_config.dbname,
                                host=self.mysql_config.host,
                                user=self.mysql_config.username,
                                port=self.mysql_config.port,
                                passwd=self.mysql_config.password,
                                **kwargs
                            )
        # print("create mysql client:{}".format(client))
        return client

class MySqlRepository(abc.ABC):
    def __init__(self, db):
        self.table = self._get_table()
        self.table._meta.database = db

    @abc.abstractmethod
    def _get_table(self):
        pass



