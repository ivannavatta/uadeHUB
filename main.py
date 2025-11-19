import re
from functools import reduce
from datetime import datetime, timedelta

#FUNCIONES DE CARGA

ARCHIVO_GLOBAL = "reservas_globales.txt"

def generar_fechas_disponibles():
    hoy = datetime.now()
    return [(hoy + timedelta(days=i)).strftime("%d-%m") for i in range(5)]

FECHAS_DISPONIBLES = generar_fechas_disponibles()

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
                        if "reservas" in lugar:
                            for r in lugar["reservas"]:
                                f.write(f"{piso['nombre']}|{clave}|{i}|{r['usuario']}|{r['fecha']}\n")

def cargar_reservas_globales():
    reservas = []
    try:
        with open(ARCHIVO_GLOBAL, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) == 5:
                    reservas.append({
                        "piso": partes[0],
                        "tipo": partes[1],
                        "lugar": int(partes[2]),
                        "usuario": partes[3],
                        "fecha": partes[4]
                    })
    except FileNotFoundError:
        with open(ARCHIVO_GLOBAL, "w", encoding="utf-8") as f:
            f.write("")
    return reservas



def cargar_pisos():
    pisos = []
    try:
        with open("pisos.txt", "r", encoding="utf-8") as f:
            lineas = [l.strip() for l in f if l.strip()]
    except IOError:
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
            for parte in partes:
                if "=" in parte:
                    c, v = parte.split("=")
                    datos[c.strip()] = v.strip()
            datos["reservas"] = [] 
            piso_actual[tipo_actual].append(datos)

    reservas = cargar_reservas_globales()
    for r in reservas:
        for piso in pisos:
            if piso["nombre"] == r["piso"]:
                if r["tipo"] in piso and len(piso[r["tipo"]]) >= r["lugar"]:
                    piso[r["tipo"]][r["lugar"] - 1]["reservas"].append({
                        "usuario": r["usuario"],
                        "fecha": r["fecha"]
                    })
    return pisos


#FUNCIONES DE USUARIO



def ver_mis_reservas(usuario):
    if not usuario["reservas"]:
        print("\nNo tenés reservas activas.")
    else:
        print("\nTus reservas activas:")
        for i, r in enumerate(usuario["reservas"], start=1):
            print(f"{i}. {r}")

def reservarLugarPrivado(pisos, usuario):
    fechas_disponibles = FECHAS_DISPONIBLES

    print("\nPisos disponibles:")
    for i, piso_dict in enumerate(pisos, start=1):
        print(i, piso_dict['nombre'])

    piso_num = input("\n✶ Elegí el número del piso (0 para volver): ").strip()
    if piso_num == "0":
        return
    while not piso_num.isdigit() or int(piso_num) < 1 or int(piso_num) > len(pisos):
        piso_num = input("Número inválido, ingresá nuevamente (0 para volver): ").strip()
        if piso_num == "0":
            return
    piso = pisos[int(piso_num) - 1]

    tipos = [t for t in piso if t not in ["nombre", "tipo", "descripcion"]]
    print("\nTipos de lugar disponibles:")
    for i, t in enumerate(tipos, start=1):
        print(i, t)

    tipo_num = input("\n✶ Elegí el tipo de lugar (0 para volver): ").strip()
    if tipo_num == "0":
        return
    while not tipo_num.isdigit() or int(tipo_num) < 1 or int(tipo_num) > len(tipos):
        tipo_num = input("Número inválido, ingresá nuevamente (0 para volver): ").strip()
        if tipo_num == "0":
            return
    tipo = tipos[int(tipo_num) - 1]
    lugares = piso[tipo]

    print("\nFechas disponibles:")
    for i, fecha in enumerate(fechas_disponibles, start=1):
        print(f"{i}. {fecha}")

    fecha_num = input("\n✶ Elegí una fecha (0 para volver): ").strip()
    if fecha_num == "0":
        return
    while not fecha_num.isdigit() or int(fecha_num) < 1 or int(fecha_num) > len(fechas_disponibles):
        fecha_num = input("Número inválido. Ingresá nuevamente (0 para volver): ").strip()
        if fecha_num == "0":
            return
    fecha = fechas_disponibles[int(fecha_num) - 1]

    reservas_globales = cargar_reservas_globales()

    print(f"\n=== Lugares disponibles en {piso['nombre']} ({tipo}) para el {fecha} ===")
    libres = []
    for i, l in enumerate(lugares, start=1):

        reservado = False
        for r in reservas_globales:
            if (
                r["piso"] == piso["nombre"] and
                r["tipo"] == tipo and
                r["lugar"] == i and
                r.get("fecha") == fecha
            ):
                reservado = True
                break

        estado = "❌ Ocupado" if reservado else "✅ Libre"

        atributos = []
        if l.get("enchufe"):
            atributos.append("Enchufe")
        if l.get("pizarron"):
            atributos.append("Pizarrón")

        attr_text = f"  ({', '.join(atributos)})" if atributos else ""
        print(f"Lugar {i}: {estado}{attr_text}")

        if not reservado:
            libres.append(i)

    if not libres:
        print("\nNo hay lugares libres para esa fecha.")
        return

    lugar_num = input("\n✶ Elegí el número del lugar que querés reservar (0 para volver): ").strip()
    if lugar_num == "0":
        return
    while not lugar_num.isdigit() or int(lugar_num) not in libres:
        lugar_num = input("Número inválido o lugar ocupado. Probá de nuevo (0 para volver): ").strip()
        if lugar_num == "0":
            return
    lugar_num = int(lugar_num)

    texto_reserva = f"{piso['nombre']} | {tipo} | Lugar {lugar_num} | Fecha {fecha}"
    usuario["reservas"].append(texto_reserva)

    guardar_reservas(usuario)

    with open(ARCHIVO_GLOBAL, "a", encoding="utf-8") as f:
        f.write(f"{piso['nombre']}|{tipo}|{lugar_num}|{usuario['nombre']}|{fecha}\n")

    print(f"\n¡Listo {usuario['nombre']}! Reservaste el {texto_reserva}.\n")

    while True:
        opcion = input("¿Querés hacer otra reserva? (s/n): ").strip().lower()
        if opcion == "s":
            reservarLugarPrivado(pisos, usuario)
            break
        elif opcion == "n":
            print("\nGracias por usar UADE Desk Finder. ¡Hasta pronto!\n")
            break
        else:
            print("Opción inválida, escribí 's' o 'n'.")



