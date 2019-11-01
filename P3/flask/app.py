from flask import request
from flask import Response
from flask import Flask, render_template 
from flask import session
from pickleshare import *
import math

app = Flask(__name__)
app.secret_key='Clave de sesión'

nPaginas = 0

def addPage(page):
	global nPaginas
    
	if(nPaginas < 3):
		nPaginas = nPaginas + 1

	historial = [0]*(nPaginas + 1)
	if(nPaginas > 1):
		for i in range(nPaginas-1, 0, -1):
			aux1 = "histo" + str(i - 1)
			aux2 = "histo" + str(i)
			session[aux2] = session[aux1] 
			historial[i] = session[aux2]
			print(session[aux2])

	session["histo0"] = page
	historial[0] = page

	return historial

def showPage(page):
	if 'username' in session:
		user=session['username']
		historial =  addPage(page)
		return render_template(page, user = user, historial = historial)
	else :
		return render_template(page)

@app.route("/surfbase.html")
@app.route("/surfbase")
def surfbase():
    return showPage("surfbase.html")

@app.route("/newsblog.html")
@app.route("/newsblog")
def newsblog():
    return showPage("newsblog.html")

@app.route("/about.html")
@app.route("/about")
def about():
    return showPage("about.html")

@app.route("/index.html")
@app.route("/index")
@app.route("/")
def index():
	return showPage('index.html')

@app.route("/login", methods = ['POST','GET'])
def login():
	if request.method == 'POST':
		user = request.form['user']
		password = request.form['pass']
		db = PickleShareDB('miBD')
        
		if db[user] and password == db[user]["passw"]: 
			session['username']= user
			return render_template("index.html", user = user)
		else:
			return render_template('index.html', error = "Contraseña incorrecta")

	else:
		if 'username' in session:
			username=session['username']
            
			return render_template('index.html', user = username)
		else:
			return render_template('index.html')

def index():
    return showPage("index.html")

@app.route('/registrar.html', methods = ['POST','GET'])
@app.route('/registrar', methods = ['POST','GET'])
def register():
	try:
		if request.method == 'POST':
			user = request.form['user']
			password = request.form['pass']
		        
			db = PickleShareDB('miBD')
			db[user] = {'passw': password}

		return render_template('index.html', user = user)

	except:
		return showPage('registrar.html')


@app.route('/logout.html')
@app.route('/logout')
def logout():
	historial =  addPage("logout")
    
	session.pop('username', None)
	global nPaginas
	if(nPaginas > 0):
		for i in range(0, nPaginas+1):
			aux = "histo" + str(i)
			session.pop(aux, None)

	nPaginas = 0; 
	return render_template("logout.html")

@app.route('/usuario.html', methods = ['POST','GET'])
@app.route('/usuario', methods = ['POST','GET'])
def usuario():
	datos = []
	historial = addPage("usuario.html")
	if request.method == 'POST':
		user = request.form['user']
		password = request.form['pass']
		        
		db = PickleShareDB('miBD')
		db[user] = {'passw': password}

		datos.append(user)
		datos.append(db[user]["passw"])

		return render_template("usuario.html", user = user, historial = historial, datos = datos)
	else:
		if 'username' in session:
			user = session['username']
			db = PickleShareDB('miBD')
			datos.append(user)
			datos.append(db[user]["passw"])

			return render_template("usuario.html", user = user, historial = historial, datos = datos)
		else: 
			return redirect(redirect('index'))