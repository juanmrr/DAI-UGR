#./flask/app.py

from flask import (
    render_template, url_for
)

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/images')
def images():
	return render_template('./images.html')

@app.route('/user/juanma')
def userJuanma():
	return 'Hola Juanma!'

@app.route("/user/<usuario>")
def users(usuario):
    return "Hola  %s" %usuario

@app.errorhandler(404)
def page_not_found(error):
    return "Oups, algo ha ocurrido! :(", 404