import psycopg2
import requests
from flask import Flask, render_template, request, redirect
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="1",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

app = Flask(__name__)


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            login = request.form.get('login1')
            password = request.form.get('password')
            if login != '' and login != ' ':

                cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(login), str(password)))
                records = list(cursor.fetchall())
                if not records:
                    return render_template('login.html', error='Такого пользователя не существует')


                return render_template('account.html', full_name=records[0][1])
            else:
                return render_template('login.html', error='Некорректый логин')
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def reg():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        if login != '' and login != ' ' and len(password) > 7:

            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                           (str(name), str(login), str(password)))
            conn.commit()

            return redirect('/login/')
        else:
            return render_template('registration.html', full_name=name)

    return render_template('registration.html')