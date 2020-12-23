# -*- coding: utf-8 -*-
import peewee

class TinyIntegerField(peewee.IntegerField):
    field_type = 'TINYINT'

class Test_Table(peewee.Model):
    id = peewee.PrimaryKeyField()
    name = peewee.CharField(10)
    status = TinyIntegerField()