#!/bin/bash
gunzip < sql_dump.sql.gz | mysql -uroot -pabcd123 Test