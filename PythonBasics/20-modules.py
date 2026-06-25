#modulo
#es un archivo de python, puede utilizarse los funciones y atributos de ese archivo
import math_util

#paquete
#un paquete es una carpeta que tiene modulos
from my_package import messages


#es posible guardar una funcion de un modulo en una variable
#guardando en cache la funcion
result = math_util.addition(3,4)

print(result)
print(messages.greet("Luis"))
print(messages.bye("Luis"))