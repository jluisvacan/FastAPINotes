from itertools import count

#tuplas
#Son colecciones ordenados, por lo que inicia desde el indice 0
#Son inmutables, una vez creadas no se pueden modificar

tuple_letters = ("a", "b", "c", "d")
tuple_numbers = (1, 2, 3, 4)
tuple_mix = (1, "b", 9.8, (1 ,2, 3), False)

#count
#Cuenta cuantas veces se repite el valor indicado
print(tuple_letters.count("a"))

#index
#trae el indice del valor indicado
print(tuple_numbers.index(2))

#Las tuplas son inmutables
print(tuple_mix)
tuple_mix[1] = 2 #Error

