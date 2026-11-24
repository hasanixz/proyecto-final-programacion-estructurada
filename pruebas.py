"""Pruebas reproducibles: python pruebas.py. Solo usa datos temporales.

Las herramientas de prueba (mock y subprocess) no forman parte de las apps.
No se necesitan dependencias externas ni clases propias.
"""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import os
import shutil
import subprocess
import sys

from Calculadora import calculadora as calc
from Cajero import cajero as banco


def esperar_error(funcion, argumentos, tipo_error):
    try:
        funcion(*argumentos)
    except tipo_error:
        return
    raise AssertionError(f"{funcion.__name__} debía rechazar {argumentos}")


def ejecutar_consola(programa, entradas, directorio):
    entorno = os.environ.copy()
    entorno["PYTHONIOENCODING"] = "utf-8"
    proceso = subprocess.run(
        [sys.executable, str(programa)], input="\n".join(entradas) + "\n",
        text=True, encoding="utf-8", capture_output=True, cwd=directorio,
        env=entorno, timeout=30,
    )
    assert proceso.returncode == 0, proceso.stderr
    assert "Traceback" not in proceso.stderr, proceso.stderr
    return proceso.stdout


def probar_calculos():
    casos = [
        (calc.sumar, (8, 2), 10), (calc.restar, (8, 2), 6),
        (calc.multiplicar, (8, 2), 16), (calc.dividir, (8, 2), 4),
        (calc.division_entera, (9, 2), 4), (calc.division_entera, (-9, 2), -5),
        (calc.calcular_modulo, (9, 2), 1), (calc.calcular_potencia, (2, 3), 8),
        (calc.raiz_cuadrada, (9,), 3), (calc.calcular_porcentaje, (200, 15), 30),
    ]
    for funcion, argumentos, esperado in casos:
        assert funcion(*argumentos) == esperado
    for funcion in (calc.dividir, calc.division_entera, calc.calcular_modulo):
        esperar_error(funcion, (1, 0), ValueError)
    esperar_error(calc.raiz_cuadrada, (-1,), ValueError)
    esperar_error(calc.calcular_potencia, (-2, 0.5), ValueError)
    esperar_error(calc.calcular_potencia, (0, -1), ValueError)
    esperar_error(calc.calcular_potencia, (1e308, 2), OverflowError)
    for numero in (float("nan"), float("inf"), -float("inf")):
        esperar_error(calc.validar_resultado, (numero,), ValueError)
    esperar_error(calc.validar_resultado, (calc.multiplicar(1e308, 10),), ValueError)
    assert calc.tabla_multiplicar(7) == [(numero, numero * 7) for numero in range(1, 11)]
    assert "iguales" in calc.comparar_numeros(2, 2)
    assert "3 es mayor" in calc.comparar_numeros(2, 3)
    assert "3 es mayor" in calc.comparar_numeros(3, 2)
    resumen = calc.analizar_lista([1, 2, 2, 7])
    assert resumen == {"Suma": 12, "Promedio": 3, "Mayor": 7, "Menor": 1,
                       "Superiores al promedio": [7], "Valores únicos": {1, 2, 7}}
    esperar_error(calc.analizar_lista, ([],), ValueError)
    esperar_error(calc.analizar_lista, ([1e308, 1e308],), ValueError)


def probar_entradas():
    with patch("builtins.input", side_effect=["M", "abc", "nan", "inf", "-inf", "2.5"]):
        assert calc.pedir_numero("Número") == 2.5
    with patch("builtins.input", return_value="M"):
        assert calc.pedir_numero("Número", 10) == 10
    with patch("builtins.input", side_effect=["abc", "0", "-1", "1.5", "3"]):
        assert calc.pedir_entero_positivo("Cantidad") == 3
    with patch("builtins.input", side_effect=["abc", "0", "-1", "1.5", "nan", "50"]):
        assert banco.pedir_cantidad("Cantidad") == 50


def probar_historial_calculadora(carpeta):
    ruta = carpeta / "historial.txt"
    assert calc.cargar_historial(ruta) == []
    historial = []
    assert calc.obtener_memoria(historial) is None
    calc.mostrar_historial(historial)
    calc.mostrar_estadisticas(historial)
    for indice in range(7):
        calc.registrar_operacion(historial, "Suma", f"{indice} + 1", indice + 1, ruta)
    assert calc.cargar_historial(ruta) == historial
    assert calc.obtener_memoria(calc.cargar_historial(ruta)) == 7
    conteos = calc.obtener_estadisticas(historial)
    assert conteos["Suma"] == 7 and sum(conteos.values()) == 7
    salida = StringIO()
    with redirect_stdout(salida), patch("builtins.input", return_value="2"):
        calc.mostrar_historial(historial)
    assert "0 + 1 =" not in salida.getvalue() and "2 + 1 = 3" in salida.getvalue()
    original = ruta.read_bytes()
    with patch("pathlib.Path.replace", side_effect=OSError("Fallo simulado")):
        esperar_error(calc.registrar_operacion, (historial, "Resta", "9 - 1", 8, ruta), OSError)
    assert ruta.read_bytes() == original and len(historial) == 7
    with patch("builtins.input", return_value="NO"):
        calc.borrar_historial(historial, ruta)
    assert ruta.read_bytes() == original
    with patch("builtins.input", return_value="SI"):
        calc.borrar_historial(historial, ruta)
    assert calc.cargar_historial(ruta) == [] and calc.obtener_memoria(historial) is None
    assert sum(calc.obtener_estadisticas(historial).values()) == 0
    for contenido in ("malformado\n", "2026-11-23 12:00:00|Suma|1 + 2|nan\n"):
        ruta.write_text(contenido, encoding="utf-8")
        esperar_error(calc.cargar_historial, (ruta,), ValueError)
        assert ruta.read_text(encoding="utf-8") == contenido