def liberarLugarPrivado(pisos, usuario):
    ver_mis_reservas(usuario)
    if not usuario["reservas"]:
        return
    num = input("\n✶ Ingresá el número de la reserva a liberar (0 para volver): ").strip()
    if num == "0":
        return
    while not num.isdigit() or int(num) < 1 or int(num) > len(usuario["reservas"]):
        num = input("Número inválido, intentá de nuevo (0 para volver): ").strip()
        if num == "0":
            return
    num = int(num)
    reserva = usuario["reservas"].pop(num - 1)
    guardar_reservas(usuario)

    partes = [p.strip() for p in reserva.split("|")]
    piso_nombre = partes[0]
    tipo = partes[1]
    lugar_num = int(''.join([c for c in partes[2] if c.isdigit()]))
    fecha = partes[3].replace("Fecha ", "")

    for piso in pisos:
        if piso["nombre"] == piso_nombre:
            lugar_lista = piso[tipo]
            lugar_lista[lugar_num - 1]["reservas"] = [
                r for r in lugar_lista[lugar_num - 1]["reservas"]
                if not (r["usuario"] == usuario["nombre"] and r["fecha"] == fecha)
            ]

    guardar_reservas_global(pisos)
    print(f"\nReserva liberada: {reserva}\n")
    while True:
        opcion = input("¿Querés liberar otra reserva? (s/n): ").strip().lower()
        if opcion == "s":
            liberarLugarPrivado(pisos, usuario)
            break
        elif opcion == "n":
            print("\nGracias por usar UADE Desk Finder. ¡Hasta pronto!\n")
            break
        else:
            print("Opción inválida, escribí 's' o 'n'.")



def consultaTotal():
    fechas_disponibles = FECHAS_DISPONIBLES
    pisos = cargar_pisos()
    print("\n=== Consulta total de lugares libres ===")
    print("Fechas disponibles:")
    for i, f in enumerate(fechas_disponibles, start=1):
        print(f"{i}. {f}")

    seleccion = input("\nElegí una fecha: ").strip()
    while not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(fechas_disponibles):
        seleccion = input("Número inválido, probá nuevamente: ")

    fecha = fechas_disponibles[int(seleccion) - 1]

    print(f"\n=== Lugares libres para el {fecha} ===")

    for piso in pisos:

        total_libres = sum(
            map(
                lambda l: 1 if fecha not in [r["fecha"] for r in l["reservas"]] else 0,
                (
                    lugar
                    for clave in piso
                    if clave not in ["nombre", "tipo", "descripcion"]
                    for lugar in piso[clave]
                )
            )
        )

        print(f"{piso['nombre']}: {total_libres} libres")

