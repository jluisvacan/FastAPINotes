#funciones
#las funciones se definen con def
#parametros son los que nesita la funcion y se definen al crear la funcino
def hello(great, name="Luis"):
    print(f"{great}, {name}")

#argumentos son los parametros necesarios al invocar la funcion
hello("Hola", "Luis")
#No es obligatorio el parametro por defecto para invocar la funcion
hello("Adios")

# args define multiples los valores
# kwargs define multiples parametros en la funcion
def big_function(*args, **kwargs):
    print(f"{args}")
    print(f"{kwargs}")

big_function(1,2,3,4,5,6,7, num1=1, num2=2, num3=3, num4=4, num5=5)