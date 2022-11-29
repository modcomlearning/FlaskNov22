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


@app.route('/programs')
def programs():
    return render_template('programs.html')


if __name__ == '__main__':
    app.run(debug=True)
