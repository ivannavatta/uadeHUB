# Representación de los pisos con una lista de diccionarios para tener la info de cada piso ya que es distinto uno de otro

# Cada número representa el estado del lugar:
#   0 -> libre
#   1 -> ocupado
pisos = [
    {
        "nombre": "Piso 10 - Espacio Panorámico",
        "tipo": "grupal o individual",
        "lugar grupal": [
            {"estado": 0, "enchufe": True, "pizarron":True, "tipo": "grupal", "usuario": None},
            {"estado": 1, "enchufe": True, "pizarron":True, "tipo": "grupal", "usuario": "Jorge"},
            {"estado": 0, "enchufe": True, "pizarron":True, "tipo": "grupal", "usuario": None},
            {"estado": 0, "enchufe": True, "pizarron":False, "tipo": "grupal", "usuario": None},
            {"estado": 0, "enchufe": True, "pizarron":True, "tipo": "grupal", "usuario": None},
            {"estado": 1, "enchufe": True, "pizarron":False, "tipo": "grupal", "usuario": "Santiago"},
            {"estado": 0, "enchufe": True, "pizarron":True, "tipo": "grupal", "usuario": None},
        ], 
        "lugar individual": [
            {"estado": 0, "enchufe": True, "tipo": "individual", "usuario": None},
            {"estado": 1, "enchufe": False, "tipo": "individual", "usuario": "Juan"},
            {"estado": 0, "enchufe": True, "tipo": "individual", "usuario": None},
            {"estado": 0, "enchufe": True, "tipo": "individual", "usuario": None},
            {"estado": 0, "enchufe": False, "tipo": "individual", "usuario": None},
            {"estado": 0, "enchufe": True, "tipo": "individual", "usuario": None},
            {"estado": 1, "enchufe": True, "tipo": "individual", "usuario": "Luis"},
            {"estado": 0, "enchufe": True, "tipo": "individual", "usuario": None},
            {"estado": 0, "enchufe": False, "tipo": "individual", "usuario": None},
            {"estado": 0, "enchufe": True, "tipo": "individual", "usuario": None}
        ],
        "descripcion": "El lugar más grande de UADE, con mesas y sillones cómodos, enchufes y pizarras para estudiar solo o en grupo."
    },
    {
        "nombre": "Chile 2 - Espacio Silencioso",
        "tipo": "silencio / conversación baja",
        "lugar silencio": [
            {"estado": 0, "enchufe": True, "tipo": "silencio", "usuario": None},
            {"estado": 0, "enchufe": True, "tipo": "silencio", "usuario": None},
            {"estado": 0, "enchufe": False, "tipo": "silencio", "usuario": None},
            {"estado": 0, "enchufe": True, "tipo": "silencio", "usuario": None}
        ],           
        "lugar conversacion baja": [
            {"estado": 1, "enchufe": True, "tipo": "conversacion baja", "usuario": "Clara"},
            {"estado": 0, "enchufe": False, "tipo": "conversacion baja", "usuario": None},
            {"estado": 0, "enchufe": True, "tipo": "conversacion baja", "usuario": None},
            {"estado": 0, "enchufe": True, "tipo": "conversacion baja", "usuario": None}
        ],  
        "descripcion": "Un espacio reducido, dividido en dos sectores: uno en silencio total y otro donde se puede hablar bajito."
    },
    {
        "nombre": "UADE Labs - Espacio Tech",
        "tipo": "computadora disponible",
        "lugares con computadora": [
            {"estado": 0, "enchufe": True, "tipo": "computadora", "usuario": None},
            {"estado": 0, "enchufe": True, "tipo": "computadora", "usuario": None},
            {"estado": 1, "enchufe": True, "tipo": "computadora", "usuario": "Mario"},
            {"estado": 0, "enchufe": True, "tipo": "computadora", "usuario": None}
        ],
        "descripcion": "Un espacio chico con computadoras disponibles y salones equipados para trabajo práctico."
    }
]


# Diccionario para traducir los números en palabras
estados = {0: "libre", 1:"ocupado"}   


""" ---------FUNCIONES--------- """


# 1) Función que muestra la disponibilidad total en todos los pisos
def consultaTotal(pisos):
    for piso in pisos:
        total_libres = 0
        for clave in piso:
            if clave not in ["nombre", "tipo", "descripcion"]:
                lugares = piso[clave]
                for lugar in lugares:
                    if lugar["estado"] == 0:
                        total_libres += 1
        print(f"En {piso['nombre']}: hay {total_libres} lugares disponibles")




