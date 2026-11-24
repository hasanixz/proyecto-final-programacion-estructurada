"""Calculadora de consola para practicar programación estructurada."""

from datetime import datetime
from pathlib import Path
import math


ARCHIVO_HISTORIAL = Path(__file__).resolve().parent / "historial_calculadora.txt"
OPERACIONES = (
    "Suma", "Resta", "Multiplicación", "División", "División entera",
    "Módulo", "Potencia", "Raíz cuadrada", "Porcentaje",
)


def sumar(a, b):
    return a + b


def restar(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        raise ValueError("No se puede dividir entre cero.")
    return a / b


def division_entera(a, b):
    if b == 0:
        raise ValueError("No se puede dividir entre cero.")
    return a // b


def calcular_modulo(a, b):
    if b == 0:
        raise ValueError("No se puede calcular el módulo entre cero.")
    return a % b


def calcular_potencia(a, b):
    if a == 0 and b < 0:
        raise ValueError("Cero no admite exponentes negativos.")
    if a < 0 and b != int(b):
        raise ValueError("Una base negativa requiere un exponente entero.")
    return a ** b


def raiz_cuadrada(numero):
    if numero < 0:
        raise ValueError("No se admiten raíces cuadradas negativas.")
    return math.sqrt(numero)


def calcular_porcentaje(numero, porcentaje):
    return numero * (porcentaje / 100)


def validar_resultado(resultado):
    """Rechaza resultados fuera del dominio real finito utilizado."""
    if not math.isfinite(resultado):
        raise ValueError("El resultado es demasiado grande o no es finito.")
    return resultado


def pedir_numero(mensaje, memoria=None):
    """Lee un float finito; M reutiliza la memoria si está disponible."""
    while True:
        entrada = input(mensaje + " (M = memoria): ").strip()
        if entrada.upper() == "M":
            if memoria is None:
                print("Todavía no existe un resultado en memoria.")
                continue
            return memoria
        try:
            numero = float(entrada)
            return validar_resultado(numero)
        except (ValueError, OverflowError):
            print("Ingresa un número real finito; usa punto para los decimales.")


def pedir_entero_positivo(mensaje):
    while True:
        try:
            numero = int(input(mensaje))
            if numero > 0:
                return numero
        except ValueError:
            pass
        print("Ingresa un número entero mayor que cero.")


def cargar_historial(ruta):
    """Recupera tuplas (fecha y hora, tipo, expresión, resultado)."""
    historial = []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                partes = linea.rstrip("\n").split("|")
                try:
                    if len(partes) != 4:
                        raise ValueError("Se esperaban cuatro campos.")
                    fecha, tipo, expresion, texto_resultado = partes
                    datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
                    resultado = validar_resultado(float(texto_resultado))
                    if tipo not in OPERACIONES or not expresion:
                        raise ValueError("Operación desconocida o expresión vacía.")
                    historial.append((fecha, tipo, expresion, resultado))
                except ValueError as error:
                    raise ValueError(f"Historial inválido en línea {numero_linea}: {error}") from error
    except FileNotFoundError:
        return []
    return historial


def guardar_historial(ruta, historial):
    """Prepara el TXT completo y lo sustituye solo si la escritura termina."""
    temporal = ruta.with_name(ruta.name + ".tmp")
    try:
        with open(temporal, "w", encoding="utf-8") as archivo:
            for fecha, tipo, expresion, resultado in historial:
                archivo.write(f"{fecha}|{tipo}|{expresion}|{resultado}\n")
        temporal.replace(ruta)
    finally:
        if temporal.exists():
            temporal.unlink()


def registrar_operacion(historial, tipo, expresion, resultado, ruta):
    """Guarda antes de modificar la lista para mantener memoria y TXT coherentes."""
    validar_resultado(resultado)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    registro = (fecha, tipo, expresion, resultado)
    guardar_historial(ruta, historial + [registro])
    historial.append(registro)


def obtener_memoria(historial):
    if historial:
        return historial[-1][3]
    return None


def realizar_operacion(opcion, historial, ruta):
    """Solicita operandos, calcula y registra únicamente resultados válidos."""
    memoria = obtener_memoria(historial)
    a = pedir_numero("Primer número", memoria)
    b = None
    if opcion != 8:
        mensaje = "Porcentaje" if opcion == 9 else "Segundo número"
        b = pedir_numero(mensaje, memoria)
    if opcion == 1:
        resultado = sumar(a, b)
        expresion = f"{a} + {b}"
    elif opcion == 2:
        resultado = restar(a, b)
        expresion = f"{a} - {b}"
    elif opcion == 3:
        resultado = multiplicar(a, b)
        expresion = f"{a} * {b}"
    elif opcion == 4:
        resultado = dividir(a, b)
        expresion = f"{a} / {b}"
    elif opcion == 5:
        resultado = division_entera(a, b)
        expresion = f"{a} // {b}"
    elif opcion == 6:
        resultado = calcular_modulo(a, b)
        expresion = f"{a} % {b}"
    elif opcion == 7:
        resultado = calcular_potencia(a, b)
        expresion = f"{a} ** {b}"
    elif opcion == 8:
        resultado = raiz_cuadrada(a)
        expresion = f"raíz de {a}"
    else:
        resultado = calcular_porcentaje(a, b)
        expresion = f"{b}% de {a}"
    validar_resultado(resultado)
    registrar_operacion(historial, OPERACIONES[opcion - 1], expresion, resultado, ruta)
    print(f"Resultado: {resultado:g}. Operación guardada.")


def tabla_multiplicar(numero):
    """Construye una lista de tuplas con los diez productos."""
    tabla = []
    for multiplicador in range(1, 11):
        resultado = validar_resultado(numero * multiplicador)
        tabla.append((multiplicador, resultado))
    return tabla


def comparar_numeros(a, b):
    if a == b:
        return "Los números son iguales."
    elif a > b:
        return f"Son diferentes: {a:g} es mayor y {b:g} es menor."
    return f"Son diferentes: {b:g} es mayor y {a:g} es menor."


def analizar_lista(numeros):
    """Devuelve estadísticas sin imprimir ni modificar la lista recibida."""
    if not numeros:
        raise ValueError("La lista no puede estar vacía.")
    total = validar_resultado(sum(numeros))
    promedio = total / len(numeros)
    return {
        "Suma": total, "Promedio": promedio,
        "Mayor": max(numeros), "Menor": min(numeros),
        "Superiores al promedio": [numero for numero in numeros if numero > promedio],
        "Valores únicos": set(numeros),
    }


def analizar_numeros(memoria):
    cantidad = pedir_entero_positivo("¿Cuántos números deseas analizar? ")
    numeros = []
    for indice in range(cantidad):
        numeros.append(pedir_numero(f"Número {indice + 1}", memoria))
    resumen = analizar_lista(numeros)
    print(f"Lista: {numeros}")
    for nombre, valor in resumen.items():
        print(f"{nombre}: {valor}")


def mostrar_historial(historial):
    if not historial:
        print("El historial está vacío.")
        return
    opcion = input("1. Completo | 2. Últimas cinco: ").strip()
    if opcion == "1":
        seleccion = historial
    elif opcion == "2":
        seleccion = historial[-5:]  # Slicing: no modifica el historial original.
    else:
        print("Opción inexistente.")
        return
    print(f"{'Fecha y hora':19}  {'Operación':16}  Expresión = resultado")
    for fecha, tipo, expresion, resultado in seleccion:
        print(f"{fecha:19}  {tipo:16}  {expresion} = {resultado:g}")


def obtener_estadisticas(historial):
    conteos = {}
    for tipo in OPERACIONES:
        conteos[tipo] = 0
    for registro in historial:
        conteos[registro[1]] += 1
    return conteos


def mostrar_estadisticas(historial):
    conteos = obtener_estadisticas(historial)
    utilizados = set()
    for tipo, cantidad in conteos.items():
        print(f"{tipo:18}: {cantidad}")
        if cantidad > 0:
            utilizados.add(tipo)
    print(f"Total de cálculos: {sum(conteos.values())}")
    if utilizados:
        mayor = max(conteos.values())
        frecuentes = [tipo for tipo, cantidad in conteos.items() if cantidad == mayor]
        print("Más utilizadas (incluye empates): " + ", ".join(frecuentes))
    else:
        print("Todavía no hay una operación más utilizada.")
    print("Tipos utilizados: " + (", ".join(sorted(utilizados)) or "ninguno"))
    pendientes = set(OPERACIONES) - utilizados
    print("Sin utilizar: " + (", ".join(sorted(pendientes)) or "ninguna"))


def borrar_historial(historial, ruta):
    if input("¿Borrar todo el historial y la memoria? Escribe SI: ").strip().upper() != "SI":
        print("Eliminación cancelada.")
        return
    guardar_historial(ruta, [])
    historial.clear()
    print("Historial, estadísticas y memoria reiniciados.")


def mostrar_menu():
    print("\n" + "=" * 48 + "\n         CALCULADORA MULTIFUNCIONAL\n" + "=" * 48)
    for indice, tipo in enumerate(OPERACIONES, start=1):
        print(f"{indice:2}. {tipo}")
    print("10. Tabla de multiplicar\n11. Comparar dos números\n12. Analizar una lista")
    print("13. Consultar historial\n14. Estadísticas de uso\n15. Memoria del último resultado")
    print("16. Borrar historial\n 0. Salir")


def main():
    """Carga los datos y mantiene el menú hasta que el usuario sale."""
    print("Bienvenido a la calculadora. Los datos se guardan junto al programa.")
    try:
        historial = cargar_historial(ARCHIVO_HISTORIAL)
    except (OSError, ValueError, UnicodeError) as error:
        print(f"No se puede abrir el historial: {error}")
        print("Revisa el archivo antes de continuar; no se modificó su contenido.")
        return
    while True:
        try:
            mostrar_menu()
            opcion = input("Selecciona una opción: ").strip()
            memoria = obtener_memoria(historial)
            if opcion in [str(numero) for numero in range(1, 10)]:
                realizar_operacion(int(opcion), historial, ARCHIVO_HISTORIAL)
            elif opcion == "10":
                numero = pedir_numero("Número de la tabla", memoria)
                for multiplicador, producto in tabla_multiplicar(numero):
                    print(f"{numero:g} x {multiplicador:2} = {producto:g}")
            elif opcion == "11":
                a = pedir_numero("Primer número", memoria)
                b = pedir_numero("Segundo número", memoria)
                print(comparar_numeros(a, b))
            elif opcion == "12":
                analizar_numeros(memoria)
            elif opcion == "13":
                mostrar_historial(historial)
            elif opcion == "14":
                mostrar_estadisticas(historial)
            elif opcion == "15":
                if memoria is None:
                    print("Todavía no existe un resultado en memoria.")
                else:
                    print(f"Memoria: {memoria:g}. Escribe M al solicitar un número para reutilizarla.")
            elif opcion == "16":
                borrar_historial(historial, ARCHIVO_HISTORIAL)
            elif opcion == "0":
                break
            else:
                print("Opción inexistente.")
        except (ValueError, OverflowError) as error:
            print(f"No se realizó el cálculo: {error}")
        except OSError as error:
            print(f"No se pudo guardar el cambio: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada interrumpida.")
            break
    print("Gracias por utilizar la calculadora. ¡Hasta pronto!")


if __name__ == "__main__":
    main()
