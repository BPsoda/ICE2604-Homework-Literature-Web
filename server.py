import flask
import pymysql
from flask import Flask
app = Flask(__name__)

# connect to Mysql
try:
    conn = pymysql.connect(host="server.acemap.cn",
                            port=13306,
                            user="ieei",
                            passwd="ieei_2021",
                            charset="utf8",
                            db="ieei_web")
    cursor = conn.cursor()
except:
    print('Fail to connect to the database.')
    exit(-1)

@app.route('/')
def welcome():
    return flask.render_template('/index.html')

@app.route('/pages/page1')
def randomDisplay():
    '''Random display 10 papers'''
    # get table colomn name
    cursor.execute("SELECT column_name FROM information_schema.columns \
                     WHERE TABLE_SCHEMA='ieei_web' AND table_name='paper'")
    labels = cursor.fetchall()
    print(labels)
    labels = [i[0] for i in labels]
    # get 10 table content
    cursor.execute('SELECT * FROM paper \
                    ORDER BY RAND() \
                    LIMIT 10')
    content = cursor.fetchall()
    return flask.render_template('/pages/page1.html', labels=labels, content=content)
    # return flask.render_template('/pages/page1.html', content=content)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)