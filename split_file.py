# -*- coding: utf-8 -*-
# @Time    : 2019-10-15 18:14
# @Author  : Ziqi Wang
# @FileName: split_file.py
# @email    ：zw280@scarletmail.rutgers.edu
from datetime import datetime


def Main():
    source_dir = '/Users/ziwan/Documents/Rutgers Course/semester3/DB/Instacart/orders.csv'
    target_dir = '/Users/ziwan/Documents/Rutgers Course/semester3/DB/Instacart/'

    # 计数器
    flag = 0

    # 文件名
    name = 1

    # 存放数据
    dataList = []

    print("start ++++++++++")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    with open(source_dir, 'r') as f_source:
        for line in f_source:
            flag += 1
            dataList.append(line)
            if flag == 80000:
                with open(target_dir + "orders" + str(name) + ".csv", 'w+') as f_target:
                    for data in dataList:
                        f_target.write(data)
                name += 1
                flag = 0
                dataList = []

    # 处理最后一批行数少于200万行的
    with open(target_dir + "orders" + str(name) + ".csv", 'w+') as f_target:
        for data in dataList:
            f_target.write(data)

    print("finish+++++++++")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == "__main__":
    Main()
