#POO
# Paradigma de programacion que modela los elementos del mundo real como objetos

#clase
# SE define con la palabra reservada class

class Person:
    #Constructor
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def work(self):
        return f"{self.name} esta trabajando"

#instancia de la clase
persona1 = Person("Luis", 30)
print(persona1.name)
print(persona1.work())