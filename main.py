import re

# ==========================
# SISTEMA DE LOGIN Y RESERVAS
# ==========================

def login():
    print("=== Inicio de sesión en UADE Desk Finder ===")

    nombre = input("Nombre: ").strip()
    while not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", nombre):
        nombre = input("Solo letras y espacios, por favor: ").strip()

    legajo = input("Legajo (7 dígitos): ").strip()
    while not re.match(r"^\d{7}$", legajo):
        legajo = input("El legajo debe tener 7 dígitos. Volvé a ingresarlo: ").strip()

    archivo = f"{legajo}.txt"
    reservas = []

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    reservas.append(linea)
        print(f"\n¡Bienvenido de nuevo, {nombre}!")
    except FileNotFoundError:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write("")
        print(f"\nCuenta creada para {nombre}.")

    return {"nombre": nombre, "legajo": legajo, "archivo": archivo, "reservas": reservas}


def guardar_reservas(usuario):
    with open(usuario["archivo"], "w", encoding="utf-8") as f:
        for r in usuario["reservas"]:
            f.write(r + "\n")


def ver_mis_reservas(usuario):
    if not usuario["reservas"]:
        print("\nNo tenés reservas activas.")
    else:
        print("\nTus reservas activas:")
        for i, r in enumerate(usuario["reservas"], start=1):
            print(f"{i}. {r}")


def reservarLugarPrivado(pisos, usuario):
    print("\nPisos disponibles:")
    for i, piso_dict in enumerate(pisos, start=1):
        print(i, piso_dict['nombre'])
    piso_num = input("\n✶ Elegí el número del piso: ").strip()

    while not piso_num.isdigit() or int(piso_num) < 1 or int(piso_num) > len(pisos):
        piso_num = input("Número inválido, ingresá nuevamente: ").strip()
    piso = pisos[int(piso_num) - 1]

    tipos = [t for t in piso if t not in ["nombre", "tipo", "descripcion"]]
    print("\nTipos de lugar disponibles:")
    for i, t in enumerate(tipos, start=1):
        print(i, t)
    tipo_num = input("\n✶ Elegí el tipo de lugar: ").strip()

    while not tipo_num.isdigit() or int(tipo_num) < 1 or int(tipo_num) > len(tipos):
        tipo_num = input("Número inválido, ingresá nuevamente: ").strip()
    tipo = tipos[int(tipo_num) - 1]
    lugares = piso[tipo]

    libres = [i + 1 for i, l in enumerate(lugares) if l["estado"] == 0]
    if not libres:
        print("No hay lugares libres.")
        return
    print("\nLugares libres:", libres)
    lugar_num = input("\n✶ Elegí número de lugar: ").strip()

    while not lugar_num.isdigit() or int(lugar_num) not in libres:
        lugar_num = input("Número inválido, ingresá nuevamente: ").strip()
    lugar_num = int(lugar_num)

    lugares[lugar_num - 1]["estado"] = 1
    lugares[lugar_num - 1]["usuario"] = usuario['nombre']

    texto_reserva = f"{piso['nombre']} | {tipo} | Lugar {lugar_num}"
    usuario["reservas"].append(texto_reserva)
    guardar_reservas(usuario)

    print(f"\n¡Listo {usuario['nombre']}! Reservaste el {texto_reserva}.\n")

    while True:
        opcion = input("¿Querés hacer otra reserva? (s/n): ").strip().lower()
        if opcion == "s":
            return True
        elif opcion == "n":
            print("\nGracias por usar UADE Desk Finder. ¡Hasta pronto!\n")
            return False
        else:
            print("Opción inválida, escribí 's' o 'n'.")


def extraer_numero(texto):
    numero = ""
    for c in texto:
        if c.isdigit():
            numero += c
    if numero == "":
        return None
    return int(numero)


def liberarLugarPrivado(pisos, usuario):
    ver_mis_reservas(usuario)
    if not usuario["reservas"]:
        return

    num = input("\n✶ Ingresá el número de la reserva a liberar: ").strip()
    while not num.isdigit() or int(num) < 1 or int(num) > len(usuario["reservas"]):
        num = input("Número inválido, intentá de nuevo: ").strip()
    num = int(num)

    reserva = usuario["reservas"].pop(num - 1)
    guardar_reservas(usuario)

    partes = reserva.split(" | ")
    piso_nombre, tipo, lugar_txt = partes
    lugar_num = extraer_numero(lugar_txt)

    for piso in pisos:
        if piso["nombre"] == piso_nombre:
            lugar_lista = piso[tipo]
            lugar_lista[lugar_num - 1]["estado"] = 0
            lugar_lista[lugar_num - 1]["usuario"] = None

    print(f"\nReserva liberada: {reserva}\n")


# ==========================
# FUNCIONES DE CONSULTA GENERAL
# ==========================

