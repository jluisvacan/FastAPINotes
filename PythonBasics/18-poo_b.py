#Clase abstracta

from abc import ABC, abstractmethod

class BankAccount(ABC): #Herencia
#la clase hereda los atributos y metodos de ABC
    #Constructor
    def __init__(self, owner, initial_balance):
        self.__balance = initial_balance    #Encapsulacion
        # Proteger los datos que no se deseen que se accedan

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def _get_balance(self):
        return self.__balance

    def _set_balance(self, new_balance):
        self.__balance = new_balance

    @abstractmethod
    def withdraw(self, amount):
        pass        #polimorfismo
    # las clases que hereden de BankAccount si o si apliquen el withdraw


    def check_balance(self):
        return f"Saldo actual: ${self.__balance}"


class SavingAccount(BankAccount):   #Herencia

    def withdraw(self, amount):
        penalty = amount * 0.05
        total = amount + penalty
        if total <= self._get_balance():
            self._set_balance(self._get_balance() - total)
        else:
            print("Fondos insuficientes en la cuenta de ahorro")


class PayrollAccount(BankAccount):   #Herencia

    def withdraw(self, amount):
        if amount <= self._get_balance():
            self._set_balance(self._get_balance() - amount)
        else:
            print("Fondos insuficientes en la cuenta de nomina")


savings = SavingAccount(owner="Luis", initial_balance=100)
payroll = PayrollAccount(owner="Jose", initial_balance=200)

savings.withdraw(10)
payroll.withdraw(5)

print("Cuenta de ahorro: $", savings.check_balance())
print("Cuenta de nomina: $", payroll.check_balance())