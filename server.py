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
        paperid = flask.request.form['searchField']
    else:
        paperid = flask.request.args.get('searchField','')

    # if user hasn't input paper id, return blank table
    if len(paperid) < 1 : 
        return flask.render_template('/pages/page3.html', flag=False, alert=False)
    # if the paperid is illegal, raise alert
    if (not paperid.isdigit()) or int(paperid) > 9999:
        return flask.render_template('/pages/page3.html', flag=False, alert = True)

    # get table colomn name
    cursor.execute("SELECT column_name FROM information_schema.columns \
                    WHERE TABLE_SCHEMA='ieei_web' AND table_name='paper'")
    labels = cursor.fetchall()
    labels = [i[0] for i in labels]
    # get table content by id
    cursor.execute('SELECT * FROM paper \
                    WHERE paper_id={}'.format(paperid))
    content = cursor.fetchall()

    # format data
    content = list(content)
    for h in range(len(content)):
        content[h] = list(content[h])
        for i in range(3, 5):
            content[h][i] = content[h][i].strip('[]').split(', ')
            for j in range(len(content[h][i])):
                content[h][i][j] = content[h][i][j].strip('"')
            content[h][i] = '\n'.join(content[h][i])
    return flask.render_template('/pages/page3.html', flag=True, labels=labels, content=content, alert=False)


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
    content = list(cursor.fetchall())
    # format data
    for h in range(len(content)):
        content[h] = list(content[h])
        for i in range(3, 5):
            content[h][i] = content[h][i].strip('[]').split(', ')
            for j in range(len(content[h][i])):
                content[h][i][j] = content[h][i][j].strip('"')
            content[h][i] = '\n'.join(content[h][i])
        
    return flask.render_template('/pages/{}.html'.format(page), labels=labels, content=content)


if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)