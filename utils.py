# -*- coding: utf-8 -*-
# @Time    : 2019-10-12 17:11
# @Author  : Ziqi Wang
# @FileName: utils.py
# @email    ：zw280@scarletmail.rutgers.edu

import pymysql
from time import time
import psycopg2


class connect_mysql():
    def __init__(self, host="localhost", user="myuser", password=None, db="db"):
        self.db = pymysql.connect(host, user, password, db)
        self.cursor = self.db.cursor()

    def run_query(self, query_statement):
        start_time = int(round(time() * 1000))
        self.cursor.execute(query_statement)
        result = self.cursor.fetchall()
        query_time = int(round(time() * 1000)) - start_time
        return result, query_time

    def disconnect(self):
        self.db.close()


class connect_redshift():
    def __init__(self, host="loaclhost", database='database', user='awsuser', password='Zw12345678', port=5439):
        self.con = psycopg2.connect(host=host, dbname=database, port=port, password=password, user=user)
        self.cur = self.con.cursor()

    def run_query(self, query_statement):
        start_time = int(round(time() * 1000))
        self.cur.execute(query_statement)
        result = self.cur.fetchall()
        query_time = int(round(time() * 1000)) - start_time
        return result, query_time

    def disconnect(self):
        self.cur.close()
        self.con.close()