def consultarDisponibilidad(pisos):
    fechas_disponibles = FECHAS_DISPONIBLES

    print("\nPisos disponibles:")
    for i, piso_dict in enumerate(pisos, start=1):
        print(f"{i}. {piso_dict['nombre']}")

    seleccion_piso = input("\nElegí un piso: ").strip()
    while not seleccion_piso.isdigit() or int(seleccion_piso) < 1 or int(seleccion_piso) > len(pisos):
        seleccion_piso = input("Número inválido. Probá de nuevo: ").strip()

    piso = pisos[int(seleccion_piso) - 1]

    print("\nFechas disponibles:")
    for i, f in enumerate(fechas_disponibles, start=1):
        print(f"{i}. {f}")

    seleccion_fecha = input("\nElegí una fecha: ").strip()
    while not seleccion_fecha.isdigit() or int(seleccion_fecha) < 1 or int(seleccion_fecha) > len(fechas_disponibles):
        seleccion_fecha = input("Número inválido. Probá nuevamente: ").strip()

    fecha = fechas_disponibles[int(seleccion_fecha) - 1]

    print(f"\n=== Disponibilidad en {piso['nombre']} para el {fecha} ===")

    reservas_globales = cargar_reservas_globales()

    for clave in piso:
        if clave not in ["nombre", "tipo", "descripcion"]:
            print(f"\nTipo: {clave}")
            lugares = piso[clave]
            for i, l in enumerate(lugares, start=1):

                reservado = False
                for r in reservas_globales:
                    if (
                        r["piso"] == piso["nombre"]
                        and r["tipo"] == clave
                        and r["lugar"] == i
                        and r["fecha"] == fecha
                    ):
                        reservado = True
                        break

                estado = "❌ Ocupado" if reservado else "✅ Libre"

                atributos = []
                if l.get("enchufe"):
                    atributos.append("Enchufe")
                if l.get("pizarron"):
                    atributos.append("Pizarrón")
                attr_txt = f" ({', '.join(atributos)})" if atributos else ""

                print(f"  Lugar {i}: {estado}{attr_txt}")



def verLugaresLibres(pisos):
    fechas_disponibles = FECHAS_DISPONIBLES

    print("\nFechas disponibles:")
    for i, f in enumerate(fechas_disponibles, start=1):
        print(f"{i}. {f}")

    seleccion = input("\nElegí una fecha: ").strip()
    while not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(fechas_disponibles):
        seleccion = input("Número inválido, probá nuevamente: ").strip()

    fecha = fechas_disponibles[int(seleccion) - 1]
    reservas_globales = cargar_reservas_globales()

    print(f"\n=== Lugares libres para el {fecha} ===")
    for piso in pisos:
        print(f"\n{piso['nombre']}")

        tipos = list(filter(lambda k: k not in ["nombre", "tipo", "descripcion"], piso.keys()))

        for tipo in tipos:
            print(f"\nTipo: {tipo}")
            lugares = piso[tipo]
            libres = []

            for i, l in enumerate(lugares, start=1):
                reservado = False
                for r in reservas_globales:
                    if (
                        r["piso"] == piso["nombre"]
                        and r["tipo"] == tipo
                        and r["lugar"] == i
                        and r["fecha"] == fecha
                    ):
                        reservado = True
                        break

                if not reservado:
                    libres.append(str(i))

            if libres:
                for inicio in range(0, len(libres), 5):
                    print("  ".join(libres[inicio:inicio+5]))
            else:
                print("No hay lugares libres en este tipo")


        
