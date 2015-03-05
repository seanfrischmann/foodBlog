# ===========================================================================
# +++flaskr.py+++|
# _______________|
#
# Sean Frischmann
# Flaskr -- Blog App
# ===========================================================================

# Imports
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
		abort, render_template, flash

# Configuration
DATABASE = 'app/food.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#create app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/desserts')
def show_desserts():
	cur = g.db.execute('select title, ingredients, review from entries order by id desc')
	entries = [dict(title=row[0], ingredients=row[1], review=row[2]) for row in cur.fetchall()]
	i = 0
	while i < len(entries):
		ingredients = entries[i]['ingredients'].split('\r\n')
		temp=''
		for x in ingredients:
			temp = temp+' '+'<li class="ing">'+x
		entries[i]['ingredients'] = temp
		i += 1
	return render_template('show_desserts.html', entries=entries)

'''
@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST' and 'photo' in request.files:
		filename = photos.save(request.files['photo'])
		rec = Photo(filename=filename, user=g.user.id)
		rec.store()
		flash("Photo saved.")
		return redirect(url_for('show', id=rec.id))
	return render_template('upload.html')

@app.route('/photo/<id>')
def show(id):
	photo = Photo.load(id)
	if photo is None:
		abort(404)
	url = photos.url(photo.filename)
	return render_template('show.html', url=url, photo=photo)
'''

@app.route('/add_dessert', methods=['POST'])
def add_dessert():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into entries (title, ingredients, review) values (?,?,?)', 
			[request.form['title'], request.form['ingredients'], request.form['review']])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_desserts'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('index'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('You were logged out')
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run()
'''
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello!"

if __name__ == "__main__":
    app.run()
'''
