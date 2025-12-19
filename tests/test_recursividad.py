from main import contar_lugares_libres_recursivo

def test_todos_lugares_libres():
    lugares = ["L1", "L2", "L3"]
    reservas = []

    resultado = contar_lugares_libres_recursivo(
        lugares,
        reservas,
        "Piso 1",
        "mesa",
        "2024-11-20"
    )

    assert resultado == 3


def test_un_lugar_ocupado():
    lugares = ["L1", "L2", "L3"]
    reservas = [
        {"piso": "Piso 1", "tipo": "mesa", "lugar": 2, "fecha": "2024-11-20"}
    ]

    resultado = contar_lugares_libres_recursivo(
        lugares,
        reservas,
        "Piso 1",
        "mesa",
        "2024-11-20"
    )

    assert resultado == 2


def test_lista_vacia():
    resultado = contar_lugares_libres_recursivo(
        [],
        [],
        "Piso 1",
        "mesa",
        "2024-11-20"
    )

    assert resultado == 0
