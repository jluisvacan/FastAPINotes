#while
#ciclo recomendado que no sa sabe cuantas veces se itera
#mientras la condicion se cumpla el ciclo seguira iterando

condition = 10

while  condition > 0:
    print(condition)
    condition -= 1
#Cuando se ejecuta el bloque anterior se ejecuta el siguiente
else:
    print("Fin")


response = ''

while response.lower() != 'stop':
    response = input("Para salir escribir stop: ")
else:
    print("Fin")