#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Controls.sqlhelper import sqlhelper

sql_guy = sqlhelper()

print(sql_guy.readstatus())
