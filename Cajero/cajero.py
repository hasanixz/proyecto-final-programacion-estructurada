"""Python Bank: simulación académica con pesos enteros y persistencia TXT."""

from datetime import datetime
from pathlib import Path


CARPETA = Path(__file__).resolve().parent
ARCHIVO_MOVIMIENTOS = CARPETA / "movimientos.txt"
ARCHIVO_COMPROBANTE = CARPETA / "comprobante.txt"


def crear_cuenta():
    """Crea datos ficticios nuevos en cada ejecución; el TXT recupera el saldo."""
    return {
        "titular": "Juan Pérez", "usuario": "cliente01", "nip": "1234",
        "numero": "00012345", "tipo": "Ahorros", "moneda": "MXN",
        "saldo_inicial": 1000, "saldo": 1000, "estado": "Activa",
    }


def formato_pesos(cantidad):
    return f"${cantidad:,} MXN"


def iniciar_sesion(cuenta):
    """Devuelve True al autenticar y False después de tres intentos fallidos."""
    print("\n" + "=" * 48 + "\n           PYTHON BANK — Acceso\n" + "=" * 48)
    print("Cuenta ficticia de demostración. No es seguridad bancaria real.")
    for intento in range(1, 4):
        usuario = input("Usuario: ").strip()
        nip = input("NIP: ").strip()
        if usuario == cuenta["usuario"] and nip == cuenta["nip"]:
            print(f"Bienvenido, {cuenta['titular']}.")
            return True
        print(f"Credenciales incorrectas. Intentos restantes: {3 - intento}")
    print("Acceso finalizado después de tres intentos incorrectos.")
    return False


def pedir_cantidad(mensaje):
    """Solo admite enteros positivos, sin decimales ni separadores de miles."""
    while True:
        try:
            cantidad = int(input(mensaje))
            if cantidad > 0:
                return cantidad
        except ValueError:
            pass
        print("Ingresa una cantidad entera mayor que cero, sin comas ni decimales.")


def cargar_movimientos(ruta, saldo_inicial):
    """Valida cada movimiento y la continuidad del saldo; no repara datos."""
    movimientos = []
    saldo = saldo_inicial
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                partes = linea.rstrip("\n").split("|")
                try:
                    if len(partes) != 5:
                        raise ValueError("Se esperaban cinco campos.")
                    tipo, texto_cantidad, fecha, hora, texto_saldo = partes
                    cantidad = int(texto_cantidad)
                    saldo_registrado = int(texto_saldo)
                    datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M:%S")
                    if tipo not in ("Depósito", "Retiro") or cantidad <= 0:
                        raise ValueError("Tipo o cantidad inválidos.")
                    if tipo == "Depósito":
                        saldo_esperado = saldo + cantidad
                    else:
                        saldo_esperado = saldo - cantidad
                    if saldo_esperado < 0 or saldo_registrado != saldo_esperado:
                        raise ValueError("El saldo no coincide con los movimientos.")
                    movimientos.append((tipo, cantidad, fecha, hora, saldo_registrado))
                    saldo = saldo_registrado
                except ValueError as error:
                    raise ValueError(f"Movimientos inválidos en línea {numero_linea}: {error}") from error
    except FileNotFoundError:
        return [], saldo_inicial
    return movimientos, saldo


def guardar_movimientos(ruta, movimientos):
    """Escribe una copia temporal y sustituye el TXT al terminar correctamente."""
    temporal = ruta.with_name(ruta.name + ".tmp")
    try:
        with open(temporal, "w", encoding="utf-8") as archivo:
            for tipo, cantidad, fecha, hora, saldo in movimientos:
                archivo.write(f"{tipo}|{cantidad}|{fecha}|{hora}|{saldo}\n")
        temporal.replace(ruta)
    finally:
        if temporal.exists():
            temporal.unlink()


def registrar_movimiento(cuenta, movimientos, tipo, cantidad, ruta):
    """Valida y guarda primero; solo después actualiza saldo e historial."""
    if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
        raise ValueError("La cantidad debe ser un entero positivo.")
    if tipo == "Depósito":
        nuevo_saldo = cuenta["saldo"] + cantidad
    elif tipo == "Retiro":
        if cantidad > cuenta["saldo"]:
            raise ValueError("Fondos insuficientes.")
        nuevo_saldo = cuenta["saldo"] - cantidad
    else:
        raise ValueError("Tipo de movimiento desconocido.")
    ahora = datetime.now()
    movimiento = (tipo, cantidad, ahora.strftime("%Y-%m-%d"), ahora.strftime("%H:%M:%S"), nuevo_saldo)
    guardar_movimientos(ruta, movimientos + [movimiento])
    movimientos.append(movimiento)
    cuenta["saldo"] = nuevo_saldo
    return movimiento


