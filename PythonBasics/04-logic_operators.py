
#and
#Todo lo que se evalua tiene que ser verdadero

age = 29
licenced = True

if age >= 18 and licenced:
    print("Puede manejar")


#or
#Si una de las condiciones es verdadero se ejecuta el bloque de codigo
is_student = False
membership = True

if membership or is_student:
    print("Puede entrar")

#not
#invierte el valor booleano siguiente

is_admin = False
if not is_admin:
    print("Acceso denegado")

# short circuiting
# Si no se envia un nombre o valor, se convierte toda la sentencia en False
name = False
# Al encontrar el primer False en a sentencia se corta y se obtiene un False
print(name and name.upper())