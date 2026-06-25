try:
    #con open se accede a un archivo
    #el modo escritura (w) crea el archivo en caso de no existir
    with open("test.txt", mode="w") as my_file:
        text = my_file.write(":) ")
    #modo de lectura (r)
    with open("test.txt", mode="r") as my_file:
        print(my_file.readlines())

    #modo de leer y escribir r+
    with open("test.txt", mode="r+") as my_file:
        print(my_file.readlines())
        text = my_file.write("Hola archivo ")

    #el modo append (a) agrega texto al final
    with open("test.txt", mode="a") as my_file:
        text = my_file.write("123 ")
        print(text)


except FileNotFoundError:
    print("Archivo no encontrado.")
except Exception as error:
    print(f"Ocurrio un error: {error}.")