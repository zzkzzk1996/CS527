from flask import Flask, request, jsonify, render_template, redirect, make_response
from utils import connect_mysql, connect_redshift

app = Flask(__name__)


@app.route('/mysql', methods=['GET', 'POST'])
def query_mysql():
    query = request.args.get('query', 'show tables;')
    connection = connect_mysql(host='database-3.c8ainggp8y19.us-east-1.rds.amazonaws.com', user='admin',
                               password='12345678', db='cs527')
    content = connection.run_query(query)
    result = {'result': content}
    respond = jsonify(result)
    connection.disconnect()
    return respond


@app.route('/redshift', methods=['GET', 'POST'])
def query_redshift():
    if request.method == 'POST':
        query = request.get_json('query', 'show tables;')
    else:
        query = request.args.get('query', 'show tables;')
    connection = connect_redshift(host='redshift-cluster-1.cxyojdkh3h9f.us-east-1.redshift.amazonaws.com',
                                  database='dev')
    content = connection.run_query(query)
    result = {'result': content}
    # respond = make_response(jsonify(result), '200')
    respond = jsonify(result)
    connection.disconnect()
    # return respond
    # return redirect('/')
    # message = respond
    return render_template('index.html', message=result)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        method = request.form['InputName']
        query = request.form['InputMessage']

        if (method == "mysql" or method == "redshift") and query is not None:
            return redirect('/' + method + '?query=' + query)
    return render_template('index.html')
