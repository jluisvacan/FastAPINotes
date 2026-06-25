#Atributos y metodos protegidos y privados

class Person:

    #atributo de clase
    species = "Humano"

    #Constructor
    def __init__(self, name, age):
        self.name = name
        self.age = age

        #dato protegido por convencion
        self._energy = 90

        #dato privado
        self.__pasword = "abc123"

    def work(self):
        return f"{self.name} esta trabajando"

    #metodo protegido por convencion
    def _waster_energy(self, quantity):
        self._energy -= quantity
        return self._energy

    #metodo privado
    def __generate_password(self):
        return f"$${self.name}{self.age}"

#instancia de la clase
persona1 = Person("Luis", 30)
print(persona1.name)
#se logra acceder a un metodo protegido
print(persona1._waster_energy(10))
#se accede a un atributo privado
print(persona1._Person__pasword)
#se invoca metodo privado
print(persona1._Person__generate_password())
print(persona1.work())