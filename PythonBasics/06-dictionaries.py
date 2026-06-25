#Diccionarios
#Son estructuras de datos llave-valor, no ordenados.
#Son mutables, es posible cambiar el valor mediante la llave

user = {

    # llave -  valor
    "name": "Luis",
    "age": 29,
    "active": False,
    (10.82, -90.01) : "Guanajuato"
}
print(user)

#Cambia el valor mediante la llave
user["name"] = "Jose"
print(user)

#Se agrega un nuevo campo llave-valor
user["country"] = "Mexico"
print(user)

#metodos

#items
#accede a todos los elementos del diccionario
print(user.items())

#values
#accede a los valores del diccionario
print(user.values())

#keys
#accede a las llaves del diccionario
print(user.keys())
