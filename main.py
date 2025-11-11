import re
from functools import reduce

ARCHIVO_GLOBAL = "reservas_globales.txt"

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
            lineas = [l.strip() for l in f.readlines() if l.strip()]
        if not lineas:
            print("\nError: archivo vacío o dañado. No se puede acceder.")
            return None
        nombre_guardado = lineas[0]
        if nombre_guardado.lower() != nombre.lower():
            print(f"\n El legajo {legajo} pertenece a otro usuario ({nombre_guardado}).")
            print("No podés iniciar sesión con un nombre diferente.")
            return None
        reservas = lineas[1:]
        print(f"\n¡Bienvenido de nuevo, {nombre_guardado}!")
    except FileNotFoundError:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(nombre + "\n")
        print(f"\nCuenta creada para {nombre} (Legajo: {legajo}).")

    return {"nombre": nombre, "legajo": legajo, "archivo": archivo, "reservas": reservas}
def guardar_reservas(usuario):
    with open(usuario["archivo"], "w", encoding="utf-8") as f:
        f.write(usuario["nombre"] + "\n")
        for r in usuario["reservas"]:
            f.write(r + "\n")

def guardar_reservas_global(pisos):
    with open(ARCHIVO_GLOBAL, "w", encoding="utf-8") as f:
        for piso in pisos:
            for clave in piso:
                if clave not in ["nombre", "tipo", "descripcion"]:
                    for i, lugar in enumerate(piso[clave], start=1):
                        if lugar["estado"] == 1 and lugar["usuario"]:
                            f.write(f"{piso['nombre']}|{clave}|{i}|{lugar['usuario']}\n")

def cargar_reservas_globales():
    reservas = []
    try:
        with open(ARCHIVO_GLOBAL, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) == 4:
                    reservas.append({"piso": partes[0], "tipo": partes[1], "lugar": int(partes[2]), "usuario": partes[3]})
    except FileNotFoundError:
        with open(ARCHIVO_GLOBAL, "w", encoding="utf-8") as f:
            f.write("")
    return reservas

def cargar_pisos():
    pisos = []
    try:
        with open("pisos.txt", "r", encoding="utf-8") as f:
            lineas = [l.strip() for l in f if l.strip() != ""]
    except FileNotFoundError:
        print("No se encontró el archivo pisos.txt. Creá uno con la estructura adecuada.")
        return pisos
    piso_actual = {}
    tipo_actual = ""
    for linea in lineas:
        if linea == "---":
            pisos.append(piso_actual)
            piso_actual = {}
            tipo_actual = ""
        elif linea.startswith("[") and linea.endswith("]"):
            tipo_actual = linea[1:-1]
            piso_actual[tipo_actual] = []
        elif "=" in linea and not tipo_actual:
            clave, valor = linea.split("=", 1)
            piso_actual[clave.strip()] = valor.strip()
        elif "=" in linea and tipo_actual:
            datos = {}
            partes = linea.split(",")
            i = 0
            while i < len(partes):
                if "=" in partes[i]:
                    c, v = partes[i].split("=")
                    c = c.strip()
                    v = v.strip()
                    if v.lower() == "true":
                        v = True
                    elif v.lower() == "false":
                        v = False
                    elif v.lower() == "none":
                        v = None
                    elif v.isdigit():
                        v = int(v)
                    datos[c] = v
                i += 1
            if "estado" not in datos:
                datos["estado"] = 0
            piso_actual[tipo_actual].append(datos)
    reservas = cargar_reservas_globales()
    for r in reservas:
        for piso in pisos:
            if piso["nombre"] == r["piso"]:
                if r["tipo"] in piso and len(piso[r["tipo"]]) >= r["lugar"]:
                    piso[r["tipo"]][r["lugar"] - 1]["estado"] = 1
                    piso[r["tipo"]][r["lugar"] - 1]["usuario"] = r["usuario"]
    return pisos

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
    reservas_globales = cargar_reservas_globales()
    for r in reservas_globales:
        if r["piso"] == piso["nombre"] and r["tipo"] == tipo and r["lugar"] == lugar_num:
            print("Ese lugar ya fue reservado por otro usuario.")
            return
    lugares[lugar_num - 1]["estado"] = 1
    lugares[lugar_num - 1]["usuario"] = usuario['nombre']
    texto_reserva = f"{piso['nombre']} | {tipo} | Lugar {lugar_num}"
    usuario["reservas"].append(texto_reserva)
    guardar_reservas(usuario)
    guardar_reservas_global(pisos)
    print(f"\n¡Listo {usuario['nombre']}! Reservaste el {texto_reserva}.\n")
    while True:
        opcion = input("¿Querés hacer otra reserva? (s/n): ").strip().lower()
        if opcion == "s":
            reservarLugarPrivado(pisos, usuario)
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
    guardar_reservas_global(pisos)
    print(f"\nReserva liberada: {reserva}\n")

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

