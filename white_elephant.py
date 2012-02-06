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

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/years", methods=["GET", "POST"])
def yearList():
    error = None
    if not session.get('logged_in') and session.get('admin'):
        abort(404)
    years = g.db.execute('select * from year order by id desc')
    return render_template('years.html', error = error, years = years)

@app.route("/users", methods=["GET", "POST"])
def userList():
    error = None
    if not session.get('logged_in') and session.get('admin'):
        abort(404)
    if request.method == "POST":
        new_user = request.form['user_name']
        user_family = request.form['user_family']
        user_email = request.form['user_email']
        if new_user:
            g.db.execute('insert into user values(null, ?, ?, 0, ?)', [new_user, user_email, user_family])
            g.db.commit()
    users = g.db.execute('select user.name, family.name from user, family where user.family_id=family.id order by user.id desc')
    families = g.db.execute('select family.name, family.id from family')
    return render_template('users.html', error = error, users = users, families = families)

@app.route("/picks", methods=["GET", "POST"])
def runPicks():
    error = None
    if not session.get('logged_in') and session.get('admin'):
        abort(404)
    return render_template('picks.html', error = error)

@app.route("/families", methods=["GET", "POST"])
def familyList():
    error = None
    if not session.get('logged_in') and session.get('admin'):
        abort(404)
    if request.method == "POST":
        new_name = request.form['family_name']
        if new_name:
            g.db.execute('insert into family values(null, ?)', [new_name])
            g.db.commit()
    families = g.db.execute('select * from family order by id desc')
    return render_template('families.html', error = error, families = families)

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
