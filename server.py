from re import search
import flask
from flask.helpers import url_for
import pymysql
from flask import Flask
from werkzeug.wrappers import request
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


@app.route('/pages/page3', methods=['POST', 'GET'])
def SearchbyId():
    '''Search paper by paper id'''
    # retrive paper id from the form 
    if flask.request.method == 'POST':
        print('Using POST method')
        paperid = flask.request.form['searchField']
        print(paperid)
    else:
        print('Using GET method.')
        paperid = flask.request.args.get('searchField','')
    print('Using GET method.')
    print(flask.request.form)
    print(paperid)
    if len(paperid) < 1 : 
        return flask.render_template('/pages/page3.html', flag=False)

    # get table colomn name
    cursor.execute("SELECT column_name FROM information_schema.columns \
                    WHERE TABLE_SCHEMA='ieei_web' AND table_name='paper'")
    labels = cursor.fetchall()
    labels = [i[0] for i in labels]
    # get table content by id
    cursor.execute('SELECT * FROM paper \
                    WHERE paper_id={}'.format(paperid))
    content = cursor.fetchall()
    return flask.render_template('/pages/page3.html', flag=True, labels=labels, content=content)

# @app.route('/pages/page1')
# def randomDisplay():
#     '''Random display 10 papers'''
#     # get table colomn name
#     cursor.execute("SELECT column_name FROM information_schema.columns \
#                     WHERE TABLE_SCHEMA='ieei_web' AND table_name='paper'")
#     labels = cursor.fetchall()
#     labels = [i[0] for i in labels]
#     # get 10 table content
#     cursor.execute('SELECT * FROM paper \
#                     ORDER BY RAND() \
#                     LIMIT 10')
#     content = cursor.fetchall()
#     return flask.render_template('/pages/page1.html', labels=labels, content=content)
#     # return flask.render_template('/pages/page1.html', content=content)

# @app.route('/pages/page2')
# def randomDisplay2():
#     '''Random display 10 papers'''
#     # get table colomn name
#     cursor.execute("SELECT column_name FROM information_schema.columns \
#                     WHERE TABLE_SCHEMA='ieei_web' AND table_name='paper'")
#     labels = cursor.fetchall()
#     labels = [i[0] for i in labels]
#     # get 10 table content
#     cursor.execute('SELECT * FROM paper \
#                     ORDER BY RAND() \
#                     LIMIT 10')
#     content = cursor.fetchall()
#     return flask.render_template('/pages/page2.html', labels=labels, content=content)
#     # return flask.render_template('/pages/page1.html', content=content)

@app.route('/pages/<page>')
def randomDisplay(page):
    '''Random display 10 papers'''
    # get table colomn name
    cursor.execute("SELECT column_name FROM information_schema.columns \
                    WHERE TABLE_SCHEMA='ieei_web' AND table_name='paper'")
    labels = cursor.fetchall()
    labels = [i[0] for i in labels]
    # get 10 table content
    cursor.execute('SELECT * FROM paper \
                    ORDER BY RAND() \
                    LIMIT 10')
    content = cursor.fetchall()
    # format data
    for i in content[3:5]:
        i = i.strip('[]').split(',')
        for j in i:
            j = j.strip('\"')
        i = '\n'.join(i)
        
    return flask.render_template('/pages/{}.html'.format(page), labels=labels, content=content)


if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)