from flask import request
from flask import Response
from flask import Flask, render_template 
from flask import session
from pickleshare import *
import math
from pymongo import MongoClient

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

	session["histo0"] = page
	historial[0] = page

	return historial

def showPage(page):
	if 'username' in session:
		user = session['username']
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
			return render_template("index.html")


# PRACTICA 4

@app.route('/mongo.html', methods = ['POST', 'GET'])
@app.route('/mongo', methods = ['POST', 'GET'])
def mongo():
	return showPage('mongo.html')

@app.route('/busqueda.html', methods = ['POST', 'GET'])
@app.route('/busqueda', methods = ['POST', 'GET'])
def busqueda():

	client = MongoClient("mongo", 27017)
	db = client.SampleCollections

	if request.method == 'POST':
		nombre = request.form['nombre']

		val = db.samples_pokemon.find({"name" : {"$regex" : nombre}})

		return render_template("busqueda.html", busqueda = val)
	else:
		return render_template("busqueda.html")

@app.route('/delete.html', methods = ['POST', 'GET'])
@app.route('/delete', methods = ['POST', 'GET'])
def delete():

	client = MongoClient("mongo", 27017)
	db = client.SampleCollections

	if request.method == 'POST':
		nombre = request.form['delete']

		if db.samples_pokemon.remove({"name" : nombre}):
			eliminado = "El elemento ha sido eliminado con éxito"

		return render_template("delete.html", eliminar = eliminado)
	else:
		return render_template("delete.html")

		
		#elif request.form['peso']:
		#	peso = request.form['peso']
		#	nombre = request.form['name']

		#	if db.samples_pokemon.update({"name" : nombre}, {$set : {"weight" : peso}}):
		#		modificado = "Ha sido modificado con éxito"

		#	return render_template('mongo.html', modificar = modificado)