def mostrarPorcentajes(pisos):
    fechas_disponibles = FECHAS_DISPONIBLES
    print("\nFechas disponibles:")
    for i, f in enumerate(fechas_disponibles, start=1):
        print(f"{i}. {f}")
    seleccion = input("\nElegí una fecha: ").strip()
    while not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(fechas_disponibles):
        seleccion = input("Número inválido, probá nuevamente: ").strip()
    fecha = fechas_disponibles[int(seleccion) - 1]
    reservas = cargar_reservas_globales()
    ocupaciones = {}

    for piso in pisos:
        total_lugares = 0
        ocupados = 0

        for clave in piso:
            if clave not in ["nombre", "tipo", "descripcion"]:
                lista = piso[clave]
                for i, _ in enumerate(lista, start=1):
                    total_lugares += 1
                    reservado = False

                    for r in reservas:
                        if r["piso"] == piso["nombre"] and r["tipo"] == clave and r["lugar"] == i and r["fecha"] == fecha:
                            reservado = True
                            break

                    if reservado:
                        ocupados += 1
        porcentaje = (ocupados / total_lugares * 100) if total_lugares > 0 else 0
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
    print("Fechas disponibles:")
    for i, f in enumerate(FECHAS_DISPONIBLES, start=1):
        print(f"{i}. {f}")

    sel = input("\nElegí una fecha: ").strip()
    while not sel.isdigit() or int(sel) < 1 or int(sel) > len(FECHAS_DISPONIBLES):
        sel = input("Número inválido, probá nuevamente: ").strip()

    fecha = FECHAS_DISPONIBLES[int(sel) - 1]
    reservas = cargar_reservas_globales()

    todos = [
        (piso["nombre"], tipo, i + 1)
        for piso in pisos
        for tipo in piso
        if tipo not in ["nombre", "tipo", "descripcion"]
        for i in range(len(piso[tipo]))
    ]

    total = len(todos)

    ocupados = reduce(
        lambda acc, t: acc + sum(
            1
            for r in reservas
            if r["piso"] == t[0] and r["tipo"] == t[1] and r["lugar"] == t[2] and r["fecha"] == fecha
        ),
        todos,
        0
    )

    libres = total - ocupados
    porc = (ocupados * 100) / total if total != 0 else 0

    print("\n=== Resultados globales ===")
    print("Total de lugares:", total)
    print("Lugares ocupados:", ocupados)
    print("Lugares libres:  ", libres)
    print(f"Porcentaje de ocupación total: {porc:.2f}%\n")



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

    fechas_disponibles = FECHAS_DISPONIBLES
    print("\nFechas disponibles:")
    for i, f in enumerate(fechas_disponibles, start=1):
        print(f"{i}. {f}")

    seleccion = input("\nElegí una fecha: ").strip()
    while not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(fechas_disponibles):
        seleccion = input("Número inválido, probá nuevamente: ").strip()

    fecha = fechas_disponibles[int(seleccion) - 1]
    reservas = cargar_reservas_globales()

    resultados = {}
    for piso in pisos:
        nombre_piso = piso["nombre"]
        resultados[nombre_piso] = {}

        for clave in piso:
            if clave not in ["nombre", "tipo", "descripcion"]:
                lugares = piso[clave]

                libres = []
                j = 0
                while j < len(lugares):
                    lugar = lugares[j]
                    ocupado = False
                    for r in reservas:
                        if r["piso"] == nombre_piso and r["tipo"] == clave and r["lugar"] == j + 1 and r["fecha"] == fecha:
                            ocupado = True
                            break
                    if not ocupado:
                        if atributo_seleccionado == "" or lugar.get(atributo_seleccionado) == "True":
                            libres.append(j + 1)
                    j += 1

                resultados[nombre_piso][clave] = libres

    hay_algo = False
    for piso in resultados:
        for tipo in resultados[piso]:
            if len(resultados[piso][tipo]) > 0:
                hay_algo = True
                break

    if hay_algo:
        if atributo_seleccionado != "":
            print("\nLugares con " + atributo_seleccionado + " disponibles en:")
        else:
            print("\nTodos los lugares libres disponibles en:")

        print("Fecha seleccionada:", fecha)
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
        print("\nNo se encontraron lugares libres con ese atributo para esa fecha.")

    input("\nPresione enter para volver al menú principal...")



def analisisUsuarios(pisos):
    print("\n=== ACCESO RESTRINGIDO ===")
    clave = input("Ingresá la contraseña de administrador: ").strip()
    if clave != "uade":
        print("\n Contraseña incorrecta. No tenés permiso para acceder al análisis de usuarios.")
        return

    pisos_actualizados = cargar_pisos()
    reservas_actualizadas = cargar_reservas_globales()

    print("\n=== Análisis de Usuarios ===")

    usuarios_por_piso = []
    for piso in pisos_actualizados:
        usuarios = set()
        for clave in piso:
            if clave not in ["nombre", "tipo", "descripcion"]:
                for lugar in piso[clave]:
                    for r in lugar.get("reservas", []):
                        if r.get("usuario"):
                            usuarios.add(r["usuario"])
        usuarios_por_piso.append(usuarios)

    if len(usuarios_por_piso) < 2:
        print("\n No hay suficientes pisos para realizar comparaciones (se necesitan al menos 2).")
        return

    union_usuarios = set.union(*usuarios_por_piso)
    interseccion_usuarios = set.intersection(*usuarios_por_piso)
    otros = set.union(*usuarios_por_piso[1:]) if len(usuarios_por_piso) > 1 else set()
    diferencia_usuarios = usuarios_por_piso[0].difference(otros)

    print("\n RESULTADOS DEL ANÁLISIS\n")
    print("► Usuarios en cualquier piso (unión):")
    print("   ", ", ".join(sorted(union_usuarios)) if union_usuarios else "   Ninguno")

    print("\n► Usuarios que reservaron en más de un piso (intersección):")
    print("   ", ", ".join(sorted(interseccion_usuarios)) if interseccion_usuarios else "   Ninguno")

    print(f"\n► Usuarios que reservaron solo en {pisos_actualizados[0]['nombre']} y no en los demás pisos:")
    print("   ", ", ".join(sorted(diferencia_usuarios)) if diferencia_usuarios else "   Ninguno")

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
        print("7. Mostrar porcentajes de ocupación por edificio")
        print("8. Filtrar lugares libres por atributo")
        print("9. Ver estadísticas globales de un dia")
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
            consultaTotal()
        elif op == "5":
            consultarDisponibilidad(pisos)
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