def probar_movimientos_banco(carpeta):
    cuenta = banco.crear_cuenta()
    ruta = carpeta / "movimientos.txt"
    movimientos, saldo = banco.cargar_movimientos(ruta, 1000)
    assert movimientos == [] and saldo == 1000
    assert banco.calcular_resumen([])["promedio_depositos"] == 0
    assert not banco.generar_comprobante(cuenta, [], carpeta / "vacio.txt")
    assert not (carpeta / "vacio.txt").exists()
    banco.registrar_movimiento(cuenta, movimientos, "Depósito", 500, ruta)
    banco.registrar_movimiento(cuenta, movimientos, "Retiro", 200, ruta)
    assert cuenta["saldo"] == 1300
    assert banco.cargar_movimientos(ruta, 1000) == (movimientos, 1300)
    for cantidad in (0, -1, 1.5, True):
        esperar_error(banco.registrar_movimiento, (cuenta, movimientos, "Depósito", cantidad, ruta), ValueError)
    esperar_error(banco.registrar_movimiento, (cuenta, movimientos, "Retiro", 1301, ruta), ValueError)
    assert len(banco.filtrar_movimientos(movimientos, "Depósito")) == 1
    assert len(banco.filtrar_movimientos(movimientos, "Retiro")) == 1
    for opcion, esperado, ausente in (("3", "$500 MXN", "$200 MXN"), ("4", "$200 MXN", "$500 MXN")):
        salida = StringIO()
        with redirect_stdout(salida), patch("builtins.input", return_value=opcion):
            banco.mostrar_movimientos(movimientos)
        assert esperado in salida.getvalue() and ausente not in salida.getvalue()
    siete_movimientos = []
    for indice in range(7):
        siete_movimientos.append(("Depósito", 101 + indice, "2026-11-23", "12:00:00", 2000 + indice))
    salida = StringIO()
    with redirect_stdout(salida), patch("builtins.input", return_value="2"):
        banco.mostrar_movimientos(siete_movimientos)
    assert "$101 MXN" not in salida.getvalue() and "$103 MXN" in salida.getvalue()
    resumen = banco.calcular_resumen(movimientos)
    assert resumen == {"total_depositado": 500, "total_retirado": 200, "movimientos": 2,
                       "depositos": 1, "retiros": 1, "mayor_deposito": 500, "mayor_retiro": 200,
                       "promedio_depositos": 500, "promedio_retiros": 200}
    assert banco.proyectar_ahorro(cuenta["saldo"], 100, 3) == [(1, 1400), (2, 1500), (3, 1600)]
    assert cuenta["saldo"] == 1300
    esperar_error(banco.proyectar_ahorro, (1300, 0, 3), ValueError)
    esperar_error(banco.proyectar_ahorro, (1300, 100, 0), ValueError)
    comprobante = carpeta / "comprobante.txt"
    assert banco.generar_comprobante(cuenta, movimientos, comprobante)
    texto = comprobante.read_text(encoding="utf-8")
    for dato in ("PYTHON BANK", "Juan Pérez", "00012345", "Retiro", "$200 MXN", "$1,300 MXN"):
        assert dato in texto
    assert "1234" not in texto.replace("00012345", "")
    original = ruta.read_bytes()
    for funcion in (banco.depositar, banco.retirar):
        with patch("builtins.input", side_effect=["100", "NO"]):
            funcion(cuenta, movimientos, ruta)
    assert ruta.read_bytes() == original and cuenta["saldo"] == 1300
    with patch("pathlib.Path.replace", side_effect=OSError("Fallo simulado")):
        esperar_error(banco.registrar_movimiento, (cuenta, movimientos, "Depósito", 100, ruta), OSError)
    with patch("builtins.open", side_effect=OSError("Fallo de escritura simulado")):
        esperar_error(banco.registrar_movimiento, (cuenta, movimientos, "Retiro", 100, ruta), OSError)
    assert ruta.read_bytes() == original and cuenta["saldo"] == 1300 and len(movimientos) == 2
    assert not ruta.with_name(ruta.name + ".tmp").exists()
    banco.registrar_movimiento(cuenta, movimientos, "Retiro", 1300, ruta)
    assert cuenta["saldo"] == 0
    for contenido in ("basura\n", "Depósito|500|2026-11-23|12:00:00|9999\n",
                      "Retiro|1001|2026-11-23|12:00:00|-1\n",
                      "Depósito|-1|2026-11-23|12:00:00|999\n"):
        ruta.write_text(contenido, encoding="utf-8")
        esperar_error(banco.cargar_movimientos, (ruta, 1000), ValueError)
        assert ruta.read_text(encoding="utf-8") == contenido


