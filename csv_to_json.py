#!/usr/bin/env python
# encoding: utf-8
# @project : HackRU
# @author: Zekun Zhang
# @contact: zekunzhang.1996@gmail.com
# @file: csv_to_json.py
# @time: 2019-11-05 13:29:49
import csv
import json

path = '/Users/zekunzhang/2019 Fall/CS527/Instacart/'
path_write = '/Users/zekunzhang/2019 Fall/CS527/Instacart/'
file_names = ['aisles', 'departments', 'orders', 'products', 'order_products']
col_names = [("aisle_id", "aisle"), ("department_id", "department"),
             ("order_id", "user_id", "order_number", "order_dow", "order_hour_of_day", "days_since_prior_order"),
             ("product_id", "product_name", "aisle_id", "department_id"),
             ("order_id", "product_id", "add_to_cart_order", "reordered")]


def csv_reader():
    for file_name, col_name in zip(file_names, col_names):
        f = open(path + file_name + '.csv', 'rU')
        reader = csv.DictReader(f, fieldnames=col_name)
        print("Read successfully")
        out = json.dumps([row for row in reader])
        print("Parse successfully")
        f = open(path_write + file_name + '.json', 'w')
        f.write(out)
        print("Write successfully")


if __name__ == '__main__':
    csv_reader()
