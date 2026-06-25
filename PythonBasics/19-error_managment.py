# try-except

def divide_numbers():

#try-except se utiliza para manejar errores esperados
    try:
        a = int(input("Ingresa el numerador: "))
        b = int(input("Ingresa el denominador: "))
        result = a / b
    except ZeroDivisionError:
        print("No se puede dividir entre 0")
    except ValueError:
        print("Ingresa un numero por favor")
    except Exception as error:
        print(type(error))
    # en dado caso de que no pase un error se ejecuta el else
    else:
        print(result)
        return result
    #el finally siempre se ejecuta, con error o sin error
    finally:
        print("Nos vemos luego")


divide_numbers()