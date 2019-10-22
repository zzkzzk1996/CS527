import pymysql
import psycopg2
from time import time


class connect_mysql():
    def __init__(self, host="localhost", user="myuser", password=None, db="db"):
        self.db = pymysql.connect(host, user, password, db)
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def run_query(self, query_statement):
        start_time = int(round(time() * 1000))
<<<<<<< Updated upstream
        try:
            self.cursor.execute(query_statement)
            result = self.cursor.fetchall()
            query_time = str(int(round(time() * 1000)) - start_time) + " ms"
            if len(result) > 100000:
                result = result[:9999]
                query_time += '\nThe result is too larger to transmit, so we limit the size to return'
            return result, query_time
        except:
            self.db.rollback()
            query_time = str(int(round(time() * 1000)) - start_time) + " ms"
            return "the statement hasn't executed properly!", query_time

    def register_user(self, user_name, password, email_address):
        user_id, password = hash(user_name), hash(password)
        # detect if there already has the same user_id
        query = 'SELECT COUNT(*) FROM user_info WHERE {}={}'
        # query_id = query.format('user_id', user_id)
        # if the userd name exist, insert, else ignore it
        sql = 'INSERT IGNORE INTO user_info (user_id, password, email_address) VALUES ({}, {}, "{}");'.format(
            str(user_id),
            str(password),
            email_address)
        try:
            self.cursor.execute(query.format('user_id', str(user_id)))
            query_id = self.cursor.fetchall()[0]['COUNT(*)']
            self.cursor.execute(query.format('email_address', '"' + email_address + '"'))
            query_email = self.cursor.fetchall()[0]['COUNT(*)']
            # ('email_address', email_address)
            if query_email > 0 and query_id > 0:
                return 'user name and email address has been used'
            elif query_id < 1 and query_email > 0:
                return 'email address has been used'
            elif query_id > 0:
                return 'user name has been used'
            else:
                self.cursor.execute(sql)
                self.db.commit()
                return 'register success'
        except:
            self.db.rollback()
            return "the statement hasn't executed properly!"

    def login(self, user_name, password, email_address):
        user_id, password = hash(user_name) if user_name is not None else user_name, hash(password)
        # .format(user_id if user_id is not None else email_address, password)
        if user_id is None:
            query = 'SELECT {}, password FROM user_info WHERE {}="{}"'.format('email_address', "email_address",
                                                                              email_address)
        else:
            query = 'SELECT {}, password FROM user_info WHERE {}={}'.format('user_id', 'user_id', user_id)
        try:
            self.cursor.execute(query)
            content = self.cursor.fetchall()[0]['password']
        except:
            self.db.rollback()
            return "wrong user name or wrong email address"
        if content == password:
            return 'login sucessful'
        else:
            return 'wrong password'
=======
        self.cursor.execute(query_statement)
        col_info = self.cursor.description
        result = self.cursor.fetchall()
        query_time = str(int(round(time() * 1000)) - start_time) + " ms"
        if len(result) > 100:
            result = result[:99]
            query_time += '\nThe result is too larger to transmit and display, so we limit the size to return'
        col_name = []
        for i in range(len(col_info)):
            col_name.append(col_info[i][0])
        return col_name, result, query_time
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

    def disconnect(self):
        self.cursor.close()
        self.db.close()


class connect_redshift():
    def __init__(self, host="loaclhost", database='database', user='awsuser', password='Cs123456', port=5439):
        self.con = psycopg2.connect(host=host, dbname=database, port=port, password=password, user=user)
        self.cur = self.con.cursor()

    def run_query(self, query_statement):
        start_time = int(round(time() * 1000))
<<<<<<< Updated upstream
        try:
            self.cur.execute(query_statement)
            result = self.cur.fetchall()
            query_time = str(int(round(time() * 1000)) - start_time) + " ms"
            if len(result) > 100000:
                result = result[:9999]
                query_time += '\nThe result is too larger to transmit, so we limit the size to return'

            return result, query_time
        except:
            self.con.rollback()
            query_time = str(int(round(time() * 1000)) - start_time) + " ms"
            return "the statement hasn't executed properly!", query_time
=======
        self.cur.execute(query_statement)
        col_info = self.cur.description
        result = self.cur.fetchall()
        query_time = str(int(round(time() * 1000)) - start_time) + " ms"
        if len(result) > 100:
            result = result[:99]
            query_time += '\nThe result is too larger to transmit and display, so we limit the size to return'
        col_name = []
        for i in range(len(col_info)):
            col_name.append(col_info[i][0])
        return col_name, result, query_time
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

    def disconnect(self):
        self.cur.close()
        self.con.close()
