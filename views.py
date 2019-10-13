# -*- coding: utf-8 -*-
# @Time    : 2019-10-12 17:12
# @Author  : Ziqi Wang
# @FileName: views.py
# @email    ：zw280@scarletmail.rutgers.edu

from flask import Flask, request, jsonify, make_response
from utils import connect_mysql, connect_redshift

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/mysql', methods=['GET'])
def query_mysql():
    query = request.args.get('query', 'show tables;')
    connection = connect_mysql(host='database-3.c8ainggp8y19.us-east-1.rds.amazonaws.com', user='admin',
                               password='12345678', db='cs527')
    content = connection.run_query(query)
    result = {'result': content}
    respond = make_response(jsonify(result), '200')
    connection.disconnect()
    return respond


@app.route('/redshift', methods=['GET'])
def query_redshift():
    query = request.args.get('query', 'show tables;')
    connection = connect_redshift(host='redshift-cluster-1.coed1bpqw3xw.us-east-1.redshift.amazonaws.com',
                                  database='dev')
    content = connection.run_query(query)
    result = {'result': content}
    respond = make_response(jsonify(result), '200')
    connection.disconnect()
    return respond


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({error: 'page not found'}), 404)
