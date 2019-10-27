#./flask/app.py

from flask import (
    render_template, url_for, send_file, request
)

from flask import Flask
app = Flask(__name__)

from PIL import Image

import time

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

@app.route('/mandelbrot')
def pintaMandelbrot():
	try:
		xa = float(request.args.get('x1'))
		xb = float(request.args.get('x2'))
		ya = float(request.args.get('y1'))
		yb = float(request.args.get('y2'))
		maxIt = int(request.args.get('iteraciones'))
		imgx = int(request.args.get('ancho'))
		imgy = int(abs (yb - ya) * imgx / abs(xb - xa));
		
		im = Image.new('RGB', (imgx, imgy), color = 'black')
  
		for y in range(imgy):
			zy = y * (yb - ya) / (imgy - 1) + ya
	    
			for x in range(imgx):
				zx = x * (xb - xa) / (imgx - 1) + xa
				z = zx + zy * 1j
				c = z
	      
				for i in range(maxIt):
					if abs(z) > 2.0: break 
					z = z * z + c
	        
				i = maxIt - i
	      
				col = (i%10*25, i%16*16, i%8*32)
	        
				im.putpixel((x, y), col)

		im.save('static/images/mandelbrot.png')

		return send_file("static/images/mandelbrot.png", mimetype='image/png')

	except:
		return render_template('./mandelbrot.html')