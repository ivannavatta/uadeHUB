from main import generar_fechas_disponibles

def test_generar_fechas_cantidad():
    fechas = generar_fechas_disponibles()
    assert len(fechas) == 5

def test_generar_fechas_formato():
    fechas = generar_fechas_disponibles()
    for f in fechas:
        assert len(f) == 5
        assert f[2] == "-"
