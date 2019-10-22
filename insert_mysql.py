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
    host = 'cs527mysql2.chmrmo5grph7.us-east-1.rds.amazonaws.com'
    user = 'Maaaartian'
    password = 'mysqls250+38qqcn'
    db = 'test'
    db = pymysql.connect(host, user, password, db)
    cursor = db.cursor()
    datas = pd.read_csv('/Users/zekunzhang/2019 Fall/CS527/Instacart/order_products.csv', header=0).values.tolist()
    # print(datas)
    table = "order_products"
    try:
        sql = "INSERT INTO {} (Order_id, Product_id, Add_to_cart_order, Reordered) VALUES (%s, %s, %s, %s)".format(
            table)
        cursor.executemany(sql, datas)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    print('success')
    db.close()