def estadisticasGlobales(pisos):
    print("\n=== Estadísticas globales de UADE Desk Finder ===")
    todos_los_lugares = [
        lugar
        for piso in pisos
        for clave in piso
        if clave not in ["nombre", "tipo", "descripcion"]
        for lugar in piso[clave]
    ]
    total_lugares = len(todos_los_lugares)
    ocupados = reduce(lambda acc, l: acc + (1 if l["estado"] == 1 else 0), todos_los_lugares, 0)
    libres = total_lugares - ocupados
    print(f"Total de lugares: {total_lugares}")
    print(f"Lugares ocupados: {ocupados}")
    print(f"Lugares libres:   {libres}")
    print(f"Porcentaje de ocupación total: {(ocupados / total_lugares * 100):.2f}%")

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

def analisisUsuarios(pisos):
    print("\n=== ACCESO RESTRINGIDO ===")
    clave = input("Ingresá la contraseña de administrador: ").strip()
    if clave != "uade":
        print("\n Contraseña incorrecta. No tenés permiso para acceder al análisis de usuarios.")
        return

    print("\n=== Análisis de Usuarios ===")
    usuarios_por_piso = []
    for piso in pisos:
        usuarios = set()
        for clave in piso:
            if clave not in ["nombre", "tipo", "descripcion"]:
                for lugar in piso[clave]:
                    if lugar["usuario"]:
                        usuarios.add(lugar["usuario"])
        usuarios_por_piso.append(usuarios)

    if len(usuarios_por_piso) < 2:
        print("\n No hay suficientes pisos para realizar comparaciones (se necesitan al menos 2).")
        return

    union_usuarios = set.union(*usuarios_por_piso)
    interseccion_usuarios = set.intersection(*usuarios_por_piso)
    diferencia_usuarios = usuarios_por_piso[0].difference(usuarios_por_piso[1])

    print("\n RESULTADOS DEL ANÁLISIS\n")
    print("► Usuarios en cualquier piso (unión):")
    if union_usuarios:
        print("   ", ", ".join(sorted(union_usuarios)))
    else:
        print("   Ninguno")

    print("\n► Usuarios que reservaron en más de un piso (intersección):")
    if interseccion_usuarios:
        print("   ", ", ".join(sorted(interseccion_usuarios)))
    else:
        print("   Ninguno")

    print(f"\n► Usuarios que reservaron solo en {pisos[0]['nombre']} y no en {pisos[1]['nombre']}:")
    if diferencia_usuarios:
        print("   ", ", ".join(sorted(diferencia_usuarios)))
    else:
        print("   Ninguno")

    print("\nFin del análisis.\n")

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
        print("9. Ver estadísticas globales")
        print("10. Análisis de usuarios")
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
            piso_num = int(input("Número de piso: ")) - 1
            consultarDisponibilidad(pisos, piso_num)
        elif op == "6":
            verLugaresLibres(pisos)
        elif op == "7":
            mostrarPorcentajes(pisos)
        elif op == "8":
            filtrarPorAtributoSimple(pisos)
        elif op == "9":
            estadisticasGlobales(pisos)
        elif op == "10":
            analisisUsuarios(pisos)
        elif op == "0":
            print("\n¡Hasta pronto!")
            break
        else:
            print("Opción inválida, intentá de nuevo.")

pisos = cargar_pisos()
if not pisos:
    print("No se pudieron cargar pisos. Cerrando programa.")
else:
    usuario = login()
    if usuario is not None:
        menuUsuario(pisos, usuario)
    else:
        print("\nInicio de sesión cancelado por seguridad.\n")