# 2) Función que muestra el estado de cada lugar en un piso elegido
def consultarDisponibilidad(pisos, piso_num):
    if piso_num < 0 or piso_num >= len(pisos):
        print("El número de piso ingresado no es válido.")
        return

    piso = pisos[piso_num]
    print(f"\n{piso['nombre']}")

    for clave in piso:
        if clave not in ["nombre", "tipo", "descripcion"]:
            print(f"\nTipo: {clave}")
            lugares = piso[clave]
            for i in range(len(lugares)):
                estado = "libre" if lugares[i]["estado"] == 0 else "ocupado"
                usuario = lugares[i]["usuario"]
                if estado == "ocupado":
                    print(f"Lugar {i + 1}: {estado} (Usuario: {usuario})")
                else:
                    print(f"Lugar {i + 1}: {estado}")




# 3) Función para mostrar todos los lugares libres de todos los pisos
def verLugaresLibres(pisos):
    for piso in pisos:
        print(f"\n{piso['nombre']}")
        
        matriz = []
        tipos = [clave for clave in piso if clave not in ["nombre", "tipo", "descripcion"]]
        for tipo in tipos:
            fila = []
            i = 0
            while i < len(piso[tipo]):
                if piso[tipo][i]["estado"] == 0:
                    fila.append("Libre")
                else:
                    fila.append("Ocupado")
                i += 1
            matriz.append(fila)
        
        t = 0
        while t < len(tipos):
            print(f"\nTipo: {tipos[t]}")
            fila = matriz[t]
            libres = []
            j = 0
            while j < len(fila):
                if fila[j] == "Libre":
                    libres.append(str(j+1))
                j += 1

            if libres:
                k = 0
                while k < len(libres):
                    print("  ".join(libres[k:k+5]))
                    k += 5
            else:
                print("No hay lugares libres en este tipo")
            t += 1



# 4) Función para reservar un lugar
def reservarLugar(pisos):
    # Elegir piso
    print("\nPisos disponibles:")
    i = 1
    for piso_dict in pisos:
        print(i, piso_dict['nombre'])
        i += 1
    piso_num = int(input("\n✶ Elegí el número del piso: ")) - 1
    if piso_num < 0 or piso_num >= len(pisos): return
    piso = pisos[piso_num]

    # Elegir tipo de lugar
    tipos = [t for t in piso if t not in ["nombre","tipo","descripcion"]]
    print("\nTipos de lugar disponibles:")
    i = 1
    for t in tipos:
        print(i, t)
        i += 1
    tipo_num = int(input("\n✶ Elegí el tipo de lugar por número: ")) - 1
    if tipo_num < 0 or tipo_num >= len(tipos): return
    tipo = tipos[tipo_num]
    lugares = piso[tipo]

    # Elegir lugar libre
    libres = []
    j = 1
    for lugar in lugares:
        if lugar["estado"] == 0: libres.append(j)
        j += 1
    if not libres: 
        print("No hay lugares libres"); return
    print("\nLugares libres disponibles:", libres)
    lugar_num = int(input("\n✶ Elegí el número de lugar: "))
    if lugar_num not in libres: return

    # Reservar
    usuario = input("✶ Ingresá tu nombre: ").strip()
    confirm = input(f"¿Seguro que querés reservar el lugar {lugar_num} en {piso['nombre']}? (s/n): ").strip().lower()
    if confirm == "s":
        lugares[lugar_num-1]["estado"] = 1
        lugares[lugar_num-1]["usuario"] = usuario
        print(f"¡Lugar {lugar_num} en {piso['nombre']} reservado por {usuario}!")
    else:
        print("Reserva cancelada.")




# 5) Función para liberar un lugar
def liberarLugar(pisos):
    # Elegir piso
    print("\nPisos disponibles:")
    i = 1
    for piso_dict in pisos:
        print(i, piso_dict['nombre'])
        i += 1
    piso_num = int(input("\n✶ Elegí el número del piso: ")) - 1
    if piso_num < 0 or piso_num >= len(pisos): return
    piso = pisos[piso_num]

    # Elegir tipo de lugar
    tipos = [t for t in piso if t not in ["nombre","tipo","descripcion"]]
    print("\nTipos de lugar disponibles:")
    i = 1
    for t in tipos:
        print(i, t)
        i += 1
    tipo_num = int(input("\n✶ Elegí el tipo de lugar por número: ")) - 1
    if tipo_num < 0 or tipo_num >= len(tipos): return
    tipo = tipos[tipo_num]
    lugares = piso[tipo]

    # Elegir lugar ocupado
    ocupados = []
    j = 1
    for lugar in lugares:
        if lugar["estado"] == 1: ocupados.append(j)
        j += 1
    if not ocupados: 
        print("No hay lugares ocupados"); return
    print("\nLugares ocupados disponibles:", ocupados)
    lugar_num = int(input("\n✶ Elegí el número de lugar a liberar: "))
    if lugar_num not in ocupados: return

    # Liberar
    confirm = input(f"¿Seguro que quieres liberar el lugar {lugar_num} en {piso['nombre']}? (s/n): ").strip().lower()
    if confirm == "s":
        lugares[lugar_num-1]["estado"] = 0
        lugares[lugar_num-1]["usuario"] = None
        print(f"¡Lugar {lugar_num} en {piso['nombre']} liberado con éxito!")
    else:
        print("Liberación cancelada.")