def probar_consola_calculadora(carpeta):
    destino = carpeta / "Calculadora"
    destino.mkdir()
    programa = destino / "calculadora.py"
    shutil.copy2(calc.__file__, programa)
    entradas = ["13", "14", "15", "99", "abc"]
    for opcion in range(1, 10):
        entradas.extend([str(opcion), "9"])
        if opcion != 8:
            entradas.append("2")
    entradas.extend(["4", "1", "0", "5", "1", "0", "6", "1", "0", "8", "-9",
                     "7", "-2", "0.5", "7", "1e308", "2", "3", "1e308", "10",
                     "1", "abc", "nan", "inf", "M", "1",
                     "10", "7", "11", "2", "3", "12", "0", "3", "1", "2", "3",
                     "13", "1", "13", "2", "14", "15", "0"])
    salida = ejecutar_consola(programa, entradas, carpeta)
    for texto in ("historial está vacío", "Opción inexistente", "Resultado: 11", "entre cero",
                  "negativas", "exponente entero", "finito", "7 x 10 = 70", "3 es mayor",
                  "Promedio: 2.0", "Total de cálculos: 10", "Memoria: 1.18"):
        assert texto in salida, (texto, salida)
    historial = calc.cargar_historial(destino / "historial_calculadora.txt")
    assert len(historial) == 10
    salida = ejecutar_consola(programa, ["15", "14", "0"], carpeta)
    assert "Memoria: 1.18" in salida and "Total de cálculos: 10" in salida
    salida = ejecutar_consola(programa, ["16", "NO", "14", "16", "SI", "15", "14", "0"], carpeta)
    assert "Eliminación cancelada" in salida and "Total de cálculos: 0" in salida
    assert calc.cargar_historial(destino / "historial_calculadora.txt") == []
    (destino / "historial_calculadora.txt").write_text("inválido\n", encoding="utf-8")
    assert "No se puede abrir" in ejecutar_consola(programa, [], carpeta)


def probar_consola_banco(carpeta):
    destino = carpeta / "Cajero"
    destino.mkdir()
    programa = destino / "cajero.py"
    shutil.copy2(banco.__file__, programa)
    salida = ejecutar_consola(programa, ["mal", "0", "mal", "0", "mal", "0"], carpeta)
    assert "Intentos restantes: 0" in salida and "Menú principal" not in salida
    entradas = ["mal", "0", "cliente01", "1234", "1", "4", "6", "8", "99", "abc",
                "2", "abc", "-5", "0", "1.5", "500", "NO", "2", "500", "SI",
                "3", "9999", "3", "200", "NO", "3", "200", "SI", "5",
                "4", "1", "4", "2", "4", "3", "4", "4", "4", "99", "6",
                "7", "0", "-1", "abc", "100", "0", "2", "1", "8", "9", "cliente01", "1234", "1", "0"]
    salida = ejecutar_consola(programa, entradas, carpeta)
    for texto in ("Credenciales incorrectas", "Todavía no hay movimientos", "No hay movimientos para",
                  "Opción inexistente", "Depósito cancelado", "Retiro cancelado", "Fondos insuficientes",
                  "Depósito realizado y guardado", "Retiro realizado y guardado", "Total depositado: $500 MXN",
                  "Saldo final proyectado: $1,500 MXN", "Sesión cerrada", "Saldo disponible: $1,300 MXN"):
        assert texto in salida, (texto, salida)
    movimientos, saldo = banco.cargar_movimientos(destino / "movimientos.txt", 1000)
    assert len(movimientos) == 2 and saldo == 1300
    assert (destino / "comprobante.txt").exists()
    salida = ejecutar_consola(programa, ["cliente01", "1234", "1", "0"], carpeta)
    assert "Saldo disponible: $1,300 MXN" in salida
    (destino / "movimientos.txt").write_text("inválido\n", encoding="utf-8")
    assert "Acceso detenido" in ejecutar_consola(programa, [], carpeta)
    assert not (carpeta / "movimientos.txt").exists()
    assert not (carpeta / "historial_calculadora.txt").exists()


def main():
    with TemporaryDirectory(prefix="proyecto_estructurada_") as temporal:
        carpeta = Path(temporal)
        unidades = carpeta / "pruebas_funciones"
        unidades.mkdir()
        # Se captura la salida de las funciones para mostrar solo resultados de prueba.
        with redirect_stdout(StringIO()):
            probar_calculos()
            probar_entradas()
            probar_historial_calculadora(unidades)
            probar_movimientos_banco(unidades)
            probar_consola_calculadora(carpeta)
            probar_consola_banco(carpeta)
    print("6 grupos de pruebas aprobados: cálculos, entradas, historial, banco y ambas consolas.")
    print("Datos aislados y eliminados automáticamente. No se modificaron los TXT de uso normal.")


if __name__ == "__main__":
    main()
