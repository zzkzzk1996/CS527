from flask import Flask, request, jsonify, render_template, redirect, make_response
from utils import connect_mysql, connect_redshift

app = Flask(__name__)


@app.route('/mysql', methods=['GET'])
def query_mysql():
    query = request.args.get('query', 'show tables;')
    connection = connect_mysql(host='database-3.c8ainggp8y19.us-east-1.rds.amazonaws.com', user='admin',
                               password='12345678', db='cs527')
    content, query_time = connection.run_query(query)
    result = {'result': content, 'query_time': query_time}
    connection.disconnect()
    return result


@app.route('/redshift', methods=['GET'])
def query_redshift():
    query = request.args.get('query', 'show tables;')
    connection = connect_redshift(host='redshift-cluster-1.cxyojdkh3h9f.us-east-1.redshift.amazonaws.com',
                                  database='dev')
    content, query_time = connection.run_query(query)
    result = {'result': content, 'query_time': query_time}
    connection.disconnect()
    return result


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