def verUsuariosActivos(pisos):
    usuarios = {}
    for piso in pisos:
        nombre_piso = piso["nombre"]
        for clave in piso:
            if clave not in ["nombre", "tipo", "descripcion"]:
                lugares = piso[clave]
                indice = 1
                for lugar in lugares:
                    if lugar["estado"] == 1 and lugar["usuario"] != None:
                        if lugar["usuario"] not in usuarios:
                            usuarios[lugar["usuario"]] = set()
                        usuarios[lugar["usuario"]].add((nombre_piso, clave, indice))
                    indice += 1

    if usuarios:
        print("Usuarios con reservas activas:")
        for usuario in usuarios:
            print("", usuario, "tiene reservados:")
            for reserva in usuarios[usuario]:
                print("  Piso:", reserva[0], "| Tipo:", reserva[1], "| Lugar:", reserva[2])
    else:
        print("No hay usuarios con reservas activas.")

def mostrarPorcentajes(pisos):
    ocupaciones = {}

    for piso in pisos:
        todas_las_listas = [piso[clave] for clave in piso if clave not in ["nombre", "tipo", "descripcion"]]

        total_lugares = 0
        ocupados = 0

        for lugares in todas_las_listas:
            for lugar in lugares:
                total_lugares += 1
                if lugar["estado"] == 1:
                    ocupados += 1

        porcentaje = (ocupados / total_lugares) * 100 if total_lugares > 0 else 0
        ocupaciones[piso["nombre"]] = porcentaje
        print(f"{piso['nombre']}: {porcentaje:.2f}% ocupación")

    if ocupaciones:
        max_ocupacion = -1
        piso_mas_ocupado = ""
        for nombre, porcentaje in ocupaciones.items():
            if porcentaje > max_ocupacion:
                max_ocupacion = porcentaje
                piso_mas_ocupado = nombre
        print(f"\nPiso más ocupado: {piso_mas_ocupado} ({max_ocupacion:.2f}% ocupación)")

def filtrarPorAtributoSimple(pisos):
    atributos = ["enchufe", "pizarron"]

    print("Atributos disponibles:")
    i = 1
    for atributo in atributos:
        print(i, atributo)
        i += 1
    print(0, "Mostrar todos")

    opcion = input("Elegí un atributo por número: ").strip()
    atributo_seleccionado = ""
    if opcion == "1":
        atributo_seleccionado = "enchufe"
    elif opcion == "2":
        atributo_seleccionado = "pizarron"

    lugares_filtrados = []
    for piso in pisos:
        nombre_piso = piso["nombre"]
        for clave in piso:
            if clave not in ["nombre", "tipo", "descripcion"]:
                numero_lugar = 1 
                for lugar in piso[clave]:
                    if lugar["estado"] == 0 and (atributo_seleccionado == "" or lugar.get(atributo_seleccionado, False)):
                        lugares_filtrados.append((nombre_piso, clave, numero_lugar))
                    numero_lugar += 1

    if lugares_filtrados:
        print("\nLugares libres filtrados:")
        for lugar in lugares_filtrados:
            print("Piso:", lugar[0], "| Tipo:", lugar[1], "| Lugar:", lugar[2])
    else:
        print("No se encontraron lugares libres con ese atributo.")


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
        print("5. Ver usuarios activos")
        print("6. Ver porcentjaes")
        print("7. Filtrar por atributo")
        print("0. Salir")
        
        opcion = input("\n ✶ Elegí una opción: ").strip()
        
        if opcion == "1":                    #si elige informacion
            submenuInformacion()            # vamos al submenú de info de pisos
        elif opcion == "2":                 # si elige consultar
            submenuConsultas(pisos)         # vamos al submenú de consultas
        elif opcion == "3":
            reservarLugar(pisos)
        elif opcion == "4":   # Liberar
            liberarLugar(pisos)
        elif opcion=="5":
            verUsuariosActivos(pisos)
        elif opcion=="6":
            mostrarPorcentajes(pisos)
        elif opcion=="7":
            filtrarPorAtributoSimple(pisos)


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