def consultaTotal(pisos):
    for piso in pisos:
        total_libres = sum(map(lambda l: 1 if l["estado"] == 0 else 0,
                            [lugar for clave in piso if clave not in ["nombre", "tipo", "descripcion"] for lugar in piso[clave]]))
        print(f"En {piso['nombre']}: hay {total_libres} lugares disponibles.")


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
                if estado == "ocupado":
                    print(f"Lugar {i + 1}: {estado}")
                else:
                    print(f"Lugar {i + 1}: {estado}")


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
    atributos = ("enchufe", "pizarron")

    print("\nAtributos disponibles:")
    i = 1
    for atributo in atributos:
        print(f'    {i}. {atributo}')
        i += 1
    print(f'    {0}. Mostrar todos')

    opcion = input("\nElegí un atributo por número: ").strip()
    atributo_seleccionado = ""
    if opcion == "1":
        atributo_seleccionado = "enchufe"
    elif opcion == "2":
        atributo_seleccionado = "pizarron"

    resultados = {}
    
    for piso in pisos:
        nombre_piso = piso["nombre"]
        resultados[nombre_piso] = {}
        for clave in piso:
            if clave not in ["nombre", "tipo", "descripcion"]:
                lugares = piso[clave]
                disponibles = list(filter(lambda l: l["estado"] == 0 and (atributo_seleccionado == "" or l.get(atributo_seleccionado, False)), lugares))
                indices = []
                j = 0
                while j < len(lugares):
                    if lugares[j] in disponibles:
                        indices.append(j + 1)
                    j += 1
                resultados[nombre_piso][clave] = indices

    if len(resultados) > 0:
        if atributo_seleccionado != "":
            print("\nLugares con " + atributo_seleccionado + " disponibles en:")
        else:
            print("\nTodos los lugares libres disponibles en:")

        for piso in resultados:
            print("-------------------------------------------------------------------")
            print("Piso: " + piso)
            for tipo in resultados[piso]:
                print("  Tipo: " + tipo)
                print("    Lugares: ", end="")
                for lugar in resultados[piso][tipo]:
                    print(str(lugar), end="  ")
                print()
        print("-------------------------------------------------------------------")
    else:
        print("\nNo se encontraron lugares libres con ese atributo.")

    input("\nPresione enter para volver al menú principal...")


# ==========================
# ESTRUCTURA DE PISOS
# ==========================

pisos = [
    {
        "nombre": "Piso 10 - Espacio Panorámico",
        "tipo": "grupal o individual",
        "lugar grupal": [
            {"estado": 0, "enchufe": True, "pizarron": True, "tipo": "grupal", "usuario": None},
            {"estado": 1, "enchufe": True, "pizarron": True, "tipo": "grupal", "usuario": "Jorge"},
            {"estado": 0, "enchufe": True, "pizarron": True, "tipo": "grupal", "usuario": None},
            {"estado": 0, "enchufe": True, "pizarron": False, "tipo": "grupal", "usuario": None},
            {"estado": 0, "enchufe": True, "pizarron": True, "tipo": "grupal", "usuario": None},
            {"estado": 1, "enchufe": True, "pizarron": False, "tipo": "grupal", "usuario": "Santiago"},
            {"estado": 0, "enchufe": True, "pizarron": True, "tipo": "grupal", "usuario": None},
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


# ==========================
# MENÚ DE USUARIO
# ==========================

def menuUsuario(pisos, usuario):
    while True:
        print("\n=== Menú de Usuario ===")
        print("1. Ver mis reservas")
        print("2. Reservar un nuevo lugar")
        print("3. Liberar una reserva")
        print("4. Consulta total de lugares libres(Vista numerica)")
        print("5. Consultar disponibilidad por piso")
        print("6. Ver todos los lugares libres(Vista Grafica)")
        print("7. Mostrar porcentajes de ocupación")
        print("8. Filtrar lugares por atributo")
        print("0. Salir")

        op = input("\n✶ Elegí una opción: ").strip()

        if op == "1":
            ver_mis_reservas(usuario)
        elif op == "2":
            reservarLugarPrivado(pisos, usuario)
        elif op == "3":
            liberarLugarPrivado(pisos, usuario)
        elif op == "4":
            consultaTotal(pisos)
        elif op == "5":
            piso_num = int(input("Número de piso (1 a 3): ")) - 1
            consultarDisponibilidad(pisos, piso_num)
        elif op == "6":
            verLugaresLibres(pisos)
        elif op == "7":
            mostrarPorcentajes(pisos)
        elif op == "8":
            filtrarPorAtributoSimple(pisos)
        elif op == "0":
            print("\n¡Hasta pronto!")
            break
        else:
            print("Opción inválida, intentá de nuevo.")


# ==========================
# INICIO DEL PROGRAMA
# ==========================

usuario = login()
menuUsuario(pisos, usuario)
