from flask import Flask, request, render_template, jsonify
from utils import connect_mysql, connect_redshift

app = Flask(__name__)


@app.route('/mysql', methods=['GET'])
def query_mysql():
    query = request.args.get('query', 'show tables;')
    connection = connect_mysql(host='database-1.cqggblhrtnvj.us-east-1.rds.amazonaws.com', user='admin',
                               password='12345678', db='cs527')
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


@app.route('/register', methods=['POST'])
def register():
    user_info = request.get_json()
    user_name = user_info.get('user_name', None)
    password = user_info.get('password', None)
    email_address = user_info.get('email_address', None)
    connection = connect_mysql(host='database-1.cqggblhrtnvj.us-east-1.rds.amazonaws.com', user='admin',
                               password='12345678', db='user')
    result = connection.register_user(user_name=user_name, password=password, email_address=email_address)
    connection.disconnect()
    return jsonify({'result': result})


@app.route('/login', methods=['POST'])
def login():
    user_info = request.get_json()
    user_name, password, email_address = user_info.get('user_name', None), user_info.get('password',
                                                                                         None), user_info.get(
        'email_address', None)
    connection = connect_mysql(host='database-1.cqggblhrtnvj.us-east-1.rds.amazonaws.com', user='admin',
                               password='12345678', db='user')
    result = connection.login(user_name=user_name, password=password, email_address=email_address)
    connection.disconnect()
    return jsonify({'result': result})
