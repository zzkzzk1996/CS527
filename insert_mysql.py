#!/usr/bin/env python
# encoding: utf-8
# @project : CS527
# @author: Zekun Zhang
# @contact: zekunzhang.1996@gmail.com
# @file: insert_mysql.py
# @time: 2019-10-15 23:27:37
import pymysql
import pandas as pd

if __name__ == '__main__':
    host = 'database-1.cqggblhrtnvj.us-east-1.rds.amazonaws.com'
    user = 'admin'
    password = '12345678'
    db = 'cs527'
    db = pymysql.connect(host, user, password, db)
    cursor = db.cursor()
    datas = pd.read_csv('/Users/zekunzhang/2019 Fall/CS527/Instacart/order_products.csv', header=0).values.tolist()
    print(datas)
    table = "Order_products"
    try:
        sql = "INSERT INTO {} (order_id, product_id, add_to_cart_order, reordered) VALUES (%s, %s, %s, %s)".format(table)
        cursor.executemany(sql, datas)
        db.commit()
    except:
        db.rollback()
        print("22222222")
    db.close()
