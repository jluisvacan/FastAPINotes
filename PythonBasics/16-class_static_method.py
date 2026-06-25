#class method
#metodo que permite cambiar valores a nivel de clase, no de instancia

class Person:
    species = "Humano"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    #El decorador @classmethod convierte el metodo a un metodo de clase
    @classmethod
    def change_species(self, new_species):
        self.species = new_species

    #Static method
    #se puede accede a nivel de clase o a nivel de instnacia d eclase
    @staticmethod
    def is_older(age):
        return age >= 18


person1 = Person("Luis", 30)
person2 = Person("Jose", 22)

print(person1.species)
print(person2.species)

#invocando el metodo de clase
Person.change_species("Dolphin")
print(person1.species)
print(person2.species)

#invocando metodo estatico
print(Person.is_older(10))
print(person1.is_older(person1.age))