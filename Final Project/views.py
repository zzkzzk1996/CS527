from flask import Flask, request, render_template, jsonify, session
from utils import connect_mysql

application = Flask(__name__)

temp_json = {'col_name': None, 'result': None, 'query_time': None}


# @application.route('/mysql', methods=['GET'])
# def query_mysql():
#     query = request.args.get('query', 'show tables;')
#     connection = connect_mysql(host='cs527mysql2.chmrmo5grph7.us-east-1.rds.amazonaws.com', user='Maaaartian',
#                                password='mysqls250+38qqcn', db='test')
#     col_name, content, query_time = connection.run_query(query)
#     result = {'col_name': col_name, 'result': content, 'query_time': query_time}
#     connection.disconnect()
#     return result


@application.route('/alexa', methods=['GET'])
def query_mysql():
    query = request.args.get('query', 'show tables;')
    connection = connect_mysql(host='cs527mysql2.chmrmo5grph7.us-east-1.rds.amazonaws.com', user='Maaaartian',
                               password='mysqls250+38qqcn', db='test')
    col_name, content, query_time = connection.run_query(query)
    # result = {'col_name': col_name, 'result': content, 'query_time': query_time}
    temp_json['col_name'] = col_name
    temp_json['result'] = content
    temp_json['query_time'] = query_time
    connection.disconnect()
    return "Success"


@application.route('/getquery', methods=['GET'])
def get_query():
    ret = {'col_name': temp_json['col_name'], 'result': temp_json['result'], 'query_time': temp_json['query_time']}
    return jsonify(ret)


# @application.route('/redshift', methods=['GET'])
# def query_redshift():
#     query = request.args.get('query', 'show tables;')
#     connection = connect_redshift(host='cs527redshift.clyua6krsyew.us-east-1.redshift.amazonaws.com', user='group3',
#                                   password='Redshift123',
#                                   database='dev')
#     col_name, content, query_time = connection.run_query(query)
#     result = {'col_name': col_name, 'result': content, 'query_time': query_time}
#     connection.disconnect()
#     return result


@application.route('/', methods=['GET'])
def index():
    return render_template('index.html')
