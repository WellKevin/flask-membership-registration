from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector
app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nn101586501",
    database="website"
)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass

    if session.get('username') is not None:
        user = session['username']
        return redirect(url_for('member', user=user))
    return redirect(url_for('signin'))


@app.route("/member", methods=['GET', 'POST'])
def member():
    if request.method == 'POST':
        pass

    if session.get('username') is not None:
        user = session['username']
        return render_template('member.html', user=user)
    return redirect(url_for('signin'))


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        acct = request.values['acct']
        pwd = request.values['pwd']

        if acct == "" or pwd == "":
            return redirect(url_for('error', message="您未輸入帳號或密碼"))

        try:
            cursor = mydb.cursor()
            sql = "SELECT * FROM user WHERE username = '" + \
                acct + "' AND password = '" + pwd + "';"
            cursor.execute(sql)
            user = cursor.fetchone()

            cursor.close()

            if user != None:
                session['username'] = user[1]
                return redirect(url_for('member'))
            return redirect(url_for('error', message="未註冊帳號 或 帳號或密碼輸入錯誤"))
        except Exception as e:
            print("Problem select from db: " + str(e))
        finally:
            cursor.close()

    return render_template('signin.html')


@app.route("/signup", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        reg_name = request.values['reg_name']
        reg_acct = request.values['reg_acct']
        reg_pwd = request.values['reg_pwd']

        try:
            cursor = mydb.cursor()
            sql = "SELECT * FROM user WHERE username = '" + reg_acct + "';"

            cursor.execute(sql)
            reg = cursor.fetchone()

            if reg != None:
                return redirect(url_for('error', message="帳號已經被註冊"))

            sql = "INSERT INTO user(id, name, username, password) VALUES (0, \"" + \
                reg_name + "\", \"" + reg_acct + "\", \"" + reg_pwd + "\");"
            cursor.execute(sql)
            mydb.commit()

        except Exception as e:
            print("Problem inserting into db: " + str(e))
        finally:
            cursor.close()

        return redirect(url_for('index'))

    return render_template('signup.html')


@app.route('/error', methods=['GET', 'POST'])
def error():
    if request.method == 'POST':
        pass

    session.pop('username', None)
    message = request.values['message']
    return render_template('error.html', message=message)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(host='127.0.0.1', port='3000', debug=True)
