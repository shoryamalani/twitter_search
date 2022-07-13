#!/usr/bin/python

from __future__ import print_function

import psycopg2
def execute_database_command(conn,command):
    cur = conn.cursor()
    cur.execute(command)
    return [conn, cur]
def executemany_database_command(conn,command):
    cur = conn.cursor()
    cur.executemany(command)
    return [conn, cur]
def execute_with_data(conn,command,data):
    cur = conn.cursor()
    cur.execute(command,data)
    return [conn, cur]