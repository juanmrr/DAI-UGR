from random import randrange

aleatorio = randrange(100)

preguntar = True

while preguntar:
	entrada = int(input ("Introduzca un número: "))
	if entrada < aleatorio:
		print ("El número misterioso es mayor")
	elif entrada > aleatorio:
		print ("El número misterioso es menor")
	else:
		print ("Ha acertado el número misterioso!")
		preguntar = False
