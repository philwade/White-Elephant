"""
    White Elephant
        A family present assignment program.
        Phil Wade (phil@philwade.org) 2011
"""

from flask import Flask, render_template, g, request, session, redirect, url_for
from sqlite3 import dbapi2 as sqlite3
app = Flask(__name__)

SECRET_KEY = "jazzamatazz"
DEBUG = True
if DEBUG:
    DATABASE = "family_debug.db"
else:
    DATABASE = "family.db"

app.debug = DEBUG
app.config.from_object(__name__)

def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()

@app.route("/")
def index():
    records = None
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        records = g.db.execute("select year.name, giver.name, receiver.name from match, year, user giver, user receiver \
                                where match.giver_id=? and giver.id=? and receiver.id=match.receiver_id and year.id=match.year_id order by year.id DESC", [session['id'], session['id']])
    return render_template('home.html', records = records)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        cur = g.db.execute('select * from user where email=? limit 1', [request.form['email']])
        result = cur.fetchone()
        if result != None:
            session['logged_in'] = True
            session['id'] = result[0]
            session['admin'] = result[3] == 1 or False
            return redirect(url_for('index'))
        else:
            error = "Unknown email"
    return render_template('login.html', error = error)

@app.route("/logout")
def logout():
    session.pop("logged_in", False)
    session.pop("admin", False)
    return render_template("loggedout.html")
    
if __name__ == "__main__":
    app.run()
