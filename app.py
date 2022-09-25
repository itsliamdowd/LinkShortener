from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random

connection = sqlite3.connect('links.db', check_same_thread=False)
cursor = connection.cursor()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    link = request.form['url']
    if 'http' not in link:
        link = 'http://' + link
    randomnumber = random.randint(100000000000000, 999999999999999)

    cursor.execute('select * from links where number=?', (randomnumber,))
    if cursor.fetchone() is None:
        cursor.execute('insert into links (number,link) values (?,?)', (randomnumber, link))
        connection.commit()
        link = 'http://127.0.0.1:5000/' + str(randomnumber)
        return render_template('shortened.html', number=link)
    else:
        return redirect(url_for('index'))
        
@app.route('/<number>')
def redirect_to_link(number):
    cursor.execute('SELECT link FROM links WHERE number=?', (number,))
    link = cursor.fetchone()[0]
    return redirect(link)

if __name__ == '__main__':
    app.run(debug=True)
