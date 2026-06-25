#las listas son colecciones ordenadas, cuentan con un indice empezando con el indice 0
list_numbers = [1, 2, 3, 4, 5]
list_letters = ["a", "b", "c", "d", "e"]
list_mix = [1, "a", [1.5, 2.5, 3.5], True, 90]


print(list_numbers)
print(type(list_letters))
print(list_mix[0])


#metodos de listas

#append
#agrega un valor a la lista y lo agrega al final
list_numbers.append(100)
print(list_numbers)

#remove
#elimina el valor indicado de la lista
list_numbers.remove(1)
print(list_numbers)

#count
# contar cuantas veces aparece un valor en la lista
print(list_numbers.count(100))
