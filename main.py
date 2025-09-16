# Representación de los pisos con una lista de diccionarios para tener la info de cada piso ya que es distinto uno de otro

# Cada número representa el estado del lugar:
#   0 -> libre
#   1 -> ocupado
pisos = [
    {
        "nombre": "Piso 10 - Espacio Panorámico",
        "tipo": "grupal o individual",
        "lugar grupal": [0, 1, 0, 0, 0, 0, 1], 
        "lugar individual": [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        "descripcion": "El lugar más grande de UADE, con mesas y sillones cómodos, enchufes y pizarras para estudiar solo o en grupo."
    },
    {
        "nombre": "Chile 2 - Espacio Silencioso",
        "tipo": "silencio / conversación baja",
        "lugar silencio": [0, 0, 0, 0],           
        "lugar conversacion baja": [1, 0, 0, 0],  
        "descripcion": "Un espacio reducido, dividido en dos sectores: uno en silencio total y otro donde se puede hablar bajito."
    },
    {
        "nombre": "UADE Labs - Espacio Tech",
        "tipo": "computadora disponible",
        "lugares con computadora": [0, 0, 1, 0],
        "descripcion": "Un espacio chico con computadoras disponibles y salones equipados para trabajo práctico."
    }
]


# Diccionario para traducir los números en palabras
estados = {0: "libre", 1:"ocupado"}   


""" ---------FUNCIONES--------- """


# 1) Función que muestra la disponibilidad total en todos los pisos
def consultaTotal(pisos):
    for piso in pisos:                                         # Recorremos cada piso
        total_libres = 0                                       # Contador de lugares libres
        
        # Lista de claves que contienen lugares (cada piso puede tener distintas) para no hacer un if eterno
        claves_lugares = ["lugar grupal", "lugar individual", "lugar silencio", 
                        "lugar conversacion baja", "lugares con computadora"]
        
        # Recorremos solo las claves que existen en el piso
        for clave in claves_lugares:
            if clave in piso:                                   # Verificamos que la clave exista
                for lugar in piso[clave]:                       # Recorremos cada lugar
                    if lugar == 0:                              # Si el lugar está libre
                        total_libres += 1                       # Sumamos 1 al total
        
        print(f"En {piso['nombre']}: hay {total_libres} lugares disponibles")  # Mostramos total



# 2) Función que muestra el estado de cada lugar en un piso elegido
def consultarDisponibilidad(pisos, piso_num):
    if piso_num < 0 or piso_num >= len(pisos):                          # Validamos que el piso exista
        print("El número de piso ingresado no es válido. Ingresá otro...")
        return

    piso = pisos[piso_num]                                              # Obtenemos el diccionario del piso
    print(f"\n{piso['nombre']}")                                        # Mostramos el nombre del piso

    # Lista de posibles claves que contienen lugares
    claves_lugares = ["lugar grupal", "lugar individual", "lugar silencio", 
                    "lugar conversacion baja", "lugares con computadora"]

    # Recorremos solo las claves que existen en este piso
    for clave in claves_lugares:
        if clave in piso:                                               # Verificamos que exista
            print(f"\nTipo: {clave}")                                   # Mostramos el tipo de lugar
            lugares = piso[clave]                                       # Lista de lugares para ese tipo

            for i in range(len(lugares)):                               # Recorremos cada lugar
                estado = "libre" if lugares[i] == 0 else "ocupado"      # Determinamos el estado con comprension
                print(f"Lugar {i + 1}: {estado}")                       # Mostramos el lugar y su estado



# 3) Función para mostrar todos los lugares libres de todos los pisos
def verLugaresLibres(pisos):
    for piso in pisos:                                          # Recorremos cada piso
        print(f"\n{piso['nombre']}")                            # Mostramos nombre del piso

        claves_lugares = ["lugar grupal", "lugar individual", "lugar silencio",
                        "lugar conversacion baja", "lugares con computadora"]

        for clave in claves_lugares:
            if clave in piso:                                   # Verificamos existencia
                libres = []                                     # Lista para los lugares libres
                for i in range(len(piso[clave])):               # Iteramos por índice
                    if piso[clave][i] == 0:
                        libres.append(i + 1)                    # Guardamos los lugares libres
                
                print(f"\nTipo: {clave}")                       # Mostramos tipo de lugar
                if libres:
                    for j in range(0, len(libres), 5):          # Mostramos de a 5 (avanza de 5 en 5, así que si hay muchos
                        for lugar in libres[j:j+5]:             # lugares libres, no imprime una línea larguísima)
                            print(lugar, end="  ")
                    print()
                else:
                    print("No hay lugares libres en este tipo")

# 4) Función para reservar un lugar
def reservarLugar(pisos, piso_num, tipo, lugar_num):
    if piso_num < 0 or piso_num >= len(pisos):    # Validamos piso
        print("El número de piso ingresado no es válido.")
        return
    
    piso = pisos[piso_num]                       # Obtenemos el piso
    if tipo not in piso:                         # Validamos tipo de lugar
        print("Ese tipo de lugar no existe en este piso.")
        return
    
    lugares = piso[tipo]                         # Obtenemos la lista de lugares
    if lugar_num < 1 or lugar_num > len(lugares):
        print("El número de lugar no es válido.")
        return

    if lugares[lugar_num - 1] == 0:              # Verificamos si está libre
        lugares[lugar_num - 1] = 1               # Lo reservamos (cambiamos a 1)
        print(f"¡El lugar {lugar_num} en {piso['nombre']} fue reservado con éxito!")
    else:
        print(f"El lugar {lugar_num} ya está ocupado.")

# 5) Función para liberar un lugar
def liberarLugar(pisos, piso_num, tipo, lugar_num):
    if piso_num < 0 or piso_num >= len(pisos):   # Validamos piso
        print("El número de piso ingresado no es válido.")
        return
    
    piso = pisos[piso_num]                      # Obtenemos el piso
    if tipo not in piso:                        # Validamos tipo de lugar
        print("Ese tipo de lugar no existe en este piso.")
        return
    
    lugares = piso[tipo]
    if lugar_num < 1 or lugar_num > len(lugares):
        print("El número de lugar no es válido.")
        return

    if lugares[lugar_num - 1] == 1:             # Verificamos si está ocupado
        lugares[lugar_num - 1] = 0              # Lo liberamos (cambiamos a 0)
        print(f"¡El lugar {lugar_num} en {piso['nombre']} fue liberado con éxito!")
    else:
        print(f"El lugar {lugar_num} ya estaba libre.")

""" ---------MENÚ PRINCIPAL--------- """
# Es el primer menú que ve el usuario, permite entrar a submenús o salir
def menuPrincipal(pisos):
    while True:                             # bucle hasta que elija salir
                # MENSAJE DE BIENVENIDA
        print("-------------------------------------------------------------------")
        print("\n¡Bienvenido/a a UADE Desk Finder!\n")
        print("Acá podés consultar la disponibilidad de los espacios de estudio en la facu,")
        print("ver los lugares libres y conocer las características de cada piso.\n")
        print("¡Elegí lo que necesites y encontrá tu lugar ideal para estudiar!\n")
        print("-------------------------------------------------------------------")
        
        print("\n       Menú Principal      ")
        print("1. Informacion sobre los espacios")
        print("2. Consultar disponibilidad")
        print("3. Reservar")
        print("4. Liberar")
        print("0. Salir")
        
        opcion = input("\n ✶ Elegí una opción: ").strip()
        
        if opcion == "1":                    #si elige informacion
            submenuInformacion()            # vamos al submenú de info de pisos
        elif opcion == "2":                 # si elige consultar
            submenuConsultas(pisos)         # vamos al submenú de consultas
        elif opcion == "3":   # Reservar
            # Mostramos al usuario la lista de pisos disponibles
            print("\nPisos disponibles:")
            
            # Usamos un bucle for para recorrer la lista de pisos y mostrarlos con un número
            for i in range(len(pisos)):
                # Mostramos el número de piso (i+1 porque los índices arrancan en 0) y el nombre del piso
                print(f"{i + 1}. {pisos[i]['nombre']}")
            
            # Le pedimos al usuario que ingrese el número del piso en el que quiere reservar
            # Restamos 1 para convertirlo al índice correcto de la lista (porque el usuario empieza a contar desde 1)
            piso = int(input("\n ✶ Ingresá el número del piso: ")) - 1
            
            # Pedimos al usuario el tipo de lugar (ej: "lugar grupal", "lugar individual", etc.)
            # .strip() elimina espacios extras y .lower() pasa el texto a minúsculas para evitar errores
            tipo = input(" ✶ Ingresá el tipo de lugar (ej: lugar grupal, lugar individual, lugar silencio, etc.): ").strip().lower()
            
            # Pedimos al usuario el número de lugar específico dentro del piso
            lugar = int(input(" ✶ Ingresá el número del lugar: "))
            
            # Llamamos a la función reservarLugar() pasando:
            # - la lista de pisos completa
            # - el piso elegido (como índice)
            # - el tipo de lugar
            # - y el número del lugar
            reservarLugar(pisos, piso, tipo, lugar)


        elif opcion == "4":   # Liberar
            # Mostramos al usuario la lista de pisos disponibles
            print("\nPisos disponibles:")
            
            # Usamos un bucle for para recorrer la lista de pisos y mostrarlos con un número
            for i in range(len(pisos)):
                # Mostramos el número de piso (i+1 porque los índices arrancan en 0) y el nombre del piso
                print(f"{i + 1}. {pisos[i]['nombre']}")
            
            # Le pedimos al usuario que ingrese el número del piso en el que quiere liberar un lugar
            # Restamos 1 para convertirlo al índice correcto de la lista
            piso = int(input("\n ✶ Ingresá el número del piso: ")) - 1
            
            # Pedimos al usuario el tipo de lugar (ej: "lugar grupal", "lugar individual", etc.)
            # Usamos .strip() y .lower() para evitar errores de espacios o mayúsculas
            tipo = input(" ✶ Ingresá el tipo de lugar (ej: lugar grupal, lugar individual, lugar silencio, etc.): ").strip().lower()
            
            # Pedimos al usuario el número de lugar específico dentro del piso
            lugar = int(input(" ✶ Ingresá el número del lugar: "))
            
            # Llamamos a la función liberarLugar() pasando:
            # - la lista de pisos completa
            # - el piso elegido (como índice)
            # - el tipo de lugar
            # - y el número del lugar
            liberarLugar(pisos, piso, tipo, lugar)

        elif opcion == "0":                 # si elige salir
            print("\nGracias por usar nuestra app")
            print("¡Hasta pronto!")
            print("\nSaliendo...")
            break                           # rompemos el bucle
        else:                               # si pone cualquier otra cosa
            print("Opción inválida, ingresá de nuevo.")


""" ---------SUBMENÚ DE INFORMACION DE PISOS--------- """
def submenuInformacion():
    while True:
        print("\n      Información de los espacios de estudio      ")
        print("1. Espacio Panorámico")
        print("2. Espacio Silencioso")
        print("3. Espacio Tech")
        print("0. Volver al menú principal")
        
        opcion = input("\n ✶ Sobre qué piso querés conocer: ").strip()
        
        if opcion == "1":
            print("\n-------------------------------------------------------------------")
            print("\nEspacio Panorámico (Piso 10)\n\nEl lugar más grande de UADE, con mesas y sillones cómodos, enchufes y pizarras con fibrones para organizar ideas. Si buscás un espacio amplio y flexible, este piso es una gran opción para estudiar solo o en grupo.")
            print("\n-------------------------------------------------------------------")
        elif opcion == "2":                 
            print("\n-------------------------------------------------------------------")
            print("\nEspacio Silencioso (Chile 2)\n\nUn ambiente más reducido y dividido en dos sectores: uno de silencio total y otro donde se puede conversar bajito. Ideal si querés concentrarte o si preferís un lugar más tranquilo con pocos compañeros.")
            print("\n-------------------------------------------------------------------")
        elif opcion == "3":                 
            print("\n-------------------------------------------------------------------")
            print("\nEspacio Tech (UADE Labs)\n\nUn espacio más chico, pero con la ventaja de reservar computadoras y usar los salones equipados. Perfecto si necesitás trabajar con software específico o armar algo práctico en equipo.")
            print("\n-------------------------------------------------------------------")
        elif opcion == "0":                 # si elige volver
            print("\nVolviendo al menú principal...")
            break
        else:                               # si pone cualquier otra cosa
            print("Opción inválida, ingresá de nuevo.")
            continue
        
        # Pregunta si quiere conocer otro piso
        while True:
            otra = input("\n¿Querés conocer otro espacio? (s/n): ").strip().lower()
            if otra == "s":                     # vuelve al inicio del submenu
                break                           # rompe el bucle de validación y repite el submenu
            elif otra == "n":                   # sale al menú principal
                print("\nVolviendo al menú principal...")
                return                         # rompe toda la función
            else:
                print("Opción inválida, ingresá 's' o 'n'.")


""" ---------SUBMENÚ DE CONSULTAS--------- """
# Muestra opciones específicas relacionadas con consultas
def submenuConsultas(pisos):
    while True:                                                  # bucle hasta volver al principal
        print("\n      Submenú de consulta de pisos      ")
        print("1. Consultar disponibilidad total de UADE")
        print("2. Consultar disponibilidad de un piso")
        print("3. Consultar lugares libres")
        print("0. Volver al menú principal")
        
        opcion = input("\n ✶ Elegí una opción: ").strip()
        
        if opcion == "1":                                       # muestra disponibilidad total
            print("\n-------------------------------------------------------------------")
            consultaTotal(pisos)
            print("-------------------------------------------------------------------")

        elif opcion == "2":                                     # muestra disponibilidad de un piso
            while True:
                print("\nPisos disponibles:")
                for i in range(len(pisos)):
                    print(f"{i + 1}. {pisos[i]['nombre']}")  # mostramos número y nombre del piso
        
                piso = int(input("\n ✶ Ingresá el número del piso que querés consultar: ")) - 1  # restamos 1 para usar el índice
                print("-------------------------------------------------------------------")
                consultarDisponibilidad(pisos, piso)            # llamamos a la función con el índice correcto
                print("-------------------------------------------------------------------")
            
                # Pregunta si quiere conocer otro piso
                while True:
                    otra = input("\n¿Querés conocer la disponibilidad de otro piso? (s/n): ").strip().lower()
                    if otra == "s":                     # vuelve al inicio del submenu
                        break                           # rompe el bucle de validación y repite el submenu
                    elif otra == "n":                   # sale al menú principal
                        print("\nVolviendo al menú principal...")
                        return                         # rompe toda la función
                    else:
                        print("Opción inválida, ingresá 's' o 'n'.")
            
        elif opcion == "3":                                     # muestra lugares libres
            while True:
                print("\nPisos disponibles:")
                for i in range(len(pisos)):
                    print(f"{i + 1}. {pisos[i]['nombre']}")     # mostramos número y nombre del piso
        
                piso = int(input("\nIngresá el número del piso que querés consultar: ")) - 1  # restamos 1 para usar el índice
                print("-------------------------------------------------------------------")
                verLugaresLibres([pisos[piso]])                 # llamamos a la función con piso
                print("-------------------------------------------------------------------")
            
                # Pregunta si quiere conocer otro piso
                while True:
                    otra = input("\n¿Querés ver los lugares libres de otro piso? (s/n): ").strip().lower()
                    if otra == "s":                             # vuelve al inicio del submenu
                        break                                   # rompe el bucle de validación y repite el submenu
                    elif otra == "n":                           # sale al menú principal
                        print("\nVolviendo al menú principal...")
                        return                                  # rompe toda la función
                    else:
                        print("Opción inválida, ingresá 's' o 'n'.")
        
        elif opcion == "0":                                     # vuelve al menú principal
            print("\nVolviendo al menú principal...")
            break
        else:                                                   # controla errores de input
            print("Opción inválida, ingresá de nuevo.")


# Punto de entrada del programa -> ejecuta el menú principal
menuPrincipal(pisos)
