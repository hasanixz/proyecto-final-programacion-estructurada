# Arquitectura del proyecto

## Estado inicial y alcance

La carpeta inicial contenía únicamente `.git`, sin commits ni fuentes. No se encontró la skill solicitada `architecture.md` ni un `AGENTS.md` aplicable en las ubicaciones revisadas. Este documento describe las decisiones tomadas para el proyecto nuevo; no pretende reproducir instrucciones de una skill ausente.

## Organización

- `Calculadora/calculadora.py`: aplicación completa de calculadora.
- `Cajero/cajero.py`: aplicación completa de simulación bancaria.
- `pruebas.py`: pruebas aisladas de funciones y ejecución real de las dos consolas.
- `README.md`: ejecución, conceptos, diagramas, persistencia, pruebas y limitaciones.
- `GUIA_EXPOSICION.md`: explicación y secuencias de demostración.

Cada programa tiene su propio `main()` y no importa al otro. No se creó un módulo común: las pequeñas validaciones independientes permiten estudiar y ejecutar cada archivo por separado. Solo se utilizan funciones, condicionales, ciclos y estructuras nativas; no hay clases propias.

## Responsabilidades de las funciones

1. **Entrada y presentación:** menús, lectura con `input()`, confirmaciones y tablas con `print()`.
2. **Cálculo:** operaciones, análisis de listas, filtros, resumen y proyección. Retornan resultados para poder reutilizarlos y comprobarlos.
3. **Persistencia:** carga y validación de registros, preparación de archivos temporales y sustitución de TXT.
4. **Coordinación:** `main()` mantiene el menú y atiende errores. Las funciones de registro guardan antes de modificar las estructuras compartidas.

Las constantes globales solo contienen rutas y el catálogo de operaciones. La cuenta, el saldo y los historiales son variables locales que se pasan como parámetros. Las listas y diccionarios son mutables; las funciones que los actualizan lo explican en sus docstrings.

## Datos e invariantes

### Calculadora

- Catálogo fijo: tupla `OPERACIONES`.
- Historial: lista de tuplas `(fecha_hora, tipo, expresion, resultado)`.
- Solo se registran las nueve operaciones aritméticas con resultado real finito.
- Memoria: último resultado del historial, o `None` si está vacío.
- Estadísticas: diccionario calculado recorriendo el historial, sin un archivo adicional.
- Borrar requiere `SI`; el archivo vacío se guarda antes de vaciar la lista.

### Banco

- Cuenta: diccionario creado por `crear_cuenta()`; el número de cuenta y el NIP son cadenas para conservar ceros iniciales.
- Movimientos: lista de tuplas `(tipo, cantidad, fecha, hora, saldo_resultante)`.
- Dinero de las transacciones: enteros positivos; saldo nunca negativo.
- Saldo recuperado: $1,000 más depósitos menos retiros, verificando cada saldo registrado.
- Solo las funciones de registro cambian el saldo. La proyección utiliza una variable local y no registra movimientos.
- Un movimiento se confirma y se agrega a memoria únicamente después de guardarlo.
- El comprobante se deriva del último movimiento, no interviene en la recuperación de saldo.

## Archivos y errores

Las rutas parten de `Path(__file__).resolve().parent`. Los TXT usan UTF-8, `|` como separador y una línea por tupla. Las cadenas guardadas son generadas por el programa, por lo que no se necesitan reglas de escape para texto libre.

Para los dos historiales se escribe una copia completa en `nombre.txt.tmp` mediante modo `w`. Después de cerrar esa copia se usa `replace()` sobre el TXT principal. Un bloque `finally` retira el temporal si todavía existe. Se asume un solo proceso por aplicación y almacenamiento local ordinario.

Un archivo inexistente representa el primer uso. Un archivo existente con datos inválidos, codificación ilegible o errores de lectura detiene el arranque con un mensaje; no se sobrescribe para intentar repararlo. No hay migraciones automáticas ni eliminación de movimientos bancarios.

Las entradas inválidas se vuelven a solicitar o regresan al menú con un mensaje. `EOFError` y `KeyboardInterrupt` terminan la interacción de forma controlada. Los errores matemáticos no llegan al registro; los errores de archivo no confirman cambios de saldo.

## Convenciones y mantenimiento

- Español, nombres descriptivos en `snake_case`, cuatro espacios y docstrings breves.
- Evitar clases, frameworks, dependencias, `eval()`, `exec()`, lambdas y abstracciones que dificulten la exposición.
- Al agregar una operación, actualizar el menú, la función correspondiente, el catálogo, las pruebas y el README.
- Si cambia el formato TXT, documentar cómo se manejarán los archivos anteriores antes de implementar el cambio.
- Ejecutar `python pruebas.py` después de modificar validaciones, cálculos o persistencia.
- Mantener este documento, la guía y la tabla del README alineados con el código real.
