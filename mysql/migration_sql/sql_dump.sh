#!/bin/bash
mysqldump -uroot -pabcd123 Test --default-character-set=utf8mb4 --single-transaction --flush-logs | gzip > sql_dump.sql.gz
