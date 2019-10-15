from flask import Flask, request, jsonify, render_template, redirect, make_response
from utils import connect_mysql, connect_redshift

app = Flask(__name__)


@app.route('/mysql', methods=['GET'])
def query_mysql():
    query = request.args.get('query', 'show tables;')
    connection = connect_mysql(host='cs527mysql2.chmrmo5grph7.us-east-1.rds.amazonaws.com', user='Maaaartian',
                               password='mysqls250+38qqcn', db='test')
    content, query_time = connection.run_query(query)
    result = {'result': content, 'query_time': query_time}
    connection.disconnect()
    return result


@app.route('/redshift', methods=['GET'])
def query_redshift():
    query = request.args.get('query', 'show tables;')
    connection = connect_redshift(host='cs527redshift.clyua6krsyew.us-east-1.redshift.amazonaws.com', user='maaaartian',
                                  password='_Sm85823201',
                                  database='test')
    content, query_time = connection.run_query(query)
    result = {'result': content, 'query_time': query_time}
    connection.disconnect()
    return result


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