def consultar_saldo(cuenta):
    print(f"Saldo disponible: {formato_pesos(cuenta['saldo'])}")


def depositar(cuenta, movimientos, ruta):
    cantidad = pedir_cantidad("Cantidad a depositar (pesos enteros): ")
    if input(f"¿Depositar {formato_pesos(cantidad)}? Escribe SI: ").strip().upper() != "SI":
        print("Depósito cancelado.")
        return
    registrar_movimiento(cuenta, movimientos, "Depósito", cantidad, ruta)
    print("Depósito realizado y guardado.")
    consultar_saldo(cuenta)


def retirar(cuenta, movimientos, ruta):
    cantidad = pedir_cantidad("Cantidad a retirar (pesos enteros): ")
    if cantidad > cuenta["saldo"]:
        print("Fondos insuficientes. No se realizó el retiro.")
        return
    if input(f"¿Retirar {formato_pesos(cantidad)}? Escribe SI: ").strip().upper() != "SI":
        print("Retiro cancelado.")
        return
    registrar_movimiento(cuenta, movimientos, "Retiro", cantidad, ruta)
    print("Retiro realizado y guardado.")
    consultar_saldo(cuenta)


def filtrar_movimientos(movimientos, tipo):
    return [movimiento for movimiento in movimientos if movimiento[0] == tipo]


def mostrar_movimientos(movimientos):
    if not movimientos:
        print("Todavía no hay movimientos.")
        return
    opcion = input("1. Todos | 2. Últimos cinco | 3. Depósitos | 4. Retiros: ").strip()
    if opcion == "1":
        seleccion = movimientos
    elif opcion == "2":
        seleccion = movimientos[-5:]
    elif opcion == "3":
        seleccion = filtrar_movimientos(movimientos, "Depósito")
    elif opcion == "4":
        seleccion = filtrar_movimientos(movimientos, "Retiro")
    else:
        print("Opción inexistente.")
        return
    print(f"{'Tipo':10} {'Cantidad':18} {'Fecha':10} {'Hora':8} {'Saldo':18}")
    tipos = set()
    for tipo, cantidad, fecha, hora, saldo in seleccion:
        tipos.add(tipo)
        print(f"{tipo:10} {formato_pesos(cantidad):18} {fecha:10} {hora:8} {formato_pesos(saldo):18}")
    if not seleccion:
        print("No hay movimientos de ese tipo.")
    print("Tipos en esta consulta: " + (", ".join(sorted(tipos)) or "ninguno"))


def mostrar_datos_cuenta(cuenta):
    # El diccionario para presentación excluye expresamente las credenciales.
    datos = {
        "Titular": cuenta["titular"], "Número de cuenta": cuenta["numero"],
        "Tipo": cuenta["tipo"], "Moneda": cuenta["moneda"],
        "Estado": cuenta["estado"], "Saldo": formato_pesos(cuenta["saldo"]),
    }
    for nombre, valor in datos.items():
        print(f"{nombre:18}: {valor}")


def calcular_resumen(movimientos):
    """Usa acumuladores y listas para obtener totales, máximos y promedios."""
    depositos = []
    retiros = []
    total_depositado = 0
    total_retirado = 0
    for tipo, cantidad, fecha, hora, saldo in movimientos:
        if tipo == "Depósito":
            depositos.append(cantidad)
            total_depositado += cantidad
        else:
            retiros.append(cantidad)
            total_retirado += cantidad
    resumen = {
        "total_depositado": total_depositado, "total_retirado": total_retirado,
        "movimientos": len(movimientos), "depositos": len(depositos), "retiros": len(retiros),
        "mayor_deposito": 0, "mayor_retiro": 0, "promedio_depositos": 0, "promedio_retiros": 0,
    }
    if depositos:
        resumen["mayor_deposito"] = max(depositos)
        resumen["promedio_depositos"] = total_depositado / len(depositos)
    if retiros:
        resumen["mayor_retiro"] = max(retiros)
        resumen["promedio_retiros"] = total_retirado / len(retiros)
    return resumen


def resumen_financiero(cuenta, movimientos):
    resumen = calcular_resumen(movimientos)
    print(f"Saldo inicial: {formato_pesos(cuenta['saldo_inicial'])}")
    consultar_saldo(cuenta)
    print(f"Total depositado: {formato_pesos(resumen['total_depositado'])}")
    print(f"Total retirado: {formato_pesos(resumen['total_retirado'])}")
    print(f"Movimientos: {resumen['movimientos']} | Depósitos: {resumen['depositos']} | Retiros: {resumen['retiros']}")
    print(f"Depósito mayor: {formato_pesos(resumen['mayor_deposito'])}")
    print(f"Retiro mayor: {formato_pesos(resumen['mayor_retiro'])}")
    print(f"Promedio de depósitos: ${resumen['promedio_depositos']:,.2f} MXN")
    print(f"Promedio de retiros: ${resumen['promedio_retiros']:,.2f} MXN")
    print("Si no hay movimientos de un tipo, su máximo y promedio se muestran como 0.")


