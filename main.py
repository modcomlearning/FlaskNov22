from flask import *

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'Working'


import pymysql
import pymysql.cursors


@app.route('/', methods=['GET'])
def home():
    connection = pymysql.connect(host='localhost', user='root', password='',
                                 database='Flask_Web')
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    # SELECT, FROM, WHERE
    # SELECT * FROM `Products` WHERE Product_Brand = 'Kinderkraft' and Product_Vendor = 'Naivas' Order by Product_Regdate DESC
    sql = '''
         SELECT * FROM `Products` Order by Product_Regdate DESC Limit 8
    '''
    cursor.execute(sql)
    if cursor.rowcount == 0:
        return render_template('Home.html', message='Coming Soon!')
    else:
        rows = cursor.fetchall()
        print(rows)
        return render_template('Home.html', rows=rows)



@app.route('/single/<pid>', methods=['GET'])
def single(pid):
    connection = pymysql.connect(host='localhost', user='root', password='',
                                 database='Flask_Web')
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    # SELECT, FROM, WHERE
    # SELECT * FROM `Products` WHERE Product_Brand = 'Kinderkraft' and Product_Vendor = 'Naivas' Order by Product_Regdate DESC
    sql = '''
         SELECT * FROM `Products` where Pid = %s Order by Product_Regdate DESC Limit 8
    '''
    cursor.execute(sql, (pid))
    if cursor.rowcount == 0:
        return render_template('single.html', message='Coming Soon!')
    else:
        row = cursor.fetchone()
        print(row)
        return render_template('single.html', row=row)


@app.route('/programs')
def programs():
    return render_template('programs.html')



@app.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method =='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        phone = request.form['phone']
        address = request.form['address']
        # check if passwords are same
        import re
        if password != confirm:
            return  render_template('signup.html', msg = 'Password Not matching')
        elif len(password)  < 8:
            return render_template('signup.html', msg = 'Must be more than 8 -xters')

        else:
            connection = pymysql.connect(host='localhost', user='root',
                                         password='',database='Flask_Web')
            cursor = connection.cursor()
            cursor.execute('insert into Users(username,email,password,phone, address)values(%s,%s,%s, %s, %s)',
                               (username, email, password, phone, address))
            # we need to make a commit to changes to dbase
            connection.commit()
            return render_template('signup.html', success = 'Thank you for Joining')
    else: # this means POST was not used, show the signup template
        return  render_template('signup.html')


# create a route for login
@app.route('/signin', methods = ['POST','GET'])
def signin():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']

        # process login
        connection = pymysql.connect(host='localhost', user='root', password='',
                                     database='Flask_Web')

        # Create a cursor to execute SQL Query
        cursor = connection.cursor()
        cursor.execute('select * from Users where email = %s and password =%s',
                       (email, password))
        # above query should either find a match or not
        # check how may rows cursor found
        if cursor.rowcount ==0:
            return render_template('signin.html', error = 'Wrong Credentials!')

        elif cursor.rowcount ==1:
            #session['key'] = email
            return redirect('/')
        else:
            return render_template('signin.html', error = 'Something went wrong')

    else:
        return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)
