#decoradores
#Agrega funcionalidades a una funcion

def require_auth(func):
    def wrapper(user):
        if user.lower() == "admin":
            return func(user)
        else:
            return "Acceso denegado"

    return wrapper

#Al agregar la etiqueta la funcion se encapsula y se crea un decorador
@require_auth
def admin_dashboard(user):
    return f"Bienvenido al panel, {user}"


print(admin_dashboard("Admin"))
print(admin_dashboard("Invitado"))