def proyectar_ahorro(saldo, cantidad_mensual, meses):
    """Devuelve pares (mes, saldo proyectado) sin alterar la cuenta."""
    if cantidad_mensual <= 0 or meses <= 0:
        raise ValueError("El ahorro mensual y los meses deben ser positivos.")
    proyeccion = []
    saldo_proyectado = saldo
    for mes in range(1, meses + 1):
        saldo_proyectado += cantidad_mensual
        proyeccion.append((mes, saldo_proyectado))
    return proyeccion


def simular_ahorro(cuenta):
    mensual = pedir_cantidad("Ahorro mensual (pesos enteros): ")
    meses = pedir_cantidad("Número de meses: ")
    proyeccion = proyectar_ahorro(cuenta["saldo"], mensual, meses)
    print("Proyección sin intereses ni comisiones; no modifica tu cuenta.")
    print(f"{'Mes':>5}  Saldo proyectado")
    for mes, saldo in proyeccion:
        print(f"{mes:5}  {formato_pesos(saldo)}")
    print(f"Saldo final proyectado: {formato_pesos(proyeccion[-1][1])}")


def generar_comprobante(cuenta, movimientos, ruta):
    if not movimientos:
        print("No hay movimientos para generar un comprobante.")
        return False
    tipo, cantidad, fecha, hora, saldo = movimientos[-1]
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("PYTHON BANK — COMPROBANTE ACADÉMICO\n")
        archivo.write(f"Titular: {cuenta['titular']}\nCuenta: {cuenta['numero']}\n")
        archivo.write(f"Fecha: {fecha}\nHora: {hora}\nTipo: {tipo}\n")
        archivo.write(f"Cantidad: {formato_pesos(cantidad)}\nSaldo resultante: {formato_pesos(saldo)}\n")
    print(f"Comprobante guardado en: {ruta}")
    return True


def mostrar_menu():
    print("\n" + "=" * 48 + "\n          PYTHON BANK — Menú principal\n" + "=" * 48)
    print("1. Consultar saldo\n2. Depositar dinero\n3. Retirar dinero\n4. Consultar movimientos")
    print("5. Consultar datos de mi cuenta\n6. Resumen financiero\n7. Simulador de ahorro")
    print("8. Generar comprobante\n9. Cerrar sesión\n0. Salir del programa")


def main():
    cuenta = crear_cuenta()
    try:
        movimientos, saldo = cargar_movimientos(ARCHIVO_MOVIMIENTOS, cuenta["saldo_inicial"])
        cuenta["saldo"] = saldo
    except (OSError, ValueError, UnicodeError) as error:
        print(f"No se puede cargar la cuenta: {error}")
        print("Acceso detenido. Revisa movimientos.txt; sus datos no se modificaron.")
        return
    sesion_activa = False
    while True:
        try:
            if not sesion_activa:
                sesion_activa = iniciar_sesion(cuenta)
                if not sesion_activa:
                    break
            mostrar_menu()
            opcion = input("Selecciona una opción: ").strip()
            if opcion == "1":
                consultar_saldo(cuenta)
            elif opcion == "2":
                depositar(cuenta, movimientos, ARCHIVO_MOVIMIENTOS)
            elif opcion == "3":
                retirar(cuenta, movimientos, ARCHIVO_MOVIMIENTOS)
            elif opcion == "4":
                mostrar_movimientos(movimientos)
            elif opcion == "5":
                mostrar_datos_cuenta(cuenta)
            elif opcion == "6":
                resumen_financiero(cuenta, movimientos)
            elif opcion == "7":
                simular_ahorro(cuenta)
            elif opcion == "8":
                generar_comprobante(cuenta, movimientos, ARCHIVO_COMPROBANTE)
            elif opcion == "9":
                sesion_activa = False
                print("Sesión cerrada. Regresando al inicio.")
            elif opcion == "0":
                break
            else:
                print("Opción inexistente.")
        except (ValueError, OverflowError) as error:
            print(f"No se realizó la operación: {error}")
        except OSError as error:
            print(f"No se pudo guardar el archivo: {error}. El saldo no cambió.")
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada interrumpida.")
            break
    print("Gracias por utilizar Python Bank. ¡Hasta pronto!")


if __name__ == "__main__":
    main()
